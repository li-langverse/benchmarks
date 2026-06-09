"""ui-ux-audit preflight — full ux-targets matrix for agent-briefing."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_GUI = {
    "agents-dashboard",
    "benchmarks-dashboard",
    "world-studio-demo",
    "gui-gen-fixture",
}
EXPECTED_TUI = {"tui-app-fixture", "tui-gen-fixture"}


class UiUxAuditTests(unittest.TestCase):
    def test_preflight_writes_full_ui_audit_matrix(self) -> None:
        agents = Path(os.environ.get("LI_CURSOR_AGENTS_ROOT", ROOT.parent / "li-cursor-agents"))
        if not (agents / "ux-harness" / "run_audit.py").is_file():
            self.skipTest("li-cursor-agents sibling clone not present")

        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts/ui-ux-audit.py"), "--mock"],
            cwd=ROOT,
            env={**os.environ, "LI_CURSOR_AGENTS_ROOT": str(agents)},
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 1, (proc.stdout or "") + (proc.stderr or ""))

        audit_path = ROOT / "data/latest/ui-audit.json"
        self.assertTrue(audit_path.is_file(), msg=proc.stderr)
        payload = json.loads(audit_path.read_text(encoding="utf-8"))
        ids = {t.get("target_id") for t in payload.get("targets") or []}
        self.assertIn("lic-docs", ids)
        self.assertTrue(EXPECTED_GUI.issubset(ids), msg=sorted(ids))
        self.assertTrue(EXPECTED_TUI.issubset(ids), msg=sorted(ids))
        self.assertGreaterEqual(int(payload.get("summary", {}).get("total") or 0), 8)

    def test_briefing_includes_ui_audit_gui_rows(self) -> None:
        audit_path = ROOT / "data/latest/ui-audit.json"
        if not audit_path.is_file():
            self.skipTest("run ui-ux-audit first")

        payload = json.loads(audit_path.read_text(encoding="utf-8"))
        ids = {t.get("target_id") for t in payload.get("targets") or []}
        self.assertIn("agents-dashboard", ids)
        self.assertIn("world-studio-demo", ids)
        self.assertIn("gui-gen-fixture", ids)

        sys.path.insert(0, str(ROOT / "scripts"))
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "agent_briefing", ROOT / "scripts" / "agent-briefing.py"
        )
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        data = {"ui_audit": payload, "recommended_agents": []}
        rec = mod.recommend_agents(data)
        agents = {r["agent"] for r in rec}
        if any(t.get("status") in ("fail", "skip") for t in payload.get("targets") or []):
            self.assertTrue(
                {"gui_ui_tester", "tui_ui_tester", "docs_ui_tester"} & agents,
                msg=sorted(agents),
            )


if __name__ == "__main__":
    unittest.main()
