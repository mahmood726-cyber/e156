# claim_language override triage — 2026-05-25T09:53:32+00:00

_Scanned `rewrite-workbook.txt` for entries that would trigger the P1-claim-language Sentinel rule. Classified each by simple pattern matching; operator decides which to whitelist via_ `# sentinel:claim-language-allow` _markers._

## Counts

- **clean**: 1611
- **likely-descriptive**: 49
- **likely-causal**: 0
- **uncertain**: 50
- **skip-already-marked**: 0


## Likely descriptive (auto-whitelist safe) (49)

_Action_: Run `python scripts/propose_claim_overrides.py --apply` to inject `# sentinel:claim-language-allow` into each of these entries.

| # | name |
|---|------|
| 1 | 501MLM |
| 5 | AfricaRCT |
| 22 | clinic-site |
| 25 | ComponentNMA |
| 39 | ctgov-search-strategies |
| 45 | dosehtml |
| 46 | DPMA |
| 47 | DTA70 |
| 55 | Fatiha-course-github-v2 |
| 61 | FragilityIndex |
| 63 | GWAM |
| 67 | HTA_Evidence_Integrity_Suite |
| 70 | idea12 |
| 75 | KMcurve |
| 79 | living-meta-engine |
| 80 | llm-meta-analysis |
| 83 | MAPriors |
| 97 | MetaMethods |
| 101 | MetaRegression |
| 103 | MetaRep |
| 108 | metasprint-autopilot |
| 110 | metasprint-dose-response |
| 112 | metasprintnma |
| 118 | Multipledatameta |
| 122 | nma-dose-response-app |
| 129 | Pairwise70 |
| 140 | prognostic-meta |
| 142 | PubBiasSuite |
| 148 | RMSTmeta |
| 152 | shahzaib-icu-landscape |
| 160 | truthcert-meta2-prototype |
| 163 | ubcma |
| 168 | WorldIPD |
| 169 | WorldIPD-private |
| 261 | lec_phase0_project |
| 332 | Reversal-CAST |
| 337 | Reversal-Vioxx-VIGOR |
| 487 | Pairwise70 |
| 355 | SAARCe156Students |
| 373 | modern-stats-global-health |
| 388 | GlobalTransportabilityAtlas |
| 455 | mpet-dta |
| 458 | aleph-point-synthesis |
| 459 | aps-methodologist-review |
| 460 | gma-dta |
| 461 | pem-dta |
| 465 | aleph-point-synthesis-final |
| 468 | SparsentanIgANLivingMA |
| 479 | shahzaib-icu-landscape |

## Likely causal (human rewrite required) (0)

_Action_: These contain an overclaim word used as the verb of an evidence claim. Rewrite the sentence (e.g. 'proves' → 'is consistent with'). Do NOT auto-whitelist — the override would silence a real signal.


## Uncertain (human review required) (50)

_Action_: Pattern matches both descriptive and causal contexts, or neither matched. Open the entry, decide whether to whitelist or rewrite.

| # | name |
|---|------|
| 12 | BiasForensics |
| 13 | Burhan |
| 14 | CardioOracle |
| 17 | CausalSynth |
| 36 | ctgov-phase-reporting-gap |
| 42 | ctgov-structural-missingness |
| 56 | FATIHA_Project |
| 84 | MAWorkbench |
| 89 | Meta_Ecosystem_Model |
| 94 | MetaFusion-Lab |
| 109 | metasprint-cardio-universe |
| 121 | New_Heterogeneity_Model |
| 131 | Pairwiseai |
| 135 | portfolio-site |
| 143 | rct-extractor-v2 |
| 158 | TrialRadar |
| 174 | AsSirat |
| 246 | EvidenceOracle |
| 263 | Living metas |
| 267 | MAFI |
| 269 | MASampleSize |
| 274 | NMA |
| 277 | PFA_AF_LivingMeta |
| 278 | rayyanreplacement |
| 286 | truthcert-openclaw-supermemory-stack |
| 291 | AuthorshipLedger |
| 304 | AutoReview |
| 339 | Reversal-ACCORD |
| 341 | Reversal-Paroxetine-Study329 |
| 342 | Reversal-Reboxetine |
| 343 | Reversal-Albumin-SAFE |
| 357 | CardioSynth |
| 489 | Orforglipron_LivingMeta |
| 490 | AuthorshipLedger |
| 400 | ZenodoPipeline |
| 428 | AntiAmyloidADLivingMA |
| 431 | DCBPADLivingMA |
| 433 | ResmetiromMASHLivingMA |
| 449 | IptacopanPNHLivingMA |
| 453 | gds-dta |
| 456 | eh-dta |
| 457 | sl12-dta |
| 462 | pem-methodologist-review |
| 463 | ees-dta |
| 464 | ees-methodologist-review |
| 474 | Fatiha |
| 477 | mem-ecosystem-model |
| 486 | arac |
| 1160 | BEZLOTOXUMAB_CDIFF_AUTO_FULL |
| 1161 | BEZLOTOXUMAB_CDIFF_AUTO |
