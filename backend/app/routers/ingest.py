# app/routers/ingest.py
import os
import tempfile
from uuid import uuid4
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException,
    BackgroundTasks,
)
from sqlalchemy.exc import IntegrityError

from app.database.db import get_session
from app.database.models import WeldGroup
from app.services.ingest import ingest_zip_into_group

router = APIRouter(prefix="/api/ingest", tags=["ingest"])


def _reserve_group(group_name: str) -> WeldGroup:
    # Create the group row now to make the name reservation atomic.
    with get_session() as session:
        group = WeldGroup(name=group_name, ingest_complete=False)
        session.add(group)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise ValueError("group_name_exists")
        session.refresh(group)
        return group


def _run_ingest_and_cleanup(zip_path: str, group_id: str) -> None:
    try:
        ingest_zip_into_group(zip_path, group_id=group_id)
    except Exception as e:
        with get_session() as s:
            g = s.get(WeldGroup, group_id)
            if g:
                g.status = "failed"
                g.ingest_error = str(e)
                s.commit()
        pass
    finally:
        try:
            os.remove(zip_path)
        except FileNotFoundError:
            pass


@router.post("/upload-zip", status_code=202)
async def upload_zip(
    background_tasks: BackgroundTasks,
    zip_file: UploadFile = File(
        ..., description="ZIP with wXXX_scandata.txt and wXXX_welddat.txt"
    ),
    group_name: str = Form("default"),
):
    try:
        group = _reserve_group(group_name)
    except ValueError as ve:
        if str(ve) == "group_name_exists":
            raise HTTPException(status_code=409, detail="group name already exists")
        raise

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tf:
            while True:
                chunk = await zip_file.read(1024 * 1024)
                if not chunk:
                    break
                tf.write(chunk)
            temp_zip_path = tf.name
    finally:
        await zip_file.close()

    background_tasks.add_task(_run_ingest_and_cleanup, temp_zip_path, group.id)

    return {"group": group.name, "groupId": group.id, "status": "accepted"}