import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid } from "recharts";
import { codecCollapseData } from "../../mocks/codecMock";

function CodecChart() {
  return (
    <div className="bg-[#131826] border border-[#232B3D] rounded-xl p-5 shadow-lg shadow-black/20">
      <p className="text-[#8993A8] text-[10px] font-semibold uppercase tracking-[0.15em] mb-4">
        Codec-collapse experiment — EER (%) by channel condition
      </p>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={codecCollapseData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#232B3D" vertical={false} />
          <XAxis dataKey="condition" stroke="#8993A8" fontSize={12} tickLine={false} axisLine={{ stroke: "#232B3D" }} />
          <YAxis stroke="#8993A8" fontSize={12} tickLine={false} axisLine={{ stroke: "#232B3D" }} />
          <Tooltip
            contentStyle={{
              backgroundColor: "#0B0F19",
              border: "1px solid #232B3D",
              borderRadius: "8px",
              padding: "10px 12px",
            }}
            labelStyle={{ color: "#8993A8", fontSize: 11, marginBottom: 4 }}
            itemStyle={{ fontSize: 12, fontFamily: "monospace" }}
          />
          <Legend wrapperStyle={{ fontSize: 12, color: "#8993A8" }} />
          <Bar dataKey="baseline" name="Clean-trained baseline" fill="#5A6478" radius={[4, 4, 0, 0]} />
          <Bar dataKey="trained" name="RTC-trained (VoiceShield)" fill="#5B8DEF" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <p className="text-[#5A6478] text-xs mt-3 italic">
        Illustrative placeholder — swap with real measured numbers once Backend 1's experiment (Section 15.1) completes.
      </p>
    </div>
  );
}
export default CodecChart;
