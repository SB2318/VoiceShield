import numpy as np
import torch
from ml.training.train_fusion_real import MultiViewModel, N_MFCC

MODEL_PATH = "ml/export/fusion_model_real.pt"
ONNX_PATH = "ml/export/fusion_model_real.onnx"


if __name__ == "__main__":
    model = MultiViewModel()

    state_dict = torch.load(
        MODEL_PATH,
        map_location="cpu",
        weights_only=True,
    )

    model.load_state_dict(state_dict)
    model.eval()

    dummy_raw = torch.randn(1, 1, 32000)
    dummy_mfcc = torch.randn(1, N_MFCC)
    dummy_ssl = torch.randn(1, 768)

    torch.onnx.export(
        model,
        (dummy_raw, dummy_mfcc, dummy_ssl),
        ONNX_PATH,
        input_names=["raw", "mfcc", "ssl"],
        output_names=["logits", "attn_weights"],
        dynamic_axes={
            "raw": {0: "batch"},
            "mfcc": {0: "batch"},
            "ssl": {0: "batch"},
            "logits": {0: "batch"},
            "attn_weights": {0: "batch"},
        },
        opset_version=18,
    )

    print(f"Exported real trained model to: {ONNX_PATH}")

    # Verify that ONNX Runtime produces the same outputs as PyTorch.
    import onnxruntime as ort

    with torch.no_grad():
        torch_logits, torch_attn = model(
            dummy_raw,
            dummy_mfcc,
            dummy_ssl,
        )

    ort_session = ort.InferenceSession(
        ONNX_PATH,
        providers=["CPUExecutionProvider"],
    )

    onnx_logits, onnx_attn = ort_session.run(
        None,
        {
            "raw": dummy_raw.numpy(),
            "mfcc": dummy_mfcc.numpy(),
            "ssl": dummy_ssl.numpy(),
        },
    )

    logits_diff = np.max(
        np.abs(torch_logits.numpy() - onnx_logits)
    )

    attn_diff = np.max(
        np.abs(torch_attn.numpy() - onnx_attn)
    )

    print(f"Max logits difference: {logits_diff:.8f}")
    print(f"Max attention difference: {attn_diff:.8f}")

    if logits_diff < 1e-4 and attn_diff < 1e-4:
        print("ONNX export verified successfully!")
    else:
        print("WARNING: ONNX and PyTorch outputs differ significantly!")