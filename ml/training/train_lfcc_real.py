import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from ml.datasets.asvspoof_dataset import ASVspoofDataset
from ml.evaluation.eer_auc_metrics import compute_eer, compute_auc

PROTOCOL_PATH = "data/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt"
AUDIO_DIR = "data/LA/ASVspoof2019_LA_train/flac"
N_LFCC = 20

class SimpleClassifier(nn.Module):
    def __init__(self, input_dim=N_LFCC):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(input_dim, 64), nn.ReLU(), nn.Linear(64, 2))

    def forward(self, x):
        return self.fc(x)

if __name__ == "__main__":
    # Start with a subset (500 samples) so this runs in minutes, not hours —
    # we'll scale up to the full 25,380 once this pipeline is confirmed working
    full_dataset = ASVspoofDataset(PROTOCOL_PATH, AUDIO_DIR, n_lfcc=N_LFCC, max_samples=500)

    train_size = int(0.8 * len(full_dataset))
    test_size = len(full_dataset) - train_size
    train_dataset, test_dataset = random_split(full_dataset, [train_size, test_size])

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

    model = SimpleClassifier()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    print(f"Training on {train_size} samples, testing on {test_size} samples...")

    for epoch in range(10):
        model.train()
        total_loss = 0
        for features, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(features)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}, Avg Loss: {total_loss/len(train_loader):.4f}")

    # Evaluate on held-out test set
    model.eval()
    all_labels = []
    all_scores = []
    with torch.no_grad():
        for features, labels in test_loader:
            outputs = model(features)
            probs = torch.softmax(outputs, dim=-1)[:, 1]  # probability of "fake"
            all_scores.extend(probs.tolist())
            all_labels.extend(labels.tolist())

    eer, eer_threshold = compute_eer(all_labels, all_scores)
    auc = compute_auc(all_labels, all_scores)

    print(f"\n=== REAL BASELINE RESULTS (LFCC branch, {len(full_dataset)} samples) ===")
    print(f"EER: {eer*100:.2f}%")
    print(f"AUC: {auc:.4f}")