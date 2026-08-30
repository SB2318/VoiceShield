function WhatsAppBotDemo() {
  return (
    <div className="max-w-sm mx-auto bg-[#0b141a] rounded-2xl p-4 border border-[#232B3D]">
      <p className="text-[#8993A8] text-[10px] font-semibold uppercase tracking-[0.15em] mb-3">
        WhatsApp — VoiceShield Bot
      </p>
      <div className="flex flex-col gap-2">
        <div className="self-end bg-[#005c4b] text-white text-sm rounded-lg px-3 py-2 max-w-[80%] leading-relaxed">
          🎙️ Voice note forwarded — 0:14
        </div>
        <div className="self-start bg-[#202c33] text-white text-sm rounded-lg px-3 py-2 max-w-[85%] leading-relaxed">
          <span className="text-amber-400 font-medium">⚠ Suspected synthetic voice</span>
          <br />
          Unnatural harmonic pattern detected in the 2–4kHz band. Confidence: <span className="font-mono">79%</span>.
          We recommend verifying independently before acting on this call.
        </div>
      </div>
    </div>
  );
}
export default WhatsAppBotDemo;
