# Verified PMID bank — journal-upgrade program

All entries verified against PubMed metadata (title + journal + volume/issue/pages
match) during this program. The v1 advanced drafts share a reference pool that
contained several WRONG PMIDs; use these verified IDs and do not revert.
**Always re-confirm any PMID not on this list before asserting it.**

## CT.gov transparency / trial-registration cluster

| Ref | PMID | DOI | Note |
|-----|------|-----|------|
| Anderson ML 2015 NEJM 372(11):1031-9 "Compliance with results reporting at ClinicalTrials.gov" | **25760355** | 10.1056/NEJMsa1409364 | v1 used wrong 25607445 (acid-base letter) |
| DeVito NJ 2020 Lancet 395:361-369 "Compliance with legal requirement…" | **31958402** | 10.1016/S0140-6736(19)33220-9 | v1 used wrong 31987386 |
| Zarin DA 2011 NEJM 364(9):852-60 "results database — update and key issues" | **21366476** | 10.1056/NEJMsa1012065 | correct in v1 |
| Zarin DA 2017 NEJM 376(4):383-391 "Update on Trial Registration 11 Years after the ICMJE Policy" | **28121511** | 10.1056/NEJMsr1601330 | v1 used wrong 28121506 (ipilimumab letter) |
| Ross JS 2012 BMJ 344:d7292 "Publication of NIH funded trials…" | **22214755** | 10.1136/bmj.d7292 | v1 sometimes used 22214756 (that is Prayle) |
| Prayle AP 2012 BMJ 344:d7373 "Compliance with mandatory reporting…" | **22214756** | 10.1136/bmj.d7373 | v1 used wrong 22214754 (that is Hart) |
| Riveros C 2013 PLoS Med 10(12):e1001566 "Timing and completeness…" | **24311990** | 10.1371/journal.pmed.1001566 | correct in v1 |
| Chan AW 2004 JAMA 291(20):2457-65 "Empirical evidence for selective reporting…" | **15161896** | 10.1001/jama.291.20.2457 | correct in v1 |
| Tasneem A 2012 PLoS One 7(3):e33677 "AACT database…" | **22438982** | 10.1371/journal.pone.0033677 | v1 used wrong 22479364 (microRNA paper) |
| Hart B 2012 BMJ 344:d7202 "Effect of reporting bias on meta-analyses…" | **22214754** | 10.1136/bmj.d7202 | (distinct paper; not a compliance study) |

## Cardiology cluster (verified 2026-07-04, papers 14 / 104 / 29)

