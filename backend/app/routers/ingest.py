import os
import tempfile
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from app.services.ingest import ingest_zip

router = APIRouter(prefix="/api/ingest", tags=["ingest"])


@router.post("/upload-zip")
async def upload_zip(
    archive: UploadFile = File(
        ...,
        description="ZIP with wXXX_scandata.txt and wXXX_welddat.txt",
    ),
    group_name: str = Form("default"),
):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tf:
            while chunk := await archive.read(1024 * 1024):
                tf.write(chunk)
            temp_zip_path = tf.name
        await archive.close()

        try:
            result = ingest_zip(temp_zip_path, group_name=group_name)
            return result
        finally:
            try:
                os.remove(temp_zip_path)
            except FileNotFoundError:
                pass
    except ValueError as ve:
        if str(ve) == "group_name_exists":
            raise HTTPException(status_code=409, detail="group name already exists")
        raise HTTPException(400, f"ZIP ingest failed: {ve}") from ve
    except Exception as e:
        raise HTTPException(400, f"ZIP ingest failed: {e}") from e