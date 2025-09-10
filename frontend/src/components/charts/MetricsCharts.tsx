import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

type Series = { x: number; y: number | null };

export function MetricsCharts({
  travel,
  voltage,
  current,
  height = 240,
}: {
  travel?: Series[];
  voltage?: Series[];
  current?: Series[];
  height?: number;
}) {
  return (
    <div className="space-y-4">
      {travel && (
        <ChartCard title="Travel Speed" unit="mm/s" data={travel} height={height} />
      )}
      {voltage && (
        <ChartCard title="Voltage" unit="V" data={voltage} height={height} />
      )}
      {current && (
        <ChartCard title="Current" unit="A" data={current} height={height} />
      )}
    </div>
  );
}

function ChartCard({
  title,
  unit,
  data,
  height,
}: {
  title: string;
  unit: string;
  data: Series[];
  height: number;
}) {
  return (
    <div className="rounded-lg border border-slate-700 bg-slate-900/60 p-3">
      <div className="mb-2 text-sm text-slate-300">{title}</div>
      <div style={{ width: "100%", height }}>
        <ResponsiveContainer>
          <LineChart data={data}>
            <CartesianGrid stroke="#1f2937" />
            <XAxis dataKey="x" stroke="#94a3b8" />
            <YAxis stroke="#94a3b8" />
            <Tooltip
              contentStyle={{ background: "#0b0f14", border: "1px solid #1f2937" }}
              labelStyle={{ color: "#e5e7eb" }}
            />
            <Line
              type="monotone"
              dataKey="y"
              stroke="#06B6D4"
              dot={false}
              isAnimationActive={false}
              connectNulls={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-1 text-xs text-slate-400">Units: {unit}</div>
    </div>
  );
}