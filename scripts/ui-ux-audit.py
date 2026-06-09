#!/usr/bin/env python3
"""Run UX harness audits and write data/latest/ui-audit.json (+ ux-audit.json).

Preflight mode audits lic-docs + benchmarks-dashboard for agent-briefing.json.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / "data/latest"
AGENTS = Path(os.environ.get("LI_CURSOR_AGENTS_ROOT", ROOT.parent / "li-cursor-agents"))
RUN_AUDIT = AGENTS / "ux-harness" / "run_audit.py"

PREFLIGHT_UI_TARGETS = ["lic-docs", "benchmarks-dashboard"]


def _merge_audit(existing: dict | None, new: dict) -> dict:
    merged: dict[str, dict] = {}
    if existing:
        for row in existing.get("targets") or []:
            if isinstance(row, dict) and row.get("target_id"):
                merged[str(row["target_id"])] = row
    for row in new.get("targets") or []:
        if isinstance(row, dict) and row.get("target_id"):
            merged[str(row["target_id"])] = row
    targets = list(merged.values())
    return {
        "generated_at": new.get("generated_at") or datetime.now(timezone.utc).isoformat(),
        "platform": new.get("platform"),
        "summary": {
            "total": len(targets),
            "failing": sum(1 for t in targets if t.get("status") == "fail"),
            "passing": sum(1 for t in targets if t.get("status") == "pass"),
            "skipped": sum(1 for t in targets if t.get("status") == "skip"),
        },
        "targets": targets,
    }


def _run_target(target: str, mode: str, mock: bool) -> dict | None:
    cmd = [sys.executable, str(RUN_AUDIT), "--target", target, "--mode", mode]
    if mock:
        cmd.append("--mock")
    proc = subprocess.run(cmd, cwd=str(AGENTS), capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return None
    payload = json.loads(proc.stdout)
    key = "ui" if mode == "ui" else "ux"
    return payload.get(key)


def run_audits(targets: list[str], *, mock: bool) -> tuple[dict | None, dict | None]:
    if not RUN_AUDIT.is_file():
        print(f"skip: ux harness missing at {RUN_AUDIT}", file=sys.stderr)
        return None, None

    ui_agg: dict | None = None
    ux_agg: dict | None = None
    for target in targets:
        ui_row = _run_target(target, "ui", mock)
        if ui_row:
            ui_agg = _merge_audit(ui_agg, ui_row)
        ux_row = _run_target(target, "ux", mock)
        if ux_row:
            ux_agg = _merge_audit(ux_agg, ux_row)
    return ui_agg, ux_agg


def write_outputs(ui: dict | None, ux: dict | None) -> None:
    LATEST.mkdir(parents=True, exist_ok=True)
    if ui:
        (LATEST / "ui-audit.json").write_text(json.dumps(ui, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {LATEST / 'ui-audit.json'}")
    if ux:
        (LATEST / "ux-audit.json").write_text(json.dumps(ux, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {LATEST / 'ux-audit.json'}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run UX harness audits for benchmarks preflight")
    parser.add_argument("--preflight", action="store_true", help="lic-docs + benchmarks-dashboard only")
    parser.add_argument("--mock", action="store_true", help="Fixture data for CI without sibling clones")
    parser.add_argument("--all", action="store_true", help="Run harness --all (may include TUI)")
    args = parser.parse_args()

    if args.all:
        if not RUN_AUDIT.is_file():
            print(f"skip: ux harness missing at {RUN_AUDIT}", file=sys.stderr)
            return 0
        cmd = [sys.executable, str(RUN_AUDIT), "--all", "--mode", "both", "--out-dir", str(LATEST)]
        if args.mock:
            cmd.append("--mock")
        proc = subprocess.run(cmd, cwd=str(AGENTS), capture_output=True, text=True)
        if proc.returncode != 0:
            print(proc.stderr or proc.stdout, file=sys.stderr)
            return proc.returncode
        print(proc.stdout)
        return 0

    targets = PREFLIGHT_UI_TARGETS if args.preflight else PREFLIGHT_UI_TARGETS
    ui, ux = run_audits(targets, mock=args.mock)
    if ui is None and ux is None:
        return 0
    write_outputs(ui, ux)
    failing = int((ui or {}).get("summary", {}).get("failing", 0))
    return 1 if failing else 0


if __name__ == "__main__":
    raise SystemExit(main())
