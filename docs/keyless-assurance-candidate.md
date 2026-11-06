# E156 mandatory keyless assurance and Pages dependency — 31 October 2026

Status: **PR development only**. No new authenticated production release or Pages deployment is asserted.

## Scope and signer

HMAC is retired as a REQUIRED E156 badge/publication mechanism. Every new
E156 release rejects badges containing legacy `signature` or `signed_at`
HMAC marks (even when an old secret happens to exist). Historical artifacts
are NOT modified, and Meta-Harness held-out identifier privacy controls are
unaffected. HMAC-only consumers must migrate to explicit verification of
Sigstore bundles rather than relying on unauthenticated legacy marks.

All new E156 badges must be signed using Cosign keyless GitHub OIDC and
verified on the original signed bytes against the exact certificate identity
`https://github.com/mahmood726-cyber/e156/.github/workflows/assurance.yml@refs/heads/master`
and OIDC issuer `https://token.actions.githubusercontent.com`. Missing,
empty, symlinked or tampered bundles and wrong signer identities refuse.
The PR OIDC exercise signs synthetic bytes only, NOT production badges.

## Same-source publication gate — issue #85

The privileged `master` assurance job must pass full corpus/zero-skip tests,
real DOI checks, pinned Sentinel, keyless sign AND verify, a second verified
dashboard build, final Sentinel rescan, commit/push and exact remote/master
HEAD/clean-tree check. Only THIS successful job's exact verified workspace can
be packaged; the deploy job has `needs: assurance` and cannot fetch a
different commit. No failed, skipped or pending assurance run can deploy its
artifact through the new dependent job.

**Admin action still required**: GitHub's existing independent branch-source
Pages publishing is not stopped merely by adding code. An owner/admin must
switch **Settings → Pages → Build and deployment → Source → GitHub Actions**,
then protect the `github-pages` environment to permit only `master`, and
only after confirming those settings set repository Actions variable
`E156_PAGES_ACTIONS_READY=true`. Until then the new packaging/deployment
steps are intentionally disabled; any old public Pages build MUST NOT be
called assured. The connected GitHub integration does not expose the
administrative Pages-source API, so these settings have not been changed.

The dependent Pages artifact uses the same checked, verified and pushed tree.
The released badge's cryptographic bundle remains the true authenticity
evidence; the HTML display is not proof without external bundle verification.
A successful unit test, synthetic OIDC canary, or old Pages build never
substitutes for a verified source/production release.

## Acceptance and boundaries

- Exact-final-head Ubuntu and Windows CI with zero silent skips and adversarial tests.
- Genuine hosted OIDC synthetic positive, tamper/wrong signer/issuer/missing
  bundle negatives and production keyless badge verification.
- GitHub-enforced protections and normal expected-head merge; verify
  post-merge `master` CI separately.
- Owner-admin Pages source switch and successful new Pages deployment only
  after the above evidence, with failures reported individually.
- Full signed Windows/Linux Sentinel→Overmind/TruthCert/memory→E156→Meta-Harness
  canary is a SEPARATE gate, NOT established by this PR.
- Preserve protected E156 AGENTS.md, YOUR REWRITE/SUBMITTED, original DOI
  sources, frozen clinical protocols, privacy and historical signatures.

Primary references:
- https://docs.sigstore.dev/cosign/signing/signing_with_blobs/
- https://docs.sigstore.dev/cosign/verifying/verify/
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
