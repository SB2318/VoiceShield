import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from ml.datasets.multiview_real_dataset import MultiViewRealDataset, N_LFCC
from ml.evaluation.eer_auc_metrics import compute_eer, compute_auc

PROTOCOL_PATH = "data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt"
AUDIO_DIR = "data/LA/ASVspoof2019_LA_train/flac"
MAX_SAMPLES = 500  # bump this up later (e.g. 3000+) for a stronger number if time allows
MODEL_SAVE_PATH = "ml/export/fusion_model_real.pt"

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
    def __init__(self, branch_dim=32):
        super().__init__()
        self.attention = nn.Linear(branch_dim, 1)
        self.classifier = nn.Linear(branch_dim, 2)
    def forward(self, raw_out, lfcc_out, ssl_out):
        stacked = torch.stack([raw_out, lfcc_out, ssl_out], dim=1)
        attn_scores = self.attention(stacked).squeeze(-1)
        attn_weights = torch.softmax(attn_scores, dim=1)
        fused = (stacked * attn_weights.unsqueeze(-1)).sum(dim=1)
        return self.classifier(fused), attn_weights

class MultiViewModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.raw_branch = RawBranch()
        self.lfcc_branch = LFCCBranch()
        self.ssl_branch = SSLBranch()
        self.fusion = AttentionFusion()
    def forward(self, raw, lfcc, ssl):
        return self.fusion(self.raw_branch(raw), self.lfcc_branch(lfcc), self.ssl_branch(ssl))

if __name__ == "__main__":
    dataset = MultiViewRealDataset(PROTOCOL_PATH, AUDIO_DIR, max_samples=MAX_SAMPLES)
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_ds, test_ds = random_split(dataset, [train_size, test_size])
    train_loader = DataLoader(train_ds, batch_size=8, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=8, shuffle=False)

    model = MultiViewModel()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    print(f"Training fusion model on {train_size} real samples, testing on {test_size}...")
    for epoch in range(10):
        model.train()
        total_loss = 0
        for raw, lfcc, ssl, labels in train_loader:
            optimizer.zero_grad()
            logits, _ = model(raw, lfcc, ssl)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}, Avg Loss: {total_loss/len(train_loader):.4f}")

    model.eval()
    all_labels, all_scores = [], []
    with torch.no_grad():
        for raw, lfcc, ssl, labels in test_loader:
            logits, _ = model(raw, lfcc, ssl)
            probs = torch.softmax(logits, dim=-1)[:, 1]
            all_scores.extend(probs.tolist())
            all_labels.extend(labels.tolist())

    eer, _ = compute_eer(all_labels, all_scores)
    auc = compute_auc(all_labels, all_scores)
    print(f"\n=== REAL FUSION MODEL RESULTS ({len(dataset)} samples) ===")
    print(f"EER: {eer*100:.2f}%")
    print(f"AUC: {auc:.4f}")

    os.makedirs("ml/export", exist_ok=True)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Saved trained model to {MODEL_SAVE_PATH}")