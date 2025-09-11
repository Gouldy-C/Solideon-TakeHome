from typing import List, Dict
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import func
from sqlmodel import select
from fastapi.concurrency import run_in_threadpool

from app.database.db import get_session
from app.database.models import WeldGroup, Layer
from app.database.schemas import (
    GroupOut,
    LayerOut,
    GroupWeldDataOut,
)
from app.services.compute_metrics import compute_group_data

router = APIRouter(prefix="/api/groups", tags=["groups"])


@router.get("", response_model=List[GroupOut])
async def list_groups(
    limit: int = Query(1000, ge=1, le=1000), offset: int = Query(0, ge=0)
):
    with get_session() as session:
        groups = session.exec(
            select(WeldGroup).order_by(WeldGroup.name).limit(limit).offset(offset)
        ).all()
        ids = [g.id for g in groups]
        counts: Dict[str, int] = {}
        if ids:
            layers = session.exec(
                select(Layer.group_id, func.count(Layer.id)) # type: ignore
                .where(Layer.group_id.in_(ids)) # type: ignore
                .group_by(Layer.group_id)
            ).all()
            counts = {gid: cnt for gid, cnt in layers}
        items = [
            GroupOut(
                id=g.id,
                name=g.name,
                layer_count=counts.get(g.id, 0),
                ingest_complete=g.ingest_complete,
                ingest_error=g.ingest_error,
                status=g.status,
                layers=[],
            )
            for g in groups
        ]
        return items


@router.get("/{group_id}", response_model=GroupOut)
async def get_group(
    group_id: str, limit: int = Query(1000000, ge=1), offset: int = Query(0, ge=0)
):
    with get_session() as session:
        group = session.get(WeldGroup, group_id)
        if not group:
            raise HTTPException(status_code=404, detail="group not found")

        layers = session.exec(
            select(Layer)
            .where(Layer.group_id == group.id)
            .order_by(Layer.layer_number) # type: ignore
            .limit(limit)
            .offset(offset)
        ).all()
        return GroupOut(
            id=group.id,
            name=group.name,
            ingest_complete=group.ingest_complete,
            ingest_error=group.ingest_error,
            status=group.status,
            layer_count=len(layers),
            layers=[
                LayerOut(
                    id=layer.id,
                    group_id=layer.group_id,
                    layer_number=layer.layer_number,
                )
                for layer in layers
            ],
        )


@router.get("/{group_id}/data", response_model=GroupWeldDataOut)
async def get_group_metrics(group_id: str):
    try:
        result = await run_in_threadpool(compute_group_data, group_id)
        print("hello")
        return result
    except ValueError as ve:
        if str(ve) == "group_not_found":
            raise HTTPException(status_code=404, detail="group not found")
        raise
