import { useState, useEffect } from "react";
import { mockCallFeed, mockMetrics } from "../../fixtures/decisions";
import { useRiskStream } from "../../hooks/useRiskStream";
import CallFeedRow from "./CallFeedRow";
import MetricsPanel from "./MetricsPanel";
import CodecChart from "./CodecChart";
import { Label } from "../../ui/Label";
import { AuroraBackground } from "../../ui/AuroraBackground";

function Dashboard() {
  const [feed, setFeed] = useState(mockCallFeed);
  const { decision } = useRiskStream();

  // Automatically prepend new incoming call decisions onto the live feed
  useEffect(() => {
    if (!decision || !decision.call_id) return;

    setFeed((prevFeed) => {
      // Avoid duplicate entries if the same call ID arrives
      const exists = prevFeed.some((item) => item.call_id === decision.call_id);
      if (exists) {
        return prevFeed.map((item) =>
          item.call_id === decision.call_id ? { ...item, ...decision } : item
        );
      }
      return [decision, ...prevFeed];
    });
  }, [decision]);

  // Handle analyst overrides (e.g., manually marking a call as 'real' or 'flagged')
  const handleOverride = (id, action) => {
    setFeed((prevFeed) =>
      prevFeed.map((call) =>
        call.call_id === id
          ? {
              ...call,
              decision: action === "verify" ? "real" : "suspected_clone",
              overrideBy: "Analyst",
            }
          : call
      )
    );
  };

  return (
    <div className="min-h-screen text-ink p-8 md:p-12 flex flex-col gap-10 relative">
      <AuroraBackground />
      <div className="relative z-10 max-w-3xl">
        <Label className="mb-2">VoiceShield · Analyst console</Label>
        <h1 className="font-display text-4xl md:text-5xl font-semibold leading-tight">
          Every call, <span className="text-terracotta-deep">verified in real time.</span>
        </h1>
        <p className="text-ink-soft mt-3 max-w-xl leading-relaxed">
          Live risk scores, per-branch model attributions, and a tamper-proof decision trail —
          in one place.
        </p>
      </div>

      <div className="relative z-10 flex flex-col gap-8">
        <MetricsPanel metrics={mockMetrics} />
        <CodecChart />
        <div>
          <div className="flex items-center justify-between mb-3">
            <Label>Live flagged calls</Label>
            <span className="text-xs font-mono text-ink-soft">
              {feed.length} total recorded calls
            </span>
          </div>
          <div className="flex flex-col gap-3">
            {feed.map((call) => (
              <CallFeedRow key={call.call_id} call={call} onOverride={handleOverride} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;