"""
risk_router.py
Backend 2 — maps per-window decisions to a tiered response action.

Tiered response per team plan (Section 5.10): flag -> challenge -> escalate.
Never a hard auto-cut of the call. Consecutive-window tracking prevents a
single noisy/uncertain window from over-triggering a challenge.
"""

from collections import deque
from enum import Enum


class Action(str, Enum):
    ALLOW = "allow"                # real, high confidence - no action
    FLAG = "flag"                  # unverified or borderline - UI badge only
    CHALLENGE = "challenge"        # suspected_clone / speaker_mismatch, or
                                    # repeated flags - trigger a liveness challenge
    ESCALATE = "escalate"          # challenge failed, or sustained high-risk -
                                    # trusted-contact silent escalation + cooldown


# How many consecutive risky windows before escalating tiers.
# Prevents one flaky window from triggering a challenge on the live call.
FLAG_STREAK_TO_CHALLENGE = 3
CHALLENGE_FAIL_TO_ESCALATE = 1   # a single failed challenge is enough to escalate

HIGH_RISK_DECISIONS = {"suspected_clone", "speaker_mismatch"}


class RiskRouter:
    """
    One instance per active call. Feed it each window's decision object
    (from model_client.score_chunk / Backend 1's response, plus any
    challenge_result once the liveness engine has run) and it returns
    the action to take next.
    """

    def __init__(self, call_id: str):
        self.call_id = call_id
        self._recent_decisions = deque(maxlen=FLAG_STREAK_TO_CHALLENGE)
        self._in_cooldown = False
        self._active_challenge = False

    def route(self, decision: str, fused_score: float, challenge_result: str = "not_triggered") -> Action:
        """
        decision: "real" | "unverified" | "suspected_clone" | "speaker_mismatch"
        fused_score: model's fused confidence score for this window
        challenge_result: "pass" | "fail" | "not_triggered" (once a challenge has run)
        """
        # A failed liveness challenge always escalates, regardless of window history.
        if challenge_result == "fail":
            self._active_challenge = False
            return Action.ESCALATE

        # A passed challenge clears the risky streak and allows the call to continue.
        if challenge_result == "pass":
            self._active_challenge = False
            self._recent_decisions.clear()
            return Action.ALLOW

        # High-risk decisions jump straight to a challenge (don't wait for a streak) -
        # these are specific, high-confidence risky classifications, not "unverified".
        if decision in HIGH_RISK_DECISIONS:
            self._active_challenge = True
            return Action.CHALLENGE

        self._recent_decisions.append(decision)

        if decision == "unverified":
            # Only escalate to a challenge after a sustained streak of uncertainty -
            # a single low-confidence window is just flagged, not acted on.
            streak_all_unverified = (
                len(self._recent_decisions) == FLAG_STREAK_TO_CHALLENGE
                and all(d == "unverified" for d in self._recent_decisions)
            )
            if streak_all_unverified and not self._active_challenge:
                self._active_challenge = True
                return Action.CHALLENGE
            return Action.FLAG

        # decision == "real"
        return Action.ALLOW

    def reset(self):
        """Call when a new call session starts, or after a full resolution."""
        self._recent_decisions.clear()
        self._active_challenge = False
        self._in_cooldown = False