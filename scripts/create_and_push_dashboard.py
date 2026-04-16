"""For each repo_ok_pages_missing entry: generate a standard E156
dashboard (index.html) and push it to the repo's main branch.

The dashboard is minimal but complete:
  - Paper title + 156-word CURRENT BODY
  - Links back to the Code repo and the Protocol file
  - Link to the Synthēsis journal submission
  - Reference to the E156 student board for claiming
  - Plain HTML, no external CDN, fully self-contained so offline works

We push via `git` over HTTPS (gh's ambient token handles auth) rather
than the GitHub Contents API because:
  1. The repo may not have the branch yet; git handles that cleanly.
  2. A real commit lets Sentinel / Overmind run on the repo if hooks
     are installed.
  3. The commit is visible in git log (audit trail) vs an API-only
     push which is slightly less discoverable.

Usage:
  python create_and_push_dashboard.py                # dry-run
  python create_and_push_dashboard.py --limit 5      # do 5 first
  python create_and_push_dashboard.py --apply        # do all
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

AUDIT = Path(__file__).resolve().parents[1] / "audit_output" / "audit_links_2026-04-16.json"
WORKBOOK = Path(__file__).resolve().parents[1] / "rewrite-workbook.txt"


def _fetch_repo_intel(owner: str, repo: str) -> dict:
    """Best-effort gh-api pull of repo-level data so each dashboard is
    genuinely unique: README excerpt, primary language, file listing,
    last commit date.

    Fails soft — missing bits are rendered as empty strings.
    """
    out = {"readme_excerpt": "", "language": "", "files": [],
           "last_commit": "", "stars": 0, "topics": []}

    # README — gh will 404 if absent, don't let that kill the push.
    r = subprocess.run(
        ["gh", "api", f"repos/{owner}/{repo}/readme", "--jq", ".content"],
        capture_output=True, text=True,
    )
    if r.returncode == 0 and r.stdout.strip():
        import base64
        try:
            decoded = base64.b64decode(r.stdout.strip()).decode("utf-8", errors="replace")
            # Strip markdown-header prefix lines; take first 400 chars of prose.
            lines = [ln for ln in decoded.splitlines() if ln.strip() and not ln.startswith("#") and not ln.startswith("![")]
            out["readme_excerpt"] = " ".join(lines)[:400]
        except Exception:
            pass

    # Repo metadata — one call gets language, stars, topics, pushed_at.
    r = subprocess.run(
        ["gh", "api", f"repos/{owner}/{repo}",
         "--jq", ".language, .stargazers_count, .pushed_at, (.topics // [] | join(\",\"))"],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        parts = r.stdout.strip().splitlines()
        if len(parts) >= 4:
            out["language"] = parts[0] if parts[0] != "null" else ""
            try:
                out["stars"] = int(parts[1])
            except ValueError:
                out["stars"] = 0
            out["last_commit"] = parts[2][:10] if parts[2] != "null" else ""
            out["topics"] = [t.strip() for t in parts[3].split(",") if t.strip()]

    # Top-level file listing — 5 most interesting files.
    r = subprocess.run(
        ["gh", "api", f"repos/{owner}/{repo}/contents", "--jq", ".[] | .name"],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        all_files = [ln for ln in r.stdout.strip().splitlines() if ln]
        # Prioritise interesting files; drop noise.
        priority = ["README.md", "E156-PROTOCOL.md", "pyproject.toml",
                    "package.json", "index.html", "setup.py",
                    "requirements.txt", "app.py", "main.py"]
        picked = [f for f in priority if f in all_files]
        rest = [f for f in all_files if f not in picked and not f.startswith(".")]
        out["files"] = (picked + rest)[:6]

    return out


def _extract_result_highlight(body: str) -> str:
    """Pull the most likely "key result" sentence/number from the body.

    The E156 format puts the result in S4 ("Result (number+interval)").
    We heuristically grab the sentence that contains a CI, percentage,
    or point estimate + CI — that's the headline stat worth featuring.
    """
    # Patterns in priority order.
    pats = [
        re.compile(r"([^.]*?\b\d+\.?\d*\s*\([^)]*(?:CI|confidence)[^)]*\)[^.]*?\.)", re.IGNORECASE),
        re.compile(r"([^.]*?\b\d+\.?\d*\s*%[^.]*?\.)"),
        re.compile(r"([^.]*?\b(?:OR|HR|RR|SMD|MD|aOR|aHR)\s*[:=]?\s*-?\d+\.\d+[^.]*?\.)", re.IGNORECASE),
    ]
    for p in pats:
        m = p.search(body)
        if m:
            return m.group(1).strip()
    return ""


DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — E156 ◆ Synthēsis</title>
<meta name="description" content="E156 micro-paper: {title} ({estimand}, {type_field}). 7 sentences, 156 words. Targeting Synthēsis.">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ padding: 2rem 1rem; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; color: #1a1a1a; background: {bg_hue}; }}
  .wrap {{ max-width: 760px; margin: 0 auto; }}
  .mark {{ color: {accent_hue}; font-weight: 600; letter-spacing: 0.02em; font-size: 0.9rem; }}
  h1 {{ font-size: 1.55rem; line-height: 1.25; margin: 0.3rem 0 0.5rem; letter-spacing: -0.01em; }}
  .sub {{ color: #6b7280; font-size: 0.9rem; margin-bottom: 1.5rem; }}
  .sub code {{ background: #e5e7eb; padding: 1px 5px; border-radius: 3px; font-size: 0.85em; }}
  .highlight {{ background: linear-gradient(135deg, {accent_hue}22, {accent_hue}0a); border-left: 4px solid {accent_hue}; padding: 0.9rem 1.1rem; border-radius: 0 6px 6px 0; margin: 0 0 1.5rem; font-size: 1rem; color: #1f2937; }}
  .highlight strong {{ color: {accent_hue}; }}
  .body {{ background: white; padding: 1.5rem; border-radius: 8px; border: 1px solid #e5e7eb; margin-bottom: 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
  .body p {{ margin: 0; }}
  .readme {{ background: #fafafa; padding: 1rem 1.2rem; border-radius: 6px; border: 1px dashed #d1d5db; margin-bottom: 1.5rem; font-size: 0.88rem; color: #4b5563; font-style: italic; }}
  .readme::before {{ content: "FROM THE README — "; font-weight: 600; font-style: normal; color: #9ca3af; font-size: 0.75rem; letter-spacing: 0.05em; }}
  .stats {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.5rem; }}
  .chip {{ background: white; border: 1px solid #e5e7eb; border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.8rem; color: #4b5563; }}
  .chip strong {{ color: #1a1a1a; }}
  .links {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 0.5rem; margin-bottom: 1rem; }}
  .links a {{ display: block; padding: 0.7rem 1rem; background: white; border: 1px solid #e5e7eb; border-radius: 6px; color: #3730a3; text-decoration: none; font-size: 0.88rem; text-align: center; }}
  .links a:hover {{ background: #f3f4f6; border-color: {accent_hue}88; }}
  .files {{ background: #f9fafb; padding: 0.8rem 1rem; border-radius: 6px; border: 1px solid #e5e7eb; margin-bottom: 1.5rem; font-size: 0.83rem; color: #6b7280; }}
  .files code {{ background: white; border: 1px solid #e5e7eb; padding: 1px 6px; border-radius: 3px; margin: 0 2px; display: inline-block; color: #1f2937; }}
  .meta {{ font-size: 0.82rem; color: #4b5563; background: white; padding: 1rem 1.2rem; border-radius: 6px; border: 1px solid #e5e7eb; }}
  .meta dt {{ font-weight: 600; margin-top: 0.4rem; color: #111827; }}
  .meta dt:first-child {{ margin-top: 0; }}
  footer {{ margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e5e7eb; color: #9ca3af; font-size: 0.8rem; text-align: center; }}
  footer a {{ color: #6b7280; }}
</style>
</head>
<body>
<div class="wrap">

<p class="mark">◆ Synthēsis · {section}</p>
<h1>{title}</h1>
<p class="sub">Project <code>{name}</code> · <strong>{type_field}</strong> study · primary estimand <strong>{estimand}</strong></p>

{highlight_block}

<div class="stats">
  <span class="chip">📏 <strong>156 words</strong> / 7 sentences</span>
  {language_chip}
  {last_commit_chip}
  {stars_chip}
</div>

<div class="body">
<p>{body_html}</p>
</div>

{readme_block}

{files_block}

<div class="links">
  <a href="{code_url}">▶ Source code</a>
  <a href="{protocol_url}">📄 E156 protocol</a>
  <a href="https://mahmood726-cyber.github.io/e156/students.html" target="_blank">🎓 Claim this paper</a>
  <a href="https://www.synthesis-medicine.org/index.php/journal" target="_blank">📖 Synthēsis journal</a>
</div>

<div class="meta">
<dt>Target journal</dt>
<dd>◆ Synthēsis (synthesis-medicine.org) — section: {section}</dd>
<dt>Format contract</dt>
<dd>E156 micro-paper: exactly 7 sentences, ≤156 words, single paragraph</dd>
<dt>License</dt>
<dd>Manuscript: CC-BY-4.0 · Code: MIT</dd>
<dt>Status</dt>
<dd>{status}</dd>
</div>

<footer>
  Landing page for <code>{name}</code> · part of the E156 portfolio ·
  <a href="https://mahmood726-cyber.github.io/e156/students.html">claim this paper on the student board</a>
</footer>

</div>
</body>
</html>
"""


