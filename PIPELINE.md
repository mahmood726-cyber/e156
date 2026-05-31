# e156 capsule pipeline

How the **living evidence capsules** are built from live data by a chain of small,
fail-closed command-line tools. The reference implementation is the pairwise
SGLT2-inhibitor heart-failure capsule (`flagship/sglt2-hf-capsule.html`); the same
machinery builds any review.

> **The AI steps run inside the host agentic CLI.** Screening and data extraction
> are performed by the orchestrating agent (Claude Code / Gemini CLI) — that agent
> *is* the LLM, so no separate API key is needed. The deterministic tools fetch the
> records; the agent reads them and writes the decision/extraction JSON; the inject
> tools commit those into the capsule.

## One command

```bash
python scripts/run_pipeline.py --config pipelines/sglt2-hf.json
```

This chains the six steps below. It is **idempotent** given the same live data
(a full re-run reproduces the capsule byte-for-byte). Use `--only a,b`, `--skip a`,
or `--dry-run`. Any step's non-zero exit stops the run.

## The steps (and the tool for each)

| # | Step | Tool | What it does |
|---|------|------|--------------|
| 1 | **Register protocol** | `scripts/register_protocol.py` | Commits the protocol (the commit SHA + GitHub date are the tamper-evident, public pre-registration — an open PROSPERO alternative) and injects the permalink into the capsule. |
| 2 | **Live registry** | `scripts/fetch_ctgov.py` | Pulls real ClinicalTrials.gov API v2 records → structured registry summaries + condition/intervention/design/enrolment/status; the capsule verifies analysed-N against registered enrolment. |
| 3 | **Live abstracts** | `scripts/fetch_pubmed.py` | Fetches the primary papers' real titles/abstracts via NCBI E-utilities (by `NCT=PMID` map; the map avoids attaching a sub-analysis). |
| 4 | **Live DOIs/citations** | `scripts/fetch_openalex.py` | Real DOIs (so references link directly), citation counts and open-access status from OpenAlex. |
| 5 | **AI screening** | agent → `scripts/inject_screening.py` | The host agent reads each record's live abstract / registry summary, applies the pre-registered eligibility criteria, and writes `data/screening-decisions.json`; the tool validates + injects it. |
| 6 | **AI extraction** | agent → `scripts/inject_extraction.py` | The host agent extracts the fields each abstract supports (N, EF, design, outcome…) with the *verbatim source sentence*; written to `data/extraction-live.json` and injected. |

Each fetch/inject tool writes its data between `/*X_START*/ … /*X_END*/` markers in
the capsule, and the capsule **prefers live data over its illustrative placeholders**,
badging the difference (`live · ClinicalTrials.gov`, `live · PubMed PMID …`, `live agent`).

## Provenance (committed)

Every fetch/agent step writes a committed JSON under `data/`, so the inputs are
reproducible and timestamped by their commit:

- `data/ctgov-records.json`, `data/pubmed-records.json`, `data/openalex-records.json` — raw live pulls.
- `data/screening-decisions.json`, `data/extraction-live.json` — agent outputs, each with a `_meta` block (who, when, against which criteria, method).

## Add a new review

1. Write `protocols/<review>-protocol.md` (PICO, eligibility, search, synthesis plan).
2. Build the capsule from the flagship template; keep the `/*…_START/END*/` markers and the `CTGOV_LIVE` / `PUBMED_LIVE` / `OPENALEX_LIVE` / `SCREEN_LIVE` / `EXTRACT_LIVE` slots.
3. Write `pipelines/<review>.json` — `capsule`, `protocol`, `author`, `ncts`, `pmid_map`, optional `mailto`, `screening`, `extraction`.
4. Run `run_pipeline.py --only protocol,ctgov,pubmed,openalex` to acquire data.
5. As the host agent: read the fetched records + the protocol criteria, write the screening and extraction JSONs.
6. Run `run_pipeline.py --only screening,extraction` to inject them.

## Honest boundaries

Abstract-only extraction can supply the outcome, N, EF, design and primary endpoint.
**Full Table-1 demographics, Risk-of-Bias adjudication and the GRADE judgements need
the full text and human review** — the capsule labels these as such rather than
fabricating them, and reaches **Gold** only on independent reproduction.
