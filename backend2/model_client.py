"""
model_client.py
Backend 2 — calls Backend 1's detection service (ml/api/detection_service.py)
with a raw audio chunk and gets back the risk decision.
"""

import os
import httpx

# Configurable via environment variable so this isn't hardwired to one machine's
# setup - Docker, CI, or a teammate's local ports can all override this without
# touching code. Falls back to local-dev default if unset.
DETECTION_SERVICE_BASE_URL = os.environ.get("DETECTION_SERVICE_BASE_URL", "http://127.0.0.1:8000")
DETECTION_SERVICE_URL = f"{DETECTION_SERVICE_BASE_URL}/detect"
DETECTION_SERVICE_HEALTH_URL = f"{DETECTION_SERVICE_BASE_URL}/health"

async def score_chunk(audio_bytes: bytes, filename: str = "chunk.wav") -> dict:
    """
    Sends one audio chunk to Backend 1's /detect endpoint.
    Returns the partial decision object (fused_score, decision, explanation).
    Raises httpx.HTTPError on failure — caller should handle (e.g. mark 'unverified').
    """
    async with httpx.AsyncClient(timeout=15.0) as client:
        files = {"file": (filename, audio_bytes, "audio/wav")}
        response = await client.post(DETECTION_SERVICE_URL, files=files)
        response.raise_for_status()
        return response.json()


async def health_check() -> bool:
    """Confirm Backend 1's service is reachable before starting the pipeline."""
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(DETECTION_SERVICE_HEALTH_URL)
            return response.status_code == 200
    except httpx.HTTPError:
        return False