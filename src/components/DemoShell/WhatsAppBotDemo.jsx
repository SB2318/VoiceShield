function WhatsAppBotDemo() {
  return (
    <div className="max-w-sm mx-auto bg-[#0b141a] rounded-2xl p-4 border border-slate-700">
      <p className="text-slate-400 text-xs mb-3">WhatsApp — VoiceShield Bot</p>
      <div className="flex flex-col gap-2">
        <div className="self-end bg-[#005c4b] text-white text-sm rounded-lg px-3 py-2 max-w-[80%]">
          🎙️ [Voice note forwarded — 0:14]
        </div>
        <div className="self-start bg-[#202c33] text-white text-sm rounded-lg px-3 py-2 max-w-[80%]">
          ⚠️ This voice sample shows signs of synthetic generation (unnatural harmonic pattern, 2–4kHz).
          Confidence: 79%. We recommend verifying independently before acting on this call.
        </div>
      </div>
    </div>
  );
}

export default WhatsAppBotDemo;