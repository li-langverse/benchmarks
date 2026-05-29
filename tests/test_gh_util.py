"""Tests for GitHub CLI helper utilities."""
from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from gh_util import gh_json  # noqa: E402


class GhUtilTests(unittest.TestCase):
    def test_gh_json_uses_utf8_and_handles_empty_stdout(self) -> None:
        with mock.patch("gh_util.subprocess.run") as run:
            run.return_value = subprocess.CompletedProcess(
                args=["gh"],
                returncode=0,
                stdout='[{"n": 1}]',
                stderr="",
            )
            self.assertEqual(gh_json(["pr", "list"], default=[]), [{"n": 1}])
            _, kwargs = run.call_args
            self.assertEqual(kwargs["encoding"], "utf-8")
            self.assertEqual(kwargs["errors"], "replace")

        with mock.patch("gh_util.subprocess.run") as run:
            run.return_value = subprocess.CompletedProcess(
                args=["gh"],
                returncode=1,
                stdout=None,
                stderr="error",
            )
            self.assertEqual(gh_json(["pr", "list"], default=[]), [])


if __name__ == "__main__":
    unittest.main()
