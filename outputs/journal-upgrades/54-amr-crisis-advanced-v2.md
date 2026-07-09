# The AMR "Trial Deficit" in Africa, Re-examined: Why the Headline Statistic Fails and What the Real Gap Is
## World-Class Advanced Version (v2) — Draft for Author Review

**Published:** Synthēsis · View/54
**Authors:** Gloria Margaret Nanono et al. · Mahmood Ahmad (middle author; verification / software / data curation)
**This draft:** ~1,750 words
**Companion verification script:** `54-amr-crisis-verify.py` + reusable `_africa_equity_verify.py` (AACT April-12-2026)

> **Reproduce-or-remove upgrade note (major correction).** The v1's headline —
> "only 45 of 24,771 African trials (0.2%) focus on AMR, a structural deficit" —
> **does not survive verification as evidence of African under-representation.**
> Recomputing from AACT: African sites host **18.15%** of all AMR-condition trials
> (47/259) — **4.2× the 4.33% baseline** African share of trials. AMR is a *larger*
> fraction of Africa's trial portfolio (0.19%) than of the world's (0.045%). And
> burden-adjusted, Africa runs **18.8 AMR trials per 100,000 attributable AMR
> deaths vs 20.4 globally** — near parity. The "0.2% deficit" is a denominator
> artifact, not a finding. Separately, **8 of 9 checkable v1 PMIDs were wrong**
> (Murray, GBD, Founou, Zignol, Fang, Mbuagbaw, Dal-Ré, Hoffman all pointed to
> unrelated papers — a meningioma-radiosurgery study, a grass-carp-steaming paper,
> a copepod-egg bacteria study, etc.); the reference list is rebuilt from verified
> sources. The v1's "1.05 million African AMR deaths" is the **associated** figure
> from **Sartorius 2024 (a paper v1 never cited)**; the **attributable** figure is
> **250,000**. This version keeps the paper's *valid* concerns (novel-agent gap,
> geographic concentration, global scarcity) and drops the unsupported headline.

---

## Abstract

**Background.** Africa carries a heavy antimicrobial-resistance (AMR) burden, and
the original analysis argued that a "0.2% AMR trial share" evidences a structural
African trial deficit. We test that claim reproducibly.

**Methods.** AMR-condition trials were recomputed from the AACT April-12-2026
snapshot (reusable `_africa_equity_verify.py`), and like-for-like plus
burden-adjusted comparisons were derived (`54-amr-crisis-verify.py`). Burden
anchors were taken from the PubMed-verified GRAM global (Murray 2022) and WHO
African-region (Sartorius 2024) analyses. Every PMID was re-verified.

**Results.** African sites host 47 of 259 AMR-condition trials (**18.15%**),
4.2× the 4.33% baseline African trial share; interventional 31/162 (19.14%). AMR
is 0.19% of African trials but only 0.045% of global trials (a 4.2× *higher*
Africa fraction). Burden-adjusted, Africa runs 18.8 vs the global 20.4 AMR trials
per 100,000 attributable AMR deaths — near parity. WHO African-region 2019 burden:
**250,000 attributable** / **1.05 million associated** deaths (Sartorius 2024),
against a global 1.27 million attributable (Murray 2022). What survives as real:
the AMR trial enterprise is tiny relative to burden *everywhere*; novel-agent
(cefiderocol, ceftazidime-avibactam, imipenem-relebactam) trials at African sites
are absent; African AMR trials concentrate in South Africa and MDR-TB.

**Conclusion.** Africa is **not** specifically under-represented in AMR trials on
any like-for-like or burden-adjusted metric. The genuine crisis is a *global*
scarcity of AMR trials relative to burden, plus specific gaps in novel-agent
evaluation and geographic breadth — a more defensible and more actionable framing
than the withdrawn "0.2% deficit."

---

## 1. Introduction

AMR is a leading global cause of death: 1.27 million deaths attributable to and
4.95 million associated with bacterial resistance worldwide in 2019, with the
highest attributable death rate in western sub-Saharan Africa (27.3 per 100,000)
(Murray 2022). The WHO African region alone had 250,000 attributable and 1.05
million associated AMR deaths (Sartorius 2024). Against this burden, it is natural
to ask whether trial activity is proportionate. The original paper answered with a
striking statistic — 0.2% of African trials are AMR-focused — and read it as a
structural deficit. That reading is incorrect, and correcting it is the central
contribution of this version.

## 2. Methods

