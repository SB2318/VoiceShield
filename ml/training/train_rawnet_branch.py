import os
import librosa
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

DATA_DIR = "ml/data/dummy"
FIXED_LEN = 32000  # ~2 seconds at 16kHz, so every clip is the same length

class RawWaveformDataset(Dataset):
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
        waveform, sr = librosa.load(filepath, sr=16000)  # force 16kHz
        # pad or trim to a fixed length so batching works
        if len(waveform) < FIXED_LEN:
            waveform = librosa.util.fix_length(waveform, size=FIXED_LEN)
        else:
            waveform = waveform[:FIXED_LEN]
        return torch.tensor(waveform, dtype=torch.float32).unsqueeze(0), label  # shape: (1, FIXED_LEN)

class SimpleRawNetStub(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 16, kernel_size=80, stride=4)
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(16, 2)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = self.pool(x).squeeze(-1)
        return self.fc(x)

if __name__ == "__main__":
    dataset = RawWaveformDataset(DATA_DIR)
    loader = DataLoader(dataset, batch_size=2, shuffle=True)

    model = SimpleRawNetStub()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(5):
        for waveforms, labels in loader:
            optimizer.zero_grad()
            outputs = model(waveforms)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

    print("RawNet stub training loop ran successfully.")