"""
ivr_line.py
Backend 2 — toll-free IVR callback line (team plan Section 15.4 / step 8).

DEMO NOTE (be upfront about this if asked): a real toll-free IVR number
requires a paid telephony provider (Twilio/Exotel/etc - none offer a free
phone number, only free trial credits). This module simulates the exact
same call-and-response IVR experience over the terminal/CLI instead of a
real phone line, so the underlying logic - menu prompts, DTMF-style input,
running the verified-callback + detection pipeline, giving a verdict - is
100% real and reusable. Swapping in Twilio later means replacing only the
input/output layer (this file) with Twilio's <Gather>/<Say> webhooks; the
verified_callback.py and alert_orchestrator.py logic underneath needs zero
changes, since IVRLine calls them exactly the way a real webhook handler would.
"""

import asyncio
import wave

from verified_callback import VerifiedCallbackSession, CallbackState
from alert_orchestrator import CallSession


class IVRLine:
    """
    Simulates the toll-free verification line described in the plan:
    a person who received a suspicious call dials/opens this line, enters
    the number that called them, and the line calls that number back
    (via verified_callback's state machine) and runs full detection on it,
    then reports real / suspected_clone / unverified back to the caller -
    same output a WhatsApp bot reply or real IVR voice prompt would give.
    """

    def __init__(self, telephony_dial_fn=None, trusted_contact_notify_fn=None):
        self._dial_fn = telephony_dial_fn
        self._notify_fn = trusted_contact_notify_fn

    def play(self, text: str):
        """Stand-in for an IVR voice prompt (<Say> in Twilio terms)."""
        print(f"[IVR] {text}")

    async def handle_call(self, caller_reported_number: str, sample_audio_path: str = None):
        """
        Simulates a full IVR session:
          1. Greet, collect the suspicious number (normally via DTMF/keypad)
          2. Run the verified-callback flow against that number
          3. Feed the callback's audio through full detection
          4. Report the verdict back to the caller
        `sample_audio_path` stands in for the audio that would come back
        on the real callback leg - for the demo, this can be Backend 1's
        test data or a mocked clip.
        """
        self.play("Welcome to the VoiceShield verification line.")
        self.play(f"You reported a suspicious call from {caller_reported_number}.")
        self.play("Please hold while we verify this number...")

        session = VerifiedCallbackSession(
            call_id=f"ivr-{caller_reported_number}",
            claimed_number=caller_reported_number,
            telephony_dial_fn=self._dial_fn,
        )
        state = await session.end_original_and_callback()

        if state != CallbackState.CALLBACK_CONNECTED:
            self.play("We were unable to reach that number. Please try again later.")
            return {"call_id": session.call_id, "state": state.value, "decision": None}

        self.play("Connected. Running voice verification now...")

        call_session = CallSession(call_id=session.call_id, trusted_contact_notify_fn=self._notify_fn)
        last_decision = None

        if sample_audio_path:
            with wave.open(sample_audio_path, "rb") as wf:
                sample_rate = wf.getframerate()
                chunk_frames = int(sample_rate * 0.1)
                while True:
                    pcm_chunk = wf.readframes(chunk_frames)
                    if not pcm_chunk:
                        break
                    events = await call_session.process_audio(pcm_chunk)
                    for e in events:
                        if e["type"].value == "window_scored":
                            last_decision = e["decision"]

        passed = last_decision == "real"
        final_state = session.resolve_with_detection(callback_passed_detection=passed)

        if final_state == CallbackState.VERIFIED:
            self.play(f"Verification complete: this number appears legitimate ({last_decision}).")
        else:
            self.play(f"Warning: this number could not be verified ({last_decision}). "
                      f"Please do not share personal or financial information.")

        return {"call_id": session.call_id, "state": final_state.value, "decision": last_decision}