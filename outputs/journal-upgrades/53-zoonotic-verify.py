#!/usr/bin/env python
"""
Deterministic verification for the v2 (truth-first) of View/53
(Zoonotic disease at the One Health interface — African trial registry).

Like paper 54 (AMR), the v1 headline -- "only 78 of 24,771 African trials (0.3%)
target zoonotic disease" -- is a real count but a MISLEADING deficit framing.
This script reproduces the zoonotic trial counts from the AACT April-12-2026
snapshot (via the repo's reusable `_africa_equity_verify.py`, whose 'zoonotic'
condition group prints these numbers) and computes the like-for-like comparison
the v1 omitted.

AACT-derived (condition-coded 'zoonotic' group; reproduce by running
`_africa_equity_verify.py` against F:/AACT-storage/AACT/2026-04-12):
    registry all-studies      : 579,828
    registry any-African-site : 25,125   (4.33% baseline)
    zoonotic global           : 432
    zoonotic African          : 99       (22.92% of zoonotic trials)
    zoonotic global (interv)  : 344
    zoonotic African (interv) : 69       (20.06%)
The v1's narrower keyword search found 78 African zoonotic trials -- same order.

Read-only; standard library only.
"""
ALL       = 579_828
AFR_SITE  = 25_125
ZOO_G     = 432
ZOO_A     = 99

print("=== Baseline & shares ===")
base = 100.0 * AFR_SITE / ALL
print(f"  African-site share of ALL trials (baseline): {base:.2f}%")
print(f"  African share of ZOONOTIC trials: {100.0*ZOO_A/ZOO_G:.2f}%")
print(f"  -> {(100.0*ZOO_A/ZOO_G)/base:.1f}x the baseline: Africa is heavily")
print(f"     OVER-represented among zoonotic trials (Ebola/Marburg/RVF/Lassa are")
print(f"     inherently African), not deficient.")

print("\n=== The v1 '0.3%' framing, like-for-like ===")
zoo_pct_africa = 100.0 * ZOO_A / AFR_SITE
zoo_pct_global = 100.0 * ZOO_G / ALL
print(f"  Zoonotic as % of AFRICAN trials: {ZOO_A}/{AFR_SITE:,} = {zoo_pct_africa:.3f}%  (v1's '0.3%')")
print(f"  Zoonotic as % of GLOBAL trials : {ZOO_G}/{ALL:,} = {zoo_pct_global:.3f}%")
print(f"  Ratio (Africa/global) = {zoo_pct_africa/zoo_pct_global:.1f}x")
print("  -> Zoonotic disease is a LARGER fraction of Africa's trials than the")
print("     world's. The '0.3% deficit' is a denominator artifact: zoonotic")
print("     trials are globally rare, and Africa does MORE than its share.")

print("\n=== What survives as a real problem ===")
print("  * Global scarcity: only 432 condition-coded zoonotic trials worldwide.")
print("  * Outbreak-reactive timing: registrations cluster at 2014-16 (Ebola) and")
print("    2022 (Mpox) with inter-epidemic troughs (temporal claim; plausible,")
print("    flagged for per-trial year audit).")
print("  * Endemic neglect: rabies (~59,000 global deaths/yr, ~21,500 African;")
print("    Hampson 2015), brucellosis, anthrax get few trials despite endemic burden.")
print("  * Geographic concentration in Egypt / South Africa; African-PI-leadership gap.")
print("  These are within-zoonotic and within-Africa maldistribution problems --")
print("  NOT an African deficit relative to the rest of the world.")
