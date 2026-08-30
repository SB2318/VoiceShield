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
    <div className="w-full max-w-md bg-[#131826] border border-[#5B8DEF]/30 rounded-xl p-6 flex flex-col gap-5 shadow-lg shadow-black/30">
      <div className="text-center">
        <p className="text-[#5B8DEF] text-[10px] font-semibold uppercase tracking-[0.15em] mb-1.5">
          Possible impersonation detected
        </p>
        <p className="text-[#E8ECF4] text-sm leading-relaxed">
          There are signs this voice may not be genuine. It's okay to pause and verify with another number.
        </p>
      </div>

      {/* Guided verification checklist */}
      <div className="bg-[#0B0F19] border border-[#232B3D] rounded-lg p-4">
        <p className="text-[#8993A8] text-[10px] font-semibold uppercase tracking-[0.15em] mb-3">
          Before you act, try one of these
        </p>
        <ol className="text-[#E8ECF4] text-sm space-y-2.5">
          {guidedSteps.map((step, i) => (
            <li key={i} className="flex gap-3">
              <span className="font-mono text-[#5B8DEF] text-xs mt-0.5">{String(i + 1).padStart(2, "0")}</span>
              <span>{step}</span>
            </li>
          ))}
        </ol>
      </div>

      {/* Safe word setup */}
      <div className="bg-[#0B0F19] border border-[#232B3D] rounded-lg p-4">
        <p className="text-[#8993A8] text-[10px] font-semibold uppercase tracking-[0.15em] mb-3">
          Family safe word
        </p>
        {!safeWordSet ? (
          <div className="flex gap-2">
            <input
              value={safeWord}
              onChange={(e) => setSafeWord(e.target.value)}
              placeholder="Set a private word"
              className="flex-1 bg-[#131826] text-sm rounded-md px-3 py-2 text-[#E8ECF4] placeholder-[#5A6478] outline-none border border-[#232B3D] focus:border-[#5B8DEF] transition-colors"
            />
            <button
              onClick={() => safeWord.trim() && setSafeWordSet(true)}
              className="px-4 py-2 bg-[#5B8DEF] hover:bg-[#4A7CE0] text-white rounded-md text-sm font-medium transition-colors"
            >
              Save
            </button>
          </div>
        ) : (
          <div className="flex items-center gap-2 text-[#5B8DEF] text-sm">
            <span className="w-1.5 h-1.5 rounded-full bg-[#5B8DEF]" />
            Safe word set. Ask for it if a call feels wrong.
          </div>
        )}
      </div>

      {/* Trusted contact silent escalation */}
      <div className="bg-[#0B0F19] border border-[#232B3D] rounded-lg p-4 flex items-center justify-between">
        <p className="text-[#E8ECF4] text-sm">Notify a trusted contact quietly</p>
        <button className="px-3.5 py-2 bg-[#1A2030] hover:bg-[#232B3D] border border-[#232B3D] rounded-md text-xs font-medium text-[#E8ECF4] transition-colors">
          Notify
        </button>
      </div>

      {/* Cooldown before any high-risk action */}
      <div className="text-center">
        <button
          disabled={cooldown > 0}
          className={`w-full py-2.5 rounded-lg text-sm font-medium font-mono transition-colors ${
            cooldown > 0
              ? "bg-[#0B0F19] border border-[#232B3D] text-[#5A6478] cursor-not-allowed"
              : "bg-[#5B8DEF] hover:bg-[#4A7CE0] text-white"
          }`}
        >
          {cooldown > 0 ? `Please wait ${cooldown}s before continuing` : "Continue"}
        </button>
      </div>
    </div>
  );
}

export default PanicCard;
