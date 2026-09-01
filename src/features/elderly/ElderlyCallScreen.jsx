import { useRiskStream } from "../../hooks/useRiskStream";
import { riskConfig } from "../call/riskConfig";

function ElderlyCallScreen() {
  const { decision } = useRiskStream();
  const risk = riskConfig[decision.decision];
  const isRisky = decision.decision !== "real";

  return (
    <div className="min-h-screen bg-canvas text-ink flex flex-col items-center justify-center gap-8 p-8 text-center">
      <p className="text-ink-soft text-2xl font-medium">Incoming call from</p>
      <h1 className="font-display text-6xl font-semibold tabular-nums">{decision.number}</h1>

      <span className={`px-8 py-4 rounded-2xl text-2xl font-bold border-2 ${
        risk.tone === "verified" ? "bg-sage/20 border-sage-deep text-sage-deep" :
        risk.tone === "caution"  ? "bg-gold/25 border-gold-deep text-gold-deep" :
        risk.tone === "alert"    ? "bg-terracotta/20 border-terracotta-deep text-terracotta-deep" :
                                    "bg-rose/20 border-rose text-rose"
      }`}>
        {risk.label}
      </span>

      {isRisky && (
        <p className="max-w-md text-xl text-ink bg-white border-2 border-hairline rounded-2xl p-6 leading-relaxed">
          {decision.explanation}
        </p>
      )}

      <button className="w-full max-w-sm py-6 bg-terracotta-deep hover:bg-terracotta rounded-2xl text-2xl font-bold text-white transition-colors">
        Hang Up &amp; Call Back Safely
      </button>
    </div>
  );
}
export default ElderlyCallScreen;