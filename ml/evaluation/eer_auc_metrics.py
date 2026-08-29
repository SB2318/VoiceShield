import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score

def compute_eer(labels, scores):
    """
    EER = Equal Error Rate — the point where false-accept rate equals false-reject rate.
    labels: 0 = real, 1 = fake (spoof)
    scores: model's predicted probability of being "fake" (higher = more suspicious)
    """
    fpr, tpr, thresholds = roc_curve(labels, scores, pos_label=1)
    fnr = 1 - tpr
    # EER is where FPR and FNR curves cross
    eer_threshold_idx = np.nanargmin(np.abs(fpr - fnr))
    eer = (fpr[eer_threshold_idx] + fnr[eer_threshold_idx]) / 2
    eer_threshold = thresholds[eer_threshold_idx]
    return eer, eer_threshold

def compute_auc(labels, scores):
    return roc_auc_score(labels, scores)

def compute_fpr_at_threshold(labels, scores, threshold):
    """FPR at a SPECIFIC decision threshold — what your team's plan calls the 'operating point'."""
    predictions = (np.array(scores) >= threshold).astype(int)
    labels = np.array(labels)
    false_positives = np.sum((predictions == 1) & (labels == 0))
    true_negatives = np.sum((predictions == 0) & (labels == 0))
    fpr = false_positives / (false_positives + true_negatives) if (false_positives + true_negatives) > 0 else 0.0
    return fpr

if __name__ == "__main__":
    # Simulated labels + scores standing in for real model output —
    # mostly separable, with some overlap, to produce a realistic-looking EER
    np.random.seed(42)
    real_scores = np.random.normal(loc=0.2, scale=0.15, size=50)   # real speech -> low fake-probability
    fake_scores = np.random.normal(loc=0.8, scale=0.15, size=50)   # spoofed speech -> high fake-probability

    labels = [0] * 50 + [1] * 50
    scores = np.concatenate([real_scores, fake_scores])
    scores = np.clip(scores, 0, 1)

    eer, eer_threshold = compute_eer(labels, scores)
    auc = compute_auc(labels, scores)
    fpr_at_05 = compute_fpr_at_threshold(labels, scores, threshold=0.5)

    print(f"EER: {eer*100:.2f}% (at threshold {eer_threshold:.4f})")
    print(f"AUC: {auc:.4f}")
    print(f"FPR at threshold 0.5: {fpr_at_05*100:.2f}%")