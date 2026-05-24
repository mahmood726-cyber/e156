"""
Regression test: students.html and rewrite-workbook.txt must not leak
template placeholders or Python literals into the rendered output.

Catches the family of bugs repaired across commits 8f6b84d (workbook),
b54e1ac (1110 rapidmeta dashboards), and cc9dc53 (upstream generator):

  - body containing the literal token "n participants" (placeholder leak
    when the actual participant count was unavailable)
  - body containing the circular phrase "the pooled estimate was the
    pooled estimate" (broken f-string template substitution)
  - body containing a bare "None" outside known whitelisted contexts
    (Python None object str-coerced into the rendered text)
  - DATA line containing "None trials" or "None participants" (same root
    cause)

A failing assertion lists the offending entry numbers so future
regressions are immediately attributable.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
STUDENTS_HTML = ROOT / "students.html"
WORKBOOK = ROOT / "rewrite-workbook.txt"


def _extract_entries() -> list[dict]:
    """Parse the const ENTRIES = [...] array embedded in students.html.

    Shares the same bracket-balanced parser used by the manual audit
    script at C:\\Users\\mahmo\\.claude\\scratch\\e156_audit.py — keep
    the two in sync if the embedding format ever changes.
    """
    html = STUDENTS_HTML.read_text(encoding="utf-8")
    m = re.search(r"const\s+ENTRIES\s*=\s*\[", html)
    assert m is not None, "ENTRIES array not found in students.html"
    start = m.end() - 1  # position of '['
    i = start
    depth = 0
    in_str = False
    str_ch = None
    esc = False
    while i < len(html):
        c = html[i]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == str_ch:
                in_str = False
        else:
            if c in '"\'':
                in_str = True
                str_ch = c
            elif c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        i += 1
    else:  # pragma: no cover
        raise AssertionError("Could not find closing bracket for ENTRIES")
    return json.loads(html[start:end])


# Whitelist: legitimate occurrences of "None" in entry text. Update
# CAREFULLY — every entry on this list bypasses the regression guard.
NONE_WHITELIST = (
    "None declared",                   # COI / funding boilerplate
    "point|None",                      # Python type-hint expression in entry #484
    "Possibility Envelope",            # the (lower, upper, point|None, min_info, assumptions) tuple in #484
)


@pytest.fixture(scope="module")
def entries() -> list[dict]:
    return _extract_entries()


def _violations(entries, predicate, field="body"):
    """Return [(num, snippet), ...] for entries whose `field` matches `predicate`."""
    out = []
    for e in entries:
        v = e.get(field) or ""
        m = predicate(v)
        if m:
            idx = m if isinstance(m, int) else m.start()
            out.append((e.get("num"), v[max(0, idx - 40): idx + 60]))
    return out


def test_no_n_participants_placeholder(entries):
    """Bodies must not contain the literal 'n participants' placeholder.

    This is what leaked when generate_rapidmeta_entries.py:synth_body()
    fell through to its else branch and emitted the variable name 'n'
    as if it were a substituted value (commit 8f6b84d fixed 1208 of them;
    commit a1052c5 fixed the generator).
    """
    pat = re.compile(r"\bn participants\b")
    bad = _violations(entries, pat.search)
    assert not bad, (
        f"{len(bad)} entries leak 'n participants' placeholder; "
        f"first 10: {[(n, s) for n, s in bad[:10]]}"
    )


def test_no_circular_pooled_estimate(entries):
    """Bodies must not contain 'the pooled estimate was the pooled estimate'."""
    pat = re.compile(r"the pooled estimate was the pooled estimate")
    bad = _violations(entries, pat.search)
    assert not bad, (
        f"{len(bad)} entries contain circular template phrase; "
        f"first 5: {[(n, s) for n, s in bad[:5]]}"
    )


def test_no_python_none_in_body(entries):
    """Bodies must not contain a bare 'None' outside known whitelist."""
    pat = re.compile(r"\bNone\b")
    bad = []
    for e in entries:
        body = e.get("body") or ""
        for m in pat.finditer(body):
            # Check context for whitelist
            ctx = body[max(0, m.start() - 40): m.end() + 40]
            if any(w in ctx for w in NONE_WHITELIST):
                continue
            bad.append((e["num"], ctx))
            break
    assert not bad, (
        f"{len(bad)} entries contain a bare 'None' in body; "
        f"first 5: {[(n, s) for n, s in bad[:5]]}"
    )


def test_no_none_in_data_line(entries):
    """DATA line must not say 'None trials' or 'None participants'."""
    pat = re.compile(r"None\s+(?:trials|participants)\b")
    bad = _violations(entries, pat.search, field="data")
    assert not bad, (
        f"{len(bad)} entries have 'None trials/participants' in DATA line; "
        f"first 10: {[(n, s) for n, s in bad[:10]]}"
    )


def test_no_python_none_in_workbook_links():
    """Workbook Code/Protocol/Dashboard lines must not contain literal 'None'."""
    text = WORKBOOK.read_text(encoding="utf-8")
    line_re = re.compile(r"^\s+(Code|Protocol|Dashboard):\s+(\S+)\s*$", re.MULTILINE)
    bad = []
    for m in line_re.finditer(text):
        url = m.group(2)
        if url == "None" or url.endswith("/None"):
            bad.append((m.group(1), url))
    assert not bad, f"{len(bad)} link lines contain None URLs: {bad[:5]}"


def test_entry_num_unique(entries):
    """Each entry number must appear exactly once."""
    from collections import Counter
    counts = Counter(e["num"] for e in entries)
    dups = [(n, c) for n, c in counts.items() if c > 1]
    assert not dups, f"Duplicate entry numbers: {dups}"


def test_every_entry_has_title_and_body(entries):
    """Every entry must have a non-empty title and body."""
    no_title = [e["num"] for e in entries if not (e.get("title") or "").strip()]
    no_body = [e["num"] for e in entries if not (e.get("body") or "").strip()]
    assert not no_title, f"{len(no_title)} entries with empty title: {no_title[:10]}"
    assert not no_body, f"{len(no_body)} entries with empty body: {no_body[:10]}"


def test_canonical_synthesis_spelling(entries):
    """target_journal must use the canonical 'Synthēsis' (with macron)."""
    bad = []
    for e in entries:
        j = e.get("target_journal") or ""
        if j and "Synth" in j and "Synthēsis" not in j:
            bad.append((e["num"], j[:60]))
    assert not bad, (
        f"{len(bad)} entries use non-canonical 'Synthesis' spelling: {bad[:5]}"
    )
