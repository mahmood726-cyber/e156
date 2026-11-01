"""Mutations proving that new Pages publishing depends on real same-run assurance.

These structural checks do not establish that GitHub Pages settings were changed
or that a privileged production deployment has run.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "assurance.yml"


def problems(wf: dict) -> list[str]:
    jobs = wf.get("jobs", {})
    assure = jobs.get("assurance", {})
    deploy = jobs.get("deploy-pages", {})
    steps = assure.get("steps", [])
    dsteps = deploy.get("steps", [])
    names = [s.get("name", "") for s in steps]
    required = [
        "Reject unverified legacy HMAC marks before mandatory keyless signing",
        "Sigstore keyless-sign badges (public, transparency-logged)",
        "Verify Sigstore badge bundles and workflow identity (hard gate)",
        "Build the public assurance dashboard (served by existing Pages)",
        "Sentinel rescan generated publication artifacts (hard gate)",
        "Commit refreshed cache, badges, signatures, dashboard",
        "Refuse stale or uncommitted assured publication source",
        "Package exact assured Pages tree (owner opt-in only)",
    ]
    if any(names.count(n) != 1 for n in required):
        return ["missing or duplicated publication gate"]
    issues = []
    if [names.index(n) for n in required] != sorted(names.index(n) for n in required):
        issues.append("wrong mandatory gate ordering")
    def named(n):
        return steps[names.index(n)]
    if named(required[0]) != {"name": required[0],
                             "run": "python scripts/assurance/require_keyless_safe_badges.py --repo ."}:
        issues.append("unverified HMAC accepted")
    if named(required[2]) != {"name": required[2],
                             "run": "python scripts/assurance/verify_sigstore_badges.py --repo ."}:
        issues.append("bundle/identity verifier bypassed")
    if "--require-keyless-verified" not in named(required[3]).get("run", ""):
        issues.append("dashboard can assert unverified authenticity")
    if named(required[7]).get("if") != "vars.E156_PAGES_ACTIONS_READY == 'true'":
        issues.append("owner opt-in bypass on upload")
    if named(required[7]).get("with", {}).get("path") != ".":
        issues.append("artifact source diverges from assured checkout")
    stale = named(required[6])
    if stale.get("if") or stale.get("continue-on-error"):
        issues.append("stale HEAD check optional")
    if stale.get("id") != "assured_head" or assure.get("outputs") != {
        "assured_sha": "${{ steps.assured_head.outputs.sha }}"
    }:
        issues.append("assurance does not export verified commit SHA")
    if 'echo "sha=$local_head" >> "$GITHUB_OUTPUT"' not in stale.get("run", ""):
        issues.append("verified commit SHA not exported")
    for text in ("git status --porcelain", "git rev-parse HEAD",
                 "git ls-remote origin refs/heads/master"):
        if text not in stale.get("run", ""):
            issues.append("missing exact source/remote HEAD test")
    if deploy.get("needs") != "assurance":
        issues.append("Pages could deploy without assurance")
    condition = str(deploy.get("if", ""))
    for text in ("vars.E156_PAGES_ACTIONS_READY == 'true'",
                 "github.repository == 'mahmood726-cyber/e156'",
                 "github.ref == 'refs/heads/master'"):
        if text not in condition:
            issues.append("Pages permission/opt-in scope insufficient")
    if deploy.get("permissions", {}).get("pages") != "write":
        issues.append("Pages deployment permission missing")
    if deploy.get("environment", {}).get("name") != "github-pages":
        issues.append("unprotected deployment environment")
    if len(dsteps) != 2 or dsteps[1].get("uses") != (
        "actions/deploy-pages@d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e"
    ):
        issues.append("unreviewed Pages deploy action")
    if not dsteps or dsteps[0].get("name") != (
        "Refuse master drift after assurance before Pages deployment"
    ) or dsteps[0].get("shell") != "bash" or dsteps[0].get("if") or dsteps[0].get("continue-on-error"):
        issues.append("deployment drift refusal is absent or optional")
    else:
        guard = dsteps[0]
        if guard.get("env") != {
            "ASSURED_SHA": "${{ needs.assurance.outputs.assured_sha }}"
        }:
            issues.append("deploy job does not consume current assured SHA")
        guard_run = guard.get("run", "")
        for text in ("set -euo pipefail", "test \"$ASSURED_SHA\" != ''",
                     "git ls-remote https://github.com/mahmood726-cyber/e156.git refs/heads/master",
                     'test "$ASSURED_SHA" = "$remote_head"', "exit 1"):
            if text not in guard_run:
                issues.append("deployment lacks exact source-ref drift refusal")
                break
    if "E156_ASSURANCE_HMAC_KEY" in str(wf):
        issues.append("HMAC remains required for new E156 badges")
    return issues


def current():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def test_real_workflow_has_dependent_pages_and_no_hmac():
    assert problems(current()) == []


def test_failure_mutations_cannot_skip_assurance_or_change_source():
    baseline = current()
    kinds = ("no-needs", "wrong-needs", "unconditional", "foreign-repo",
             "no-opt-in", "no-preflight", "no-verify", "no-dashboard-gate",
             "wrong-artifact", "stale-skipped", "no-clean-source",
             "unreviewed-deployer", "missing-output", "wrong-output",
             "no-deploy-drift", "wrong-deploy-assured-ref", "no-guard",
             "optional-guard", "no-emit")
    for kind in kinds:
        bad = deepcopy(baseline)
        deploy = bad["jobs"]["deploy-pages"]
        steps = bad["jobs"]["assurance"]["steps"]
        if kind == "no-needs":
            deploy.pop("needs")
        elif kind == "wrong-needs":
            deploy["needs"] = "unreviewed-independent-job"
        elif kind == "unconditional":
            deploy["if"] = "true"
        elif kind == "foreign-repo":
            deploy["if"] = deploy["if"].replace("mahmood726-cyber/e156", "other/repo")
        elif kind == "no-opt-in":
            deploy["if"] = deploy["if"].replace("vars.E156_PAGES_ACTIONS_READY == 'true'", "true")
        elif kind == "no-preflight":
            steps[:] = [s for s in steps if not s.get("name", "").startswith("Reject unverified")]
        elif kind == "no-verify":
            next(s for s in steps if s.get("name", "").startswith("Verify Sigstore"))["run"] = "echo bypass"
        elif kind == "no-dashboard-gate":
            next(s for s in steps if s.get("name", "").startswith("Build the public"))["run"] = "echo no"
        elif kind == "wrong-artifact":
            next(s for s in steps if s.get("name", "").startswith("Package exact"))["with"]["path"] = "other/"
        elif kind == "stale-skipped":
            next(s for s in steps if s.get("name", "").startswith("Refuse stale"))["if"] = "false"
        elif kind == "no-clean-source":
            next(s for s in steps if s.get("name", "").startswith("Refuse stale"))["run"] = "echo pass"
        elif kind == "missing-output":
            bad["jobs"]["assurance"].pop("outputs")
        elif kind == "wrong-output":
            bad["jobs"]["assurance"]["outputs"]["assured_sha"] = "${{ github.sha }}"
        elif kind == "no-deploy-drift":
            deploy["steps"][0]["run"] = "echo bypass"
        elif kind == "wrong-deploy-assured-ref":
            deploy["steps"][0]["env"]["ASSURED_SHA"] = "${{ github.sha }}"
        elif kind == "no-guard":
            deploy["steps"].pop(0)
        elif kind == "optional-guard":
            deploy["steps"][0]["if"] = "false"
        elif kind == "no-emit":
            stale = next(s for s in steps if s.get("name", "").startswith("Refuse stale"))
            stale["run"] = stale["run"].replace('echo "sha=$local_head" >> "$GITHUB_OUTPUT"', "echo bypass")
        else:
            deploy["steps"][-1]["uses"] = "actions/deploy-pages@v4"
        assert problems(bad), kind
