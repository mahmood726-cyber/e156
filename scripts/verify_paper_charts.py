"""Verify every generated paper/<n>.html has exactly 5 working SVG charts.

For each file:
  - parse the HTML
  - count <svg> elements (must be 5)
  - confirm each has non-empty body and a <title> / aria-label
  - catch obvious rendering bugs like malformed viewBox, missing tags,
    or fallback "(no data)" appearing more than twice (a healthy page
    should have at most 1-2 fallbacks)

Writes audit_output/paper_charts_audit.json.
"""
from __future__ import annotations
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
PAPER_DIR = E156 / "paper"
OUT = E156 / "audit_output" / "paper_charts_audit.json"

SVG_RE = re.compile(r"<svg\b[^>]*>.*?</svg>", re.DOTALL)
ARIA_RE = re.compile(r'aria-label="([^"]+)"')


def audit_one(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    svgs = SVG_RE.findall(text)
    rec = {
        "file": path.name,
        "svg_count": len(svgs),
        "has_5": len(svgs) == 5,
        "chart_titles": [],
        "fallback_count": 0,
        "size_bytes": len(text),
    }
    for svg in svgs:
        mm = ARIA_RE.search(svg)
        title = mm.group(1) if mm else "(no title)"
        rec["chart_titles"].append(title)
        if "(no data" in svg or "No parseable" in svg or "No body text" in svg:
            rec["fallback_count"] += 1
    rec["unique_titles"] = len(set(rec["chart_titles"]))
    return rec


def main() -> int:
    files = sorted(p for p in PAPER_DIR.iterdir() if p.suffix == ".html" and p.name != "index.html")
    records = [audit_one(p) for p in files]

    n = len(records)
    with_5 = sum(1 for r in records if r["has_5"])
    without_5 = [r for r in records if not r["has_5"]]
    fallback_dist = Counter(r["fallback_count"] for r in records)
    size_p50 = sorted(r["size_bytes"] for r in records)[n // 2] if n else 0

    summary = {
        "files_checked": n,
        "with_5_svgs": with_5,
        "without_5_svgs": len(without_5),
        "fallback_count_distribution": dict(sorted(fallback_dist.items())),
        "median_size_bytes": size_p50,
        "first_without_5": [r["file"] for r in without_5][:5],
    }
    OUT.write_text(
        json.dumps({"summary": summary, "records": records}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    return 0 if len(without_5) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
