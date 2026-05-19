#!/usr/bin/env python3
"""Unit tests for discover-new-org-repos.py (no gh required)."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parent / "discover-new-org-repos.py"
_spec = importlib.util.spec_from_file_location("discover_new_org_repos", _SCRIPT)
assert _spec and _spec.loader
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

classify_new_repo = _mod.classify_new_repo
collect_known_repos = _mod.collect_known_repos
diff_org_repos = _mod.diff_org_repos
onboarding_steps_for_repo = _mod.onboarding_steps_for_repo


class DiscoverNewOrgReposTest(unittest.TestCase):
    def test_diff_finds_new_and_stale(self) -> None:
        known = {"lic", "benchmarks", "ghost-repo"}
        diff = diff_org_repos(["lic", "benchmarks", "li-new-pkg"], known)
        self.assertEqual(diff["new_repos"], ["li-new-pkg"])
        self.assertEqual(diff["stale_known_repos"], ["ghost-repo"])
        self.assertEqual(len(diff["new_repo_entries"]), 1)
        self.assertEqual(diff["new_repo_entries"][0]["repo"], "li-new-pkg")

    def test_collect_known_merges_audits(self) -> None:
        known = collect_known_repos(
            org_ci_audit={"repos_ok": ["lic"], "repos_missing_ci": [{"repo": "li-local-ci"}]},
            org_agent_kit_audit={"repos_needing_sync": [{"repo": "lip", "status": "drift"}]},
            ecosystem_audit={"repos_without_live_docs": ["roadmap"]},
            org_packages={"li-std-math": {"status": "ok"}},
            extra=["li-demo"],
        )
        self.assertIn("lic", known)
        self.assertIn("li-local-ci", known)
        self.assertIn("lip", known)
        self.assertIn("roadmap", known)
        self.assertIn("li-std-math", known)
        self.assertIn("li-demo", known)
        self.assertIn("benchmarks", known)  # from CORE fallback in collect — actually CORE list

    def test_classify_mirror_vs_unclassified(self) -> None:
        self.assertEqual(classify_new_repo("li-std-foo"), "official_mirror")
        self.assertEqual(classify_new_repo("lic"), "core_tooling")
        self.assertEqual(classify_new_repo("my-experiment"), "unclassified")

    def test_onboarding_includes_package_architect_for_unclassified(self) -> None:
        steps = onboarding_steps_for_repo("my-experiment", "unclassified")
        agents = {s["agent"] for s in steps}
        self.assertIn("package_architect", agents)
        self.assertIn("ci_maintainer", agents)


if __name__ == "__main__":
    unittest.main()
