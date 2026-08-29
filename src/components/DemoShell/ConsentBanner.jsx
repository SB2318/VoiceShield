import { useState } from "react";

function ConsentBanner() {
  const [dismissed, setDismissed] = useState(false);
  if (dismissed) return null;

  return (
    <div className="bg-amber-900/40 border border-amber-700/50 text-amber-200 text-xs px-4 py-2 flex justify-between items-center">
      <span>🔔 This call may be screened by VoiceShield for voice-authenticity verification.</span>
      <button onClick={() => setDismissed(true)} className="underline ml-2 shrink-0">
        Acknowledge
      </button>
    </div>
  );
}

export default ConsentBanner;