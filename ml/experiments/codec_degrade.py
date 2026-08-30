import subprocess
import os

INPUT_DIR = "ml/data/dummy"
OUTPUT_DIR = "ml/data/dummy_degraded"

CODEC_CONFIGS = {
    "opus_16kbps": {"args": ["-c:a", "libopus", "-b:a", "16k"], "ext": "ogg"},
    "amr_nb": {"args": ["-ar", "8000", "-ac", "1", "-c:a", "libopencore_amrnb", "-b:a", "12.2k"], "ext": "amr"},
    "g711_ulaw": {"args": ["-c:a", "pcm_mulaw", "-ar", "8000"], "ext": "wav"},
}

def degrade_audio(input_path, output_path, codec_args):
    cmd = ["ffmpeg", "-y", "-i", input_path] + codec_args + [output_path]
    subprocess.run(cmd, check=True, capture_output=True)

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for folder in ["real", "fake"]:
        in_folder = os.path.join(INPUT_DIR, folder)
        out_folder = os.path.join(OUTPUT_DIR, folder)
        os.makedirs(out_folder, exist_ok=True)
        for filename in os.listdir(in_folder):
            input_path = os.path.join(in_folder, filename)
            base_name = os.path.splitext(filename)[0]
            for codec_name, config in CODEC_CONFIGS.items():
                output_path = os.path.join(out_folder, f"{base_name}_{codec_name}.{config['ext']}")
                try:
                    degrade_audio(input_path, output_path, config["args"])
                    print(f"Created: {output_path}")
                except subprocess.CalledProcessError as e:
                    print(f"FAILED: {output_path} — {e.stderr.decode()[-300:]}")  # last 300 chars, more useful than the version banner