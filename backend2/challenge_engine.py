"""
challenge_engine.py
Backend 2 — liveness challenge generation and scoring.

Three challenge types per team plan (Section 5.5 / Frontend spec):
  - phrase: repeat a short random phrase
  - acoustic: cough / laugh / hum on command
  - semantic: compositional instruction ("say the Nth word, then count backwards")

Speech-based challenges (phrase, semantic) use free Google Web Speech API via
the `speech_recognition` library - no API key required, works over the network.
The acoustic challenge (cough/laugh/hum) uses a simple energy/duration heuristic
as a hackathon-speed stand-in for a trained sound-event classifier - this is a
deliberate scope simplification (same pattern as the team's other honest scope
notes), and should be described as such if asked, not presented as production-grade
audio event detection.
"""

import random
import difflib
import io
import wave

try:
    import speech_recognition as sr
    _SR_AVAILABLE = True
except ImportError:
    _SR_AVAILABLE = False

CHALLENGE_PHRASES = [
    "the quick brown fox jumps over the lazy dog",
    "purple elephants dance under bright starlight",
    "seven silver spoons stir the warm soup",
    "banking apps should always protect your voice",
]

SEMANTIC_SENTENCES = [
    "the river flows quietly past the old mill",
    "green apples fell softly onto the grass",
    "morning light filled the quiet kitchen",
]


class Challenge:
    def __init__(self, challenge_type: str, prompt: str, expected: dict):
        self.challenge_type = challenge_type   # "phrase" | "acoustic" | "semantic"
        self.prompt = prompt                   # text shown to the user (Frontend renders this)
        self.expected = expected               # internal - what a correct response looks like


class ChallengeEngine:
    """
    Stateless generator + scorer. The RiskRouter decides *when* to challenge;
    this decides *what* the challenge is and *whether the response passes*.
    """

    def generate(self, challenge_type: str = None) -> Challenge:
        if challenge_type is None:
            challenge_type = random.choice(["phrase", "acoustic", "semantic"])

        if challenge_type == "phrase":
            phrase = random.choice(CHALLENGE_PHRASES)
            return Challenge(
                "phrase",
                prompt=f"Please repeat: \"{phrase}\"",
                expected={"phrase": phrase},
            )

        if challenge_type == "acoustic":
            action = random.choice(["cough", "laugh", "hum"])
            return Challenge(
                "acoustic",
                prompt=f"Please {action} into the microphone now.",
                expected={"action": action},
            )

        if challenge_type == "semantic":
            sentence = random.choice(SEMANTIC_SENTENCES)
            words = sentence.split()
            n = random.randint(2, min(4, len(words)))
            nth_word = words[n - 1]
            return Challenge(
                "semantic",
                prompt=(f"For the sentence \"{sentence}\", say word number {n}, "
                        f"then count backwards from five to one."),
                expected={"nth_word": nth_word, "countdown": ["five", "four", "three", "two", "one"]},
            )

        raise ValueError(f"Unknown challenge_type: {challenge_type}")

    def score(self, challenge: Challenge, audio_bytes: bytes) -> str:
        """
        Returns "pass" or "fail". audio_bytes should be a WAV file
        (use StreamChunker.pcm_to_wav_bytes if you have raw PCM).
        """
        if challenge.challenge_type == "acoustic":
            return self._score_acoustic(challenge, audio_bytes)

        transcript = self._transcribe(audio_bytes)
        if transcript is None:
            return "fail"   # couldn't transcribe -> treat as fail, safer default

        if challenge.challenge_type == "phrase":
            return self._score_phrase(challenge, transcript)

        if challenge.challenge_type == "semantic":
            return self._score_semantic(challenge, transcript)

        return "fail"

    def _transcribe(self, audio_bytes: bytes):
        if not _SR_AVAILABLE:
            return None
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                audio = recognizer.record(source)
            return recognizer.recognize_google(audio).lower()
        except (sr.UnknownValueError, sr.RequestError, Exception):
            return None

    def _score_phrase(self, challenge: Challenge, transcript: str) -> str:
        expected = challenge.expected["phrase"]
        similarity = difflib.SequenceMatcher(None, expected, transcript).ratio()
        return "pass" if similarity >= 0.75 else "fail"

    def _score_semantic(self, challenge: Challenge, transcript: str) -> str:
        tokens = transcript.split()
        expected_word = challenge.expected["nth_word"]
        expected_countdown = challenge.expected["countdown"]

        has_nth_word = expected_word in tokens
        countdown_hits = sum(1 for w in expected_countdown if w in tokens)
        countdown_ok = countdown_hits >= 4   # allow one mis-hear out of five

        return "pass" if (has_nth_word and countdown_ok) else "fail"

    def _score_acoustic(self, challenge: Challenge, audio_bytes: bytes) -> str:
        """
        Hackathon-speed heuristic, not a trained classifier: checks that the
        clip has enough energy and isn't silence/near-silence, as a stand-in
        for "the user made *some* deliberate sound". Does not distinguish
        cough vs laugh vs hum from each other - flagged as a known limitation.
        """
        try:
            with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
                frames = wf.readframes(wf.getnframes())
                if not frames:
                    return "fail"
                import array
                samples = array.array("h", frames)
                if len(samples) == 0:
                    return "fail"
                rms = (sum(s * s for s in samples) / len(samples)) ** 0.5
                return "pass" if rms > 300 else "fail"
        except Exception:
            return "fail"