| Ref | PMID | DOI | Note |
|-----|------|-----|------|
| Kang DH 2020 NEJM 382(2):111-9 RECOVERY (early surgery asx AS) | **31733181** | 10.1056/NEJMoa1912846 | primary op-mort/CV-death HR 0.09 (0.01-0.67); all-cause death 0.33 (0.12-0.90) |
| Banovic M 2022 Circulation 145(9):648-58 AVATAR | **34779220** | 10.1161/CIRCULATIONAHA.121.057639 | composite HR 0.46 (0.23-0.90); 13/78 vs 26/79 |
| Généreux P 2025 NEJM 392(3):217-227 EARLY TAVR | **39466903** | 10.1056/NEJMoa2405880 | composite HR 0.50 (0.40-0.63); 122/455 vs 202/446; the trial v1 called "RECOVERY-2" |
| Loganath K 2025 JAMA 333(3):213-221 EVOLVED (AS+fibrosis) | **39466640** | 10.1001/jama.2024.22730 | composite HR 0.79 (0.44-1.43) NS; all-cause death 1.22; AS-hosp 0.37 |
| Généreux P 2024 JACC 85(9):912-922 asx-AS study-level MA | **39641732** | 10.1016/j.jacc.2024.11.006 | hosp 0.40, stroke 0.62, all-cause mort 0.68 (NS), CV mort 0.67 (NS) |
| Montori VM 2005 JAMA 294(17):2203-9 "trials stopped early for benefit" | **16264162** | 10.1001/jama.294.17.2203 | v1 (paper 104) used wrong 16286622 (a cataract-surgery paper) |
| Ross J & Braunwald E 1968 Circulation 38(1 Suppl):61-7 "Aortic stenosis" | **4894151** | 10.1161/01.cir.38.1s5.v-61 | v1 used wrong 4874588 (Russian biography) |
| Pellikka PA 2005 Circulation 111(24):3290-5 (asx AS outcome, 622 adults) | **15956131** | 10.1161/CIRCULATIONAHA.104.495903 | v1 used wrong 15967845 (atherosclerosis gene-profiling) |
| IntHout J 2016 BMJ Open 6(7):e010247 "prediction intervals" | **27406637** | 10.1136/bmjopen-2015-010247 | v1 (papers 14/29) used wrong 27406442 (radiation-oncology) |
| Hong SJ 2015 JAMA 314(20):2155-63 IVUS-XPL | **26556051** | 10.1001/jama.2015.15454 | HR 0.48 (0.28-0.83) |
| Gao XF 2021 JACC Interv 14(3):247-57 ULTIMATE-3yr | **33541535** | 10.1016/j.jcin.2020.10.001 | 47/714 vs 76/734 |
| Holm NR 2023 NEJM 389(16):1477-87 OCTOBER | **37634149** | 10.1056/NEJMoa2307770 | HR 0.70 (0.50-0.98) |
| Ali ZA 2023 NEJM 389(16):1466-76 ILUMIEN IV | **37634188** | 10.1056/NEJMoa2305861 | HR 0.90 (0.67-1.19) |
| Bhatt DL 2021 NEJM 384(2):117-28 SOLOIST-WHF | **33200892** | 10.1056/NEJMoa2030183 | rate ratio 0.67 (0.52-0.85) |
| Bhatt DL 2021 NEJM 384(2):129-39 SCORED | **33200891** | 10.1056/NEJMoa2030186 | rate ratio 0.74 (0.63-0.88) |

## Cardiogenic shock + severe-asthma-biologics cluster (verified 2026-07-04, papers 23 / 106)

| Ref | PMID | DOI | Note |
|-----|------|-----|------|
| Thiele 2012 NEJM 367:1287-96 IABP-SHOCK II | **22920912** | 10.1056/NEJMoa1208410 | 30-d RR 0.96 (0.79-1.17) |
| Ouweneel 2017 JACC 69:278-87 IMPRESS | **27810347** | 10.1016/j.jacc.2016.10.022 | Impella vs IABP, HR 0.96 (0.42-2.18) |
| Ostadal 2023 Circulation 147:454-64 ECMO-CS | **36335478** | 10.1161/CIRCULATIONAHA.122.062949 | composite primary |
| Thiele 2023 NEJM 389:1286-97 ECLS-SHOCK | **37634145** | 10.1056/NEJMoa2307227 | VA-ECMO RR 0.98 (0.80-1.19) |
| Møller 2024 NEJM 390:1382-93 DanGer Shock | **38587239** | 10.1056/NEJMoa2312572 | Impella STEMI HR 0.74 (0.55-0.99); v1 mis-cited pp 1284-97 |
| Zeymer 2023 Lancet 402:1338-46 VA-ECMO IPD-MA | **37643628** | 10.1016/S0140-6736(23)01607-0 | 4 trials, OR 0.93 (0.66-1.29) NS |
| Ytterberg 2022 NEJM 386:316-26 ORAL Surveillance | **35081280** | 10.1056/NEJMoa2109927 | tofacitinib MACE 1.33 (0.91-1.94), cancer 1.48 (1.04-2.09) |
| Smolen 2023 Ann Rheum Dis 82:3-18 EULAR RA 2022 | **36357155** | 10.1136/ard-2022-223356 | guideline |
| Hanania 2011 Ann Intern Med 154:573-82 EXTRA omalizumab | **21536936** | 10.7326/0003-4819-154-9-201105030-00002 | IRR 0.75 (0.61-0.92) |
| Ortega 2014 NEJM 371:1198-207 MENSA mepolizumab | **25199059** | 10.1056/NEJMoa1403290 | SC RR 0.47, IV 0.53 |
| Bleecker 2016 Lancet 388:2115-27 SIROCCO benralizumab | **27609408** | 10.1016/S0140-6736(16)31324-1 | eos≥300 Q8W 0.49 |
| FitzGerald 2016 Lancet 388:2128-41 CALIMA benralizumab | **27609406** | 10.1016/S0140-6736(16)31322-8 | eos≥300 Q4W 0.64 |
| Castro 2018 NEJM 378:2486-96 QUEST dupilumab | **29782217** | 10.1056/NEJMoa1804092 | overall 0.53; eos≥300 0.34 |
| Menzies-Gow 2021 NEJM 384:1800-9 NAVIGATOR tezepelumab | **33979488** | 10.1056/NEJMoa2034975 | overall 0.44; eos<300 0.59 |

