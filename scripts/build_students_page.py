"""Build the student claim page for https://mahmood726-cyber.github.io/e156/students.html

Parses rewrite-workbook.txt, extracts all 483 entries + their SUBMISSION
METADATA, and emits a single-file HTML with embedded JSON data. Students
browse, filter, and click "Claim" which opens a pre-filled mailto: email.

Claim tracking: reads claims.json from the same directory at page load.
The user (mahmood) updates claims.json manually after receiving claim
emails. The page shows the current claim state live.

Outputs:
  - students.html        (single-file, no external deps)
  - claims.json          (initialized empty if missing)

Single file, dark-mode, system fonts, WCAG-AA contrast. No CDN.
"""
from __future__ import annotations
import html as htmlmod
import json
import re
from pathlib import Path


E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
OUT_HTML = E156 / "students.html"
CLAIMS_JSON = E156 / "claims.json"
SEP = "=" * 70

AUTHOR_EMAIL = "mahmood.ahmad2@nhs.net"
TARGET_JOURNAL = "Synthēsis"  # must match masthead exactly per feedback_e156_authorship.md
CLAIM_WINDOW_DAYS = 30  # base window; students may request a 10-day auto-extension
EXTENSION_DAYS = 10     # added to window if claim carries `"extended": true`
GH_REPO = "mahmood726-cyber/e156"
GH_ISSUE_BASE = f"https://github.com/{GH_REPO}/issues/new"

ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)
LOCAL_PATH_RE = re.compile(r"\b[A-Za-z]:\\[^\s<>'\"),;]+")


def parse_entries(text: str) -> list[dict]:
    blocks = text.split(SEP)
    out: list[dict] = []
    seen: set[int] = set()
    for block in blocks:
        m = ENTRY_HEAD_RE.search(block)
        if not m:
            continue
        num = int(m.group(1))
        if num in seen:
            # P1-19 — workbook has occasional duplicate [N/T] headers.
            # Keep the first occurrence and LOG the collision so future edits
            # surface it immediately; silent drop is load-bearing but should
            # never be invisible.
            name = m.group(2).strip() if m.lastindex and m.lastindex >= 2 else "?"
            print(f"[WARN] duplicate paper_num {num} — dropping second block titled {name!r}")
            continue
        seen.add(num)
        name = m.group(2)
        data = {"num": num, "name": name}
        lines = block.splitlines()
        for j, line in enumerate(lines):
            if line.startswith("TITLE:"):
                data["title"] = line[6:].strip()
            elif line.startswith("TYPE:"):
                data["type"] = line[5:].strip()
            elif line.startswith("DATA:"):
                data["data"] = line[5:].strip()
            elif line.startswith("PATH:"):
                data["path"] = line[5:].strip()
            elif line.startswith("CURRENT BODY") and "body" not in data:
                # Only extract the FIRST CURRENT BODY per entry. A handful
                # of workbook entries (371, 468) have stray "=== NEW
                # PROJECT: xxx ===" + second CURRENT BODY lines appended
                # from an old merge; the `"body" not in data` guard keeps
                # the legitimate first body from being overwritten.
                body_lines: list[str] = []
                k = j + 1
                while k < len(lines) and not lines[k].strip():
                    k += 1
                while (k < len(lines) and lines[k].strip()
                       and not lines[k].startswith("YOUR REWRITE")
                       and not lines[k].startswith("=== NEW PROJECT")):
                    body_lines.append(lines[k])
                    k += 1
                data["body"] = " ".join(body_lines).strip()
        # Links block — all three URLs. Require line-start (with optional
        # leading whitespace) AND http(s):// prefix so that e.g. a title
        # containing "Code:" (like #49 "Everything Claude Code: Modular...")
        # doesn't capture the next word as the URL.
        code_m = re.search(r"^\s+Code:\s+(https?://\S+)", block, re.MULTILINE)
        protocol_m = re.search(r"^\s+Protocol:\s+(https?://\S+)", block, re.MULTILINE)
        pages_m = re.search(r"^\s+Dashboard:\s+(https?://\S+)", block, re.MULTILINE)
        data["code_url"] = code_m.group(1) if code_m else ""
        data["protocol_url"] = protocol_m.group(1) if protocol_m else ""
        data["pages_url"] = pages_m.group(1) if pages_m else ""

        # Topic pack label is extracted below after the refs block
        # using a version that handles nested parens. Default to
        # "unknown" if the refs block is missing entirely.
        data["topic"] = "unknown"

        # Full references list — capture the numbered entries after
        # "References (topic pack: ...):" up to the next blank-line
        # boundary. The topic-pack label can contain nested parens
        # (e.g. "trial sequential analysis (TSA)" or "individual
        # participant data (IPD) meta-analysis"), so we match non-greedy
        # up to `):` rather than using a character-class negation that
        # stops at the first `)`.
        ref_block_m = re.search(
            r"References \(topic pack:.+?\):\s*\n((?:\s*\d+\..+(?:\n|$))+)",
            block,
        )
        refs: list[str] = []
        if ref_block_m:
            for ln in ref_block_m.group(1).splitlines():
                s = ln.strip()
                if re.match(r"^\d+\.\s", s):
                    refs.append(s)
        data["references"] = refs

        # Same fix for the topic label extraction (used to label the
        # card's topic chip).
        pack_m = re.search(r"References \(topic pack:\s*(.+?)\):", block)
        if pack_m:
            data["topic"] = pack_m.group(1).strip()

        # Target journal + section line.
        journal_m = re.search(
            r"Target journal:\s*([^\n]+?)\s*\n\s*Section:\s*([^\n—(]+?)(?:\s*[—(]|\s*\n)",
            block,
        )
        data["target_journal"] = journal_m.group(1).strip() if journal_m else ""
        data["section"] = journal_m.group(2).strip() if journal_m else ""

        # Standard statement blocks — each is a paragraph after its
        # label and before the next blank line / next label.
        def _grab(label: str) -> str:
            m = re.search(
                rf"{re.escape(label)}\s*(.+?)(?:\n\s*\n|\nCorresponding author:|\nORCID:|\nAffiliation:|\nLinks:|\nReferences|\nData availability:|\nEthics:|\nFunding:|\nCompeting interests:|\nAuthor contributions|\nAI disclosure:|\nPreprint:|\nReporting checklist:|\nTarget journal:|\nManuscript license:|\nCode license:|\nSUBMITTED:)",
                block,
                re.DOTALL,
            )
            if not m:
                return ""
            # Collapse inline wrapping: join the lines of this paragraph
            # into a single string while preserving the bullet structure.
            return " ".join(ln.strip() for ln in m.group(1).splitlines() if ln.strip())

        data["data_availability"] = _grab("Data availability:")
        data["ethics"] = _grab("Ethics:")
        data["funding"] = _grab("Funding:")
        data["competing_interests"] = _grab("Competing interests:")
        data["ai_disclosure"] = _grab("AI disclosure:")
        data["reporting_checklist"] = _grab("Reporting checklist:")
        data["credit"] = _grab("Author contributions (CRediT):")
        data["preprint"] = _grab("Preprint:")

        # Corresponding-author block + ORCID + affiliation.
        corresp_m = re.search(r"Corresponding author:\s*([^\n]+)", block)
        orcid_m = re.search(r"ORCID:\s*([\d\-]+)", block)
        affil_m = re.search(r"Affiliation:\s*([^\n]+)", block)
        data["corresponding_author"] = corresp_m.group(1).strip() if corresp_m else ""
        data["orcid"] = orcid_m.group(1).strip() if orcid_m else ""
        data["affiliation"] = affil_m.group(1).strip() if affil_m else ""

        # Submitted status (the per-entry marker)
        sub_m = re.search(r"^SUBMITTED:\s*\[(\s|x|X)\]", block, re.MULTILINE)
        data["submitted_head"] = bool(sub_m and sub_m.group(1).lower() == "x")

        out.append(data)
    return out


def normalize_credit(text: str) -> str:
    """Adapt legacy workbook CRediT placeholders to current optional-mentor policy."""
    if not text:
        return ""
    text = re.sub(
        r"\[SUPERVISING FACULTY,\s*last/senior author\]\s*[—-]\s*"
        r"Supervision,\s*Validation,\s*Writing\s*[–-]\s*review\s*&\s*editing\.?",
        "[OPTIONAL MENTOR/CO-AUTHOR, if included] — Supervision, Validation, Writing – review & editing.",
        text,
    )
    text = text.replace(
        "Mahmood Ahmad (middle author, NOT first or last)",
        "Mahmood Ahmad (non-corresponding co-author)",
    )
    return text


