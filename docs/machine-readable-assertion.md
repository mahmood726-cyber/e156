# E156 Machine-Readable Assertion

A small structured file that ships **alongside** each E156 micro-paper and carries
its single primary estimand as data. The prose body stays the human artifact; the
assertion makes the central claim **independently checkable** — disclosure taken
one step further into verifiability.

- Schema: [`schemas/e156-assertion.schema.json`](../schemas/e156-assertion.schema.json) (JSON Schema draft 2020-12)
- Worked example: [`schemas/example-reduced-dose-doacs.assertion.json`](../schemas/example-reduced-dose-doacs.assertion.json)

## Why this fits truth-first

It only ever makes the claim **more falsifiable**, never more confident:

1. **The estimand is bound to its data.** `provenance.data_binding.sha256` hashes
   the exact study-level rows the pool was computed from. An auditor recomputes
   the pool and checks `assertion.point` / `assertion.ci` match. A wrong number
   can now be *caught mechanically*, not just eyeballed.
2. **The assertion is bound to one body.** `paper.body_sha256` pins the 7-sentence
   text. Edit the body and the hash no longer matches — the assertion is *known
   stale* rather than silently mismatched.
3. **Direction is forced into a field.** `favours_lower` makes the author state
   which way the effect cuts, instead of leaving it to prose tone.
4. **Identifiers are typed.** PMID / DOI / NCT have regex patterns; the publish
   step DOI-resolves them (per the citation-misattribution lesson). No free-text
   "approximately NCT…".
5. **No overclaim surface added.** There is exactly one estimand slot — the format's
   hard rule — so the file cannot smuggle in a second headline number.

## Nanopublication mapping

The three top-level blocks mirror the nanopublication model so an E156 assertion
can later be lifted to RDF/TriG without re-modelling:

| Nanopublication graph | E156 block | Holds |
|---|---|---|
| Assertion | `assertion` | the one estimand: measure, scale, point, CI, direction |
| Provenance | `provenance` | data hash, study/participant counts, search date, source article |
| Publication info | `pubinfo` | version, date, GRADE certainty, validation state, DOI, license |

The Outside Note block of the paper is the human-readable shadow of this file;
fields are intended to agree (`Type`↔`paper.variant`, `Primary estimand`↔
`assertion.estimand_label`, `Certainty`↔`pubinfo.certainty`, etc.). A future
check can assert that agreement automatically.

## Filling the two hash placeholders

The example ships with `body_sha256` and `data_binding.sha256` set to all-zeros
**on purpose** — they are computed at release, not hand-written. Do not publish an
assertion with zero-hashes (that is an unpopulated-token violation; a validator
should reject it). Compute them from the repo root:

```python
import hashlib, json, pathlib

def sha256_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

# body: hash the exact released 7-sentence paragraph (one line, no trailing newline)
body = "In adults receiving extended anticoagulation ... de-intensify therapy."
print("body_sha256:", hashlib.sha256(body.encode("utf-8")).hexdigest())

# data: hash the bound rows file referenced by rows_uri
print("data sha256:", sha256_file("releases/<slug>/data/major_bleeding_rows.json"))
```

## Validating an assertion

Offline, no network (matches the E156 / GitHub-Pages no-CDN rule):

```bash
python -m pip install jsonschema   # one-time, dev only
python - <<'PY'
import json, jsonschema
schema = json.load(open("schemas/e156-assertion.schema.json"))
inst   = json.load(open("schemas/example-reduced-dose-doacs.assertion.json"))
jsonschema.validate(inst, schema)   # raises on any contract breach
print("assertion valid")
PY
```

A release-gate check should additionally fail closed when:
- either hash is all-zeros (unpopulated token),
- `pubinfo.validation != "PASS"`,
- the CI is mis-ordered — `not (ci.low <= point <= ci.high)` or `ci.low > ci.high`.
  JSON Schema cannot compare two sibling instance values, so the schema's `allOf`
  enforces scale/sign/bounds but this ordering check must live in the gate,
- a recompute of the pool from `rows_uri` disagrees with `assertion.point`/`ci`
  beyond rounding tolerance,
- any of PMID/DOI/NCT is present but does not resolve.

These four are the difference between "we attached a JSON file" and "we attached a
claim someone else can refute."
