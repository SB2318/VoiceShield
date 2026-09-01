import { useState } from "react";
import { challengePrompts } from "./challengePrompts";

function ChallengeCard({ challengeType, onResult }) {
  const [result, setResult] = useState("not_triggered");
  const challenge = challengePrompts[challengeType] || challengePrompts.none;

  if (challengeType === "none") return null;

  return (
    <div className="w-full max-w-xs bg-[#131826] border border-[#232B3D] rounded-xl p-5 flex flex-col items-center gap-4 shadow-lg shadow-black/30">
      <p className="text-[10px] font-semibold tracking-[0.15em] text-[#8993A8] uppercase">
        {challenge.title}
      </p>

      <p className="text-[#E8ECF4] text-center font-medium leading-snug">
        {challenge.prompt}
      </p>

      {result === "not_triggered" && (
        <div className="flex gap-3 w-full">
          <button
            onClick={() => { setResult("pass"); onResult?.("pass"); }}
            className="flex-1 px-4 py-2 bg-emerald-600/90 hover:bg-emerald-500 text-white rounded-lg text-sm font-medium transition-colors"
          >
            Simulate pass
          </button>
          <button
            onClick={() => { setResult("fail"); onResult?.("fail"); }}
            className="flex-1 px-4 py-2 bg-red-600/90 hover:bg-red-500 text-white rounded-lg text-sm font-medium transition-colors"
          >
            Simulate fail
          </button>
        </div>
      )}

      {result === "pass" && (
        <div className="flex items-center gap-2 text-emerald-400 font-semibold text-sm">
          <span className="w-2 h-2 rounded-full bg-emerald-400" />
          Challenge passed
        </div>
      )}

      {result === "fail" && (
        <div className="flex items-center gap-2 text-red-400 font-semibold text-sm">
          <span className="w-2 h-2 rounded-full bg-red-400" />
          Challenge failed
        </div>
      )}
    </div>
  );
}

export default ChallengeCard;
