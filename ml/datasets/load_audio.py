import librosa

def load_audio(filepath):
    waveform, sample_rate = librosa.load(filepath, sr=None)
    print(f"Loaded: {filepath}")
    print(f"Shape: {waveform.shape}, Sample rate: {sample_rate}")
    return waveform, sample_rate

if __name__ == "__main__":
    load_audio("ml/data/dummy/audio1.m4a")