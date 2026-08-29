import os
import librosa
import torch
import torch.nn as nn
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2Model

DATA_DIR = "ml/data/dummy"
MODEL_NAME = "facebook/wav2vec2-base"
MATCH_THRESHOLD = 0.85  # cosine similarity above this = same speaker

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
ssl_model = Wav2Vec2Model.from_pretrained(MODEL_NAME)
ssl_model.eval()

def get_voiceprint(filepath):
    """Turns an audio clip into a single embedding vector — stand-in for a real voiceprint."""
    waveform, sr = librosa.load(filepath, sr=16000)
    inputs = feature_extractor(waveform, sampling_rate=16000, return_tensors="pt")
    with torch.no_grad():
        outputs = ssl_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze(0)  # (768,)

def verify_speaker(enrolled_embedding, live_embedding):
    """Stage B: does the live voice match the claimed enrolled identity?"""
    cos_sim = nn.functional.cosine_similarity(
        enrolled_embedding.unsqueeze(0), live_embedding.unsqueeze(0)
    ).item()
    is_match = cos_sim >= MATCH_THRESHOLD
    return cos_sim, is_match

if __name__ == "__main__":
    real_folder = os.path.join(DATA_DIR, "real")
    real_files = [os.path.join(real_folder, f) for f in os.listdir(real_folder)]
    fake_folder = os.path.join(DATA_DIR, "fake")
    fake_files = [os.path.join(fake_folder, f) for f in os.listdir(fake_folder)]

    # Pretend the first "real" clip is the enrolled voiceprint (e.g. "your father's voice")
    enrolled_embedding = get_voiceprint(real_files[0])
    print(f"Enrolled voiceprint from: {real_files[0]}")

    # Test every other clip against it
    test_files = real_files[1:] + fake_files
    for filepath in test_files:
        live_embedding = get_voiceprint(filepath)
        cos_sim, is_match = verify_speaker(enrolled_embedding, live_embedding)
        print(f"{filepath} -> similarity: {cos_sim:.4f}, match: {is_match}")