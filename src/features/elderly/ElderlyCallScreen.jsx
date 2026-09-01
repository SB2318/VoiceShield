import { mockDecision } from "../../fixtures/decisions";
import { riskConfig } from "../call/riskConfig";

function ElderlyCallScreen() {
  const risk = riskConfig[mockDecision.decision];

  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col items-center justify-center gap-8 p-8 text-center">
      <p className="text-slate-400 text-xl">Incoming call from</p>
      <h1 className="text-5xl font-bold">{mockDecision.number}</h1>

      <span className={`px-8 py-4 rounded-2xl text-2xl font-bold ${risk.color}`}>
        {risk.label === "Suspected Clone" ? "⚠️ This may not be a real voice" : risk.label}
      </span>

      <p className="max-w-md text-xl text-slate-200 bg-slate-800 rounded-2xl p-6">
        {mockDecision.explanation}
      </p>

      <button className="w-full max-w-sm py-6 bg-sky-600 hover:bg-sky-500 rounded-2xl text-2xl font-bold">
        Hang Up & Call Back Safely
      </button>
    </div>
  );
}

export default ElderlyCallScreen;