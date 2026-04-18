"""Remove entry numbers of successfully-pushed targets from hide_repo_404.json.

Reads push_log_<date>.jsonl and push_retry_log_<date>.jsonl (today's date),
collects every `entry_nums` from records where `status == "OK"`, drops
those numbers from the hide list.

Also accepts a list of target repos via --also-pushed-manually NAME[,NAME]
for cases where a repo was pushed outside the logged pipeline (e.g. a
one-off `git push -u origin main` in a failed dir). Those targets are
resolved to their entry_nums via resolution_plan.json.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
from pathlib import Path

E156 = Path(__file__).resolve().parents[1]
HIDE_LIST = E156 / "audit_output" / "hide_repo_404.json"
PLAN = E156 / "audit_output" / "resolution_plan.json"
LOG_DIR = E156 / "audit_output"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=dt.datetime.now(dt.UTC).strftime("%Y-%m-%d"))
    ap.add_argument("--also-pushed-manually", default="",
                    help="Comma-separated target repo names pushed outside the pipeline")
    args = ap.parse_args()

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    target_to_nums: dict[str, list[int]] = {
        g["target_repo"]: g["entry_nums"] for g in plan["push_from_local"]
    }

    hide_nums = set(json.loads(HIDE_LIST.read_text(encoding="utf-8")))
    before = len(hide_nums)

    unhidden: list[dict] = []

    for logname in (f"push_log_{args.date}.jsonl", f"push_retry_log_{args.date}.jsonl"):
        path = LOG_DIR / logname
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if r["status"] != "OK":
                continue
            for num in r["entry_nums"]:
                if num in hide_nums:
                    hide_nums.discard(num)
                    unhidden.append({"num": num, "target": r["target"], "source_log": logname})

    manual = [n.strip() for n in args.also_pushed_manually.split(",") if n.strip()]
    for target in manual:
        nums = target_to_nums.get(target, [])
        if not nums:
            print(f"WARN: manual target {target!r} not in resolution_plan push_from_local")
            continue
        for num in nums:
            if num in hide_nums:
                hide_nums.discard(num)
                unhidden.append({"num": num, "target": target, "source_log": "manual"})

    HIDE_LIST.write_text(json.dumps(sorted(hide_nums)) + "\n", encoding="utf-8")
    print(f"Hide list: {before} -> {len(hide_nums)} ({before - len(hide_nums)} un-hidden)")
    print(f"Unique targets un-hidden: {len({u['target'] for u in unhidden})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
