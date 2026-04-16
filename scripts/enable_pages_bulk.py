"""Enable GitHub Pages on every repo flagged as repo_ok_pages_missing.

Uses the GitHub REST API:
  POST /repos/{owner}/{repo}/pages
  body: {"source": {"branch": "main", "path": "/"}}

Some repos serve Pages from /docs; we try main//, fall back to
main/docs, then master/ and master/docs. We stop at the first 2xx.

Prereq: `gh auth login` already done (we re-use gh's token via
`gh auth token`). Without it, Pages creation requires a PAT with the
`pages:write` scope.

Usage:
  python enable_pages_bulk.py                  # dry-run
  python enable_pages_bulk.py --apply          # actually call the API
  python enable_pages_bulk.py --limit 10       # test on 10 repos first
"""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[1] / "audit_output" / "audit_links_2026-04-16.json"


def gh_token() -> str:
    r = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True)
    return r.stdout.strip()


def enable_pages(owner: str, repo: str, token: str, branch: str = "main",
                 path: str = "/") -> tuple[int, str]:
    """Return (status_code, response_body_excerpt)."""
    body = json.dumps({"source": {"branch": branch, "path": path}})
    cmd = [
        "curl", "-s", "-X", "POST",
        "-H", f"Authorization: Bearer {token}",
        "-H", "Accept: application/vnd.github+json",
        "-H", "X-GitHub-Api-Version: 2022-11-28",
        "-w", "\n---STATUS:%{http_code}",
        "-d", body,
        f"https://api.github.com/repos/{owner}/{repo}/pages",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = r.stdout
    # Parse out the status from the suffix
    status = 0
    if "---STATUS:" in out:
        body_text, _, tail = out.rpartition("---STATUS:")
        try:
            status = int(tail.strip())
        except ValueError:
            pass
    else:
        body_text = out
    return status, body_text[:200]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--audit", default=str(AUDIT))
    args = ap.parse_args()

    audit = json.load(open(args.audit, encoding="utf-8"))
    targets = [e for e in audit["entries"] if e["tag"] == "repo_ok_pages_missing"]
    if args.limit:
        targets = targets[: args.limit]

    print(f"[pages] {len(targets)} repos need Pages enabled", file=sys.stderr)
    if not args.apply:
        for t in targets[:10]:
            print(f"  [{t['num']}] {t['name']:<28} {t['code']}")
        print(f"\n[dry-run] run with --apply to call the API.")
        return 0

    token = gh_token()
    results = {"ok": 0, "already_enabled": 0, "branch_not_main": 0, "failed": [], "rate_limited": 0}

    for i, t in enumerate(targets, 1):
        # Extract owner/repo from the code URL
        parts = t["code"].rstrip("/").split("/")
        owner, repo = parts[-2], parts[-1]

        print(f"[{i}/{len(targets)}] {owner}/{repo}", file=sys.stderr, flush=True)
        # Try main / first
        status, body = enable_pages(owner, repo, token, "main", "/")
        if status == 201:
            results["ok"] += 1
        elif status == 409 and "already exists" in body.lower():
            results["already_enabled"] += 1
        elif status == 422:
            # Maybe it's master / or the branch doesn't exist. Try master.
            status2, body2 = enable_pages(owner, repo, token, "master", "/")
            if status2 == 201:
                results["ok"] += 1
                results["branch_not_main"] += 1
            else:
                results["failed"].append({"repo": f"{owner}/{repo}", "status": status2, "body": body2[:120]})
        elif status == 403 and "rate limit" in body.lower():
            results["rate_limited"] += 1
            time.sleep(60)
        else:
            results["failed"].append({"repo": f"{owner}/{repo}", "status": status, "body": body[:120]})

        # Gentle pace — GitHub allows ~5000 req/hr authenticated
        time.sleep(0.25)

    print()
    print("=" * 60)
    print(f"Enabled Pages on {results['ok']} repos "
          f"({results['branch_not_main']} used master instead of main)")
    print(f"Already enabled:  {results['already_enabled']}")
    print(f"Rate limited:     {results['rate_limited']}")
    print(f"Failed:           {len(results['failed'])}")
    if results["failed"]:
        print("\nFailures:")
        for f in results["failed"][:20]:
            print(f"  {f['repo']:<50} [{f['status']}] {f['body']}")

    # Save detailed log
    out = Path(__file__).resolve().parents[1] / "audit_output" / "pages_enabled_log.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nLog: {out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
