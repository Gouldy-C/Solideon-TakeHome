from typing import List, Dict, Optional
from statistics import fmean
from sqlmodel import select

from app.database.db import get_session
from app.database.models import Layer, WeldGroup, WeldMetric
from app.database.schemas import (
    MetricsSeriesPoint,
    MetricsSeriesPointWithLayer,
    MetricsSummary,
    LayerMetricsOut,
    LayerMetricsSummary,
    GroupMetricsOut,
)


def _min_or_none(vals):
    vals = [v for v in vals if v is not None]
    return min(vals) if vals else None


def _max_or_none(vals):
    vals = [v for v in vals if v is not None]
    return max(vals) if vals else None


def _avg_or_none(vals):
    vals = [v for v in vals if v is not None]
    return fmean(vals) if vals else None


def compute_layer_metrics(layer_id: str) -> LayerMetricsOut:
    with get_session() as session:
        rows = session.exec(
            select(WeldMetric)
            .where(WeldMetric.layer_id == layer_id)
            .order_by(WeldMetric.seq)
        ).all()

        series: List[MetricsSeriesPoint] = []
        for r in rows:
            series.append(
                MetricsSeriesPoint(
                    x=r.seq,
                    travel_speed=r.robot_speed,
                    voltage=r.voltage,
                    current=r.current,
                )
            )

        travel = [p.travel_speed for p in series]
        volt = [p.voltage for p in series]
        curr = [p.current for p in series]

        summary = MetricsSummary(
            n=len(series),
            travel_speed_avg=_avg_or_none(travel),
            travel_speed_min=_min_or_none(travel),
            travel_speed_max=_max_or_none(travel),
            voltage_avg=_avg_or_none(volt),
            voltage_min=_min_or_none(volt),
            voltage_max=_max_or_none(volt),
            current_avg=_avg_or_none(curr),
            current_min=_min_or_none(curr),
            current_max=_max_or_none(curr),
        )

        return LayerMetricsOut(
            layer_id=layer_id,
            series=series,
            summary=summary,
        )


def compute_group_metrics(
    group_id: str
) -> GroupMetricsOut:
    with get_session() as session:
        group = session.get(WeldGroup, group_id)
        if not group:
            raise ValueError("group_not_found")

        stmt = (
            select(WeldMetric, Layer.id, Layer.layer_number)
            .join(Layer, Layer.id == WeldMetric.layer_id)
            .where(Layer.group_id == group_id)
            .order_by(Layer.layer_number, WeldMetric.seq)
        )
        rows = session.exec(stmt).all()

        per_layer_vals: Dict[str, Dict[str, List[Optional[float]]]] = {}
        per_layer_number: Dict[str, int] = {}
        group_travel: List[Optional[float]] = []
        group_volt: List[Optional[float]] = []
        group_curr: List[Optional[float]] = []

        for sample, layer_id, layer_number in rows:
            bucket = per_layer_vals.setdefault(
                layer_id,
                {
                    "travel": [],
                    "volt": [],
                    "curr": [],
                },
            )
            per_layer_number[layer_id] = layer_number

            # Append to per-layer and group aggregates
            bucket["travel"].append(sample.robot_speed)
            bucket["volt"].append(sample.voltage)
            bucket["curr"].append(sample.current)

            group_travel.append(sample.robot_speed)
            group_volt.append(sample.voltage)
            group_curr.append(sample.current)

        # Build per-layer summaries
        per_layer: List[LayerMetricsSummary] = []
        for layer_id, vals in per_layer_vals.items():
            travel = vals["travel"]
            volt = vals["volt"]
            curr = vals["curr"]
            summary = MetricsSummary(
                n=len([v for v in travel if v is not None]),
                travel_speed_avg=_avg_or_none(travel),
                travel_speed_min=_min_or_none(travel),
                travel_speed_max=_max_or_none(travel),
                voltage_avg=_avg_or_none(volt),
                voltage_min=_min_or_none(volt),
                voltage_max=_max_or_none(volt),
                current_avg=_avg_or_none(curr),
                current_min=_min_or_none(curr),
                current_max=_max_or_none(curr),
            )
            per_layer.append(
                LayerMetricsSummary(
                    layer_id=layer_id,
                    layer_number=per_layer_number[layer_id],
                    summary=summary,
                )
            )

        # Group-wide summary
        summary = MetricsSummary(
            n=len([v for v in group_travel if v is not None]),
            travel_speed_avg=_avg_or_none(group_travel),
            travel_speed_min=_min_or_none(group_travel),
            travel_speed_max=_max_or_none(group_travel),
            voltage_avg=_avg_or_none(group_volt),
            voltage_min=_min_or_none(group_volt),
            voltage_max=_max_or_none(group_volt),
            current_avg=_avg_or_none(group_curr),
            current_min=_min_or_none(group_curr),
            current_max=_max_or_none(group_curr),
        )

        # Sort per-layer summaries by layer_number
        per_layer.sort(key=lambda x: x.layer_number)

        return GroupMetricsOut(
            group_id=group.id,
            name=group.name,
            summary=summary,
            per_layer=per_layer
        )