"""Retry the 429-rate-limited URLs from board_verify_<date>.json with
throttling (1 worker, 0.8s sleep between requests) + honor Retry-After
header.
"""
from __future__ import annotations
import datetime as dt
import io
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
LOG_DIR = E156 / "audit_output"
TIMEOUT = 10.0
BASE_DELAY = 0.8
USER_AGENT = "Mozilla/5.0 (E156-retry)"


def check_once(url: str) -> dict:
    try:
        req = urllib.request.Request(url, method="HEAD",
            headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return {"status": resp.status, "url": url}
    except urllib.error.HTTPError as e:
        retry_after = None
        try:
            retry_after = int(e.headers.get("Retry-After", "0"))
        except Exception:
            pass
        return {"status": e.code, "url": url, "retry_after": retry_after}
    except Exception as e:
        return {"status": None, "url": url, "error": str(e)}


def main() -> int:
    date_tag = dt.datetime.now(dt.UTC).strftime("%Y-%m-%d")
    src = LOG_DIR / f"board_verify_{date_tag}.json"
    report = json.loads(src.read_text(encoding="utf-8"))

    # Collect unique 429 URLs
    urls_429: set[str] = set()
    for e in report["per_entry"]:
        for label in ("code", "protocol", "pages"):
            rec = e[label]
            if rec.get("status") == 429 and rec.get("url"):
                urls_429.add(rec["url"])
    urls = sorted(urls_429)
    print(f"Retrying {len(urls)} rate-limited URLs (sequential, {BASE_DELAY}s delay)...")

    results: dict[str, dict] = {}
    for i, u in enumerate(urls, 1):
        r = check_once(u)
        if r.get("status") == 429:
            # Respect retry-after, up to 10s
            wait = min(r.get("retry_after") or 5, 10)
            print(f"  [{i}/{len(urls)}] 429 again, sleeping {wait}s")
            time.sleep(wait)
            r = check_once(u)
        results[u] = r
        if i % 25 == 0:
            print(f"  [{i}/{len(urls)}] ...")
        time.sleep(BASE_DELAY)

    # Merge back into per_entry
    updated = 0
    for e in report["per_entry"]:
        for label in ("code", "protocol", "pages"):
            rec = e[label]
            if rec.get("status") == 429 and rec.get("url") in results:
                new = results[rec["url"]]
                if new.get("status") != 429:
                    e[label] = {**rec, "status": new.get("status"),
                                "error": new.get("error"), "retried": True}
                    updated += 1
    print(f"Updated {updated} per-entry records with retry results")

    # Recompute status distributions
    from collections import defaultdict
    def count_by(label):
        c = defaultdict(int)
        for e in report["per_entry"]:
            s = e[label].get("status")
            c[str(s) if s is not None else "NONE"] += 1
        return dict(c)

    report["summary"]["code_url_status_dist"] = count_by("code")
    report["summary"]["protocol_url_status_dist"] = count_by("protocol")
    report["summary"]["pages_url_status_dist"] = count_by("pages")
    report["retry_applied"] = True

    src.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {src}")
    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
