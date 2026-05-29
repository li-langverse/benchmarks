# Swarm observer — meta audit (`swarm_coverage`)

**Run id:** `swarm_observer-2026-05-29-swarm-coverage-r4`  
**Generated:** 2026-05-29T12:00Z  
**Research goal:** `swarm_coverage`  
**north_star_fit:** ecosystem, ai — gap registry, backlog apply, handoffs  
**Briefing hash:** `32439f2bba84e2c1` (compact snapshot 2026-05-29T11:05Z)  
**Orchestrator note:** `lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r3-missing-package-sweep.md`

---

## Executive summary

- **Posture: degraded** — ecosystem grade **C (72.8)**, `unattended_safe: false` (`benchmarks/data/latest/ecosystem-quality-report.json`, regenerated this pass).
- **Unattended operation: not safe** — 35 open PRs with failing CI, `agents_live: 0`, six of eight goal-directed runners not live, eight preflight scripts on `--skip-slow`.
- **SDK auth OK** — `CURSOR_API_KEY` set; DB shows 718 `error` rows in 24h but the latest terminal sample has **0% leaf error rate** (115 `running`, 5 terminal) — reconcile noise dominates historical counts.
- **Async swarm active** — supervisor tick at 11:59Z dispatched heap agents (`pr_alignment`, `implementation_gaps`, `bug_fixer`, etc.); local `swarm_health.healthy: true` with **goal_mismatch** finding only.
- **Gap orchestration (orch-r3): complete** — ingest + apply re-run; three `missing_package` gaps patched to `pending` in `ecosystem-package-backlog.md`; registry orch-r3 row **closed**; handoff to `issue_planner` / `package_architect`.
- **Programmatic observer:** `retry_counts: {}`, `stopped_agents: []`; remediations queued `implementation_gaps` + `workspace_sweeper` (goal-align).
- **Stale Supabase report:** `control_plane_reports.is_latest` still **2026-05-25** — use DB `agent_runs` + disk runs for live posture.
- **Next orchestrator todo:** `orch-r4-ui-ux-signals` (`ui_ux` / studio-ui-ux plan linkage).

---

## Deliverable / findings

### Findings table

| Agent / area | Symptom | Evidence | Severity |
|--------------|---------|----------|----------|
| **Ecosystem** | 35 failing PR CI | `benchmarks/data/latest/agent-briefing.json` | high |
| **Goal-directed** | 6 runners stopped, `agents_live: 0` | `lic/data/goal-directed-agents/snapshot.json` | high |
| **Gap registry** | 52 open gaps (3 package, 19 plan_debt, 30 competitor) | `lic/data/swarm-gap-registry/registry.yaml`, `swarm-gap-actions.json` | high |
| **Briefing drift** | Top recommended agents not in recent reconcile sample | `li-cursor-agents/data/control-plane/state.json` → `goal_mismatch` | medium |
| **Preflight** | `org_agent_kit_audit` exit 1 (28 repos need kit) | `agent-briefing.preflight_runs` | medium |
| **Preflight** | 8× `--skip-slow` (plan_audit, ci_bug_triage, …) | same | medium |
| **bug_fixer** | SDK `status: error` after long lic PR #319 attempt | `li-cursor-agents/data/runs/bug_fixer-1780051882294.json` | medium |
| **Dashboard** | `control_plane_reports` stale 4 days | Supabase `control_plane_reports` | medium |
| **Swarm files** | 115+ runs `running` in 120-sample (SDK finalize lag) | `ecosystem-quality-report` → `swarm-many-running` | low |
| **agent_kit_maintainer** | 5 `finished` in 6h window | DB `agent_runs` | low |

### Error classification (sampled)

| Root cause | Evidence | Notes |
|------------|----------|-------|
| Supervisor reconcile / preempt | Historical `unregistered_running_reconciled` in DB | Exclude from leaf `error_rate` in observer |
| SDK run error (leaf) | `bug_fixer-1780051882294` — workspace `li-demo`, triage target `lic` | Prompt: bind workspace repo to triage `repo` field |
| Stale preflight | Briefing 11:05Z vs tick 11:59Z | Drop `--skip-slow` on degraded/meta ticks |
| Running-not-finalized | 115 `running` in grade sample | Reconcile stale `running` > N hours |

