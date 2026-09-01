import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, CartesianGrid } from "recharts";
import { codecCollapseData } from "../../fixtures/codec";
import { Card } from "../../ui/Card";
import { Label } from "../../ui/Label";

function CodecChart() {
  return (
    <Card>
      <Label className="mb-4">Codec-collapse experiment — EER (%) by channel condition</Label>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={codecCollapseData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5DCC3" vertical={false} />
          <XAxis dataKey="condition" stroke="#6E7195" fontSize={12} tickLine={false} axisLine={{ stroke: "#E5DCC3" }} />
          <YAxis stroke="#6E7195" fontSize={12} tickLine={false} axisLine={{ stroke: "#E5DCC3" }} />
          <Tooltip contentStyle={{ backgroundColor: "#FFFFFF", border: "1px solid #E5DCC3", borderRadius: "10px", padding: "10px 12px" }}
            labelStyle={{ color: "#6E7195", fontSize: 11, marginBottom: 4 }} itemStyle={{ fontSize: 12, fontFamily: "monospace" }} />
          <Legend wrapperStyle={{ fontSize: 12, color: "#6E7195" }} />
          <Bar dataKey="baseline" name="Clean-trained baseline" fill="#A4A6C4" radius={[6, 6, 0, 0]} />
          <Bar dataKey="trained" name="RTC-trained (VoiceShield)" fill="#E07A5F" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
      <p className="text-ink-faint text-xs mt-3 italic">
        Illustrative placeholder — swap with real measured numbers once the codec-collapse experiment completes.
      </p>
    </Card>
  );
}
export default CodecChart;