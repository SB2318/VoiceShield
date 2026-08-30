"""
backend2_service.py
Backend 2 — the actual FastAPI service exposing the pipeline to the outside
world: a WebSocket endpoint Frontend connects to (per useRiskStream.js),
streaming decision objects that match the team's shared contract exactly.

Runs on port 8002 (Backend 1's detection service owns 8000 - don't collide).
Frontend's SOCKET_URL should point to ws://localhost:8002/ws/risk-stream.

log_decision() below is a MOCK standing in for Backend 3's tamper-evident
hash-chain log, which hasn't been built yet - it returns a fake log_hash
so the contract shape is complete for Frontend/demo purposes. Swap this
for a real call to Backend 3's log-write API once it exists; nothing else
in this file needs to change.
"""

import asyncio
import hashlib
import wave
from datetime import datetime, timezone

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from audio_chunker import StreamChunker
from model_client import score_chunk
from risk_router import RiskRouter, Action
from challenge_engine import ChallengeEngine

app = FastAPI(title="VoiceShield Backend 2 - Real-Time Pipeline")

DEMO_CALL_ID = "demo-001"
DEMO_NUMBER = "+91 98765 43210"


def log_decision(decision_obj: dict) -> str:
    """
    MOCK for Backend 3's hash-chain log. Real version should POST this
    decision object to Backend 3's log-write API and return the real hash.
    This fake version just hashes the decision content so it's at least
    deterministic and unique per decision, not a random placeholder string.
    """
    raw = f"{decision_obj['call_id']}{decision_obj['timestamp']}{decision_obj['fused_score']}"
    return "0x" + hashlib.sha256(raw.encode()).hexdigest()[:12]


def build_decision_object(call_id, number, model_result, challenge_type="none",
                           challenge_result="not_triggered") -> dict:
    """Assembles a full decision object matching the team's Section 2 contract."""
    obj = {
        "call_id": call_id,
        "number": number,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "branch_scores": model_result.get("branch_scores", {"rawnet2": None, "spectrogram": None, "ssl": None}),
        "fused_score": model_result["fused_score"],
        "decision": model_result["decision"],
        "challenge_type": challenge_type,
        "challenge_result": challenge_result,
        "explanation": model_result["explanation"],
    }
    obj["log_hash"] = log_decision(obj)
    return obj


@app.websocket("/ws/risk-stream")
async def risk_stream(websocket: WebSocket):
    await websocket.accept()

    chunker = StreamChunker()
    router = RiskRouter(call_id=DEMO_CALL_ID)
    challenges = ChallengeEngine()
    pending_challenge_type = "none"
    pending_challenge_result = "not_triggered"

    try:
        with wave.open("test_sample.wav", "rb") as wf:
            sample_rate = wf.getframerate()
            chunk_frames = int(sample_rate * 0.1)

            while True:
                pcm_chunk = wf.readframes(chunk_frames)
                if not pcm_chunk:
                    wf.rewind()
                    continue  # loop the demo audio so the stream never ends

                chunker.add_audio(pcm_chunk)
                for audio_bytes, has_speech in chunker.get_ready_windows():
                    wav_bytes = chunker.pcm_to_wav_bytes(audio_bytes)
                    result = await score_chunk(wav_bytes)
                    action = router.route(result["decision"], result["fused_score"])

                    if action == Action.CHALLENGE and pending_challenge_type == "none":
                        challenge = challenges.generate()
                        pending_challenge_type = challenge.challenge_type
                        pending_challenge_result = "not_triggered"

                    decision_obj = build_decision_object(
                        DEMO_CALL_ID, DEMO_NUMBER, result,
                        challenge_type=pending_challenge_type,
                        challenge_result=pending_challenge_result,
                    )
                    await websocket.send_json(decision_obj)
                    await asyncio.sleep(0.3)   # matches Frontend's 200-500ms cadence

    except WebSocketDisconnect:
        pass


@app.get("/health")
async def health():
    return {"status": "ok", "service": "backend2-realtime-pipeline"}