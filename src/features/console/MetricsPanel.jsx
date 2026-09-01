import { Stat } from "../../ui/Stat";
function MetricsPanel({ metrics }) {
  const items = [
    { label: "EER", value: metrics.eer, unit: "%" },
    { label: "Latency", value: metrics.latencyMs, unit: "ms" },
    { label: "FPR @ threshold", value: metrics.fprAtThreshold, unit: "%" },
  ];
  return (
    <div className="grid grid-cols-3 gap-4">
      {items.map((i) => <Stat key={i.label} {...i} />)}
    </div>
  );
}
export default MetricsPanel;