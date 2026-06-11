#!/usr/bin/env python3
"""Deterministic ecosystem quality scorecard for swarm meta-agents.

Reads agent-briefing.json, optional goal-directed snapshot, swarm-gap-actions,
ecosystem-audit embeds, and a sample of li-cursor-agents data/runs/*.json.

Writes data/latest/ecosystem-quality-report.json (no LLM, no network).
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/latest/ecosystem-quality-report.json"
LATEST = ROOT / "data/latest"
def _resolve_agents_root() -> Path:
    env = os.environ.get("LI_CURSOR_AGENTS_ROOT")
    if env:
        return Path(env)
    for candidate in (ROOT.parent / "li-cursor-agents", Path("/app")):
        if (candidate / "data/runs").is_dir():
            return candidate
    return ROOT.parent / "li-cursor-agents"


AGENTS_ROOT = _resolve_agents_root()
LIC_ROOT = Path(os.environ.get("LIC_ROOT", ROOT.parent / "lic"))
SNAPSHOT = LIC_ROOT / "data/goal-directed-agents/snapshot.json"
RUNS_DIR = AGENTS_ROOT / "data/runs"
MAX_RUN_SAMPLE = 120


def _load_json(path: Path) -> dict | list | None:
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _parse_ts(raw: str | None) -> datetime | None:
    if not raw or not isinstance(raw, str):
        return None
    s = raw.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def _clamp(n: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, n))


def _letter_grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def score_briefing(briefing: dict | None) -> tuple[float, list[dict], dict]:
    findings: list[dict] = []
    if not briefing:
        findings.append(
            {
                "id": "briefing-missing",
                "severity": "critical",
                "message": "agent-briefing.json missing — run agent-briefing.py",
                "evidence": str(LATEST / "agent-briefing.json"),
            }
        )
        return 0.0, findings, {"briefing_present": False}

    score = 100.0
    generated = _parse_ts(str(briefing.get("generated_at", "")))
    if generated:
        age_h = (datetime.now(timezone.utc) - generated.astimezone(timezone.utc)).total_seconds() / 3600
        if age_h > 48:
            score -= 25
            findings.append(
                {
                    "id": "briefing-stale",
                    "severity": "high",
                    "message": f"Briefing older than 48h ({age_h:.0f}h)",
                    "evidence": str(LATEST / "agent-briefing.json"),
                }
            )
        elif age_h > 24:
            score -= 12
            findings.append(
                {
                    "id": "briefing-aging",
                    "severity": "medium",
                    "message": f"Briefing older than 24h ({age_h:.0f}h)",
                    "evidence": str(LATEST / "agent-briefing.json"),
                }
            )

    preflight = briefing.get("preflight_runs") or {}
    failed = 0
    skipped = 0
    for key, row in preflight.items():
        if not isinstance(row, dict):
            continue
        if row.get("skipped"):
            skipped += 1
            continue
        ec = row.get("exit_code")
        if ec is not None and int(ec) != 0:
            failed += 1
    if failed:
        deduct = min(35, failed * 8)
        score -= deduct
        findings.append(
            {
                "id": "preflight-failures",
                "severity": "high" if failed >= 2 else "medium",
                "message": f"{failed} preflight script(s) exited non-zero",
                "evidence": "agent-briefing.preflight_runs",
            }
        )
    if skipped >= 4:
        score -= min(15, skipped * 2)
        findings.append(
            {
                "id": "preflight-skipped",
                "severity": "medium",
                "message": f"{skipped} preflight scripts skipped (--skip-slow)",
                "evidence": "agent-briefing.preflight_runs",
            }
        )

    rec = briefing.get("recommended_agents") or []
    signals = {
        "briefing_present": True,
        "preflight_failed": failed,
        "preflight_skipped": skipped,
        "recommended_agent_count": len(rec) if isinstance(rec, list) else 0,
    }
    return _clamp(score), findings, signals


def score_ecosystem_posture(briefing: dict | None) -> tuple[float, list[dict], dict]:
    findings: list[dict] = []
    audit = None
    if briefing and isinstance(briefing.get("ecosystem_audit"), dict):
        audit = briefing["ecosystem_audit"]
    if audit is None:
        audit = _load_json(LATEST / "ecosystem-audit.json")
    if not audit:
        return 70.0, findings, {"audit_present": False}

    score = 100.0
    metrics = audit.get("metrics") or {}
    failed_prs = int(metrics.get("failed_prs") or 0)
    open_prs = int(metrics.get("open_prs") or 0)
    missing_ci = int(metrics.get("repos_missing_ci_main") or 0)
    missing_docs = int(metrics.get("repos_without_live_pages") or 0)

    if failed_prs:
        score -= min(30, failed_prs * 2)
        findings.append(
            {
                "id": "failed-pr-ci",
                "severity": "high" if failed_prs >= 10 else "medium",
                "message": f"{failed_prs} open PR(s) with failing CI",
                "evidence": "ecosystem-audit.metrics.failed_prs",
            }
        )
    if missing_ci:
        score -= min(25, missing_ci * 3)
        findings.append(
            {
                "id": "repos-missing-ci",
                "severity": "high",
                "message": f"{missing_ci} repos missing CI on main",
                "evidence": "ecosystem-audit.metrics.repos_missing_ci_main",
            }
        )
    if missing_docs >= 5:
        score -= min(15, missing_docs)
        findings.append(
            {
                "id": "repos-missing-live-docs",
                "severity": "low",
                "message": f"{missing_docs} repos without live docs pages",
                "evidence": "ecosystem-audit.metrics.repos_without_live_pages",
            }
        )

    bench = audit.get("benchmarks") or {}
    reds = bench.get("red") or []
    if reds:
        score -= min(25, len(reds) * 5)
        findings.append(
            {
                "id": "benchmark-red-rows",
                "severity": "high",
                "message": f"{len(reds)} red benchmark row(s)",
                "evidence": "ecosystem-audit.benchmarks.red",
            }
        )

    signals = {
        "audit_present": True,
        "open_prs": open_prs,
        "failed_prs": failed_prs,
        "repos_missing_ci_main": missing_ci,
        "benchmark_red_count": len(reds),
    }
    return _clamp(score), findings, signals


def score_goal_directed(snapshot: dict | None) -> tuple[float, list[dict], dict]:
    findings: list[dict] = []
    if not snapshot:
        return 75.0, findings, {"snapshot_present": False}

    score = 100.0
    runners = snapshot.get("runners") or []
    if not isinstance(runners, list) or not runners:
        return 80.0, findings, {"snapshot_present": True, "runner_count": 0}

    stopped = 0
    pending = 0
    total_todos = 0
    for r in runners:
        if not isinstance(r, dict):
            continue
        if not r.get("running"):
            stopped += 1
        todos = r.get("todos") or []
        if isinstance(todos, list):
            for t in todos:
                if not isinstance(t, dict):
                    continue
                total_todos += 1
                if t.get("status") != "completed":
                    pending += 1

    if stopped:
        score -= min(30, stopped * 12)
        findings.append(
            {
                "id": "goal-runners-stopped",
                "severity": "high",
                "message": f"{stopped} goal-directed runner(s) not running",
                "evidence": str(SNAPSHOT),
            }
        )
    if total_todos and pending / total_todos > 0.55:
        score -= 15
        findings.append(
            {
                "id": "goal-plan-backlog",
                "severity": "medium",
                "message": f"{pending}/{total_todos} plan todos still pending",
                "evidence": str(SNAPSHOT),
            }
        )

    signals = {
        "snapshot_present": True,
        "runner_count": len(runners),
        "runners_stopped": stopped,
        "plan_todos_pending": pending,
        "plan_todos_total": total_todos,
        "agents_live": snapshot.get("agents_live"),
    }
    return _clamp(score), findings, signals


def sample_runs() -> list[dict]:
    if not RUNS_DIR.is_dir():
        return []
    files = sorted(RUNS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    out: list[dict] = []
    for path in files[:MAX_RUN_SAMPLE]:
        row = _load_json(path)
        if isinstance(row, dict):
            row["_path"] = str(path)
            out.append(row)
    return out


def score_swarm_execution(runs: list[dict]) -> tuple[float, list[dict], dict]:
    findings: list[dict] = []
    if not runs:
        return 65.0, findings, {"runs_sampled": 0}

    score = 100.0
    terminal = [r for r in runs if r.get("status") in ("finished", "error", "cancelled", "incomplete")]
    errors = [r for r in terminal if r.get("status") == "error"]
    incomplete = [r for r in terminal if r.get("status") == "incomplete"]
    running = [r for r in runs if r.get("status") == "running"]

    n_term = len(terminal) or 1
    err_rate = len(errors) / n_term
    inc_rate = len(incomplete) / n_term

    if err_rate > 0.25:
        score -= 35
        findings.append(
            {
                "id": "swarm-error-rate",
                "severity": "critical",
                "message": f"Error rate {err_rate:.0%} over last {len(terminal)} terminal runs",
                "evidence": str(RUNS_DIR),
            }
        )
    elif err_rate > 0.12:
        score -= 20
        findings.append(
            {
                "id": "swarm-error-rate",
                "severity": "high",
                "message": f"Error rate {err_rate:.0%} over last {len(terminal)} terminal runs",
                "evidence": str(RUNS_DIR),
            }
        )
    elif err_rate > 0.05:
        score -= 10

    if inc_rate > 0.15:
        score -= min(20, int(inc_rate * 100))
        findings.append(
            {
                "id": "swarm-incomplete-rate",
                "severity": "medium",
                "message": f"Incomplete rate {inc_rate:.0%}",
                "evidence": str(RUNS_DIR),
            }
        )

    if len(running) >= 8:
        score -= 10
        findings.append(
            {
                "id": "swarm-many-running",
                "severity": "medium",
                "message": f"{len(running)} runs still marked running (possible stuck SDK)",
                "evidence": str(RUNS_DIR),
            }
        )

    by_agent: dict[str, int] = {}
    for r in errors:
        aid = str(r.get("agentId") or "unknown")
        by_agent[aid] = by_agent.get(aid, 0) + 1
    top_err = sorted(by_agent.items(), key=lambda x: -x[1])[:3]

    signals = {
        "runs_sampled": len(runs),
        "terminal_runs": len(terminal),
        "error_count": len(errors),
        "incomplete_count": len(incomplete),
        "running_count": len(running),
        "error_rate": round(err_rate, 4),
        "incomplete_rate": round(inc_rate, 4),
        "top_error_agents": [{"agent": a, "count": c} for a, c in top_err],
    }
    return _clamp(score), findings, signals


def score_gap_pressure() -> tuple[float, list[dict], dict]:
    findings: list[dict] = []
    gap = _load_json(LATEST / "swarm-gap-actions.json")
    if not gap:
        return 85.0, findings, {"gap_report_present": False}

    open_gaps = int(gap.get("open_gaps") or 0)
    score = 100.0
    if open_gaps > 50:
        score -= 30
        sev = "high"
    elif open_gaps > 30:
        score -= 18
        sev = "medium"
    elif open_gaps > 15:
        score -= 8
        sev = "low"
    else:
        sev = None

    if sev:
        findings.append(
            {
                "id": "swarm-gap-backlog",
                "severity": sev,
                "message": f"{open_gaps} open gap(s) in registry apply pipeline",
                "evidence": str(LATEST / "swarm-gap-actions.json"),
            }
        )

    by_kind = gap.get("by_kind") or {}
    plan_debt = int(by_kind.get("plan_debt") or 0) if isinstance(by_kind, dict) else 0
    if plan_debt > 25:
        score -= 10
        findings.append(
            {
                "id": "plan-debt-gaps",
                "severity": "medium",
                "message": f"{plan_debt} plan_debt gap rows",
                "evidence": "swarm-gap-actions.by_kind.plan_debt",
            }
        )

    signals = {
        "gap_report_present": True,
        "open_gaps": open_gaps,
        "by_kind": by_kind,
    }
    return _clamp(score), findings, signals


def build_recommended_agents(
    overall: float,
    dim_scores: dict[str, float],
    briefing: dict | None,
) -> list[dict]:
    out: list[dict] = []
    if dim_scores.get("swarm_execution", 100) < 75:
        out.append(
            {
                "agent": "swarm_observer",
                "reason": "swarm_execution dimension below 75 — meta audit runs/errors",
            }
        )
    if dim_scores.get("gap_pressure", 100) < 80:
        out.append(
            {
                "agent": "gap_explorer",
                "reason": "gap_pressure dimension below 80 — reconcile swarm-gap registry",
            }
        )
    if overall < 70:
        out.append(
            {
                "agent": "ecosystem_grader",
                "reason": "overall ecosystem quality below 70 — narrative grade + dispatch order",
            }
        )
    if dim_scores.get("ecosystem_posture", 100) < 70:
        out.append(
            {
                "agent": "ci_maintainer",
                "reason": "ecosystem_posture weak — missing CI / failed PR signals",
            }
        )
    if dim_scores.get("briefing_health", 100) < 80:
        out.append(
            {
                "agent": "plan_verifier",
                "reason": "briefing_health weak — refresh plan audit preflight",
            }
        )

    seen = {r["agent"] for r in out}
    if briefing and isinstance(briefing.get("recommended_agents"), list):
        for row in briefing["recommended_agents"][:3]:
            if not isinstance(row, dict):
                continue
            agent = row.get("agent")
            if agent and agent not in seen:
                out.append(
                    {
                        "agent": agent,
                        "reason": f"briefing P0: {row.get('reason', '')}"[:120],
                    }
                )
                seen.add(agent)
    return out[:8]


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    briefing_path = LATEST / "agent-briefing.json"
    briefing = _load_json(briefing_path)
    snapshot = _load_json(SNAPSHOT)
    runs = sample_runs()

    weights = {
        "briefing_health": 0.15,
        "ecosystem_posture": 0.25,
        "goal_directed_health": 0.20,
        "swarm_execution": 0.25,
        "gap_pressure": 0.15,
    }

    all_findings: list[dict] = []
    dimensions: dict[str, dict] = {}

    scorers = [
        ("briefing_health", score_briefing, briefing),
        ("ecosystem_posture", score_ecosystem_posture, briefing),
        ("goal_directed_health", score_goal_directed, snapshot),
        ("swarm_execution", score_swarm_execution, runs),
        ("gap_pressure", score_gap_pressure, None),
    ]

    dim_scores: dict[str, float] = {}
    for dim_id, fn, arg in scorers:
        if dim_id == "gap_pressure":
            score, findings, signals = fn()
        elif dim_id == "swarm_execution":
            score, findings, signals = fn(arg)  # type: ignore[arg-type]
        else:
            score, findings, signals = fn(arg)  # type: ignore[arg-type]
        dim_scores[dim_id] = score
        all_findings.extend(findings)
        dimensions[dim_id] = {
            "score": round(score, 1),
            "weight": weights[dim_id],
            "signals": signals,
            "finding_count": len(findings),
        }

    overall = sum(dim_scores[k] * weights[k] for k in weights)
    overall = round(_clamp(overall), 1)
    grade = _letter_grade(overall)
    unattended_safe = overall >= 75 and dim_scores["swarm_execution"] >= 70

    report = {
        "generated_at": now,
        "role": "ecosystem_quality_scorecard",
        "overall_score": overall,
        "grade": grade,
        "unattended_safe": unattended_safe,
        "dimensions": dimensions,
        "findings": sorted(
            all_findings,
            key=lambda f: {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(
                str(f.get("severity")), 9
            ),
        ),
        "recommended_agents": build_recommended_agents(overall, dim_scores, briefing),
        "inputs": {
            "briefing": str(briefing_path),
            "goal_directed_snapshot": str(SNAPSHOT) if snapshot else None,
            "runs_dir": str(RUNS_DIR),
            "runs_sampled": len(runs),
            "swarm_gap_actions": str(LATEST / "swarm-gap-actions.json"),
        },
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"overall_score={overall} grade={grade} unattended_safe={unattended_safe}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
