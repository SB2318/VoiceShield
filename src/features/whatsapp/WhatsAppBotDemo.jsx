import { useState } from "react";

function WhatsAppBotDemo() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "user",
      type: "audio",
      duration: "0:14",
      timestamp: "10:42 AM",
    },
    {
      id: 2,
      sender: "bot",
      type: "result",
      status: "clone",
      score: 79,
      reason: "Unnatural harmonic pattern detected in the 2–4kHz band.",
      timestamp: "10:42 AM",
    },
  ]);

  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleSimulateNote = (type) => {
    setIsAnalyzing(true);
    const newAudioId = Date.now();
    const currentTime = new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });

    // Append forwarded voice note message
    const newAudioMessage = {
      id: newAudioId,
      sender: "user",
      type: "audio",
      duration: type === "clone" ? "0:18" : "0:11",
      timestamp: currentTime,
    };

    setMessages((prev) => [...prev, newAudioMessage]);

    // Simulate analysis response delay
    setTimeout(() => {
      const newResultMessage = {
        id: newAudioId + 1,
        sender: "bot",
        type: "result",
        status: type,
        score: type === "clone" ? 84 : 12,
        reason:
          type === "clone"
            ? "Phase discontinuity detected across pitch contours."
            : "Acoustic features align with natural speaker profile.",
        timestamp: currentTime,
      };

      setMessages((prev) => [...prev, newResultMessage]);
      setIsAnalyzing(false);
    }, 1200);
  };

  return (
    <div className="min-h-screen text-ink p-6 flex flex-col items-center justify-center relative">
      <div className="w-full max-w-sm bg-[#0b141a] rounded-3xl p-4 border border-[#232B3D] shadow-2xl flex flex-col gap-4">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-[#232B3D] pb-3">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-[#00a884] flex items-center justify-center text-white text-xs font-bold">
              VS
            </div>
            <div>
              <p className="text-white text-xs font-medium">VoiceShield ShieldBot</p>
              <p className="text-[#8993A8] text-[10px]">Official Verification</p>
            </div>
          </div>
          <span className="text-[10px] text-[#00a884] font-semibold uppercase tracking-wider bg-[#00a884]/10 px-2 py-0.5 rounded-full">
            Active
          </span>
        </div>

        {/* Chat Stream */}
        <div className="flex flex-col gap-3 min-h-[300px] max-h-[420px] overflow-y-auto pr-1">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${
                msg.sender === "user" ? "items-end" : "items-start"
              }`}
            >
              {msg.type === "audio" ? (
                <div className="bg-[#005c4b] text-white text-xs rounded-2xl rounded-tr-none px-3.5 py-2.5 max-w-[80%] shadow-sm">
                  <div className="flex items-center gap-2">
                    <span>🎙️</span>
                    <span className="font-medium">Voice note forwarded</span>
                    <span className="text-[10px] opacity-75 font-mono">
                      {msg.duration}
                    </span>
                  </div>
                  <span className="text-[9px] text-[#8696a0] block text-right mt-1">
                    {msg.timestamp}
                  </span>
                </div>
              ) : (
                <div className="bg-[#202c33] text-white text-xs rounded-2xl rounded-tl-none px-3.5 py-2.5 max-w-[88%] leading-relaxed shadow-sm">
                  {msg.status === "clone" ? (
                    <>
                      <span className="text-amber-400 font-semibold flex items-center gap-1 mb-1">
                        ⚠ Suspected synthetic voice
                      </span>
                      <p className="text-[#d1d7db] text-[11px] leading-normal">
                        {msg.reason}
                      </p>
                      <div className="mt-2 text-[10px] text-[#8696a0]">
                        Risk score:{" "}
                        <span className="font-mono text-amber-400 font-bold">
                          {msg.score}%
                        </span>
                      </div>
                    </>
                  ) : (
                    <>
                      <span className="text-[#00a884] font-semibold flex items-center gap-1 mb-1">
                        ✓ Verified authentic voice
                      </span>
                      <p className="text-[#d1d7db] text-[11px] leading-normal">
                        {msg.reason}
                      </p>
                      <div className="mt-2 text-[10px] text-[#8696a0]">
                        Risk score:{" "}
                        <span className="font-mono text-[#00a884] font-bold">
                          {msg.score}%
                        </span>
                      </div>
                    </>
                  )}
                  <span className="text-[9px] text-[#8696a0] block text-right mt-1">
                    {msg.timestamp}
                  </span>
                </div>
              )}
            </div>
          ))}

          {isAnalyzing && (
            <div className="self-start bg-[#202c33] text-[#8696a0] text-xs rounded-2xl rounded-tl-none px-3 py-2 animate-pulse flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#00a884] animate-ping" />
              Analyzing audio spectral signatures...
            </div>
          )}
        </div>

        {/* Demo Controls */}
        <div className="border-t border-[#232B3D] pt-3 flex flex-col gap-2">
          <span className="text-[10px] text-[#8993A8] uppercase tracking-wider font-semibold text-center">
            Simulate Incoming Voice Note
          </span>
          <div className="flex gap-2">
            <button
              disabled={isAnalyzing}
              onClick={() => handleSimulateNote("real")}
              className="flex-1 bg-[#202c33] hover:bg-[#2a3942] disabled:opacity-50 text-xs text-[#00a884] font-semibold py-2 px-3 rounded-xl border border-[#00a884]/30 transition-all"
            >
              Forward Real Note
            </button>
            <button
              disabled={isAnalyzing}
              onClick={() => handleSimulateNote("clone")}
              className="flex-1 bg-[#202c33] hover:bg-[#2a3942] disabled:opacity-50 text-xs text-amber-400 font-semibold py-2 px-3 rounded-xl border border-amber-400/30 transition-all"
            >
              Forward Deepfake
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default WhatsAppBotDemo;