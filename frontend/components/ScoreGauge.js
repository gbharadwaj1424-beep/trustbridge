import { RadialBarChart, RadialBar, PolarAngleAxis } from "recharts";

const tierColor = (tier) => {
  if (tier === "High Trust") return "#02C39A";
  if (tier === "Building Trust") return "#F2B134";
  return "#E15554";
};

export default function ScoreGauge({ score, tier }) {
  const data = [{ name: "score", value: score, fill: tierColor(tier) }];

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative" style={{ width: 220, height: 220 }}>
        <RadialBarChart
          width={220}
          height={220}
          cx="50%"
          cy="50%"
          innerRadius="75%"
          outerRadius="100%"
          barSize={18}
          data={data}
          startAngle={90}
          endAngle={-270}
        >
          <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
          <RadialBar background dataKey="value" cornerRadius={10} angleAxisId={0} />
        </RadialBarChart>
        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
          <span className="text-5xl font-bold text-ink">{Math.round(score)}</span>
          <span className="text-sm text-ink/60">out of 100</span>
        </div>
      </div>
      <span
        className="px-4 py-1 rounded-full text-sm font-semibold text-white"
        style={{ backgroundColor: tierColor(tier) }}
      >
        {tier}
      </span>
    </div>
  );
}
