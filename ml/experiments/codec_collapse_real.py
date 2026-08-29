import os
import subprocess
import torch
import librosa
from ml.training.train_fusion_real import MultiViewModel
from ml.datasets.multiview_real_dataset import feature_extractor, ssl_model, N_LFCC, FIXED_LEN
from ml.evaluation.eer_auc_metrics import compute_eer

PROTOCOL_PATH = "data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.eval.trl.txt"
AUDIO_DIR = "data/LA/ASVspoof2019_LA_eval/flac"
MODEL_PATH = "ml/export/fusion_model_real.pt"
DEGRADED_DIR = "ml/data/eval_degraded"
NUM_TEST_SAMPLES = 100

CODEC_CONFIGS = {
    "opus_16kbps": {"args": ["-c:a", "libopus", "-b:a", "16k"], "ext": "ogg"},
    "amr_nb": {"args": ["-ar", "8000", "-ac", "1", "-c:a", "libopencore_amrnb", "-b:a", "12.2k"], "ext": "amr"},
}

def degrade_file(input_path, output_path, codec_args):
    cmd = ["ffmpeg", "-y", "-i", input_path] + codec_args + [output_path]
    subprocess.run(cmd, check=True, capture_output=True)

def extract_views(filepath):
    raw_waveform, sr = librosa.load(filepath, sr=16000)
    fixed = librosa.util.fix_length(raw_waveform, size=FIXED_LEN) if len(raw_waveform) < FIXED_LEN else raw_waveform[:FIXED_LEN]
    raw_tensor = torch.tensor(fixed, dtype=torch.float32).unsqueeze(0).unsqueeze(0)

    lfcc = librosa.feature.mfcc(y=raw_waveform, sr=16000, n_mfcc=N_LFCC)
    lfcc_tensor = torch.tensor(lfcc.mean(axis=1), dtype=torch.float32).unsqueeze(0)

    inputs = feature_extractor(raw_waveform, sampling_rate=16000, return_tensors="pt")
    with torch.no_grad():
        ssl_out = ssl_model(**inputs)
    ssl_tensor = ssl_out.last_hidden_state.mean(dim=1)

    return raw_tensor, lfcc_tensor, ssl_tensor

def evaluate(model, filepaths_labels):
    all_labels, all_scores = [], []
    for filepath, label in filepaths_labels:
        raw, lfcc, ssl = extract_views(filepath)
        with torch.no_grad():
            logits, _ = model(raw, lfcc, ssl)
            prob_fake = torch.softmax(logits, dim=-1)[0, 1].item()
        all_scores.append(prob_fake)
        all_labels.append(label)
    eer, _ = compute_eer(all_labels, all_scores)
    return eer

if __name__ == "__main__":
    from ml.datasets.parse_protocol import parse_protocol_file, build_filepath
    import random

    samples = parse_protocol_file(PROTOCOL_PATH)
    rng = random.Random(42)
    rng.shuffle(samples)
    samples = samples[:NUM_TEST_SAMPLES]

    model = MultiViewModel()
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()

    # --- Clean EER ---
    clean_pairs = [(build_filepath(uid, AUDIO_DIR), label) for uid, label in samples]
    clean_eer = evaluate(model, clean_pairs)
    print(f"Clean EER: {clean_eer*100:.2f}%")

    # --- Degrade audio, then measure EER per codec ---
    os.makedirs(DEGRADED_DIR, exist_ok=True)
    for codec_name, config in CODEC_CONFIGS.items():
        degraded_pairs = []
        for utterance_id, label in samples:
            input_path = build_filepath(utterance_id, AUDIO_DIR)
            output_path = os.path.join(DEGRADED_DIR, f"{utterance_id}_{codec_name}.{config['ext']}")
            if not os.path.exists(output_path):
                try:
                    degrade_file(input_path, output_path, config["args"])
                except subprocess.CalledProcessError:
                    continue
            if os.path.exists(output_path):
                degraded_pairs.append((output_path, label))

        degraded_eer = evaluate(model, degraded_pairs)
        print(f"{codec_name} EER: {degraded_eer*100:.2f}% (on {len(degraded_pairs)} samples)")