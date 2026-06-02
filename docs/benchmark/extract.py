"""Extract the capsule pooling engine's output for the benchmark (docs/engine-benchmark.md).
Headless-loads a flagship meta-analysis capsule, drives the method selector and
Hartung-Knapp checkbox, and reads the Overall pooled readout + methodTag (tau^2).

Usage: python docs/benchmark/extract.py [capsule.html]   (default: flagship/sglt2-hf-capsule.html)
Requires: selenium + Chrome (Selenium Manager auto-resolves the driver).
"""
import sys, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CAP = sys.argv[1] if len(sys.argv) > 1 else r"C:/Projects/e156/flagship/sglt2-hf-capsule.html"
# Dataset A is the capsule's shipped data; pass Dataset B to test heterogeneity.
HET = [(0.55,0.45,0.67),(0.72,0.62,0.84),(0.88,0.77,1.00),(1.05,0.92,1.20),(0.63,0.51,0.78)]

def asc(s): return (s or "").encode("ascii", "replace").decode().replace("?", "").strip()

def read_pooled(d):
    hr = d.execute_script(
        "var t=[...document.querySelectorAll('#forest text')]"
        ".filter(function(x){return /^\\d\\.\\d\\d \\(/.test(x.textContent);});"
        "return t.length?t[t.length-1].textContent:null;")
    tau = d.execute_script("var m=document.getElementById('methodTag');return m?m.textContent:'';")
    return asc(hr), asc(tau)

def main():
    opts = Options()
    for a in ("--headless=new", "--no-sandbox", "--disable-gpu"):
        opts.add_argument(a)
    d = webdriver.Chrome(options=opts)
    try:
        d.get("file:///" + CAP.replace("\\", "/")); time.sleep(1.6)
        for label, hksj in (("Dataset A (shipped, HK off)", False), ("Dataset A (HK on)", True)):
            d.execute_script(
                "var c=document.getElementById('hksjChk');"
                "if(c){c.checked=arguments[0];c.dispatchEvent(new Event('change',{bubbles:true}));}", hksj)
            time.sleep(0.5)
            for m in ("REML", "PM", "DL"):
                d.execute_script(
                    "var s=document.getElementById('methodSel');"
                    "if(s){s.value=arguments[0];s.dispatchEvent(new Event('change',{bubbles:true}));}", m)
                time.sleep(0.4)
                hr, tau = read_pooled(d)
                print(f"{label} | {m:4s} -> {hr}   {tau}")
    finally:
        d.quit()

if __name__ == "__main__":
    main()
