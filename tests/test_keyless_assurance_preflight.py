"""Safety regressions for the HMAC-absent, mandatory-Sigstore assurance path."""
import importlib.util
import json
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

    def test_signing_workflow_requires_keyless_gate_after_optional_hmac(self):
        workflow = (ROOT / ".github" / "workflows" / "assurance.yml").read_text(encoding="utf-8")
        hmac = workflow.index("HMAC legacy authentication or strict keyless preflight")
        sign = workflow.index("Sigstore keyless-sign badges")
        verify = workflow.index("Verify Sigstore badge bundles and workflow identity (hard gate)")
        dashboard = workflow.index("Build the public assurance dashboard")
        self.assertLess(hmac, sign)
        self.assertLess(sign, verify)
        self.assertLess(verify, dashboard)
        self.assertIn("id-token: write", workflow)
        self.assertIn("require_keyless_safe_badges.py --repo .", workflow)
        self.assertNotIn("if: ${{", workflow[sign:dashboard])
        verifier = (ROOT / "scripts" / "assurance" / "verify_sigstore_badges.py").read_text(encoding="utf-8")
        self.assertIn("--certificate-identity", verifier)
        self.assertIn("--certificate-oidc-issuer", verifier)
        self.assertIn("no badges exist; zero Sigstore checks is not success", verifier)


if __name__ == "__main__":
    unittest.main()
