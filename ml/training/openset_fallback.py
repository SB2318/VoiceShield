import torch

# Thresholds — tune these once you have real data and can see actual confidence distributions
CONFIDENCE_THRESHOLD = 0.65  # below this, we don't trust either "real" or "fake" guess

def classify_with_fallback(logits):
    """
    Takes raw model logits (shape: batch x 2) and returns a decision per sample:
    'real', 'suspected_clone', or 'unverified' — never a forced binary guess.
    """
    probs = torch.softmax(logits, dim=-1)  # (batch, 2) -> [prob_real, prob_fake]
    confidence, predicted_class = torch.max(probs, dim=-1)

    decisions = []
    for conf, pred_class in zip(confidence, predicted_class):
        if conf.item() < CONFIDENCE_THRESHOLD:
            decisions.append("unverified")
        elif pred_class.item() == 0:
            decisions.append("real")
        else:
            decisions.append("suspected_clone")
    return decisions, confidence.tolist()

if __name__ == "__main__":
    # Simulated logits standing in for real model output —
    # one confident-real, one confident-fake, one genuinely uncertain
    dummy_logits = torch.tensor([
        [4.0, 0.1],   # strongly predicts "real"
        [0.2, 3.8],   # strongly predicts "fake"
        [0.6, 0.5],   # nearly a coin flip -> should trigger "unverified"
    ])

    decisions, confidences = classify_with_fallback(dummy_logits)
    for i, (decision, conf) in enumerate(zip(decisions, confidences)):
        print(f"Sample {i}: decision='{decision}', confidence={conf:.4f}")