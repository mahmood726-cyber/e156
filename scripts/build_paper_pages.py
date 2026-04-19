"""Generate a unique per-paper HTML info dashboard for every visible E156
entry. Writes to C:/E156/paper/<num>.html, served at
`https://mahmood726-cyber.github.io/e156/paper/<num>.html`.

Fields rendered:
  num, title, type, estimand, data, body (156 words), references,
  corresponding author, affiliation, target journal, protocol URL,
  code URL, claim button.

Matches students.html's dark-theme styling for visual consistency.
"""
from __future__ import annotations
import html as htmlmod
import io
import json
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
HIDE_LIST = E156 / "audit_output" / "hide_repo_404.json"
OUT_DIR = E156 / "paper"

SEP = "=" * 70
ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)
GH_ISSUE_BASE = "https://github.com/mahmood726-cyber/e156/issues/new"


def esc(s: str) -> str:
    return htmlmod.escape(s or "", quote=True)


def parse_entries() -> list[dict]:
    text = WORKBOOK.read_text(encoding="utf-8")
    # P0-4 — strip BOM if present (mirrors build_students_page.py)
    text = text.lstrip("\ufeff")
    blocks = text.split(SEP)
    out: list[dict] = []
    seen: set[int] = set()
    for block in blocks:
        m = ENTRY_HEAD_RE.search(block)
        if not m:
            continue
        num = int(m.group(1))
        if num in seen:
            continue
        seen.add(num)
        name = m.group(2).strip()
        entry = {"num": num, "name": name}
        for line in block.splitlines():
            if line.startswith("TITLE:"):
                entry["title"] = line[6:].strip()
            elif line.startswith("TYPE:"):
                typ = line[5:].strip()
                # "methods  |  ESTIMAND: SMD"
                if "|" in typ:
                    parts = [p.strip() for p in typ.split("|")]
                    entry["type"] = parts[0]
                    for p in parts[1:]:
                        if p.upper().startswith("ESTIMAND:"):
                            entry["estimand"] = p.split(":", 1)[1].strip()
                else:
                    entry["type"] = typ
            elif line.startswith("DATA:"):
                entry["data"] = line[5:].strip()
            elif line.startswith("PATH:"):
                entry["path"] = line[5:].strip()

        # CURRENT BODY (first one wins — earlier lesson on duplicate entries)
        body_m = re.search(
            r"CURRENT BODY[^\n]*\n\n?(.+?)\n\n",
            block, re.DOTALL,
        )
        entry["body"] = body_m.group(1).strip() if body_m else ""

        # Links block
        code_m = re.search(r"Code:\s+(\S+)", block)
        protocol_m = re.search(r"Protocol:\s+(\S+)", block)
        pages_m = re.search(r"Dashboard:\s+(\S+)", block)
        entry["code_url"] = code_m.group(1) if code_m else ""
        entry["protocol_url"] = protocol_m.group(1) if protocol_m else ""
        entry["pages_url"] = pages_m.group(1) if pages_m else ""

        # Submission metadata parsing — needed for refs + target journal
        sub_m = re.search(r"SUBMISSION METADATA:\s*\n(.+)", block, re.DOTALL)
        sub_text = sub_m.group(1) if sub_m else ""
        ca_m = re.search(r"Corresponding author:\s*(.+)", sub_text)
        entry["corresponding_author"] = ca_m.group(1).strip() if ca_m else ""
        aff_m = re.search(r"Affiliation:\s*(.+)", sub_text)
        entry["affiliation"] = aff_m.group(1).strip() if aff_m else ""
        tj_m = re.search(r"Target journal:\s*(.+)", sub_text)
        entry["target_journal"] = tj_m.group(1).strip() if tj_m else ""
        # Competing-interests block: multi-line, terminated by next 'Author' or 'AI' header
        ci_m = re.search(r"Competing interests:\s*(.+?)(?=\n\s*\n\S|\nAuthor contributions|\nAI disclosure|\Z)",
                         sub_text, re.DOTALL)
        entry["competing_interests"] = re.sub(r"\s+", " ", ci_m.group(1)).strip() if ci_m else ""
        refs = []
        ref_match = re.search(r"References\s*\([^)]*\):\s*\n((?:\s*\d+\.\s.+\n?)+)", sub_text)
        if ref_match:
            for rm in re.finditer(r"^\s*\d+\.\s*(.+)$", ref_match.group(1), re.MULTILINE):
                refs.append(rm.group(1).strip())
        entry["references"] = refs

        out.append(entry)
    return out


