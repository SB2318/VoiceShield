"""
test_orchestrator.py
Full integration test: CallSession processing a simulated live stream,
hitting a challenge, submitting a response, and (if failed) escalating
with trusted-contact notification + cooldown.
"""

import asyncio
import wave
from alert_orchestrator import CallSession

CHUNK_MS = 100


async def mock_notify(call_id: str, reason: str):
    print(f"  >> [MOCK NOTIFY] Trusted contact alerted for {call_id}: {reason}")


async def main():
    session = CallSession(call_id="demo-call-1", trusted_contact_notify_fn=mock_notify)

    with wave.open("test_sample.wav", "rb") as wf:
        sample_rate = wf.getframerate()
        chunk_frames = int(sample_rate * (CHUNK_MS / 1000))

        while True:
            pcm_chunk = wf.readframes(chunk_frames)
            if not pcm_chunk:
                break

            events = await session.process_audio(pcm_chunk)
            for e in events:
                print(e)

    if session._pending_challenge is not None:
        print("\n--- Challenge is pending. Submitting a deliberately WRONG response ---")
        fake_response = b"\x00\x00" * 8000  # silence-ish PCM, will fail transcription/energy checks
        wav_fake = session.chunker.pcm_to_wav_bytes(fake_response)
        events = await session.submit_challenge_response(wav_fake)
        for e in events:
            print(e)

        print("\nWaiting for cooldown to resolve in the background...")
        await asyncio.sleep(9)
        print("Cooldown complete. Session no longer in cooldown:", not session._in_cooldown)


asyncio.run(main())