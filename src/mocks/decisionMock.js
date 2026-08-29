export const mockDecision = {
  call_id: "demo-001",
  number: "+91 98765 43210",
  timestamp: new Date().toISOString(),
  branch_scores: { rawnet2: 0.82, spectrogram: 0.75, ssl: 0.79 },
  fused_score: 0.79,
  decision: "suspected_clone", // real | unverified | suspected_clone | speaker_mismatch
  challenge_type: "vocalization", // phrase | prosody | acoustic | vocalization | semantic | none
  challenge_result: "not_triggered", // pass | fail | not_triggered
  explanation: "Spectrogram branch flagged unnatural harmonic structure in the 2–4kHz band.",
  log_hash: "0xabc123..."
};