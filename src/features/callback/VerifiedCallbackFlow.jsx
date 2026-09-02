import { useState } from "react";
import { Card } from "../../ui/Card";
import { Label } from "../../ui/Label";
import { Badge } from "../../ui/Badge";
import { Button } from "../../ui/Button";
import { AuroraBackground } from "../../ui/AuroraBackground";
import CallScreen from "../call/CallScreen";

function VerifiedCallbackFlow() {
  const [step, setStep] = useState("risk");
  const number = "+91 90000 11223"; // placeholder unknown caller

  if (step === "protected") {
    return (
      <div className="min-h-screen text-ink flex flex-col items-center gap-3 p-6 relative">
        <AuroraBackground />
        <div className="relative z-10 w-full max-w-md text-center mb-2">
          <Badge tone="verified">Screened via VoiceShield callback</Badge>
        </div>
        <div className="relative z-10 w-full">
          <CallScreen embedded />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen text-ink flex flex-col items-center justify-center gap-7 p-6 relative">
      <AuroraBackground />
      <div className="w-full max-w-md flex flex-col items-center gap-6 relative z-10">

        {step === "risk" && (
          <>
            <Label>Incoming call</Label>
            <h1 className="font-display text-4xl font-semibold tabular-nums whitespace-nowrap">
              {number}
            </h1>
            <Badge tone="caution">Unrecognised number — no direct audio access</Badge>
            <Card className="w-full" hover>
              <p className="text-sm text-ink leading-relaxed">
                We can't hear this call directly — no app on your phone can, by design. If this
                could be someone claiming to be a known contact, you can verify safely instead.
              </p>
            </Card>
            <div className="flex gap-3 w-full">
              <Button variant="outline" className="flex-1">Answer anyway</Button>
              <Button variant="primary" className="flex-1" onClick={() => setStep("guidance")}>
                Verify first
              </Button>
            </div>
          </>
        )}

        {step === "guidance" && (
          <>
            <Label>Verify safely</Label>
            <Card className="w-full text-center" hover>
              <p className="text-ink text-sm leading-relaxed">
                Hang up now. VoiceShield will place a fresh call back through its own secure
                session — audio we can actually screen in real time.
              </p>
            </Card>
            <Button variant="primary" className="w-full" onClick={() => setStep("connecting")}>
              Hang up &amp; call back safely
            </Button>
          </>
        )}

        {step === "connecting" && (
          <>
            <Label>Placing callback</Label>
            <div className="animate-pulse">
              <Badge tone="caution">Connecting through VoiceShield…</Badge>
            </div>
            <Button variant="outline" onClick={() => setStep("protected")}>
              Simulate: call connected
            </Button>
          </>
        )}
      </div>
    </div>
  );
}
export default VerifiedCallbackFlow;
