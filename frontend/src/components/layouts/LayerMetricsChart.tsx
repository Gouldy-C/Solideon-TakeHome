import {
  LineChart,
  Line,
  Tooltip,
  CartesianGrid,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { normalizeLayerMetrics } from "../../lib/metrics";
import type {  MetricKey, WeldData } from "../../lib/types";

type Props = {
  metrics: WeldData[] | undefined;
};

const COLORS = [
  "#60a5fa",
  "#34d399",
  "#f472b6",
  "#fbbf24",
  "#a78bfa",
  "#fb7185",
  "#22d3ee",
  "#f59e0b",
  "#4ade80",
  "#10b981",
];

export function LayerMetricsChart({ metrics }: Props) {
  const { data, keys, total } = normalizeLayerMetrics(metrics);

  if (!data.length || !keys.length || total === 0) {
    return (
      <div className="flex h-full items-center justify-center text-slate-400">
        No metrics to display
      </div>
    );
  }

  const ticks = buildSampleTicks(total);

  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis
          dataKey="samplePos"
          type="number"
          domain={["dataMin", "dataMax"]}
          ticks={ticks}
          tickFormatter={(pos) => formatSamplePos(pos as number, total)}
          label={{
            value: "Sample (i/N)",
            position: "insideBottomRight",
            offset: -6,
          }}
        />
        <YAxis />
        <Tooltip
          labelFormatter={(pos) =>
            `Sample ${formatSamplePos(pos as number, total)}`
          }
          formatter={(value, name) => [String(value), String(name)]}
          contentStyle={{
            backgroundColor: "rgba(30, 30, 30, 0.7)",
            borderRadius: "8px",
            color: "white",
          }}
        />
        <Legend />
        {keys.map((k: MetricKey, i) => (
          <Line
            key={k}
            type="monotone"
            dataKey={k}
            stroke={COLORS[i % COLORS.length]}
            dot={false}
            strokeWidth={2}
            isAnimationActive={false}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  );
}

function buildSampleTicks(total: number, approx = 6): number[] {
  if (total <= approx) {
    return Array.from({ length: total }, (_, i) => (i + 1) / total);
  }
  const set = new Set<number>();
  for (let j = 0; j <= approx; j++) {
    const idx = Math.max(
      1,
      Math.min(total, Math.round((j / approx) * total))
    );
    set.add(idx);
  }
  return Array.from(set)
    .sort((a, b) => a - b)
    .map((i) => i / total);
}

function formatSamplePos(pos: number, total: number): string {
  const idx = Math.min(Math.max(Math.round(pos * total), 1), total);
  return `${idx}/${total}`;
}