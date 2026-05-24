# Mobile rewrite workflow

Edit your E156 workbook rewrites from a phone using Google Drive + Google Docs.

## One-time setup (laptop)

1. The `C:\E156` folder syncs to Google Drive (already set up).
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
python C:\E156\merge-rewrite.py
```

This produces:

- `C:\E156\rewrite-workbook.NEW.txt` — full workbook with your edits applied (the original is untouched).
- `C:\E156\merge-report.md` — per-entry summary (applied / skipped / unchanged + original-vs-new length).

Review `merge-report.md`. When you're happy, replace the original:

```
move C:\E156\rewrite-workbook.txt C:\E156\rewrite-workbook.BAK.txt
move C:\E156\rewrite-workbook.NEW.txt C:\E156\rewrite-workbook.txt
```

Then run the existing E156 validator as usual:

```
python C:\E156\scripts\apply_rewrites.py
```

## Regenerating the chunk files

If you bump the workbook (new entries appended on the laptop), regenerate the phone chunks:

```
python C:\E156\split_for_phone.py
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
