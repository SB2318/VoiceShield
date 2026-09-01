import { useState, useEffect } from "react";
import { guidedSteps } from "./guidedSteps";
import { Card } from "../../ui/Card";
import { Label } from "../../ui/Label";
import { Button } from "../../ui/Button";

function PanicCard() {
  const [cooldown, setCooldown] = useState(8);
  const [safeWordSet, setSafeWordSet] = useState(false);
  const [safeWord, setSafeWord] = useState("");

  useEffect(() => {
    if (cooldown <= 0) return;
    const t = setTimeout(() => setCooldown((c) => c - 1), 1000);
    return () => clearTimeout(t);
  }, [cooldown]);

  return (
    <Card className="w-full max-w-md flex flex-col gap-5 !border-terracotta/25">
      <div className="text-center">
        <Label className="!text-terracotta-deep mb-1.5">Possible impersonation detected</Label>
        <p className="text-ink text-sm leading-relaxed">
          There are signs this voice may not be genuine. It's okay to pause and verify with another number.
        </p>
      </div>
      <div className="bg-raised/60 border border-hairline rounded-xl p-4">
        <Label className="mb-3">Before you act, try one of these</Label>
        <ol className="text-ink text-sm space-y-2.5">
          {guidedSteps.map((step, i) => (
            <li key={i} className="flex gap-3">
              <span className="font-mono text-terracotta-deep text-xs mt-0.5 font-bold">{String(i + 1).padStart(2, "0")}</span>
              <span>{step}</span>
            </li>
          ))}
        </ol>
      </div>
      <div className="bg-raised/60 border border-hairline rounded-xl p-4">
        <Label className="mb-3">Family safe word</Label>
        {!safeWordSet ? (
          <div className="flex gap-2">
            <input value={safeWord} onChange={(e) => setSafeWord(e.target.value)} placeholder="Set a private word"
              className="flex-1 bg-white text-sm rounded-lg px-3 py-2 text-ink placeholder-ink-faint outline-none border border-hairline focus:border-terracotta transition-colors" />
            <Button variant="primary" onClick={() => safeWord.trim() && setSafeWordSet(true)}>Save</Button>
          </div>
        ) : (
          <div className="flex items-center gap-2 text-terracotta-deep text-sm font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-terracotta" />Safe word set. Ask for it if a call feels wrong.
          </div>
        )}
      </div>
      <div className="bg-raised/60 border border-hairline rounded-xl p-4 flex items-center justify-between">
        <p className="text-ink text-sm font-medium">Notify a trusted contact quietly</p>
        <Button variant="outline">Notify</Button>
      </div>
      <div className="text-center">
        <button disabled={cooldown > 0}
          className={`w-full py-3 rounded-xl text-sm font-bold font-mono transition-all ${
            cooldown > 0 ? "bg-raised text-ink-faint cursor-not-allowed"
                         : "bg-gradient-to-r from-terracotta to-terracotta-deep text-white glow-terracotta"}`}>
          {cooldown > 0 ? `Please wait ${cooldown}s before continuing` : "Continue"}
        </button>
      </div>
    </Card>
  );
}
export default PanicCard;