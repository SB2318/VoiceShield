import { riskConfig } from "../call/riskConfig";
import { Badge } from "../../ui/Badge";
import { Button } from "../../ui/Button";

function CallFeedRow({ call, onOverride }) {
  const risk = riskConfig[call.decision];
  return (
    <div className="glass rounded-2xl px-5 py-4 flex items-center justify-between shadow-[0_4px_20px_-10px_rgba(61,64,91,0.15)] card-hover">
      <div>
        <p className="text-ink text-sm font-semibold font-mono">{call.number}</p>
        <p className="text-ink-faint text-xs mt-0.5">{call.call_id}</p>
      </div>
      <Badge tone={risk.tone}>{risk.label}</Badge>
      <p className="text-ink text-sm w-16 text-right font-mono font-semibold">{(call.fused_score * 100).toFixed(0)}%</p>
      <div className="flex gap-2">
        <Button variant="sage" className="!px-3 !py-1.5 !text-xs" onClick={() => onOverride?.(call.call_id, "confirmed")}>Confirm</Button>
        <Button variant="outline" className="!px-3 !py-1.5 !text-xs" onClick={() => onOverride?.(call.call_id, "overridden")}>Override</Button>
      </div>
    </div>
  );
}
export default CallFeedRow;