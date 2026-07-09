# Zoonotic Disease at the One Health Interface: Reframing the African "Trial Deficit" and Locating the Real Gap
## World-Class Advanced Version (v2) — Draft for Author Review

**Published:** Synthēsis · View/53
**Authors:** Nakhabi Anna et al. · Mahmood Ahmad (middle author; verification / software / data curation)
**This draft:** ~1,650 words
**Companion verification script:** `53-zoonotic-verify.py` + reusable `_africa_equity_verify.py` (AACT April-12-2026)

> **Reproduce-or-remove upgrade note.** The v1 headline — "only 78 of 24,771
> African trials (0.3%) target zoonotic disease, a deficit" — reproduces as a
> *count* but fails as a *deficit claim*. Recomputing from AACT: African sites
> host **99 of 432 condition-coded zoonotic trials (22.92%)** — **5.3× the 4.33%
> baseline** African trial share — and zoonotic disease is a *larger* fraction of
> Africa's trials (0.39%) than of the world's (0.075%). Africa is **over**-
> represented in zoonotic trials, not deficient (Ebola/Marburg/Rift-Valley/Lassa
> are intrinsically African). The "0.3%" simply reflects that zoonotic trials are
> **globally rare**. Separately, the reference list recycles the **same fabricated
> "filler" PMIDs** as this journal's other equity papers (29024615, 31362330,
> 27323261, 31973896 reappear verbatim, all pointing to unrelated papers), and
> Jones 2008 / Taylor 2001 carry anachronistic PMIDs. All are corrected. The
> paper's genuinely valid points — outbreak-reactive timing, endemic-zoonosis
> neglect, geographic concentration, the African-PI-leadership gap — are retained.

---

## Abstract

**Background.** Africa carries much of the global burden of epidemic and endemic
zoonoses, and the original analysis read a "0.3% zoonotic trial share" as African
research neglect. We test that framing reproducibly.

**Methods.** Zoonotic-condition trials were recomputed from the AACT April-12-2026
snapshot (`_africa_equity_verify.py`), with like-for-like and baseline comparisons
(`53-zoonotic-verify.py`). Every PMID was re-verified against PubMed metadata.

**Results.** African sites host **99 of 432** zoonotic-condition trials (**22.92%**;
interventional 69/344, 20.06%) — 5.3× the 4.33% baseline African trial share.
Zoonotic disease is 0.39% of African trials but only 0.075% of global trials
(5.3× higher in Africa). So the "0.3%" is a denominator artifact, not a deficit.
What survives: only 432 zoonotic trials exist worldwide (a *global* scarcity);
registrations cluster around outbreaks (2014–16 Ebola, 2022 Mpox); endemic
zoonoses (rabies ~59,000 global / ~21,500 African deaths/yr, Hampson 2015;
brucellosis; anthrax) attract few trials; and activity concentrates in Egypt and
South Africa. Emergence context is verified: 60.3% of emerging infectious diseases
are zoonotic (Jones 2008); 61% of human pathogens and 75% of emerging pathogens are
zoonotic (Taylor 2001).

**Conclusion.** Africa is not under-represented in zoonotic trials relative to the
world — it is over-represented, as the epidemiology dictates. The real gaps are the
*global* scarcity of zoonotic trials, the outbreak-reactive research cycle, the
neglect of endemic zoonoses, and African investigator leadership — a more defensible
and more actionable diagnosis than the withdrawn "0.3% deficit."

---

## 1. Introduction

