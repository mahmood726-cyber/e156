#!/usr/bin/env python3
"""Split rewrite-workbook.txt into 19 phone-editable chunks + header + index.

Reads C:\\E156\\rewrite-workbook.txt (read-only).
Writes rewrite-PHONE-000-HEADER.md, rewrite-PHONE-NNN.md (001-019),
rewrite-PHONE-INDEX.md, merge-rewrite.py, HOW-TO-USE.md.

Run: python C:\\E156\\split_for_phone.py
"""
from __future__ import annotations
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

E156 = Path(r"C:\E156")
WORKBOOK = E156 / "rewrite-workbook.txt"
CHUNK_SIZE = 50

ENTRY_RE = re.compile(r"^\[(\d+)/921\]\s*(.*)$")
CURRENT_RE = re.compile(r"^CURRENT BODY\b.*?:\s*$")
REWRITE_RE = re.compile(r"^YOUR REWRITE\b.*?:\s*$")
END_MARKERS = ("SUBMISSION METADATA", "SUBMITTED:", "==========")


def load_lines() -> list[str]:
    return WORKBOOK.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)


def find_entries(lines: list[str]) -> list[dict]:
    """Return list of {n, slug, start_line, end_line} for each [N/921] marker.
    Lines are 1-indexed. end_line is inclusive (last line of this entry).
    """
    markers = []
    for i, ln in enumerate(lines, 1):
        m = ENTRY_RE.match(ln)
        if m:
            markers.append({"n": int(m.group(1)), "slug": m.group(2).strip(), "start_line": i})
    for idx, mk in enumerate(markers):
        if idx + 1 < len(markers):
            mk["end_line"] = markers[idx + 1]["start_line"] - 1
        else:
            mk["end_line"] = len(lines)
    return markers


def parse_sections(entry_lines: list[str]) -> dict:
    """Within one entry's lines, locate CURRENT BODY block, YOUR REWRITE block.
    Returns dict with current_body (str), your_rewrite (str), metadata (str: header lines before CURRENT BODY).
    """
    cur_start = cur_end = rw_start = rw_end = -1
    for i, ln in enumerate(entry_lines):
        if CURRENT_RE.match(ln):
            cur_start = i + 1
        elif REWRITE_RE.match(ln):
            if cur_start >= 0 and cur_end < 0:
                cur_end = i
            rw_start = i + 1
        elif rw_start >= 0 and rw_end < 0:
            stripped = ln.strip()
            if any(stripped.startswith(em) for em in END_MARKERS):
                rw_end = i
    if cur_start >= 0 and cur_end < 0:
        cur_end = rw_start if rw_start > 0 else len(entry_lines)
    if rw_start >= 0 and rw_end < 0:
        rw_end = len(entry_lines)

    metadata = "".join(entry_lines[1: cur_start - 1]) if cur_start > 0 else ""
    current_body = "".join(entry_lines[cur_start:cur_end]).strip("\n") if cur_start >= 0 else ""
    your_rewrite = "".join(entry_lines[rw_start:rw_end]).strip("\n") if rw_start >= 0 else ""
    return {
        "metadata": metadata.rstrip(),
        "current_body": current_body,
        "your_rewrite": your_rewrite,
    }


def chunk_label(idx: int) -> str:
    return f"{idx:03d}"


def write_header_chunk(lines: list[str]) -> None:
    """Write rewrite-PHONE-000-HEADER.md: lines 1-92 of the original."""
    header_lines = lines[:92]
    out = E156 / "rewrite-PHONE-000-HEADER.md"
    body = "".join(header_lines)
    md = (
        "# Workbook header (frozen reference — do not edit)\n\n"
        "_Index: rewrite-PHONE-INDEX.md | Next: rewrite-PHONE-001.md_\n\n"
        "This is the original workbook header (lines 1-92). It contains submission\n"
        "instructions and authorship rules. Read it before rewriting any entry.\n"
        "Editing this file has no effect on the merge — only YOUR REWRITE blocks\n"
        "in rewrite-PHONE-001.md..019.md are picked up.\n\n"
        "```\n"
        + body
        + ("\n" if not body.endswith("\n") else "")
        + "```\n"
    )
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out.name} ({len(md):,} bytes)")


