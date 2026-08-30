from fastapi import FastAPI, UploadFile, File
import torch
import librosa
import io
from ml.training.train_fusion_real import MultiViewModel, N_LFCC
from ml.datasets.multiview_real_dataset import feature_extractor, ssl_model, FIXED_LEN

MODEL_PATH = "ml/export/fusion_model_real.pt"
CONFIDENCE_THRESHOLD = 0.65

app = FastAPI(title="VoiceShield Detection Service")

model = MultiViewModel()
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()

def extract_views(waveform):
    fixed = librosa.util.fix_length(waveform, size=FIXED_LEN) if len(waveform) < FIXED_LEN else waveform[:FIXED_LEN]
    raw_tensor = torch.tensor(fixed, dtype=torch.float32).unsqueeze(0).unsqueeze(0)

    lfcc = librosa.feature.mfcc(y=waveform, sr=16000, n_mfcc=N_LFCC)
    lfcc_tensor = torch.tensor(lfcc.mean(axis=1), dtype=torch.float32).unsqueeze(0)

    inputs = feature_extractor(waveform, sampling_rate=16000, return_tensors="pt")
    with torch.no_grad():
        ssl_out = ssl_model(**inputs)
    ssl_tensor = ssl_out.last_hidden_state.mean(dim=1)

    return raw_tensor, lfcc_tensor, ssl_tensor

@app.post("/detect")
async def detect(file: UploadFile = File(...)):
    """
    Matches the team's shared decision-object contract (minus fields Backend 2/3 add later).
    """
    audio_bytes = await file.read()
    waveform, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)

    raw, lfcc, ssl = extract_views(waveform)
    with torch.no_grad():
        logits, attn_weights = model(raw, lfcc, ssl)
        probs = torch.softmax(logits, dim=-1)
        confidence, predicted_class = torch.max(probs, dim=-1)

    confidence_val = confidence.item()
    if confidence_val < CONFIDENCE_THRESHOLD:
        decision = "unverified"
    elif predicted_class.item() == 0:
        decision = "real"
    else:
        decision = "suspected_clone"

    weights = attn_weights[0].tolist()  # [raw_weight, lfcc_weight, ssl_weight]

    return {
        "branch_scores": {
            "rawnet2": round(weights[0], 4),
            "spectrogram": round(weights[1], 4),
            "ssl": round(weights[2], 4),
        },
        "fused_score": probs[0, 1].item(),
        "decision": decision,
        "explanation": f"Model confidence: {confidence_val:.2%}. Branch trust weights show which detection view most influenced this result.",
    }

@app.get("/health")
async def health():
    return {"status": "ok"}