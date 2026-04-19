"""Build the student claim page for https://mahmood726-cyber.github.io/e156/students.html

Parses rewrite-workbook.txt, extracts all 483 entries + their SUBMISSION
METADATA, and emits a single-file HTML with embedded JSON data. Students
browse, filter, and click "Claim" which opens a pre-filled mailto: email.

Claim tracking: reads claims.json from the same directory at page load.
The user (mahmood) updates claims.json manually after receiving claim
emails. The page shows the current claim state live.

Outputs:
  - C:\\E156\\students.html        (single-file, no external deps)
  - C:\\E156\\claims.json          (initialized empty if missing)

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
TARGET_JOURNAL = "Synthesis Medicine"
CLAIM_WINDOW_DAYS = 42  # 6 weeks — student loses claim if not submitted by then
GH_REPO = "mahmood726-cyber/e156"
GH_ISSUE_BASE = f"https://github.com/{GH_REPO}/issues/new"

ENTRY_HEAD_RE = re.compile(r"^\[(\d+)/\d+\]\s+(.+?)\s*$", re.MULTILINE)


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
            # Workbook has some duplicate [N/T] headers (e.g. #339 and #351
            # both appear twice with different titles). Keep the first
            # occurrence only — matches build_paper_pages.py behavior and
            # prevents rendering one paper num as two cards with different
            # Dashboard URLs.
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
        # Links block — all three URLs.
        code_m = re.search(r"Code:\s+(\S+)", block)
        protocol_m = re.search(r"Protocol:\s+(\S+)", block)
        pages_m = re.search(r"Dashboard:\s+(\S+)", block)
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


HTML_TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>E156 Student Board — Claim, rewrite, submit to Synthesis Medicine</title>
<meta name="description" content="__N_VISIBLE__ E156 micro-papers open to student co-authorship. Target journal: Synthesis Medicine. Claim via GitHub Issues, 6 weeks to submit, then claim expires.">

<style>
:root {
  --bg: #0b1120;
  --bg-elev: #111827;
  --bg-card: #1a2236;
  --border: #2a3244;
  --text: #e5e7eb;
  --text-dim: #9ca3af;
  --text-faint: #6b7280;
  --accent: #22c55e;
  --warn: #eab308;
  --claimed: #3b82f6;
  --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  --sans: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
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
.toolbar input[type="search"] { flex: 1 1 240px; min-width: 180px; }
.toolbar select { min-width: 140px; }
.toolbar .count-chip { color: var(--text-dim); font-family: var(--mono); font-size: 0.88rem; margin-left: auto; }

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
  padding: 0.45rem 0.9rem;
  border-radius: 5px;
  font-size: 0.85rem;
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

.toggle-body { background: none; border: 0; color: var(--text-faint); font-family: var(--mono); font-size: 0.75rem; cursor: pointer; padding: 0; margin-top: 0.3rem; }
.toggle-body:hover { color: var(--accent); }

footer { padding: 2rem 0; border-top: 1px solid var(--border); color: var(--text-dim); font-size: 0.85rem; text-align: center; }
</style>
</head>
<body>

<header>
  <div class="container">
    <h1><span class="accent">E156</span> Student Board <span class="journal-mark" title="Target journal: Synthēsis (synthesis-medicine.org)">◆ Synthēsis</span></h1>
    <p class="tagline">Pick a paper, rewrite the 156-word body, submit to <strong>◆ Synthēsis</strong> (Methods Note section, ≤400 words). Open to Ugandan medical students and anyone else interested in evidence-synthesis co-authorship. — Mahmood Ahmad, Tahir Heart Institute.</p>

    <div class="instructions">
      <h2>How this works</h2>
      <ol>
        <li><strong>You need a GitHub account</strong> (free, 2-minute signup at <a href="https://github.com/signup" target="_blank">github.com/signup</a>). If you're a researcher you'll want one anyway.</li>
        <li>Browse the list. Search by topic (e.g. "heart failure", "network meta-analysis", "diagnostic").</li>
        <li>Click <strong>▶ Claim this paper</strong> on the card you want. A GitHub form opens pre-filled with the paper number — fill in your name, affiliation, email, <strong>nominate a senior / last author (your faculty supervisor)</strong>, tick the agreements, click "Submit new issue". <strong>Within ~60 seconds this board updates automatically</strong> showing your name and a 42-day countdown.</li>
        <li>Copy the <span class="mono">Current body</span> on your card. Rewrite it in your own words: 156 words, 7 sentences (Question · Dataset · Method · Result · Robustness · Interpretation · Boundary).</li>
        <li>Submit your rewrite to <strong>Synthesis Medicine Journal</strong> (synthesis-medicine.org). The journal mints DOIs on acceptance; no Zenodo step needed.</li>
        <li>Once submitted, click <strong>✓ Confirm submission</strong> on your card. A second GitHub form opens — paste your submission ID / DOI, submit. Board updates to show SUBMITTED. You are listed as first author.</li>
        <li><strong>You have 6 weeks (42 days) from claim to submission.</strong> If you don't confirm submission within that window, your claim expires and the paper reopens for another student. Pick a paper you can actually finish in 6 weeks.</li>
      </ol>

      <h2>Authorship rules (read before claiming)</h2>
      <ul>
        <li><strong>You are first author</strong> on the submission you claim.</li>
        <li>You must nominate a <strong>senior / last author</strong> — typically your faculty supervisor or a co-investigator from your institution. The claim form has a required field for this. <strong>No supervisor available yet?</strong> Type exactly <span class="mono">TBD - request mentor</span> in that field and Mahmood will help nominate a faculty co-investigator from the E156 advisory pool before you submit.</li>
        <li><strong>Mahmood Ahmad will appear as a middle author only</strong> — never first, never last. This is a fixed workbook-wide rule (his role: Conceptualization, Methodology, Software, Data curation; not original drafting).</li>
        <li>Every submission must include the competing-interests statement: <em>"MA serves on the editorial board of Synthēsis (the target journal); MA had no role in editorial decisions on this manuscript, which was handled by an independent editor of the journal."</em> This is auto-included in the SUBMISSION METADATA block of every workbook entry.</li>
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
        <li><strong>Copy/paste these blocks unchanged from the SUBMISSION METADATA on your card:</strong> Data availability, Ethics, Funding, Competing interests (the editorial-board statement), CRediT (3-actor template), AI disclosure.</li>
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
            <li>1st = <strong>YOU</strong> (first author)</li>
            <li>middle = <strong>Mahmood Ahmad</strong>, ORCID 0000-0001-9107-3704, Tahir Heart Institute, Rabwah, Pakistan</li>
            <li>last = your <strong>faculty supervisor</strong> (the senior author you named on the claim form)</li>
          </ul>
          Then paste the Vancouver references.</li>
        <li><strong>Confirmation</strong> — review and click <strong>"Finish Submission"</strong>.</li>
        <li><strong>Next Steps</strong> — note the submission ID shown on screen. You'll need it for the next step.</li>
      </ol>

      <h3>Step 4 — Confirm on this board</h3>
      <ul>
        <li>Come back to this page, find your card, click <strong>✓ Confirm submission</strong>, and paste your OJS submission ID (or DOI once minted). Your card flips to SUBMITTED. The 42-day countdown stops.</li>
      </ul>

      <p style="font-size:0.85rem; color:var(--text-dim); margin-top:1rem;">
        <strong>Fallback:</strong> if the OJS site is down, email <a href="mailto:submissions@synthes.is">submissions@synthes.is</a> with the .docx attached and the subject "RE: E156 Methods Note submission, paper #N", then still confirm here so the board updates.
      </p>
    </div>

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
      <input type="search" id="search" placeholder="Search title, body, data, topic...">
      <select id="filter-topic"><option value="">All topics</option></select>
      <select id="filter-status">
        <option value="">All statuses</option>
        <option value="open">Open to claim</option>
        <option value="claimed">Claimed</option>
        <option value="submitted">Submitted</option>
      </select>
      <span class="count-chip" id="count-chip">showing 0 of 0</span>
    </div>
  </div>
</div>

<div class="container">
  <div class="grid" id="grid"></div>
</div>

<footer>
  <div class="container">
    <p>Live workbook · Updates when I merge your rewrite · Questions → <a href="mailto:__AUTHOR_EMAIL__">__AUTHOR_EMAIL__</a></p>
  </div>
</footer>

<script>
const AUTHOR_EMAIL = "__AUTHOR_EMAIL__";
const TARGET_JOURNAL = "__TARGET_JOURNAL__";
const CLAIM_WINDOW_DAYS = __CLAIM_WINDOW__;
const MS_PER_DAY = 86400000;
const ENTRIES = __ENTRIES_JSON__;

let claims = {};  // populated from claims.json
let filterText = "";
let filterTopic = "";
let filterStatus = "";

function daysLeft(claimDate) {
  // claimDate is "YYYY-MM-DD". Returns integer days remaining (may be negative).
  if (!claimDate) return null;
  const claim = new Date(claimDate + "T00:00:00Z").getTime();
  const now = Date.now();
  const elapsed = (now - claim) / MS_PER_DAY;
  return Math.ceil(CLAIM_WINDOW_DAYS - elapsed);
}

function statusOf(entry) {
  if (entry.submitted_head) return "submitted";
  const c = claims[entry.num];
  if (!c) return "open";
  if (c.status === "submitted") return "submitted";
  // If expired (past 6 weeks without submission), treat as open
  const left = daysLeft(c.claim_date);
  if (left !== null && left < 0) return "open";
  return "claimed";
}

function escapeHtml(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
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
  const isOpen = details.style.display !== 'none';
  if (isOpen) {
    body.classList.remove('expanded');
    details.style.display = 'none';
    btn.textContent = 'show full details ▼';
  } else {
    body.classList.add('expanded');
    details.style.display = 'block';
    btn.textContent = 'hide details ▲';
  }
}

function linkIfUrl(val, fallback) {
  if (!val) return escapeHtml(fallback || '');
  const url = String(val).trim();
  if (url.startsWith('http')) {
    return `<a href="${escapeHtml(url)}" target="_blank" rel="noopener">${escapeHtml(url)}</a>`;
  }
  return escapeHtml(val);
}

function renderRefs(refs) {
  if (!Array.isArray(refs) || !refs.length) return '<em style="color:var(--text-faint)">(no references in workbook)</em>';
  return '<ol style="margin:0.3rem 0 0.3rem 1.2rem; padding:0;">' +
    refs.map(r => {
      // Linkify trailing "doi:X" tokens
      const linked = escapeHtml(r).replace(/doi:(\S+)/g, 'doi:<a href="https://doi.org/$1" target="_blank">$1</a>');
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
  const d = daysLeft(c.claim_date);
  if (d === null) return "";
  if (d < 0) return `<span class="days-left expired">expired — claim reopened</span>`;
  let cls = "ok";
  if (d <= 2) cls = "urgent";
  else if (d <= 7) cls = "warn";
  const plural = d === 1 ? "day" : "days";
  return `<span class="days-left ${cls}">${d} ${plural} left to submit</span>`;
}

function render() {
  const grid = document.getElementById("grid");
  const q = filterText.toLowerCase().trim();
  const matches = ENTRIES.filter(e => {
    if (filterTopic && e.topic !== filterTopic) return false;
    if (filterStatus && statusOf(e) !== filterStatus) return false;
    if (!q) return true;
    const hay = (e.title + " " + e.body + " " + e.data + " " + e.topic + " " + e.name).toLowerCase();
    return hay.includes(q);
  });

  document.getElementById("count-chip").textContent = `showing ${matches.length} of ${ENTRIES.length}`;

  if (matches.length === 0) {
    grid.innerHTML = '<p style="color:var(--text-dim); text-align:center; padding:3rem 0;">No papers match your filters.</p>';
    return;
  }

  grid.innerHTML = matches.map(e => {
    const status = statusOf(e);
    const claim = claims[e.num];
    const statusLabel = status === "open" ? "OPEN" : status === "claimed" ? "CLAIMED" : "SUBMITTED";
    const btnDisabled = status !== "open";
    return `
      <div class="card ${status}">
        <div class="card-head">
          <span class="card-num">[${e.num}]</span>
          <div class="card-title">${escapeHtml(e.title || e.name)}</div>
          <span class="card-badge ${status}">${statusLabel}</span>
        </div>
        <div class="card-meta">
          <span>${escapeHtml(e.type || "")}</span>
          <span>${escapeHtml(e.data || "")}</span>
          <span class="topic">${escapeHtml(e.topic)}</span>
        </div>
        <div class="card-body" id="body-${e.num}">${escapeHtml(e.body || "(no body)")}</div>
        <button class="toggle-body" onclick="toggleCard(${e.num}, this)">show full details ▼</button>
        <div class="card-details" id="details-${e.num}" style="display:none; margin-top:0.8rem; padding-top:0.8rem; border-top:1px solid var(--border); font-size:0.86rem; line-height:1.5;">
          ${renderDetails(e)}
        </div>
        ${claim && status !== "open"
          ? `<div class="claimed-by">${status === "submitted" ? "Submitted by" : "Claimed by"} <strong>${escapeHtml(claim.name)}</strong>${claim.affiliation ? ` · ${escapeHtml(claim.affiliation)}` : ""}${claim.claim_date ? ` · claimed ${escapeHtml(claim.claim_date)}` : ""}${status === "claimed" ? ` · ${daysLeftLabel(e)}` : ""}${status === "submitted" && claim.submit_date ? ` · submitted ${escapeHtml(claim.submit_date)}` : ""}</div>`
          : ""}
        <div class="card-actions">
          ${status === "open"
            ? `<a class="btn primary" href="${claimIssueUrl(e)}" target="_blank" rel="noopener">▶ Claim this paper</a>`
            : status === "claimed"
              ? `<a class="btn primary" href="${submitIssueUrl(e)}" target="_blank" rel="noopener">✓ Confirm submission to ${TARGET_JOURNAL}</a>`
              : `<button class="btn" disabled>✓ Submitted</button>`}
          ${e.code_url ? `<a class="btn ghost" href="${escapeHtml(e.code_url)}" target="_blank">code ↗</a>` : ""}
          ${e.pages_url ? `<a class="btn ghost" href="${escapeHtml(e.pages_url)}" target="_blank">dashboard ↗</a>` : ""}
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

// Load claims.json (fire-and-forget; if missing, start with empty)
fetch("claims.json", { cache: "no-cache" })
  .then(r => r.ok ? r.json() : {})
  .then(data => { claims = data || {}; updateStats(); render(); })
  .catch(() => { claims = {}; updateStats(); render(); });

document.getElementById("search").addEventListener("input", e => { filterText = e.target.value; render(); });
document.getElementById("filter-topic").addEventListener("change", e => { filterTopic = e.target.value; render(); });
document.getElementById("filter-status").addEventListener("change", e => { filterStatus = e.target.value; render(); });

populateTopicFilter();
updateStats();
render();
</script>

</body>
</html>
"""


