import os

def parse_protocol_file(protocol_path):
    """
    Parses an ASVspoof protocol file into a list of (utterance_id, label) tuples.
    label: 0 = bonafide (real), 1 = spoof (fake)
    """
    samples = []
    with open(protocol_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 5:
                continue  # skip malformed/blank lines
            utterance_id = parts[1]
            label_str = parts[4]
            label = 0 if label_str == "bonafide" else 1
            samples.append((utterance_id, label))
    return samples

def build_filepath(utterance_id, audio_dir, extension=".flac"):
    """ASVspoof audio files are named exactly as the utterance_id in the protocol."""
    return os.path.join(audio_dir, utterance_id + extension)

if __name__ == "__main__":
    # Update these paths once your dataset is downloaded and unzipped
    PROTOCOL_PATH = "data/ASVspoof2019/LA/ASVspoof2019_LA_cm_protocols/ASVspoof2019.LA.cm.train.trn.txt"
    AUDIO_DIR = "data/ASVspoof2019/LA/ASVspoof2019_LA_train/flac"

    if not os.path.exists(PROTOCOL_PATH):
        print(f"Protocol file not found yet at: {PROTOCOL_PATH}")
        print("This is expected if your dataset hasn't finished downloading — script logic is ready to go once it has.")
    else:
        samples = parse_protocol_file(PROTOCOL_PATH)
        print(f"Parsed {len(samples)} samples from protocol file")
        print(f"First 3 entries: {samples[:3]}")

        # Sanity check: does the first audio file actually exist where we expect?
        first_utterance_id, first_label = samples[0]
        filepath = build_filepath(first_utterance_id, AUDIO_DIR)
        print(f"Expected audio path: {filepath}")
        print(f"File exists: {os.path.exists(filepath)}")