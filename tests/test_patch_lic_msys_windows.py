"""Windows lic MSYS patch — idempotent shims for benchmark-nightly prepare-lic-windows."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH_SCRIPT = ROOT / "scripts/patch-lic-msys-windows.sh"
WORKFLOW = ROOT / ".github/workflows/benchmark-nightly.yml"


class PatchLicMsysWindowsTests(unittest.TestCase):
    def test_patch_script_includes_inference_sse_winsock_shim(self):
        text = PATCH_SCRIPT.read_text(encoding="utf-8")
        self.assertIn("li_rt_inference_sse.c", text)
        self.assertIn("li_rt_posix_compat.h", text)
        self.assertIn("recv()", text)

    def test_workflow_windows_cache_keys_include_patch_script(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        cache_lines = [
            line
            for line in workflow.splitlines()
            if "lic-build-windows-" in line and "hashFiles" in line
        ]
        self.assertEqual(len(cache_lines), 2, "expected two Windows lic cache keys")
        for line in cache_lines:
            self.assertIn(
                "scripts/patch-lic-msys-windows.sh",
                line,
                f"cache key must bust when patch changes: {line}",
            )


if __name__ == "__main__":
    unittest.main()
