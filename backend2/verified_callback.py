"""
verified_callback.py
Backend 2 — verified-callback pattern (team plan Section 13.1).

Core idea: when a call from an unverified/unknown number shows risk signals,
we don't trust anything further on that live line (attacker could stay
connected). Instead we end the original call and place a NEW outbound call
through our own trusted VoIP session to the claimed number, then run full
detection on that fresh, self-initiated connection.

This module models the state machine only. The actual "place outbound call"
action is a pluggable callback (telephony_dial_fn) - for the demo this can be
a mock/simulated dial; in production it would call the IVR line's telephony
provider (Twilio/Exotel), which is step 8 of the plan and reuses this same
state machine.
"""

from enum import Enum


class CallbackState(str, Enum):
    IDLE = "idle"
    ORIGINAL_ENDED = "original_ended"
    DIALING_BACK = "dialing_back"
    CALLBACK_CONNECTED = "callback_connected"
    CALLBACK_FAILED = "callback_failed"
    VERIFIED = "verified"          # callback connected + passed detection
    REJECTED = "rejected"          # callback failed, or detection failed on callback


class VerifiedCallbackSession:
    """
    One instance per call needing verification. `telephony_dial_fn` is an
    injected async function: async def dial_fn(number: str) -> bool
    (True = call connected, False = failed/no answer/busy). This keeps the
    state machine testable without a real telephony provider, and lets
    step 8 (IVR line) supply the real Twilio/Exotel dial function later.
    """

    def __init__(self, call_id: str, claimed_number: str, telephony_dial_fn=None):
        self.call_id = call_id
        self.claimed_number = claimed_number
        self.state = CallbackState.IDLE
        self._dial_fn = telephony_dial_fn

    async def end_original_and_callback(self) -> CallbackState:
        """
        Step 1: end the original (untrusted) call.
        Step 2: dial the claimed number ourselves via the injected telephony function.
        """
        self.state = CallbackState.ORIGINAL_ENDED
        self.state = CallbackState.DIALING_BACK

        if self._dial_fn is None:
            # No real telephony wired in yet (e.g. running before step 8 is built) -
            # simulate a successful connect so the rest of the pipeline can be tested.
            connected = True
        else:
            connected = await self._dial_fn(self.claimed_number)

        self.state = CallbackState.CALLBACK_CONNECTED if connected else CallbackState.CALLBACK_FAILED
        return self.state

    def resolve_with_detection(self, callback_passed_detection: bool) -> CallbackState:
        """
        Call this once full detection has run on the callback leg
        (i.e. the callback audio has gone through the normal
        chunker -> model_client -> risk_router pipeline and come out clean).
        """
        if self.state != CallbackState.CALLBACK_CONNECTED:
            self.state = CallbackState.REJECTED
            return self.state

        self.state = CallbackState.VERIFIED if callback_passed_detection else CallbackState.REJECTED
        return self.state