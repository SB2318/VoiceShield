import torch
import torch.nn as nn
import numpy as np
import onnxruntime as ort

N_LFCC = 20

# Same architecture as train_fusion.py — kept simple/self-contained here
# so this script can run independently without needing the full training pipeline
class RawBranch(nn.Module):
    def __init__(self, out_dim=32):
        super().__init__()
        self.conv1 = nn.Conv1d(1, 16, kernel_size=80, stride=4)
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(16, out_dim)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = self.pool(x).squeeze(-1)
        return self.fc(x)

class LFCCBranch(nn.Module):
    def __init__(self, out_dim=32):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(N_LFCC, 32), nn.ReLU(), nn.Linear(32, out_dim))

    def forward(self, x):
        return self.fc(x)

class SSLBranch(nn.Module):
    def __init__(self, out_dim=32):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(768, 64), nn.ReLU(), nn.Linear(64, out_dim))

    def forward(self, x):
        return self.fc(x)

class AttentionFusion(nn.Module):
    def __init__(self, branch_dim=32):
        super().__init__()
        self.attention = nn.Linear(branch_dim, 1)
        self.classifier = nn.Linear(branch_dim, 2)

    def forward(self, raw_out, lfcc_out, ssl_out):
        stacked = torch.stack([raw_out, lfcc_out, ssl_out], dim=1)
        attn_scores = self.attention(stacked).squeeze(-1)
        attn_weights = torch.softmax(attn_scores, dim=1)
        fused = (stacked * attn_weights.unsqueeze(-1)).sum(dim=1)
        return self.classifier(fused)

class MultiViewModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.raw_branch = RawBranch()
        self.lfcc_branch = LFCCBranch()
        self.ssl_branch = SSLBranch()
        self.fusion = AttentionFusion()

    def forward(self, raw, lfcc, ssl):
        raw_out = self.raw_branch(raw)
        lfcc_out = self.lfcc_branch(lfcc)
        ssl_out = self.ssl_branch(ssl)
        return self.fusion(raw_out, lfcc_out, ssl_out)

if __name__ == "__main__":
    model = MultiViewModel()
    model.eval()

    # Dummy inputs matching each branch's expected shape (batch size 1)
    dummy_raw = torch.randn(1, 1, 32000)
    dummy_lfcc = torch.randn(1, N_LFCC)
    dummy_ssl = torch.randn(1, 768)

    onnx_path = "ml/export/multiview_model.onnx"
    torch.onnx.export(
        model,
        (dummy_raw, dummy_lfcc, dummy_ssl),
        onnx_path,
        input_names=["raw", "lfcc", "ssl"],
        output_names=["logits"],
        dynamic_axes={"raw": {0: "batch"}, "lfcc": {0: "batch"}, "ssl": {0: "batch"}, "logits": {0: "batch"}},
        opset_version=14,
    )
    print(f"Exported ONNX model to: {onnx_path}")

    # Verify: does the exported ONNX model give the SAME output as the original PyTorch model?
    with torch.no_grad():
        torch_output = model(dummy_raw, dummy_lfcc, dummy_ssl).numpy()

    ort_session = ort.InferenceSession(onnx_path)
    onnx_output = ort_session.run(
        None,
        {
            "raw": dummy_raw.numpy(),
            "lfcc": dummy_lfcc.numpy(),
            "ssl": dummy_ssl.numpy(),
        },
    )[0]

    max_diff = np.max(np.abs(torch_output - onnx_output))
    print(f"PyTorch output: {torch_output}")
    print(f"ONNX output:    {onnx_output}")
    print(f"Max difference: {max_diff:.8f}")
    print("Export verified successfully!" if max_diff < 1e-4 else "WARNING: outputs differ significantly!")