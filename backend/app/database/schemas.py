from typing import List, Optional
from pydantic import BaseModel


class GroupOut(BaseModel):
    id: str
    name: str
    layer_count: int
    ingest_complete: bool
    status: Optional[str]
    ingest_error: Optional[str]


class LayerOut(BaseModel):
    id: str
    group_id: str
    layer_number: int


class GroupDetailOut(BaseModel):
    id: str
    name: str
    layers: List[LayerOut]
    ingest_complete: bool
    status: Optional[str]
    ingest_error: Optional[str]


class LayerDetailOut(BaseModel):
    id: str
    group_id: str
    layer_number: int
    scandata_file: Optional[str] = None
    welddat_file: Optional[str] = None


class WaypointOut(BaseModel):
    seq: int
    x: float
    y: float
    z: float
    scan_value: Optional[float] = None


class WaypointWithLayerOut(BaseModel):
    layer_id: str
    layer_number: int
    seq: int
    x: float
    y: float
    z: float
    scan_value: Optional[float] = None


class MetricsSeriesPoint(BaseModel):
    x: int
    travel_speed: Optional[float] = None
    voltage: Optional[float] = None
    current: Optional[float] = None


class MetricsSeriesPointWithLayer(BaseModel):
    layer_id: str
    layer_number: int
    x: int  # seq within layer
    travel_speed: Optional[float] = None
    voltage: Optional[float] = None
    current: Optional[float] = None


class MetricsSummary(BaseModel):
    n: int
    travel_speed_avg: Optional[float] = None
    travel_speed_min: Optional[float] = None
    travel_speed_max: Optional[float] = None
    voltage_avg: Optional[float] = None
    voltage_min: Optional[float] = None
    voltage_max: Optional[float] = None
    current_avg: Optional[float] = None
    current_min: Optional[float] = None
    current_max: Optional[float] = None


class LayerMetricsOut(BaseModel):
    layer_id: str
    series: List[MetricsSeriesPoint]
    summary: MetricsSummary


class LayerMetricsSummary(BaseModel):
    layer_id: str
    layer_number: int
    summary: MetricsSummary


class GroupMetricsOut(BaseModel):
    group_id: str
    name: str
    summary: MetricsSummary
    per_layer: List[LayerMetricsSummary]