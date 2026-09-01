import { useState } from "react";
import CallScreen from "../features/call/CallScreen";
import Dashboard from "../features/console/Dashboard";
import DemoShell from "../features/device/DemoShell";
import ElderlyCallScreen from "../features/elderly/ElderlyCallScreen";

const TABS = [
  { key: "call", label: "Call Screen" },
  { key: "dashboard", label: "Dashboard" },
  { key: "demo", label: "Demo Shell" },
  { key: "elderly", label: "Elderly Mode" },
];

function App() {
  const [view, setView] = useState("call");
  return (
    <div>
      <nav className="sticky top-4 z-50 mx-4 md:mx-8 glass rounded-full px-3 py-2
                      shadow-[0_8px_28px_-10px_rgba(61,64,91,0.25)] flex items-center gap-1">
        <span className="w-7 h-7 rounded-full bg-gradient-to-br from-terracotta to-sage-deep mr-2 shrink-0" />
        <span className="font-display font-semibold text-base text-ink mr-3 shrink-0">VoiceShield</span>
        {TABS.map((t) => (
          <button key={t.key} onClick={() => setView(t.key)}
            className={`px-4 py-2 rounded-full text-sm font-semibold transition-all duration-300 ${
              view === t.key
                ? "bg-gradient-to-r from-terracotta to-terracotta-deep text-white shadow-md"
                : "text-ink-soft hover:bg-raised"}`}>
            {t.label}
          </button>
        ))}
      </nav>
      <div className="pt-6">
        {view === "call" && <CallScreen />}
        {view === "dashboard" && <Dashboard />}
        {view === "demo" && <DemoShell />}
        {view === "elderly" && <ElderlyCallScreen />}
      </div>
    </div>
  );
}
export default App;