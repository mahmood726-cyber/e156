# E156 keyless assurance candidate — 31 October 2026

Status: **development-only draft; do not merge or publish until the gates below pass.**

## Problem and proposed authenticated alternative

The existing master assurance workflow requires an authentic CI-only HMAC secret,
`E156_ASSURANCE_HMAC_KEY`. Its absence correctly prevented the HMAC gate from
claiming success. The GitHub Actions workflow already contains a separate,
mandatory Sigstore/Cosign keyless signer backed by GitHub OIDC and a verifier
pinned to the E156 repository, `master` workflow identity and OIDC issuer.

This candidate offers two explicitly different paths:

1. **HMAC available:** run the unchanged fail-closed HMAC signing and
   verification, followed by mandatory Sigstore keyless signing and verification.
2. **HMAC unavailable:** refuse badges carrying unverified legacy HMAC signature
   or signed-at fields, then require the same non-vacuous Sigstore keyless signer
   and exact workflow-identity verification before continuing.

There is **no invented HMAC key, no unsigned-success fallback, no skipped
Sigstore verification**, and no automatic re-issuance of historical signatures.
A keyless Cosign bundle proves the signed bytes were emitted under the pinned
GitHub Actions identity; it is not interchangeable with a previously issued
HMAC signature for clients that explicitly require HMAC verification.

## Non-negotiable release and publication gates

- Full exact-head Ubuntu and Windows tests, including missing-badge, malformed,
  stale-HMAC, symlink and wrong-identity/ref/issuer failures.
- A genuine GitHub-hosted OIDC/Cosign positive path using current source and a
  real negative with a modified badge or mismatched identity.
- Live DOI, pinned Sentinel and source integrity checks must all succeed first.
- GitHub branch protections and normal expected-head merge must be satisfied.
- **Issue #85 remains a separate blocker:** GitHub Pages currently has an
  independent publishing source. A successful keyless assurance workflow must
  gate publication of the **same verified files and commit** before the public
  site is represented as assured. GitHub Pages owner/admin configuration may be
  required. Do not claim a green Pages build is cryptographic assurance.
- Existing HMAC-only consumers must either continue using the authentic legacy
  key or explicitly adopt verification of the published Sigstore bundles.
- No changes to the rewrite workbook, human YOUR REWRITE/SUBMITTED fields,
  patient information, historical certificates or signed records.

## What is static versus verified dynamically

| Component | What is pinned/static | Required dynamic evidence |
|---|---|---|
| Signer identity | E156 repository, master, assurance.yml, GitHub OIDC issuer | Valid Fulcio certificate and transparency bundle on exact badge bytes |
| HMAC mode | Legacy signer/verifier unchanged | Authentic secret exists; signing and verification succeed |
| Keyless mode | Reject legacy-HMAC marks when no key | Sigstore sign-blob and identity-bound verify-blob succeed |
| Release gate | DOI/Sentinel/assurance workflow source | Passing current-head CI, source checks and deployment dependency |
| Scientific claims | Existing badge contents and evidence fields | Independent scientific validation remains separate and unproven |

Official references:
- https://docs.sigstore.dev/quickstart/quickstart-cosign/
- https://docs.sigstore.dev/cosign/verifying/verify/
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

This draft is an authenticated **alternative under evaluation**, not evidence
that the previous failed HMAC job has been repaired or that production Pages is
securely gated.
