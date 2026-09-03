from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import Optional
import torch
import torch.nn as nn
import librosa
import io
import numpy as np
import onnxruntime as ort
from pathlib import Path
import logging

from speechbrain.inference.speaker import EncoderClassifier
from speechbrain.utils.fetching import LocalStrategy

from ml.training.train_fusion_real import MultiViewModel, N_MFCC
from ml.datasets.multiview_real_dataset import (
    feature_extractor,
    ssl_model,
    FIXED_LEN,
)


ML_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = ML_DIR / "export" / "fusion_model_real.pt"
ONNX_MODEL_PATH = ML_DIR / "export" / "fusion_model_real.onnx"

CONFIDENCE_THRESHOLD = 0.65
SPEAKER_MATCH_THRESHOLD = 0.55

app = FastAPI(title="VoiceShield Detection Service")

logger = logging.getLogger(__name__)

# PyTorch model is loaded lazily.
# This allows the API to start even if the checkpoint is unavailable.
model = None


def get_model():
    global model

    if model is None:
        try:
            loaded_model = MultiViewModel()

            state_dict = torch.load(
                MODEL_PATH,
                map_location="cpu",
                weights_only=True,
            )

            loaded_model.load_state_dict(state_dict)
            loaded_model.eval()

            model = loaded_model

        except FileNotFoundError:
            logger.exception(
                "Detection model checkpoint not found: %s",
                MODEL_PATH,
            )
            raise HTTPException(
                status_code=503,
                detail="Detection model is unavailable.",
            )

        except Exception:
            logger.exception("Failed to load detection model")
            raise HTTPException(
                status_code=503,
                detail="Detection model could not be loaded.",
            )

    return model


# ONNX Runtime session is also loaded lazily.
# ONNX is preferred for inference, with PyTorch as a fallback.
onnx_session = None


def get_onnx_session():
    global onnx_session

    if onnx_session is None:
        if not ONNX_MODEL_PATH.exists():
            logger.warning(
                "ONNX model not found: %s. Falling back to PyTorch.",
                ONNX_MODEL_PATH,
            )
            return None

        try:
            onnx_session = ort.InferenceSession(
                str(ONNX_MODEL_PATH),
                providers=["CPUExecutionProvider"],
            )

        except Exception:
            logger.exception("Failed to load ONNX model")
            return None

    return onnx_session


# Dedicated speaker-verification model.
# This is separate from the spoof-detection SSL branch.
# ECAPA-TDNN is trained specifically for speaker identity verification.
speaker_model = EncoderClassifier.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir="ml/export/speechbrain_ecapa",
    run_opts={"device": "cpu"},
    local_strategy=LocalStrategy.COPY,
)

enrolled_voiceprints = {}


def extract_views(waveform):
    fixed = (
        librosa.util.fix_length(waveform, size=FIXED_LEN)
        if len(waveform) < FIXED_LEN
        else waveform[:FIXED_LEN]
    )

    raw_tensor = (
        torch.tensor(fixed, dtype=torch.float32)
        .unsqueeze(0)
        .unsqueeze(0)
    )

    # MFCC feature branch
    mfcc = librosa.feature.mfcc(
        y=waveform,
        sr=16000,
        n_mfcc=N_MFCC,
    )

    mfcc_tensor = torch.tensor(
        mfcc.mean(axis=1),
        dtype=torch.float32,
    ).unsqueeze(0)

    # Wav2Vec2 SSL feature branch
    inputs = feature_extractor(
        waveform,
        sampling_rate=16000,
        return_tensors="pt",
    )

    with torch.no_grad():
        ssl_out = ssl_model(**inputs)

    ssl_tensor = ssl_out.last_hidden_state.mean(dim=1)

    return raw_tensor, mfcc_tensor, ssl_tensor


def get_voiceprint_embedding(waveform):
    """Stage B: dedicated speaker-verification embedding via ECAPA-TDNN."""
    waveform_tensor = torch.tensor(
        waveform,
        dtype=torch.float32,
    ).unsqueeze(0)

    with torch.no_grad():
        embedding = speaker_model.encode_batch(waveform_tensor)

    return embedding.squeeze(0).squeeze(0)


@app.post("/enroll")
async def enroll(
    name: str = Form(...),
    file: UploadFile = File(...),
):
    audio_bytes = await file.read()

    waveform, sr = librosa.load(
        io.BytesIO(audio_bytes),
        sr=16000,
    )

    embedding = get_voiceprint_embedding(waveform)

    enrolled_voiceprints[name] = embedding

    return {
        "status": "enrolled",
        "name": name,
    }


@app.post("/detect")
async def detect(
    file: UploadFile = File(...),
    claimed_identity: Optional[str] = Form(None),
):
    audio_bytes = await file.read()

    waveform, sr = librosa.load(
        io.BytesIO(audio_bytes),
        sr=16000,
    )

    # Extract the three model views.
    raw, mfcc, ssl = extract_views(waveform)

    # Prefer ONNX Runtime inference.
    detection_onnx = get_onnx_session()

    if detection_onnx is not None:
        onnx_outputs = detection_onnx.run(
            ["logits", "attn_weights"],
            {
                "raw": raw.numpy(),
                "mfcc": mfcc.numpy(),
                "ssl": ssl.numpy(),
            },
        )

        logits = torch.from_numpy(onnx_outputs[0])
        attn_weights = torch.from_numpy(onnx_outputs[1])

    else:
        # PyTorch fallback if ONNX is unavailable.
        detection_model = get_model()

        with torch.no_grad():
            logits, attn_weights = detection_model(
                raw,
                mfcc,
                ssl,
            )

    # Common post-processing for both ONNX and PyTorch.
    probs = torch.softmax(logits, dim=-1)
    confidence, predicted_class = torch.max(
        probs,
        dim=-1,
    )

    confidence_val = confidence.item()

    if confidence_val < CONFIDENCE_THRESHOLD:
        decision = "unverified"

    elif predicted_class.item() == 0:
        decision = "real"

    else:
        decision = "suspected_clone"

    weights = attn_weights[0].tolist()

    speaker_match_result = None

    # Optional speaker identity verification.
    if claimed_identity:
        if claimed_identity not in enrolled_voiceprints:
            speaker_match_result = {
                "checked": False,
                "reason": (
                    f"No enrolled voiceprint found for "
                    f"'{claimed_identity}'"
                ),
            }

        else:
            live_embedding = get_voiceprint_embedding(waveform)

            enrolled_embedding = enrolled_voiceprints[
                claimed_identity
            ]

            cos_sim = nn.functional.cosine_similarity(
                enrolled_embedding.unsqueeze(0),
                live_embedding.unsqueeze(0),
            ).item()

            is_match = cos_sim >= SPEAKER_MATCH_THRESHOLD

            speaker_match_result = {
                "checked": True,
                "claimed_identity": claimed_identity,
                "similarity": round(cos_sim, 4),
                "match": is_match,
            }

            if not is_match and decision == "real":
                decision = "speaker_mismatch"

    return {
        "branch_scores": {
            "rawnet2": round(weights[0], 4),
            "spectrogram": round(weights[1], 4),
            "ssl": round(weights[2], 4),
        },
        "fused_score": probs[0, 1].item(),
        "decision": decision,
        "speaker_verification": speaker_match_result,
        "explanation": (
            f"Model confidence: {confidence_val:.2%}. "
            "Branch trust weights show which detection view "
            "most influenced this result."
        ),
    }


@app.get("/health")
async def health():
    return {"status": "ok"}