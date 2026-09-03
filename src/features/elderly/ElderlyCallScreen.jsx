import { useRiskStream } from "../../hooks/useRiskStream";
import { riskConfig } from "../call/riskConfig";

function ElderlyCallScreen() {
  const { decision, setDemoScenario } = useRiskStream();

  const currentDecision = decision?.decision || "real";
  const currentNumber = decision?.number || "+91 98765 43210";
  const risk = riskConfig[currentDecision] || riskConfig.real;
  const isRisky = currentDecision !== "real";

  return (
    <div className="min-h-screen bg-canvas text-ink flex flex-col items-center justify-center gap-8 p-8 text-center relative">
      <div className="w-full max-w-lg flex flex-col items-center gap-6">
        <p className="text-ink-soft text-2xl font-medium">Incoming call from</p>
        <h1 className="font-display text-5xl md:text-6xl font-semibold tabular-nums tracking-tight">
          {currentNumber}
        </h1>

        <span
          className={`w-full max-w-sm px-8 py-5 rounded-2xl text-2xl md:text-3xl font-bold border-4 transition-all shadow-md ${
            risk.tone === "verified"
              ? "bg-sage/20 border-sage-deep text-sage-deep"
              : risk.tone === "caution"
              ? "bg-gold/25 border-gold-deep text-gold-deep"
              : risk.tone === "alert"
              ? "bg-terracotta/20 border-terracotta-deep text-terracotta-deep"
              : "bg-rose/20 border-rose text-rose"
          }`}
        >
          {risk.label}
        </span>

        {isRisky ? (
          <div className="max-w-md text-xl text-ink bg-white border-2 border-terracotta-deep/40 rounded-2xl p-6 leading-relaxed shadow-sm">
            <p className="font-semibold text-terracotta-deep mb-2 text-2xl">
              ⚠️ Warning
            </p>
            {decision?.explanation || "Unnatural voice features detected."}
          </div>
        ) : (
          <div className="max-w-md text-xl text-ink bg-white border-2 border-sage-deep/40 rounded-2xl p-6 leading-relaxed shadow-sm">
            <p className="font-semibold text-sage-deep mb-2 text-2xl">
              ✓ Voice Verified
            </p>
            This call matches your contact's natural speech patterns.
          </div>
        )}

        <button
          onClick={() => alert("Initiating safe callback procedure...")}
          className="w-full max-w-sm py-6 bg-terracotta-deep hover:bg-terracotta rounded-2xl text-2xl font-bold text-white transition-all shadow-lg active:scale-[0.98]"
        >
          Hang Up &amp; Call Back Safely
        </button>

        {/* Presentation Demo Controls */}
        <div className="mt-6 pt-6 border-t border-hairline w-full max-w-sm flex flex-col gap-3">
          <p className="text-xs font-semibold text-ink-soft uppercase tracking-wider">
            Demo Control Switch
          </p>
          <div className="flex gap-3">
            <button
              onClick={() => setDemoScenario("real")}
              className={`flex-1 py-3 px-4 rounded-xl text-sm font-bold border-2 transition-all ${
                !isRisky
                  ? "bg-sage-deep text-white border-sage-deep"
                  : "bg-white text-ink border-hairline hover:bg-canvas"
              }`}
            >
              Simulate Real
            </button>
            <button
              onClick={() => setDemoScenario("clone")}
              className={`flex-1 py-3 px-4 rounded-xl text-sm font-bold border-2 transition-all ${
                isRisky
                  ? "bg-terracotta-deep text-white border-terracotta-deep"
                  : "bg-white text-ink border-hairline hover:bg-canvas"
              }`}
            >
              Simulate Clone
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ElderlyCallScreen;