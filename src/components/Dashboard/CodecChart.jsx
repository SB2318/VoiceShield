import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from "recharts";
import { codecCollapseData } from "../../mocks/codecMock";

function CodecChart() {
  return (
    <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
      <p className="text-slate-400 text-xs uppercase tracking-wide mb-3">
        Codec-Collapse Experiment — EER (%) by channel condition
      </p>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={codecCollapseData}>
          <XAxis dataKey="condition" stroke="#94a3b8" fontSize={12} />
          <YAxis stroke="#94a3b8" fontSize={12} />
          <Tooltip contentStyle={{ backgroundColor: "#1e293b", border: "none" }} />
          <Legend />
          <Bar dataKey="baseline" name="Clean-trained baseline" fill="#f97316" />
          <Bar dataKey="trained" name="RTC-trained (VoiceShield)" fill="#38bdf8" />
        </BarChart>
      </ResponsiveContainer>
      <p className="text-slate-500 text-xs mt-2 italic">
        Illustrative placeholder — swap with real measured numbers once Backend 1's experiment (Section 15.1) completes.
      </p>
    </div>
  );
}

export default CodecChart;