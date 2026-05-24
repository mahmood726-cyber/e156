# E156 AI-harness — academic grounding

This document maps the E156 / Sentinel / Overmind verification architecture onto the active 2025–26 academic literature on agentic verification, reproducibility assessment, and pre-commit/pre-push gating. The goal is to position E156 inside a named research conversation rather than as an isolated piece of infrastructure.

## Architectural correspondence

| E156 component | Academic vocabulary | Reference |
|---|---|---|
| Sentinel + Overmind as a pair | **"Agent-as-a-Judge with environment access"** — a judge agent that doesn't just read text but actually inspects the repo state, runs tests, and queries external registries | [arXiv 2508.02994](https://arxiv.org/abs/2508.02994) |
| Overmind verdict taxonomy (CERTIFIED / PASS / UNVERIFIED / REJECT / FAIL / SKIP) | **Agentic Reproducibility Assessment (ARA)** — a graded reproducibility certificate with explicit "incomplete" states distinct from pass/fail | [arXiv 2605.02651](https://arxiv.org/abs/2605.02651) |
| Sentinel as a pre-push git hook with BLOCK / WARN / INFO severity | **Verify-Before-Commit** — gating mutations at the version-control boundary rather than after merge | [arXiv 2604.08401](https://arxiv.org/abs/2604.08401) |
| E156 capsule self-checking — the "agreement with itself" principle | **e156 Assurance Standard** (this project) — four risk classes × three-tier badge system; see `F:\e156\docs\assurance-standard.md` |

## Citations the architecture builds on

1. **Agent-as-a-Judge with environment access** ([arXiv 2508.02994](https://arxiv.org/abs/2508.02994)). The paper that names the pattern we already implement: a judge agent that has tool access to the artifacts it's evaluating, not just their text. Sentinel (commit-time, repo-scope) + Overmind (nightly, portfolio-scope) together realize this with a 29-rule defect-rule engine and a 6-witness verifier.

2. **ARA: Agentic Reproducibility Assessment** ([arXiv 2605.02651](https://arxiv.org/abs/2605.02651)). Defines a graded reproducibility certificate. Overmind's distinction between CERTIFIED (full pass) and UNVERIFIED (passes but numerical baseline missing — explicitly NOT a release pass per the 2026-05-06 SKIP-as-pass incident fix) directly matches the ARA taxonomy.

3. **Verify-Before-Commit** ([arXiv 2604.08401](https://arxiv.org/abs/2604.08401)). Argues for gating at the version-control boundary. Our `.git/hooks/pre-commit` → `check_workbook_commit.py` and the Sentinel pre-push hook are exactly this pattern; we additionally surface a `SENTINEL_BYPASS=1` audit log so bypasses are traceable.

4. **BadScientist** ([arXiv 2510.18003](https://arxiv.org/abs/2510.18003)). Five-strategy fabrication test pack for evaluating reproducibility frameworks. Phase 2 of the E156 Assurance Standard will implement these five strategies as Sentinel test fixtures so a fabrication-detection capability becomes a published claim of the framework rather than an internal hope.

## What we deliberately don't do

**Vanilla multi-agent debate** ([arXiv 2601.22297](https://arxiv.org/abs/2601.22297)). The 2025–26 literature increasingly shows that MAD often loses to majority voting on the same task budget. The defect-rule-driven Sentinel is the stronger architecture for our use case (deterministic patterns over consensus-of-personas). If we add personas later, they will be tool-anchored (each persona constrained to query a specific source) rather than freely-debating LLMs.

## Where E156 is ahead of the field (per the prior research scan)

- **Per-claim atomic granularity** in systematic reviews. The SR community is still at paper- or trial-level granularity; only ~2 % of published systematic-review work explores full-process automation (per [arXiv 2504.20113](https://arxiv.org/abs/2504.20113)). E156's 156-word atomic claim + capsule structure operates at a finer grain.
- **DOI-bound provenance for AI-generated artifacts**. LLMOps has tracing; academic publishing has DOIs; the join of the two — a DOI that resolves to a self-auditing AI-curated capsule — does not have an established public analogue.
- **Portfolio-scale reconciliation across capsules**. `F:\ProjectIndex\reconcile_counts.py` enforces cross-registry agreement (manifest ⟷ INDEX.md ⟷ workbook ⟷ on-disk paths) on 600+ projects with fail-closed semantics. No public analogue found.

## What we should adopt next (Phase 2 of the improvement plan)

- **Patronus Lynx-8B** or **Vectara HHEM-2.1-Open** as a sub-second small-classifier tier in a bronze/silver/gold prose-hallucination stack (deterministic regex → small classifier → LLM judge).
- **UKGovernmentBEIS/inspect_ai** as the transcript format for Overmind nightly runs, so eval traces are inspectable in standard tooling.
- **BadScientist** five-strategy fabrication test pack as a Sentinel rule suite, with documented capability claims.
- **refchecker** (Mark Russinovich) for the citation-cascade rule (CrossRef → Semantic Scholar → OpenAlex) instead of hand-rolling.

## Provenance

- Architecture vocabulary collected from a prior research scan dated ≤ 2026-05-20 (user email of that date documents the mapping).
- arXiv URL HEAD-check 2026-05-24: all five citations above return HTTP 200.
- This document is intentionally short. The full Assurance Standard lives at `F:\e156\docs\assurance-standard.md`.