def sanitize_public_text(text: str) -> str:
    """Remove workstation-local paths before embedding workbook prose in public HTML."""
    if not text:
        return ""
    return LOCAL_PATH_RE.sub("[local path redacted]", text)


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>E156 Student Board — Claim, rewrite, submit to Synthēsis</title>
<meta name="description" content="__N_VISIBLE__ E156 micro-papers open to student co-authorship. Target journal: Synthēsis. Claim via GitHub Issues; one paper at a time; 30-day window, +10-day extension available; then claim expires.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='3' fill='%230b1120'/%3E%3Ctext x='8' y='12' font-family='ui-monospace,monospace' font-size='10' font-weight='700' text-anchor='middle' fill='%2322c55e'%3EE%3C/text%3E%3C/svg%3E">

<style>
:root {
  --bg: #ffffff;
  --bg-elev: #f6f6f2;
  --bg-card: #ffffff;
  --border: #e4e4df;
  --text: #141414;
  --text-dim: #5c5c5c;
  --text-faint: #8c8c8c;
  --accent: #15803d;
  --warn: #b45309;
  --claimed: #1d4ed8;
  --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  --sans: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --serif: Georgia, "Times New Roman", serif;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: var(--sans); font-size: 15px; line-height: 1.55; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
code { font-family: var(--mono); font-size: 0.88em; background: var(--bg-elev); padding: 0.1em 0.35em; border-radius: 3px; }

.container { max-width: 1100px; margin: 0 auto; padding: 0 1.5rem; }

header { padding: 3rem 0 2rem; border-bottom: 1px solid var(--border); background:
  radial-gradient(ellipse at 20% 0%, rgba(34, 197, 94, 0.08), transparent 60%),
  var(--bg); }
header h1 { font-size: clamp(1.75rem, 4vw, 2.5rem); font-weight: 700; margin: 0 0 0.5rem; letter-spacing: -0.01em; }
header h1 .accent { color: var(--accent); }
header h1 .journal-mark { color: var(--text-dim); font-size: 0.55em; font-weight: 500; margin-left: 0.6rem; vertical-align: middle; letter-spacing: 0.02em; white-space: nowrap; }
header p.tagline { font-size: 1.05rem; color: var(--text-dim); margin: 0 0 1.5rem; max-width: 720px; }

.instructions {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  padding: 1.25rem 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}
.instructions h2 { margin: 0 0 0.75rem; font-size: 1rem; letter-spacing: 0.03em; text-transform: uppercase; color: var(--accent); }
.instructions ol { margin: 0; padding-left: 1.25rem; }
.instructions ol li { margin-bottom: 0.4rem; color: var(--text); }
.instructions .mono { font-family: var(--mono); font-size: 0.9em; }

.stats { display: flex; gap: 1.5rem; flex-wrap: wrap; margin-top: 1rem; }
.stat { background: var(--bg-elev); border: 1px solid var(--border); border-radius: 6px; padding: 0.6rem 1rem; }
.stat .n { font-family: var(--mono); font-size: 1.3rem; font-weight: 700; color: var(--accent); }
.stat .n.w { color: var(--warn); }
.stat .n.b { color: var(--claimed); }
.stat .l { font-size: 0.72rem; color: var(--text-dim); text-transform: uppercase; letter-spacing: 0.05em; margin-left: 0.4rem; }

.toolbar {
  position: sticky; top: 0; z-index: 10;
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  padding: 0.8rem 0;
}
.toolbar-row { display: flex; gap: 0.6rem; flex-wrap: wrap; align-items: center; }
.toolbar input, .toolbar select {
  background: var(--bg-card);
  color: var(--text);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.55rem 0.8rem;
  font-family: inherit;
  font-size: 0.95rem;
  outline: none;
}
.toolbar input:focus, .toolbar select:focus { border-color: var(--accent); }
/* P1-8 — visible focus ring for keyboard users (replaces the `outline:none`). */
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 4px; }
.toolbar input[type="search"] { flex: 1 1 240px; min-width: 180px; }
.toolbar select { min-width: 140px; }
.toolbar .count-chip { color: var(--text-dim); font-family: var(--mono); font-size: 0.88rem; margin-left: auto; }
.toolbar #clear-filters {
  background: var(--bg-card); color: var(--text-dim); border: 1px solid var(--border);
  border-radius: 6px; padding: 0.45rem 0.7rem; font-family: inherit; font-size: 0.85rem;
  cursor: pointer; transition: color 0.15s, border-color 0.15s;
}
.toolbar #clear-filters:hover { color: var(--text); border-color: var(--text-faint); }
.toolbar #clear-filters[hidden] { display: none; }

dialog#kbd-help {
  background: var(--bg-card); color: var(--text); border: 1px solid var(--border);
  border-radius: 8px; padding: 1.5rem 2rem; max-width: 480px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}
dialog#kbd-help::backdrop { background: rgba(11, 17, 32, 0.7); }
dialog#kbd-help h2 { margin: 0 0 1rem; font-size: 1.1rem; color: var(--accent); }
dialog#kbd-help dl { display: grid; grid-template-columns: auto 1fr; gap: 0.5rem 1.5rem; margin: 0; }
dialog#kbd-help dt { font-family: var(--mono); background: var(--bg-elev); padding: 0.15em 0.5em; border-radius: 4px; font-size: 0.85em; }
dialog#kbd-help dd { margin: 0; align-self: center; color: var(--text-dim); }
dialog#kbd-help button { margin-top: 1.2rem; background: var(--bg-elev); color: var(--text); border: 1px solid var(--border); border-radius: 6px; padding: 0.5rem 1rem; cursor: pointer; }

.empty-state { color: var(--text-dim); text-align: center; padding: 3rem 0; }
.empty-state .actions { margin-top: 1rem; display: flex; gap: 0.5rem; justify-content: center; flex-wrap: wrap; }
.empty-state .actions button {
  background: var(--bg-card); color: var(--text); border: 1px solid var(--border);
  border-radius: 6px; padding: 0.45rem 0.9rem; font-family: inherit; font-size: 0.88rem; cursor: pointer;
}
.empty-state .actions button:hover { border-color: var(--accent); color: var(--accent); }

.grid { display: flex; flex-direction: column; gap: 0.9rem; padding: 1.5rem 0 4rem; }

.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.1rem 1.35rem;
  transition: border-color 0.15s;
}
.card.claimed { border-left: 3px solid var(--claimed); }
.card.submitted { border-left: 3px solid var(--accent); opacity: 0.8; }
.card:hover { border-color: var(--text-faint); }

.card-head { display: flex; gap: 0.75rem; align-items: flex-start; flex-wrap: wrap; margin-bottom: 0.5rem; }
.card-num { font-family: var(--mono); font-size: 0.85rem; color: var(--text-faint); white-space: nowrap; }
.card-title { font-size: 1.05rem; font-weight: 600; color: var(--text); flex: 1 1 300px; }
.card-badge {
  padding: 0.15em 0.5em; border-radius: 3px; font-size: 0.7rem; font-family: var(--mono);
  font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;
}
.card-badge.open { background: rgba(34, 197, 94, 0.15); color: var(--accent); }
.card-badge.claimed { background: rgba(59, 130, 246, 0.15); color: var(--claimed); }
.card-badge.submitted { background: rgba(234, 179, 8, 0.15); color: var(--warn); }

.card-meta { font-size: 0.85rem; color: var(--text-dim); margin-bottom: 0.4rem; }
.card-meta span { margin-right: 1rem; }
.card-meta .topic { color: var(--accent); }

.card-body { font-size: 0.92rem; color: var(--text); margin: 0.5rem 0 0.8rem; line-height: 1.55; max-height: 6em; overflow: hidden; position: relative; transition: max-height 0.3s; }
.card-body.expanded { max-height: 200em; }
.card-body::after {
  content: ""; position: absolute; bottom: 0; left: 0; right: 0; height: 2em;
  background: linear-gradient(transparent, var(--bg-card));
  pointer-events: none;
}
.card-body.expanded::after { display: none; }

