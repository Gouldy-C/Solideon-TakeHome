from typing import List, Optional
from pydantic import BaseModel

class LayerOut(BaseModel):
    id: str
    group_id: str
    layer_number: int
    scandata_file: Optional[str] = None
    welddat_file: Optional[str] = None

class GroupOut(BaseModel):
    id: str
    name: str
    layer_count: int
    ingest_complete: bool
    status: Optional[str]
    ingest_error: Optional[str]
    layers: List[LayerOut]

class ScanDataOut(BaseModel):
    layer_id: str
    layer_number: int
    seq: int
    x: float
    y: float
    z: float
    scan_value: Optional[float] = None

class WeldDataOut(BaseModel):
    layer_id: str
    layer_number: int
    seq: int
    x: float
    y: float
    z: float
    wire_feed_rate: Optional[float] = None
    travel_speed: Optional[float] = None
    voltage: Optional[float] = None
    current: Optional[float] = None


class WeldDataSummary(BaseModel):
    n: int
    wire_feed_rate_avg: Optional[float] = None
    wire_feed_rate_min: Optional[float] = None
    wire_feed_rate_max: Optional[float] = None
    travel_speed_avg: Optional[float] = None
    travel_speed_min: Optional[float] = None
    travel_speed_max: Optional[float] = None
    voltage_avg: Optional[float] = None
    voltage_min: Optional[float] = None
    voltage_max: Optional[float] = None
    current_avg: Optional[float] = None
    current_min: Optional[float] = None
    current_max: Optional[float] = None


class LayerDataOut(BaseModel):
    layer_id: str
    group_id: str
    layer_number: int
    scan_data: List[ScanDataOut]
    weld_data: List[WeldDataOut]
    summary: WeldDataSummary


class GroupWeldDataOut(BaseModel):
    group_id: str
    name: str
    summary: WeldDataSummary
    per_layer: List[WeldDataSummary]