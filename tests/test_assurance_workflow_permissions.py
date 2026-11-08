"""Workflow trust boundaries, permissions, and keyless canary contracts."""
from __future__ import annotations

from pathlib import Path
import hashlib

import pytest
import yaml


WORKFLOW = (
    Path(__file__).resolve().parents[1]
    / ".github" / "workflows" / "assurance.yml"
)


def require_production_workflow(workflow: str) -> None:
    root = yaml.safe_load(workflow)
    # PyYAML's YAML 1.1 resolver may parse the event key 'on' as True.
    # A trigger change can make a privileged workflow run in the wrong trust
    # context while all of the existing pre-checkout step checks still pass.
    assert root.get("on", root.get(True)) == {
        "workflow_dispatch": None,
        "schedule": [{"cron": "0 6 * * 1"}],
        "push": {"branches": ["master"]},
    }
    assert root.get("permissions") == {"contents": "write", "id-token": "write"}
    # A top-level env/defaults block can change the first Bash process before
    # workflow steps run (for example via BASH_ENV).
    assert "env" not in root and "defaults" not in root
    jobs = root["jobs"]
    assert set(jobs) == {"assurance", "deploy-pages"}
    assurance = jobs["assurance"]
    assert "permissions" not in assurance
    # A self-hosted or expression-selected runner may execute pre-job hooks
    # and reuse workspace/cache content before workflow steps.
    assert assurance.get("runs-on") == "ubuntu-latest"
    assert "if" not in assurance and "continue-on-error" not in assurance
    # A job-level environment can inject BASH_ENV into the first bash process.
    assert "env" not in assurance and "defaults" not in assurance
    # Job containers/services can execute code before workflow steps.
    assert "container" not in assurance and "services" not in assurance
    steps = assurance["steps"]
    assert len(steps) >= 2
    assert steps[0].get("uses", "").startswith("actions/checkout@")

    # GitHub Actions implicitly gates ordinary steps on success(), but an
    # explicit always()/failure() can execute checkout or publication steps
    # after a failure. Keep the intentionally diagnostic JUnit checker,
    # and the original owner-opt-in Pages conditions, as the only exceptions.
    allowed_conditions = {
        "Refuse omitted or skipped tests (hard gate)": "always()",
        "Stage only committed assured Pages source (owner opt-in only)":
            "vars.E156_PAGES_ACTIONS_READY == 'true'",
        "Package exact assured Pages tree (owner opt-in only)":
            "vars.E156_PAGES_ACTIONS_READY == 'true'",
    }
    for step in steps:
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
    assert deploy.get("permissions") == {"contents": "read", "pages": "write", "id-token": "write"}
    # GitHub Actions permits job-level always() to bypass failed needs.
    assert deploy.get("if") == (
        "github.repository == 'mahmood726-cyber/e156' && "
        "github.ref == 'refs/heads/master' && "
        "vars.E156_PAGES_ACTIONS_READY == 'true'"
    )
    assert "continue-on-error" not in deploy


def test_production_workflow_permissions_and_triggers():
    source = WORKFLOW.read_text(encoding="utf-8")
    require_production_workflow(source)
    # Negative controls: earlier versions checked only job/step layout, so a
    # privileged pull_request_target event or removed push gate went unnoticed.
    for before, after in (
        ("  push:\n    branches: [master]", "  pull_request_target:\n    branches: [master]"),
        ("  push:\n    branches: [master]", "  push:\n    branches: [unreviewed]"),
        ('    - cron: "0 6 * * 1"', '    - cron: "* * * * *"'),
        ("permissions:\n  contents: write", "permissions:\n  contents: read"),
    ):
        assert source.count(before) == 1
        with pytest.raises(AssertionError):
            require_production_workflow(source.replace(before, after, 1))


