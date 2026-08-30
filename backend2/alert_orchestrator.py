"""
alert_orchestrator.py
Backend 2 — ties risk_router + challenge_engine + verified_callback into one
call-session flow, and implements the panic-aware response pieces from the
team plan (Section 5.10): trusted-contact silent escalation, and a cooldown
timer before any high-risk action is confirmed (never a hard auto-cut).

trusted_contact_notify_fn is an injected async function:
    async def notify_fn(call_id: str, reason: str) -> None
so this module doesn't need to know HOW the notification is sent (SMS/WhatsApp/
push) - Backend 3's WhatsApp bot or similar can be wired in here later without
touching this file, same pattern as verified_callback's telephony_dial_fn.
"""

import asyncio
from enum import Enum

from audio_chunker import StreamChunker
from model_client import score_chunk
from risk_router import RiskRouter, Action
from challenge_engine import ChallengeEngine, Challenge

COOLDOWN_SECONDS = 8   # per Section 5.10: brief cool-down before a high-risk action is confirmed


class SessionEvent(str, Enum):
    WINDOW_SCORED = "window_scored"
    CHALLENGE_ISSUED = "challenge_issued"
    CHALLENGE_RESOLVED = "challenge_resolved"
    COOLDOWN_STARTED = "cooldown_started"
    ESCALATED = "escalated"


class CallSession:
    """
    One instance per live call. Feed raw PCM audio in with process_audio();
    it drives chunking -> scoring -> routing, and returns a list of events
    describing what happened (for the Frontend/dashboard to render, and for
    Backend 3 to log). When a CHALLENGE action fires, the caller is expected
    to present challenge.prompt to the user and later call submit_challenge_response().
    """

    def __init__(self, call_id: str, trusted_contact_notify_fn=None):
        self.call_id = call_id
        self.chunker = StreamChunker()
        self.router = RiskRouter(call_id=call_id)
        self.challenges = ChallengeEngine()
        self._notify_fn = trusted_contact_notify_fn

        self._pending_challenge: Challenge | None = None
        self._in_cooldown = False

    async def process_audio(self, pcm_bytes: bytes) -> list[dict]:
        """Feed raw audio in; returns events for any windows that became ready."""
        events = []
        self.chunker.add_audio(pcm_bytes)

        for audio_bytes, has_speech in self.chunker.get_ready_windows():
            wav_bytes = self.chunker.pcm_to_wav_bytes(audio_bytes)
            result = await score_chunk(wav_bytes)

            action = self.router.route(result["decision"], result["fused_score"])
            events.append({
                "type": SessionEvent.WINDOW_SCORED,
                "decision": result["decision"],
                "fused_score": result["fused_score"],
                "explanation": result["explanation"],
                "action": action.value,
            })

            if action == Action.CHALLENGE and self._pending_challenge is None:
                challenge = self.challenges.generate()
                self._pending_challenge = challenge
                events.append({
                    "type": SessionEvent.CHALLENGE_ISSUED,
                    "challenge_type": challenge.challenge_type,
                    "prompt": challenge.prompt,
                })

            if action == Action.ESCALATE:
                escalate_events = await self._handle_escalation(result["explanation"])
                events.extend(escalate_events)

        return events

    async def submit_challenge_response(self, response_audio: bytes) -> list[dict]:
        """
        Call this once the user has responded to a challenge prompt
        (e.g. Frontend collected their audio response and passed it here).
        """
        if self._pending_challenge is None:
            return []

        result = self.challenges.score(self._pending_challenge, response_audio)
        challenge_type = self._pending_challenge.challenge_type
        self._pending_challenge = None

        action = self.router.route(decision="unverified", fused_score=0.5, challenge_result=result)

        events = [{
            "type": SessionEvent.CHALLENGE_RESOLVED,
            "challenge_type": challenge_type,
            "result": result,
            "action": action.value,
        }]

        if action == Action.ESCALATE:
            escalate_events = await self._handle_escalation(f"Failed {challenge_type} challenge")
            events.extend(escalate_events)

        return events

    async def _handle_escalation(self, reason: str) -> list[dict]:
        """
        Trusted-contact silent escalation + cooldown before any high-risk
        action is confirmed. Never auto-cuts the call - just notifies and waits.
        """
        events = [{"type": SessionEvent.COOLDOWN_STARTED, "seconds": COOLDOWN_SECONDS}]
        self._in_cooldown = True

        if self._notify_fn is not None:
            await self._notify_fn(self.call_id, reason)
        events.append({"type": SessionEvent.ESCALATED, "reason": reason})

        # cooldown runs in the background so audio processing isn't blocked;
        # a real implementation would let the Frontend show the countdown live
        asyncio.create_task(self._end_cooldown_after_delay())

        return events

    async def _end_cooldown_after_delay(self):
        await asyncio.sleep(COOLDOWN_SECONDS)
        self._in_cooldown = False