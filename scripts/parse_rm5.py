#!/usr/bin/env python3
"""
parse_rm5.py -- RevMan (.rm5) parser for the HFrEF union-ledger lane.

Extracts BOTH halves of a RevMan export:
  1. ANALYSES_AND_DATA -> per-study per-arm outcome cells (dichotomous + continuous)
  2. STUDIES + CHARACTERISTICS_OF_INCLUDED_STUDIES -> trial characteristics

Design constraints this parser encodes (each traces to a recorded incident):

* OUTCOME NAMES ARE READ, NEVER INFERRED.  A prior lane took a figure for
  all-cause mortality that was in fact total hospitalisations -- right trials,
  perfect arithmetic, wrong endpoint.  Every emitted cell carries the
  comparison name, outcome name and both group labels VERBATIM.  If an outcome
  has no readable name the cell is emitted with outcome_name=None and flagged
  UNNAMED-OUTCOME rather than being given a name from its position.

* DUAL DIALECT.  RevMan writes outcome/comparison names as a CHILD <NAME>
  element in genuine Cochrane exports, but some tooling emits a NAME attribute
  instead.  Reading only the attribute yields BLANK outcome names on real
  Cochrane files -- silently, and precisely on the files that matter.  We read
  the child element first and fall back to the attribute.

* Tag aliases: CONT_DATA/CONT_OUTCOME (Cochrane) vs
  CONTINUOUS_DATA/CONTINUOUS_OUTCOME (other emitters); arm denominators are
  TOTAL_1/TOTAL_2 in the former and N_1/N_2 in the latter.

* STUDY_ID values are XML-name-escaped (STD-MRC_x002d_1 == "MRC-1").  Left
  undecoded these will not join to anything.

* Study IDs are RevMan-local labels ("Author Year"), NOT trial identities.
  Every emitted record carries resolution_status=UNRESOLVED.  A sibling lane
  mistook "Lewis 1989" for Lewis 2022 -- forty years apart, same surname.
  Resolution is a separate, evidenced step; this parser never guesses.

Nothing here merges into a ledger.  Output is staged as PROPOSED.

Usage:
    python parse_rm5.py <file.rm5> [more.rm5 ...] --out staged.jsonl
    python parse_rm5.py --selftest
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SCHEMA = "rm5-parse/v1"

# Tag aliases across RevMan emitter dialects.
CONT_OUTCOME_TAGS = ("CONT_OUTCOME", "CONTINUOUS_OUTCOME")
CONT_DATA_TAGS = ("CONT_DATA", "CONTINUOUS_DATA")
DICH_SUBGROUP_TAGS = ("DICH_SUBGROUP",)
CONT_SUBGROUP_TAGS = ("CONT_SUBGROUP", "CONTINUOUS_SUBGROUP")

_XML_ESC = re.compile(r"_x([0-9A-Fa-f]{4})_")


def unescape_id(raw: str | None) -> str | None:
    """Decode RevMan's _xNNNN_ XML-name escaping. STD-MRC_x002d_1 -> MRC-1."""
    if raw is None:
        return None
    s = _XML_ESC.sub(lambda m: chr(int(m.group(1), 16)), raw)
    if s.startswith("STD-"):
        s = s[4:]
    return s.strip() or None


def _text(el) -> str | None:
    if el is None:
        return None
    s = "".join(el.itertext()).strip()
    return s or None


def name_of(el) -> str | None:
    """Read a NAME from the child element first, then the attribute.

    Child-element-first is load-bearing: genuine Cochrane exports have no NAME
    attribute at all, so an attribute-only read returns None for every outcome.
    """
    if el is None:
        return None
    child = _text(el.find("NAME"))
    if child:
        return child
    attr = (el.attrib.get("NAME") or "").strip()
    return attr or None


def _int(v):
    """Parse an integer field. Returns None on blank/absent/non-numeric."""
    if v is None:
        return None
    v = str(v).strip()
    if not v:
        return None
    try:
        return int(float(v))
    except ValueError:
        return None


