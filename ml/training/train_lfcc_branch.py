import os
import librosa
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

DATA_DIR = "ml/data/dummy"
N_LFCC = 20

class SpoofDataset(Dataset):
    def __init__(self, data_dir):
        self.samples = []
        for label, folder in enumerate(["real", "fake"]):  # real=0, fake=1
            folder_path = os.path.join(data_dir, folder)
            for filename in os.listdir(folder_path):
                self.samples.append((os.path.join(folder_path, filename), label))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        filepath, label = self.samples[idx]
        waveform, sr = librosa.load(filepath, sr=None)
        lfcc = librosa.feature.mfcc(y=waveform, sr=sr, n_mfcc=N_LFCC)
        lfcc_mean = lfcc.mean(axis=1)  # collapse time axis for now — simple baseline
        return torch.tensor(lfcc_mean, dtype=torch.float32), label

class SimpleClassifier(nn.Module):
    def __init__(self, input_dim=N_LFCC):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 2)  # 2 classes: real, fake
        )

    def forward(self, x):
        return self.fc(x)

if __name__ == "__main__":
    dataset = SpoofDataset(DATA_DIR)
    loader = DataLoader(dataset, batch_size=2, shuffle=True)

    model = SimpleClassifier()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(5):
        for features, labels in loader:
            optimizer.zero_grad()
            outputs = model(features)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

    print("Training loop ran successfully.")