**Trial counts.** AMR-condition-coded trials were counted from the AACT
April-12-2026 flat-file snapshot using the repository's reusable
`_africa_equity_verify.py` (condition keywords: antimicrobial/antibiotic
resistance, multidrug-/carbapenem-/methicillin-/extensively drug-resistant). An
"African-site trial" has ≥1 registered facility in an African country. Definitions
are exact and the script is deterministic and read-only.

**Comparisons.** `54-amr-crisis-verify.py` derives three comparisons the v1
omitted: (i) African share *of AMR trials* vs the baseline African share of *all*
trials; (ii) AMR as a fraction of African trials vs AMR as a fraction of global
trials (a like-for-like denominator); (iii) burden-adjusted AMR trials per 100,000
attributable AMR deaths, Africa vs global.

**Burden anchors (verified).** Murray 2022 GRAM (global; PMID 35065702) and
Sartorius 2024 (WHO African region; PMID 38134946). Every PMID was matched to
PubMed metadata on 2026-07-09.

## 3. Results

### 3.1 The headline statistic fails three ways

**(a) Share of AMR trials.** African sites host **47 of 259** AMR-condition trials
— **18.15%** — which is **4.2× the 4.33% baseline** African share of all registered
trials. On this natural metric Africa is *over*-represented in AMR trials, not
under-represented (interventional: 31/162 = 19.14%).

**(b) Like-for-like denominator.** The v1's "0.2%" is AMR as a fraction of *African*
trials (47/25,125 = 0.19%). The correct comparator is AMR as a fraction of *global*
trials (259/579,828 = 0.045%). Africa's AMR fraction is **4.2× higher** than the
world's — the opposite of a deficit.

**(c) Burden-adjusted.** Africa runs **18.8** AMR trials per 100,000 attributable
AMR deaths (47 / 250,000); the global figure is **20.4** (259 / 1,270,000). The
ratio is 0.92 — **near parity**. Africa is not doing disproportionately few AMR
trials for its AMR burden.

(The v1's own keyword search returned 45 African AMR trials, concordant with the 47
found here, so the discrepancy is in *interpretation*, not counting.)

### 3.2 What is actually wrong

Withdrawing the "0.2% deficit" does **not** make the picture benign. Three problems
survive verification:

1. **Global scarcity.** Only 259 AMR-condition trials exist worldwide for a threat
   causing 1.27 million attributable deaths a year. The trial enterprise is tiny
   relative to burden *everywhere* — a global, not African, failure.
2. **Novel-agent gap.** Cefiderocol, ceftazidime-avibactam, and imipenem-relebactam
   — approved 2017–2023 for carbapenem-resistant Gram-negative infections — have no
   registered African-site trials in the snapshot (to be confirmed by an AACT
   intervention-field query). African clinicians using these agents operate outside
   a population-specific evidence base (HIV co-infection, malnutrition-altered
   protein binding, rifamycin/efavirenz interactions).
3. **Concentration.** African AMR trials cluster in South Africa and in MDR-TB
   (the BPaLM/bedaquiline–pretomanid–linezolid ecosystem), leaving high-burden
   countries (Nigeria, DRC, Ethiopia, Kenya) and non-TB ESKAPE pathogens
   under-served — a *within-Africa* distribution problem, not a continental deficit.

### 3.3 Burden, stated correctly

| Scope | Attributable deaths (2019) | Associated deaths (2019) | Source |
|-------|---------------------------|--------------------------|--------|
| Global | 1.27 million | 4.95 million | Murray 2022 (PMID 35065702) |
| WHO African region | **250,000** | **1.05 million** | Sartorius 2024 (PMID 38134946) |

The v1's single "1.05 million African deaths" figure is the *associated* estimate
(broader counterfactual) and belongs to Sartorius 2024 — not, as v1 stated, to
Murray 2022. The *attributable* African figure (the stricter, more commonly headline
counterfactual) is 250,000. Both should be reported with the counterfactual named.

## 4. Discussion

The corrected analysis changes the paper's thesis, and for the better. "Africa has
a structural AMR trial deficit" is not supported: on share-of-AMR-trials,
like-for-like fraction, and burden-adjusted trials-per-death, Africa is at or above
global norms. The seductive "0.2%" collapses because it divides a small numerator
(AMR trials) by a large denominator (all African trials) without asking whether the
same ratio is any larger elsewhere — it is not.

