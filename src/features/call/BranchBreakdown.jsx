function BranchBreakdown({ branchScores }) {
  const branches = [
    { key: "rawnet2", label: "RawNet2 (waveform)" },
    { key: "spectrogram", label: "Spectrogram (ResNet2D)" },
    { key: "ssl", label: "SSL Embedding (WavLM)" },
  ];

  const hasData = branches.some((b) => branchScores?.[b.key] != null);
  if (!hasData) return null;

  return (
    <div className="w-full max-w-sm bg-slate-800 rounded-lg p-4 border border-slate-700">
      <p className="text-slate-400 text-xs uppercase tracking-wide mb-3">
        Why this decision — per-branch scores
      </p>
      <div className="flex flex-col gap-2">
        {branches.map((b) => (
          <div key={b.key}>
            <div className="flex justify-between text-xs text-slate-300 mb-1">
              <span>{b.label}</span>
              <span>{((branchScores[b.key] ?? 0) * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full bg-slate-700 rounded-full h-2 overflow-hidden">
              <div
                className="h-full bg-purple-500"
                style={{ width: `${(branchScores[b.key] ?? 0) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default BranchBreakdown;