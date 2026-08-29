function MetricsPanel({ metrics }) {
  const items = [
    { label: "EER", value: `${metrics.eer}%` },
    { label: "Latency", value: `${metrics.latencyMs}ms` },
    { label: "FPR @ Threshold", value: `${metrics.fprAtThreshold}%` },
  ];

  return (
    <div className="grid grid-cols-3 gap-4">
      {items.map((item) => (
        <div key={item.label} className="bg-slate-800 rounded-lg p-4 text-center border border-slate-700">
          <p className="text-slate-400 text-xs uppercase tracking-wide">{item.label}</p>
          <p className="text-white text-2xl font-bold mt-1">{item.value}</p>
        </div>
      ))}
    </div>
  );
}

export default MetricsPanel;