@pytest.mark.parametrize("mutation", [
    lambda src: src.replace(
            "      - uses: actions/checkout@",
            "      - if: always()\n        uses: actions/checkout@", 1,
        ),
    lambda src: src.replace(
            "      - name: Resolve DOIs against doi.org (live)",
            "      - name: Resolve DOIs against doi.org (live)\n        if: always()", 1,
        ),
    lambda src: src.replace(
            "jobs:\n", "env:\n  BASH_ENV: /tmp/unsafe-startup\njobs:\n", 1,
        ),
    lambda src: src.replace(
            "    if: github.repository == 'mahmood726-cyber/e156'",
            "    if: always() # github.repository == 'mahmood726-cyber/e156'",
            1,
        ),
    lambda src: src.replace(
            'run: python scripts/assurance/require_corpus_results.py "$RUNNER_TEMP/e156-assurance-junit.xml"',
            'run: python scripts/assurance/doi_resolver.py --repo .', 1,
        ),
    lambda src: src.replace(
            "    runs-on: ubuntu-latest\n",
            "    runs-on: ubuntu-latest\n    container: ubuntu:latest\n", 1,
        ),
    lambda src: src.replace(
            "    runs-on: ubuntu-latest\n",
            "    runs-on: self-hosted\n", 1,
        ),
    lambda src: src.replace(
            "    runs-on: ubuntu-24.04\n",
            "    runs-on: self-hosted\n", 1,
        ),
    lambda src: src.replace(
            "jobs:\n", "defaults:\n  run:\n    shell: bash\njobs:\n", 1,
        ),
])
def test_production_workflow_mutations_are_refused(mutation):
    source = WORKFLOW.read_text(encoding="utf-8")
    planted = mutation(source)
    assert planted != source
    with pytest.raises(AssertionError):
        require_production_workflow(planted)


# PR CI retains read-only permissions and a strictly synthetic OIDC canary.
PR_WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "assurance-pr.yml"


def require_pr_workflow(workflow: str) -> None:
    root = yaml.safe_load(workflow)
    assert isinstance(root, dict)
    assert root.get("on", root.get(True)) == {
        "pull_request": {"branches": ["master"]},
        "workflow_dispatch": None,
    }
    assert "env" not in root and "defaults" not in root
    assert root.get("permissions") == {"contents": "read"}
    jobs = root["jobs"]
    assert set(jobs) == {"assurance-tests", "keyless-oidc-canary"}
    job = jobs["assurance-tests"]
    assert "permissions" not in job
    for forbidden in ("if", "continue-on-error", "env", "defaults", "container", "services"):
        assert forbidden not in job
    assert job.get("runs-on") == "${{ matrix.os }}"
    assert job.get("strategy") == {
        "fail-fast": False,
        "matrix": {"os": ["ubuntu-24.04", "windows-2022"]},
    }
    steps = job["steps"]
    assert len(steps) > 3
    always = [step for step in steps if step.get("if") == "always()"]
    assert len(always) == 2
    assert sum(step.get("name") == "Refuse omitted, skipped, or failed test cases"
               for step in always) == 1
    checkout = steps[0]
    assert set(checkout) == {"uses", "with"}
    assert checkout["uses"] == "actions/checkout@11d5960a326750d5838078e36cf38b85af677262"
    assert checkout["with"] == {"persist-credentials": False}

    for step in steps:
        assert "continue-on-error" not in step
        condition = step.get("if")
        if condition is None:
            continue
        # Only the exact diagnostic/reporting steps can run after failure.
        assert condition == "always()"
        if step.get("name") == "Refuse omitted, skipped, or failed test cases":
            assert set(step) == {"name", "if", "shell", "run"}
            assert step["shell"] == "pwsh"
            assert [line.strip() for line in step["run"].splitlines() if line.strip()] == [
                "$report = Join-Path $env:RUNNER_TEMP 'e156-assurance-junit.xml'",
                "python scripts/assurance/require_corpus_results.py $report",
                'if ($LASTEXITCODE -ne 0) { throw "Assurance coverage gate failed" }',
            ]
        else:
            assert step.get("uses") == (
                "actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02"
            )
            assert set(step) == {"uses", "if", "with"}
            assert step["with"] == {
                "name": "assurance-junit-${{ matrix.os }}",
                "path": "${{ runner.temp }}/e156-assurance-junit.xml",
                "if-no-files-found": "error",
            }

    # This job is allowed only because it is synthetic and checkout-free.
    canary = jobs["keyless-oidc-canary"]
    # This OIDC-enabled canary must remain strictly synthetic; checking only
    # for absence of checkout does not prevent network access or arbitrary runs.
    assert set(canary) == {"name", "if", "runs-on", "permissions", "steps"}
    assert canary["name"] == "Keyless OIDC canary (synthetic, no publication)"
    assert canary["if"] == (
        "github.event_name == 'pull_request' && "
        "github.event.pull_request.head.repo.full_name == github.repository"
    )
    assert canary["runs-on"] == "ubuntu-24.04"
    assert canary["permissions"] == {"contents": "read", "id-token": "write"}
    assert len(canary["steps"]) == 2
    installer, synthetic_canary = canary["steps"]
    assert installer == {
        "uses": "sigstore/cosign-installer@398d4b0eeef1380460a10c8013a76f728fb906ac",
        "with": {"cosign-release": "v2.5.2"},
    }
    assert set(synthetic_canary) == {"name", "shell", "run"}
    assert synthetic_canary["name"] == "Sign synthetic blob and refuse altered bytes or wrong issuer"
    assert synthetic_canary["shell"] == "bash"
    # Pin the reviewed shell commands; any unreviewed fetch, modified signature
    # checks or additional execution must fail before privileged OIDC approval.
    assert hashlib.sha256(synthetic_canary["run"].encode("utf-8")).hexdigest() == (
        "03d8d1634ff3b0e68b1c3cf55613192ea616bee365cdb0b33d0ae5946335940e"
    )


