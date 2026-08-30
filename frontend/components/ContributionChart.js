import { BarChart, Bar, XAxis, YAxis, Cell, ResponsiveContainer, Tooltip } from "recharts";

export default function ContributionChart({ contributions }) {
  const data = [...contributions]
    .slice(0, 8)
    .sort((a, b) => a.impact - b.impact)
    .map((c) => ({ ...c, shortLabel: c.label.replace(/\s*\(.*?\)\s*/g, "") }));

  return (
    <ResponsiveContainer width="100%" height={320}>
      <BarChart data={data} layout="vertical" margin={{ left: 10, right: 30, top: 10, bottom: 10 }}>
        <XAxis type="number" hide />
        <YAxis
          type="category"
          dataKey="shortLabel"
          width={200}
          tick={{ fontSize: 12, fill: "#0E2A2E" }}
          axisLine={false}
          tickLine={false}
        />
        <Tooltip
          formatter={(value) => [value.toFixed(2), "Contribution"]}
          contentStyle={{ borderRadius: 8, fontSize: 12 }}
        />
        <Bar dataKey="impact" radius={[0, 6, 6, 0]}>
          {data.map((entry, index) => (
            <Cell key={index} fill={entry.impact >= 0 ? "#02C39A" : "#E15554"} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
