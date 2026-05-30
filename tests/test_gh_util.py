"""Unit tests for gh_util."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gh_util import gh_json  # noqa: E402


class GhUtilTests(unittest.TestCase):
    def test_gh_json_returns_default_on_empty_stdout(self) -> None:
        with mock.patch("gh_util.subprocess.run") as run:
            run.return_value = mock.Mock(returncode=0, stdout="", stderr="")
            self.assertEqual(gh_json(["api", "foo"], default=[]), [])

    def test_gh_json_parses_utf8(self) -> None:
        payload = [{"title": "café"}]
        with mock.patch("gh_util.subprocess.run") as run:
            run.return_value = mock.Mock(
                returncode=0,
                stdout=json.dumps(payload),
                stderr="",
            )
            self.assertEqual(gh_json(["issue", "list"]), payload)


if __name__ == "__main__":
    unittest.main()
