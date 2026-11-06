"""Fail-closed source-rights hold for E156's privileged production workflow.

No Synthesis permission manifest or private decision log is available. The
production job must stop before checkout, cache reads, DOI network traffic,
Sentinel article scanning, or publication artifacts. These mutation tests use
only the workflow YAML and do not authorize any article processing.
"""
from __future__ import annotations

from pathlib import Path
import re

import pytest
import yaml


WORKFLOW = (
    Path(__file__).resolve().parents[1]
    / ".github" / "workflows" / "assurance.yml"
)


def require_precheckout_hold(workflow: str) -> None:
    root = yaml.safe_load(workflow)
    # A top-level env/defaults block can change the first Bash process before
    # its hold script runs (for example via BASH_ENV).
    assert "env" not in root and "defaults" not in root
    jobs = root["jobs"]
    assert set(jobs) == {"assurance", "deploy-pages"}
    assurance = jobs["assurance"]
    # A self-hosted or expression-selected runner may execute pre-job hooks
    # and reuse workspace/cache content before the first refusal step.
    assert assurance.get("runs-on") == "ubuntu-latest"
    assert "if" not in assurance and "continue-on-error" not in assurance
    # A job-level environment can inject BASH_ENV into the first bash process.
    assert "env" not in assurance and "defaults" not in assurance
    # Job containers/services can execute code before any step-level refusal.
    assert "container" not in assurance and "services" not in assurance
    steps = assurance["steps"]
    assert len(steps) >= 2
    hold = steps[0]
    # Prevent hook or shell-startup injection on the first step. Merely
    # finding "exit 1" somewhere in an arbitrary script does not prove a hold.
    assert set(hold) == {"name", "shell", "run"}
    assert hold["name"] == "SOURCE_RIGHTS_HOLD — fail closed before publication processing"
    assert hold["shell"] == "bash"
    commands = [line.strip() for line in hold["run"].splitlines() if line.strip()]
    assert len(commands) == 2
    assert re.fullmatch(r"printf '%s\\n' 'SOURCE_RIGHTS_HOLD: [^']*' >&2", commands[0])
    assert commands[1] == "exit 1"
    assert steps[1]["uses"].startswith("actions/checkout@")

    # GitHub Actions implicitly gates ordinary steps on success(), but an
    # explicit always()/failure() can execute checkout or publication steps
    # after the hold failed. Keep the intentionally diagnostic JUnit checker,
    # and the original owner-opt-in Pages conditions, as the only exceptions.
    allowed_conditions = {
        "Refuse omitted or skipped tests (hard gate)": "always()",
        "Stage only committed assured Pages source (owner opt-in only)":
            "vars.E156_PAGES_ACTIONS_READY == 'true'",
        "Package exact assured Pages tree (owner opt-in only)":
            "vars.E156_PAGES_ACTIONS_READY == 'true'",
    }
    for step in steps[1:]:
        assert "continue-on-error" not in step
        if "if" in step:
            assert step["if"] == allowed_conditions.get(step.get("name"))
            if step["if"] == "always()":
                # A name alone is not a safety boundary: a forged diagnostic
                # step must never use always() to run DOI processing.
                assert set(step) == {"name", "if", "run"}
                assert step["run"] == (
                    'python scripts/assurance/require_corpus_results.py '
                    '"$RUNNER_TEMP/e156-assurance-junit.xml"'
                )
    deploy = jobs["deploy-pages"]
    # Keep deployment on a known ephemeral GitHub-hosted runner as well.
    assert deploy.get("runs-on") == "ubuntu-24.04"
    assert deploy.get("needs") == "assurance"
    # GitHub Actions permits job-level always() to bypass failed needs.
    assert deploy.get("if") == (
        "github.repository == 'mahmood726-cyber/e156' && "
        "github.ref == 'refs/heads/master' && "
        "vars.E156_PAGES_ACTIONS_READY == 'true'"
    )
    assert "continue-on-error" not in deploy


