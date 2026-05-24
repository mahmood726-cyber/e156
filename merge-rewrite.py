#!/usr/bin/env python3
r"""Assemble edited YOUR REWRITE blocks from rewrite-PHONE-*.md back into a
new workbook file. Never touches the original rewrite-workbook.txt.

Reads:
  C:\E156\rewrite-PHONE-001.md .. rewrite-PHONE-019.md
  C:\E156\rewrite-workbook.txt   (original, read-only)

Writes:
  C:\E156\rewrite-workbook.NEW.txt
  C:\E156\merge-report.md

Run: python C:\E156\merge-rewrite.py
"""
from __future__ import annotations
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(r"C:\E156")
WORKBOOK = E156 / "rewrite-workbook.txt"
NEW_WORKBOOK = E156 / "rewrite-workbook.NEW.txt"
REPORT = E156 / "merge-report.md"

ENTRY_RE = re.compile(r"^\[(\d+)/921\]\s*(.*)$")
REWRITE_RE = re.compile(r"^YOUR REWRITE\b.*?:\s*$")
END_MARKERS = ("SUBMISSION METADATA", "SUBMITTED:", "==========")
CHUNK_ENTRY_RE = re.compile(r"^## Entry (\d+) \(\[(\d+)/921\]\) — (.*)$")
BEGIN_RW = "<!-- BEGIN-REWRITE -->"
END_RW = "<!-- END-REWRITE -->"


def load_chunk_rewrites() -> dict[int, str]:
    """Return {ordinal_position -> rewrite_text} extracted from rewrite-PHONE-NNN.md files."""
    rewrites: dict[int, str] = {}
    files = sorted(E156.glob("rewrite-PHONE-*.md"))
    chunk_files = [f for f in files if re.match(r"rewrite-PHONE-\d{3}\.md$", f.name)]
    for cf in chunk_files:
        text = cf.read_text(encoding="utf-8", errors="replace")
        cur_ord: int | None = None
        collecting = False
        buf: list[str] = []
        for raw in text.splitlines(keepends=False):
            entry_m = CHUNK_ENTRY_RE.match(raw)
            if entry_m:
                if cur_ord is not None and collecting is False and buf:
                    rewrites[cur_ord] = "\n".join(buf).strip("\n")
                cur_ord = int(entry_m.group(1))
                collecting = False
                buf = []
                continue
            if raw.strip() == BEGIN_RW:
                collecting = True
                buf = []
                continue
            if raw.strip() == END_RW:
                if cur_ord is not None and collecting:
                    rewrites[cur_ord] = "\n".join(buf).strip("\n")
                collecting = False
                continue
            if collecting:
                buf.append(raw)
    return rewrites


def find_entries(lines: list[str]) -> list[dict]:
    markers = []
    for i, ln in enumerate(lines, 1):
        m = ENTRY_RE.match(ln)
        if m:
            markers.append({"n": int(m.group(1)), "slug": m.group(2).strip(), "start_line": i})
    for idx, mk in enumerate(markers):
        mk["ord"] = idx + 1
        if idx + 1 < len(markers):
            mk["end_line"] = markers[idx + 1]["start_line"] - 1
        else:
            mk["end_line"] = len(lines)
    return markers


def locate_rewrite_block(entry_lines: list[str]) -> tuple[int, int]:
    """Return (rw_body_start_idx, rw_body_end_idx_exclusive) inside entry_lines.
    rw_body_start_idx is the index of the first body line AFTER the YOUR REWRITE header line.
    rw_body_end_idx_exclusive is the index of the first END_MARKERS line (or len).
    Returns (-1, -1) if no YOUR REWRITE header present.
    """
    rw_start = -1
    rw_end = -1
    for i, ln in enumerate(entry_lines):
        if REWRITE_RE.match(ln):
            rw_start = i + 1
        elif rw_start >= 0 and rw_end < 0:
            stripped = ln.strip()
            if any(stripped.startswith(em) for em in END_MARKERS):
                rw_end = i
    if rw_start >= 0 and rw_end < 0:
        rw_end = len(entry_lines)
    return rw_start, rw_end


def main() -> int:
    rewrites = load_chunk_rewrites()
    print(f"Loaded {len(rewrites)} rewrite blocks from rewrite-PHONE-*.md files")

    lines = WORKBOOK.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
    markers = find_entries(lines)
    print(f"Found {len(markers)} entries in original workbook")

    out_lines = list(lines)
    applied = 0
    skipped_empty = 0
    skipped_no_block = 0
    report_rows: list[tuple[int, int, str, int, int, int, int, str]] = []

    for mk in markers:
        ord_pos = mk["ord"]
        entry_slice = lines[mk["start_line"] - 1 : mk["end_line"]]
        rw_start, rw_end = locate_rewrite_block(entry_slice)
        existing = "".join(entry_slice[rw_start:rw_end]).strip("\n") if rw_start >= 0 else ""
        new_rewrite = rewrites.get(ord_pos, "")
        status = "unchanged"
        if rw_start < 0:
            status = "no-rewrite-block-in-source"
            skipped_no_block += 1
        elif not new_rewrite.strip():
            status = "empty-rewrite-skipped"
            skipped_empty += 1
        elif new_rewrite.strip() == existing.strip():
            status = "unchanged"
        else:
            abs_start = mk["start_line"] - 1 + rw_start
            abs_end = mk["start_line"] - 1 + rw_end
            new_block = new_rewrite if new_rewrite.endswith("\n") else new_rewrite + "\n"
            new_block_lines = new_block.splitlines(keepends=True)
            out_lines[abs_start:abs_end] = new_block_lines
            applied += 1
            status = "applied"
            shift = len(new_block_lines) - (rw_end - rw_start)
            if shift != 0:
                for later in markers:
                    if later["ord"] > ord_pos:
                        later["start_line"] += shift
                        later["end_line"] += shift
                lines = out_lines

        report_rows.append(
            (
                ord_pos,
                mk["n"],
                mk["slug"],
                mk["start_line"],
                mk["end_line"],
                len(existing),
                len(new_rewrite),
                status,
            )
        )

    NEW_WORKBOOK.write_text("".join(out_lines), encoding="utf-8")
    print(f"wrote {NEW_WORKBOOK.name} ({NEW_WORKBOOK.stat().st_size:,} bytes)")
    print(f"applied={applied} skipped_empty={skipped_empty} skipped_no_block={skipped_no_block}")

    rep = [
        "# merge-rewrite report\n\n",
        f"Source: `{WORKBOOK.name}` (read-only)  \n",
        f"Output: `{NEW_WORKBOOK.name}`\n\n",
        f"- Entries scanned: {len(markers)}\n",
        f"- Rewrites applied: {applied}\n",
        f"- Empty rewrites skipped: {skipped_empty}\n",
        f"- Entries lacking a YOUR REWRITE block in source: {skipped_no_block}\n\n",
        "| Ord | N | Slug | Line range | Orig len | New len | Status |\n",
        "|----:|--:|:-----|:-----------|---------:|--------:|:-------|\n",
    ]
    for row in report_rows:
        rep.append("| {} | {} | {} | {}-{} | {} | {} | {} |\n".format(*row[:3], row[3], row[4], row[5], row[6], row[7]))
    REPORT.write_text("".join(rep), encoding="utf-8")
    print(f"wrote {REPORT.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
