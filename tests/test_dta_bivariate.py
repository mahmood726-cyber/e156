"""Numerical baseline: the dta capsule's in-browser bivariate (Reitsma) REML MLE
must reproduce mada::reitsma to < 1e-4 on the interior-rho fixture.

The expected values were captured from R (mada::reitsma) on hsroc-tiny.csv and are
the same fixture allmeta uses. This guards the pure-JS Fisher-scoring MLE against
regression — it is the load-bearing statistical claim of the capsule.
"""
import json
import subprocess
import sys
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
CAPSULE = ROOT / "flagship" / "dta-capsule.html"

# captured from Rscript: mada::reitsma on hsroc-tiny.csv (interior rho, no boundary)
MADA = {
    "mu1": 1.428039825037, "mu2": -1.898869844426,
    "tau1_sq": 1.015957863695, "tau2_sq": 0.5762041201539,
    "rho": -0.8844495722827,
}
FIXTURE = [[80, 40, 20, 160], [95, 5, 5, 95], [60, 30, 40, 170],
           [88, 12, 12, 88], [70, 50, 30, 150], [92, 8, 8, 192], [55, 45, 45, 155]]
TOL = 1e-4

HARNESS = r"""
const fs=require('fs');
let s=fs.readFileSync(process.argv[2],'utf8').match(/<script>([\s\S]*)<\/script>/)[1];
global.localStorage={getItem:()=>null,setItem:()=>{}};
global.document={getElementById:()=>null,addEventListener:()=>{},querySelector:()=>null,querySelectorAll:()=>[],documentElement:{style:{setProperty:()=>{}},setAttribute:()=>{},getAttribute:()=>null}};
global.window={matchMedia:()=>({matches:false})};global.matchMedia=global.window.matchMedia;
global.__fix=JSON.parse(process.argv[3]);
s=s.slice(0,s.indexOf("document.getElementById('cBody').addEventListener")).replace('"use strict";','');
const probe=';globalThis.__b=bivariate(globalThis.__fix.map(function(a){return studyStats({tp:a[0],fp:a[1],fn:a[2],tn:a[3]});}));';
(0,eval)(s+probe);
const b=globalThis.__b;
console.log(JSON.stringify({mu1:b.mu[0],mu2:b.mu[1],tau1_sq:b.t1sq,tau2_sq:b.t2sq,rho:b.rho}));
"""


@pytest.mark.skipif(shutil.which("node") is None, reason="node not available")
def test_bivariate_matches_mada():
    js = ROOT / "tests" / "_dta_biv_harness.js"
    js.write_text(HARNESS, encoding="utf-8")
    try:
        r = subprocess.run(["node", str(js), str(CAPSULE), json.dumps(FIXTURE)],
                           capture_output=True, text=True, timeout=60)
        assert r.returncode == 0, r.stderr
        got = json.loads(r.stdout.strip().splitlines()[-1])
    finally:
        js.unlink(missing_ok=True)
    for k, want in MADA.items():
        assert abs(got[k] - want) < TOL, f"{k}: capsule {got[k]} vs mada {want} (Δ {abs(got[k]-want):.2e} > {TOL})"
