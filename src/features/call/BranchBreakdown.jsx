import { Card } from "../../ui/Card";
import { Label } from "../../ui/Label";

function BranchBreakdown({ branchScores }) {
  const branches = [
    { key: "rawnet2", label: "RawNet2 · waveform" },
    { key: "spectrogram", label: "ResNet2D · spectrogram" },
    { key: "ssl", label: "WavLM · SSL embedding" },
  ];
  if (!branches.some((b) => branchScores?.[b.key] != null)) return null;

  return (
    <Card className="w-full max-w-sm">
      <Label className="mb-3">Why this decision — per-branch scores</Label>
      <div className="flex flex-col gap-3">
        {branches.map((b) => (
          <div key={b.key}>
            <div className="flex justify-between text-xs text-ink-soft mb-1.5 font-medium">
              <span>{b.label}</span>
              <span className="font-mono text-ink">{((branchScores[b.key] ?? 0) * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full bg-raised rounded-full h-2 overflow-hidden">
              <div className="h-full rounded-full bg-gradient-to-r from-terracotta to-sage-deep transition-all duration-500"
                style={{ width: `${(branchScores[b.key] ?? 0) * 100}%` }} />
            </div>
          </div>
        ))}
      </div>
      <p className="text-[11px] text-ink-faint mt-3 leading-relaxed">
        Disagreement between branches escalates to a live challenge.
      </p>
    </Card>
  );
}
export default BranchBreakdown;