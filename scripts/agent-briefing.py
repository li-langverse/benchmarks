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
LIC = Path(os.environ.get("LIC_ROOT", ROOT.parent / "lic"))
ROADMAP = Path(os.environ.get("ROADMAP_ROOT", ROOT.parent / "roadmap"))

PREFLIGHT_SCRIPTS = [
    ("issue_triage", ["python3", "scripts/issue-feature-triage.py"]),
    ("issue_hygiene", ["python3", "scripts/issue-backlog-hygiene.py"]),
    ("plan_audit", ["python3", "scripts/plan-completion-audit.py"]),
    ("ecosystem_audit", ["python3", "scripts/ecosystem-audit.py"]),
    ("org_ci_audit", ["python3", "scripts/ensure-org-repo-ci.py"]),
    ("org_agent_kit_audit", ["python3", "scripts/ensure-org-agent-kit.py", "--local-only"]),
    ("explorer", ["python3", "scripts/ecosystem-explorer.py"]),
    ("merge_plan", ["python3", "scripts/pr-merge-queue-plan.py"]),
    ("pr_program", ["python3", "scripts/run-pr-program.py"]),
    ("pr_branch_hygiene", ["python3", "scripts/pr-branch-hygiene.py"]),
    ("ci_bug_triage", ["python3", "scripts/ci-bug-triage.py"]),
    ("security_cwe_audit", ["python3", "scripts/security-cwe-audit.py"]),
    ("workspace_dirty_sweep", ["python3", "scripts/workspace-dirty-sweep.py"]),
]

def _normalize_agent_skills(row: dict) -> list[str]:
    if row.get("skills"):
        return list(row["skills"])
    if row.get("skill"):
        return [str(row["skill"])]
    return []


def _enrich_cursor_agents(agents_root: Path) -> list[dict]:
    """Attach skill_paths under li-cursor-agents/.cursor/skills (SDK source of truth)."""
    skill_root = agents_root / ".cursor" / "skills"
    out: list[dict] = []
    for row in CURSOR_AGENTS:
        entry = dict(row)
        skills = _normalize_agent_skills(entry)
        if skills:
            entry["skills"] = skills
            entry.pop("skill", None)
        entry["skill_paths"] = [
            str(skill_root / sid / "SKILL.md") for sid in skills
        ]
        out.append(entry)
    return out


