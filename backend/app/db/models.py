from typing import Optional
from sqlmodel import SQLModel, Field

class WeldGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class Layer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="weldgroup.id", index=True)
    layer_number: int = Field(index=True)
    scandata_file: Optional[str] = None
    welddat_file: Optional[str] = None

class Waypoint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    layer_id: int = Field(foreign_key="layer.id", index=True)
    seq: int = Field(index=True)
    x: float
    y: float
    z: float
    scan_raw: Optional[float] = None
    scan_value: Optional[float] = None
    speed: Optional[float] = None

class WeldSample(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    layer_id: int = Field(foreign_key="layer.id", index=True)
    seq: int = Field(index=True)
    wire_feed_rate: Optional[float] = None
    robot_speed: Optional[float] = None
    current: Optional[float] = None
    voltage: Optional[float] = None