def test_production_refuses_source_processing_before_checkout():
    require_precheckout_hold(WORKFLOW.read_text(encoding="utf-8"))


@pytest.mark.parametrize(
    "mutation",
    [
        lambda src: src.replace("          exit 1", "          echo proceed", 1),
        lambda src: src.replace(
            "      - name: SOURCE_RIGHTS_HOLD", "      - name: renamed", 1
        ).replace("SOURCE_RIGHTS_HOLD: no reviewed", "unreviewed", 1),
        lambda src: src.replace(
            "      - name: SOURCE_RIGHTS_HOLD",
            "      - name: SOURCE_RIGHTS_HOLD\n        if: false",
            1,
        ),
        lambda src: src.replace(
            "      - name: SOURCE_RIGHTS_HOLD",
            "      - name: SOURCE_RIGHTS_HOLD\n        continue-on-error: true",
            1,
        ),
        # Old substring-only assertions accepted an entire DOI invocation before
        # the exit, an unreachable exit, or downstream always() processing.
        lambda src: src.replace(
            "          exit 1",
            "          python scripts/assurance/doi_resolver.py --repo .\n          exit 1",
            1,
        ),
        lambda src: src.replace(
            "          exit 1", "          if false; then exit 1; fi", 1,
        ),
        lambda src: src.replace(
            "      - uses: actions/checkout@",
            "      - if: always()\n        uses: actions/checkout@", 1,
        ),
        lambda src: src.replace(
            "      - name: Resolve DOIs against doi.org (live)",
            "      - name: Resolve DOIs against doi.org (live)\n        if: always()", 1,
        ),
        lambda src: src.replace(
            "        shell: bash\n", "        shell: bash\n        env:\n          BASH_ENV: /tmp/unsafe-startup\n", 1,
        ),
        # Workflow-level BASH_ENV is inherited before the first bash command.
        lambda src: src.replace(
            "jobs:\n", "env:\n  BASH_ENV: /tmp/unsafe-startup\njobs:\n", 1,
        ),
        # An always() on the dependent job defeats the failed prerequisite.
        lambda src: src.replace(
            "    if: github.repository == 'mahmood726-cyber/e156'",
            "    if: always() # github.repository == 'mahmood726-cyber/e156'",
            1,
        ),
        # The existing exception for an always() diagnostic must not be
        # available to a renamed invocation of the DOI resolver.
        lambda src: src.replace(
            'run: python scripts/assurance/require_corpus_results.py "$RUNNER_TEMP/e156-assurance-junit.xml"',
            'run: python scripts/assurance/doi_resolver.py --repo .', 1,
        ),
        # Pre-step container initialization is another execution route.
        lambda src: src.replace(
            "    runs-on: ubuntu-latest\n",
            "    runs-on: ubuntu-latest\n    container: ubuntu:latest\n", 1,
        ),
        # Selecting a persistent or untrusted runner allows pre-step hooks and
        # cached content to run before SOURCE_RIGHTS_HOLD is evaluated.
        lambda src: src.replace(
            "    runs-on: ubuntu-latest\n",
            "    runs-on: self-hosted\n", 1,
        ),
        lambda src: src.replace(
            "    runs-on: ubuntu-24.04\n",
            "    runs-on: self-hosted\n", 1,
        ),
        # Workflow-level defaults should not be a mutable shell-startup hook.
        lambda src: src.replace(
            "jobs:\n", "defaults:\n  run:\n    shell: bash\njobs:\n", 1,
        ),
        lambda src: src.replace(
            "      - uses: actions/checkout@",
            "      - uses: actions/checkout@",
            1,
        ).replace(
            "    steps:\n      # Run before checkout",
            "    steps:\n      - uses: actions/checkout@v4\n      # Run before checkout",
            1,
        ),
    ],
)
def test_source_rights_hold_bypass_mutations_are_refused(mutation):
    source = WORKFLOW.read_text(encoding="utf-8")
    planted = mutation(source)
    assert planted != source
    with pytest.raises(AssertionError):
        require_precheckout_hold(planted)