### Self-heal actions taken (programmatic observer)

| Action | Status |
|--------|--------|
| Auto-retry (`observer.retry_counts`) | **Empty** |
| `stopped_agents` | **[]** |
| Remediations (local state) | `dispatch_healer: implementation_gaps`, `retry_agent: workspace_sweeper` (goal-align) |
| Gap ingest + apply | **Executed** this pass (`registry.yaml` updated_at 12:00Z) |
| Meta observer dispatch | Quality report recommends `gap_explorer`, `ecosystem_grader`, `ci_maintainer` |

### Gap orchestration (`swarm_coverage` / orch-r3)

| Metric | Value |
|--------|-------|
| Open gaps | 52 (3 `missing_package`, 19 `plan_debt`, 30 `competitor_feature`) |
| Package backlog | `pkg-line-profiler`, `pkg-std-summary`, `pkg-std-plot` → **pending** |
| Orch-r3 registry | `gap-plan-pending-swarm-observer-orch-r3-missing-package-sweep` → **closed** |
| Note | `lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r3-missing-package-sweep.md` |
| Next | `orch-r4-ui-ux-signals` |

### Recommended control-plane fixes

| Area | Change | Path |
|------|--------|------|
| Error metrics | Classify `unregistered_running_reconciled`; exclude from grade | `li-cursor-agents/src/observer/` |
| Reports | Upsert `control_plane_reports` each supervisor tick | `li-cursor-agents/src/supervisor/` |
| Preflight | Full audit on meta/degraded ticks (no `--skip-slow`) | `benchmarks/scripts/agent-briefing.py` |
| bug_fixer | Workspace repo must match triage `repo` field | `li-cursor-agents/prompts/bug-fixer.md` |
| Running runs | Reconcile stale `running` > N hours | `li-cursor-agents/src/control-plane/finalize-run.ts` |

### Human-only blockers

- **lic** studio waves PRs #367–379 — governance review; no auto-merge.
- **roadmap** agent-kit PR #25 — human merge only.
- **28 agent-kit rollout PRs** — review + CI before merge (li-demo #15 red).
- **trusted.lean** / provability policy — human-approved issues only.

### Agent deliverable checklist

- [x] Ecosystem quality report regenerated (72.8, grade C)
- [x] Control-plane DB queried (`agent_runs`, `control_plane_state`, `control_plane_reports`)
- [x] Local `state.json` + error run samples
- [x] Gap ingest + apply (orch-r3)
- [x] Orchestrator note `orch-r3-missing-package-sweep`
- [x] Digest + JSON under `benchmarks/data/runs/`
- [ ] PR on `li-cursor-agents` for observer reconcile metrics (recommended)
- [x] No PRs merged by observer

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| feat(ecosystem): tracking issues for std.summary, std.plot, line_profiler | lic | `ecosystem`, `PH-IO`, `agent:issue_planner` |
| chore(ecosystem): close orch-r3 — package backlog pending + registry | lic | `ecosystem`, `agent:swarm_observer` |
| chore(benchmarks): add `competitive/verticals.toml` on main | benchmarks | `ecosystem`, `agent:docs_maintainer` |
| fix(ci): li-demo PR #15 agent-kit sync | li-demo | `bug`, `ecosystem-ci` |
| refactor(agents): exclude reconcile errors from swarm_execution grade | li-cursor-agents | `control-plane` |
| chore(agent-kit): resolve org_agent_kit_audit preflight exit 1 | benchmarks | `ecosystem-ci` |

---

## Deferred

- `orch-r4-ui-ux-signals` — studio-ui-ux / `gui_ux_tester` → `ui_ux` gaps
- Observer metric PR on `li-cursor-agents` (`npm test` evidence)
- Plan-debt master_plan rows without runner backlog mapping (apply script defers)
- Tier-1 yellow bench (`matmul_blocked`) — `bench_improver` via implement goals
- Sync stale `control_plane_reports` to Supabase (ops / supervisor deploy)
