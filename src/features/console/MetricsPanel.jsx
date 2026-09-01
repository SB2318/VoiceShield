function MetricsPanel({ metrics }) {
  const items = [
    { label: "EER", value: `${metrics.eer}%` },
    { label: "Latency", value: `${metrics.latencyMs}ms` },
    { label: "FPR @ threshold", value: `${metrics.fprAtThreshold}%` },
  ];

  return (
    <div className="grid grid-cols-3 gap-4">
      {items.map((item) => (
        <div
          key={item.label}
          className="bg-[#131826] border border-[#232B3D] rounded-xl p-5 shadow-lg shadow-black/20"
        >
          <p className="text-[#8993A8] text-[10px] font-semibold uppercase tracking-[0.15em]">
            {item.label}
          </p>
          <p className="text-[#E8ECF4] text-3xl font-semibold font-mono mt-2">
            {item.value}
          </p>
        </div>
      ))}
    </div>
  );
}
export default MetricsPanel;
