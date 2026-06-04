#!/usr/bin/env python
"""Tidy the blank-state title of e156-submission/index.html.

The page renders from a paper-data object D whose title is the empty-draft
sentinel "Untitled E156" (paper.json/paper.md are genuinely unwritten). Rather
than show 'Untitled E156' on a public page, present the empty state cleanly as
'E156 — Interactive Micro-Paper'. If the paper is ever populated with a real
title, that real title is used unchanged (load-a-paper behaviour preserved).
"""
import os

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "e156-submission", "index.html")

REPL = [
    ('<title>Untitled E156 — E156</title>',
     '<title>E156 — Interactive Micro-Paper</title>'),
    ('document.getElementById("title").textContent = D.title || "Untitled";',
     'document.getElementById("title").textContent = '
     '(D.title && D.title !== "Untitled E156") ? D.title : "E156 \\u2014 Interactive Micro-Paper";'),
    ('document.title = (D.title||"E156") + " \\u2014 E156 Interactive Paper";',
     'document.title = (D.title && D.title !== "Untitled E156") '
     '? (D.title + " \\u2014 E156 Interactive Paper") : "E156 \\u2014 Interactive Micro-Paper";'),
]


def main():
    data = open(PATH, "rb").read().decode("utf-8", "replace")
    for old, new in REPL:
        assert data.count(old) == 1, f"anchor not found ({data.count(old)}): {old[:60]!r}"
        data = data.replace(old, new, 1)
    open(PATH, "wb").write(data.encode("utf-8"))
    print("submission title tidied -> 'E156 — Interactive Micro-Paper' (empty-state)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
