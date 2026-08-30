import asyncio
from model_client import score_chunk, health_check

async def main():
    is_up = await health_check()
    print("Backend 1 service up:", is_up)

    with open("test_sample.wav", "rb") as f:
        audio_bytes = f.read()

    result = await score_chunk(audio_bytes)
    print("Detection result:", result)

asyncio.run(main())