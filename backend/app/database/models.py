from typing import Optional
from uuid import uuid4
from sqlmodel import SQLModel, Field
import logging

logger = logging.getLogger(__name__)

def _uuid() -> str:
    return str(uuid4())


class WeldGroup(SQLModel, table=True):
    id: str = Field(default_factory=_uuid, primary_key=True)
    name: str = Field(index=True, sa_column_kwargs={"unique": True})
    ingest_complete: bool = False
    ingest_error: Optional[str] = None
    status: Optional[str] = None


class Layer(SQLModel, table=True):
    id: str = Field(default_factory=_uuid, primary_key=True)
    group_id: str = Field(foreign_key="weldgroup.id", index=True)
    layer_number: int = Field(index=True)
    scandata_file: Optional[str] = None
    welddat_file: Optional[str] = None


class ScanData(SQLModel, table=True):
    id: str = Field(default_factory=_uuid, primary_key=True)
    layer_id: str = Field(foreign_key="layer.id", index=True)
    layer_number: int = Field(index=True)
    seq: int = Field(index=True)
    x: float
    y: float
    z: float
    scan_raw: Optional[float] = None
    scan_value: Optional[float] = None
    speed: Optional[float] = None


class WeldData(SQLModel, table=True):
    id: str = Field(default_factory=_uuid, primary_key=True)
    layer_id: str = Field(foreign_key="layer.id", index=True)
    layer_number: int = Field(index=True)
    seq: int = Field(index=True)
    x: float
    y: float
    z: float
    wire_feed_rate: Optional[float] = None
    robot_speed: Optional[float] = None
    current: Optional[float] = None
    voltage: Optional[float] = None

def init_models() -> None:
    logger.info("Initializing models")