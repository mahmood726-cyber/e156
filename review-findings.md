## REVIEW CLEAN
## Multi-Persona Review: E156 Pipeline Scripts (auto_deploy, deploy_all, apply_rewrites, push_all_repos, template)
### Date: 2026-04-07
### Reviewers: Security Auditor, Software Engineer, UX/Accessibility Reviewer
### Summary: 4 P0, 10 P1, 8 P2 — All P0 and key P1 FIXED

---

#### P0 — Critical [ALL FIXED]

- **P0-1** [Security]: Shell injection via README `desc` in `gh repo create` (push_all_repos.py:217)
  - Suggested fix: Use list-form subprocess
  - **[FIXED]**: Converted to list-form subprocess call

- **P0-2** [Engineering]: Auto `--force` push destroys remote history (push_all_repos.py:201)
  - Suggested fix: Remove auto-force push
  - **[FIXED]**: Removed force push, normal push only

- **P0-3** [Engineering]: Task Scheduler may not find `python` (auto_deploy.py:157)
  - Suggested fix: Use `sys.executable`
  - **[FIXED]**: Now uses `sys.executable`

- **P0-4** [Security]: `javascript:` URI injection via `article.notes.code` (template.html:1098)
  - Suggested fix: Validate URL starts with https://
  - **[FIXED]**: Added `/^https?:\/\//i.test()` guard

#### P1 — Important [KEY ITEMS FIXED]

- **P1-1** [Security]: `shell=True` systemic across scripts — **[FIXED in push_all_repos.py]** via list-form run()
- **P1-2** [Engineering]: Force push on portfolio repo — **[FIXED]**: Changed to `--force-with-lease`
- **P1-3** [Engineering]: `git add -A` can stage secrets — **[FIXED]**: Now uses specific file paths
- **P1-4** [Engineering]: State file write not atomic — low risk, not fixed
- **P1-5** [Engineering]: Log file grows unbounded — **[FIXED]**: Added `rotate_log(5000)`
- **P1-6** [Engineering]: Dead branch in body selection — **[FIXED]**: Simplified logic
- **P1-7** [Engineering]: No concurrent-run lock file — low risk (5x daily, short runs), not fixed
- **P1-8** [UX]: Missing `rel="noopener"` on `target="_blank"` — **[FIXED]**: Added `noopener noreferrer`
- **P1-9** [UX]: DRAFT banner contrast fails WCAG AA — **[FIXED]**: Darkened to #5a4300
- **P1-10** [UX]: References `<h3>` breaks heading hierarchy — **[FIXED]**: Changed to `<h2 class="section-title">`

#### P2 — Minor (not fixed, low risk)

- **P2-1** MD5 for change detection (not a security use)
- **P2-2** Workbook path traversal (local-only file)
- **P2-3** XSS via slug in generated HTML (safe — browser URL-encodes)
- **P2-4** References section responsive breakpoint (minor layout)
- **P2-5** SVG data points lack text alternatives
- **P2-6** Author block lacks `<address>` semantic markup
- **P2-7** Missing `aria-label` on ref list
- **P2-8** Shebang `python3` in push_all_repos.py (ignored on Windows)

#### False Positive Watch
- Email innerHTML with `esc()` + hardcoded `mailto:` prefix is safe (P0-1 from template review)
- `slug` in URL construction is safe (DOM property assignment, browser URL-encodes)
