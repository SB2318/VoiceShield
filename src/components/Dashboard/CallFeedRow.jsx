import { riskConfig } from "../CallScreen/riskConfig";

function CallFeedRow({ call, onOverride }) {
  const risk = riskConfig[call.decision];

  return (
    <div className="flex items-center justify-between bg-slate-800 rounded-lg px-4 py-3 border border-slate-700">
      <div>
        <p className="text-white text-sm font-medium">{call.number}</p>
        <p className="text-slate-500 text-xs">{call.call_id}</p>
      </div>

      <span className={`px-3 py-1 rounded-full text-xs font-medium ${risk.color}`}>
        {risk.label}
      </span>

      <p className="text-slate-300 text-sm w-16 text-right">
        {(call.fused_score * 100).toFixed(0)}%
      </p>

      <div className="flex gap-2">
        <button
          onClick={() => onOverride?.(call.call_id, "confirmed")}
          className="px-3 py-1 bg-green-700 hover:bg-green-600 rounded-md text-xs"
        >
          Confirm
        </button>
        <button
          onClick={() => onOverride?.(call.call_id, "overridden")}
          className="px-3 py-1 bg-slate-600 hover:bg-slate-500 rounded-md text-xs"
        >
          Override
        </button>
      </div>
    </div>
  );
}

export default CallFeedRow;