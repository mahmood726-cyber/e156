#!/usr/bin/env python
"""Headless-Chrome smoke test of the e156 dashboards + flagship capsules.
Loads each, captures severe JS console errors, and checks that content/charts
actually rendered."""
import glob
import io
import os
import sys
import time

if "pytest" not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

ROOT = os.path.dirname(os.path.abspath(__file__))
FILES = (["e156-library.html", "flagship/index.html", "e156-submission/index.html"]
         + sorted(os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "flagship", "*-capsule.html"))))


def driver():
    o = Options()
    o.add_argument("--headless=new")
    o.add_argument("--no-sandbox")
    o.add_argument("--disable-gpu")
    o.add_argument("--window-size=1280,900")
    o.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    d = webdriver.Chrome(options=o)
    d.set_page_load_timeout(60)
    return d


def main():
    d = driver()
    bad = {}
    try:
        for rel in FILES:
            p = os.path.join(ROOT, rel)
            url = "file:///" + p.replace("\\", "/")
            probs = []
            try:
                d.get(url)
                time.sleep(1.2)  # let inline chart JS run
                # severe console errors
                errs = [l["message"][:140] for l in d.get_log("browser")
                        if l["level"] == "SEVERE"
                        and "favicon" not in l["message"].lower()]
                if errs:
                    probs.append(f"{len(errs)} JS error(s): {errs[:2]}")
                # content render check
                svgs = d.find_elements(By.CSS_SELECTOR, "svg")
                svg_filled = any(len(s.find_elements(By.CSS_SELECTOR, "*")) > 2 for s in svgs)
                rows = d.find_elements(By.CSS_SELECTOR, ".card, tr, .paper, li")
                if "capsule" in rel and not svg_filled:
                    probs.append("no rendered SVG chart")
                if rel.endswith("index.html") or "library" in rel:
                    if len(rows) < 3:
                        probs.append(f"sparse content ({len(rows)} rows/cards)")
                title = (d.title or "")[:40]
            except Exception as e:
                probs.append(f"LOAD FAIL: {type(e).__name__}: {str(e)[:80]}")
                title = "?"
            status = "OK" if not probs else "!!"
            print(f"  [{status}] {rel:40} {title}")
            if probs:
                bad[rel] = probs
    finally:
        d.quit()
    print(f"\n{len(FILES)-len(bad)}/{len(FILES)} clean.")
    if bad:
        print("FINDINGS:")
        for f, p in bad.items():
            print(f"  {f}: {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
