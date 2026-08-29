import torch
import torch.nn as nn

class CrossBranchAgreementGate(nn.Module):
    """
    Compares each branch's independent prediction. If branches disagree strongly,
    flags the sample as 'escalate to challenge' instead of trusting the fused score.
    """
    def __init__(self, branch_dim=32, disagreement_threshold=0.3):
        super().__init__()
        # Each branch gets its own small classifier head so it can vote independently
        self.raw_head = nn.Linear(branch_dim, 2)
        self.lfcc_head = nn.Linear(branch_dim, 2)
        self.ssl_head = nn.Linear(branch_dim, 2)
        self.disagreement_threshold = disagreement_threshold

    def forward(self, raw_out, lfcc_out, ssl_out):
        # Each branch independently predicts spoof-probability
        raw_probs = torch.softmax(self.raw_head(raw_out), dim=-1)[:, 1]   # prob of "fake"
        lfcc_probs = torch.softmax(self.lfcc_head(lfcc_out), dim=-1)[:, 1]
        ssl_probs = torch.softmax(self.ssl_head(ssl_out), dim=-1)[:, 1]

        stacked_probs = torch.stack([raw_probs, lfcc_probs, ssl_probs], dim=1)  # (batch, 3)

        # Disagreement = how spread out the branch opinions are
        disagreement = stacked_probs.std(dim=1)  # (batch,)
        escalate = disagreement > self.disagreement_threshold  # bool per sample

        return stacked_probs, disagreement, escalate


if __name__ == "__main__":
    # Quick sanity test with fake numbers standing in for real branch outputs
    dummy_raw = torch.randn(4, 32)
    dummy_lfcc = torch.randn(4, 32)
    dummy_ssl = torch.randn(4, 32)

    gate = CrossBranchAgreementGate()
    probs, disagreement, escalate = gate(dummy_raw, dummy_lfcc, dummy_ssl)

    print("Per-branch probabilities:\n", probs)
    print("Disagreement scores:\n", disagreement)
    print("Escalate to challenge?:\n", escalate)