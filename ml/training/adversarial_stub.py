import os
import librosa
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

DATA_DIR = "ml/data/dummy"
N_LFCC = 20
EPSILON = 0.05  # how strong the adversarial perturbation is

class SpoofDataset(Dataset):
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
        waveform, sr = librosa.load(filepath, sr=None)
        lfcc = librosa.feature.mfcc(y=waveform, sr=sr, n_mfcc=N_LFCC)
        lfcc_mean = lfcc.mean(axis=1)
        return torch.tensor(lfcc_mean, dtype=torch.float32), label

class SimpleClassifier(nn.Module):
    def __init__(self, input_dim=N_LFCC):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(input_dim, 32), nn.ReLU(), nn.Linear(32, 2))

    def forward(self, x):
        return self.fc(x)

def fgsm_attack(model, features, labels, criterion, epsilon):
    """Generates an adversarial version of `features` designed to fool the model."""
    features = features.clone().detach().requires_grad_(True)
    outputs = model(features)
    loss = criterion(outputs, labels)
    model.zero_grad()
    loss.backward()

    # Nudge the input in the direction that INCREASES the loss the most
    perturbation = epsilon * features.grad.sign()
    adversarial_features = features + perturbation
    return adversarial_features.detach()

if __name__ == "__main__":
    dataset = SpoofDataset(DATA_DIR)
    loader = DataLoader(dataset, batch_size=2, shuffle=True)

    model = SimpleClassifier()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(5):
        for features, labels in loader:
            # Generate adversarial examples using the model's CURRENT weights
            adv_features = fgsm_attack(model, features, labels, criterion, EPSILON)

            # Train on BOTH clean and adversarial examples in the same step
            optimizer.zero_grad()
            clean_outputs = model(features)
            adv_outputs = model(adv_features)
            loss = criterion(clean_outputs, labels) + criterion(adv_outputs, labels)
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch+1}, Combined Loss: {loss.item():.4f}")

    print("Adversarial training stub ran successfully.")