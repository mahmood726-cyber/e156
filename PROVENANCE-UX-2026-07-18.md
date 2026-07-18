# Provenance UX for RapidMeta — total transparency without overwhelm

**Date:** 2026-07-18
**Status:** research + design + worked mock. **No live app modified.**
**Deliverables:** this file · `F:\E156\provenance-mock\provenance-ux-mock.html` · `F:\E156\provenance-mock\bedaquiline-death-record.json`
**Lane:** claimed in `F:\E156\SHARED-LANE-NOTES.md`. `rapidmeta-finerenone`, `bias-adjusted-nma-adv`, `F:\E156\tournament` were read-only throughout.

---

## 0. The frame, and what the evidence did to it

The starting thesis: *published metas are unreconstructable because they are not transparent; every field we make mandatory and visible is one whose absence broke reconstruction.*

That thesis survived contact with the evidence, but it sharpened in a way worth stating up front. I expected the failure mode to be **suppression** — the number exists, the paper won't show its receipt. What I actually found in two worked examples is **structural absence and estimand ambiguity**:

- Bedaquiline C208: the registry's dedicated all-cause-death field is **`null`**, and 25 posted serious-event terms contain no death term. The number isn't hidden. It was never put there.
- HARMONY: the MACE **event counts do not exist anywhere in the registry record**. All 21 posted outcomes are rates. The counts live only in the journal article.
- Bedaquiline again: "deaths" resolves to **three different correct numbers** depending on which source and which estimand — 10 vs 2 (FDA, ITT, during-or-after-discontinuation), 6 vs 1 (CT.gov, discontinuation-attributed-to-death), absent (CT.gov AE module).

So the design target is not "show the receipt for the number." It is **"show which number this is, from which source, under which definition, as of which date — and make disagreement visible instead of resolving it silently."** A UI that renders one authoritative figure per cell is *structurally incapable* of being honest about this data. That single conclusion drives everything below.

---

## 1. Research — what others actually do

Every claim in this section carries a fetched source. Where a strand could not verify something, that is stated rather than smoothed over — the unverified list is in §8.

### 1.1 The convergent shape: three tiers

Marker → excerpt panel → full source. Independently arrived at by Wikipedia, Our World in Data, distill.pub, scite, and MAGICapp. This is the answer to "transparent but not overwhelming," and it is not controversial — it is what everyone who has taken the problem seriously has built.

### 1.2 Cochrane / systematic review — the closest analog

