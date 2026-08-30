import { useState } from "react";
import { useRiskStream } from "../../hooks/useRiskStream";
import { riskConfig } from "./riskConfig";
import ChallengeCard from "../Challenge/ChallengeCard";
import PanicCard from "../PanicMode/PanicCard";
import BranchBreakdown from "./BranchBreakdown";

function CallScreen({ embedded = false }) {
  const { decision, status } = useRiskStream();
  const [showPanic, setShowPanic] = useState(false);
  const risk = riskConfig[decision.decision];

  // Signature element: a voice-equalizer-style meter instead of a flat bar.
  // Bar heights are deterministic from the score so it doesn't jitter on
  // every re-render, but still reads as "live audio," not a loading bar.
  const barCount = 24;
  const bars = Array.from({ length: barCount }, (_, i) => {
    const seed = Math.sin(i * 12.9898 + decision.fused_score * 78.233) * 43758.5453;
    const wobble = seed - Math.floor(seed); // 0–1 pseudo-random, stable per score
    const active = i / barCount < decision.fused_score;
    const height = active ? 20 + wobble * 80 : 12 + wobble * 10;
    return { height, active };
  });

  return (
    <div
      className={
        embedded
          ? "text-[#E8ECF4] flex flex-col items-center gap-6 p-4"
          : "min-h-screen bg-[#0B0F19] text-[#E8ECF4] flex flex-col items-center justify-center gap-6 p-6"
      }
    >
      <div className="w-full max-w-md flex flex-col items-center gap-6">

        {/* Status line */}
        <div className="flex flex-col items-center gap-1">
          <p className="text-[10px] font-semibold tracking-[0.2em] text-[#8993A8] uppercase">
            Incoming call
          </p>
          {status === "error" && (
            <p className="text-red-400 text-xs">⚠ Connection lost — showing last known state</p>
          )}
          {status === "connecting" && (
            <p className="text-[#5B8DEF] text-xs animate-pulse">Connecting to detection service…</p>
          )}
        </div>

        {/* Number + risk badge, given real visual weight */}
        <div className="flex flex-col items-center gap-3">
          <h1 className="text-3xl font-semibold font-mono tracking-tight">
            {decision.number}
          </h1>
          <span
            className={`px-4 py-1.5 rounded-full text-xs font-semibold tracking-wide uppercase ${risk.color}`}
          >
            {risk.label}
          </span>
        </div>

        {/* Signature equalizer-style confidence meter */}
        <div className="w-full flex flex-col items-center gap-2">
          <div className="flex items-end gap-[3px] h-16 w-full max-w-xs justify-center">
            {bars.map((bar, i) => (
              <div
                key={i}
                className={`w-1.5 rounded-full transition-all duration-500 ${
                  bar.active ? "bg-[#5B8DEF]" : "bg-[#232B3D]"
                }`}
                style={{ height: `${bar.height}%` }}
              />
            ))}
          </div>
          <p className="text-sm text-[#8993A8] font-mono">
            confidence <span className="text-[#E8ECF4]">{(decision.fused_score * 100).toFixed(1)}%</span>
          </p>
        </div>

        {/* Explanation card — real elevation, not a flat box */}
        <div className="w-full bg-[#131826] border border-[#232B3D] rounded-xl p-4 shadow-lg shadow-black/30">
          <p className="text-[10px] font-semibold tracking-[0.15em] text-[#8993A8] uppercase mb-2">
            Why this decision
          </p>
          <p className="text-sm text-[#E8ECF4] leading-relaxed">
            {decision.explanation}
          </p>
        </div>

        <ChallengeCard
          challengeType={decision.challenge_type}
          onResult={(res) => console.log("Challenge result:", res)}
        />

        <BranchBreakdown branchScores={decision.branch_scores} />

        {!showPanic ? (
          <button
            onClick={() => setShowPanic(true)}
            className="text-xs text-[#8993A8] hover:text-[#5B8DEF] underline underline-offset-4 transition-colors"
          >
            Simulate: this looks like an emotional/panic-inducing call
          </button>
        ) : (
          <PanicCard />
        )}
      </div>
    </div>
  );
}

export default CallScreen;
