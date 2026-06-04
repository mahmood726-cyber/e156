#!/usr/bin/env python
"""Convert students.html to a light, NYT-style editorial theme + a parable-spine
tagline that explains the concept. The page is variable-driven, so the palette
flips via :root; a small override block fixes the few status colors that were
light-on-dark, and adds serif headlines. Functionality (board, claim, search,
scripts) is untouched -- only CSS + the tagline change.
"""
from __future__ import annotations
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
TARGETS = [os.path.join(ROOT, "students.html"),
           os.path.join(ROOT, "scripts", "build_students_page.py")]

NEW_ROOT = """:root {
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
}"""

OVERRIDES = """
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
</style>"""

OLD_TAGLINE = ('<p class="tagline">Pick a paper, rewrite the 156-word body, submit to '
               '<strong>◆ Synthēsis</strong> (Methods Note section, ≤400 words). '
               'Open to Ugandan medical students and anyone else interested in '
               'evidence-synthesis co-authorship. — Mahmood Ahmad, Tahir Heart Institute.</p>')

NEW_TAGLINE = ('<p class="tagline">Every paper on this board is a complete, machine-drafted '
               'meta-analysis &mdash; rigorous, but unwritten. Claim one, rewrite the 156-word '
               'body in your own voice and judgement, and submit it to '
               '<strong>◆ Synthēsis</strong> under your name. Real authorship, in a real '
               'journal &mdash; open to Ugandan medical students and anyone learning evidence '
               'synthesis. <span style="white-space:nowrap">&mdash; Mahmood Ahmad, Tahir Heart '
               'Institute.</span></p>')


def restyle(path):
    data = open(path, "rb").read().decode("utf-8", "replace")
    changed = []
    # 1) palette flip (only if still dark)
    if "--bg: #0b1120" in data:
        data = re.sub(r":root\s*\{.*?\}", lambda m: NEW_ROOT, data, count=1, flags=re.S)
        changed.append("palette")
    # 2) overrides (only once)
    if "NYT-editorial light theme" not in data:
        data = data.replace("</style>", OVERRIDES, 1)
        changed.append("overrides")
    # 3) parable tagline
    if OLD_TAGLINE in data:
        data = data.replace(OLD_TAGLINE, NEW_TAGLINE, 1)
        changed.append("tagline")
    open(path, "wb").write(data.encode("utf-8"))
    return changed


def main():
    for p in TARGETS:
        if not os.path.exists(p):
            print(f"skip (missing): {p}")
            continue
        ch = restyle(p)
        print(f"{os.path.basename(p)}: {ch if ch else 'already styled (no-op)'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
