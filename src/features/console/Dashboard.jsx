import { useState } from "react";
import { mockCallFeed, mockMetrics } from "../../fixtures/decisions";
import CallFeedRow from "./CallFeedRow";
import MetricsPanel from "./MetricsPanel";
import CodecChart from "./CodecChart";
import { Label } from "../../ui/Label";
import { AuroraBackground } from "../../ui/AuroraBackground";

function Dashboard() {
  const [feed, setFeed] = useState(mockCallFeed);
  const handleOverride = (id, action) => console.log(`Call ${id} -> ${action}`);

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
          <Label className="mb-3">Live flagged calls</Label>
          <div className="flex flex-col gap-3">
            {feed.map((call) => <CallFeedRow key={call.call_id} call={call} onOverride={handleOverride} />)}
          </div>
        </div>
      </div>
    </div>
  );
}
export default Dashboard;