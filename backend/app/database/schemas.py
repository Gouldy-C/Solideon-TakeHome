from typing import List, Optional
from pydantic import BaseModel

class LayerOut(BaseModel):
    id: int
    group_id: int
    layer_number: int

class WaypointOut(BaseModel):
    seq: int
    x: float
    y: float
    z: float
    scan_value: Optional[float] = None

class MetricsSeriesPoint(BaseModel):
    x: int  # seq index
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
    layer_id: int
    series: List[MetricsSeriesPoint]
    summary: MetricsSummary