CURSOR_AGENTS = [
    {
        "id": "orchestrator",
        "prompt": ".cursor/automations/agent-orchestrator.md",
        "skill": "explore-control-plane-db",
        "when": "Weekly — route work from briefing",
    },
    {
        "id": "plan_verifier",
        "prompt": "li-cursor-agents/prompts/plan-verifier.md",
        "skill": "audit-plan-completion",
        "when": "Open plans / PH trackers vs reality",
        "preflight": ["plan_audit"],
    },
    {
        "id": "gap_explorer",
        "prompt": "li-cursor-agents/prompts/gap-explorer.md",
        "skill": "explore-li-ecosystem",
        "when": "Missing libs, HPC parity, Reddit/web SOTA",
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
        "id": "code_implementer",
        "prompt": "li-cursor-agents/prompts/code-implementer.md",
        "skills": ["explore-li-ecosystem", "audit-plan-completion", "push-li-github"],
        "when": "Implement gaps/queue items and open PRs",
        "preflight": ["plan_audit", "explorer", "ci_bug_triage"],
    },
    {
        "id": "bug_fixer",
        "prompt": "li-cursor-agents/prompts/bug-fixer.md",
        "skills": ["explore-li-ecosystem", "agent-diagnose-fix-li", "push-li-github"],
        "when": "CI failures (local-ci/GHA) and bug issues",
        "preflight": ["ci_bug_triage", "pr_program"],
    },
    {
        "id": "security_auditor",
        "prompt": "li-cursor-agents/prompts/security-auditor.md",
        "skill": "li-ecosystem-discipline",
        "when": "CVE/CWE catalog gaps across org repos",
        "preflight": ["security_cwe_audit"],
    },
    {
        "id": "issue_planner",
        "prompt": ".cursor/automations/issue-feature-planner.md",
        "skill": "plan-feature-from-issue",
        "when": "plan-needed / feature issues",
        "preflight": ["issue_triage"],
    },
    {
        "id": "issue_hygiene",
        "prompt": ".cursor/automations/issue-hygiene-agent.md",
        "when": "Duplicate/stale issues, explorer-finding bursts, backlog routing",
        "preflight": ["issue_hygiene", "issue_triage"],
    },
    {
        "id": "pr_branch_opener",
        "prompt": "li-cursor-agents/prompts/pr-branch-opener.md",
        "skill": "review-pr-alignment",
        "when": "Pushed branches with no open PR",
        "preflight": ["merge_plan", "pr_program", "pr_branch_hygiene"],
    },
    {
        "id": "pr_alignment",
        "prompt": ".cursor/automations/pr-alignment-agent.md",
        "skill": "review-pr-alignment",
        "when": "Open PRs vs vision / roadmap / philosophy; close superseded PRs",
        "preflight": ["merge_plan", "pr_program", "pr_branch_hygiene", "issue_triage"],
    },
    {
        "id": "pr_reviewer",
        "prompt": "li-cursor-agents/prompts/pr-reviewer.md",
        "skills": ["merge-approved-pr", "review-pr-alignment"],
        "when": "CI-green PRs — proof, security, perf, release notes",
        "preflight": ["merge_plan", "pr_program"],
    },
    {
        "id": "pr_merger",
        "prompt": "li-cursor-agents/prompts/pr-merger.md",
        "skills": ["plan-merge-queue", "merge-approved-pr"],
        "when": "merge-approved + gate ready + reviewed",
        "preflight": ["merge_plan", "pr_program"],
    },
    {
        "id": "numerics_researcher",
        "prompt": "li-cursor-agents/prompts/numerics-researcher.md",
        "skill": "research-li-numerics",
        "when": "Red benches — existing algorithms (books, libs, papers)",
        "preflight": ["ecosystem_audit", "explorer"],
    },
    {
        "id": "autoresearch",
        "prompt": "li-cursor-agents/prompts/autoresearch.md",
        "skills": ["numerics-autoresearch", "research-li-numerics"],
        "when": "Novel algos, pure_li reds, numerics-autoresearch issues",
        "preflight": ["ecosystem_audit", "explorer"],
    },
    {
        "id": "bench_improver",
        "prompt": "li-cursor-agents/prompts/bench-improver.md",
        "skills": ["research-li-numerics", "hpc-competitive-review"],
        "when": "Red/yellow dashboard rows — lic harness fixes",
        "preflight": ["ecosystem_audit"],
    },
    {
        "id": "docs_maintainer",
        "prompt": "li-cursor-agents/prompts/docs-maintainer.md",
        "skill": "explore-li-ecosystem",
        "when": "Missing live docs / handbook gaps",
        "preflight": ["ecosystem_audit", "explorer"],
    },
    {
        "id": "ci_maintainer",
        "prompt": "li-cursor-agents/prompts/ci-maintainer.md",
        "when": "Repos missing ci.yml on main",
        "preflight": ["org_ci_audit", "ecosystem_audit"],
    },
    {
        "id": "agent_kit_maintainer",
        "prompt": "li-cursor-agents/prompts/agent-kit-maintainer.md",
        "skills": ["li-ecosystem-discipline"],
        "when": "Repos missing or drifted roadmap agent-kit (.cursor rules/hooks)",
        "preflight": ["org_agent_kit_audit", "ecosystem_explorer"],
    },
    {
        "id": "workspace_sweeper",
        "prompt": "li-cursor-agents/prompts/workspace-sweeper.md",
        "when": "Uncommitted work in sibling clones — fallback commit/push/PR + restart stack",
        "preflight": ["workspace_dirty_sweep"],
    },
]


def run_script(name: str, cmd: list[str], skip_slow: bool) -> dict:
  # merge_plan must run every briefing — pr_merger depends on ordered queue
    slow = name in (
        "explorer",
        "plan_audit",
        "pr_program",
        "pr_branch_hygiene",
        "ci_bug_triage",
        "security_cwe_audit",
        "issue_hygiene",
    )
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


def _has_agent(rec: list[dict], agent_id: str) -> bool:
    return any(r.get("agent") == agent_id for r in rec)


