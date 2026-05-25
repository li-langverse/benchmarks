"""Regression tests for scripts/ensure-org-repo-ci.py (WP-A2)."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "ensure-org-repo-ci.py"


def load_module():
    name = "ensure_org_repo_ci_test"
    spec = importlib.util.spec_from_file_location(name, SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


class EnsureOrgRepoCiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_module()

    def test_has_ci_accepts_yaml_variant(self):
        self.assertTrue(self.mod.has_ci(["ci.yaml"]))
        self.assertTrue(self.mod.has_ci(["ci.yml", "pages.yml"]))
        self.assertFalse(self.mod.has_ci(["pages.yml"]))

    def test_lidb_gated_when_default_not_main(self):
        with (
            patch.object(self.mod, "default_branch", return_value="feat/ph-db-2-liorm-liq"),
            patch.object(
                self.mod,
                "workflow_names",
                return_value=(["ci.yml"], "local", None),
            ),
        ):
            entry = self.mod.audit_repo("lidb", allow_local_fallback=True)
        self.assertEqual(entry["status"], "gated_non_main_default")
        self.assertIn("WP-H0", entry["fix"])

    def test_lidb_ok_on_main_with_github_ci(self):
        with (
            patch.object(self.mod, "default_branch", return_value="main"),
            patch.object(
                self.mod,
                "workflow_names",
                return_value=(["ci.yml"], "github", None),
            ),
        ):
            entry = self.mod.audit_repo("lidb", allow_local_fallback=False)
        self.assertEqual(entry["status"], "ok")

    def test_no_local_fallback_when_api_fails(self):
        with (
            patch.object(self.mod, "default_branch", return_value="main"),
            patch.object(
                self.mod,
                "workflow_names",
                return_value=([], "none", "rate limit"),
            ),
        ):
            entry = self.mod.audit_repo("lidb", allow_local_fallback=False)
        self.assertEqual(entry["status"], "audit_incomplete")

    def test_local_fallback_only_when_opt_in(self):
        with (
            patch.object(self.mod, "default_branch", return_value="main"),
            patch.object(
                self.mod,
                "workflow_names",
                return_value=(["ci.yml"], "local", "rate limit"),
            ),
        ):
            entry = self.mod.audit_repo("lidb", allow_local_fallback=True)
        self.assertEqual(entry["status"], "ok")
        self.assertEqual(entry["workflow_source"], "local")

    def test_missing_ci_on_main_without_workflows(self):
        with (
            patch.object(self.mod, "default_branch", return_value="main"),
            patch.object(
                self.mod,
                "workflow_names",
                return_value=([], "github", None),
            ),
        ):
            entry = self.mod.audit_repo("li-local-ci", allow_local_fallback=False)
        self.assertEqual(entry["status"], "missing_ci")


if __name__ == "__main__":
    unittest.main()
