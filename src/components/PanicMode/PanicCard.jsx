import { useState, useEffect } from "react";
import { guidedSteps } from "./guidedSteps";

function PanicCard() {
  const [cooldown, setCooldown] = useState(8);
  const [safeWordSet, setSafeWordSet] = useState(false);
  const [safeWord, setSafeWord] = useState("");

  useEffect(() => {
    if (cooldown <= 0) return;
    const timer = setTimeout(() => setCooldown((c) => c - 1), 1000);
    return () => clearTimeout(timer);
  }, [cooldown]);

  return (
    <div className="w-96 bg-slate-800 rounded-xl p-6 flex flex-col gap-5 border border-sky-800/40">
      <div className="text-center">
        <p className="text-sky-300 text-xs uppercase tracking-wide mb-1">
          Possible impersonation detected
        </p>
        <p className="text-slate-200 text-sm">
          There are signs this voice may not be genuine. It's okay to pause and verify with another number.
        </p>
      </div>

      {/* Guided verification checklist */}
      <div className="bg-slate-900/60 rounded-lg p-4">
        <p className="text-slate-400 text-xs uppercase tracking-wide mb-2">
          Before you act, try one of these
        </p>
        <ol className="text-slate-200 text-sm space-y-2 list-decimal list-inside">
          {guidedSteps.map((step, i) => (
            <li key={i}>{step}</li>
          ))}
        </ol>
      </div>

      {/* Safe word setup */}
      <div className="bg-slate-900/60 rounded-lg p-4">
        <p className="text-slate-400 text-xs uppercase tracking-wide mb-2">
          Family safe word
        </p>
        {!safeWordSet ? (
          <div className="flex gap-2">
            <input
              value={safeWord}
              onChange={(e) => setSafeWord(e.target.value)}
              placeholder="Set a private word"
              className="flex-1 bg-slate-800 text-sm rounded-md px-3 py-2 text-white placeholder-slate-500 outline-none border border-slate-700 focus:border-sky-500"
            />
            <button
              onClick={() => safeWord.trim() && setSafeWordSet(true)}
              className="px-3 py-2 bg-sky-700 hover:bg-sky-600 rounded-md text-sm font-medium"
            >
              Save
            </button>
          </div>
        ) : (
          <p className="text-sky-300 text-sm">✓ Safe word set. Ask for it if a call feels wrong.</p>
        )}
      </div>

      {/* Trusted contact silent escalation */}
      <div className="bg-slate-900/60 rounded-lg p-4 flex items-center justify-between">
        <p className="text-slate-300 text-sm">Notify a trusted contact quietly</p>
        <button className="px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded-md text-xs font-medium">
          Notify
        </button>
      </div>

      {/* Cooldown before any high-risk action */}
      <div className="text-center">
        <button
          disabled={cooldown > 0}
          className={`w-full py-2 rounded-lg text-sm font-medium transition ${
            cooldown > 0
              ? "bg-slate-700 text-slate-400 cursor-not-allowed"
              : "bg-sky-600 hover:bg-sky-500 text-white"
          }`}
        >
          {cooldown > 0 ? `Please wait ${cooldown}s before continuing` : "Continue"}
        </button>
      </div>
    </div>
  );
}

export default PanicCard;