| Source | Finding | Link |
|---|---|---|
| **RoB 2** (Handbook ch.8) | Mandates the justification be a **verbatim quotation**: *"Brief, direct quotations from the text of the study report should be used whenever possible."* Also requires recording all sources consulted, and a reason whenever the author overrides the algorithm's proposed judgement. | [Handbook ch.8](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-08) |
| **robvis** | **The chain breaks here.** The input data frame is study × domain × overall × weight. There is **no column for the supporting quote at all**, and plots are "static ggplot2 objects, not interactive." The mandated receipt is structurally discarded before the figure most readers see. | [CRAN vignette](https://cran.r-project.org/web/packages/robvis/vignettes/Introduction_to_robvis.html) · [rob_traffic_light ref](https://mcguinlu.github.io/robvis/reference/rob_traffic_light.html) |
| **GRADE SoF** (Handbook ch.14) | Reason for a rating lives in a **footnote**, not the cell. But guidance itself prefers inlining: *"Enter the information for readers directly into the table if possible."* Downgrades are **typed**: domain × severity (`serious` −1 / `very serious` −2 / `extremely serious` −3) × quantifier (all/majority/minority/some). | [Handbook ch.14](https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-14) |
| **iSoF** (Epistemonikos) | Layered SoF where users *"'drill-down' for more information by scrolling over terms, concepts or **interactive footnotes**"*, and each outcome is viewable in several simultaneous renderings (plain language / absolute numbers / graphic / relative). | [Cochrane Colloquium 2015](https://abstracts.cochrane.org/2015-vienna/interactive-summary-findings-table-isof) |
| **MAGICapp** | *"the user decides the level of detail… can dig down into layers of information, **all the way to the primary study data** that is underlying the effect estimates."* Architecture is **unique IDs per element**, which is what makes drill-down and embeddable widgets possible. EtD splits **`Research evidence` from `Additional considerations`** — sourced fact vs panel judgement, as separate fields. | [magicevidence.org](https://magicevidence.org/magicapp/) · [features](https://help.magicapp.org/support/solutions/articles/201000062728-our-list-of-features) |
| **RevMan** | Stores **arm-level events/totals**, not just the computed effect — so every estimate is re-derivable. Note the scoping subtlety: RoB2 domain 1 is study-level, domains 2–5 are **outcome-level**; a display that flattens both mis-attributes. | [RevMan KB](https://documentation.cochrane.org/revman-kb/enter-study-data-manually-260702485.html) |

**The robvis finding is the one to internalise.** The field is collected, mandated, stored — and then dropped by the visualization layer. That is precisely how RapidMeta would fail if provenance were treated as a data-model feature rather than a rendering requirement.

### 1.3 Inline citation with preview

| Source | Finding | Link |
|---|---|---|
| **Wikipedia** | Three distinct systems. The load-bearing asymmetry: **Page Previews shows *"a portion of the first paragraph"*; Reference Previews shows *"the full content of the reference."*** Summaries truncate; receipts do not. Reference Tooltips default dwell 200ms, supports nesting. | [Page Previews](https://www.mediawiki.org/wiki/Page_Previews) · [Extension:Popups](https://www.mediawiki.org/wiki/Extension:Popups) · [Reference Tooltips](https://www.mediawiki.org/wiki/Reference_Tooltips) |
| **Wikipedia `{{Citation needed}}`** | Absence gets a **typed, dated, countable** marker (`|reason=`, `|date=July 2026`) feeding a maintenance category — **580,650 articles** at fetch time. The gap is queryable at corpus scale *because* it is structured. | [Citation needed](https://en.wikipedia.org/wiki/Wikipedia:Citation_needed) |
| **Our World in Data** | Verified against live metadata JSON. Per-origin fields: `producer`, `citationFull`, `urlMain`, **`dateAccessed` ≠ `datePublished`**, `license{name,url}`. Plus **`processingLevel: "major"`** (machine-readable tier) and a separate **`descriptionProcessing`** free-text field for what OWID itself did. Producer-truth and processor-truth never blend. | [OWID metadata reference](https://docs.owid.io/projects/etl/architecture/metadata/reference/) |
| **distill.pub** | Verified from `template.v2.js` source. Bibliography is **embedded JSON inside the page** — the receipt renders with zero network dependency. `HoverBox` grants **300ms grace on trigger mouseout, 500ms on panel mouseout**, specifically so the mouse can travel *into* the box and click the link inside. | [template.v2.js](https://distill.pub/template.v2.js) |
| **scite.ai** | Citation statements carry **verbatim text + typed stance (supporting/contrasting/mentioning) + a confidence percentage** — three fields, not one. Corpus is ~92% "mentioning", which is itself the argument for showing the statement rather than the tally. ⚠️ *All scite.ai URLs returned HTTP 403; this is from the QSS paper landing page and library guides, not a live report.* | [QSS 2(3):882–898](https://digitalcommons.unl.edu/scholcom/247/) · [ERAU guide](https://guides.erau.edu/scite-ai/smart-citations) |

### 1.4 Provenance / receipts

| Source | Finding | Link |
|---|---|---|
| **ClinicalTrials.gov** | Verified against live API v2. Every date is a struct with a **`type: ACTUAL \| ESTIMATED`** discriminator — epistemic status stamped on the scalar. Every AE term carries **`sourceVocabulary: "MedDRA 18.0"`** — vocabulary versioned at term level. Analyses carry **`estimateComment: "All Empagliflozin divided by Placebo"`** — ratio direction is an explicit field, not a convention. `moreInfoModule.limitationsAndCaveats` gives caveats a structured home. | [study data structure](https://clinicaltrials.gov/data-api/about-api/study-data-structure) |
| **OpenTrials** | **Dead** — *"an archived project… no longer active."* Design still worth stealing: three-state completeness signalling — **green present / amber submitted-but-not-validated / red outstanding** — and an explicit goal to *"identify and flag inconsistencies in data on the same feature of the same trial in different places."* | [opentrials.net](http://opentrials.net/) · [Trials 17:164](https://pmc.ncbi.nlm.nih.gov/articles/PMC4825083/) |
| **Nanopublications** | **Four** named graphs, not three: head / assertion / **provenance** / **publication info**. Provenance attaches to `:assertion`; pubinfo attaches to the nanopub itself — *who vouches for the claim* and *who published the record* are separately addressable. **Trusty URIs** content-hash the bundle. | [nanopub.net guidelines](https://nanopub.net/guidelines/working_draft/) |
| **W3C PROV-O** | **`prov:wasQuotedFrom` already exists** — a subproperty of `wasDerivedFrom` for an entity created *"by repeating some or all of the original."* That is excerpt-as-receipt, already standardized. Plus the Qualification Pattern to reify a derivation with its activity. | [PROV-O](https://www.w3.org/TR/prov-o/) |
| **Europe PMC / SciLite** | Verified against a live API response. Anchoring is a **TextQuoteSelector — `prefix` / `exact` / `suffix`, character-offset-free**, so it survives re-pagination and PDF-vs-XML rendering. The live sample contained a visible false positive ("soma" tagged as a Clinical Drug) — **catchable only because the excerpt was shown.** | [AnnotationsApi](https://europepmc.org/AnnotationsApi) |
| **Covidence / DistillerSR / EPPI-Reviewer** | **The live gap.** Covidence shows *"a supporting quote from the PDF… alongside the suggestion"* — **only for AI suggestions**, and only on a narrow field set. Human extraction records **no anchor at all**; the PDF is merely adjacent. The tool keeps more evidence about the machine than about the human, which is backwards for auditability. EPPI-Reviewer is the only one where select-text→attach-code is the primary workflow. | [Covidence AI extraction](https://support.covidence.org/help/ai-feature-extraction-suggestions) · [EPPI-Reviewer](https://eppi.ioe.ac.uk/cms/Default.aspx?tabid=3822) |

### 1.5 Deep-link mechanics

| Mechanism | Verdict | Notes |
|---|---|---|
| **W3C Text Fragments** `#:~:text=[prefix-,]start[,end][,-suffix]` | Mechanism good, payload fragile | **92.09% global support.** *The "Firefox lags" premise is outdated — Firefox shipped in 131 (Oct 2024).* **Must percent-encode `-`, `&`, `,`** — clinical prose is full of hyphens ("double-blind") and each silently corrupts the directive. Requires **user activation**, so it cannot be validated by automation. |
| **PDF `#page=N`** | Only durable PDF locator | Chrome + pdf.js honour it; **Safari unverified — no authoritative Apple doc found.** `#search=` and `#highlight=` are **Acrobat-only, dead in browsers.** `page` must precede `zoom`/`view`. Absolute index: a reposted PDF with a new cover sheet shifts every stored page silently. |
| **CT.gov anchors** | **Verified live** | `?tab=results#adverse-events`, `#participant-flow`, `#outcome-measures`, `#baseline-characteristics`, `#more-information`. Anchor names **map 1:1 onto API v2 module names.** |
| **PMC** | Best table linking anywhere | **`/articles/{PMCID}/table/T1/`** is a real server-rendered page with its own URL — verified with a 404 negative control. Per-**cell** anchors exist (`#t1c7`). Section ID schemes vary by publisher (`#sec2` vs `#s2A`) — **read them from the document, never assume.** |
| **FDA** | URL excellent, page anchor moderate | `drugsatfda_docs/nda/{year}/{ApplNo}Orig1s000{Type}.pdf`. No named destinations. Many are **image scans with no text layer** — page number is the only handle *and is unverifiable*. |
| **W3C Web Annotation selectors** | **The right storage format** | `TextQuoteSelector{exact,prefix,suffix}`, `TextPositionSelector`, `FragmentSelector`, `RangeSelector`, `refinedBy`. Structurally **isomorphic to Text Fragments** — a stored selector *compiles into* a `#:~:text=` URL. |
| RFC 5147 / EPUB CFI | Not applicable | `text/plain` only / EPUB only. But RFC 5147's `length=`/`md5=` **integrity check** idea is worth stealing. |

**Two traps that cost me time and will cost anyone else the same:**

1. **Never validate an SPA anchor with `curl`.** I checked CT.gov for `#adverse-events`, found nothing in the served HTML, and "corrected" my own record to remove the anchors. That was wrong — CT.gov is an Angular SPA that creates anchors at runtime, and live browser navigation lands exactly on target (`rectTop: 0`). Absence from served HTML is **not** absence at runtime. Same family as the [verify-the-feed](#) lesson: I validated the check, not the thing.
2. **Never trust HTTP 200 from an SPA.** CT.gov returns 200 for `?tab=bogusvalue`. Always run a negative control with a deliberately invalid ID — PMC's `/table/TZZ99/` correctly 404s, which is what makes its 200s meaningful.

---

## 2. The three-layer spec

### Layer 1 — GLANCE (default, always visible, no interaction)

```
10 / 79  vs  2 / 81   ● FDA reviewer   FDA Summary Review · as of 2012-10-25
```

Four elements, nothing more:
1. **The value**, tabular-numerals.
2. **Provenance-tier chip** — coloured dot + 2-word tier name.
3. **Source in ~3 words.**
4. **`as_of` date** when the datum is a count or a cumulative event tally (see §3, field 7).

**Tiers.** Deliberately about *evidentiary independence*, not prestige:

| Tier | Meaning | Why this rank |
|---|---|---|
| **1 — Regulator reviewer** | FDA/EMA reviewer's own analysis | Independent re-analysis of patient-level data by a party with subpoena power and no publication incentive |
| **2 — Registry, structured** | CT.gov / EudraCT posted results | Sponsor-submitted but schema-constrained and legally mandated |
| **3 — Journal** | Peer-reviewed publication | Sponsor-authored, peer-filtered, selection-prone |
| **4 — Derived / imputed** | Anything RapidMeta computed | Ours. Always the lowest tier, never silently promoted |

Tier is **not** confidence. A tier-1 source can be wrong and a tier-3 right. Tier answers *"who is telling me this, and what were their incentives?"*

**Rule:** the glance layer must never show a value whose tier chip is missing. An unattributed number is a bug, not a default.

### Layer 2 — EXPAND (one hover or click, resolves in place)

Following iSoF's interactive footnote and Wikipedia's *full*-content reference preview:

1. **Verbatim excerpt** — the receipt. Monospace, visually quoted, **never truncated** (Wikipedia's asymmetry: summaries truncate, receipts don't).
2. **Section label in words** — `FDA NDA 204-384, Deputy Division Director Summary Review → §8.0 Summary of Clinical Safety → deaths-by-trial table → row "Trial C208 Stage 2 / Deaths" — printed p.13 (PDF p.14)`. Prose, not a selector. The reader must be able to find it by eye in a paper copy.
3. **Line / row identifier** — `Table row "Trial C208 Stage 2 / Deaths"`, or `manuscript lines 312–313`.
4. **Full provenance tag** + `as_of` + estimand qualifiers.
5. **Disagreement panel, when other sources exist** — see §2.1.

**Interaction requirements, from distill's source:**
- The panel **must be enterable** — grace timeout ≥300ms on trigger mouseout, ≥500ms on panel mouseout. *A hover card that vanishes when you reach for its link is a hover card whose deep link does not exist.*
- Touch: tap toggles, `stopPropagation`, body-tap dismisses.
- Keyboard: focusable trigger, `Esc` closes, panel in the tab order.

### Layer 3 — GO TO SOURCE (deep link, lands on the number)

Cascade per source type, best first, degrading gracefully:

| Source | 1st | 2nd | 3rd | Floor |
|---|---|---|---|---|
| **CT.gov** | `?tab=results#adverse-events` | `?tab=results` | `/study/{NCT}` | API v2 module path |
| **PMC** | `/articles/{PMCID}/table/T1/` | `#T1` / `#t1c7` | `#:~:text=` on the value | `/articles/{PMCID}/` |
| **FDA** | `…{ApplNo}Orig1s000{Type}.pdf#page=N` | bare PDF URL | Drugs@FDA overview by ApplNo | ApplNo + doc type + page as a rebuild recipe |
| **Paywalled journal** | **PMC copy if one exists** | `https://doi.org/…` | `#T1`/`#Tab1` opportunistically | DOI + stored selector + the value itself |

**Storage principle — the single most important recommendation here:**

> **Store selectors; synthesize URLs at render time.** Never store a rendered deep-link URL as the only record. Store a stable document identifier plus a *set* of redundant locators (structural + quote-based + value), and compile the URL on demand. This turns a site redesign into a re-render problem instead of data loss.

Carry the **value itself** alongside the locator, so that when every link rots the reader still sees the number and can search for it. Graceful degradation, not a dead link.

### 2.1 The disagreement panel — the part no one else has

Nothing surveyed does this. OpenTrials *intended* to (*"identify and flag inconsistencies… in different places"*) and died before shipping it. This is where RapidMeta can be genuinely first, and it is the direct answer to the bedaquiline case.

When ≥2 sources give different values for the same conceptual datum, layer 2 shows **all of them, side by side, each with its own tier / excerpt / estimand**, plus a plain-language line on *why they differ*. Never a single reconciled figure.

Rules:
- **Never auto-resolve.** Show the pooled choice and mark the others as not-pooled, with the reason.
- **Distinguish "conflict" from "different estimand."** Bedaquiline's 10-vs-6 is *not* a conflict — it is two different questions. Labelling it a conflict would be a second error on top of the first.
- **`null` is not `0`.** An empty registry field renders as *"not reported at this source"*, never as a zero. This is the bug that would silently zero out C208's mortality.

### 2.2 The absent state, as a first-class citizen

From Wikipedia's `{{Citation needed}}` (typed, dated, countable) and OpenTrials' amber tier. Three states that must never collapse into one:

| State | Meaning | Renders as |
|---|---|---|
| **Not sought** | We didn't look | *"not checked"* — and it should be rare enough to be a defect |
| **Not in schema** | Source has no such field | *"source does not report this"* |
| **Present but empty** | Field exists, left blank | *"reported as blank by sponsor"* ← **this is evidence about the trial** |
| **Present, unvalidated** | Extracted, not yet checked | amber |

Only the third is evidence. Collapsing it into "missing" is how C208 reads as zero deaths.

---

## 3. Capture-at-source fields — irrecoverable later

These must be written **in the same pass that reads the number**. Reconstructing them afterwards means re-reading the source, which is the cost the whole project exists to avoid.

| # | Field | Example | Why irrecoverable |
|---|---|---|---|
| 1 | `url_deep` | `…204384Orig1s000SumR.pdf#page=14` | Needs the resolved page/anchor you were on |
| 2 | `page_or_anchor` | `{pdf_page: 14, printed_page_label: 13}` | **Store both.** `#page=` is physical; the header prints 13. One alone breaks either the link or the citation |
| 3 | `excerpt_verbatim` | *"Trial C208 Stage 2 \| Deaths \| … N=79 \| 10 (12.6%) \| N=81 \| 2 (2.5%)"* | The single highest-value field. Carries the estimand for free (see below) |
| 4 | `section_label` | `§8.0 Summary of Clinical Safety → deaths-by-trial table` | Requires document context you no longer have |
| 5 | `line_or_row` | `Table row "Trial C208 Stage 2 / Deaths"` / `manuscript lines 312–313` | Lost the moment you close the document |
| 6 | `provenance_tag` | `FDA_REVIEWER` | Trivial at read time, guesswork later |
| **7** | **`as_of`** | **`2012-10-25` ("4-month safety update")** | **New — see below** |

### The seventh field, and why the original six aren't enough

Bedaquiline forced this. From the FDA Statistical Review (PDF p.13, verbatim):

> *"Based on a 4-month safety update report submitted in October, 2012, in the ITT population there were 10 and 2 deaths during the trial or after discontinuation from the trial in the TMC207 and placebo groups, respectively."*

The count **10** is a function of the **submission cut-off**, not of the trial. At the original submission it was lower. Two reviews quoting "C208 deaths" from different data locks are **not in conflict** — but without `as_of` they look like they are, and someone will "reconcile" them. **A count carried without its data-lock date is uncomparable.** Mandatory for any count or cumulative event tally.

### Why the excerpt beats the parsed number

That one quoted sentence carries, for free: the **population** (ITT), the **window** (during the trial *or after discontinuation*), the **lock** (October 2012), the **effect** (10.2%, 95% CI [2.1%, 19.7%]), and the **test** (p = 0.0167). A parsed `{events: 10, n: 79}` throws all of it away. **Store the sentence; parse from it; keep the sentence.**

### Recommended storage shape

Don't invent a vocabulary — `prov:wasQuotedFrom` and W3C `TextQuoteSelector` already exist.

```json
{
  "value": {"events": 10, "n": 79},
  "as_of": "2012-10-25",
  "source": {"type": "fda", "applNo": "204384", "docType": "SumR", "year": 2012},
  "structural": {"pdf_page": 14, "printed_page_label": 13,
                 "section_label": "§8.0 Summary of Clinical Safety"},
  "quote": {"type": "TextQuoteSelector",
            "exact": "10 (12.6%)", "prefix": "N=79 ", "suffix": " N=81"},
  "provenance_tag": "FDA_REVIEWER",
  "estimand": {"population": "ITT", "window": "during trial or after discontinuation"}
}
```

`structural` and `quote` are redundant **on purpose** — when the PDF is reposted and pages shift, the quote relocates it; when the text is re-typeset, the page still works. Add a checksum (OWID's `dataChecksum`, nanopub's Trusty URIs, RFC 5147's `md5=`) so silent edits are detectable.

---

## 4. Copyright rule

| Source class | Rule |
|---|---|
| **US Government** (FDA, CT.gov) | Public domain. Quote full table rows and paragraphs freely. |
| **OA CC-BY** | Free with attribution. Quote table rows and multi-sentence passages. |
| **OA CC-BY-NC-ND** (e.g. the HARMONY accepted manuscript) | Attribution required. **Single data line only.** Short quotation for verification is quotation, not a derivative — but do not reproduce tables wholesale. |
| **Paywalled / all-rights-reserved** | **One data line, never a paragraph.** Enough to verify the number, never a substitute for the article. Prefer routing to a PMC copy when one exists. |

**Operating rule:** the excerpt exists to let a reader *verify a number*, not to let them *avoid the source*. If an excerpt is long enough to substitute for reading the paper, it is too long. Store the licence with the excerpt so the renderer can enforce a length cap per class.

---

## 5. HARMONY as a glance — with a correction

The brief asked to show HARMONY reduced to a glance:

> `"338/428 — CT.gov Results, [excerpt], [deep link]"`

**The number is right. The source attribution is wrong.** This matters more than a nitpick — it is the exact failure the design prevents, occurring in the specification of the design.

**Verified against the live record (NCT02465515):** `338` and `428` appear in the CT.gov JSON **only** inside zip codes, geo-coordinates and a DOI. All **21** posted outcome measures are rates or changes. The primary outcome is `unitOfMeasure: "Events per 100 person years"` — **4.57 vs 5.87**, with denominators 4731 / 4732. **The event counts are not in the registry at all.**

They are in the paper. Verified by local extraction of the OA accepted manuscript (PDF p.16, manuscript lines 312–313):

> *"The primary composite endpoint occurred in 338 of 4731 patients (7.1%; 4.57 events per 100 person-years) in the albiglutide group and in 428 of 4732 patients (9.0%; 5.87 events per 100 person-years)…"*

and again in Table 2 (PDF p.32): `Primary composite outcome 338 (7.1) 4.57 428 (9.0) 5.87 0.78`.

**Corrected glance:**

```
338 / 4731  vs  428 / 4732     ● Journal     Lancet 2018, Table 2
```

**Expand reveals the cross-check that makes this cell strong:**

| Quantity | Lancet | CT.gov | Agree? |
|---|---|---|---|
| Events per 100 py, albiglutide | 4.57 | 4.57 | exact |
| Events per 100 py, placebo | 5.87 | 5.87 | exact |
| Event counts | 338 / 428 | **absent** | n/a |

The registry independently confirms the paper's rates to two decimals — a genuine arithmetic check on a tier-3 source using a tier-2 one — while supplying none of the counts. That is a far more useful thing to show a reader than a single attributed number, and it is invisible without the disagreement panel.

**What the reconstruction actually cost, and what the glance replaces:** locating the trial, pulling the v2 JSON, discovering the primary outcome is a rate, searching the full record for the counts, finding only zip-code matches, locating an OA copy, extracting it locally, and confirming against two separate pages. The three-layer record collapses that to one line plus one expand — *and* it records the fact that the registry cannot supply the counts, which the reconstruction learned and would otherwise have thrown away.

---

## 6. Bedaquiline mock record

Full record: `F:\E156\provenance-mock\bedaquiline-death-record.json`. Interactive mock: `F:\E156\provenance-mock\provenance-ux-mock.html`.

**Glance:**
```
10 / 79  vs  2 / 81     ● FDA reviewer     FDA Summary Review · as of 2012-10-25
```

**Expand:**
- **Excerpt** (FDA Summary Review, PDF p.14 / printed p.13): `Trial C208 Stage 2 | Deaths | Randomized, placebo-controlled, 24 week exposure | N=79 | 10 (12.6%) | N=81 | 2 (2.5%)` — with the table's own attribution line, *"Source: FDA Medical Officer's Review"*.
- **Section label:** `FDA NDA 204-384, Deputy Division Director Summary Review → §8.0 Summary of Clinical Safety → deaths-by-trial table → row "Trial C208 Stage 2 / Deaths"`
- **Corroboration** (§6.0, PDF p.9): *"he expressed concern regarding an imbalance in deaths seen in Study 208 Stage 2 and recommended that the imbalance in deaths should be conveyed in the product labeling."*
- **Data lock** (Statistical Review, PDF p.13, quoted in §3 above), with the sensitivity analysis from p.4: excluding 3 deaths gives *"a mortality rate for bedaquiline of 9/79 (11.4%)"*.
- **Disagreement panel:**

| Source | Bedaquiline | Placebo | What it counts |
|---|---|---|---|
| FDA Summary Review | 10 / 79 | 2 / 81 | All-cause death, ITT, during or after discontinuation |
| CT.gov participant flow | 6 / 79 | 1 / 81 | Discontinuation *attributed to* death, during treatment |
| CT.gov AE death field | `null` | `null` | Empty for all four arms |

- **Why 10 ≠ 6 — mechanism, not error:** the FDA figure includes deaths *after discontinuation*; CT.gov's flow field can only count deaths that **are** the discontinuation event. The registry is structurally incapable of carrying the rest.

**Deep links** (all verified HTTP 200): FDA `…SumR.pdf#page=14` · CT.gov `?tab=results#participant-flow` · CT.gov `?tab=results#adverse-events`.

**A dangling citation, recorded honestly.** The FDA table attributes itself to the *Medical Officer's Review* — but `204384Orig1s000MedR.pdf` returns **404**; that review is not independently posted for this NDA (`SumR`, `StatR`, `CrossR`, `ClinPharmR`, `OtherR` are). **Rule: `url_deep` must point at the document you actually read, never at the document it cites.** Provenance chains have dangling ends and the record must show where yours stops.

---

## 7. Cost, and what breaks

### Cost

| Item | Cost | Note |
|---|---|---|
| CT.gov capture | **~zero** | Deep link, excerpt, section label and anchor are all derivable from the v2 JSON already being pulled. Module names map 1:1 to page anchors |
| FDA capture | **~zero marginal** | Page number is known in the same Read/vision pass that reads the count. Capturing it later means re-reading the PDF |
| Journal capture | **moderate** | Needs an OA copy and local extraction. Highest value (counts often exist *only* here) and highest cost |
| Storage | negligible | ~1–2 KB per datum |
| Render | low | Static HTML/CSS + one toggle. Mock is 15 KB, self-contained, zero dependencies |
| **Retrofit of existing apps** | **the real cost** | Capture-at-source cannot be backfilled without re-reading every source. This is why the field list is time-critical |

### What breaks

1. **Retrofit is not possible.** The six-plus-one fields are irrecoverable by definition. Every app generated before this lands is unfixable without a full re-extraction. **This is the argument for adopting the field list now even if the UI ships later.**
2. **Link rot.** FDA paths are decade-stable and the documents immutable; CT.gov NCT IDs are permanent; DOIs are permanent; **publisher URLs are not.** Mitigated by storing selectors and synthesizing URLs, plus carrying the value itself.
3. **Page drift.** `#page=N` is an absolute index — a repost with a new cover sheet shifts everything silently. Mitigated by the redundant quote selector and a stored `Content-Length`.
4. **Text fragments cannot be automatically validated.** They require user activation, so any link-checker reports false negatives on every one. Validate by string-matching the decoded quote against the fetched body — never by driving a browser.
5. **Scanned FDA PDFs have no text layer** — no excerpt, no text fragment, page number unverifiable. Record that explicitly rather than implying precision you don't have.
6. **The robvis failure mode is the one to watch.** A justification field that the data model collects and the renderer drops is worse than none, because it looks like diligence. **Any glance-layer artifact that cannot carry the excerpt must at minimum carry a pointer to it.**
7. **Tier chips can become theatre.** If everything renders tier 1 they signal nothing. Audit the tier distribution across the corpus periodically; a distribution that isn't broad is a bug.
8. **Excerpt length creep.** Copyright and usefulness push the same way: cap it. If the excerpt substitutes for the source, it is too long.
9. **The disagreement panel could overwhelm** — the exact failure the brief warns against. Mitigation: it stays **collapsed by default** and appears in layer 2 only. Layer 1 shows one number, one tier, one source. Disagreement is one click away, never in your face.

---

## 8. Honest limitations

**Could not verify:**
- **Live SPA observation.** iSoF (`isof.epistemonikos.org`) and MAGICapp guideline pages are client-rendered and returned empty/shell bodies. Their layer structure is documented from vendor docs and a peer-reviewed colloquium abstract — **not from watching them run.**
- **scite.ai.** Every scite URL returned **HTTP 403**. Description is from the QSS paper landing page and library guides; **no live scite report was seen.** The ~92.6/6.5/0.8% distribution is from a search snippet, not a primary source.
- **DistillerSR PDF anchoring.** Supported only by a press-release phrase. No technical documentation. **Vendor claim, not verified capability.**
- **EPPI-Reviewer storage model** — feature exists; manual was an unextractable 7 MB PDF.
- **Elicit click-to-quote** — product claim verified, specific UI behaviour asserted by third parties only.
- **Safari PDF `#page=`** — no authoritative Apple documentation found. Do not assume.
- **FDA PDF `#page=` rendering** — inferred from viewer support, not observed (harness intercepted as download).
- **Text fragment real-user scroll** — structurally unverifiable in automation.
- **Crossref component DOIs** for tables/figures — no authoritative source located.

**My own error, recorded.** I checked CT.gov section anchors with `curl`, found none in the served HTML, and edited my record to remove them as unsupported. That was wrong — the anchors are created at runtime by the SPA and resolve correctly under live browser navigation. **I validated my check instead of the thing, and briefly made a correct record incorrect.** Reverted; trap documented in §1.5 and in the JSON record.

**The mock is structurally verified, not visually verified.** Div balance (38/38), blockquote balance, single `</script>`, no placeholders, no `None` leaks, no hardcoded local paths, self-contained (zero external assets), all four outbound links HTTP 200. But the Browser pane blocks `file://`, `127.0.0.1` and external origins by policy, so **I never saw it render.** It should be opened in a normal browser before any design decision rests on its appearance.

**Not claimed:** that this improves extraction accuracy. It improves *auditability* — the ability to check a number against its source cheaply. Those are different things, and only the second is evidenced here.

---

## ⚠️ CORRECTION 2026-07-18 (REMEDIATION lane) — QUOTE THE SCHEMA AS A **DESIGN**, NOT A MEASURED CAPABILITY

Red-teamed in `ADVERSARIAL-REDTEAM-2026-07-18.md` §6: **WEAKENED.** The verdict there is
worth repeating exactly: *"The provenance schema is excellent and it has never once been
tested against a cell that could fail."*

Measured from this lane's own outputs:

| artifact | count |
|---|---|
| `excerpt_verification.json` — data points with a verified verbatim excerpt | **12** |
| distinct apps covered | **3** |
| of those 12, `ok: true` | **12 (100%)** |
| `transparency_ledger_final.jsonl` — apps | 62 |
| `transparency_ledger_final.jsonl` — **total `data_points`** | **12** |
| corpus in the shadow run | 373 |
| live app corpus | ~1,448 |

All 14 provenance fields are populated 12/12 — but the deep-link-plus-excerpt layer exists
for roughly **0.8% of the shadow corpus and ~0.2% of the live corpus**, with a **100% success
rate and zero recorded failures**.

**This is the house's own "a gate must be able to fail" lesson.** A verifier that has never
returned a failure has not been shown to discriminate. And the failure mode is already known
— **from this lane's own two findings**:

- **HARMONY:** the MACE counts **do not exist in CT.gov at all** (the registry posts only
  rates). A registry deep-link cannot source that cell.
- **Bedaquiline C208:** CT.gov's structured death field is **`null` for all four arms**, and
  none of the 25 serious-event terms is a death term.

⇒ **The two cells anyone would most want to cite are exactly the two that cannot carry a
registry deep-link.** The 12 verified cells are not a random sample; they are the cells that
happened to be verifiable — selection on the outcome, one layer up.

> **Quote as:** "reconstructable by construction" is **demonstrated on 12 data points across
> 3 apps** (~0.2% of the live corpus) with **no failure cases recorded**. The base rate at
> which an arbitrary stored cell can carry a true deep-link **plus** a verbatim excerpt is
> **unmeasured**. Until a sample *including failures* is drawn, this is a **design**, not a
> measured capability.

**What survives intact and should still be adopted:** the **capture-at-source field list**
(§3), plus `as_of` and `ascertainment_window`. Those are time-critical and irrecoverable
after the extraction pass — and the `as_of` requirement was independently re-derived by two
other lanes on the same day (the bedaquiline data-lock splice). The schema being
under-evidenced is **not** an argument against capturing the fields; it is an argument
against quoting a coverage number the lane never measured.
