import { useState } from "react";
import { challengePrompts } from "./challengePrompts";

function ChallengeCard({ challengeType, onResult }) {
  const [result, setResult] = useState("not_triggered");
  const challenge = challengePrompts[challengeType] || challengePrompts.none;

  if (challengeType === "none") return null;

  return (
    <div className="w-80 bg-slate-800 rounded-xl p-5 flex flex-col items-center gap-4 border border-slate-700">
      <p className="text-slate-400 text-xs uppercase tracking-wide">{challenge.title}</p>
      <p className="text-white text-center font-medium">{challenge.prompt}</p>

      {result === "not_triggered" && (
        <div className="flex gap-3">
          <button
            onClick={() => { setResult("pass"); onResult?.("pass"); }}
            className="px-4 py-2 bg-green-600 hover:bg-green-500 rounded-lg text-sm font-medium"
          >
            Simulate Pass
          </button>
          <button
            onClick={() => { setResult("fail"); onResult?.("fail"); }}
            className="px-4 py-2 bg-red-600 hover:bg-red-500 rounded-lg text-sm font-medium"
          >
            Simulate Fail
          </button>
        </div>
      )}

      {result === "pass" && (
        <p className="text-green-400 font-semibold">✅ Challenge passed</p>
      )}
      {result === "fail" && (
        <p className="text-red-400 font-semibold">❌ Challenge failed</p>
      )}
    </div>
  );
}

export default ChallengeCard;