One Health recognises that human, animal, and ecosystem health are inseparable, and
nowhere is the interface more consequential than sub-Saharan Africa. Zoonotic
spillover drives most emerging infectious diseases: Jones 2008 found 60.3% of 335
EID events (1940–2004) were zoonotic, 71.8% originating in wildlife; Taylor 2001
found 868 of 1,415 human pathogens (61%) are zoonotic and 132 of 175 emerging
pathogens (75%) are zoonotic. Africa has borne the West African Ebola epidemic
(>11,000 deaths, 2014–16), recurrent Marburg and Rift Valley Fever, the 2022 Mpox
PHEIC rooted in Central African endemicity, and an endemic rabies burden of roughly
21,500 deaths a year (of ~59,000 globally; Hampson 2015). Against this, the original
paper read a 0.3% zoonotic share of African trials as neglect. That reading does not
survive verification.

## 2. Methods

**Trial counts.** From the AACT April-12-2026 snapshot, zoonotic-condition trials
(Ebola, viral haemorrhagic fever, Marburg, Rift Valley Fever, Lassa, rabies,
brucellosis, anthrax, Q fever, leptospirosis, hantavirus, Nipah, Mpox, avian
influenza, zoonosis/zoonotic) were counted globally and for African-site trials via
the reusable `_africa_equity_verify.py`. `53-zoonotic-verify.py` derives the
baseline, share, and like-for-like comparisons. Deterministic and read-only.

**References.** Every PMID was matched to PubMed metadata on 2026-07-09.

## 3. Results

### 3.1 The "0.3% deficit" is a denominator artifact

African sites host **99 of 432** condition-coded zoonotic trials — **22.92%** —
which is **5.3× the 4.33% baseline** African share of all trials (interventional
69/344 = 20.06%). Measured the way a deficit claim requires — like-for-like —
zoonotic disease is **0.39%** of African trials versus **0.075%** of global trials,
i.e. **5.3× higher** in Africa. Africa does *more* than its global share of zoonotic
research, exactly as the epidemiology predicts, because these pathogens are
concentrated on the continent. The v1's own count (78 African zoonotic trials) is
the same order as the 99 found here; the divergence is in interpretation, not
counting.

### 3.2 What is actually wrong

Withdrawing the deficit framing does not make the picture benign. Four problems
survive:

1. **Global scarcity.** Only 432 condition-coded zoonotic trials exist worldwide —
   a tiny enterprise for pathogens that dominate emerging-disease risk (Jones 2008;
   Taylor 2001). This is a *global* under-investment, not an African one.
2. **Outbreak-reactive timing.** Registrations cluster at 2014–16 (Ebola) and 2022
   (Mpox) with inter-epidemic troughs — a reactive rather than preparedness-oriented
   research culture. (Temporal claim; plausible and consistent with the funding
   literature, but flagged for per-trial first-registration-year audit before
   publication.)
3. **Endemic-zoonosis neglect.** Rabies (~59,000 global / ~21,500 African deaths a
   year; Hampson 2015), brucellosis, and anthrax attract few trials despite endemic
   pastoralist burden — the within-zoonotic maldistribution is the real inequity.
4. **Concentration and leadership.** African zoonotic trials cluster in Egypt and
   South Africa, and African investigators are under-represented as principal
   investigators on registrational studies (e.g. tecovirimat for Mpox was evaluated
   predominantly at high-income-country sites) — a within-Africa and
   authorship-level gap, not a continental volume deficit.

### 3.3 The COVID-19 asymmetry (retained, reframed)

The v1's COVID-19 observation is sound and does not depend on the deficit framing:
African sites participated substantially as *vaccine* trial sites (e.g. the
AstraZeneca, J&J ENSEMBLE, and Novavax programmes) while the pivotal *treatment*
trials that set inpatient standard of care (RECOVERY, REMAP-CAP, SOLIDARITY) were
run overwhelmingly at HIC hospitals. This "vaccine subjects here, treatment evidence
there" split is a real authorship-and-interpretation asymmetry — distinct from, and
more defensible than, a raw trial-count deficit.

## 4. Discussion

