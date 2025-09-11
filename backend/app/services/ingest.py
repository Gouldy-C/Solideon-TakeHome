# app/services/ingest.py
import os
import re
import zipfile
import tempfile
from typing import Dict, Optional, Tuple

from app.database.db import get_session
from app.database.models import Layer, ScanData, WeldData, WeldGroup
from app.utils.parsers import parse_scandata, parse_welddat
from app.utils.transforms import transform_scan_value

PAIR_RE = re.compile(r"^w(\d+)_([a-zA-Z]+)\.txt$")


def _safe_extractall(zf: zipfile.ZipFile, dest: str) -> None:
    dest_real = os.path.realpath(dest)
    for member in zf.infolist():
        member_path = os.path.realpath(os.path.join(dest, member.filename))
        if not member_path.startswith(dest_real + os.sep) and member_path != dest_real:
            raise ValueError(f"Illegal path in archive: {member.filename}")
    zf.extractall(dest)


def _pair_files(root_dir: str) -> Dict[int, Dict[str, Optional[str]]]:
    layers: Dict[int, Dict[str, Optional[str]]] = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for fname in filenames:
            if not fname.lower().endswith(".txt"):
                continue
            m = PAIR_RE.match(fname)
            if not m:
                continue
            num = int(m.group(1))
            kind = m.group(2).lower()
            entry = layers.setdefault(num, {"scandata": None, "welddat": None})
            full_path = os.path.join(dirpath, fname)
            if "scan" in kind:
                entry["scandata"] = full_path
            elif "weld" in kind:
                entry["welddat"] = full_path
    return layers


def _ingest_pair_into_layer(
    session,
    layer: Layer,
    scandata_path: str,
    welddat_path: str,
) -> Tuple[int, int]:
    with open(scandata_path, "r") as f:
        scan_rows = parse_scandata(f)

    waypoints: list[ScanData] = []
    for seq, raw, x, y, z, v in scan_rows:
        waypoints.append(
            ScanData(
                layer_id=layer.id,
                layer_number=layer.layer_number,
                seq=seq,
                x=x,
                y=y,
                z=z,
                scan_raw=raw,
                scan_value=transform_scan_value(raw),
                speed=v,
            )
        )
    session.add_all(waypoints)

    with open(welddat_path, "r") as f:
        weld_rows = parse_welddat(f)

    metrics: list[WeldData] = []
    for seq, wfr, rs, cur, volt, x, y, z in weld_rows:
        metrics.append(
            WeldData(
                layer_id=layer.id,
                layer_number=layer.layer_number,
                seq=seq,
                wire_feed_rate=wfr,
                robot_speed=rs,
                current=cur,
                voltage=volt,
                x=x,
                y=y,
                z=z,
            )
        )
    session.add_all(metrics)
    session.commit()
    return (len(waypoints), len(metrics))


def ingest_directory_into_group(data_dir: str, group_id: str) -> dict:
    assert os.path.isdir(data_dir), f"Directory not found: {data_dir}"
    pairs = _pair_files(data_dir)

    created, errors = 0, 0
    details: list[dict] = []

    with get_session() as session:
        group = session.get(WeldGroup, group_id)
        if not group:
            raise ValueError(f"group_not_found: {group_id}")

        for layer_number, files in sorted(pairs.items()):
            scandata = files.get("scandata")
            welddat = files.get("welddat")
            if not scandata or not welddat:
                errors += 1
                details.append(
                    {
                        "layer_number": layer_number,
                        "status": "error",
                        "reason": "missing_pair",
                    }
                )
                continue

            layer = Layer(
                group_id=group.id,
                layer_number=layer_number,
                scandata_file=os.path.basename(scandata),
                welddat_file=os.path.basename(welddat),
            )
            session.add(layer)
            session.commit()
            session.refresh(layer)

            wp_count, sm_count = _ingest_pair_into_layer(
                session, layer, scandata, welddat
            )
            created += 1
            details.append(
                {
                    "layer_number": layer_number,
                    "status": "created",
                    "waypoints": wp_count,
                    "metrics": sm_count,
                }
            )

        group.ingest_complete = True
        group.status = "ingested"
        session.commit()
        session.refresh(group)

    return {
        "groupId": group_id,
        "created": created,
        "errors": errors,
        "details": details,
    }


def ingest_zip_into_group(zip_path: str, group_id: str) -> dict:
    if not os.path.isfile(zip_path):
        raise FileNotFoundError(f"Missing file: {zip_path}")

    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(zip_path, "r") as zf:
            _safe_extractall(zf, td)
        return ingest_directory_into_group(td, group_id)