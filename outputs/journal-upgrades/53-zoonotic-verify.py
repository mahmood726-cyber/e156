#!/usr/bin/env python
"""
Deterministic verification for the v2 (truth-first) of View/53
(Zoonotic disease at the One Health interface — African trial registry).

Like paper 54 (AMR), the v1 headline -- "only 78 of 24,771 African trials (0.3%)
target zoonotic disease" -- is a real count but a MISLEADING deficit framing.
This script LIVE-DERIVES the zoonotic trial counts by streaming the raw AACT
April-12-2026 flat files (studies.txt / facilities.txt / conditions.txt) via the
shared `_aact_africa.py` substrate, then computes the like-for-like comparison the
v1 omitted. No count is hardcoded — every AACT figure is regenerated from the
snapshot on each run, so it cannot silently drift from the data (fix 2026-07-12,
prompted by a cross-vendor Codex objection that the prior version hardcoded 432/99).

Condition group (exact keywords, see `_aact_africa.py::GROUPS['zoonotic']`):
    zoonotic/zoonosis, brucellosis, rift valley fever, lassa fever, ebola,
    marburg, anthrax, q fever, leptospirosis, hantavirus, nipah, monkeypox/mpox,
    avian influenza, rabies.
Definitions: African-site = >=1 facility in a 54-state AU list; interventional =
studies.study_type == INTERVENTIONAL. Expected (as of the 2026-04-12 snapshot):
zoonotic global 432 / African 99 (22.92%); v1's narrower search found 78 (same order).

Read-only; standard library only.
"""
import sys
from _aact_africa import derive_group

print("Streaming AACT (facilities, study types, conditions)…", file=sys.stderr)
_d = derive_group("zoonotic")
print(f"  [live] snapshot = {_d['snapshot']}", file=sys.stderr)

ALL       = _d["all"]         # live: registry all-studies
AFR_SITE  = _d["afr_site"]    # live: registry any-African-site
ZOO_G     = _d["g_global"]    # live: zoonotic global
ZOO_A     = _d["g_africa"]    # live: zoonotic African
ZOO_GI    = _d["g_glob_intv"] # live: zoonotic global (interventional)
ZOO_AI    = _d["g_afr_intv"]  # live: zoonotic African (interventional)

print(f"=== LIVE-DERIVED AACT counts ({_d['snapshot']}) ===")
print(f"  all={ALL:,}  African-site={AFR_SITE:,}")
print(f"  zoonotic global={ZOO_G}  African={ZOO_A}  (interv {ZOO_AI}/{ZOO_GI})")

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
print(f"  * Global scarcity: only {ZOO_G} condition-coded zoonotic trials worldwide.")
print("  * Outbreak-reactive timing: registrations cluster at 2014-16 (Ebola) and")
print("    2022 (Mpox) with inter-epidemic troughs (temporal claim; plausible,")
print("    flagged for per-trial year audit).")
print("  * Endemic neglect: rabies (~59,000 global deaths/yr, ~21,500 African;")
print("    Hampson 2015), brucellosis, anthrax get few trials despite endemic burden.")
print("  * Geographic concentration in Egypt / South Africa; African-PI-leadership gap.")
print("  These are within-zoonotic and within-Africa maldistribution problems --")
print("  NOT an African deficit relative to the rest of the world.")
