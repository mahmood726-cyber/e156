# E156 Micro-Paper Specification v0.1

## Purpose

E156 is a compact, executable micro-paper standard for meta-analyses and related evidence syntheses. The body is a stand-alone meaning layer. Data, code, interactive app links, DOI, version, and validation details sit outside the body.

## Core body rules

* Exactly 7 sentences
* Exactly 156 words in final release mode
* Single paragraph
* No title inside the body
* No headings inside the body
* No citations or references inside the body
* No links inside the body
* No metadata inside the body

## Sentence schema

1. Question: population/condition, intervention or exposure or comparison, and main endpoint.
2. Dataset: studies, participants, scope, or follow-up.
3. Method: synthesis method and analytic level.
4. Primary result: one main estimate with interval.
5. Robustness: heterogeneity, sensitivity, subgroup, consistency, or stability.
6. Interpretation: plain-language meaning with restrained wording.
7. Boundary: limitation, scope limit, or caution.

## Outside note block

* App
* Data
* Code
* DOI
* Version
* Date
* Optional validation status

## House style

* One idea per sentence
* Numbers over adjectives
* No hype
* No causal overreach unless justified by design and evidence
* Limitation mandatory
* Paragraph must make sense when screenshot alone

## Production workflow

1. Draft at 165 to 180 words.
2. Reduce to 156 words.
3. Run multi-persona review.
4. Freeze body.
5. Attach outside note block.

## Multi-persona review

* Clinician: practical clarity
* Statistician: numerical honesty
* Methods Editor: structure discipline
* Skeptic: overclaim and causality check
* Reader: flow and readability

## Validation checklist

* 7 sentences
* 156 words
* sentence roles preserved
* result sentence contains estimate and interval
* limitation sentence present
* interpretation does not outrun evidence
* outside note block present

## Prompt shell

Write a 7-sentence micro-paper body in exactly 156 words. Do not include a title, headings, citations, references, links, or metadata. Sentence 1 states the question. Sentence 2 states the evidence base. Sentence 3 states the method. Sentence 4 reports the primary numerical result with interval. Sentence 5 reports robustness or heterogeneity. Sentence 6 gives a restrained interpretation. Sentence 7 states a limitation or boundary. The paragraph must stand alone.
