"""setup-lic-for-bench.sh — lic-ci container skips sudo apt on Linux."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETUP_SCRIPT = ROOT / "scripts/setup-lic-for-bench.sh"
WORKFLOW = ROOT / ".github/workflows/benchmark-nightly.yml"


class SetupLicForBenchTests(unittest.TestCase):
    def test_linux_lic_ci_skips_sudo_apt(self):
        text = SETUP_SCRIPT.read_text(encoding="utf-8")
        self.assertIn("_linux_skip_apt", text)
        self.assertIn("LIC_CI_CONTAINER", text)
        self.assertIn("Linux lic-ci — skip apt", text)

    def test_prepare_lic_linux_sets_lic_ci_container(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        prepare = workflow.split("prepare-lic-macos:")[0]
        self.assertIn("prepare-lic-linux:", prepare)
        self.assertIn("LIC_CI_CONTAINER: \"1\"", prepare)
        self.assertIn("ghcr.io/li-langverse/lic-ci:ubuntu24-llvm22", prepare)


if __name__ == "__main__":
    unittest.main()