.card-actions { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; margin-top: 0.6rem; }
.btn {
  font-family: inherit;
  /* P1-9 — 44x44 touch target (WCAG 2.5.5). */
  padding: 0.6rem 1rem;
  min-height: 44px;
  border-radius: 5px;
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid var(--border);
  background: var(--bg-elev);
  color: var(--text);
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
}
.btn[aria-disabled="true"], .btn.greyed { opacity: 0.4; cursor: not-allowed; pointer-events: none; }
.btn:hover { background: var(--border); text-decoration: none; }
.btn.primary { background: var(--accent); color: #052e16; border-color: var(--accent); font-weight: 600; }
.btn.primary:hover { background: #16a34a; }
.btn.ghost { background: transparent; }
.btn[disabled] { opacity: 0.5; cursor: not-allowed; }

.claimed-by {
  margin-top: 0.5rem;
  padding: 0.4rem 0.7rem;
  background: rgba(59, 130, 246, 0.08);
  border: 1px dashed var(--claimed);
  border-radius: 4px;
  font-size: 0.82rem;
  color: var(--text);
}
.claimed-by strong { color: var(--claimed); }
.days-left { font-family: var(--mono); }
.days-left.ok { color: var(--accent); }
.days-left.warn { color: var(--warn); }
.days-left.urgent { color: #f87171; font-weight: 600; }
.days-left.expired { color: #ef4444; font-weight: 700; text-transform: uppercase; }
.ext-badge { font-family: var(--mono); font-size: 0.75em; background: rgba(59, 130, 246, 0.2); color: var(--claimed); border: 1px solid rgba(59, 130, 246, 0.4); padding: 0.05em 0.4em; border-radius: 3px; margin-left: 0.3em; }
.series-badge { font-family: var(--mono); font-size: 0.75em; background: rgba(168, 85, 247, 0.18); color: #c4b5fd; border: 1px solid rgba(168, 85, 247, 0.4); padding: 0.1em 0.55em; border-radius: 3px; cursor: pointer; margin-left: 0.4em; }
.series-badge:hover { background: rgba(168, 85, 247, 0.3); }

.toggle-body { background: none; border: 0; color: var(--text-faint); font-family: var(--mono); font-size: 0.8rem; cursor: pointer; padding: 0.5rem 0.2rem; min-height: 36px; margin-top: 0.3rem; }
.toggle-body:hover { color: var(--accent); }
/* P1-10 — claims fetch-failure banner */
.claims-error { background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; color: #fecaca; padding: 0.7rem 1rem; border-radius: 6px; margin: 1rem 0; font-size: 0.9rem; }
.claims-error button { margin-left: 0.8rem; background: #ef4444; color: white; border: 0; padding: 0.35rem 0.8rem; border-radius: 4px; cursor: pointer; font-weight: 600; }
/* P1-13 — collapsible instructions details/summary */
.instructions-wrap { margin-bottom: 1.5rem; }
.instructions-wrap summary { cursor: pointer; color: var(--accent); font-weight: 600; padding: 0.6rem 0; font-size: 0.95rem; list-style: none; }
.instructions-wrap summary::-webkit-details-marker { display: none; }
.instructions-wrap summary::before { content: "▸ "; display: inline-block; transition: transform 0.15s; }
.instructions-wrap[open] summary::before { transform: rotate(90deg); }

footer { padding: 2rem 0; border-top: 1px solid var(--border); color: var(--text-dim); font-size: 0.85rem; text-align: center; }

/* === NYT-editorial light theme (overrides) === */
body { font-size: 16px; }
.container { max-width: 1080px; }
header { padding: 4.5rem 0 2.25rem; background: #fff; border-bottom: 1px solid var(--text); }
header h1 { font-family: var(--serif); font-weight: 700; letter-spacing: -0.015em; font-size: clamp(2rem,4.5vw,2.9rem); }
header h1 .accent { color: var(--accent); }
header h1 .journal-mark { font-family: var(--sans); color: var(--text-faint); }
header p.tagline { font-family: var(--serif); font-size: clamp(1.08rem,2vw,1.28rem); line-height: 1.52; color: #333; max-width: 66ch; }
h2, .card-title { font-family: var(--serif); }
.instructions h2 { font-family: var(--sans); color: var(--text-dim); }
.instructions-wrap summary { color: var(--accent); }
.card { border-radius: 4px; }
.card-title { font-weight: 700; font-size: 1.1rem; }
.card:hover { border-color: var(--text-faint); box-shadow: 0 1px 10px rgba(0,0,0,0.05); }
.btn.primary { color: #fff; }
.btn.primary:hover { background: #166534; }
.stat { background: var(--bg-elev); }
/* fix status colours that were light-on-dark (would vanish on white) */
.days-left.urgent { color: #dc2626; }
.days-left.expired { color: #b91c1c; }
.claims-error { color: #991b1b; }
.series-badge { color: #6d28d9; background: rgba(124,58,237,0.10); border-color: rgba(124,58,237,0.35); }
.series-badge:hover { background: rgba(124,58,237,0.18); }
dialog#kbd-help::backdrop { background: rgba(0,0,0,0.35); }
footer { color: var(--text-dim); border-top-color: var(--border); }
</style>
</head>
<body>

<header>
  <div class="container">
    <h1><span class="accent">E156</span> Student Board <span class="journal-mark" title="Target journal: Synthēsis (synthesis-medicine.org)">◆ Synthēsis</span></h1>
    <p class="tagline">Every paper on this board is a complete, machine-drafted meta-analysis &mdash; rigorous, but unwritten. Claim one, rewrite the 156-word body in your own voice and judgement, and submit it to <strong>◆ Synthēsis</strong> under your name. Real authorship, in a real journal &mdash; open to Ugandan medical students and anyone learning evidence synthesis. <span style="white-space:nowrap">&mdash; Mahmood Ahmad, Tahir Heart Institute.</span></p>

    <details class="instructions-wrap instructions" open>
      <summary>How this works (click to collapse)</summary>
      <h2>How this works</h2>
      <ol>
        <li><strong>You need a GitHub account</strong> (free, 2-minute signup at <a href="https://github.com/signup" target="_blank" rel="noopener">github.com/signup</a>). If you're a researcher you'll want one anyway.</li>
        <li>Browse the list. Search by topic (e.g. "heart failure", "network meta-analysis", "diagnostic").</li>
        <li>Click <strong>▶ Claim this paper</strong> on the card you want. A GitHub form opens pre-filled with the paper number — fill in your name, affiliation, email, and optional mentor/co-author details if you already have them, tick the agreements, click "Submit new issue". <strong>Within ~60 seconds this board updates automatically</strong> showing your name and a 30-day countdown (extendable to 40).</li>
        <li>Copy the <span class="mono">Current body</span> on your card. Rewrite it in your own words: 156 words, 7 sentences (Question · Dataset · Method · Result · Robustness · Interpretation · Boundary).</li>
        <li>Submit your rewrite to <strong>Synthēsis</strong> (<a href="https://www.synthesis-medicine.org/index.php/journal" target="_blank">synthesis-medicine.org</a>). The journal mints DOIs on acceptance; no Zenodo step needed.</li>
        <li>Once submitted, click <strong>✓ Confirm submission</strong> on your card. A second GitHub form opens — paste your submission ID / DOI, submit. Board updates to show SUBMITTED. You are listed as first author.</li>
        <li><strong>One paper at a time.</strong> You may hold AT MOST one active claim until you either submit or let it expire.</li>
        <li><strong>You have 30 days from claim to submission.</strong> Need more time? Click <strong>+10-day extension</strong> on your card and a GitHub form opens — just submit it. Auto-approved, gives you 40 days total. If you don't confirm submission within the window (30 days, or 40 if extended), your claim expires and the paper reopens for another student.</li>
      </ol>

      <h2>Authorship rules (read before claiming)</h2>
      <ul>
        <li><strong>You are first author AND corresponding author</strong> on the submission you claim. You fill in the corresponding-author fields (name, email, affiliation) on the OJS submission form yourself — Mahmood is not the contact for the journal.</li>
        <li><strong>A mentor/co-author is optional, not required.</strong> If you already have a supervisor, mentor, or co-investigator, include them. If you do not, leave that field blank and submit without one.</li>
        <li><strong>Mahmood Ahmad must not be first author or corresponding author.</strong> His role, where included, is Conceptualization, Methodology, Software, Data curation; not original drafting.</li>
        <li><strong>Competing interests:</strong> none declared. (Mahmood is not on the Synthēsis editorial board; there's no COI to disclose.)</li>
      </ul>

      <h2 id="how-to-submit">How to submit to ◆ Synthēsis (OJS, step-by-step)</h2>
      <p>Synthēsis runs on OJS (Open Journal Systems). The flow is the same for every paper.</p>

      <h3>Step 1 — Prepare the manuscript file</h3>
      <ul>
        <li>Microsoft Word <span class="mono">.docx</span>, A4 page, 1.5 line spacing, 2.5&nbsp;cm margins.</li>
        <li>Font: 11-pt <strong>Calibri</strong> OR 12-pt <strong>Times New Roman</strong> (consistent throughout).</li>
        <li>Order: Title · Authors + ORCIDs + affiliations · Body · References · Data availability · Ethics · Funding · Competing interests · CRediT · AI disclosure · Copyright line.</li>
        <li><strong>Body length:</strong> paste your 156-word, 7-sentence E156 rewrite verbatim — that <em>is</em> the submission. The journal caps main text at ≤400 words, but the E156 format deliberately targets 156 words; do <strong>NOT</strong> pad to 400. References, tables, figures, and captions don't count against the 400 ceiling anyway.</li>
        <li><strong>References:</strong> Vancouver / numeric, NLM journal abbreviations, DOI without URL prefix; up to 6 authors then "et al.". Two starter refs are already in your card's SUBMISSION METADATA — keep them, add more as needed.</li>
        <li><strong>Copy/paste these blocks unchanged from the SUBMISSION METADATA on your card:</strong> Data availability, Ethics, Funding, Competing interests ("None declared."), CRediT, AI disclosure. If the CRediT block mentions a supervising faculty author and you are submitting without one, remove that placeholder line.</li>
        <li><strong>Copyright line at the very bottom:</strong> <span class="mono">© The Author(s) 2026. CC BY 4.0.</span></li>
      </ul>

      <h3>Step 2 — Register / login</h3>
      <ul>
        <li>Register: <a href="https://www.synthesis-medicine.org/index.php/journal/user/register" target="_blank" rel="noopener">synthesis-medicine.org/.../register</a> — use your ORCID where possible, tick the <strong>Author</strong> role.</li>
        <li>Login: <a href="https://www.synthesis-medicine.org/index.php/journal/login" target="_blank" rel="noopener">synthesis-medicine.org/.../login</a></li>
      </ul>

      <h3>Step 3 — OJS 5-step submission wizard</h3>
      <ol>
        <li><strong>Start</strong> — Section: pick whatever section is listed on YOUR card's <span class="mono">Target journal: ◆ Synthēsis</span> block (one of <strong>Methods Note</strong>, <strong>Short Meta-Analysis</strong>, or <strong>Brief Update</strong>). The section is preassigned per paper — you don't need to reason about which one fits. Language: English. Tick all 5 submission-checklist items. Agree to CC-BY-4.0 copyright + privacy.</li>
        <li><strong>Upload File</strong> — upload your <span class="mono">.docx</span>. Component: <strong>"Article Text"</strong>.</li>
        <li><strong>Enter Metadata</strong> — paste the title; paste YOUR REWRITE (the 156-word body) verbatim as the abstract — the E156 7-sentence structure <em>is</em> the abstract, no shortening needed; add 4-6 keywords; <strong>add ALL contributors with ORCIDs and affiliations IN ORDER</strong>:
          <ul>
            <li>1st = <strong>YOU</strong> (first author + <strong>corresponding author</strong> — enter your email as the contact address)</li>
            <li><strong>Mahmood Ahmad</strong> · ORCID 0000-0001-9107-3704 · <a href="mailto:mahmood.ahmad2@nhs.net">mahmood.ahmad2@nhs.net</a> · Tahir Heart Institute, Rabwah, Pakistan. <em>Do NOT tick "corresponding author" on this row.</em></li>
            <li>Optional: your mentor, supervisor, or co-investigator if you have one. This is not required.</li>
          </ul>
          Then paste the Vancouver references.</li>
        <li><strong>Confirmation</strong> — review and click <strong>"Finish Submission"</strong>.</li>
        <li><strong>Next Steps</strong> — note the submission ID shown on screen. You'll need it for the next step.</li>
      </ol>

      <h3>Step 4 — Confirm on this board</h3>
      <ul>
        <li>Come back to this page, find your card, click <strong>✓ Confirm submission</strong>, and paste your OJS submission ID (or DOI once minted). Your card flips to SUBMITTED. The countdown stops.</li>
      </ul>

      <p style="font-size:0.85rem; color:var(--text-dim); margin-top:1rem;">
        <strong>Fallback:</strong> if the OJS site is down, try again after a few hours — do NOT email a .docx to a personal address. The canonical submission channel is the Synthēsis OJS submission wizard. Still confirm here once you complete the submission so the board updates.
      </p>
    </details>

    <div class="stats">
      <div class="stat"><span class="n" id="stat-total">0</span><span class="l">total papers</span></div>
      <div class="stat"><span class="n" id="stat-open">0</span><span class="l">open to claim</span></div>
      <div class="stat"><span class="n b" id="stat-claimed">0</span><span class="l">claimed</span></div>
      <div class="stat"><span class="n w" id="stat-submitted">0</span><span class="l">already submitted</span></div>
    </div>
  </div>
</header>

<div class="toolbar">
  <div class="container">
    <div class="toolbar-row">
      <input type="search" id="search" aria-label="Search papers by title, body, data, or topic" placeholder='Search e.g. "heart failure" or "diagnostic"'>
      <select id="filter-kind" aria-label="Filter by paper kind">
        <option value="">All kinds</option>
        <option value="rapidmeta">RapidMeta (living MA engine)</option>
        <option value="living-ma">Living meta-analysis</option>
        <option value="methods">Methods / software</option>
        <option value="clinical">Clinical</option>
        <option value="other">Other</option>
      </select>
      <select id="filter-series" aria-label="Filter by shared code repository (series)"><option value="">All series</option></select>
      <select id="filter-topic" aria-label="Filter by topic"><option value="">All topics</option></select>
      <select id="filter-status" aria-label="Filter by claim status">
        <option value="">All statuses</option>
        <option value="open">Open to claim</option>
        <option value="claimed">Claimed</option>
        <option value="submitted">Submitted</option>
      </select>
      <select id="sort-by" aria-label="Sort papers">
        <option value="num">Sort: Paper #</option>
        <option value="open-first">Sort: Open first</option>
        <option value="recent-claim">Sort: Recently claimed</option>
        <option value="az">Sort: A–Z by title</option>
        <option value="topic">Sort: By topic</option>
      </select>
      <button type="button" id="clear-filters" hidden aria-label="Clear all filters">Clear filters</button>
      <span class="count-chip" id="count-chip" role="status" aria-live="polite">showing 0 of 0</span>
    </div>
  </div>
</div>

<dialog id="kbd-help" aria-labelledby="kbd-help-title">
  <h2 id="kbd-help-title">Keyboard shortcuts</h2>
  <dl>
    <dt>/</dt><dd>focus the search box</dd>
    <dt>Esc</dt><dd>clear search if filled, otherwise close help</dd>
    <dt>?</dt><dd>toggle this help</dd>
    <dt>c</dt><dd>clear all filters</dd>
  </dl>
  <button type="button" autofocus onclick="this.closest('dialog').close()">Close</button>
</dialog>

<main class="container" id="main">
  <div id="claims-error" class="claims-error" hidden role="alert">
    <!-- P1-10 — shown if claims.json fetch fails so students don't claim
         papers that are actually already taken. -->
    Could not load live claim data. Cards may show "Open to claim" for
    papers that have already been claimed. Refresh to retry.
    <button type="button" onclick="location.reload()">Refresh</button>
  </div>
  <div class="grid" id="grid"></div>
</main>

<footer>
  <div class="container">
    <p>Live workbook · Updates when I merge your rewrite · Questions → <a href="mailto:__AUTHOR_EMAIL__">__AUTHOR_EMAIL__</a></p>
  </div>
</footer>

<script>
const AUTHOR_EMAIL = "__AUTHOR_EMAIL__";
const TARGET_JOURNAL = "__TARGET_JOURNAL__";
const CLAIM_WINDOW_DAYS = __CLAIM_WINDOW__;
const EXTENSION_DAYS = __EXTENSION_DAYS__;
const MS_PER_DAY = 86400000;
const ENTRIES = __ENTRIES_JSON__;

let claims = {};  // populated from claims.json
let claimsLoaded = false;  // P1-10 — false if fetch failed
let currentUser = null;    // P1-12 — set by URL `?user=` hint or localStorage
// Filter + sort state. B2 (2026-05-24): restored from / mirrored to URL
// search params so a filtered view is shareable.
let filterText = "";
let filterTopic = "";
let filterStatus = "";
let filterKind = "";
let filterSeries = "";
let sortBy = "num";  // num | open-first | recent-claim | az | topic

function readFilterStateFromUrl() {
  try {
    const p = new URLSearchParams(location.search);
    filterText   = p.get("q")      || "";
    filterKind   = p.get("kind")   || "";
    filterSeries = p.get("series") || "";
    filterTopic  = p.get("topic")  || "";
    filterStatus = p.get("status") || "";
    sortBy       = p.get("sort")   || "num";
  } catch (_) { /* malformed URL — ignore */ }
}

function writeFilterStateToUrl() {
  try {
    const p = new URLSearchParams();
    if (filterText)   p.set("q",      filterText);
    if (filterKind)   p.set("kind",   filterKind);
    if (filterSeries) p.set("series", filterSeries);
    if (filterTopic)  p.set("topic",  filterTopic);
    if (filterStatus) p.set("status", filterStatus);
    if (sortBy !== "num") p.set("sort", sortBy);
    // Preserve ?focus= so deep-links keep working alongside filter state
    const focus = new URLSearchParams(location.search).get("focus");
    if (focus) p.set("focus", focus);
    const qs = p.toString();
    const target = qs ? `?${qs}` : location.pathname;
    history.replaceState(null, "", target);
  } catch (_) { /* history API unsupported — ignore */ }
}

function hasAnyFilter() {
  return !!(filterText || filterKind || filterSeries || filterTopic || filterStatus || sortBy !== "num");
}

// Coarse kind-classification. Order:
//   1. RapidMeta — papers backed by the rapidmeta-finerenone multi-therapy
//      engine get their own bucket (currently ~58 papers). Promoted out
//      of "Living meta-analysis" so the two categories are exclusive on
//      the Kind dropdown.
//   2. Living meta-analysis — any paper with an MA-ish TYPE or title.
//      Catches methods-about-MA (Bayesian-MA, DTA-MA, IPD-MA, etc.).
//   3. Methods — software / methodological / tool papers that aren't MA.
//   4. Clinical / other — fallbacks.
function kindOf(entry) {
  if (entry.code_url && entry.code_url.includes("rapidmeta-finerenone")) return "rapidmeta";
  const typ = (entry.type || "").toLowerCase().split("|")[0].trim();
  const title = (entry.title || "").toLowerCase();
  const fullType = (entry.type || "").toLowerCase();
  const isMA = (
    typ.includes("living-ma") || typ.includes("meta-analysis") ||
    typ.includes("pairwise") || typ.includes("network") ||
    typ.startsWith("meta-") || typ.startsWith("meta ") || typ === "meta" ||
    title.includes("meta-analysis") || title.includes("meta analysis") ||
    title.includes("living meta") || title.includes("network meta") ||
    fullType.includes("ma ") || fullType.includes("nma ")
  );
  if (isMA) return "living-ma";
  if (typ.includes("methods") || typ.includes("methodological") || typ.includes("tool")) return "methods";
  if (typ.includes("clinical")) return "clinical";
  return "other";
}

// Series = shared code_url, shown as a badge + a filter dropdown. Useful
// for clusters like rapidmeta-finerenone (17 papers share one repo).
const SERIES_INDEX = (() => {
  const counts = {};
  ENTRIES.forEach(e => {
    if (!e.code_url) return;
    counts[e.code_url] = (counts[e.code_url] || 0) + 1;
  });
  return counts;
})();
function seriesOf(entry) {
  if (!entry.code_url) return "";
  return (SERIES_INDEX[entry.code_url] || 0) >= 2 ? entry.code_url : "";
}
function seriesLabel(url) {
  try { return new URL(url).pathname.replace(/^\/[^/]+\//, ""); }
  catch (_) { return url; }
}

function windowDaysFor(claim) {
  // 10-day auto-extension adds to the base window iff claim has the flag.
  return CLAIM_WINDOW_DAYS + (claim && claim.extended ? EXTENSION_DAYS : 0);
}

function daysLeft(claim) {
  // claim is the claims.json record. Returns integer days remaining (may be negative).
  // P1-1 / P1-3 — use date-only difference (ignore sub-day UTC/local phase).
  // P1-2 — NaN guard on malformed claim_date.
  if (!claim || !claim.claim_date) return null;
  const claimMs = Date.parse(claim.claim_date + "T00:00:00Z");
  if (isNaN(claimMs)) return null;
  const now = new Date();
  const todayUtcMs = Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
  const age = Math.floor((todayUtcMs - claimMs) / MS_PER_DAY);
  // Align with Python expire_stale_claims: expired iff age > window.
  // Returns days remaining. 0 means "expires today at midnight UTC"; < 0 is expired.
  return windowDaysFor(claim) - age;
}

function statusOf(entry) {
  if (entry.submitted_head) return "submitted";
  const c = claims[entry.num];
  if (!c) return "open";
  if (c.status === "submitted") return "submitted";
  // Expired iff days-remaining < 0.
  const left = daysLeft(c);
  if (left !== null && left < 0) return "open";
  return "claimed";
}

// P1-12 — returns the current user's active claim (if any) to grey out
// other Claim buttons. Identity is cookie-free: we infer it from
// `localStorage.e156_github_user` (set after the first successful claim)
// or the URL parameter ?user=<login> (useful for testing and deep links).
function currentUsersActiveClaim() {
  if (!currentUser) return null;
  for (const n in claims) {
    const c = claims[n];
    if (c.status !== "claimed") continue;
    if (c.github_user !== currentUser) continue;
    const left = daysLeft(c);
    if (left !== null && left < 0) continue;  // expired
    return {num: Number(n), claim: c};
  }
  return null;
}

function escapeHtml(s) {
  // P2-1 — include single-quote for attribute-safety in single-quoted contexts
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}

// P0-8 — URL-scheme allowlist. Reject anything that isn't http(s). Prevents
// `javascript:alert()` or `data:` URLs from sneaking in via a rogue workbook
// edit. Returns empty string if the URL fails validation.
function safeHref(url) {
  if (!url) return "";
  const s = String(url).trim();
  if (s.startsWith("https://") || s.startsWith("http://")) return s;
  return "";
}

const GH_ISSUE_BASE = "__GH_ISSUE_BASE__";

function claimIssueUrl(entry) {
  // GitHub form-template URL-prefill: match field IDs from claim.yml
  // `title` is a separate param; form field prefills use their ID names.
  const params = new URLSearchParams({
    template: "claim.yml",
    title: `[CLAIM #${entry.num}] ${(entry.title || entry.name).slice(0, 80)}`,
    "paper_number": String(entry.num),
    "paper_title": entry.title || entry.name,
  });
  return `${GH_ISSUE_BASE}?${params.toString()}`;
}

function submitIssueUrl(entry) {
  const params = new URLSearchParams({
    template: "submitted.yml",
    title: `[SUBMITTED #${entry.num}] ${(entry.title || entry.name).slice(0, 80)}`,
    "paper_number": String(entry.num),
  });
  return `${GH_ISSUE_BASE}?${params.toString()}`;
}

function toggleCard(num, btn) {
  const body = document.getElementById('body-' + num);
  const details = document.getElementById('details-' + num);
  const isOpen = !details.hidden;
  if (isOpen) {
    body.classList.remove('expanded');
    details.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = 'show full details <span aria-hidden="true">▼</span>';
  } else {
    // P0-2 / P2-14 — render the details panel on first expand only.
    if (!details.dataset.rendered) {
      const entry = ENTRIES.find(e => e.num === num);
      if (entry) {
        details.innerHTML = renderDetails(entry);
        details.style.cssText = 'margin-top:0.8rem; padding-top:0.8rem; border-top:1px solid var(--border); font-size:0.86rem; line-height:1.5;';
        details.dataset.rendered = '1';
      }
    }
    body.classList.add('expanded');
    details.hidden = false;
    btn.setAttribute('aria-expanded', 'true');
    btn.innerHTML = 'hide details <span aria-hidden="true">▲</span>';
  }
}

function linkIfUrl(val, fallback) {
  if (!val) return escapeHtml(fallback || '');
  const safe = safeHref(val);
  if (safe) {
    return `<a href="${escapeHtml(safe)}" target="_blank" rel="noopener">${escapeHtml(safe)}</a>`;
  }
  return escapeHtml(val);
}

// P0-9 — only linkify DOI captures that match the DOI syntax from
// Crossref's registration agency spec. Anything that includes URL-encoded
// characters, quotes, or non-DOI syntax is rendered as plain escaped text.
const DOI_RE = /doi:(10\.\d{4,9}\/[-._;()/:A-Z0-9]+)/gi;

function renderRefs(refs) {
  if (!Array.isArray(refs) || !refs.length) return '<em style="color:var(--text-faint)">(no references in workbook)</em>';
  return '<ol style="margin:0.3rem 0 0.3rem 1.2rem; padding:0;">' +
    refs.map(r => {
      const linked = escapeHtml(r).replace(DOI_RE, (match, doi) =>
        `doi:<a href="https://doi.org/${encodeURIComponent(doi)}" target="_blank" rel="noopener">${escapeHtml(doi)}</a>`);
      return `<li style="margin-bottom:0.3rem;">${linked}</li>`;
    }).join('') + '</ol>';
}

function renderDetails(e) {
  const row = (label, value) => {
    if (!value) return '';
    return `<div style="margin-bottom:0.5rem;"><strong style="color:var(--text-dim); font-size:0.78rem; text-transform:uppercase; letter-spacing:0.04em; display:block; margin-bottom:0.15rem;">${label}</strong><span>${value}</span></div>`;
  };

  const linkRow = (label, url) => {
    if (!url) return '';
    return row(label, `<a href="${escapeHtml(url)}" target="_blank" rel="noopener" style="word-break:break-all;">${escapeHtml(url)}</a>`);
  };

  return [
    // Repo / paper infrastructure links
    linkRow('Source code (GitHub)', e.code_url),
    linkRow('E156 protocol', e.protocol_url),
    linkRow('Dashboard (GitHub Pages)', e.pages_url),
    row('Target journal / section', e.target_journal ? `${escapeHtml(e.target_journal)}<br><span style="color:var(--text-dim);">Section: ${escapeHtml(e.section)}</span>` : ''),
    // Author info
    row('Corresponding author', e.corresponding_author ? `${escapeHtml(e.corresponding_author)}${e.orcid ? ` · ORCID ${escapeHtml(e.orcid)}` : ''}${e.affiliation ? `<br><span style="color:var(--text-dim);">${escapeHtml(e.affiliation)}</span>` : ''}` : ''),
    // References (the 2+ topic-pack refs)
    row('References', renderRefs(e.references)),
    // Standard submission statements
    row('Data availability', e.data_availability ? escapeHtml(e.data_availability) : ''),
    row('Ethics', e.ethics ? escapeHtml(e.ethics) : ''),
    row('Funding', e.funding ? escapeHtml(e.funding) : ''),
    row('Competing interests', e.competing_interests ? escapeHtml(e.competing_interests) : ''),
    row('Author contributions (CRediT)', e.credit ? escapeHtml(e.credit) : ''),
    row('AI disclosure', e.ai_disclosure ? escapeHtml(e.ai_disclosure) : ''),
    row('Reporting checklist', e.reporting_checklist ? escapeHtml(e.reporting_checklist) : ''),
    row('Preprint', e.preprint ? escapeHtml(e.preprint) : ''),
  ].filter(Boolean).join('');
}

function daysLeftLabel(entry) {
  const c = claims[entry.num];
  if (!c || !c.claim_date) return "";
  const d = daysLeft(c);
  if (d === null) return "";
  if (d < 0) return `<span class="days-left expired">expired — claim reopened</span>`;
  let cls = "ok";
  if (d <= 2) cls = "urgent";
  else if (d <= 7) cls = "warn";
  const plural = d === 1 ? "day" : "days";
  const extBadge = c.extended
    ? ` <span class="ext-badge" title="10-day extension granted">+10</span>`
    : "";
  return `<span class="days-left ${cls}">${d} ${plural} left to submit${extBadge}</span>`;
}

function extensionIssueUrl(entry) {
  const params = new URLSearchParams({
    template: "extension.yml",
    title: `[EXTENSION #${entry.num}] ${(entry.title || entry.name).slice(0, 80)}`,
    "paper_number": String(entry.num),
  });
  return `${GH_ISSUE_BASE}?${params.toString()}`;
}

function render() {
  // B2: keep URL in sync so filtered views can be shared by URL.
  writeFilterStateToUrl();

  // B1: show/hide the clear-filters button based on whether any filter is active.
  const clearBtn = document.getElementById("clear-filters");
  if (clearBtn) clearBtn.hidden = !hasAnyFilter();

  const grid = document.getElementById("grid");
  const q = filterText.toLowerCase().trim();
  const matches = ENTRIES.filter(e => {
    if (filterKind && kindOf(e) !== filterKind) return false;
    if (filterSeries && e.code_url !== filterSeries) return false;
    if (filterTopic && e.topic !== filterTopic) return false;
    if (filterStatus && statusOf(e) !== filterStatus) return false;
    if (!q) return true;
    const hay = (e.title + " " + e.body + " " + e.data + " " + e.topic + " " + e.name).toLowerCase();
    return hay.includes(q);
  });

  // B4: sort. Default ("num") keeps original ENTRIES ordering.
  if (sortBy === "open-first") {
    const rank = e => statusOf(e) === "open" ? 0 : statusOf(e) === "claimed" ? 1 : 2;
    matches.sort((a, b) => rank(a) - rank(b) || a.num - b.num);
  } else if (sortBy === "recent-claim") {
    const ts = e => {
      const c = claims[e.num];
      if (!c) return 0;
      const d = c.submit_date || c.claim_date;
      return d ? Date.parse(d) || 0 : 0;
    };
    matches.sort((a, b) => ts(b) - ts(a) || a.num - b.num);
  } else if (sortBy === "az") {
    matches.sort((a, b) => (a.title || a.name || "").localeCompare(b.title || b.name || ""));
  } else if (sortBy === "topic") {
    matches.sort((a, b) => (a.topic || "").localeCompare(b.topic || "") || a.num - b.num);
  }

  document.getElementById("count-chip").textContent = `showing ${matches.length} of ${ENTRIES.length}`;

  if (matches.length === 0) {
    // B5: empty-state with action chips. Each chip prefills a sample search
    // so the student doesn't dead-end on "no matches".
    grid.innerHTML = `
      <div class="empty-state">
        <p>No papers match your filters.</p>
        <div class="actions">
          <button type="button" data-action="clear">Clear all filters</button>
          <button type="button" data-action="try" data-q="living MA">Try "living MA"</button>
          <button type="button" data-action="try" data-q="rapidmeta">Try "rapidmeta"</button>
          <button type="button" data-action="try" data-q="diagnostic">Try "diagnostic"</button>
        </div>
      </div>`;
    return;
  }

  // P1-12 — if current user already holds an active claim on a DIFFERENT
  // paper, grey out the Claim button on every other open card.
  const mine = currentUsersActiveClaim();

  grid.innerHTML = matches.map(e => {
    const status = statusOf(e);
    const claim = claims[e.num];
    const statusLabel = status === "open" ? "OPEN" : status === "claimed" ? "CLAIMED" : "SUBMITTED";
    const blockedByMineRule = mine && status === "open" && mine.num !== e.num;
    // P0-2 / P2-14 — lazy-render the details panel on first expand.
    return `
      <div class="card ${status}">
        <div class="card-head">
          <span class="card-num" aria-hidden="true">[${e.num}]</span>
          <div class="card-title">${escapeHtml(e.title || e.name)}</div>
          <span class="card-badge ${status}" aria-label="status: ${statusLabel}">${statusLabel}</span>
        </div>
        <div class="card-meta">
          <span>${escapeHtml(e.type || "")}</span>
          <span>${escapeHtml(e.data || "")}</span>
          <span class="topic">${escapeHtml(e.topic)}</span>
          ${seriesOf(e) ? `<span class="series-badge" title="Shared repo with ${SERIES_INDEX[e.code_url]-1} other paper(s) — click to filter">📚 ${escapeHtml(seriesLabel(seriesOf(e)))}</span>` : ""}
        </div>
        <div class="card-body" id="body-${e.num}">${escapeHtml(e.body || "(no body)")}</div>
        <button class="toggle-body" aria-expanded="false" aria-controls="details-${e.num}" data-num="${e.num}">show full details <span aria-hidden="true">▼</span></button>
        <div class="card-details" id="details-${e.num}" hidden data-num="${e.num}"></div>
        ${claim && status !== "open"
          ? `<div class="claimed-by">${status === "submitted" ? "Submitted by" : "Claimed by"} <strong>${escapeHtml(claim.name)}</strong>${claim.affiliation ? ` · ${escapeHtml(claim.affiliation)}` : ""}${claim.claim_date ? ` · claimed ${escapeHtml(claim.claim_date)}` : ""}${status === "claimed" ? ` · ${daysLeftLabel(e)}` : ""}${status === "submitted" && claim.submit_date ? ` · submitted ${escapeHtml(claim.submit_date)}` : ""}</div>`
          : ""}
        <div class="card-actions">
          ${status === "open"
            ? (blockedByMineRule
                ? `<span class="btn greyed" aria-disabled="true" title="You already hold claim #${mine.num} — submit or let it expire first.">▶ One claim at a time</span>`
                : `<a class="btn primary" href="${claimIssueUrl(e)}" target="_blank" rel="noopener" aria-label="Claim paper ${e.num}"><span aria-hidden="true">▶ </span>Claim this paper</a>`)
            : status === "claimed"
              ? `<a class="btn primary" href="${submitIssueUrl(e)}" target="_blank" rel="noopener"><span aria-hidden="true">✓ </span>Confirm submission to ${TARGET_JOURNAL}</a>
                 ${claim && !claim.extended ? `<a class="btn" href="${extensionIssueUrl(e)}" target="_blank" rel="noopener" title="Adds 10 days to your window — auto-approved">+10-day extension</a>` : ""}`
              : `<button class="btn" disabled><span aria-hidden="true">✓ </span>Submitted</button>`}
          ${safeHref(e.code_url) ? `<a class="btn ghost" href="${escapeHtml(safeHref(e.code_url))}" target="_blank" rel="noopener" aria-label="Source code for paper ${e.num}">code <span aria-hidden="true">↗</span></a>` : ""}
          ${safeHref(e.pages_url) ? `<a class="btn ghost" href="${escapeHtml(safeHref(e.pages_url))}" target="_blank" rel="noopener" aria-label="Dashboard for paper ${e.num}">dashboard <span aria-hidden="true">↗</span></a>` : ""}
        </div>
      </div>`;
  }).join("");
}

function updateStats() {
  const total = ENTRIES.length;
  let open = 0, claimed = 0, submitted = 0;
  ENTRIES.forEach(e => {
    const s = statusOf(e);
    if (s === "open") open++;
    else if (s === "claimed") claimed++;
    else submitted++;
  });
  document.getElementById("stat-total").textContent = total;
  document.getElementById("stat-open").textContent = open;
  document.getElementById("stat-claimed").textContent = claimed;
  document.getElementById("stat-submitted").textContent = submitted;
}

function populateTopicFilter() {
  const topics = [...new Set(ENTRIES.map(e => e.topic))].sort();
  const sel = document.getElementById("filter-topic");
  topics.forEach(t => {
    const opt = document.createElement("option");
    opt.value = t;
    opt.textContent = t;
    sel.appendChild(opt);
  });
}

function populateSeriesFilter() {
  // Series = code repos that back 2+ papers. Sorted by paper count desc
  // so the biggest clusters (rapidmeta-finerenone with 17, Fatiha-Course
  // with 13) sit at the top of the dropdown.
  const shared = Object.entries(SERIES_INDEX).filter(([_, n]) => n >= 2);
  shared.sort((a, b) => b[1] - a[1]);
  const sel = document.getElementById("filter-series");
  shared.forEach(([url, n]) => {
    const opt = document.createElement("option");
    opt.value = url;
    opt.textContent = `${seriesLabel(url)} (${n} papers)`;
    sel.appendChild(opt);
  });
}

// P1-10 — if claims.json fetch fails, show the error banner so students
// don't mistakenly claim papers that are actually already taken.
fetch("claims.json", { cache: "no-cache" })
  .then(r => {
    if (!r.ok) throw new Error("HTTP " + r.status);
    return r.json();
  })
  .then(data => {
    claims = data || {};
    claimsLoaded = true;
    updateStats();
    render();
    if (typeof applyFocusFromQuery === "function") applyFocusFromQuery();
  })
  .catch(() => {
    claims = {};
    claimsLoaded = false;
    document.getElementById("claims-error").hidden = false;
    updateStats();
    render();
    if (typeof applyFocusFromQuery === "function") applyFocusFromQuery();
  });

// P1-12 — remember the user's GitHub login once they've claimed once
// (best-effort; no auth). Read from URL (?user=login) or localStorage.
try {
  const urlUser = new URLSearchParams(location.search).get("user");
  if (urlUser) {
    currentUser = urlUser;
    localStorage.setItem("e156_github_user", urlUser);
  } else {
    currentUser = localStorage.getItem("e156_github_user");
  }
} catch (_) { /* private-mode; ignore */ }

// P0-2 — debounce search so every keystroke doesn't rebuild 485 cards.
function debounce(fn, ms) {
  let t; return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
}
const searchEl = document.getElementById("search");
const onSearch = debounce(() => { filterText = searchEl.value; render(); }, 200);
searchEl.addEventListener("input", onSearch);
document.getElementById("filter-topic").addEventListener("change", e => { filterTopic = e.target.value; render(); });
document.getElementById("filter-status").addEventListener("change", e => { filterStatus = e.target.value; render(); });
document.getElementById("filter-kind").addEventListener("change", e => { filterKind = e.target.value; render(); });
document.getElementById("filter-series").addEventListener("change", e => { filterSeries = e.target.value; render(); });
document.getElementById("sort-by").addEventListener("change", e => { sortBy = e.target.value; render(); });

// B1: Clear-all-filters resets every control + URL state in one click.
function clearAllFilters() {
  filterText = ""; filterTopic = ""; filterStatus = ""; filterKind = "";
  filterSeries = ""; sortBy = "num";
  document.getElementById("search").value = "";
  document.getElementById("filter-kind").value = "";
  document.getElementById("filter-series").value = "";
  document.getElementById("filter-topic").value = "";
  document.getElementById("filter-status").value = "";
  document.getElementById("sort-by").value = "num";
  render();
}
document.getElementById("clear-filters").addEventListener("click", clearAllFilters);

// B5: empty-state action chips. Delegated on #grid since they only exist
// when matches.length === 0 and the DOM is re-rendered each time.
document.getElementById("grid").addEventListener("click", ev => {
  const btn = ev.target.closest(".empty-state button[data-action]");
  if (!btn) return;
  if (btn.dataset.action === "clear") {
    clearAllFilters();
  } else if (btn.dataset.action === "try" && btn.dataset.q) {
    clearAllFilters();
    filterText = btn.dataset.q;
    document.getElementById("search").value = btn.dataset.q;
    render();
  }
});

// B3: keyboard shortcuts. Skip when an input/textarea/select is focused.
document.addEventListener("keydown", ev => {
  const tag = (ev.target && ev.target.tagName || "").toUpperCase();
  const inField = tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT";
  const helpDlg = document.getElementById("kbd-help");
  if (ev.key === "/" && !inField) {
    ev.preventDefault();
    document.getElementById("search").focus();
  } else if (ev.key === "?" && !inField) {
    ev.preventDefault();
    if (helpDlg.open) helpDlg.close();
    else if (helpDlg.showModal) helpDlg.showModal();
  } else if (ev.key === "Escape") {
    const s = document.getElementById("search");
    if (document.activeElement === s) {
      if (s.value) { s.value = ""; filterText = ""; render(); }
      else { s.blur(); }
    } else if (helpDlg.open) {
      helpDlg.close();
    }
  } else if (ev.key === "c" && !inField && !ev.ctrlKey && !ev.metaKey && !ev.altKey) {
    clearAllFilters();
  }
});

// P2-2 — event delegation for toggle buttons (avoids 485 inline onclicks).
document.getElementById("grid").addEventListener("click", ev => {
  const badge = ev.target.closest(".series-badge");
  if (badge) {
    // Click a series badge to filter the board to just that series
    const card = badge.closest(".card");
    const entry = ENTRIES.find(e => card && card.querySelector(`[data-num="${e.num}"]`));
    if (entry && entry.code_url) {
      filterSeries = entry.code_url;
      const sel = document.getElementById("filter-series");
      sel.value = entry.code_url;
      render();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
    return;
  }
  const btn = ev.target.closest(".toggle-body");
  if (!btn) return;
  const num = Number(btn.dataset.num);
  if (Number.isFinite(num)) toggleCard(num, btn);
});

populateTopicFilter();
populateSeriesFilter();
updateStats();

// B2: restore filter state from URL on first load. Must run AFTER the
// topic/series dropdowns are populated (so the .value=... below succeeds)
// but BEFORE the first render() so we don't render twice.
readFilterStateFromUrl();
document.getElementById("search").value = filterText;
document.getElementById("filter-kind").value = filterKind;
document.getElementById("filter-series").value = filterSeries;
document.getElementById("filter-topic").value = filterTopic;
document.getElementById("filter-status").value = filterStatus;
document.getElementById("sort-by").value = sortBy;

render();

// Deep-link: ?focus=NNN scrolls to and highlights paper number NNN.
// Used by rapidmeta-finerenone landing page and dashboards to send students
// directly to a specific paper. Pure visual — does not change any filter.
//
// Uses a MutationObserver on #grid so the highlight survives re-renders
// triggered by claims.json fetch settlement and filter changes.
let __focusInitDone = false;
let __focusObserver = null;
function applyFocusFromQuery() {
  let focusNum;
  try { focusNum = new URLSearchParams(location.search).get("focus"); } catch (_) { return; }
  if (!focusNum) return;
  const target = String(focusNum).trim();
  if (!/^\d+$/.test(target)) return;

  function highlightAndMaybeScroll(scroll) {
    const cards = document.querySelectorAll(".card");
    for (const c of cards) {
      const numEl = c.querySelector(".card-num");
      if (numEl && numEl.textContent.replace(/[^\d]/g, "") === target) {
        c.style.transition = "box-shadow 0.3s, border-color 0.3s";
        c.style.boxShadow = "0 0 0 3px var(--accent)";
        c.style.borderColor = "var(--accent)";
        c.classList.add("focus-deeplinked");
        if (scroll) c.scrollIntoView({ behavior: "smooth", block: "center" });
        return c;
      }
    }
    return null;
  }

  // Initial poll for up to 5s — in case the first render is async
  if (!__focusInitDone) {
    let attempts = 0;
    const tick = () => {
      if (highlightAndMaybeScroll(true)) { __focusInitDone = true; return; }
      if (++attempts < 25) setTimeout(tick, 200);
      else __focusInitDone = true;
    };
    setTimeout(tick, 200);
  } else {
    // Subsequent calls (post-fetch / post-filter) — re-apply without re-scrolling
    highlightAndMaybeScroll(false);
  }

  // Bind observer once so re-renders re-apply the highlight automatically
  if (!__focusObserver) {
    const grid = document.getElementById("grid");
    if (grid) {
      __focusObserver = new MutationObserver(() => highlightAndMaybeScroll(false));
      __focusObserver.observe(grid, { childList: true, subtree: false });
    }
  }
}
applyFocusFromQuery();
</script>

</body>
</html>
"""


HIDE_LIST = Path(__file__).resolve().parents[1] / "audit_output" / "hide_repo_404.json"


def main() -> int:
    text = WORKBOOK.read_text(encoding="utf-8")
    # P0-4 — strip a leading UTF-8 BOM if present. Some editors silently add
    # one on save; without this `ENTRY_HEAD_RE.search` would fail on the first
    # block and we'd silently ship an empty board.
    text = text.lstrip("\ufeff")
    entries = parse_entries(text)
    entries.sort(key=lambda e: e["num"])

    # P0-4 — fail-closed floor: if parsing produced fewer entries than the
    # workbook must contain, abort rather than ship a tiny or empty board.
    if len(entries) < 400:
        raise SystemExit(
            f"ERROR: parse_entries returned only {len(entries)} entries — "
            f"expected ≥ 400. Workbook may be corrupted (BOM, encoding, "
            f"or header format drift). Aborting build."
        )

    # Filter out entries whose repos don't exist on GitHub.
    # The hide list is generated by audit_links.py + repo_404_triage.py;
    # entries are hidden (not deleted from the workbook) so they can be
    # un-hidden the moment the repo is pushed.
    hide_nums: set[int] = set()
    if HIDE_LIST.is_file():
        hide_nums = set(json.loads(HIDE_LIST.read_text(encoding="utf-8")))
    if hide_nums:
        before = len(entries)
        entries = [e for e in entries if e["num"] not in hide_nums]
        print(f"Filtered {before - len(entries)} entries with missing repos "
              f"({len(entries)} remain, {len(hide_nums)} hidden)")

    # Build each entry for the browser. All fields parsed from the
    # SUBMISSION METADATA block are preserved so renderDetails() can
    # show the full paper context on expand (GitHub links, refs, ethics,
    # CRediT, COI, AI disclosure, target journal, etc.).
    compact = [
        {
            # Card head / filter
            "num": e["num"],
            "name": sanitize_public_text(e.get("name", "")),
            "title": sanitize_public_text(e.get("title", "")),
            "type": sanitize_public_text(e.get("type", "")),
            "data": sanitize_public_text(e.get("data", "")),
            "body": sanitize_public_text(e.get("body", "")),
            "topic": sanitize_public_text(e.get("topic", "unknown")),
            "submitted_head": e.get("submitted_head", False),
            # Links
            "code_url": e.get("code_url", ""),
            "protocol_url": e.get("protocol_url", ""),
            "pages_url": e.get("pages_url", ""),
            # Expanded-details block
            "target_journal": sanitize_public_text(e.get("target_journal", "")),
            "section": sanitize_public_text(e.get("section", "")),
            "corresponding_author": sanitize_public_text(e.get("corresponding_author", "")),
            "orcid": sanitize_public_text(e.get("orcid", "")),
            "affiliation": sanitize_public_text(e.get("affiliation", "")),
            "references": [sanitize_public_text(ref) for ref in e.get("references", [])],
            "data_availability": sanitize_public_text(e.get("data_availability", "")),
            "ethics": sanitize_public_text(e.get("ethics", "")),
            "funding": sanitize_public_text(e.get("funding", "")),
            "competing_interests": sanitize_public_text(e.get("competing_interests", "")),
            "credit": sanitize_public_text(normalize_credit(e.get("credit", ""))),
            "ai_disclosure": sanitize_public_text(e.get("ai_disclosure", "")),
            "reporting_checklist": sanitize_public_text(e.get("reporting_checklist", "")),
            "preprint": sanitize_public_text(e.get("preprint", "")),
        }
        for e in entries
    ]

    html_out = (
        HTML_TEMPLATE
        .replace("__AUTHOR_EMAIL__", AUTHOR_EMAIL)
        .replace("__TARGET_JOURNAL__", TARGET_JOURNAL)
        .replace("__CLAIM_WINDOW__", str(CLAIM_WINDOW_DAYS))
        .replace("__EXTENSION_DAYS__", str(EXTENSION_DAYS))
        .replace("__GH_ISSUE_BASE__", GH_ISSUE_BASE)
        .replace("__N_VISIBLE__", str(len(entries)))
        .replace("__ENTRIES_JSON__", json.dumps(compact, ensure_ascii=False))
    )
    OUT_HTML.write_text(html_out, encoding="utf-8")
    print(f"Wrote {OUT_HTML} ({len(html_out):,} bytes, {len(entries)} entries)")

    if not CLAIMS_JSON.exists():
        CLAIMS_JSON.write_text("{}\n", encoding="utf-8")
        print(f"Initialized empty {CLAIMS_JSON}")
    else:
        print(f"claims.json already exists; leaving untouched")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
