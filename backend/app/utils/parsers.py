from typing import List, Tuple, Iterable, Optional
import re

def _to_floats(line: str) -> Optional[List[float]]:
    parts = re.split(r"[,\s]+", line.strip())
    nums: List[float] = []
    for p in parts:
        if p == "":
            continue
        try:
            nums.append(float(p))
        except ValueError:
            return None
    return nums if nums else None


def parse_scandata(
    lines: Iterable[str],
) -> List[Tuple[int, float, float, float, float, Optional[float]]]:
    """
    Format: [ScanValue, Xpos, Ypos, Zpos, V]
    Returns list of (seq, raw, x, y, z, v).
    """
    seq = 0
    out: List[Tuple[int, float, float, float, float, Optional[float]]] = []
    for line in lines:
        nums = _to_floats(line)
        if not nums:
            continue
        if len(nums) < 4:
            continue
        raw, x, y, z = nums[0], nums[1], nums[2], nums[3]
        v = nums[4] if len(nums) >= 5 else None
        out.append((seq, raw, x, y, z, v))
        seq += 1
    return out


def parse_welddat(
    lines: Iterable[str],
) -> List[Tuple[int, float, float, float, float]]:
    """
    Format:[Feedrate, CurrentValue, VoltageValue, Xpos, Ypos, Zpos, TravelSpeed]
    Returns list of (seq, wire_feed_rate, robot_speed, current, voltage).
    """
    seq = 0
    out: List[Tuple[int, float, float, float, float]] = []
    for line in lines:
        nums = _to_floats(line)
        if not nums:
            continue
        if len(nums) < 7:
            continue
        wfr = nums[0]
        cur = nums[1]
        volt = nums[2]
        rs = nums[6]
        out.append((seq, wfr, rs, cur, volt))
        seq += 1
    return out