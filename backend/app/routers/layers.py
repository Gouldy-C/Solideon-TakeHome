from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool
from sqlmodel import select

from app.services.compute_metrics import compute_layer_data
from app.database.db import get_session
from app.database.models import Layer, ScanData
from app.database.schemas import LayerDataOut, LayerOut

router = APIRouter(prefix="/api/layers", tags=["layers"])


@router.get("/{layer_id}", response_model=LayerOut)
async def get_layer(layer_id: str):
    with get_session() as session:
        layer = session.get(Layer, layer_id)
        if not layer:
            raise HTTPException(status_code=404, detail="layer not found")
        return LayerOut(
            id=layer.id,
            group_id=layer.group_id,
            layer_number=layer.layer_number,
            scandata_file=layer.scandata_file,
            welddat_file=layer.welddat_file,
        )


@router.get("/{layer_id}/data", response_model=LayerDataOut)
async def get_metrics(layer_id: str):
    try:
        result = await run_in_threadpool(
            compute_layer_data, layer_id
        )
        return result
    except ValueError as ve:
        if str(ve) == "group_not_found":
            raise HTTPException(status_code=404, detail="group not found")
        raise