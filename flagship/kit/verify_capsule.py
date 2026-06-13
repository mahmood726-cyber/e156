"""Headless-render verification for e156 capsules.

Loads a capsule file:// in headless Chrome, waits for the engine to run, then
asserts: (1) no severe console errors, (2) every named SVG target has child
nodes (chart actually drew), (3) optional required-tag checks per svg.

Usage:
  python kit/verify_capsule.py ../metaregression-capsule.html#bubble:polyline,circle
  python kit/verify_capsule.py ../ce-plane-capsule.html#planePlot:circle

Each arg: <path>#<svgId>:<comma-tags>  (tags optional). Multiple #frag allowed
by repeating the path arg. Exit 0 = all pass, 1 = any failure.
"""
import sys
import io
from pathlib import Path

if "pytest" not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def build_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--window-size=1200,1400")
    opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    return webdriver.Chrome(options=opts)


def check(driver, path: Path, targets):
    url = path.resolve().as_uri()
    driver.get(url)
    driver.implicitly_wait(5)
    import time
    time.sleep(1.2)  # let on-load engine + render settle

    problems = []

    # console errors (ignore favicon / benign)
    for entry in driver.get_log("browser"):
        if entry["level"] == "SEVERE" and "favicon" not in entry["message"]:
            problems.append(f"CONSOLE: {entry['message'][:300]}")

    for svg_id, tags in targets:
        n = driver.execute_script(
            "var e=document.getElementById(arguments[0]);return e?e.querySelectorAll('*').length:-1;",
            svg_id)
        if n < 0:
            problems.append(f"#{svg_id}: element not found")
        elif n == 0:
            problems.append(f"#{svg_id}: empty (chart did not draw)")
        for t in tags:
            c = driver.execute_script(
                "var e=document.getElementById(arguments[0]);return e?e.querySelectorAll(arguments[1]).length:0;",
                svg_id, t)
            if c == 0:
                problems.append(f"#{svg_id}: missing <{t}>")
            else:
                print(f"    #{svg_id} <{t}> x{c}")
    return problems


def parse(arg):
    # path#id:tag,tag  (may repeat #frag)
    path, _, frag = arg.partition("#")
    targets = []
    if frag:
        for part in frag.split("#"):
            sid, _, tagstr = part.partition(":")
            tags = [t for t in tagstr.split(",") if t]
            targets.append((sid, tags))
    return Path(path), targets


def main(argv):
    if not argv:
        raise SystemExit(__doc__)
    driver = build_driver()
    fails = 0
    try:
        for arg in argv:
            path, targets = parse(arg)
            print(f"\n=== {path.name} ===")
            probs = check(driver, path, targets)
            if probs:
                fails += 1
                for p in probs:
                    print(f"  FAIL {p}")
            else:
                print("  PASS")
    finally:
        driver.quit()
    print(f"\n{'ALL PASS' if fails == 0 else str(fails) + ' FAILED'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