# Colour hues seeded from repo name — gives each page a stable but
# distinct accent so the portfolio looks alive rather than template-y.
_HUE_PALETTE = [
    ("#eef2ff", "#4338ca"),  # indigo
    ("#f0fdf4", "#15803d"),  # green
    ("#fff7ed", "#c2410c"),  # orange
    ("#fdf2f8", "#be185d"),  # pink
    ("#ecfeff", "#0e7490"),  # cyan
    ("#f5f3ff", "#6d28d9"),  # violet
    ("#fef3c7", "#92400e"),  # amber
    ("#f0f9ff", "#0369a1"),  # sky
]


def _hue_for(name: str) -> tuple[str, str]:
    h = sum(ord(c) for c in name) % len(_HUE_PALETTE)
    return _HUE_PALETTE[h]


def _extract_entry_details(num: int) -> dict | None:
    """Pull title, type, estimand, body, and section for an entry from the workbook."""
    text = WORKBOOK.read_text(encoding="utf-8")
    # Look for the entry header line `[N/M] name`
    pattern = re.compile(
        rf"\[{num}/\d+\]\s+(\S+)\s*\n"
        r"TITLE:\s*(.+?)\s*\n"
        r"TYPE:\s+(\S+)\s*\|\s*ESTIMAND:\s+(\S+)\s*\n"
        r".+?"
        r"CURRENT BODY \(\d+ words\):\s*\n(.+?)\n\s*\n"
        r".+?"
        r"Section:\s*([^\n(]+?)(?:\s*\(|\s*—|\n)",
        re.DOTALL,
    )
    m = pattern.search(text)
    if not m:
        return None
    return {
        "name": m.group(1),
        "title": m.group(2),
        "type_field": m.group(3),
        "estimand": m.group(4),
        "body": m.group(5).strip(),
        "section": m.group(6).strip() or "Methods Note",
    }


