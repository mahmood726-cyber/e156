"""Generate the public e156 Assurance dashboard for GitHub Pages.

Collects every assurance.json in the repo and renders a single offline,
self-contained `assurance.html` (no CDN, no hardcoded local paths) showing each
capsule's tier, per-check verdicts, and whether the badge is cryptographically
signed. Served by the repo's EXISTING GitHub Pages setup (the assurance
workflow commits this file; it does NOT run a deploy-pages job that would
overwrite the rest of the site).

Anyone visiting <user>.github.io/<repo>/assurance.html can see how much
reassurance each capsule carries.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TIER_META = {
    "gold": ("Gold", "#d4af37"),
    "silver": ("Silver", "#9aa0a6"),
    "bronze": ("Bronze", "#cd7f32"),
    "none": ("Unrated", "#cfcfcf"),
}
CHECK_KEYS = [
    "citation_cascade", "denominator_logic", "claim_language",
    "data_file_present", "code_runs", "dashboard_match",
    "analysis_rerun", "external_review",
]
VERDICT_MARK = {"pass": "&#10003;", "warn": "!", "fail": "&#10007;", "not-run": "&middot;"}
LOCK = "&#128274;"
DASH = "&mdash;"

_CSS = """<style>
body{font-family:system-ui,Segoe UI,Arial,sans-serif;margin:2rem;color:#1a1a1a;background:#fafafa}
h1{margin-bottom:.2rem}
.motto{font-style:italic;color:#555;margin-top:0}
table{border-collapse:collapse;width:100%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.1)}
th,td{padding:.4rem .6rem;border-bottom:1px solid #eee;text-align:center;font-size:.9rem}
th:first-child,td:first-child{text-align:left}
.pill{display:inline-block;padding:.1rem .55rem;border-radius:1rem;color:#222;font-weight:600;font-size:.8rem}
.foot{color:#666;font-size:.85rem;margin-top:1rem}
</style>"""


def _esc(value) -> str:
    return html.escape(str(value))


def collect_badges(root: Path) -> list[dict]:
    out: list[dict] = []
    for p in sorted(root.rglob("assurance.json")):
        if ".git" in p.parts:
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(data, dict):
            continue
        data = dict(data)
        data["_rel"] = p.relative_to(root).as_posix()
        data["_signed"] = bool(data.get("signature"))
        out.append(data)
    return out


def build_dashboard_html(badges, *, title="e156 Assurance Status", generated_at=None) -> str:
    generated_at = generated_at or datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    counts = {t: 0 for t in TIER_META}
    rows = []
    for b in sorted(badges, key=lambda x: (x.get("tier", ""), x.get("_rel", ""))):
        tier = str(b.get("tier", "none"))
        counts[tier] = counts.get(tier, 0) + 1
        label, color = TIER_META.get(tier, ("Unrated", "#cfcfcf"))
        name = _esc(b.get("project_name") or b.get("_rel", "?"))
        checks = b.get("checks") if isinstance(b.get("checks"), dict) else {}
        cells = "".join(
            '<td title="' + _esc(k) + ": " + _esc(checks.get(k, "-")) + '">'
            + VERDICT_MARK.get(str(checks.get(k)), "&middot;") + "</td>"
            for k in CHECK_KEYS
        )
        signed = LOCK if (b.get("signature") or b.get("_signed")) else DASH
        rows.append(
            "<tr><td>" + name + '</td><td><span class="pill" style="background:'
            + color + '">' + _esc(label) + "</span></td>" + cells
            + "<td>" + signed + "</td></tr>"
        )
    head_cells = "".join("<th>" + _esc(k.replace("_", " ")) + "</th>" for k in CHECK_KEYS)
    summary = (" &middot; ").join(
        TIER_META[t][0] + ": " + str(counts.get(t, 0)) for t in ("gold", "silver", "bronze", "none")
    )
    parts = [
        "<!doctype html>",
        '<html lang="en"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>" + _esc(title) + "</title>",
        '<meta property="og:title" content="' + _esc(title) + '">',
        _CSS,
        "</head><body>",
        "<h1>" + _esc(title) + "</h1>",
        '<p class="motto">The capsule must agree with itself before asking the world to agree with it.</p>',
        "<p>" + summary + " " + DASH + " generated " + _esc(generated_at) + "</p>",
        "<table><thead><tr><th>Capsule</th><th>Tier</th>" + head_cells + "<th>Signed</th></tr></thead><tbody>",
        "".join(rows),
        "</tbody></table>",
        '<p class="foot">Tiers are derived from automated checks, never hand-set. '
        + LOCK + " = cryptographically signed. Marks: &#10003; pass &middot; ! warn &middot; &#10007; fail &middot; &middot; not-run.</p>",
        "</body></html>",
    ]
    return "\n".join(parts)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build the public e156 assurance dashboard.")
    ap.add_argument("--repo", default=".", help="Repo root to scan (default: cwd)")
    ap.add_argument("--out", help="Output HTML path (default: <repo>/assurance.html)")
    args = ap.parse_args(argv)
    root = Path(args.repo).resolve()
    if not root.is_dir():
        sys.stderr.write(f"not a directory: {root}\n")
        return 2
    badges = collect_badges(root)
    out = Path(args.out) if args.out else root / "assurance.html"
    out.write_text(build_dashboard_html(badges), encoding="utf-8")
    print(f"wrote {out} ({len(badges)} badges)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
