"""Safety regressions for mandatory keyless-only E156 assurance."""
import importlib.util
import json
import os
from types import SimpleNamespace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "require_keyless_safe_badges",
    ROOT / "scripts" / "assurance" / "require_keyless_safe_badges.py",
)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class KeylessPreflightTests(unittest.TestCase):
    def test_valid_unsigned_badge(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "capsule" / "assurance.json"
            p.parent.mkdir()
            p.write_text(json.dumps({"tier": "none", "checks": {}}), encoding="utf-8")
            self.assertEqual(MOD.check(Path(d)), 0)

    def test_no_badges_refused(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertNotEqual(MOD.check(Path(d)), 0)

    # Each refusal case must have its own JUnit testcase identity. Pytest
    # includes unittest subTest outcomes in the suite total but does not emit
    # separate testcase XML nodes; the fail-closed coverage gate must remain
    # able to reconcile declared and observed counts without exceptions.
    def _assert_badge_refused(self, payload):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "assurance.json"
            p.write_text(payload, encoding="utf-8")
            self.assertNotEqual(MOD.check(Path(d)), 0)

    def test_legacy_hmac_signature_refused_without_key(self):
        self._assert_badge_refused(json.dumps({"tier": "none", "signature": "tampered"}))

    def test_legacy_hmac_signed_at_refused_without_key(self):
        self._assert_badge_refused(json.dumps({"tier": "none", "signed_at": "old"}))

    def test_non_object_badge_refused(self):
        self._assert_badge_refused("[]")

    def test_malformed_badge_refused(self):
        self._assert_badge_refused("{broken")

    def test_symlinked_badge_refused_on_all_platforms(self):
        # Some Windows CI hosts cannot create actual symlinks without a
        # privilege; simulate Path.is_symlink so no test is skipped.
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "assurance.json").write_text('{"tier": "none"}', encoding="utf-8")
            original = Path.is_symlink

            def flagged(path):
                return path.name == "assurance.json" or original(path)

            with patch.object(Path, "is_symlink", flagged):
                self.assertNotEqual(MOD.check(root), 0)

    def _sigstore_verifier(self):
        spec = importlib.util.spec_from_file_location(
            "verify_sigstore_badges_exact_sha",
            ROOT / "scripts" / "assurance" / "verify_sigstore_badges.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_current_oidc_sha_and_repository_claims_are_mandatory(self):
        verifier = self._sigstore_verifier()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "assurance.json").write_text('{"tier":"none"}', encoding="utf-8")
            (root / "assurance.json.cosign.bundle").write_text("synthetic", encoding="utf-8")
            env = {
                "GITHUB_REPOSITORY": "mahmood726-cyber/e156",
                "GITHUB_REF": "refs/heads/master",
                "GITHUB_SHA": "a" * 40,
            }
            with patch.dict(os.environ, env, clear=True), patch.object(
                verifier.subprocess, "run",
                return_value=SimpleNamespace(returncode=0, stderr=""),
            ) as execute:
                self.assertEqual(verifier.verify(root), 0)
                execute.assert_called_once()
                argv = execute.call_args.args[0]
                self.assertEqual(argv[argv.index("--certificate-github-workflow-sha") + 1], "a" * 40)
                self.assertEqual(argv[argv.index("--certificate-github-workflow-repository") + 1],
                                 "mahmood726-cyber/e156")
                self.assertEqual(argv[argv.index("--certificate-github-workflow-ref") + 1],
                                 "refs/heads/master")
                self.assertIn("--certificate-identity", argv)
                self.assertIn("--certificate-oidc-issuer", argv)

    def test_missing_or_invalid_source_sha_refused_before_cosign(self):
        verifier = self._sigstore_verifier()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "assurance.json").write_text('{"tier":"none"}', encoding="utf-8")
            (root / "assurance.json.cosign.bundle").write_text("synthetic", encoding="utf-8")
            for bad_sha in ("", "b" * 39, "G" * 40, "b" * 64):
                env = {
                    "GITHUB_REPOSITORY": "mahmood726-cyber/e156",
                    "GITHUB_REF": "refs/heads/master",
                    "GITHUB_SHA": bad_sha,
                }
                with patch.dict(os.environ, env, clear=True), patch.object(
                    verifier.subprocess, "run",
                ) as execute:
                    self.assertNotEqual(verifier.verify(root), 0)
                    execute.assert_not_called()

    def test_signing_workflow_requires_keyless_gate_and_no_hmac_branch(self):
        workflow = (ROOT / ".github" / "workflows" / "assurance.yml").read_text(encoding="utf-8")
        hmac = workflow.index("Reject unverified legacy HMAC marks before mandatory keyless signing")
        sign = workflow.index("Sigstore keyless-sign badges")
        verify = workflow.index("Verify Sigstore badge bundles and workflow identity (hard gate)")
        dashboard = workflow.index("Build the public assurance dashboard")
        self.assertLess(hmac, sign)
        self.assertLess(sign, verify)
        self.assertLess(verify, dashboard)
        self.assertIn("--require-keyless-verified", workflow)
        self.assertNotIn("E156_ASSURANCE_HMAC_KEY", workflow)
        self.assertNotIn("publish_hmac_badges.py", workflow)
        self.assertEqual(workflow.count("require_keyless_safe_badges.py --repo ."), 1)
        self.assertIn("id-token: write", workflow)
        self.assertIn("require_keyless_safe_badges.py --repo .", workflow)
        self.assertNotIn("if: ${{", workflow[sign:dashboard])
        verifier = (ROOT / "scripts" / "assurance" / "verify_sigstore_badges.py").read_text(encoding="utf-8")
        self.assertIn("--certificate-identity", verifier)
        self.assertIn("--certificate-oidc-issuer", verifier)
        self.assertIn("--certificate-github-workflow-sha", verifier)
        self.assertIn("no badges exist; zero Sigstore checks is not success", verifier)


if __name__ == "__main__":
    unittest.main()