def write_chunk(
    chunk_idx: int,
    total_chunks: int,
    entries_in_chunk: list[tuple[dict, dict]],
    lines: list[str],
) -> None:
    """Write rewrite-PHONE-NNN.md for one chunk of entries.
    entries_in_chunk: list of (marker_dict, parsed_dict) tuples.
    """
    label = chunk_label(chunk_idx)
    prev_label = chunk_label(chunk_idx - 1) if chunk_idx > 1 else "000-HEADER"
    next_label = chunk_label(chunk_idx + 1) if chunk_idx < total_chunks else None

    first_marker = entries_in_chunk[0][0]
    last_marker = entries_in_chunk[-1][0]
    # Track by ordinal position in file (1-based), since some Ns are duplicated
    # We'll use the marker's own N for display purposes.
    ord_start = first_marker.get("ord", first_marker["n"])
    ord_end = last_marker.get("ord", last_marker["n"])

    nav_parts = [f"Previous: rewrite-PHONE-{prev_label}.md"]
    if next_label:
        nav_parts.append(f"Next: rewrite-PHONE-{next_label}.md")
    nav_parts.append("Index: rewrite-PHONE-INDEX.md")
    nav = " | ".join(nav_parts)

    out_lines: list[str] = []
    out_lines.append(f"# Rewrite chunk {label} — entries {ord_start}-{ord_end}\n\n")
    out_lines.append(f"_{nav}_\n\n")
    out_lines.append(
        "Edit ONLY the `YOUR REWRITE` section under each entry. The `Original`\n"
        "block is frozen — do not edit it. Save the file when done. On your\n"
        "laptop run `python C:\\E156\\merge-rewrite.py` to assemble a new\n"
        "workbook (`rewrite-workbook.NEW.txt`) with your edits applied.\n\n"
        "---\n\n"
    )

    for marker, parsed in entries_in_chunk:
        n = marker["n"]
        slug = marker["slug"]
        ord_pos = marker.get("ord", n)
        line_range = f"{marker['start_line']}-{marker['end_line']}"
        out_lines.append(f"## Entry {ord_pos} ([{n}/921]) — {slug}\n\n")
        if parsed["metadata"]:
            out_lines.append(f"<details><summary>Metadata</summary>\n\n```\n{parsed['metadata']}\n```\n\n</details>\n\n")
        out_lines.append("### Original (frozen — do not edit)\n\n")
        out_lines.append("```\n")
        out_lines.append(parsed["current_body"])
        if not parsed["current_body"].endswith("\n"):
            out_lines.append("\n")
        out_lines.append("```\n\n")
        out_lines.append("### YOUR REWRITE\n\n")
        out_lines.append("<!-- BEGIN-REWRITE -->\n")
        out_lines.append(parsed["your_rewrite"])
        if parsed["your_rewrite"] and not parsed["your_rewrite"].endswith("\n"):
            out_lines.append("\n")
        out_lines.append("<!-- END-REWRITE -->\n\n")
        out_lines.append(f"_Line range {line_range} in rewrite-workbook.txt_\n\n")
        out_lines.append("---\n\n")

    out = E156 / f"rewrite-PHONE-{label}.md"
    content = "".join(out_lines)
    out.write_text(content, encoding="utf-8")
    print(f"wrote {out.name} ({len(content):,} bytes, {len(entries_in_chunk)} entries)")


def write_index(chunks: list[list[tuple[dict, dict]]]) -> None:
    lines = [
        "# Rewrite phone-edit index\n\n",
        "Open any file below in Google Docs / your phone editor of choice.\n",
        "Edit only the `YOUR REWRITE` blocks (between `<!-- BEGIN-REWRITE -->` and\n",
        "`<!-- END-REWRITE -->`). When done, run `python C:\\E156\\merge-rewrite.py`\n",
        "on your laptop to assemble `rewrite-workbook.NEW.txt`.\n\n",
        "See `HOW-TO-USE.md` for the full mobile workflow.\n\n",
        "## Files\n\n",
        "- [rewrite-PHONE-000-HEADER.md](rewrite-PHONE-000-HEADER.md) — workbook header (frozen reference)\n",
    ]
    for idx, chunk in enumerate(chunks, 1):
        label = chunk_label(idx)
        first = chunk[0][0]
        last = chunk[-1][0]
        ord_start = first.get("ord", first["n"])
        ord_end = last.get("ord", last["n"])
        first_slug = first["slug"]
        last_slug = last["slug"]
        lines.append(
            f"- [rewrite-PHONE-{label}.md](rewrite-PHONE-{label}.md) — entries {ord_start}-{ord_end} "
            f"({first_slug} … {last_slug})\n"
        )
    lines.append("\n## Tools\n\n")
    lines.append("- `merge-rewrite.py` — assemble edits into `rewrite-workbook.NEW.txt`\n")
    lines.append("- `split_for_phone.py` — regenerate these chunk files from `rewrite-workbook.txt`\n")
    out = E156 / "rewrite-PHONE-INDEX.md"
    content = "".join(lines)
    out.write_text(content, encoding="utf-8")
    print(f"wrote {out.name}")


