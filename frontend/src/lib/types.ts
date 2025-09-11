export type Group = {
  id: string;
  name: string;
  layer_count: number;
  ingest_complete?: boolean;
  status?: string;
  ingest_error?: string;
  layers?: Layer[];
  metrics?: GroupData;
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

export interface WeldDataSummary {
  n: number;
  wire_feed_rate_avg: number;
  wire_feed_rate_min: number;
  wire_feed_rate_max: number;
  travel_speed_avg: number;
  travel_speed_min: number;
  travel_speed_max: number;
  voltage_avg: number;
  voltage_min: number;
  voltage_max: number;
  current_avg: number;
  current_min: number;
  current_max: number;
}

export type MetricKey = "travel_speed" | "voltage" | "current" | "wire_feed_rate";

export interface WeldData {
  layer_id: string;
  layer_number: number;
  seq: number;
  x: number;
  y: number;
  z: number;
  wire_feed_rate?: number;
  travel_speed?: number;
  voltage?: number;
  current?: number;
}

export type ScanData = {
  layer_id: string
  layer_number: number
  seq: number
  x: number
  y: number
  z: number
  scan_value?: number
}

export interface LayerData {
  layer_id: string;
  group_id: string;
  layer_number: number
  weld_data: WeldData[];
  scan_data: ScanData[];
  summary: WeldDataSummary;
}

export type GroupData = {
  group_id: string;
  name?: string;
  summary: WeldDataSummary;
  per_layer: WeldDataSummary[];
};