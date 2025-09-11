from typing import Dict, List, Optional
from statistics import fmean
from sqlmodel import select

from app.database.db import get_session
from app.database.models import Layer, ScanData, WeldGroup, WeldData
from app.database.schemas import (
    GroupWeldDataOut,
    LayerDataOut,
    ScanDataOut,
    WeldDataOut,
    WeldDataSummary,
)


def _min_or_none(vals: List[Optional[float]]) -> Optional[float]:
    clean = [v for v in vals if v is not None]
    return min(clean) if clean else None


def _max_or_none(vals: List[Optional[float]]) -> Optional[float]:
    clean = [v for v in vals if v is not None]
    return max(clean) if clean else None


def _avg_or_none(vals: List[Optional[float]]) -> Optional[float]:
    clean = [v for v in vals if v is not None]
    return fmean(clean) if clean else None


def compute_layer_data(layer_id: str) -> LayerDataOut:
    """
    Build a LayerDataOut using WeldData rows for a single layer.
    """
    with get_session() as session:
        layer = session.get(Layer, layer_id)
        if not layer:
            raise ValueError("layer_not_found")

        weld_rows: List[WeldData] = (
            session.exec(
                select(WeldData)
                .where(WeldData.layer_id == layer_id)
                .order_by(WeldData.seq)  # type: ignore
            )
        ).all()
        
        scan_rows: List[ScanData] = (
            session.exec(
                select(ScanData)
                .where(ScanData.layer_id == layer_id)
                .order_by(ScanData.seq)  # type: ignore
            )
        ).all()

        weld_points: List[WeldDataOut] = []
        for r in weld_rows:
            weld_points.append(
                WeldDataOut(
                    layer_id=r.layer_id,
                    layer_number=layer.layer_number,
                    seq=r.seq,
                    x=r.x,
                    y=r.y,
                    z=r.z,
                    wire_feed_rate=r.wire_feed_rate,
                    travel_speed=r.robot_speed,  # map robot_speed -> travel_speed
                    voltage=r.voltage,
                    current=r.current,
                )
            )

        wire_feed_rate_vals: List[Optional[float]] = [
            p.wire_feed_rate for p in weld_points
        ]
        travel_speed_vals: List[Optional[float]] = [
            p.travel_speed for p in weld_points
        ]
        voltage_vals: List[Optional[float]] = [p.voltage for p in weld_points]
        current_vals: List[Optional[float]] = [p.current for p in weld_points]

        summary = WeldDataSummary(
            n=len(weld_points),
            wire_feed_rate_avg=_avg_or_none(wire_feed_rate_vals),
            wire_feed_rate_min=_min_or_none(wire_feed_rate_vals),
            wire_feed_rate_max=_max_or_none(wire_feed_rate_vals),
            travel_speed_avg=_avg_or_none(travel_speed_vals),
            travel_speed_min=_min_or_none(travel_speed_vals),
            travel_speed_max=_max_or_none(travel_speed_vals),
            voltage_avg=_avg_or_none(voltage_vals),
            voltage_min=_min_or_none(voltage_vals),
            voltage_max=_max_or_none(voltage_vals),
            current_avg=_avg_or_none(current_vals),
            current_min=_min_or_none(current_vals),
            current_max=_max_or_none(current_vals),
        )

        return LayerDataOut(
            layer_id=layer.id,
            group_id=layer.group_id,
            layer_number=layer.layer_number,
            scan_data=[
                ScanDataOut(
                    layer_id=r.layer_id,
                    layer_number=layer.layer_number,
                    seq=r.seq,
                    x=r.x,
                    y=r.y,
                    z=r.z,
                    scan_value=r.scan_value,
                )
                for r in scan_rows
            ],
            weld_data=weld_points,
            summary=summary,
        )


def compute_group_data(group_id: str) -> GroupWeldDataOut:
    """
    Build a GroupWeldDataOut summary for a group, including per-layer summaries
    (ordered by layer_number).
    """
    with get_session() as session:
        group = session.get(WeldGroup, group_id)
        if not group:
            raise ValueError("group_not_found")

        rows: List[tuple[WeldData, str, int]] = session.exec(
            select(WeldData, Layer.id, Layer.layer_number)
            .join(Layer, Layer.id == WeldData.layer_id)  # type: ignore
            .where(Layer.group_id == group_id)
            .order_by(Layer.layer_number, WeldData.seq)  # type: ignore
        ).all()

        per_layer_vals: Dict[str, Dict[str, List[Optional[float]]]] = {}
        per_layer_number: Dict[str, int] = {}

        group_wire_feed_rate: List[Optional[float]] = []
        group_travel_speed: List[Optional[float]] = []
        group_voltage: List[Optional[float]] = []
        group_current: List[Optional[float]] = []

        for sample, l_id, l_num in rows:
            bucket = per_layer_vals.setdefault(
                l_id,
                {
                    "wire_feed_rate": [],
                    "travel_speed": [],
                    "voltage": [],
                    "current": [],
                },
            )
            per_layer_number[l_id] = l_num

            bucket["wire_feed_rate"].append(sample.wire_feed_rate)
            bucket["travel_speed"].append(sample.robot_speed)
            bucket["voltage"].append(sample.voltage)
            bucket["current"].append(sample.current)

            group_wire_feed_rate.append(sample.wire_feed_rate)
            group_travel_speed.append(sample.robot_speed)
            group_voltage.append(sample.voltage)
            group_current.append(sample.current)

        per_layer_entries: List[tuple[int, WeldDataSummary]] = []
        for l_id, vals in per_layer_vals.items():
            wire_feed_rate = vals["wire_feed_rate"]
            travel_speed = vals["travel_speed"]
            voltage = vals["voltage"]
            current = vals["current"]

            summary = WeldDataSummary(
                n=len(wire_feed_rate),
                wire_feed_rate_avg=_avg_or_none(wire_feed_rate),
                wire_feed_rate_min=_min_or_none(wire_feed_rate),
                wire_feed_rate_max=_max_or_none(wire_feed_rate),
                travel_speed_avg=_avg_or_none(travel_speed),
                travel_speed_min=_min_or_none(travel_speed),
                travel_speed_max=_max_or_none(travel_speed),
                voltage_avg=_avg_or_none(voltage),
                voltage_min=_min_or_none(voltage),
                voltage_max=_max_or_none(voltage),
                current_avg=_avg_or_none(current),
                current_min=_min_or_none(current),
                current_max=_max_or_none(current),
            )
            per_layer_entries.append((per_layer_number[l_id], summary))

        per_layer_entries.sort(key=lambda t: t[0])
        per_layer_summaries: List[WeldDataSummary] = [t[1] for t in per_layer_entries]

        group_summary = WeldDataSummary(
            n=len(group_wire_feed_rate),
            wire_feed_rate_avg=_avg_or_none(group_wire_feed_rate),
            wire_feed_rate_min=_min_or_none(group_wire_feed_rate),
            wire_feed_rate_max=_max_or_none(group_wire_feed_rate),
            travel_speed_avg=_avg_or_none(group_travel_speed),
            travel_speed_min=_min_or_none(group_travel_speed),
            travel_speed_max=_max_or_none(group_travel_speed),
            voltage_avg=_avg_or_none(group_voltage),
            voltage_min=_min_or_none(group_voltage),
            voltage_max=_max_or_none(group_voltage),
            current_avg=_avg_or_none(group_current),
            current_min=_min_or_none(group_current),
            current_max=_max_or_none(group_current),
        )

        return GroupWeldDataOut(
            group_id=group.id,
            name=group.name,
            summary=group_summary,
            per_layer=per_layer_summaries,
        )