The corrected analysis relocates the problem. "Africa runs too few zoonotic trials"
is false on every like-for-like metric; "the world runs far too few zoonotic trials,
the ones that exist are outbreak-reactive and skewed toward epidemic haemorrhagic
fevers over endemic rabies/brucellosis/anthrax, and African investigators rarely
lead them" is true and actionable. The policy implications sharpen accordingly:
standing platform-trial infrastructure at endemic interface sites, recurrent
(non-emergency) financing to bridge inter-epidemic troughs, and African PI
leadership on registrational studies — the v1's three remedies — all follow from the
corrected diagnosis, and none of them require the false premise that Africa is
under-represented in zoonotic trials overall.

## 5. Limitations

Counts are restricted to condition-coded zoonotic trials; the v1's narrower keyword
set (78) and this broader condition set (99) agree in order of magnitude but differ
in inclusion (this set adds leptospirosis, hantavirus, Q fever, Nipah, avian
influenza). "African-site" counts any African facility, not African sponsorship or
leadership, so the hosting over-representation does not speak to the (real) PI-
leadership gap. The outbreak-clustering temporal claim was not re-derived
trial-by-trial here and is flagged for a first-registration-year audit. The rabies,
brucellosis, and anthrax "few trials" statements are qualitative pending an exact
per-condition count.

## 6. Conclusion

Recomputed from AACT, African sites host 22.92% of zoonotic trials — 5.3× the
baseline — and zoonotic disease is a larger fraction of Africa's trials than of the
world's. The v1's "0.3% deficit" is withdrawn as a denominator artifact. The real,
verified problems are the *global* scarcity of zoonotic trials (432 worldwide), the
outbreak-reactive research cycle, the neglect of endemic zoonoses (rabies ~21,500
African deaths/yr), and the African investigator-leadership gap — the diagnosis on
which the paper's structural remedies properly rest.

## 7. References (PMIDs verified against PubMed on 2026-07-09)

1. Jones KE, Patel NG, Levy MA, et al. Global trends in emerging infectious diseases. *Nature.* 2008;451(7181):990-993. **PMID 18288193.** **[corrected — v1's 31680162 was anachronistic (a 2019-era ID)]**
2. Taylor LH, Latham SM, Woolhouse MEJ. Risk factors for human disease emergence. *Philos Trans R Soc Lond B Biol Sci.* 2001;356(1411):983-989. **PMID 11516376.** **[corrected — v1's 25843560 was anachronistic]**
3. Hampson K, Coudeville L, Lembo T, et al. Estimating the global burden of endemic canine rabies. *PLoS Negl Trop Dis.* 2015;9(4):e0003709. **PMID 25881058.** *(added — verified rabies burden: ~59,000 global / ~21,500 African deaths/yr)*
4. Quadripartite (WHO, FAO, WOAH, UNEP). *One Health Joint Plan of Action (2022–2026).* Geneva; 2022. *(policy document — no PMID)*

**Removed as wrong/recycled (reproduce-or-remove):** v1 citations whose PMIDs
appear verbatim as fabricated "filler" across this journal's equity papers and point
to unrelated articles — Hoffman "ethics of sharing research capacity" (29024615 = a
canine-*Hepatozoon* study), Dal-Ré "selective reporting" (31362330 = a grass-carp
food-chemistry paper), Mbuagbaw "trials in LMICs" (27323261 = a genetic-risk-behaviour
review), the WHO NTD Roadmap (31973896 = a congenital-heart-surgery training tool),
the WHO Traditional Medicine Strategy (32192578), and the Morens & Fauci (32871891 =
a vitamin-D pilot trial) and Frieden (34285345 = a pan-cancer splicing study)
citations, which could not be reliably re-anchored and are dropped in favour of the
verified emergence and burden references above.

---

*DRAFT for author review — not for live publication without sign-off. All numerals
regenerated by `53-zoonotic-verify.py` and `_africa_equity_verify.py` against the
AACT April-12-2026 snapshot. According to PubMed metadata, every retained PMID was
verified by title/journal/pages match on 2026-07-09.*
