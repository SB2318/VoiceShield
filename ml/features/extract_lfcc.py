import librosa
import numpy as np

def extract_lfcc(filepath, n_lfcc=20):
    waveform, sample_rate = librosa.load(filepath, sr=None)
    lfcc = librosa.feature.mfcc(y=waveform, sr=sample_rate, n_mfcc=n_lfcc)
    print(f"LFCC shape: {lfcc.shape}")  # (n_lfcc, time_frames)
    return lfcc

if __name__ == "__main__":
    extract_lfcc("ml/data/dummy/audio1.m4a")