def _num(v):
    if v is None:
        return None
    v = str(v).strip()
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def _hash(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()[:16]


def _find_first(root, tags):
    for t in tags:
        for el in root.iter(t):
            yield el


# --------------------------------------------------------------------------
# characteristics
# --------------------------------------------------------------------------

CHAR_FIELDS = (
    "CHAR_METHODS",
    "CHAR_PARTICIPANTS",
    "CHAR_INTERVENTIONS",
    "CHAR_OUTCOMES",
    "CHAR_NOTES",
)

# Follow-up phrasings seen in RevMan characteristics prose. Extraction is
# SUGGESTIVE ONLY -- emitted as *_extracted with the source string retained so
# a human can confirm. Never treated as an authoritative field.
_FOLLOWUP_RE = re.compile(
    r"(?:follow(?:ed)?[\s-]?up|duration|treated for|over)\D{0,25}?"
    r"(\d+(?:\.\d+)?)\s*(week|month|year|day)s?",
    re.I,
)
_PHASE_RE = re.compile(r"\bphase\s*(I{1,3}V?|IV|[1-4])\b", re.I)


def parse_characteristics(root) -> dict:
    """Map study_id -> characteristics dict from STUDY + INCLUDED_CHAR."""
    chars: dict[str, dict] = {}

    for st in root.iter("STUDY"):
        sid = unescape_id(st.attrib.get("ID"))
        if not sid:
            continue
        year = st.attrib.get("YEAR") or st.attrib.get("YEAR_OF_PUB")
        chars[sid] = {
            "study_id": sid,
            "study_name": (st.attrib.get("NAME") or "").strip() or None,
            "year_of_pub": _int(year),
            "data_source": st.attrib.get("DATA_SOURCE"),
            "characteristics_present": False,
        }

    for ic in root.iter("INCLUDED_CHAR"):
        sid = unescape_id(ic.attrib.get("STUDY_ID"))
        if not sid:
            continue
        rec = chars.setdefault(sid, {"study_id": sid, "study_name": None,
                                     "year_of_pub": None, "data_source": None})
        blob_parts = []
        for f in CHAR_FIELDS:
            val = _text(ic.find(f))
            rec[f.lower()] = val
            if val:
                blob_parts.append(val)
        blob = " ".join(blob_parts)
        rec["characteristics_present"] = bool(blob)

        # Suggestive-only derivations. Retain the evidence string.
        fu = _FOLLOWUP_RE.search(blob) if blob else None
        rec["followup_extracted"] = (
            {"value": _num(fu.group(1)), "unit": fu.group(2).lower(),
             "evidence": fu.group(0).strip(), "confidence": "SUGGESTIVE-ONLY"}
            if fu else None
        )
        ph = _PHASE_RE.search(blob) if blob else None
        rec["phase_extracted"] = (
            {"value": ph.group(1).upper(), "evidence": ph.group(0).strip(),
             "confidence": "SUGGESTIVE-ONLY"} if ph else None
        )

    return chars


# --------------------------------------------------------------------------
# outcome cells
# --------------------------------------------------------------------------

def _walk_data(outcome_el, data_tags, subgroup_tags):
    """Yield (data_el, subgroup_name). Handles optional subgroup nesting."""
    sub_tagset = set(subgroup_tags)
    for sg in outcome_el:
        if sg.tag in sub_tagset:
            sg_name = name_of(sg)
            for t in data_tags:
                for d in sg.iter(t):
                    yield d, sg_name
    # data sitting directly under the outcome (no subgroup)
    for t in data_tags:
        for d in outcome_el.findall(t):
            yield d, None


def parse_analyses(root, review_id: str, source_file: str) -> list[dict]:
    cells: list[dict] = []

    for comp in root.iter("COMPARISON"):
        comp_name = name_of(comp)
        comp_id = comp.attrib.get("ID")

        # --- dichotomous ---
        for out in comp.iter("DICH_OUTCOME"):
            o_name = name_of(out)
            for d, sg_name in _walk_data(out, ("DICH_DATA",), DICH_SUBGROUP_TAGS):
                sid = unescape_id(d.attrib.get("STUDY_ID"))
                e1, t1 = _int(d.attrib.get("EVENTS_1")), _int(d.attrib.get("TOTAL_1"))
                e2, t2 = _int(d.attrib.get("EVENTS_2")), _int(d.attrib.get("TOTAL_2"))
                flags = []
                if not o_name:
                    flags.append("UNNAMED-OUTCOME")
                # matn reconciliation: events cannot exceed the arm denominator
                for lbl, e, t in (("arm1", e1, t1), ("arm2", e2, t2)):
                    if e is not None and t is not None and e > t:
                        flags.append(f"MATN-VIOLATION-{lbl}-events>{t}")
                    if t is not None and t <= 0:
                        flags.append(f"NONPOSITIVE-DENOMINATOR-{lbl}")
                if None in (e1, t1, e2, t2):
                    flags.append("INCOMPLETE-CELL")
                total_events = None
                if e1 is not None and e2 is not None:
                    total_events = e1 + e2
                    if total_events <= 2:
                        flags.append("ARITHMETICALLY-INERT-events<=2")

                cell = {
                    "schema": SCHEMA,
                    "record_type": "OUTCOME_CELL",
                    "review_id": review_id,
                    "source_file": source_file,
                    "comparison_id": comp_id,
                    "comparison_name": comp_name,
                    "outcome_id": out.attrib.get("ID"),
                    "outcome_name": o_name,          # verbatim, never inferred
                    "outcome_type": "DICHOTOMOUS",
                    "subgroup_name": sg_name,
                    "effect_measure": out.attrib.get("EFFECT_MEASURE"),
                    "group_label_1": _text(out.find("GROUP_LABEL_1"))
                                     or out.attrib.get("GROUP_LABEL_1"),
                    "group_label_2": _text(out.find("GROUP_LABEL_2"))
                                     or out.attrib.get("GROUP_LABEL_2"),
                    "study_id": sid,
                    "study_id_raw": d.attrib.get("STUDY_ID"),
                    "events_1": e1, "total_1": t1,
                    "events_2": e2, "total_2": t2,
                    "total_events_both_arms": total_events,
                    "randomised_n_both_arms": (t1 + t2) if None not in (t1, t2) else None,
                    "extraction_method": "RM5-XML-DIRECT",
                    "epistemic_status": "PROPOSED",
                    "resolution_status": "UNRESOLVED",
                    "second_family_witness": "NOT-ATTEMPTED",
                    "flags": flags,
                }
                cell["representation_hash"] = _hash(cell)
                cells.append(cell)

        # --- continuous ---
        for tag in CONT_OUTCOME_TAGS:
            for out in comp.iter(tag):
                o_name = name_of(out)
                for d, sg_name in _walk_data(out, CONT_DATA_TAGS, CONT_SUBGROUP_TAGS):
                    sid = unescape_id(d.attrib.get("STUDY_ID"))
                    a = d.attrib
                    n1 = _int(a.get("TOTAL_1") or a.get("N_1"))
                    n2 = _int(a.get("TOTAL_2") or a.get("N_2"))
                    flags = [] if o_name else ["UNNAMED-OUTCOME"]
                    cell = {
                        "schema": SCHEMA,
                        "record_type": "OUTCOME_CELL",
                        "review_id": review_id,
                        "source_file": source_file,
                        "comparison_id": comp_id,
                        "comparison_name": comp_name,
                        "outcome_id": out.attrib.get("ID"),
                        "outcome_name": o_name,
                        "outcome_type": "CONTINUOUS",
                        "subgroup_name": sg_name,
                        "effect_measure": out.attrib.get("EFFECT_MEASURE"),
                        "group_label_1": _text(out.find("GROUP_LABEL_1"))
                                         or out.attrib.get("GROUP_LABEL_1"),
                        "group_label_2": _text(out.find("GROUP_LABEL_2"))
                                         or out.attrib.get("GROUP_LABEL_2"),
                        "study_id": sid,
                        "study_id_raw": a.get("STUDY_ID"),
                        "n_1": n1, "mean_1": _num(a.get("MEAN_1")), "sd_1": _num(a.get("SD_1")),
                        "n_2": n2, "mean_2": _num(a.get("MEAN_2")), "sd_2": _num(a.get("SD_2")),
                        "randomised_n_both_arms": (n1 + n2) if None not in (n1, n2) else None,
                        "extraction_method": "RM5-XML-DIRECT",
                        "epistemic_status": "PROPOSED",
                        "resolution_status": "UNRESOLVED",
                        "second_family_witness": "NOT-ATTEMPTED",
                        "flags": flags,
                    }
                    cell["representation_hash"] = _hash(cell)
                    cells.append(cell)

    return cells


def parse_file(path: Path) -> dict:
    root = ET.parse(path).getroot()
    review_id = (root.attrib.get("ID")
                 or _text(root.find("COVER_SHEET/TITLE"))
                 or path.stem)
    cells = parse_analyses(root, review_id, path.name)
    chars = parse_characteristics(root)

    for sid, c in chars.items():
        c.update({
            "schema": SCHEMA,
            "record_type": "TRIAL_CHARACTERISTICS",
            "review_id": review_id,
            "source_file": path.name,
            "epistemic_status": "PROPOSED",
            "resolution_status": "UNRESOLVED",
        })

    # Cross-link: total events on each named outcome, per study.
    cells_by_study: dict[str, list] = {}
    for c in cells:
        if c.get("study_id"):
            cells_by_study.setdefault(c["study_id"], []).append(c)
    for sid, c in chars.items():
        mine = cells_by_study.get(sid, [])
        c["outcomes_with_data"] = sorted(
            {x["outcome_name"] for x in mine if x.get("outcome_name")}
        )
        c["n_cells"] = len(mine)
        c["randomised_n_from_data"] = next(
            (x["randomised_n_both_arms"] for x in mine
             if x.get("randomised_n_both_arms")), None
        )

    orphan_cells = sorted({c["study_id"] for c in cells
                           if c.get("study_id") and c["study_id"] not in chars})

    return {
        "review_id": review_id,
        "source_file": path.name,
        "cells": cells,
        "characteristics": list(chars.values()),
        "summary": {
            "n_cells": len(cells),
            "n_dich": sum(1 for c in cells if c["outcome_type"] == "DICHOTOMOUS"),
            "n_cont": sum(1 for c in cells if c["outcome_type"] == "CONTINUOUS"),
            "n_studies_char": len(chars),
            "distinct_outcomes": sorted({c["outcome_name"] for c in cells
                                         if c.get("outcome_name")}),
            "unnamed_outcome_cells": sum(1 for c in cells
                                         if "UNNAMED-OUTCOME" in c["flags"]),
            "matn_violations": [c["representation_hash"] for c in cells
                                if any(f.startswith("MATN-VIOLATION")
                                       for f in c["flags"])],
            "inert_cells": sum(1 for c in cells
                               if any("INERT" in f for f in c["flags"])),
            "orphan_study_ids": orphan_cells,
        },
    }


# --------------------------------------------------------------------------

def _selftest_fixtures():
    """Locate .rm5 fixtures without hardcoding anyone's home directory.

    Two absolute developer paths used to be literals here. They break on every
    other machine, and one of them embedded the developer's Windows username in
    what is a PUBLIC repository. Resolution order:

      1. RM5_FIXTURES         - os.pathsep-separated .rm5 files and/or dirs
      2. R_LIBS_USER / R_LIBS - the R `meta` package ships extdata/Fleiss1993.rm5
      3. tests/fixtures/revman/ under this repo, plus ALLMETA_ROOT when set

    Returns only files that exist, in order, de-duplicated.
    """
    out = []
    seen = set()

    def add(p):
        try:
            rp = p.resolve()
            if rp in seen or rp.suffix.lower() != ".rm5" or not rp.is_file():
                return
        except OSError:
            return
        seen.add(rp)
        out.append(rp)

    def add_tree(d):
        try:
            if not d.is_dir():
                return
            for p in sorted(d.rglob("*.rm5")):
                add(p)
        except OSError:
            return

    for token in os.environ.get("RM5_FIXTURES", "").split(os.pathsep):
        token = token.strip()
        if not token:
            continue
        p = Path(token)
        if p.is_dir():
            add_tree(p)
        else:
            add(p)

    for var in ("R_LIBS_USER", "R_LIBS"):
        for token in os.environ.get(var, "").split(os.pathsep):
            token = token.strip()
            if token:
                add(Path(token) / "meta" / "extdata" / "Fleiss1993.rm5")

    repo_root = Path(__file__).resolve().parent.parent
    add_tree(repo_root / "tests" / "fixtures" / "revman")
    allmeta = os.environ.get("ALLMETA_ROOT", "").strip()
    if allmeta:
        add_tree(Path(allmeta) / "tests" / "fixtures" / "revman")

    return out


def selftest() -> int:
    """Parse every discoverable .rm5 fixture (both dialects).

    Fails CLOSED. The previous version hardcoded two absolute paths, printed
    "SKIP (absent)" for each one that did not exist, and then printed
    SELFTEST PASS and returned 0 -- a pass that had parsed nothing. Not
    assessable is not a pass.
    """
    fixtures = _selftest_fixtures()
    print(f"fixtures resolved: {len(fixtures)}")
    for f in fixtures:
        print(f"  {f}")
    if not fixtures:
        print(
            "NOT ASSESSABLE: no .rm5 fixture resolved, so nothing was parsed. "
            "Set RM5_FIXTURES to one or more .rm5 files or directories "
            "(os.pathsep-separated), or R_LIBS_USER to an R library that "
            "contains meta/extdata/Fleiss1993.rm5.",
            file=sys.stderr,
        )
        return 2
    failures = []
    for f in fixtures:
        if not f.exists():
            print(f"SKIP (absent): {f}")
            continue
        r = parse_file(f)
        s = r["summary"]
        print(f"\n=== {f.name} [{r['review_id'][:60]}]")
        print(f"  cells={s['n_cells']} (dich={s['n_dich']} cont={s['n_cont']}) "
              f"studies={s['n_studies_char']}")
        print(f"  outcomes: {s['distinct_outcomes']}")
        print(f"  unnamed={s['unnamed_outcome_cells']} "
              f"matn_violations={len(s['matn_violations'])} inert={s['inert_cells']}")
        if s["orphan_study_ids"]:
            print(f"  orphan study_ids: {s['orphan_study_ids']}")

        if s["n_cells"] == 0:
            failures.append(f"{f.name}: parsed zero cells")
        # The load-bearing assertion: every cell must carry a read outcome name.
        if s["unnamed_outcome_cells"]:
            failures.append(f"{f.name}: {s['unnamed_outcome_cells']} cells lack an "
                            f"outcome name -- endpoint-substitution risk")
        if s["matn_violations"]:
            failures.append(f"{f.name}: matn violations {s['matn_violations']}")
        # ID unescaping must have worked.
        raw = [c["study_id_raw"] for c in r["cells"] if c.get("study_id_raw")]
        if any("_x" in (x or "") for x in raw):
            got = [c["study_id"] for c in r["cells"] if "_x" in (c["study_id_raw"] or "")]
            if any("_x" in (g or "") for g in got):
                failures.append(f"{f.name}: STUDY_ID escaping not decoded")

    print()
    if failures:
        for x in failures:
            print("FAIL:", x)
        return 1
    print("SELFTEST PASS -- both dialects parsed, all outcomes named, matn clean.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", type=Path)
    ap.add_argument("--out", type=Path, help="write staged PROPOSED jsonl here")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.files:
        ap.error("give at least one .rm5, or --selftest")

    staged, reports = [], []
    for f in args.files:
        if not f.exists():
            print(f"MISSING: {f}", file=sys.stderr)
            return 2
        r = parse_file(f)
        staged.extend(r["cells"])
        staged.extend(r["characteristics"])
        reports.append(r["summary"] | {"review_id": r["review_id"],
                                       "source_file": r["source_file"]})

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            for rec in staged:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        print(f"staged {len(staged)} PROPOSED records -> {args.out}")

    print(json.dumps(reports, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
