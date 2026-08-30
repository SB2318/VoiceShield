"""
test_chunker.py
Simulates a live audio stream by feeding test_sample.wav into StreamChunker
in small pieces, scores each ready window against Backend 1's model, and
routes each decision through the RiskRouter to see the action taken.
"""

import asyncio
import wave
from audio_chunker import StreamChunker
from model_client import score_chunk
from risk_router import RiskRouter

CHUNK_MS = 100  # simulate audio arriving in 100ms pieces, like a real stream


async def main():
    chunker = StreamChunker()
    router = RiskRouter(call_id="test-call-1")

    with wave.open("test_sample.wav", "rb") as wf:
        sample_rate = wf.getframerate()
        bytes_per_sample = wf.getsampwidth()
        chunk_frames = int(sample_rate * (CHUNK_MS / 1000))

        window_count = 0
        while True:
            pcm_chunk = wf.readframes(chunk_frames)
            if not pcm_chunk:
                break

            chunker.add_audio(pcm_chunk)
            ready_windows = chunker.get_ready_windows()

            for audio_bytes, has_speech in ready_windows:
                window_count += 1
                wav_bytes = chunker.pcm_to_wav_bytes(audio_bytes)
                result = await score_chunk(wav_bytes, filename=f"window_{window_count}.wav")

                action = router.route(result["decision"], result["fused_score"])

                print(f"Window {window_count} | has_speech={has_speech} | "
                      f"decision={result['decision']} | fused_score={result['fused_score']:.3f} | "
                      f"action={action.value}")

    print(f"\nDone. {window_count} windows scored and routed.")


asyncio.run(main())