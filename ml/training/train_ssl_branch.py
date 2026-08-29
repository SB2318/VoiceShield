import os
import librosa
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model

DATA_DIR = "ml/data/dummy"
MODEL_NAME = "facebook/wav2vec2-base"

# Load these ONCE, outside the dataset class — reloading per-sample would be very slow
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
ssl_model = Wav2Vec2Model.from_pretrained(MODEL_NAME)
ssl_model.eval()

class SSLDataset(Dataset):
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
        waveform, sr = librosa.load(filepath, sr=16000)
        inputs = feature_extractor(waveform, sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            outputs = ssl_model(**inputs)
        embedding = outputs.last_hidden_state.mean(dim=1).squeeze(0)  # average over time -> (768,)
        return embedding, label

class SSLClassifier(nn.Module):
    def __init__(self, input_dim=768):
        super().__init__()
        self.fc = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 2)
        )

    def forward(self, x):
        return self.fc(x)

if __name__ == "__main__":
    dataset = SSLDataset(DATA_DIR)
    loader = DataLoader(dataset, batch_size=2, shuffle=True)

    model = SSLClassifier()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    for epoch in range(5):
        for embeddings, labels in loader:
            optimizer.zero_grad()
            outputs = model(embeddings)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

    print("SSL branch training loop ran successfully.")