## Lipid-lowering cluster (verified 2026-07-04, paper 11)

| Ref | PMID | DOI | Note |
|-----|------|-----|------|
| CTT Collaboration 2010 Lancet 376:1670-81 | **21067804** | 10.1016/S0140-6736(10)61350-5 | RR 0.78 (0.76-0.80)/mmol/L, NO threshold |
| Sabatine 2017 NEJM 376:1713-22 FOURIER evolocumab | **28304224** | 10.1056/NEJMoa1615664 | HR 0.85 (0.79-0.92); 9.8% vs 11.3%; LDL 92→30 |
| Schwartz 2018 NEJM 379:2097-2107 ODYSSEY OUTCOMES | **30403574** | 10.1056/NEJMoa1801174 | alirocumab HR 0.85 (0.78-0.93); v1 used wrong 29957120 (nanomedicine cancer paper) |
| Cannon 2015 NEJM 372:2387-97 IMPROVE-IT ezetimibe | **26039521** | — | HR 0.936 |
| Ference 2017 Eur Heart J 38:2459-72 (LDL causal) | **28444290** | — | consensus |

## Cardiology reproducibility / HF-classification (verified 2026-07-04, paper 9)

| Ref | PMID | DOI | Note |
|-----|------|-----|------|
| McDonagh 2021 Eur Heart J 42:3599-3726 (2021 ESC HF) | **34447992** | 10.1093/eurheartj/ehab368 | guideline |
| Bozkurt 2021 Eur J Heart Fail 23:352-380 (Universal Def) | **33605000** | 10.1002/ejhf.2115 | HFmrEF 41-49% |
| Thavendiranathan 2013 JACC 61:77-84 (EF reproducibility) | **23199515** | 10.1016/j.jacc.2012.09.035 | 2D temporal EF var >0.10; 3D ~0.06 |

> **Fabricated/wrong v1 PMIDs found & removed:** paper 106 — 34236781 (→cardiac-surgery), 26302026 (→prediabetes), 28366640 (→chemistry sensor), 28366441 (→gastric endoscopy). Paper 104 — Montori 16286622 (→cataract). Paper 23 — 24279442 (→Czech CRP review). Paper 14 — IntHout 27406442, Pellikka 15967845, Ross-Braunwald 4874588 (all →unrelated). Paper 11 — ODYSSEY 29957120 (→nanomedicine cancer paper). **Systemic pattern: v1 clinical drafts carry heavily fabricated reference lists; verify EVERY PMID before asserting.**

## IPD meta-analysis methods

| Ref | PMID | DOI | Note |
|-----|------|-----|------|
| Riley RD 2010 BMJ 340:c221 "Meta-analysis of IPD: rationale, conduct, and reporting" | **20139215** | 10.1136/bmj.c221 | v1 used wrong 20139432 (lot-quality-sampling editorial) |
| Burke DL 2017 Stat Med 36(5):855-875 "IPD: one-stage and two-stage…" | **27747915** | 10.1002/sim.7141 | v1 used wrong 27804221 (chromatography paper) |
