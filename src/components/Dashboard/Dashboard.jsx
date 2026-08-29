import { useState } from "react";
import { mockCallFeed, mockMetrics } from "../../mocks/decisionMock";
import CallFeedRow from "./CallFeedRow";
import MetricsPanel from "./MetricsPanel";

function Dashboard() {
  const [feed, setFeed] = useState(mockCallFeed);

  const handleOverride = (callId, action) => {
    console.log(`Call ${callId} -> ${action}`);
    // In real integration, this would PATCH the decision object and log the override
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white p-8 flex flex-col gap-8">
      <h1 className="text-2xl font-bold">Analyst Dashboard</h1>

      <MetricsPanel metrics={mockMetrics} />

      <div>
        <h2 className="text-slate-400 text-sm uppercase tracking-wide mb-3">Live Flagged Calls</h2>
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