import type { MetricKey, WeldData } from "./types";

export type ChartRow = {
  sampleIndex: number;
  samplePos: number;
} & Partial<Record<MetricKey, number>>;

export type LayerMetricsData = {
  layerId: string;
  layerNumber: number;
  metrics: WeldData[];
};

export function normalizeLayerMetrics(
  input?: WeldData[]
): { data: ChartRow[]; keys: MetricKey[]; total: number } {
  const series = input ?? [];
  const total = series.length;
  if (total === 0) return { data: [], keys: [], total: 0 };

  const keys: MetricKey[] = deriveMetricKeys(series);
  const data: ChartRow[] = series.map((p, i) =>
    toChartRow(p, i, total, keys)
  );

  return { data, keys, total };
}

type MetricCarrier = Partial<Record<MetricKey, unknown>>;

function deriveMetricKeys<T extends MetricCarrier>(series: T[]): MetricKey[] {
  const possible: MetricKey[] = [
    "travel_speed",
    "voltage",
    "current",
    "wire_feed_rate",
  ];

  return possible.filter((k) =>
    series.some(
      (p) => typeof p[k] === "number" && Number.isFinite(p[k] as number)
    )
  );
}

function toChartRow<T extends MetricCarrier>(
  point: T,
  index: number,
  total: number,
  keys: MetricKey[]
): ChartRow {
  const row: ChartRow = {
    sampleIndex: index + 1,
    samplePos: (index + 1) / total,
  };

  for (const k of keys) {
    const v = point[k];
    if (typeof v === "number" && Number.isFinite(v)) {
      row[k] = v;
    }
  }

  return row;
}

export function normalizeLayerMetricsData(input: LayerMetricsData): {
  layerId: string;
  layerNumber: number;
  data: ChartRow[];
  keys: MetricKey[];
  total: number;
} {
  const { layerId, layerNumber, metrics } = input;
  const { data, keys, total } = normalizeLayerMetrics(metrics);
  return { layerId, layerNumber, data, keys, total };
}