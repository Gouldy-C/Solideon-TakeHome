import os
import re
import tempfile
import zipfile
from sqlmodel import select
from database.db import get_session
from database.models import WeldGroup, Layer, Waypoint, WeldSample
from utils.parsers import parse_scandata, parse_welddat
from utils.transforms import transform_scan_value

PAIR_RE = re.compile(r"^w(\d+)_([a-zA-Z]+)\.txt$")


def _pair_files(data_dir: str):
    files = [f for f in os.listdir(data_dir) if f.endswith(".txt")]
    layers = {}
    for f in files:
        m = PAIR_RE.match(f)
        if not m:
            continue
        num = int(m.group(1))
        kind = m.group(2).lower()
        entry = layers.setdefault(num, {"scandata": None, "welddat": None})
        if "scan" in kind:
            entry["scandata"] = os.path.join(data_dir, f)
        elif "weld" in kind:
            entry["welddat"] = os.path.join(data_dir, f)
    return layers


def _get_or_create_group(session, group_name: str) -> WeldGroup:
    group = session.exec(
        select(WeldGroup).where(WeldGroup.name == group_name)
    ).first()
    if not group:
        group = WeldGroup(name=group_name)
        session.add(group)
        session.commit()
        session.refresh(group)
    return group


def ingest_directory(data_dir: str, group_name: str = "default") -> dict:
    assert os.path.isdir(data_dir), f"Directory not found: {data_dir}"
    pairs = _pair_files(data_dir)
    created_layers = 0

    with get_session() as session:
        group = _get_or_create_group(session, group_name)

        for layer_number, files in sorted(pairs.items()):
            if not files["scandata"] or not files["welddat"]:
                continue

            layer = Layer(
                group_id=group.id,
                layer_number=layer_number,
                scandata_file=files["scandata"],
                welddat_file=files["welddat"],
            )
            session.add(layer)
            session.commit()
            session.refresh(layer)

            # Parse scan data -> waypoints
            with open(files["scandata"], "r") as f:
                scan_rows = parse_scandata(f)

            waypoints = []
            for seq, raw, x, y, z, v in scan_rows:
                waypoints.append(
                    Waypoint(
                        layer_id=layer.id,
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

            # Parse weld data -> samples
            with open(files["welddat"], "r") as f:
                weld_rows = parse_welddat(f)

            samples = []
            for seq, wfr, rs, cur, volt in weld_rows:
                samples.append(
                    WeldSample(
                        layer_id=layer.id,
                        seq=seq,
                        wire_feed_rate=wfr,
                        robot_speed=rs,
                        current=cur,
                        voltage=volt,
                    )
                )
            session.add_all(samples)
            session.commit()
            created_layers += 1

    return {"group": group_name, "layers_ingested": created_layers}


def ingest_pair(
    scandata_path: str,
    welddat_path: str,
    layer_number: int,
    group_name: str = "default",
) -> dict:
    """
    Ingest a single layer pair from explicit file paths and layer number.
    """
    assert os.path.isfile(scandata_path), f"Missing file: {scandata_path}"
    assert os.path.isfile(welddat_path), f"Missing file: {welddat_path}"

    with get_session() as session:
        group = _get_or_create_group(session, group_name)

        layer = Layer(
            group_id=group.id,
            layer_number=layer_number,
            scandata_file=scandata_path,
            welddat_file=welddat_path,
        )
        session.add(layer)
        session.commit()
        session.refresh(layer)

        with open(scandata_path, "r") as f:
            scan_rows = parse_scandata(f)
        waypoints = []
        for seq, raw, x, y, z, v in scan_rows:
            waypoints.append(
                Waypoint(
                    layer_id=layer.id,
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
        samples = []
        for seq, wfr, rs, cur, volt in weld_rows:
            samples.append(
                WeldSample(
                    layer_id=layer.id,
                    seq=seq,
                    wire_feed_rate=wfr,
                    robot_speed=rs,
                    current=cur,
                    voltage=volt,
                )
            )
        session.add_all(samples)
        session.commit()

        return {"group": group_name, "layer_id": layer.id, "layer_number": layer.layer_number}


def ingest_zip(zip_path: str, group_name: str = "default") -> dict:
    """
    Extract a ZIP and ingest all matching pairs inside.
    """
    assert os.path.isfile(zip_path), f"Missing file: {zip_path}"
    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(td)
        return ingest_directory(td, group_name=group_name)