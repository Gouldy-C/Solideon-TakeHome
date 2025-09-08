from pathlib import Path
import json
from typing import Any, Dict, Optional, Union

CONFIG: Dict[str, Any] = {}
_CONFIG_DIR: Optional[Path] = None


def _deep_merge(a: Dict[str, Any], b: Dict[str, Any]) -> Dict[str, Any]:
    res = dict(a)
    for k, v in b.items():
        if k in res and isinstance(res[k], dict) and isinstance(v, dict):
            res[k] = _deep_merge(res[k], v)
        else:
            res[k] = v
    return res


def _load_dir(directory: Path) -> Dict[str, Any]:
    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    out: Dict[str, Any] = {}
    for path in sorted(directory.glob("*.json"), key=lambda p: p.name.lower()):
        key = path.stem
        with path.open("r", encoding="utf-8-sig") as f:
            data = json.load(f)
        if key in out:
            raise ValueError(f"Duplicate config key '{key}' from file: {path}")
        out[key] = data
    return out


def init_load(directory: Union[str, Path]) -> Dict[str, Any]:
    global _CONFIG_DIR
    _CONFIG_DIR = Path(directory).expanduser().resolve()
    CONFIG.clear()
    CONFIG.update(_load_dir(_CONFIG_DIR))
    return CONFIG


def reload() -> Dict[str, Any]:
    if _CONFIG_DIR is None:
        raise RuntimeError("Call init_load(directory) first")
    CONFIG.clear()
    CONFIG.update(_load_dir(_CONFIG_DIR))
    return CONFIG