MERGE_SCRIPT = r'''#!/usr/bin/env python3
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
'''


HOW_TO = """# Mobile rewrite workflow

Edit your E156 workbook rewrites from a phone using Google Drive + Google Docs.

## One-time setup (laptop)

1. The `C:\\E156` folder syncs to Google Drive (already set up).
2. Once these files exist (you're reading this, so they do), they appear in Drive automatically.

## Editing on the phone

1. Open Google Drive on your phone, navigate into the `e156` folder.
2. Tap `rewrite-PHONE-INDEX.md` to see the list of 19 chunk files.
3. Tap any `rewrite-PHONE-001.md` … `rewrite-PHONE-019.md` to open it (Google Docs handles ~1 MB files fine).
4. For each entry you want to rewrite, find the `### YOUR REWRITE` section.
5. Edit **only** the text between `<!-- BEGIN-REWRITE -->` and `<!-- END-REWRITE -->`.
   - Leave the `### Original (frozen — do not edit)` block alone.
   - Keep your rewrite at most 156 words / 7 sentences (S1=Question, S2=Dataset, S3=Method, S4=Result, S5=Robustness, S6=Interpretation, S7=Boundary).
   - Saving in Docs is automatic.
6. To skip an entry, leave the BEGIN/END block alone (keeps whatever is currently there).

## Merging back into the workbook (laptop)

```
python C:\\E156\\merge-rewrite.py
```

This produces:

- `C:\\E156\\rewrite-workbook.NEW.txt` — full workbook with your edits applied (the original is untouched).
- `C:\\E156\\merge-report.md` — per-entry summary (applied / skipped / unchanged + original-vs-new length).

Review `merge-report.md`. When you're happy, replace the original:

```
move C:\\E156\\rewrite-workbook.txt C:\\E156\\rewrite-workbook.BAK.txt
move C:\\E156\\rewrite-workbook.NEW.txt C:\\E156\\rewrite-workbook.txt
```

Then run the existing E156 validator as usual:

```
python C:\\E156\\scripts\\apply_rewrites.py
```

## Regenerating the chunk files

If you bump the workbook (new entries appended on the laptop), regenerate the phone chunks:

```
python C:\\E156\\split_for_phone.py
```

The 19 chunks are produced fresh; any unmerged phone edits in old chunk files will be lost,
so always run `merge-rewrite.py` before regenerating.

## File map

- `rewrite-workbook.txt` — canonical source (laptop-only edits via `apply_rewrites.py`).
- `rewrite-PHONE-000-HEADER.md` — header (frozen reference, not edited).
- `rewrite-PHONE-001.md … rewrite-PHONE-019.md` — 50-entry chunks for phone editing.
- `rewrite-PHONE-INDEX.md` — index of chunks with entry ranges.
- `split_for_phone.py` — regenerates chunks from the workbook.
- `merge-rewrite.py` — assembles phone edits into `rewrite-workbook.NEW.txt`.
- `merge-report.md` — output of the last merge run.
- `HOW-TO-USE.md` — this file.
"""


def main() -> int:
    if not WORKBOOK.exists():
        print(f"ERROR: {WORKBOOK} not found", file=sys.stderr)
        return 1
    lines = load_lines()
    print(f"Loaded {len(lines):,} lines, {WORKBOOK.stat().st_size:,} bytes")
    markers = find_entries(lines)
    print(f"Found {len(markers)} entry markers")
    if len(markers) != 921:
        print(f"WARNING: expected 921 entries, found {len(markers)}", file=sys.stderr)
    for idx, mk in enumerate(markers):
        mk["ord"] = idx + 1

    entries: list[tuple[dict, dict]] = []
    for mk in markers:
        entry_lines = lines[mk["start_line"] - 1 : mk["end_line"]]
        parsed = parse_sections(entry_lines)
        entries.append((mk, parsed))

    write_header_chunk(lines)

    chunks: list[list[tuple[dict, dict]]] = []
    for i in range(0, len(entries), CHUNK_SIZE):
        chunks.append(entries[i : i + CHUNK_SIZE])
    total_chunks = len(chunks)
    print(f"Producing {total_chunks} chunk files (chunk size {CHUNK_SIZE})")

    for idx, chunk in enumerate(chunks, 1):
        write_chunk(idx, total_chunks, chunk, lines)

    write_index(chunks)

    (E156 / "merge-rewrite.py").write_text(MERGE_SCRIPT, encoding="utf-8")
    print("wrote merge-rewrite.py")

    (E156 / "HOW-TO-USE.md").write_text(HOW_TO, encoding="utf-8")
    print("wrote HOW-TO-USE.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
