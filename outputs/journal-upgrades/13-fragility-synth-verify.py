#!/usr/bin/env python
"""
Deterministic Fragility Index (FI) and Fragility Quotient (FQ) computation for the
v2 advanced version of the Synthesis paper "Fragility Synthesis" (View/13).

FI (Walsh 2014, J Clin Epidemiol): for a significant 2x2 trial (two-sided Fisher
p<=0.05), the minimum number of events that must be ADDED to the fewer-event (usually
treatment) arm -- converting non-events to events, holding N fixed -- to render the
result non-significant (p>0.05). FQ = FI / N_total.

Primary-endpoint 2x2 tables (PubMed-verified from the NEJM abstracts, 2026-07-04):
  DAPA-HF         McMurray 2019  PMID 31535829  386/2373 (dapa) vs 502/2371 (pbo)
  EMPEROR-Reduced Packer 2020    PMID 32865377  361/1863 (empa) vs 462/1867 (pbo)
  PARADIGM-HF     McMurray 2014  PMID 25176015  914/4187 (LCZ) vs 1117/4212 (enal)
  PLATO           Wallentin 2009 PMID 19717846  864/9333 (tica) vs 1014/9291 (clop)
                                 (raw counts verified in Synthesis paper 27)

Internal validity check: DAPA-HF FI should reproduce ~62 and PLATO ~73 (both computed
independently earlier in this journal-upgrade program). Deterministic; scipy only.
"""
from scipy.stats import fisher_exact

def fisher_p(a, n1, c, n2):
    b, d = n1 - a, n2 - c
    return fisher_exact([[a, b], [c, d]], alternative="two-sided")[1]

def fragility_index(e1, n1, e2, n2):
    # ensure arm1 = fewer-event arm (events added here -> tests robustness to more harm)
    if e1 / n1 > e2 / n2:
        e1, n1, e2, n2 = e2, n2, e1, n1
    p0 = fisher_p(e1, n1, e2, n2)
    if p0 > 0.05:
        return None, p0  # not significant -> FI undefined
    k = 0
    a = e1
    while a < n1:
        a += 1; k += 1
        if fisher_p(a, n1, e2, n2) > 0.05:
            return k, p0
    return None, p0  # never crossed (exhausted arm)

TRIALS = [
    ("DAPA-HF",         386, 2373, 502, 2371),
    ("EMPEROR-Reduced", 361, 1863, 462, 1867),
    ("PARADIGM-HF",     914, 4187, 1117, 4212),
    ("PLATO",           864, 9333, 1014, 9291),
]

print("Cardiovascular trial Fragility Index — deterministic (v2)")
print(f"{'Trial':<18}{'events tx/N':<16}{'events ctl/N':<16}{'Fisher p':>11}{'FI':>6}{'FQ':>9}{'LTFU?':>8}")
for nm, e1, n1, e2, n2 in TRIALS:
    fi, p0 = fragility_index(e1, n1, e2, n2)
    N = n1 + n2
    fq = fi / N if fi is not None else float('nan')
    print(f"{nm:<18}{f'{e1}/{n1}':<16}{f'{e2}/{n2}':<16}{p0:>11.2e}{fi:>6}{fq:>9.4f}", end="")
    print(f"{'':>8}")

print("\nInternal validity check:")
fi_dapa,_ = fragility_index(386,2373,502,2371)
fi_plato,_ = fragility_index(864,9333,1014,9291)
print(f"  DAPA-HF FI = {fi_dapa}  (expected ~62 from prior program computation: "
      f"{'MATCH' if abs(fi_dapa-62)<=2 else 'CHECK'})")
print(f"  PLATO   FI = {fi_plato}  (expected ~73 from Synthesis paper 27: "
      f"{'MATCH' if abs(fi_plato-73)<=2 else 'CHECK'})")

print("\n" + "="*66)
print("Reading: mega-trial COMPOSITE endpoints are robust (FI 50-120), but FQ is")
print("tiny (0.004-0.03) -- robustness is bought with enormous N, not large margins.")
print("Corpus-level medians from published analyses (cited, NOT recomputed here):")
print("  revascularisation ~8, ACS ~12, general CV ~13, antithrombotic ~24.5;")
print("  a large minority of guideline-supporting trials have FI<10, and FI often")
print("  falls below the number lost to follow-up -> mortality endpoints & smaller")
print("  trials are frequently fragile even when the mega-trial composites are not.")
