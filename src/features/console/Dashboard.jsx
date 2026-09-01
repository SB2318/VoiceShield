import { useState } from "react";
import { mockCallFeed, mockMetrics } from "../../fixtures/decisions";
import CallFeedRow from "./CallFeedRow";
import MetricsPanel from "./MetricsPanel";
import CodecChart from "./CodecChart";

function Dashboard() {
  const [feed, setFeed] = useState(mockCallFeed);

  const handleOverride = (callId, action) => {
    console.log(`Call ${callId} -> ${action}`);
    // In real integration, this would PATCH the decision object and log the override
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] text-[#E8ECF4] p-8 flex flex-col gap-8">
      <div>
        <p className="text-[10px] font-semibold tracking-[0.2em] text-[#8993A8] uppercase mb-1">
          VoiceShield
        </p>
        <h1 className="text-2xl font-semibold">Analyst dashboard</h1>
      </div>

      <MetricsPanel metrics={mockMetrics} />
      <CodecChart />

      <div>
        <h2 className="text-[10px] font-semibold tracking-[0.15em] text-[#8993A8] uppercase mb-3">
          Live flagged calls
        </h2>
        <div className="flex flex-col gap-3">
          {feed.map((call) => (
            <CallFeedRow key={call.call_id} call={call} onOverride={handleOverride} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
