import { useState } from "react";

function ConsentBanner() {
  const [dismissed, setDismissed] = useState(false);
  if (dismissed) return null;
  return (
    <div className="bg-sage/12 border-y border-sage/30 text-sage-deep text-xs px-4 py-2.5 flex justify-between items-center gap-3">
      <span className="leading-relaxed">This call may be screened by VoiceShield for voice-authenticity verification.</span>
      <button onClick={() => setDismissed(true)} className="underline underline-offset-2 shrink-0 hover:text-terracotta-deep transition-colors font-semibold">
        Acknowledge
      </button>
    </div>
  );
}
export default ConsentBanner;