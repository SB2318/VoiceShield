export const mockDecision = {
  call_id: "demo-001",
  number: "+91 98765 43210",
  timestamp: new Date().toISOString(),
  branch_scores: {
    rawnet2: 0.82,
    spectrogram: 0.75,
    ssl: 0.79
  },
  fused_score: 0.79,
  decision: "suspected_clone",
  challenge_type: "vocalization",
  challenge_result: "not_triggered",
  explanation:
    "Spectrogram branch flagged unnatural harmonic structure in the 2–4kHz band.",
  log_hash: "0xabc123..."
};


// ===============================
// DEMO: REAL VOICE
// ===============================

export const demoRealDecision = {
  call_id: "demo-real",
  number: "+91 98765 43210",
  timestamp: new Date().toISOString(),

  branch_scores: {
    rawnet2: 0.10,
    spectrogram: 0.14,
    ssl: 0.12
  },

  fused_score: 0.12,

  decision: "real",

  challenge_type: "vocalization",

  challenge_result: "passed",

  explanation:
    "Voice characteristics closely match the verified speaker across waveform, spectrogram, and SSL branches.",

  log_hash: "0xreal123..."
};


// ===============================
// DEMO: SUSPECTED CLONE
// ===============================

export const demoCloneDecision = {
  call_id: "demo-clone",
  number: "+91 98765 43210",
  timestamp: new Date().toISOString(),

  branch_scores: {
    rawnet2: 0.82,
    spectrogram: 0.75,
    ssl: 0.79
  },

  fused_score: 0.79,

  decision: "suspected_clone",

  challenge_type: "vocalization",

  challenge_result: "not_triggered",

  explanation:
    "Spectrogram branch flagged unnatural harmonic structure in the 2–4kHz band.",

  log_hash: "0xabc123..."
};


export const mockCallFeed = [
  {
    call_id: "demo-001",
    number: "+91 98765 43210",
    decision: "suspected_clone",
    fused_score: 0.79,
    timestamp: new Date().toISOString()
  },

  {
    call_id: "demo-002",
    number: "+91 91234 56789",
    decision: "unverified",
    fused_score: 0.52,
    timestamp: new Date().toISOString()
  },

  {
    call_id: "demo-003",
    number: "+91 99887 66554",
    decision: "real",
    fused_score: 0.12,
    timestamp: new Date().toISOString()
  },

  {
    call_id: "demo-004",
    number: "+91 90001 22334",
    decision: "speaker_mismatch",
    fused_score: 0.88,
    timestamp: new Date().toISOString()
  }
];


export const mockMetrics = {
  eer: 4.7,
  latencyMs: 340,
  fprAtThreshold: 2.1
};