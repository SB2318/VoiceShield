import { useState } from "react";

function ConsentBanner() {
  const [dismissed, setDismissed] = useState(false);
  if (dismissed) return null;

  return (
    <div className="bg-[#5B8DEF]/10 border-y border-[#5B8DEF]/30 text-[#B8CBF5] text-xs px-4 py-2.5 flex justify-between items-center gap-3">
      <span className="leading-relaxed">
        This call may be screened by VoiceShield for voice-authenticity verification.
      </span>
      <button
        onClick={() => setDismissed(true)}
        className="underline underline-offset-2 shrink-0 hover:text-white transition-colors font-medium"
      >
        Acknowledge
      </button>
    </div>
  );
}
export default ConsentBanner;