def build_agent_deliverable_gaps(data: dict) -> dict:
    deliverable = data.get("agent_pr_deliverable_gate") or {}
    plan = data.get("plan_completion_audit") or {}
    plan_open = 0
    if isinstance(plan, dict):
        plan_open = int((plan.get("summary") or {}).get("total_findings", 0) or 0)
    incomplete = []
    if isinstance(deliverable, dict):
        incomplete = deliverable.get("agent_incomplete_runs") or []
    failures = []
    if isinstance(deliverable, dict):
        failures = deliverable.get("failures") or []
    summary = deliverable.get("summary") if isinstance(deliverable, dict) else {}
    numerics_blocked = int((summary or {}).get("numerics_blocked", 0) or 0)
    return {
        "plan_open_items": plan_open,
        "incomplete_runs": len(incomplete),
        "agent_prs_blocked": len(failures),
        "numerics_without_evidence": numerics_blocked,
        "incomplete_run_rows": incomplete[:12],
        "agent_pr_failures": failures[:12],
    }


def recommend_agents(data: dict) -> list[dict]:
    rec: list[dict] = []

    plan = data.get("plan_completion_audit") or {}
    if isinstance(plan, dict) and plan.get("summary", {}).get("total_findings", 0) > 0:
        rec.append({"agent": "plan_verifier", "reason": "plan-completion-audit findings"})
        rec.append({"agent": "implementation_gaps", "reason": "cross-check plan vs implementation"})

    explorer = data.get("ecosystem_explorer") or {}
    if isinstance(explorer, dict):
        miss = [m for m in explorer.get("missing_std_modules", []) if m.get("status") == "missing"]
        if miss:
            rec.append({"agent": "gap_explorer", "reason": f"{len(miss)} missing std modules"})
        partial_hpc = [
            h
            for h in explorer.get("hpc_libraries", [])
            if h.get("li_status") in ("missing", "partial")
        ]
        if partial_hpc and not _has_agent(rec, "gap_explorer"):
            rec.append({"agent": "gap_explorer", "reason": f"{len(partial_hpc)} HPC library gaps"})
        kit = explorer.get("agent_kit") or {}
        if kit.get("drift") and not _has_agent(rec, "agent_kit_maintainer"):
            rec.append(
                {
                    "agent": "agent_kit_maintainer",
                    "reason": "agent-kit version mismatch across sibling clones",
                }
            )

    org_ci = data.get("org_ci_audit") or {}
    if isinstance(org_ci, dict):
        missing_ci = org_ci.get("repos_missing_ci") or []
        if missing_ci:
            rec.append({"agent": "ci_maintainer", "reason": f"{len(missing_ci)} repos missing CI on main"})

    kit_audit = data.get("org_agent_kit_audit") or {}
    if isinstance(kit_audit, dict):
        needing = kit_audit.get("repos_needing_sync") or []
        adoption = kit_audit.get("downstream_adoption") or {}
        if adoption.get("kit_bumped") and not _has_agent(rec, "agent_kit_maintainer"):
            rec.insert(
                0,
                {
                    "agent": "agent_kit_maintainer",
                    "reason": adoption.get("summary")
                    or "roadmap agent-kit bumped — downstream repos need adoption",
                },
            )
        elif needing and not _has_agent(rec, "agent_kit_maintainer"):
            version_behind = kit_audit.get("repos_version_behind") or []
            canon_v = kit_audit.get("canonical_version") or "?"
            if version_behind:
                reason = (
                    f"{len(version_behind)} repo(s) behind agent-kit {canon_v} "
                    f"({len(needing)} total need sync)"
                )
            else:
                reason = f"{len(needing)} repos missing or drifted agent-kit"
            rec.append({"agent": "agent_kit_maintainer", "reason": reason})

    audit = data.get("ecosystem_audit") or {}
    if isinstance(audit, dict):
        if audit.get("repos_without_live_docs"):
            rec.append(
                {
                    "agent": "docs_maintainer",
                    "reason": f"{len(audit['repos_without_live_docs'])} repos without live docs",
                }
            )
        if audit.get("missing_ci_on_main") and not _has_agent(rec, "ci_maintainer"):
            rec.append(
                {
                    "agent": "ci_maintainer",
                    "reason": f"{len(audit['missing_ci_on_main'])} repos missing CI (audit)",
                }
            )

    pr_hygiene = data.get("pr_branch_hygiene") or {}
    if isinstance(pr_hygiene, dict):
        n_branch = int((pr_hygiene.get("summary") or {}).get("branches_needing_pr") or 0)
        if n_branch > 0 and not _has_agent(rec, "pr_branch_opener"):
            rec.append(
                {
                    "agent": "pr_branch_opener",
                    "reason": f"{n_branch} branch(es) pushed without open PR",
                }
            )
        n_close = int((pr_hygiene.get("summary") or {}).get("prs_recommended_close") or 0)
        if n_close > 0 and not _has_agent(rec, "pr_alignment"):
            rec.append(
                {
                    "agent": "pr_alignment",
                    "reason": f"{n_close} PR(s) flagged for close/supersede review",
                }
            )

    ci_bug = data.get("ci_bug_triage") or {}
    if isinstance(ci_bug, dict):
        q = int((ci_bug.get("summary") or {}).get("work_queue_size") or 0)
        if q > 0 and not _has_agent(rec, "bug_fixer"):
            rec.append(
                {
                    "agent": "bug_fixer",
                    "reason": f"{q} CI/bug item(s) in work queue (local-ci + issues + GHA red)",
                }
            )
        if q > 0 and not _has_agent(rec, "code_implementer"):
            rec.append(
                {
                    "agent": "code_implementer",
                    "reason": "implement fixes from ci-bug-triage work queue",
                }
            )

    sec = data.get("security_cwe_audit") or {}
    if isinstance(sec, dict):
        gaps_n = int((sec.get("summary") or {}).get("catalog_gaps") or 0)
        wf_n = int((sec.get("summary") or {}).get("repos_without_security_workflow") or 0)
        if (gaps_n > 0 or wf_n > 0) and not _has_agent(rec, "security_auditor"):
            rec.append(
                {
                    "agent": "security_auditor",
                    "reason": f"CWE/catalog gaps={gaps_n}, repos missing security workflow={wf_n}",
                }
            )

    explorer = data.get("ecosystem_explorer") or {}
    if isinstance(explorer, dict) and explorer.get("missing_std_modules") and not _has_agent(
        rec, "code_implementer"
    ):
        rec.append(
            {
                "agent": "code_implementer",
                "reason": "implement missing std modules from explorer",
            }
        )

    pr_prog = data.get("pr_program") or {}
    if isinstance(pr_prog, dict) and pr_prog.get("open", 0) > 0:
        if not _has_agent(rec, "pr_alignment"):
            rec.append({"agent": "pr_alignment", "reason": "open PRs need alignment triage"})
        if pr_prog.get("ci_green", 0) > 0:
            rec.append({"agent": "pr_reviewer", "reason": "CI-green PRs ready for standards review"})
        if pr_prog.get("gate_ready_labeled", 0) > 0:
            rec.append({"agent": "pr_merger", "reason": "merge-approved PRs with passing gates"})

    merge_plan = data.get("merge_plan") or {}
    if isinstance(merge_plan, dict):
        seq = merge_plan.get("merge_sequence") or []
        nxt = merge_plan.get("next_merge") or merge_plan.get("merge_first")
        if nxt and not _has_agent(rec, "pr_merger"):
            rec.append(
                {
                    "agent": "pr_merger",
                    "reason": (
                        f"merge queue: next {nxt.get('repo')}#{nxt.get('number')} "
                        f"({len(seq)} in sequence)"
                    ),
                }
            )

    hygiene = data.get("issue_backlog_hygiene") or {}
    if isinstance(hygiene, dict):
        summary = hygiene.get("summary") or {}
        dup = int(summary.get("duplicate_clusters") or 0)
        stale_n = int(summary.get("stale_candidates") or 0)
        spam = int(summary.get("explorer_spam_repos") or 0)
        if (dup > 0 or stale_n > 3 or spam > 0) and not _has_agent(rec, "issue_hygiene"):
            rec.append(
                {
                    "agent": "issue_hygiene",
                    "reason": (
                        f"backlog hygiene: dup_clusters={dup} stale={stale_n} "
                        f"explorer_spam_repos={spam}"
                    ),
                }
            )

    triage = data.get("issue_triage") or {}
    if isinstance(triage, dict) and triage.get("needs_plan"):
        rec.append({"agent": "issue_planner", "reason": "issues need plans"})

    gaps = data.get("agent_deliverable_gaps") or {}
    if isinstance(gaps, dict):
        if gaps.get("incomplete_runs", 0) > 0 and not _has_agent(rec, "implementation_gaps"):
            rec.append(
                {
                    "agent": "implementation_gaps",
                    "reason": f"{gaps['incomplete_runs']} incomplete agent run(s) — SDK may have ended before PR/tests",
                }
            )
        if gaps.get("agent_prs_blocked", 0) > 0 and not _has_agent(rec, "pr_reviewer"):
            rec.append(
                {
                    "agent": "pr_reviewer",
                    "reason": f"{gaps['agent_prs_blocked']} agent PR(s) fail deliverable / test-evidence gate",
                }
            )
        if gaps.get("numerics_without_evidence", 0) > 0:
            if not _has_agent(rec, "numerics_researcher"):
                rec.append(
                    {
                        "agent": "numerics_researcher",
                        "reason": f"{gaps['numerics_without_evidence']} numerics PR(s) without bench/test proof",
                    }
                )
            if not _has_agent(rec, "autoresearch"):
                rec.append(
                    {
                        "agent": "autoresearch",
                        "reason": "autoresearch PR(s) missing li-tests/benchmarks evidence",
                    }
                )


    dirty = data.get("workspace_dirty_sweep") or {}
    if isinstance(dirty, dict):
        n_dirty = int(dirty.get("dirty_count") or 0)
        if n_dirty > 0 and not _has_agent(rec, "workspace_sweeper"):
            rec.insert(
                0,
                {
                    "agent": "workspace_sweeper",
                    "reason": f"{n_dirty} sibling repo(s) with uncommitted work — fallback sweep",
                },
            )

    bench = (data.get("ecosystem_audit") or {}).get("benchmarks") or {}
    if isinstance(bench, dict) and bench.get("red"):
        rec.append({"agent": "numerics_researcher", "reason": "red benchmark rows"})
        rec.append({"agent": "bench_improver", "reason": "fix red rows in lic harness"})
        pure_li = [
            r
            for r in bench["red"]
            if "pure_li" in str(r.get("benchmark", r.get("id", "")))
        ]
        if pure_li:
            rec.append({"agent": "autoresearch", "reason": f"{len(pure_li)} pure_li red — novel codegen path"})

    if not rec:
        rec.append({"agent": "orchestrator", "reason": "routine weekly sweep"})
    return rec