HIDE_LIST = Path(__file__).resolve().parents[1] / "audit_output" / "hide_repo_404.json"


def main() -> int:
    text = WORKBOOK.read_text(encoding="utf-8")
    entries = parse_entries(text)
    entries.sort(key=lambda e: e["num"])

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
            "name": e.get("name", ""),
            "title": e.get("title", ""),
            "type": e.get("type", ""),
            "data": e.get("data", ""),
            "body": e.get("body", ""),
            "topic": e.get("topic", "unknown"),
            "submitted_head": e.get("submitted_head", False),
            # Links
            "code_url": e.get("code_url", ""),
            "protocol_url": e.get("protocol_url", ""),
            "pages_url": e.get("pages_url", ""),
            # Expanded-details block
            "target_journal": e.get("target_journal", ""),
            "section": e.get("section", ""),
            "corresponding_author": e.get("corresponding_author", ""),
            "orcid": e.get("orcid", ""),
            "affiliation": e.get("affiliation", ""),
            "references": e.get("references", []),
            "data_availability": e.get("data_availability", ""),
            "ethics": e.get("ethics", ""),
            "funding": e.get("funding", ""),
            "competing_interests": e.get("competing_interests", ""),
            "credit": e.get("credit", ""),
            "ai_disclosure": e.get("ai_disclosure", ""),
            "reporting_checklist": e.get("reporting_checklist", ""),
            "preprint": e.get("preprint", ""),
        }
        for e in entries
    ]

    html_out = (
        HTML_TEMPLATE
        .replace("__AUTHOR_EMAIL__", AUTHOR_EMAIL)
        .replace("__TARGET_JOURNAL__", TARGET_JOURNAL)
        .replace("__CLAIM_WINDOW__", str(CLAIM_WINDOW_DAYS))
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
