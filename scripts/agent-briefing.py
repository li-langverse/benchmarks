#!/usr/bin/env python3
"""Aggregate preflight JSON for Cursor agents (explorer, PR review, plan gaps, numerics).

Agents read data/latest/agent-briefing.json — this script does NOT do web research or PR review.

Usage:
  python3 scripts/agent-briefing.py
  python3 scripts/agent-briefing.py --skip-slow
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
OUT = ROOT / "data/latest/agent-briefing.json"
LATEST = ROOT / "data/latest"

PREFLIGHT_SCRIPTS = [
    ("issue_triage", ["python3", "scripts/issue-feature-triage.py"]),
    ("plan_audit", ["python3", "scripts/plan-completion-audit.py"]),
    ("ecosystem_audit", ["python3", "scripts/ecosystem-audit.py"]),
    ("org_ci_audit", ["python3", "scripts/ensure-org-repo-ci.py"]),
    ("explorer", ["python3", "scripts/ecosystem-explorer.py"]),
    ("merge_plan", ["python3", "scripts/pr-merge-queue-plan.py"]),
    ("pr_program", ["python3", "scripts/run-pr-program.py"]),
]

CURSOR_AGENTS = [
    {
        "id": "orchestrator",
        "prompt": ".cursor/automations/agent-orchestrator.md",
        "when": "Weekly — route work from briefing",
    },
    {
        "id": "ecosystem_explorer",
        "prompt": ".cursor/automations/ecosystem-explorer.md",
        "skill": "explore-li-ecosystem",
        "when": "Missing libs, HPC parity, Reddit/web — needs web search",
        "preflight": ["explorer", "ecosystem_audit"],
    },
    {
        "id": "implementation_gaps",
        "prompt": ".cursor/automations/implementation-gaps-agent.md",
        "skills": ["explore-li-ecosystem", "audit-plan-completion"],
        "when": "Plan vs code drift, PH boxes, scaffold packages",
        "preflight": ["plan_audit", "explorer", "issue_triage"],
    },
    {
        "id": "plan_completion",
        "prompt": ".cursor/automations/plan-completion-audit.md",
        "skill": "audit-plan-completion",
        "when": "Master plan / G-* / catalog gaps",
        "preflight": ["plan_audit"],
    },
    {
        "id": "pr_alignment",
        "prompt": ".cursor/automations/pr-alignment-agent.md",
        "skill": "review-pr-alignment",
        "when": "Open PRs vs plan-approved / vision / redundant stacks",
        "preflight": ["merge_plan", "pr_program", "issue_triage"],
    },
    {
        "id": "pr_review",
        "prompt": ".cursor/automations/pr-review-agent.md",
        "skills": ["merge-approved-pr", "review-pr-alignment"],
        "when": "CI-green PRs — standards review before merge-approved",
        "preflight": ["merge_plan", "pr_program"],
    },
    {
        "id": "numerics_research",
        "prompt": ".cursor/automations/numerics-research-cycle.md",
        "skills": ["research-li-numerics", "numerics-autoresearch"],
        "when": "Red benches, numerics-research issues — needs web/HPC search",
        "preflight": ["ecosystem_audit", "explorer"],
    },
    {
        "id": "issue_planner",
        "prompt": ".cursor/automations/issue-feature-planner.md",
        "skill": "plan-feature-from-issue",
        "when": "plan-needed / feature issues",
        "preflight": ["issue_triage"],
    },
    {
        "id": "merge_queue",
        "prompt": ".cursor/automations/pr-auto-merge.md",
        "skills": ["plan-merge-queue", "merge-approved-pr"],
        "when": "merge-approved label + gate",
        "preflight": ["merge_plan", "pr_program"],
    },
]


def run_script(name: str, cmd: list[str], skip_slow: bool) -> dict:
    slow = name in ("explorer", "plan_audit", "pr_program", "merge_plan")
    if skip_slow and slow:
        return {"skipped": True, "reason": "--skip-slow"}
    env = os.environ.copy()
    lic = Path(os.environ.get("LIC_ROOT", ROOT / "lic"))
    if lic.is_dir():
        env["LIC_ROOT"] = str(lic)
    proc = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True, text=True)
    return {
        "command": " ".join(cmd),
        "exit_code": proc.returncode,
        "stdout_tail": proc.stdout[-500:] if proc.stdout else "",
        "stderr_tail": proc.stderr[-300:] if proc.stderr else "",
    }


def load_json(path: Path) -> dict | list | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"error": f"invalid json: {path.name}"}


def recommend_agents(data: dict) -> list[dict]:
    rec = []
    plan = data.get("plan_completion_audit") or {}
    if isinstance(plan, dict) and plan.get("summary", {}).get("total_findings", 0) > 0:
        rec.append({"agent": "plan_completion", "reason": "plan-completion-audit findings"})
        rec.append({"agent": "implementation_gaps", "reason": "cross-check plan vs implementation"})

    explorer = data.get("ecosystem_explorer") or {}
    if isinstance(explorer, dict):
        miss = [m for m in explorer.get("missing_std_modules", []) if m.get("status") == "missing"]
        if miss:
            rec.append({"agent": "ecosystem_explorer", "reason": f"{len(miss)} missing std modules"})

    pr_prog = data.get("pr_program") or {}
    if isinstance(pr_prog, dict) and pr_prog.get("open", 0) > 0:
        rec.append({"agent": "pr_alignment", "reason": "open PRs need alignment triage"})
        if pr_prog.get("ci_green", 0) > 0:
            rec.append({"agent": "pr_review", "reason": "CI-green PRs ready for standards review"})

    triage = data.get("issue_triage") or {}
    if isinstance(triage, dict) and triage.get("needs_plan"):
        rec.append({"agent": "issue_planner", "reason": "issues need plans"})

    bench = (data.get("ecosystem_audit") or {}).get("benchmarks") or {}
    if isinstance(bench, dict) and bench.get("red"):
        rec.append({"agent": "numerics_research", "reason": "red benchmark rows"})

    if not rec:
        rec.append({"agent": "orchestrator", "reason": "routine weekly sweep"})
    return rec


def main() -> int:
    parser = argparse.ArgumentParser(description="Build agent briefing JSON for Cursor agents")
    parser.add_argument("--skip-slow", action="store_true", help="skip slower audit scripts")
    args = parser.parse_args()

    LATEST.mkdir(parents=True, exist_ok=True)
    runs: dict[str, dict] = {}
    for name, cmd in PREFLIGHT_SCRIPTS:
        runs[name] = run_script(name, cmd, args.skip_slow)

    data = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "role": "preflight_for_cursor_agents",
        "note": "Intelligence (web, review, gaps) runs in Cursor Automations — not in this file.",
        "preflight_runs": runs,
        "issue_triage": load_json(LATEST / "issue-feature-triage.json"),
        "plan_completion_audit": load_json(LATEST / "plan-completion-audit.json"),
        "ecosystem_audit": load_json(LATEST / "ecosystem-audit.json"),
        "ecosystem_explorer": load_json(LATEST / "ecosystem-explorer.json"),
        "org_ci_audit": load_json(LATEST / "org-repo-ci-audit.json"),
        "merge_plan": load_json(LATEST / "pr-merge-queue-plan.json"),
        "pr_program": load_json(LATEST / "pr-program-run.json"),
        "cursor_agents": CURSOR_AGENTS,
        "recommended_agents": [],
    }
    data["recommended_agents"] = recommend_agents(data)

    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print("Recommended Cursor agents this run:")
    for r in data["recommended_agents"]:
        print(f"  - {r['agent']}: {r['reason']}")
    print("\nNext: cursor.com/automations or local Agent with prompt from .cursor/automations/<agent>.md")
    failed = [k for k, v in runs.items() if v.get("exit_code", 0) != 0 and not v.get("skipped")]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