def load_org_roadmap(plan_audit: dict | None) -> dict:
    """Org roadmap context for agents — vision pillars + current PH debt."""
    vision_path = ROADMAP / "docs/ecosystem/vision-and-roadmap.md"
    pillars = ["easy", "ai-first", "secure", "provable", "blazingly-fast"]
    current_ph = None
    open_items = 0
    if isinstance(plan_audit, dict):
        summary = plan_audit.get("summary") or {}
        open_items = int(summary.get("total_findings") or summary.get("open_tracker_items") or 0)
        master = plan_audit.get("master_plan_open") or []
        if master:
            current_ph = str(master[0].get("item", ""))[:120]
    master_plan = LIC / "docs/superpowers/plans/2026-05-14-li-master-plan.md"
    if not current_ph and master_plan.is_file():
        for line in master_plan.read_text(encoding="utf-8").splitlines():
            if "PH-" in line and "[ ]" in line:
                current_ph = line.strip()[:120]
                break
    return {
        "loaded_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "vision_url": "https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/vision-and-roadmap.md",
        "engineering_standards_url": "https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/engineering-standards.md",
        "master_plan_url": "https://github.com/li-langverse/lic/blob/main/docs/superpowers/plans/2026-05-14-li-master-plan.md",
        "pillars": pillars,
        "current_ph": current_ph,
        "master_plan_open_items": open_items,
        "roadmap_repo": str(ROADMAP) if ROADMAP.is_dir() else None,
        "vision_local": str(vision_path) if vision_path.is_file() else None,
    }


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
        "issue_backlog_hygiene": load_json(LATEST / "issue-backlog-hygiene.json"),
        "plan_completion_audit": load_json(LATEST / "plan-completion-audit.json"),
        "ecosystem_audit": load_json(LATEST / "ecosystem-audit.json"),
        "ecosystem_explorer": load_json(LATEST / "ecosystem-explorer.json"),
        "org_ci_audit": load_json(LATEST / "org-repo-ci-audit.json"),
        "org_agent_kit_audit": load_json(LATEST / "org-agent-kit-audit.json"),
        "merge_plan": load_json(LATEST / "pr-merge-queue-plan.json"),
        "pr_program": load_json(LATEST / "pr-program-run.json"),
        "pr_branch_hygiene": load_json(LATEST / "pr-branch-hygiene.json"),
        "ci_bug_triage": load_json(LATEST / "ci-bug-triage.json"),
        "security_cwe_audit": load_json(LATEST / "security-cwe-audit.json"),
        "workspace_dirty_sweep": load_json(LATEST / "workspace-dirty-sweep.json"),
        "local_ci_results": load_json(LATEST / "local-ci-results.json"),
        "recommended_agents": [],
    }
    agents_root = Path(os.environ.get("LI_CURSOR_AGENTS_ROOT", ROOT.parent / "li-cursor-agents"))
    data["agent_skill_root"] = str(agents_root / ".cursor" / "skills")
    data["cursor_agents"] = _enrich_cursor_agents(agents_root)
    agents_enabled = os.environ.get("LI_CURSOR_AGENTS_ENABLED", "0") == "1"
    if (
        agents_enabled
        and agents_root.is_dir()
        and not args.skip_slow
        and subprocess.run(["which", "gh"], capture_output=True).returncode == 0
    ):
        runs["agent_deliverable_gate"] = run_script(
            "agent_deliverable_gate",
            ["python3", "scripts/agent-pr-deliverable-gate.py", "--sweep-agent-prs"],
            False,
        )
    else:
        runs["agent_deliverable_gate"] = {
            "skipped": True,
            "reason": "li-cursor-agents disabled (set LI_CURSOR_AGENTS_ENABLED=1 to scan)",
        }

    data["agent_pr_deliverable_gate"] = load_json(LATEST / "agent-pr-deliverable-gate.json")
    if not data["agent_pr_deliverable_gate"] and agents_root.is_dir():
        import importlib.util

        gate_path = ROOT / "scripts" / "agent-pr-deliverable-gate.py"
        if gate_path.is_file():
            spec = importlib.util.spec_from_file_location("agent_pr_deliverable_gate", gate_path)
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                incomplete_only = mod.scan_incomplete_runs(agents_root)
                if incomplete_only:
                    data["agent_pr_deliverable_gate"] = {
                        "agent_incomplete_runs": incomplete_only,
                        "failures": [],
                        "summary": {"incomplete_runs": len(incomplete_only)},
                    }

    data["agent_deliverable_gaps"] = build_agent_deliverable_gaps(data)
    data["agent_incomplete_runs"] = (
        (data.get("agent_pr_deliverable_gate") or {}).get("agent_incomplete_runs") or []
        if isinstance(data.get("agent_pr_deliverable_gate"), dict)
        else []
    )
    data["agent_pr_deliverable_failures"] = (
        (data.get("agent_pr_deliverable_gate") or {}).get("failures") or []
        if isinstance(data.get("agent_pr_deliverable_gate"), dict)
        else []
    )

    data["recommended_agents"] = recommend_agents(data)
    plan_audit = data.get("plan_completion_audit")
    data["org_roadmap"] = load_org_roadmap(plan_audit if isinstance(plan_audit, dict) else None)

    sys.path.insert(0, str(ROOT / "scripts"))
    from heap_plan import build_heap_plan  # noqa: E402

    data["heap_plan"] = build_heap_plan(data["recommended_agents"])

    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print("Recommended Cursor agents this run:")
    for r in data["recommended_agents"]:
        print(f"  - {r['agent']}: {r['reason']}")
    hp = data["heap_plan"]
    print(f"\nHeap coordinators ({len(hp.get('priority_order', []))}):")
    for layer in hp.get("layers", []):
        agents = ", ".join(a["agent"] for a in layer.get("agents", []))
        print(f"  - {layer['coordinator']}: {agents}")
    if hp.get("validation_errors"):
        print("Heap validation errors:", hp["validation_errors"])
    print("\nNext: cursor.com/automations or ./scripts/run-pr-program.py --execute")
    failed = [k for k, v in runs.items() if v.get("exit_code", 0) != 0 and not v.get("skipped")]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
