# Multi-Persona Review Prompt

Review the E156 body as five personas and produce one JSON file matching `templates/multipersona_review_template.json`.

Required personas:

- `clinician`: practical clarity
- `statistician`: numerical honesty
- `methods_editor`: structure discipline
- `skeptic`: overclaim and causality check
- `reader`: flow and readability

For each persona:

- choose exactly one verdict: `pass`, `revise`, or `block`
- include a short `reviewer_id`
- include a `signed_at` timestamp
- write concise notes
- list required actions only if something must change

Review principles:

- Judge the frozen 156-word body, not the future full manuscript.
- Flag overclaim if interpretation outruns the stated evidence.
- Flag structure drift if sentence roles are blurred.
- Flag unclear denominators, effect scales, or intervals.
- Flag awkward flow that harms screenshot readability.

Overall gate logic:

- any `block` => overall `block`
- else any `revise` => overall `revise`
- else overall `pass`
