"""Expire E156 claims older than CLAIM_WINDOW_DAYS without a submission.

Run periodically (weekly cron or manual). If a claim has
`status == "claimed"` and `claim_date` is more than 42 days ago, remove
the entry from claims.json — the paper reopens on the student board.

Does not touch submitted claims (those stay forever as historical record).

Usage:
  python expire_stale_claims.py              # show what would expire
  python expire_stale_claims.py --apply      # actually remove stale entries
  python expire_stale_claims.py --apply --window 56   # custom window (days)

The page's JS ALSO treats out-of-window claims as expired (they show
reopened on load), so running this script is mostly for cleaning up the
claims.json file itself.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

CLAIMS = Path(__file__).resolve().parents[1] / "claims.json"
DEFAULT_WINDOW_DAYS = 30
EXTENSION_DAYS = 10


def main() -> int:
    # P2-7 — guard docstring-based description against a stripped __doc__.
    desc = (__doc__ or "Expire stale E156 claims.").splitlines()[0]
    ap = argparse.ArgumentParser(description=desc)
    ap.add_argument("--apply", action="store_true", help="actually remove stale entries (default is dry-run)")
    ap.add_argument("--window", type=int, default=DEFAULT_WINDOW_DAYS, help=f"days until claim expires (default {DEFAULT_WINDOW_DAYS}; +{EXTENSION_DAYS} if extended)")
    args = ap.parse_args()

    if not CLAIMS.is_file():
        print(f"{CLAIMS} does not exist yet; nothing to expire.", file=sys.stderr)
        return 0

    data = json.loads(CLAIMS.read_text(encoding="utf-8") or "{}")
    if not data:
        print("claims.json is empty; nothing to expire.")
        return 0

    today = dt.date.today()

    to_expire: list[tuple[str, dict, int]] = []
    kept: dict[str, dict] = {}

    for num, entry in data.items():
        status = entry.get("status", "claimed")
        claim_date_str = entry.get("claim_date", "")
        if status == "submitted":
            kept[num] = entry
            continue
        try:
            claim_date = dt.date.fromisoformat(claim_date_str)
        except ValueError:
            print(f"  [warn] paper #{num}: invalid claim_date {claim_date_str!r} — keeping as-is")
            kept[num] = entry
            continue
        # Per-claim window: base + extension if granted
        window = args.window + (EXTENSION_DAYS if entry.get("extended") else 0)
        age = (today - claim_date).days
        if age > window:
            to_expire.append((num, entry, age))
        else:
            kept[num] = entry

    print(f"{'Paper':>7}  {'Name':<25}  {'Claimed':<12}  {'Age(d)':>6}  Action")
    print("-" * 72)
    for num, entry, age in sorted(to_expire, key=lambda x: -x[2]):
        print(f"  #{num:<5}  {entry.get('name', '?')[:25]:<25}  {entry.get('claim_date', '?'):<12}  {age:>6}  EXPIRE (reopen)")

    print()
    print(f"Summary: {len(data)} total claims, {len(to_expire)} to expire, {len(kept)} kept")

    if not to_expire:
        return 0

    if args.apply:
        CLAIMS.write_text(json.dumps(kept, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"\nWrote {CLAIMS}: {len(kept)} entries remaining. Commit + push to refresh the board.")
    else:
        print("\n[DRY RUN — pass --apply to actually remove the stale entries]")

    return 0


if __name__ == "__main__":
    sys.exit(main())
