"""Phase-2b L1 — scan rewrite-workbook.txt for claim_language WARN firings,
classify each as likely-descriptive | likely-causal | uncertain, and either
emit a triage markdown (default) or apply the descriptive overrides.

Why: the claim_language Sentinel rule currently fires ~2788 WARNs against
the live workbook because words like 'confirmed' / 'eliminates' have
legitimate descriptive uses ('confirmed cases', 'eliminates wrangling').
This script lets the operator inject `# sentinel:claim-language-allow`
markers into the genuinely-descriptive entries en masse so the rule can
be re-promoted from WARN to BLOCK in a future commit.

Classification heuristic (pattern-based, no LLM):
  likely-descriptive — word appears in a phrase from a curated whitelist
    (e.g. "confirmed cases", "rule out", "eliminates the need for", "safe
    and well-tolerated", "drug-eluting", "well-established").
  likely-causal — word is the active verb of an evidence claim (subject
    or object is "evidence" / "data" / "trial" / "study" / "review", or
    word is followed by "the/that/this/our").
  uncertain — neither pattern fires confidently → human review needed.

Usage:
  python scripts/propose_claim_overrides.py                # write triage MD
  python scripts/propose_claim_overrides.py --apply        # apply markers
  python scripts/propose_claim_overrides.py --report-only  # stats, no MD
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

if sys.platform == "win32" and "pytest" not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")


E156 = Path(__file__).resolve().parents[1]
WORKBOOK = E156 / "rewrite-workbook.txt"
TRIAGE_MD = E156 / "claim_language_overrides.md"
APPLIED_JSON = E156 / ".claim-overrides-applied.json"
OVERRIDE_MARKER = "# sentinel:claim-language-allow"
SEP = "=" * 70

# Words this script considers (same set as the Sentinel rule)
TARGET_WORDS_RE = re.compile(
    r"\b(prov(?:es|en)|confirm(?:s|ed)|eliminat(?:es|ed)|"
    r"definitiv(?:e|ely)|undeniably|conclusively|"
    r"safe|effective|cures|prevents?)\b",
    re.IGNORECASE,
)

# Analysis-method tokens. When ANY of these appears within 60 chars BEFORE
# the target word (decoupled — no requirement to be adjacent), the usage is
# treated as descriptive reporting of an analysis result, not a causal claim.
ANALYSIS_METHOD_TOKEN_RE = re.compile(
    r"\b(?:sensitivity\s+analys[ei]s|leave-one-out|leave-out|leave-one-design-out|"
    r"validation|cross-?validation|robust\s+variance|holdout|held-out|"
    r"specification\s+check|robustness\s+check|jackknife|bootstrap|"
    r"permutation|bayesian\s+(?:check|model)|posterior\s+predictive|"
    r"selenium\s+test(?:s|ing)?|lighthouse\s+(?:testing|score)|regression\s+test|"
    r"unit\s+test(?:s|ing)?|smoke\s+test|reproducibility\s+test|metafor|"
    r"simulation(?:s)?|benchmark(?:s|ing)?|sanity\s+check|cross-?check|"
    r"sensitivity\s+re-?run|stability\s+(?:check|analys[ei]s)|"
    r"replication(?:s)?|monte\s+carlo)\b",
    re.IGNORECASE,
)

# Subjects of a "confirmed/showed" verb that indicate descriptive reporting.
# Look BEHIND the target word for these.
DESCRIPTIVE_SUBJECT_RE = re.compile(
    r"\b(?:analys[ei]s|analyses|test(?:s|ing)?|validation|score|score\s+of|"
    r"correlation|consistency|reproduc[ei]bility|"
    r"sensitivity|stability|directional\s+accuracy|model\s+stability|"
    r"convergence|cross-validation|rerun|re-run)\b",
    re.IGNORECASE,
)

# Phrases that mark a usage as descriptive (operator can safely WHITELIST).
# Pattern matched against 60-char window around the target word.
DESCRIPTIVE_PHRASES_RE = re.compile(
    r"\b(confirmed\s+cases?|confirmed\s+diagnos[ei]s|confirmed\s+positive|"
    r"confirmed\s+(?:dead|deaths?|infections?|outcome|by)|"
    r"(?:radiographically|histologically|laboratory|microbiologically|"
    r"genetically|biopsy)[-\s]confirmed|"
    r"confirmed\s+by|confirmation\s+of|to\s+be\s+confirmed|"
    r"rule\s+out|ruled\s+out|"
    r"eliminat(?:es|ed|ion)\s+(?:of\s+)?(?:the\s+need|repetitive|wrangling|"
    r"manual|chore|step|requirement|barrier|gap|drudgery|guesswork|noise|"
    r"redundancy|duplication|burden|the\s+gap|the\s+need|the\s+barrier)|"
    r"eliminat(?:es|ed|ion)\s+(?:from|by|via|across)|"
    r"safe\s+(?:and\s+(?:well-tolerated|effective|feasible)|"
    r"in\s+the\s+context|to\s+(?:use|apply|deploy|run|interpret)|"
    r"defaults?|conservative|operator|harbour)|"
    r"safety\s+(?:profile|signal|monitoring|outcome|endpoint|review|alert|"
    r"benefit|trade-off|margin|net)|"
    r"safety\s+(?:data|run|set|review)|"
    r"prevents?\s+(?:re-)?(?:infection|disease|fracture|stroke|death|"
    r"recurrence|relapse|hospitalisation|hospitalization|progression|"
    r"this|that|operators?|drift|the|inconsistency|the\s+rule|the\s+bug)|"
    r"prevents?\s+future|"
    r"well-established|cost-effective|effective\s+(?:against|across|in\s+|number|"
    r"sample|coverage|reproducibility)|"
    r"drug-eluting|effective\s+number\s+of|"
    r"definitive\s+(?:diagnos[ei]s|test|imaging|scan|outcome|guideline)|"
    r"prevention\s+of|public\s+health|"
    r"safe\s*\(\s*no\s+|\bsafely\s+(?:bypass|skip|drop|delete|merge)|"
    r"\bso\s+safe\b|"
    r"effective(?:ness)?\s+(?:rate|comparison|study|review|measure|estimator))\b",
    re.IGNORECASE,
)

# Causal-claim patterns (operator should rewrite the sentence, not whitelist).
# Match the target word as the verb of an evidence claim.
CAUSAL_CONTEXT_RE = re.compile(
    r"(?:evidence|data|results?|trial|study|review|analysis|meta-analysis|"
    r"finding|outcome|comparison)\s+(?:that\s+)?"
    r"(?:prov(?:es|en)|confirm(?:s|ed)|eliminat(?:es|ed)|"
    r"definitiv(?:e|ely)|conclusively)",
    re.IGNORECASE,
)


def _classify_entry_body(body: str) -> str:
    """Returns one of: likely-descriptive | likely-causal | uncertain | clean."""
    hits = list(TARGET_WORDS_RE.finditer(body))
    if not hits:
        return "clean"

    has_descriptive = False
    has_causal = False
    for h in hits:
        window_start = max(0, h.start() - 80)
        window_end = min(len(body), h.end() + 60)
        window = body[window_start:window_end]
        # Behind-only window (subject context)
        behind = body[window_start:h.start()]
        if DESCRIPTIVE_PHRASES_RE.search(window):
            has_descriptive = True
        # Analysis-method token anywhere within 80 chars before the target
        if ANALYSIS_METHOD_TOKEN_RE.search(behind):
            has_descriptive = True
        # Descriptive-subject token immediately preceding the verb
        if DESCRIPTIVE_SUBJECT_RE.search(behind):
            has_descriptive = True
        if CAUSAL_CONTEXT_RE.search(window):
            has_causal = True

    if has_descriptive and not has_causal:
        return "likely-descriptive"
    if has_causal and not has_descriptive:
        return "likely-causal"
    if has_descriptive and has_causal:
        return "uncertain"
    # Has target word but neither context matched
    return "uncertain"


def _iter_blocks():
    text = WORKBOOK.read_text(encoding="utf-8")
    blocks = text.split(SEP)
    cursor = 0
    for blk in blocks:
        offset = cursor
        cursor += len(blk) + len(SEP)
        m = re.search(r"^\[(\d+)/\d+\]\s+(.+?)$", blk, re.MULTILINE)
        if not m:
            continue
        # Skip entries that already have the override marker
        if OVERRIDE_MARKER in blk:
            yield {"num": int(m.group(1)), "name": m.group(2).strip(),
                   "block": blk, "offset": offset, "already_marked": True,
                   "classification": "skip-already-marked"}
            continue
        # Extract body if any
        body_m = re.search(
            r"^CURRENT BODY[^\n]*\n(.*?)(?=\n\nYOUR REWRITE|\n\nSUBMISSION|\n=)",
            blk, re.MULTILINE | re.DOTALL,
        )
        body = body_m.group(1) if body_m else ""
        cls = _classify_entry_body(body)
        yield {"num": int(m.group(1)), "name": m.group(2).strip(),
               "block": blk, "offset": offset, "already_marked": False,
               "classification": cls, "body": body}


def emit_triage(entries: list[dict]) -> str:
    """Markdown triage report for operator review."""
    by_class: dict[str, list[dict]] = {}
    for e in entries:
        by_class.setdefault(e["classification"], []).append(e)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")

    lines = [
        f"# claim_language override triage — {now}",
        "",
        f"_Scanned `{WORKBOOK.name}` for entries that would trigger the "
        f"P0-claim-language-workbook Sentinel rule. Classified each by simple "
        f"pattern matching; operator decides which to whitelist via_ "
        f"`{OVERRIDE_MARKER}` _markers._",
        "",
    ]
    counts = Counter(e["classification"] for e in entries)
    lines.append("## Counts\n")
    for k in ("clean", "likely-descriptive", "likely-causal", "uncertain",
              "skip-already-marked"):
        lines.append(f"- **{k}**: {counts.get(k, 0)}")
    lines.append("")

    for cls_name, cls_label, action in [
        ("likely-descriptive",
         "## Likely descriptive (auto-whitelist safe)",
         f"Run `python scripts/propose_claim_overrides.py --apply` to inject "
         f"`{OVERRIDE_MARKER}` into each of these entries."),
        ("likely-causal",
         "## Likely causal (human rewrite required)",
         "These contain an overclaim word used as the verb of an evidence claim. "
         "Rewrite the sentence (e.g. 'proves' → 'is consistent with'). "
         "Do NOT auto-whitelist — the override would silence a real signal."),
        ("uncertain",
         "## Uncertain (human review required)",
         "Pattern matches both descriptive and causal contexts, or neither "
         "matched. Open the entry, decide whether to whitelist or rewrite."),
    ]:
        items = by_class.get(cls_name, [])
        lines.append(f"\n{cls_label} ({len(items)})\n")
        lines.append(f"_Action_: {action}\n")
        if items:
            lines.append("| # | name |")
            lines.append("|---|------|")
            for e in items[:300]:
                lines.append(f"| {e['num']} | {e['name']} |")
            if len(items) > 300:
                lines.append(f"| _... and {len(items) - 300} more_ | |")

    return "\n".join(lines) + "\n"


def apply_descriptive_overrides(entries: list[dict]) -> tuple[int, list[int]]:
    """Insert the override marker just below the [N/T] header line for every
    likely-descriptive entry. Returns (count, list of applied entry-nums).

    Idempotent: skips entries that already have the marker.
    """
    text = WORKBOOK.read_text(encoding="utf-8")
    blocks = text.split(SEP)
    applied: list[int] = []

    # Build a {num: classification} lookup
    target_nums = {e["num"] for e in entries
                   if e["classification"] == "likely-descriptive"
                   and not e["already_marked"]}
    if not target_nums:
        return 0, []

    new_blocks: list[str] = []
    for blk in blocks:
        m = re.search(r"^(\[\d+/\d+\][^\n]*\n)", blk, re.MULTILINE)
        if not m:
            new_blocks.append(blk)
            continue
        num_m = re.match(r"\[(\d+)/", m.group(1))
        if not num_m:
            new_blocks.append(blk)
            continue
        num = int(num_m.group(1))
        if num not in target_nums:
            new_blocks.append(blk)
            continue
        if OVERRIDE_MARKER in blk:
            new_blocks.append(blk)
            continue
        # Insert marker right after the [N/T] header line
        header_end = m.end()
        new_blk = blk[:header_end] + OVERRIDE_MARKER + "\n" + blk[header_end:]
        new_blocks.append(new_blk)
        applied.append(num)

    if applied:
        WORKBOOK.write_text(SEP.join(new_blocks), encoding="utf-8")
        APPLIED_JSON.write_text(
            json.dumps({"applied_at": datetime.now(timezone.utc).isoformat(),
                        "count": len(applied), "nums": sorted(applied)},
                       indent=2),
            encoding="utf-8",
        )
    return len(applied), applied


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="apply the override markers (default: just emit triage MD)")
    ap.add_argument("--report-only", action="store_true",
                    help="just print stats; don't write the MD")
    args = ap.parse_args(argv)

    if not WORKBOOK.is_file():
        sys.stderr.write(f"Workbook not found: {WORKBOOK}\n")
        return 1

    entries = list(_iter_blocks())
    counts = Counter(e["classification"] for e in entries)
    print(f"Scanned {len(entries)} workbook entries:")
    for k in ("clean", "likely-descriptive", "likely-causal", "uncertain",
              "skip-already-marked"):
        print(f"  {k:25s} {counts.get(k, 0)}")

    if args.report_only:
        return 0

    if args.apply:
        n, nums = apply_descriptive_overrides(entries)
        print(f"\nApplied {OVERRIDE_MARKER} to {n} entries.")
        if n:
            print(f"Affected entry numbers (first 20): {nums[:20]}")
            print(f"Audit: {APPLIED_JSON}")
        return 0

    md = emit_triage(entries)
    TRIAGE_MD.write_text(md, encoding="utf-8")
    print(f"\nWrote triage MD: {TRIAGE_MD}")
    print("Review and then run with --apply to inject markers for the "
          "likely-descriptive set.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
