// src/lib/types.ts
export type Group = {
  id: string;
  name: string;
  layer_count?: number;
  ingest_complete?: boolean;
};

export type Layer = {
  id: string;
  group_id: string;
  layer_number: number;
};

export type Waypoint = {
  seq: number;
  x: number;
  y: number;
  z: number;
};

export type LayerMetrics = {
  layer_id: string;
  layer_number: number;
  // Arrays can contain nulls; aligned by index when possible
  travel_speed?: Array<number | null>;
  voltage?: Array<number | null>;
  current?: Array<number | null>;
  // Optional: computed aggregates
  avg_travel_speed?: number | null;
  avg_voltage?: number | null;
  avg_current?: number | null;
};

export type GroupMetrics = {
  group_id: string;
  name?: string;
  // Aggregates across layers
  avg_travel_speed?: number | null;
  avg_voltage?: number | null;
  avg_current?: number | null;
};