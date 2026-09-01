import { useState } from "react";
import CallScreen from "../features/call/CallScreen";
import Dashboard from "../features/console/Dashboard";
import DemoShell from "../features/device/DemoShell";
import ElderlyCallScreen from "../features/elderly/ElderlyCallScreen";

function App() {
  const [view, setView] = useState("call");

  return (
    <div>
      <nav className="flex gap-2 p-3 bg-slate-950 border-b border-slate-800">
        <button
          onClick={() => setView("call")}
          className={`px-4 py-2 rounded-md text-sm font-medium ${
            view === "call" ? "bg-sky-600 text-white" : "bg-slate-800 text-slate-400"
          }`}
        >
          Call Screen
        </button>
        <button
          onClick={() => setView("dashboard")}
          className={`px-4 py-2 rounded-md text-sm font-medium ${
            view === "dashboard" ? "bg-sky-600 text-white" : "bg-slate-800 text-slate-400"
          }`}
        >
          Dashboard
        </button>
        <button
          onClick={() => setView("demo")}
          className={`px-4 py-2 rounded-md text-sm font-medium ${
            view === "demo" ? "bg-sky-600 text-white" : "bg-slate-800 text-slate-400"
          }`}
        >
          Demo Shell
        </button>
        <button
          onClick={() => setView("elderly")}
          className={`px-4 py-2 rounded-md text-sm font-medium ${
            view === "elderly" ? "bg-sky-600 text-white" : "bg-slate-800 text-slate-400"
          }`}
        >
          Elderly Mode
        </button>
      </nav>

      {view === "call" && <CallScreen />}
      {view === "dashboard" && <Dashboard />}
      {view === "demo" && <DemoShell />}
      {view === "elderly" && <ElderlyCallScreen />}
    </div>
  );
}

export default App;