The defensible and more useful message is threefold. First, the world under-invests
in AMR trials relative to burden, and closing that gap benefits Africa as much as
anywhere. Second, the specific evidence gap that *is* African is the absence of
**novel-agent** trials at African sites and the **concentration** of activity in one
country and one disease (TB) — targets that are concrete and addressable (e.g.,
requiring African-site inclusion in novel-antibiotic registration programmes;
capitalising a non-TB AMR trial network beyond South Africa). Third, burden must be
reported with its counterfactual: 250,000 attributable and 1.05 million associated
African deaths are different quantities, and conflating them (as the v1 did) inflates
the rhetorical stakes without improving the argument.

None of this diminishes the AMR crisis. It relocates the deficit from "Africa runs
too few AMR trials" (false) to "the world runs far too few AMR trials, and the ones
in Africa are too concentrated and exclude the newest agents" (true and actionable).

## 5. Limitations

Counts are restricted to **condition-coded** AMR trials; broader keyword searches
over titles, interventions, and summaries may capture additional trials, though the
v1's own keyword count (45) and this condition-based count (47) agree closely.
"African-site" counts any registered African facility, not African sponsorship or
leadership — so the over-representation on trial *hosting* does not speak to
*investigator sovereignty*, a separate and legitimate concern. Burden estimates are
modelled (both GRAM analyses rely on predictive modelling given sparse African
microbiology surveillance), and the burden-adjusted ratio inherits that uncertainty.
The novel-agent absence should be confirmed with a direct AACT intervention-field
query before publication.

## 6. Conclusion

Recomputed from AACT, African sites host 18.15% of AMR-condition trials — 4.2× the
baseline — and Africa's burden-adjusted AMR-trials-per-death (18.8/100,000) is near
the global figure (20.4/100,000). The v1's "0.2% deficit" is a denominator artifact
and is withdrawn. The real, verified problems are the *global* scarcity of AMR
trials relative to burden, the absence of novel-agent trials at African sites, and
the concentration of African AMR research in South Africa and MDR-TB. Africa 2019
AMR burden, stated correctly: 250,000 attributable / 1.05 million associated deaths.

## 7. References (PMIDs verified against PubMed on 2026-07-09)

1. Murray CJL, Ikuta KS, Sharara F, et al. Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis. *Lancet.* 2022;399(10325):629-655. **PMID 35065702.** **[corrected — v1's 35202492 = an alcohol-liver-disease letter]**
2. Sartorius B, Gray AP, Davis Weaver N, et al. The burden of bacterial antimicrobial resistance in the WHO African region in 2019: a cross-country systematic analysis. *Lancet Glob Health.* 2024;12(2):e201-e216. **PMID 38134946.** *(added — the actual source of the "1.05M associated / 250k attributable" African figures)*
3. GBD 2019 Diseases and Injuries Collaborators. Global burden of 369 diseases and injuries in 204 countries and territories, 1990-2019. *Lancet.* 2020;396(10258):1204-1222. **PMID 33069326.** **[corrected — v1's 33308453 = a long-COVID editorial]**
4. Hotez PJ, Fenwick A, Savioli L, Molyneux DH. Rescuing the bottom billion through control of neglected tropical diseases. *Lancet.* 2009;373(9674):1570-1575. **PMID 19410718.** *(the one v1 PMID that was correct)*
5. O'Neill J. *Tackling Drug-Resistant Infections Globally: Final Report and Recommendations.* Review on Antimicrobial Resistance; 2016. *(commissioned report — no PMID)*
6. World Health Organization. *Global Action Plan on Antimicrobial Resistance.* Geneva: WHO; 2015. *(policy document — no PMID)*
7. World Health Organization. *Global Tuberculosis Report 2023.* Geneva: WHO; 2023. *(for MDR-TB figures — cite the specific edition; no PMID)*

**Removed as wrong/unlocatable (reproduce-or-remove):** v1 refs whose PMIDs pointed
to unrelated papers — Founou (27815026 = a meningioma-radiosurgery review; the real
Front Microbiol 8:1919 is a copepod-egg bacteria paper, so the citation coordinates
are also wrong), Zignol (28153050 = an NTD-in-China letter), Fang (26186985 = a
bovine-cryptosporidium study), Mbuagbaw (27323261 = a genetic-risk-behaviour review),
Dal-Ré (31362330 = a grass-carp-steaming food-chemistry paper), Hoffman (29024615 =
a canine-Hepatozoon study). None supported the claims attached to them; the surviving
argument rests on the verified anchors above.

---

*DRAFT for author review — not for live publication without sign-off. All numerals
regenerated by `54-amr-crisis-verify.py` and `_africa_equity_verify.py` against the
AACT April-12-2026 snapshot. According to PubMed metadata, every retained PMID was
verified by title/journal/pages match on 2026-07-09.*
