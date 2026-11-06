"""Structural regression: PR CI must not read publication-derived fixtures while held.

Pure workflow metadata and deterministic synthetic mutations only. No paper,
cache, workbook, DOI or supplementary file is loaded by this test.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

WORKFLOW = Path(__file__).resolve().parents[1] / '.github/workflows/assurance-pr.yml'
HOLD_NAME = 'SOURCE_RIGHTS_HOLD — pause publication-derived PR tests before checkout'
HOLD_RUN = (
    "Write-Error 'SOURCE_RIGHTS_HOLD: full PR corpus is held until a reviewed, "
    "operation-specific source-rights gate and private decision log are available.'\n"
    'exit 1\n'
)
CANARY_STEP = 'Sign synthetic blob and refuse altered bytes or wrong issuer'
CANARY_ACTION = 'sigstore/cosign-installer@398d4b0eeef1380460a10c8013a76f728fb906ac'


def require_fail_closed_pr_workflow(document: dict) -> None:
    assert isinstance(document, dict)
    assert not any(k in document for k in ('env', 'defaults'))
    jobs = document['jobs']
    assert set(jobs) == {'assurance-tests', 'keyless-oidc-canary'}
    corpus = jobs['assurance-tests']
    assert not any(k in corpus for k in ('env', 'defaults', 'container', 'services',
                                         'continue-on-error', 'if'))
    assert corpus['runs-on'] == '${{ matrix.os }}'
    assert corpus['strategy']['matrix']['os'] == ['ubuntu-24.04', 'windows-2022']
    steps = corpus['steps']
    assert len(steps) > 3
    assert steps[0] == {'name': HOLD_NAME, 'shell': 'pwsh', 'run': HOLD_RUN}
    # Diagnostic always() steps may fail due to a missing report, but must
    # not check out article material or run publication commands.
    always = [s for s in steps[1:] if s.get('if') == 'always()']
    assert len(always) == 2
    by_name = {s.get('name'): s for s in always}
    diagnostic = by_name['Refuse omitted, skipped, or failed test cases']
    assert 'require_corpus_results.py' in diagnostic['run']
    assert not any(word in diagnostic['run'] for word in ('doi_resolver.py', 'build_pages', 'sentinel scan'))
    uploads = [s for s in always if s.get('uses', '').startswith('actions/upload-artifact@')]
    assert len(uploads) == 1
    assert uploads[0]['with']['path'] == '${{ runner.temp }}/e156-assurance-junit.xml'
    assert uploads[0]['with']['if-no-files-found'] == 'error'

    # OIDC canary signs its own synthetic tempfile; full checkout would
    # unnecessarily read held publication-derived Git tree objects.
    canary = jobs['keyless-oidc-canary']
    assert canary['runs-on'] == 'ubuntu-24.04'
    assert not any(k in canary for k in ('env', 'defaults', 'container', 'services',
                                         'continue-on-error'))
    canary_steps = canary['steps']
    assert len(canary_steps) == 2
    assert canary_steps[0] == {'uses': CANARY_ACTION, 'with': {'cosign-release': 'v2.5.2'}}
    assert canary_steps[1]['name'] == CANARY_STEP
    assert canary_steps[1]['shell'] == 'bash'
    assert set(canary_steps[1]) == {'name', 'shell', 'run'}
    script = canary_steps[1]['run']
    assert 'synthetic OIDC preflight; not an assurance badge' in script
    assert 'cosign sign-blob' in script and 'cosign verify-blob' in script
    assert not any(word in script for word in ('doi_resolver', 'rewrite-workbook', 'git clone',
                                               'actions/checkout', 'git checkout', 'curl ', 'wget '))


def load_workflow() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding='utf-8'))


def test_pr_gate_refuses_before_checkout_and_oidc_canary_is_synthetic_only():
    require_fail_closed_pr_workflow(load_workflow())


@pytest.mark.parametrize('mutate', [
    lambda d: d['jobs']['assurance-tests']['steps'].pop(0),
    lambda d: d['jobs']['assurance-tests']['steps'][0].update({'if': 'false'}),
    lambda d: d['jobs']['assurance-tests']['steps'][0].update({'run': 'echo green\nexit 0\n'}),
    lambda d: d['jobs']['assurance-tests']['steps'][0].update({'continue-on-error': True}),
    lambda d: d['jobs']['assurance-tests']['steps'].insert(0, {'uses': 'actions/checkout@v4'}),
    lambda d: d['jobs']['assurance-tests'].update({'runs-on': 'self-hosted'}),
    lambda d: d['jobs']['assurance-tests'].update({'container': 'ubuntu:latest'}),
    lambda d: d.update({'env': {'BASH_ENV': '/tmp/unsafe-startup'}}),
    lambda d: d['jobs']['keyless-oidc-canary']['steps'].insert(0, {'uses': 'actions/checkout@v4'}),
    lambda d: d['jobs']['keyless-oidc-canary']['steps'][1].update({'run': 'python scripts/assurance/doi_resolver.py --repo .'}),
    lambda d: d['jobs']['assurance-tests']['steps'][-1]['with'].update({'if-no-files-found': 'warn'}),
])
def test_pr_rights_hold_mutations_are_refused(mutate):
    source = load_workflow()
    altered = deepcopy(source)
    mutate(altered)
    with pytest.raises((AssertionError, KeyError, IndexError)):
        require_fail_closed_pr_workflow(altered)
