import os
import numpy as np
from pydub import AudioSegment

CLEAN_DIR = "ml/data/dummy"
DEGRADED_DIR = "ml/data/dummy_degraded"

def audio_stats(filepath):
    audio = AudioSegment.from_file(filepath)  # ffmpeg handles any format under the hood
    samples = np.array(audio.get_array_of_samples()).astype(np.float32)
    samples /= (1 << (8 * audio.sample_width - 1))  # normalize to -1..1 range
    return {
        "duration": len(audio) / 1000.0,  # pydub gives length in ms
        "rms_energy": float(np.sqrt(np.mean(samples**2))),
        "sample_rate": audio.frame_rate,
    }

if __name__ == "__main__":
    for folder in ["real", "fake"]:
        clean_folder = os.path.join(CLEAN_DIR, folder)
        degraded_folder = os.path.join(DEGRADED_DIR, folder)

        for filename in os.listdir(clean_folder):
            base_name = os.path.splitext(filename)[0]
            clean_path = os.path.join(clean_folder, filename)
            clean_stats = audio_stats(clean_path)
            print(f"\n{filename} (clean): {clean_stats}")

            for degraded_file in os.listdir(degraded_folder):
                if degraded_file.startswith(base_name):
                    degraded_path = os.path.join(degraded_folder, degraded_file)
                    degraded_stats = audio_stats(degraded_path)
                    print(f"  -> {degraded_file}: {degraded_stats}")