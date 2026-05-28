"""Locate the Sentinel repo on this machine.

The e156 assurance layer spans two repos: the badge builder lives in E156
(scripts/build_assurance_jsons.py) while the detection rules live in
Sentinel. These helpers find Sentinel without hardcoding a single drive
(lessons.md: "Do not hardcode one drive"). Resolution order:

  1. $SENTINEL_ROOT
  2. C:\\Sentinel  (NTFS junction on this PC)
  3. F:\\Sentinel  (canonical)
  4. sibling of the E156 repo root (e.g. C:\\E156 -> C:\\Sentinel)

Returns None if none resolve, so callers can skip with a clear reason
instead of failing on a machine that only has the E156 checkout.
"""
from __future__ import annotations

import os
from pathlib import Path


def find_sentinel_root() -> Path | None:
    candidates: list[Path] = []
    env = os.environ.get("SENTINEL_ROOT")
    if env:
        candidates.append(Path(env))
    candidates.append(Path(r"C:\Sentinel"))
    candidates.append(Path(r"F:\Sentinel"))
    here = Path(__file__).resolve()
    candidates.append(here.parents[2] / "Sentinel")  # C:\E156\tests\x -> C:\Sentinel
    for c in candidates:
        if (c / "sentinel" / "rules" / "plugins").is_dir():
            return c
    return None


def plugins_dir() -> Path | None:
    root = find_sentinel_root()
    return (root / "sentinel" / "rules" / "plugins") if root else None
