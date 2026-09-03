import random
import librosa
import torch
from torch.utils.data import Dataset
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model
from ml.datasets.parse_protocol import parse_protocol_file, build_filepath

N_MFCC = 20
FIXED_LEN = 32000
MODEL_NAME = "facebook/wav2vec2-base"

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
ssl_model = Wav2Vec2Model.from_pretrained(MODEL_NAME)
ssl_model.eval()


class MultiViewRealDataset(Dataset):
    def __init__(self, protocol_path, audio_dir, max_samples=None, seed=42):
        self.audio_dir = audio_dir
        self.samples = parse_protocol_file(protocol_path)

        if max_samples:
            rng = random.Random(seed)
            rng.shuffle(self.samples)
            self.samples = self.samples[:max_samples]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        utterance_id, label = self.samples[idx]
        filepath = build_filepath(utterance_id, self.audio_dir)

        # Raw waveform (16 kHz)
        raw_waveform, sr = librosa.load(filepath, sr=16000)

        # Fixed-length raw input for RawNet branch
        if len(raw_waveform) < FIXED_LEN:
            raw_waveform_fixed = librosa.util.fix_length(
                raw_waveform,
                size=FIXED_LEN,
            )
        else:
            raw_waveform_fixed = raw_waveform[:FIXED_LEN]

        raw_tensor = torch.tensor(
            raw_waveform_fixed,
            dtype=torch.float32,
        ).unsqueeze(0)

        # MFCC feature branch
        mfcc = librosa.feature.mfcc(
            y=raw_waveform,
            sr=16000,
            n_mfcc=N_MFCC,
        )

        mfcc_tensor = torch.tensor(
            mfcc.mean(axis=1),
            dtype=torch.float32,
        )

        # SSL embedding branch (wav2vec2)
        inputs = feature_extractor(
            raw_waveform,
            sampling_rate=16000,
            return_tensors="pt",
        )

        with torch.no_grad():
            ssl_out = ssl_model(**inputs)

        ssl_tensor = ssl_out.last_hidden_state.mean(dim=1).squeeze(0)

        return raw_tensor, mfcc_tensor, ssl_tensor, label