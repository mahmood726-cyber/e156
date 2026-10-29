"""Isolated negative controls for the Sigstore publication gate.

Mocked subprocess returns exercise refusal semantics, not real Sigstore
signatures, release authentication, production OIDC or a full-system canary.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/assurance/verify_sigstore_badges.py"
spec = importlib.util.spec_from_file_location("e156_sigstore_gate", SCRIPT)
assert spec and spec.loader
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def _badge(tmp_path):
    badge = tmp_path / "assurance.json"
    badge.write_text('{"tier":"bronze"}', encoding="utf-8")
    bundle = tmp_path / "assurance.json.cosign.bundle"
    bundle.write_text('{"mediaType":"test-fixture-not-a-real-signature"}', encoding="utf-8")
    return badge, bundle


def _context(monkeypatch):
    monkeypatch.setenv("GITHUB_REPOSITORY", gate.REPOSITORY)
    monkeypatch.setenv("GITHUB_REF", gate.REF)


def test_missing_wrong_repo_or_ref_refuses(tmp_path, monkeypatch):
    _badge(tmp_path)
    assert gate.verify(tmp_path) == 2
    _context(monkeypatch)
    monkeypatch.setenv("GITHUB_REPOSITORY", "other/repo")
    assert gate.verify(tmp_path) == 2
    _context(monkeypatch)
    monkeypatch.setenv("GITHUB_REF", "refs/heads/unreviewed")
    assert gate.verify(tmp_path) == 2


def test_empty_badge_set_or_missing_empty_bundle_refuses(tmp_path, monkeypatch):
    _context(monkeypatch)
    assert gate.verify(tmp_path) == 2
    badge, bundle = _badge(tmp_path)
    bundle.unlink()
    assert gate.verify(tmp_path) == 2
    bundle.touch()
    assert gate.verify(tmp_path) == 2
    badge.unlink()
    assert gate.verify(tmp_path) == 2


def test_injected_symlink_path_refuses_on_windows_and_linux(tmp_path, monkeypatch):
    _context(monkeypatch)
    _, bundle = _badge(tmp_path)
    # Do not require Windows SeCreateSymbolicLinkPrivilege to test the guard.
    original = Path.is_symlink
    monkeypatch.setattr(Path, "is_symlink",
                        lambda self: self == bundle or original(self))
    assert gate.verify(tmp_path) == 2


def test_cosign_failure_and_missing_binary_refuse(tmp_path, monkeypatch):
    _context(monkeypatch)
    _badge(tmp_path)
    monkeypatch.setattr(gate.subprocess, "run",
                        lambda *a, **kw: SimpleNamespace(returncode=1, stderr="invalid signature"))
    assert gate.verify(tmp_path) == 2
    def missing(*args, **kwargs):
        raise FileNotFoundError("cosign")
    monkeypatch.setattr(gate.subprocess, "run", missing)
    assert gate.verify(tmp_path) == 2


def test_success_requires_exact_workflow_identity_issuer_and_payload(tmp_path, monkeypatch):
    _context(monkeypatch)
    badge, bundle = _badge(tmp_path)
    commands = []
    def accepted(command, **kwargs):
        commands.append(command)
        return SimpleNamespace(returncode=0, stderr="")
    monkeypatch.setattr(gate.subprocess, "run", accepted)
    assert gate.verify(tmp_path) == 0
    assert commands == [[
        "cosign", "verify-blob", "--bundle", str(bundle),
        "--certificate-identity", gate.IDENTITY,
        "--certificate-oidc-issuer", gate.ISSUER, str(badge),
    ]]


def test_production_workflow_requires_sigstore_verification_before_dashboard():
    text = (ROOT / ".github/workflows/assurance.yml").read_text(encoding="utf-8")
    signing = "Sigstore keyless-sign badges (public, transparency-logged)"
    verification = "Verify Sigstore badge bundles and workflow identity (hard gate)"
    dashboard = "Build the public assurance dashboard (served by existing Pages)"
    assert text.count(verification) == 1
    assert text.index(signing) < text.index(verification) < text.index(dashboard)
    assert "run: python scripts/assurance/verify_sigstore_badges.py --repo ." in text