PAGE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>[#{num}] {title_esc} — E156</title>
<meta name="description" content="E156 paper #{num}: {title_esc}. Target journal: Synthēsis. Open to student co-authorship.">
<style>
:root {{
  --bg:#0b1120; --bg-elev:#111827; --bg-card:#1a2236; --border:#2a3244;
  --text:#e5e7eb; --text-dim:#9ca3af; --text-faint:#6b7280;
  --accent:#22c55e; --claimed:#3b82f6; --warn:#eab308;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,monospace;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
}}
*{{box-sizing:border-box}}
html,body{{margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:var(--sans);font-size:15px;line-height:1.6}}
a{{color:var(--accent);text-decoration:none}}
a:hover{{text-decoration:underline}}
code,.mono{{font-family:var(--mono)}}
.container{{max-width:840px;margin:0 auto;padding:0 1.5rem}}
header{{padding:2.5rem 0 1.5rem;border-bottom:1px solid var(--border)}}
header .breadcrumb{{color:var(--text-faint);font-size:0.85rem;font-family:var(--mono);margin-bottom:0.6rem}}
header .breadcrumb a{{color:var(--text-dim)}}
header h1{{margin:0.2rem 0 0.6rem;font-size:clamp(1.4rem,3.5vw,2rem);font-weight:700;letter-spacing:-0.01em}}
header .num{{color:var(--accent);font-family:var(--mono);font-size:0.85em;margin-right:0.4rem}}
.badges{{display:flex;gap:0.4rem;flex-wrap:wrap;margin-top:0.5rem}}
.badge{{background:var(--bg-card);border:1px solid var(--border);padding:0.2em 0.65em;border-radius:4px;font-size:0.78rem;color:var(--text-dim)}}
.badge.topic{{color:var(--accent);border-color:rgba(34,197,94,0.3)}}
section{{padding:1.5rem 0;border-bottom:1px solid var(--border)}}
section:last-of-type{{border-bottom:0}}
section h2{{margin:0 0 0.6rem;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.06em;color:var(--accent);font-weight:600}}
.body-text{{font-size:1rem;line-height:1.7;color:var(--text);background:var(--bg-card);padding:1.2rem 1.4rem;border-left:3px solid var(--accent);border-radius:6px}}
.meta-grid{{display:grid;grid-template-columns:max-content 1fr;gap:0.3rem 1rem;font-size:0.9rem;align-items:baseline}}
.meta-grid dt{{color:var(--text-dim);font-family:var(--mono);font-size:0.8rem;white-space:nowrap}}
.meta-grid dd{{margin:0;color:var(--text)}}
.refs ol{{margin:0;padding-left:1.4rem}}
.refs li{{margin-bottom:0.4rem;font-size:0.88rem;color:var(--text)}}
.action-bar{{display:flex;gap:0.6rem;flex-wrap:wrap;padding:1.2rem 0}}
.btn{{padding:0.55rem 1rem;border-radius:5px;font-size:0.9rem;font-weight:500;border:1px solid var(--border);background:var(--bg-elev);color:var(--text);text-decoration:none;display:inline-flex;align-items:center;gap:0.35rem}}
.btn:hover{{background:var(--border);text-decoration:none}}
.btn.primary{{background:var(--accent);color:#052e16;border-color:var(--accent);font-weight:600}}
.btn.primary:hover{{background:#16a34a}}
footer{{padding:1.5rem 0 3rem;color:var(--text-dim);font-size:0.82rem;text-align:center;border-top:1px solid var(--border);margin-top:1rem}}
footer a{{color:var(--text-dim);text-decoration:underline}}
</style>
</head>
<body>
<div class="container">

<header>
  <div class="breadcrumb"><a href="../students.html">← E156 Student Board</a></div>
  <h1><span class="num">#{num}</span>{title_esc}</h1>
  <div class="badges">{badges}</div>
</header>

{body_section}

<section>
  <h2>At a glance</h2>
  <dl class="meta-grid">{meta_rows}</dl>
</section>

{refs_section}

{coi_section}

<div class="action-bar">
  <a class="btn primary" href="{claim_url}" target="_blank" rel="noopener">▶ Claim this paper</a>
  {code_btn}
  {protocol_btn}
  <a class="btn" href="../students.html">All papers</a>
</div>

<footer>
  Auto-generated by <code>scripts/build_paper_pages.py</code> from
  <code>rewrite-workbook.txt</code>. Target journal:
  <a href="https://www.synthesis-medicine.org/" target="_blank">Synthēsis</a>
  (Methods Note, ≤400 words).
  First author: the student who claims this paper. Middle author: Mahmood Ahmad.
  Senior author: the student's faculty supervisor.
</footer>
</div>
</body>
</html>
"""


def render_page(entry: dict) -> str:
    num = entry["num"]
    title = entry.get("title") or entry.get("name", "")
    claim_url = (
        f"{GH_ISSUE_BASE}?template=claim.yml"
        f"&title={esc('[CLAIM #' + str(num) + '] ' + title[:80])}"
        f"&paper_number={num}"
        f"&paper_title={esc(title)}"
    )
    badges_list: list[str] = []
    if entry.get("type"):
        badges_list.append(f'<span class="badge topic">{esc(entry["type"])}</span>')
    if entry.get("estimand"):
        badges_list.append(f'<span class="badge">estimand: {esc(entry["estimand"])}</span>')
    badges = "".join(badges_list)

    # 156-word body
    body_section = ""
    if entry.get("body"):
        body_section = (
            f'<section><h2>156-word body (current version)</h2>'
            f'<div class="body-text">{esc(entry["body"])}</div>'
            f'<p style="font-size:0.82rem;color:var(--text-faint);margin-top:0.8rem;">'
            f'Your rewrite should preserve all numbers, CIs, and percentages exactly '
            f'— rephrase the surrounding prose in 7 sentences, ≤156 words.'
            f'</p></section>'
        )

    # At-a-glance rows
    rows = []
    if entry.get("data"):
        rows.append(("Dataset", esc(entry["data"])))
    if entry.get("corresponding_author"):
        ca_line = esc(entry["corresponding_author"])
        if entry.get("affiliation"):
            ca_line += "<br><span style='color:var(--text-dim)'>" + esc(entry["affiliation"]) + "</span>"
        rows.append(("Mahmood (middle author)", ca_line))
    if entry.get("target_journal"):
        rows.append(("Target journal", esc(entry["target_journal"])))
    meta_rows = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)

    # References
    refs_section = ""
    if entry.get("references"):
        refs_html = "".join(
            f"<li>{esc(ref)}</li>" for ref in entry["references"]
        )
        refs_section = f'<section class="refs"><h2>References</h2><ol>{refs_html}</ol></section>'

    # Competing interests (P0-5): render the editorial-board COI on the public
    # landing page. Required because Mahmood serves on the Synthēsis editorial
    # board; public disclosure at the canonical per-paper URL is part of the
    # feedback_e156_authorship.md contract.
    coi_section = ""
    if entry.get("competing_interests"):
        coi_section = (
            '<section><h2>Competing interests</h2>'
            f'<p style="margin:0;color:var(--text);font-size:0.9rem;line-height:1.6;">'
            f'{esc(entry["competing_interests"])}</p></section>'
        )

    # Button HTML
    code_btn = (f'<a class="btn" href="{esc(entry["code_url"])}" target="_blank" rel="noopener">'
                f'Source code ↗</a>') if entry.get("code_url") else ""
    protocol_btn = (f'<a class="btn" href="{esc(entry["protocol_url"])}" target="_blank" rel="noopener">'
                    f'E156 protocol ↗</a>') if entry.get("protocol_url") else ""

    return PAGE_TEMPLATE.format(
        num=num,
        title_esc=esc(title),
        badges=badges,
        body_section=body_section,
        meta_rows=meta_rows,
        refs_section=refs_section,
        coi_section=coi_section,
        claim_url=claim_url,
        code_btn=code_btn,
        protocol_btn=protocol_btn,
    )


def render_index(entries: list[dict]) -> str:
    items = []
    for e in sorted(entries, key=lambda x: x["num"]):
        items.append(
            f'<li><a href="{e["num"]}.html"><code>[#{e["num"]}]</code> '
            f'{esc(e.get("title") or e.get("name", ""))}</a></li>'
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>E156 paper index</title>
<style>
body{{font-family:system-ui,sans-serif;background:#0b1120;color:#e5e7eb;max-width:920px;margin:0 auto;padding:2rem 1.5rem}}
a{{color:#22c55e;text-decoration:none}} a:hover{{text-decoration:underline}}
h1{{margin-top:0}}
code{{font-family:ui-monospace,monospace;color:#9ca3af;font-size:0.85em}}
ul{{list-style:none;padding:0;column-count:2;column-gap:2rem}}
@media(max-width:640px){{ul{{column-count:1}}}}
li{{break-inside:avoid;margin-bottom:0.4rem}}
</style></head><body>
<h1>E156 paper pages — {len(entries)} entries</h1>
<p><a href="../students.html">← back to student board</a></p>
<ul>
{"".join(items)}
</ul></body></html>
"""


def main() -> int:
    OUT_DIR.mkdir(exist_ok=True)

    entries = parse_entries()
    # P1-18 — mirror build_students_page.py's existence check; a fresh
    # clone without audit_output/ would otherwise crash here.
    hide = set()
    if HIDE_LIST.is_file():
        hide = set(json.loads(HIDE_LIST.read_text(encoding="utf-8")))
    visible = [e for e in entries if e["num"] not in hide]
    # P0-4 — fail-closed floor
    if len(visible) < 400:
        raise SystemExit(
            f"ERROR: only {len(visible)} visible entries — expected ≥ 400. "
            f"Check workbook integrity / hide_repo_404.json."
        )
    print(f"Rendering {len(visible)} per-paper pages to {OUT_DIR}")

    for e in visible:
        path = OUT_DIR / f"{e['num']}.html"
        path.write_text(render_page(e), encoding="utf-8")

    (OUT_DIR / "index.html").write_text(render_index(visible), encoding="utf-8")
    print(f"Wrote {len(visible)} paper pages + index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
