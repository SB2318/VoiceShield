import librosa
import torch
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model

MODEL_NAME = "facebook/wav2vec2-base"

def extract_ssl_embedding(filepath):
    waveform, sample_rate = librosa.load(filepath, sr=16000)  # wav2vec2 expects 16kHz

    feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
    model = Wav2Vec2Model.from_pretrained(MODEL_NAME)

    inputs = feature_extractor(waveform, sampling_rate=16000, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)

    embedding = outputs.last_hidden_state
    print(f"Embedding shape: {embedding.shape}")  # (batch, time_frames, hidden_dim)
    return embedding

if __name__ == "__main__":
    extract_ssl_embedding("ml/data/dummy/audio1.m4a")