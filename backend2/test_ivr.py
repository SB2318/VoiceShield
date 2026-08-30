"""
test_ivr.py
Runs a simulated IVR call end to end using test_sample.wav as the
"callback leg" audio.
"""

import asyncio
from ivr_line import IVRLine


async def main():
    ivr = IVRLine()  # no real telephony wired in yet - simulates a successful connect
    result = await ivr.handle_call(
        caller_reported_number="+911234567890",
        sample_audio_path="test_sample.wav",
    )
    print("\nResult:", result)


asyncio.run(main())