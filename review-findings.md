## Multi-Persona Review: E156 Rewrite Workbook (290 entries)
### Date: 2026-03-31
### Reviewers: Statistical Methodologist, Domain Expert, Format Compliance, Writing Quality, Completeness Auditor, Security Auditor
### Summary: 5 P0, 10 P1, 6 P2

---

#### P0 -- Critical

- **P0-1** [Format]: `apply_rewrites.py` line 51 regex searches for `"YOUR REWRITE (exactly 156 words, 7 sentences):"` but workbook uses `"YOUR REWRITE (at most 156 words, 7 sentences):"`. **Script will silently find ZERO rewrites.**
  - Fix: Update regex in apply_rewrites.py to match "at most"
  - **FIXED**: Regex already corrected to "at most" (verified line 51)

- **P0-2** [Format]: 91 of 175 rewrites (52%) have wrong sentence count (!= 7). User's natural writing fragments 7 sentences into 8-12 shorter ones.
  - Fix: Batch merge — run a sentence-count checker, then merge short fragments back into 7 sentences per entry
  - **FIXED**: All 325 rewrites now have exactly 7 sentences. Fixes: capitalized lowercase-after-period boundary sentences (10 entries) and avoided "al." abbreviation-protection false positives (3 entries)

- **P0-3** [Stats]: BayesianMA (entry 10) reports "posterior OR mean was -0.53" — OR cannot be negative. This is a log-OR value.
  - Fix: Change to "posterior log-OR mean was -0.53" or exponentiate to OR = 0.59 (95% CrI 0.28 to 1.14)
  - **FIXED**: Changed "posterior OR mean" to "posterior log-OR mean" in config.json body and sentences[3].text

- **P0-4** [Domain]: 7 capsule entries have header-body mismatch — TITLE/TYPE/ESTIMAND/DATA still say "Reproducibility Capsule" and "documentation proportion" while YOUR REWRITE contains real scientific content with different estimands.
  - Affected: [5] AfricaRCT, [16] CausalSynth, [18] chat2, [19] chatpaper, [49] everything-claude-code, [81] mahmood726-cyber.github.io, [105] MetaReproducer, [120] my-python-project, [124] nmapaper111025, [133] Paper2.111025
  - Fix: Update header fields to match rewritten content (or flag apply script to ignore headers)
  - **FIXED**: Updated TITLE, ESTIMAND, and DATA for all 10 affected entries to match rewrite content

- **P0-5** [Completeness]: 6 duplicate project pairs (same project at two paths):
  - AutoGRADE: [8] + [9], CausalSynth: [16] + [17], EvidenceHalfLife: [52] + [245], MetaReproducer: [105] + [106], Pairwise70: [129] + [130], advanced-nma-pooling: [4] + [171]
  - Fix: Deduplicate — keep the substantive version, remove the stub/capsule
  - **FIXED**: Removed 6 entries ([8], [16], [105], [130], [171], [245]). Kept substantive versions. Total count 331 -> 325

---

#### P1 -- Important

- **P1-1** [Format]: 17 rewrites exceed 156 words (range 157-163). Entries: TDA_MA (163), truthcert-denominator-phase1 (163), metaoverfit-paper (160), PredictionGap (160), Multilevelerror (159), rmstnma (159), TGEP_Development (159), plus 10 more.
  - Fix: Trim each to ≤156 words

- **P1-2** [Writing]: Typos changing meaning in 4 entries:
  - [6] AlMizan: "exemples" → "examples"
  - [116] MLMResearch: "applyies" → "applies"
  - [114] MethodsSuite: "aht" → "that"
  - [115] MLM501: "us" → "was"

- **P1-3** [Writing]: Grammar errors in 7+ entries:
  - [9] AutoGRADE: "There is guided assessments" → "There are"
  - [115] MLM501: "to constructed" → "to construct"
  - [7] Asa: "Our question was can..." → "Can..."
  - [103] MetaRep: "Can a new clinical trial will replicate" → "Can a new clinical trial replicate"
  - [144] DOAC: "We looked at three randomized trials...compared" → broken structure

- **P1-4** [Writing]: Missing space after period in 6 entries: MetaRegression, MetaReproducer, metasprint-dose-response, PRISMAChecker, pub-bias-simulation, truthcert-meta2-prototype
  - Fix: Add space after every period

- **P1-5** [Writing]: Double spaces in 28 entries scattered throughout workbook
  - Fix: Global find-and-replace double spaces → single space

- **P1-6** [Format]: S1 not phrased as question in 6 entries (ends with period not "?"): BenfordMA, metaoverfit, NNTMapper, OverlapDetector, registry_first_rct_meta, repo100
  - Fix: Add question marks

- **P1-7** [Stats]: Dataset count ambiguity — Pairwise70 appears as 501, 473, 403, or 307 reviews depending on entry, without stating filter criteria.
  - Fix: Each entry should state its filter (e.g., "307 reviews with k≥5 from the 501-review Pairwise70 corpus")

- **P1-8** [Format]: validate_e156.py line 86 has dead code: `words <= 156 if strict_words else words <= 156` — both branches identical, --max-156 flag does nothing.
  - Fix: Restore intended behaviour or remove the flag

- **P1-9** [Format]: Spec prompt shell (spec.md line 121) says "exactly 156 words" but Hard Body Rules (line 9) says "At most 156 words". Inconsistent.
  - Fix: Update prompt shell to say "at most 156 words"

- **P1-10** [Format]: 23 of 75 CT.gov auto-generated bodies have 8 sentences (not 7). These came from config.json with sentence split issues.
  - Fix: Merge 8-sentence CT.gov bodies down to 7

---

#### P2 -- Minor

- **P2-1** [Writing]: "This" as sentence starter overuse — 25 entries, 54 instances. Creates vague, AI-sounding prose.
  - Fix: Replace pronoun with specific noun

- **P2-2** [Domain]: Systematic "Can" → "Will"/"Should" weakening in ~15 rewrites changes feasibility questions into predictions.
  - Fix: Prefer "Can" for demonstrations; "Will" only for prospective predictions

- **P2-3** [Writing]: Sentence fragments (4-5 words) in 10 entries feel choppy.
  - Fix: Merge with adjacent sentences

- **P2-4** [Completeness]: 7 entries are not research: clinic-site, everything-claude-code, mahmood726-cyber.github.io, my-python-project, private-website, 3dvitreous-grapher, Scripts
  - Fix: User to decide: keep or remove

- **P2-5** [Security]: Identifiable info in bodies: "London Cardiology Clinic", "Wimbledon", "mahmood726". Not sensitive but deanonymizing if workbook published.
  - Fix: Review before public sharing

- **P2-6** [Security]: 2 WSL path leaks in DATA fields: DPMA, ROBMA show `/mnt/c/Models/...`
  - Fix: Convert to Windows paths

---

#### False Positive Watch

- Statin RR 0.74 — correct per CTT meta-analysis
- Asa 100% sensitivity with 85 cases — CI 95.7% is correct Clopper-Pearson
- Fragility index median 3 — consistent with published literature
- HKSJ worse PI coverage than DL — plausible (HKSJ adjusts CIs not PIs)
- Clayton copula theta formula — correct per lessons.md
