import { useState, useEffect } from "react";
import { mockDecision } from "../../mocks/decisionMock";
import { riskConfig } from "./riskConfig";
import ChallengeCard from "../Challenge/ChallengeCard";
import PanicCard from "../PanicMode/PanicCard";

function CallScreen({ embedded = false }) {
  const [score, setScore] = useState(mockDecision.fused_score);
  const [showPanic, setShowPanic] = useState(false);
  const risk = riskConfig[mockDecision.decision];

  useEffect(() => {
    const interval = setInterval(() => {
      setScore((prev) => {
        const jitter = (Math.random() - 0.5) * 0.05;
        return Math.min(1, Math.max(0, prev + jitter));
      });
    }, 300);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className={
      embedded
        ? "text-white flex flex-col items-center gap-5 p-4"
        : "min-h-screen bg-slate-900 text-white flex flex-col items-center justify-center gap-6 p-6"
    }>
      <p className="text-slate-400 text-sm">Incoming call</p>
      <h1 className="text-2xl font-semibold">{mockDecision.number}</h1>

      <span className={`px-4 py-1 rounded-full text-sm font-medium ${risk.color}`}>
        {risk.label}
      </span>

      <div className="w-64 bg-slate-700 rounded-full h-3 overflow-hidden">
        <div
          className="h-full bg-blue-500 transition-all duration-300"
          style={{ width: `${score * 100}%` }}
        />
      </div>
      <p className="text-sm text-slate-400">Confidence score: {(score * 100).toFixed(1)}%</p>

      <p className="max-w-sm text-center text-slate-300 text-sm bg-slate-800 rounded-lg p-3">
        {mockDecision.explanation}
      </p>

      <ChallengeCard
        challengeType={mockDecision.challenge_type}
        onResult={(res) => console.log("Challenge result:", res)}
      />

      {!showPanic ? (
        <button
          onClick={() => setShowPanic(true)}
          className="text-xs text-slate-500 underline"
        >
          Simulate: this looks like an emotional/panic-inducing call
        </button>
      ) : (
        <PanicCard />
      )}
    </div>
  );
}

export default CallScreen;