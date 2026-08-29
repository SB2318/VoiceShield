import os
import random
import librosa
import torch
from torch.utils.data import Dataset
from ml.datasets.parse_protocol import parse_protocol_file, build_filepath

class ASVspoofDataset(Dataset):
    def __init__(self, protocol_path, audio_dir, n_lfcc=20, max_samples=None, seed=42):
        self.audio_dir = audio_dir
        self.n_lfcc = n_lfcc
        self.samples = parse_protocol_file(protocol_path)

        if max_samples:
            rng = random.Random(seed)  # fixed seed so results are reproducible
            rng.shuffle(self.samples)
            self.samples = self.samples[:max_samples]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        utterance_id, label = self.samples[idx]
        filepath = build_filepath(utterance_id, self.audio_dir)

        waveform, sr = librosa.load(filepath, sr=16000)
        lfcc = librosa.feature.mfcc(y=waveform, sr=sr, n_mfcc=self.n_lfcc)
        lfcc_mean = lfcc.mean(axis=1)

        return torch.tensor(lfcc_mean, dtype=torch.float32), label


if __name__ == "__main__":
    PROTOCOL_PATH = "data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt"
    AUDIO_DIR = "data/LA/ASVspoof2019_LA_train/flac"

    if not os.path.exists(PROTOCOL_PATH):
        print("Dataset not extracted yet — update paths above once unzip finishes, then rerun.")
    else:
        dataset = ASVspoofDataset(PROTOCOL_PATH, AUDIO_DIR, max_samples=5)
        print(f"Dataset size (limited to 5 for testing): {len(dataset)}")

        features, label = dataset[0]
        print(f"First sample -> feature shape: {features.shape}, label: {label}")