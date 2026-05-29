# Swarm observer — meta audit (`swarm_coverage`)

**Run id:** `swarm_observer-2026-05-29-swarm-coverage-r5`  
**Generated:** 2026-05-29T12:18Z  
**Research goal:** `swarm_coverage`  
**north_star_fit:** ecosystem, ai — gap registry, backlog apply, handoffs  
**Briefing hash:** `5ebb031963cff33b` (compact snapshot 2026-05-29T11:05Z; stale vs live tick)  
**Orchestrator note:** `lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r3-missing-package-sweep.md`

---

## Executive summary

- **Posture: critical** — ecosystem grade **D (64.0)**, `unattended_safe: false` (`benchmarks/data/latest/ecosystem-quality-report.json`, regenerated this pass).
- **Unattended operation: not safe** — 35 failing PR CI, `agents_live: 0`, six of eight goal-directed runners not live, 52 open swarm gaps, briefing preflight 1 failure + 8 skipped.
- **SDK auth OK** — `CURSOR_API_KEY` set; programmatic heal can dispatch agents.
- **Execution storm (12:14Z)** — parallel heap dispatch caused a **mass error burst** (~311 `error` rows in 2h); 710/718 terminal errors in 24h have **null completion** (reconcile/preempt bookkeeping, not leaf failures).
- **Gap orchestration (orch-r3): complete** — ingest + apply re-run; three `missing_package` gaps → `pending` in `ecosystem-package-backlog.md`; registry `orch-r3` row **closed**.
- **Programmatic observer:** `retry_counts: {}`, `stopped_agents: []`; remediations `implementation_gaps` + `workspace_sweeper`; local `swarm_health.healthy: true` with **goal_mismatch** only.
- **Stale Supabase report:** `control_plane_reports.is_latest` still **2026-05-25** — use DB `agent_runs` + `li-cursor-agents/data/control-plane/state.json` for live posture.
- **Next orchestrator todo:** `orch-r4-ui-ux-signals` (`ui_ux` / studio-ui-ux plan linkage).

---

## Deliverable / findings

### Findings table

| Agent / area | Symptom | Evidence | Severity |
|--------------|---------|----------|----------|
| **Swarm execution** | 33% error rate on last 16 terminal runs (grade sample) | `benchmarks/data/latest/ecosystem-quality-report.json` | critical |
| **DB reconcile noise** | 710/718 `error` rows (24h) with null `completion` | Supabase `agent_runs` | high |
| **Parallel dispatch** | 12:14Z burst: 10+ agents `error` within 30s, then re-`running` | `agent_runs` ORDER BY `started_at` | high |
| **Ecosystem** | 35 failing PR CI, 92 open PRs | `benchmarks/data/latest/agent-briefing.json` | high |
| **Goal-directed** | 6 runners stopped, `agents_live: 0` | `lic/data/goal-directed-agents/snapshot.json` | high |
| **Gap registry** | 52 open gaps (3 package, 19 plan_debt, 30 competitor) | `lic/data/swarm-gap-registry/registry.yaml` | high |
| **Briefing drift** | Top recommended not in recent runs (`goal_mismatch`) | `li-cursor-agents/data/control-plane/state.json` | medium |
| **Preflight** | `org_agent_kit_audit` exit 1 (28 repos need kit) | `agent-briefing.preflight_runs` | medium |
| **Dashboard** | `control_plane_reports` stale 4 days | Supabase `control_plane_reports` | medium |
| **SDK premature** | `output too short — SDK may have ended prematurely` | `agent_runs.completion` sample | medium |
| **Running-not-finalized** | 105+ runs `running` in 120-sample | grade `swarm-many-running` | low |

### Error classification (sampled)

| Root cause | Evidence | Notes |
|------------|----------|-------|
| Reconcile / preempt (bookkeeping) | 710 null `completion` on `status=error` | Exclude from leaf `error_rate`; tag `unregistered_running_reconciled` |
| Parallel dispatch collision | 12:14Z correlated errors across heap agents | Cap concurrent SDK dispatches per tick |
| SDK premature end | `completion.gaps` contains premature output | Retry budget; prompt min-output guard |
| Stale preflight | Briefing 11:05Z vs observer 12:16Z | Full audit on meta/degraded ticks (no `--skip-slow`) |
| Deliverable gap | PR body missing checklist (9 rows) | `pr_branch_opener` / template enforcement |

### Self-heal actions taken (programmatic observer)

| Action | Status |
|--------|--------|
| Auto-retry (`observer.retry_counts`) | **Empty** |
| `stopped_agents` | **[]** |
| Remediations (local state) | `dispatch_healer: implementation_gaps`, `retry_agent: workspace_sweeper` |
| Gap ingest + apply | **Executed** (`registry.yaml` 12:16Z, `swarm-gap-actions.json`) |
| Meta observer | This pass (`swarm_coverage` / orch-r3) |

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
| Error metrics | Classify reconcile rows; exclude from `swarm_execution` grade | `li-cursor-agents/src/observer/`, `benchmarks/scripts/ecosystem-quality-grade.py` |
| Dispatch | Per-tick concurrency cap for heap agents | `li-cursor-agents/src/supervisor/` |
| Reports | Upsert `control_plane_reports` each supervisor tick | `li-cursor-agents/src/control-plane/build-report.ts` |
| Preflight | Full audit on meta/degraded ticks | `benchmarks/scripts/agent-briefing.py` |
| Running runs | Reconcile stale `running` > N hours | `li-cursor-agents/src/db/reconcile-stale-runs.ts` |

### Human-only blockers

- **lic** studio waves PRs #367–379 — governance review; no auto-merge.
- **28 agent-kit rollout PRs** — review + CI before merge (li-demo #15 red).
- **trusted.lean** / provability policy — human-approved issues only.

### Agent deliverable checklist

- [x] Ecosystem quality report regenerated (64.0, grade D)
- [x] Control-plane DB queried (`agent_runs`, `control_plane_state`, `control_plane_reports`)
- [x] Local `state.json` + error classification
- [x] Gap ingest + apply (orch-r3)
- [x] Orchestrator note `orch-r3-missing-package-sweep`
- [x] Digest + JSON under `benchmarks/data/runs/`
- [ ] PR on `li-cursor-agents` for reconcile-aware grade + dispatch cap (recommended)
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
| feat(supervisor): cap parallel heap SDK dispatches per tick | li-cursor-agents | `control-plane` |

---

## Deferred

- `orch-r4-ui-ux-signals` — studio-ui-ux / `gui_ux_tester` → `ui_ux` gaps
- Observer metric + dispatch-cap PR on `li-cursor-agents` (`npm test` evidence)
- Plan-debt master_plan rows without runner backlog mapping (apply script defers)
- Tier-1 yellow bench (`matmul_blocked`) — `bench_improver` via implement goals
- Sync stale `control_plane_reports` to Supabase (ops / supervisor deploy)
