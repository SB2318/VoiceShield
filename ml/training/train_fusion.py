import os
import librosa
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model

DATA_DIR = "ml/data/dummy"
N_LFCC = 20
FIXED_LEN = 32000
MODEL_NAME = "facebook/wav2vec2-base"

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
ssl_model = Wav2Vec2Model.from_pretrained(MODEL_NAME)
ssl_model.eval()

class MultiViewDataset(Dataset):
    def __init__(self, data_dir):
        self.samples = []
        for label, folder in enumerate(["real", "fake"]):
            folder_path = os.path.join(data_dir, folder)
            for filename in os.listdir(folder_path):
                self.samples.append((os.path.join(folder_path, filename), label))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        filepath, label = self.samples[idx]

        # --- Raw waveform view (for RawNet branch) ---
        raw_waveform, sr = librosa.load(filepath, sr=16000)
        if len(raw_waveform) < FIXED_LEN:
            raw_waveform = librosa.util.fix_length(raw_waveform, size=FIXED_LEN)
        else:
            raw_waveform = raw_waveform[:FIXED_LEN]
        raw_tensor = torch.tensor(raw_waveform, dtype=torch.float32).unsqueeze(0)

        # --- LFCC view ---
        lfcc = librosa.feature.mfcc(y=raw_waveform, sr=16000, n_mfcc=N_LFCC)
        lfcc_tensor = torch.tensor(lfcc.mean(axis=1), dtype=torch.float32)

        # --- SSL embedding view ---
        inputs = feature_extractor(raw_waveform, sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            ssl_out = ssl_model(**inputs)
        ssl_tensor = ssl_out.last_hidden_state.mean(dim=1).squeeze(0)

        return raw_tensor, lfcc_tensor, ssl_tensor, label


class RawBranch(nn.Module):
    def __init__(self, out_dim=32):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 16, kernel_size=80, stride=4)
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(16, out_dim)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = self.pool(x).squeeze(-1)
        return self.fc(x)


class LFCCBranch(nn.Module):
    def __init__(self, out_dim=32):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(N_LFCC, 32), nn.ReLU(), nn.Linear(32, out_dim))

    def forward(self, x):
        return self.fc(x)


class SSLBranch(nn.Module):
    def __init__(self, out_dim=32):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(768, 64), nn.ReLU(), nn.Linear(64, out_dim))

    def forward(self, x):
        return self.fc(x)


class AttentionFusion(nn.Module):
    """Learns how much to trust each branch, rather than simple averaging."""
    def __init__(self, branch_dim=32, num_branches=3):
        super().__init__()
        self.attention = nn.Linear(branch_dim, 1)  # scores each branch's output
        self.classifier = nn.Linear(branch_dim, 2)

    def forward(self, branch_outputs):
        # branch_outputs: list of (batch, branch_dim) tensors, one per branch
        stacked = torch.stack(branch_outputs, dim=1)  # (batch, num_branches, branch_dim)
        attn_scores = self.attention(stacked).squeeze(-1)  # (batch, num_branches)
        attn_weights = torch.softmax(attn_scores, dim=1)  # how much to trust each branch
        fused = (stacked * attn_weights.unsqueeze(-1)).sum(dim=1)  # weighted sum
        return self.classifier(fused), attn_weights


class MultiViewModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.raw_branch = RawBranch()
        self.lfcc_branch = LFCCBranch()
        self.ssl_branch = SSLBranch()
        self.fusion = AttentionFusion()

    def forward(self, raw, lfcc, ssl):
        raw_out = self.raw_branch(raw)
        lfcc_out = self.lfcc_branch(lfcc)
        ssl_out = self.ssl_branch(ssl)
        logits, attn_weights = self.fusion([raw_out, lfcc_out, ssl_out])
        return logits, attn_weights


if __name__ == "__main__":
    dataset = MultiViewDataset(DATA_DIR)
    loader = DataLoader(dataset, batch_size=2, shuffle=True)

    model = MultiViewModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(5):
        for raw, lfcc, ssl, labels in loader:
            optimizer.zero_grad()
            logits, attn_weights = model(raw, lfcc, ssl)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}, Attention weights (last batch): {attn_weights.detach().numpy()}")

    print("Fusion model training loop ran successfully.")