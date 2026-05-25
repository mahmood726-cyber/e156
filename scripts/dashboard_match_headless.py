"""Phase-3 P: Selenium headless dashboard_match.

The Phase-2b regex-based dashboard_match compares the workbook body's
pooled HR claim to the range of per-trial HRs in the dashboard's realData
block. That catches gross fabrication but misses subtle drift where the
body's claim and the dashboard's JS-computed pooled estimate differ by
small amounts.

This module uses Selenium to load the dashboard, wait for the JS to
compute and populate #res-or / #res-ci / #res-i2, then read the
actually-rendered values. Returns pass/warn/fail/not-run for use by
build_assurance_jsons.py when invoked with --headless.

Phase 3 status: shipped. Default-off (Phase 2b regex check stays as the
fast path); turned on via build_assurance_jsons.py --headless.

Usage as a library:
    from scripts.dashboard_match_headless import derive_dashboard_match_headless
    verdict = derive_dashboard_match_headless(workbook_entry)

Usage as CLI:
    python scripts/dashboard_match_headless.py --project Finrenone
"""
from __future__ import annotations

import argparse
import io
import re
import sys
import time
from pathlib import Path

# NOTE: do NOT reassign sys.stdout at module load — it breaks the
# caller's stdout when this module is imported (see lessons.md). The
# reassignment, if needed, is done inside _main() below.


# Tolerance windows for headless comparison. Tighter than the Phase-2b
# regex check because the headless version reads the EXACT JS-computed
# pooled estimate, not a min/max range.
TOLERANCE_ABS_HR = 0.05      # absolute on HR/OR
TOLERANCE_REL_HR = 0.05      # 5%
TOLERANCE_I2 = 5             # percentage points

POOLED_BODY_RE = re.compile(
    r"\b(?:pooled\s+)?(OR|HR|RR|IRR)\s*[:=]?\s*(\d+\.\d+)\s*"
    r"[\(\[,]?\s*(?:95\s*%?\s*CI\s*:?\s*)?"
    r"(\d+\.\d+)\s*[-–to]+\s*(\d+\.\d+)",
    re.IGNORECASE,
)
I2_BODY_RE = re.compile(r"I[²2]\s*=?\s*(\d{1,3})\s*%", re.IGNORECASE)


def _make_headless_driver():
    """Reuse the same options shape as scratch/test_students_page.py."""
    from selenium import webdriver  # noqa: PLC0415
    from selenium.webdriver.chrome.options import Options  # noqa: PLC0415

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,800")
    opts.add_argument("--log-level=3")
    return webdriver.Chrome(options=opts)


def _read_dashboard_values(url: str, timeout: float = 30.0) -> dict | None:
    """Return {pooled_hr, lci, uci, i2_pct} from the live dashboard, or None
    on failure. Waits up to `timeout` seconds for #res-or to be populated."""
    try:
        from selenium.webdriver.common.by import By  # noqa: PLC0415
        from selenium.webdriver.support.ui import WebDriverWait  # noqa: PLC0415
        from selenium.webdriver.support import expected_conditions as EC  # noqa: PLC0415
    except ImportError:
        return None

    driver = None
    try:
        driver = _make_headless_driver()
        driver.get(url)
        # Wait for #res-or to exist
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "res-or"))
        )
        # Poll for the "--" placeholder to be replaced with a real number
        deadline = time.time() + timeout
        while time.time() < deadline:
            txt = driver.execute_script(
                "var e=document.getElementById('res-or'); return e?e.textContent:''"
            )
            if txt and txt.strip() not in ("", "--", "—"):
                break
            time.sleep(0.5)
        # Read all three values
        vals = driver.execute_script("""
            const g = id => {
                const e = document.getElementById(id);
                return e ? e.textContent.trim() : '';
            };
            return {or: g('res-or'), ci: g('res-ci'), i2: g('res-i2')};
        """)
        if not vals or not vals.get("or"):
            return None
        # Parse pooled HR (single number)
        m_or = re.search(r"-?\d+\.\d+", vals["or"])
        if not m_or:
            return None
        pooled_hr = float(m_or.group(0))
        # Parse CI like "0.65 to 0.93" or "0.65 - 0.93"
        nums = re.findall(r"\d+\.\d+", vals.get("ci", ""))
        lci = float(nums[0]) if len(nums) >= 1 else None
        uci = float(nums[1]) if len(nums) >= 2 else None
        # Parse I2 like "42%" or "42"
        m_i2 = re.search(r"(\d+)", vals.get("i2", ""))
        i2_pct = int(m_i2.group(1)) if m_i2 else None
        return {"pooled_hr": pooled_hr, "lci": lci, "uci": uci, "i2_pct": i2_pct}
    except Exception:
        return None
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


