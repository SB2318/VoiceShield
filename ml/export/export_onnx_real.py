import torch
from ml.training.train_fusion_real import MultiViewModel, N_LFCC

MODEL_PATH = "ml/export/fusion_model_real.pt"
ONNX_PATH = "ml/export/fusion_model_real.onnx"

if __name__ == "__main__":
    model = MultiViewModel()
    model.load_state_dict(torch.load(MODEL_PATH))
    model.eval()

    dummy_raw = torch.randn(1, 1, 32000)
    dummy_lfcc = torch.randn(1, N_LFCC)
    dummy_ssl = torch.randn(1, 768)

    torch.onnx.export(
        model,
        (dummy_raw, dummy_lfcc, dummy_ssl),
        ONNX_PATH,
        input_names=["raw", "lfcc", "ssl"],
        output_names=["logits", "attn_weights"],
        dynamic_axes={"raw": {0: "batch"}, "lfcc": {0: "batch"}, "ssl": {0: "batch"}},
        opset_version=18,
    )
    print(f"Exported real trained model to: {ONNX_PATH}")