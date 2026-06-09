#!/usr/bin/env python3
"""Run UX harness audits and write data/latest/ui-audit.json (+ ux-audit.json).

Invokes li-cursor-agents/ux-harness/run_audit.py for all ux-targets.json rows
(docs + GUI + TUI). Preflight mode is the default for agent-briefing integration.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / "data/latest"
AGENTS = Path(os.environ.get("LI_CURSOR_AGENTS_ROOT", ROOT.parent / "li-cursor-agents"))
RUN_AUDIT = AGENTS / "ux-harness" / "run_audit.py"
MANIFEST = AGENTS / "config" / "ux-targets.json"


def _load_target_ids(*, surface: str | None = None) -> list[str]:
    if not MANIFEST.is_file():
        return []
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ids: list[str] = []
    for row in data.get("targets") or []:
        if not isinstance(row, dict) or not row.get("id"):
            continue
        if surface and row.get("surface") != surface:
            continue
        ids.append(str(row["id"]))
    return ids


def _run_harness_all(*, mock: bool, out_dir: Path) -> tuple[int, str, str]:
    cmd = [sys.executable, str(RUN_AUDIT), "--all", "--mode", "both", "--out-dir", str(out_dir)]
    if mock:
        cmd.append("--mock")
    proc = subprocess.run(cmd, cwd=str(AGENTS), capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


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
        "generated_at": new.get("generated_at"),
        "platform": new.get("platform"),
        "summary": {
            "total": len(targets),
            "failing": sum(1 for t in targets if t.get("status") == "fail"),
            "passing": sum(1 for t in targets if t.get("status") == "pass"),
            "skipped": sum(1 for t in targets if t.get("status") == "skip"),
        },
        "targets": targets,
    }


def _run_harness_targets(targets: list[str], *, mock: bool, out_dir: Path) -> tuple[int, str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    ui_agg: dict | None = None
    ux_agg: dict | None = None
    last_code = 0
    combined_out: list[str] = []
    combined_err: list[str] = []

    for target in targets:
        cmd = [sys.executable, str(RUN_AUDIT), "--target", target, "--mode", "both"]
        if mock:
            cmd.append("--mock")
        proc = subprocess.run(cmd, cwd=str(AGENTS), capture_output=True, text=True)
        if proc.stdout:
            combined_out.append(proc.stdout.strip())
        if proc.stderr:
            combined_err.append(proc.stderr.strip())
        if proc.returncode != 0:
            last_code = proc.returncode
            continue
        payload = json.loads(proc.stdout)
        if payload.get("ui"):
            ui_agg = _merge_audit(ui_agg, payload["ui"])
        if payload.get("ux"):
            ux_agg = _merge_audit(ux_agg, payload["ux"])

    if ui_agg:
        (out_dir / "ui-audit.json").write_text(json.dumps(ui_agg, indent=2) + "\n", encoding="utf-8")
    if ux_agg:
        (out_dir / "ux-audit.json").write_text(json.dumps(ux_agg, indent=2) + "\n", encoding="utf-8")

    return last_code, "\n".join(combined_out), "\n".join(combined_err)


def _audit_summary(path: Path) -> dict | None:
    if not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    return payload.get("summary") if isinstance(payload.get("summary"), dict) else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Run UX harness audits for benchmarks preflight")
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="Full ux-targets matrix for agent-briefing (default when no batch flags)",
    )
    parser.add_argument("--all", action="store_true", help="Run harness --all")
    parser.add_argument("--surface", choices=["docs", "gui", "tui"], help="Audit one surface batch")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Fixture data for CI without sibling clones",
    )
    args = parser.parse_args()

    use_mock = args.mock or os.environ.get("LI_UI_AUDIT_MOCK", "0") == "1"
    out_dir = LATEST

    if not RUN_AUDIT.is_file():
        print(f"skip: ux harness missing at {RUN_AUDIT}", file=sys.stderr)
        return 0

    if args.surface:
        targets = _load_target_ids(surface=args.surface)
        if not targets:
            print(f"skip: no targets for surface={args.surface}", file=sys.stderr)
            return 0
        code, stdout, stderr = _run_harness_targets(targets, mock=use_mock, out_dir=out_dir)
    else:
        # Default, --preflight, and --all share the full matrix run.
        code, stdout, stderr = _run_harness_all(mock=use_mock, out_dir=out_dir)

    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)

    if code != 0:
        return code

    ui_summary = _audit_summary(out_dir / "ui-audit.json")
    if ui_summary and int(ui_summary.get("failing") or 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