def build_dashboard(entry: dict, audit_entry: dict, owner: str, repo: str,
                    status: str = "Open — claim on the student board") -> str:
    """Pull live repo intel + unique accent hue and render a per-paper dashboard."""
    # Paragraph-safe HTML-escape for the body.
    esc = lambda s: (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    body_html = esc(entry["body"])

    intel = _fetch_repo_intel(owner, repo)
    bg_hue, accent_hue = _hue_for(repo)

    # Headline stat — pulled from the body's S4 result sentence.
    highlight_sentence = _extract_result_highlight(entry["body"])
    if highlight_sentence:
        highlight_block = (
            f'<div class="highlight"><strong>Key result:</strong> '
            f'{esc(highlight_sentence)}</div>'
        )
    else:
        highlight_block = ""

    # Repo-intel blocks (each rendered or empty if data missing).
    language_chip = (f'<span class="chip">💻 <strong>{esc(intel["language"])}</strong></span>'
                     if intel["language"] else "")
    last_commit_chip = (f'<span class="chip">🕒 last push <strong>{esc(intel["last_commit"])}</strong></span>'
                        if intel["last_commit"] else "")
    stars_chip = (f'<span class="chip">⭐ <strong>{intel["stars"]}</strong></span>'
                  if intel["stars"] else "")

    readme_block = ""
    if intel["readme_excerpt"]:
        readme_block = f'<div class="readme">{esc(intel["readme_excerpt"])}</div>'

    files_block = ""
    if intel["files"]:
        files_html = " ".join(f'<code>{esc(f)}</code>' for f in intel["files"])
        files_block = f'<div class="files">Repo contents: {files_html}</div>'

    return DASHBOARD_TEMPLATE.format(
        title=esc(entry["title"]), name=esc(entry["name"]),
        type_field=esc(entry["type_field"]), estimand=esc(entry["estimand"]),
        body_html=body_html, section=esc(entry["section"]),
        code_url=audit_entry["code"],
        protocol_url=audit_entry.get("protocol", audit_entry["code"]),
        status=esc(status),
        bg_hue=bg_hue, accent_hue=accent_hue,
        highlight_block=highlight_block,
        language_chip=language_chip, last_commit_chip=last_commit_chip,
        stars_chip=stars_chip,
        readme_block=readme_block, files_block=files_block,
    )


def push_to_repo(owner: str, repo: str, html: str, dry_run: bool = True) -> tuple[str, str]:
    """Clone repo, write/update index.html, commit + push.

    Returns (outcome, message) where outcome is one of:
      "pushed-new"       — no index.html existed, we added one
      "pushed-updated"   — index.html existed but ours is different; overwrote
      "skipped-same"     — index.html exists and matches ours; no push needed
      "failed"           — clone or push failed; see message
    """
    if dry_run:
        return "pushed-new", "dry-run"
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / repo
        clone = subprocess.run(
            ["gh", "repo", "clone", f"{owner}/{repo}", str(tmp)],
            capture_output=True, text=True,
        )
        if clone.returncode != 0:
            return "failed", f"clone failed: {clone.stderr[:120]}"
        head = subprocess.run(
            ["git", "-C", str(tmp), "symbolic-ref", "HEAD"],
            capture_output=True, text=True,
        ).stdout.strip()
        branch = head.rsplit("/", 1)[-1] if head else "main"

        index_path = tmp / "index.html"
        existed = index_path.exists()
        existing_content = index_path.read_text(encoding="utf-8", errors="replace") if existed else ""
        if existed and existing_content == html:
            return "skipped-same", "identical index.html already present"

        # Respect hand-made dashboards: if the existing file does NOT look
        # like one of our auto-generated E156 dashboards (our unique marker
        # is the "◆ Synthēsis · " string in the header + the
        # "Landing page for <code>" footer), skip to avoid clobbering.
        if existed and "Landing page for <code>" not in existing_content:
            return "failed", "index.html exists but isn't an E156 auto-dashboard — not clobbering"

        index_path.write_text(html, encoding="utf-8")
        action_msg = "update existing E156 dashboard" if existed else "add E156 dashboard"

        for cmd in [
            ["git", "-C", str(tmp), "add", "index.html"],
            ["git", "-C", str(tmp),
             "-c", "user.email=mahmood726-cyber@users.noreply.github.com",
             "-c", "user.name=mahmood726-cyber",
             "commit", "-m",
             f"feat(pages): {action_msg}\n\nAuto-generated per-paper E156 landing page — unique accent, repo\nintel (language, file list, last push, README excerpt), and the\n156-word body. Links back to the student claim board at\nhttps://mahmood726-cyber.github.io/e156/students.html."],
            ["git", "-C", str(tmp), "push", "origin", branch],
        ]:
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                return "failed", f"{' '.join(cmd[:4])} failed: {r.stderr[:150]}"

    return ("pushed-updated" if existed else "pushed-new"), f"pushed to {branch}"


def enable_pages(owner: str, repo: str) -> tuple[bool, str]:
    # Use gh CLI which already has the token
    r = subprocess.run([
        "gh", "api", "-X", "POST", f"repos/{owner}/{repo}/pages",
        "-f", "source[branch]=main", "-f", "source[path]=/",
    ], capture_output=True, text=True)
    if r.returncode == 0:
        return True, "enabled on main"
    # Retry with master
    if "422" in r.stderr or "branch" in r.stderr.lower():
        r2 = subprocess.run([
            "gh", "api", "-X", "POST", f"repos/{owner}/{repo}/pages",
            "-f", "source[branch]=master", "-f", "source[path]=/",
        ], capture_output=True, text=True)
        if r2.returncode == 0:
            return True, "enabled on master"
        return False, r2.stderr[:120]
    # Already enabled is fine
    if "already exists" in r.stderr.lower() or "409" in r.stderr:
        return True, "already enabled"
    return False, r.stderr[:120]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--start-at", type=int, default=0, help="skip first N targets (for resume)")
    args = ap.parse_args()

    audit = json.load(open(AUDIT, encoding="utf-8"))
    targets = [e for e in audit["entries"] if e["tag"] == "repo_ok_pages_missing"]
    targets = targets[args.start_at:]
    if args.limit:
        targets = targets[: args.limit]

    print(f"[dash] {len(targets)} repos will be processed")

    results = {"pushed_new": 0, "pushed_updated": 0,
               "has_existing_index": 0, "enabled_pages": 0,
               "pages_already": 0, "failed": []}

    for i, t in enumerate(targets, 1):
        parts = t["code"].rstrip("/").split("/")
        owner, repo = parts[-2], parts[-1]

        print(f"[{i}/{len(targets)}] {owner}/{repo}", end=" ")
        sys.stdout.flush()

        # Check whether repo already has an index.html via gh api — avoids
        # the expensive clone when the file is already present.
        r = subprocess.run(
            ["gh", "api", f"repos/{owner}/{repo}/contents/index.html",
             "--jq", ".type"],
            capture_output=True, text=True,
        )
        already_has_index = (r.returncode == 0 and r.stdout.strip() == "file")

        if already_has_index:
            results["has_existing_index"] += 1
            print("has index.html;", end=" ")
            if args.apply:
                ok2, msg2 = enable_pages(owner, repo)
                print(f"pages:{msg2}")
                if ok2:
                    if "already" in msg2.lower():
                        results["pages_already"] += 1
                    else:
                        results["enabled_pages"] += 1
                time.sleep(0.4)
            else:
                print("(dry-run — would enable Pages)")
            continue

        # No index.html yet — build one from the workbook entry and push.
        entry = _extract_entry_details(t["num"])
        if not entry:
            print(f"FAIL: couldn't parse workbook entry")
            results["failed"].append({"num": t["num"], "name": t["name"], "reason": "workbook parse failed"})
            continue

        html = build_dashboard(entry, t, owner, repo)
        print(f"({len(html)} B new)", end=" ")
        sys.stdout.flush()
        outcome, msg = push_to_repo(owner, repo, html, dry_run=not args.apply)
        if outcome == "failed":
            print(f"FAIL: {msg}")
            results["failed"].append({"num": t["num"], "name": t["name"], "reason": msg})
            continue

        print(f"push:{outcome}", end=" ")
        if outcome == "pushed-new":
            results["pushed_new"] += 1
        elif outcome == "pushed-updated":
            results["pushed_updated"] += 1

        if args.apply:
            ok2, msg2 = enable_pages(owner, repo)
            print(f"pages:{msg2}")
            if ok2:
                if "already" in msg2.lower():
                    results["pages_already"] += 1
                else:
                    results["enabled_pages"] += 1
            time.sleep(0.5)
        else:
            print()

    print()
    print("=" * 60)
    print(f"Pushed new dashboards:          {results['pushed_new']}")
    print(f"Pushed updated dashboards:      {results['pushed_updated']}")
    print(f"Had existing hand-made index:   {results['has_existing_index']}")
    print(f"Pages enabled (new):            {results['enabled_pages']}")
    print(f"Pages already enabled:          {results['pages_already']}")
    print(f"Failed:                         {len(results['failed'])}")
    if results["failed"]:
        print("\nFailures:")
        for f in results["failed"][:20]:
            print(f"  [{f['num']}] {f['name']}: {f['reason']}")

    log = Path(__file__).resolve().parents[1] / "audit_output" / "dashboards_pushed_log.json"
    log.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nLog: {log}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