def test_pr_workflow_permissions_and_triggers():
    source = PR_WORKFLOW.read_text(encoding="utf-8")
    require_pr_workflow(source)
    # A pull_request_target event changes the trust boundary even though
    # the first refusal step and the OIDC canary scripts are unchanged.
    for before, after in (
        ("  pull_request:\n    branches: [master]", "  pull_request_target:\n    branches: [master]"),
        ("  pull_request:\n    branches: [master]", "  pull_request:\n    branches: [unreviewed]"),
        ("  workflow_dispatch:", "  push:"),
    ):
        assert source.count(before) == 1
        with pytest.raises(AssertionError):
            require_pr_workflow(source.replace(before, after, 1))


@pytest.mark.parametrize("mutation", [
    lambda src: src.replace(
            "      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262",
            "      - if: always()\n        uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262", 1,
        ),
    lambda src: src.replace(
            "        os: [ubuntu-24.04, windows-2022]",
            "        os: [self-hosted, windows-2022]", 1,
        ),
    lambda src: src.replace(
            "    strategy:\n", "    container: python:3.12\n    strategy:\n", 1,
        ),
    lambda src: src.replace(
            "permissions:\n  contents: read",
            "permissions:\n  contents: write", 1,
        ),
    lambda src: src.replace(
            "jobs:\n", "env:\n  BASH_ENV: /tmp/startup-hook\njobs:\n", 1,
        ),
    lambda src: src.replace(
            "          if-no-files-found: error",
            "          if-no-files-found: warn", 1,
        ),
    lambda src: src.replace(
            "          path: ${{ runner.temp }}/e156-assurance-junit.xml",
            "          path: rewrite-workbook.txt", 1,
        ),
    lambda src: src.replace(
            "      - uses: sigstore/cosign-installer@",
            "      - uses: actions/checkout@v4\n      - uses: sigstore/cosign-installer@", 1,
        ),
    lambda src: src.replace(
            "          echo 'Keyless OIDC signing and negative controls passed; no publication performed.'",
            "          echo 'unreviewed side effect'\n"
            "          echo 'Keyless OIDC signing and negative controls passed; no publication performed.'", 1,
        ),
    lambda src: src.replace(
            "      - uses: sigstore/cosign-installer@",
            "      - name: unreviewed preflight\n"
            "        shell: bash\n"
            "        run: echo unreviewed\n"
            "      - uses: sigstore/cosign-installer@", 1,
        ),
    lambda src: src.replace(
            "    if: github.event_name == 'pull_request' && github.event.pull_request.head.repo.full_name == github.repository",
            "    if: always()", 1,
        ),
    lambda src: src.replace(
            "          cosign-release: v2.5.2",
            "          cosign-release: v0.0.0", 1,
        ),
    lambda src: src.replace(
            "      - name: Sign synthetic blob and refuse altered bytes or wrong issuer",
            "      - name: Sign synthetic blob and refuse altered bytes or wrong issuer\n"
            "        env:\n"
            "          BASH_ENV: ./unreviewed-startup", 1,
        ),
])
def test_pr_workflow_mutations_are_refused(mutation):
    original = PR_WORKFLOW.read_text(encoding="utf-8")
    planted = mutation(original)
    assert planted != original, "mutation did not reach intended source"
    with pytest.raises(AssertionError):
        require_pr_workflow(planted)