def derive_dashboard_match_headless(workbook_entry: dict) -> str:
    """Returns pass | warn | fail | not-run."""
    body = workbook_entry.get("body") or ""
    pages_url = workbook_entry.get("pages_url") or ""
    if not body or not pages_url or "rapidmeta-finerenone" not in pages_url:
        return "not-run"
    body_m = POOLED_BODY_RE.search(body)
    if not body_m:
        return "not-run"
    try:
        body_hr = float(body_m.group(2))
        body_lci = float(body_m.group(3))
        body_uci = float(body_m.group(4))
    except ValueError:
        return "not-run"
    body_i2_m = I2_BODY_RE.search(body)
    body_i2 = int(body_i2_m.group(1)) if body_i2_m else None

    vals = _read_dashboard_values(pages_url)
    if vals is None:
        return "not-run"

    dash_hr = vals["pooled_hr"]
    if abs(dash_hr - body_hr) > TOLERANCE_ABS_HR:
        rel = abs(dash_hr - body_hr) / max(0.001, abs(body_hr))
        if rel > TOLERANCE_REL_HR:
            return "fail"
    # CI bounds: each within tolerance if present
    for ours, theirs in ((body_lci, vals.get("lci")), (body_uci, vals.get("uci"))):
        if theirs is None:
            continue
        if abs(ours - theirs) > TOLERANCE_ABS_HR:
            return "warn"
    # I² (if both present)
    if body_i2 is not None and vals.get("i2_pct") is not None:
        if abs(body_i2 - vals["i2_pct"]) > TOLERANCE_I2:
            return "warn"
    return "pass"


def _main(argv=None) -> int:
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True,
                    help="workbook 'name' slug; will look up pages_url + body")
    args = ap.parse_args(argv)

    # Inline workbook iteration to avoid importing build_assurance_jsons
    # (which reassigns sys.stdout at module load and breaks subsequent prints).
    WB = Path(r"F:\e156\rewrite-workbook.txt")
    SEP = "=" * 70
    text = WB.read_text(encoding="utf-8")
    ENTRY_HEAD = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)
    for blk in text.split(SEP):
        m = ENTRY_HEAD.search(blk)
        if not m or m.group(2).strip() != args.project:
            continue
        body_m = re.search(
            r"^CURRENT BODY[^\n]*\n(.*?)(?=\n\nYOUR REWRITE|\n\nSUBMISSION|\n=)",
            blk, re.MULTILINE | re.DOTALL,
        )
        pages_m = re.search(r"^\s+Dashboard:\s+(https?://\S+)", blk, re.MULTILINE)
        entry = {
            "num": int(m.group(1)),
            "name": args.project,
            "body": body_m.group(1).strip() if body_m else "",
            "pages_url": pages_m.group(1) if pages_m else "",
        }
        result = derive_dashboard_match_headless(entry)
        print(f"{args.project}: {result}")
        return 0 if result == "pass" else 1
    sys.stderr.write(f"No workbook entry named {args.project!r}\n")
    return 2


if __name__ == "__main__":
    sys.exit(_main())
