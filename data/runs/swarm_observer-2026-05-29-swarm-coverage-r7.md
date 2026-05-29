# Swarm observer — meta audit (`swarm_coverage` / orch-r3)

**Run id:** `swarm_observer-2026-05-29-swarm-coverage-r7`  
**Generated:** 2026-05-29T12:58Z  
**Research goal:** `swarm_coverage`  
**north_star_fit:** ecosystem, ai — gap registry, backlog apply, handoffs  
**Briefing hash:** `6dafd0f997c09105` (preflight 2026-05-29T12:44Z)  
**Orchestrator note:** `lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r3-missing-package-sweep.md`

---

## Executive summary

- **Posture: critical** — ecosystem grade **D (64.0)**, `unattended_safe: false` (`benchmarks/data/latest/ecosystem-quality-report.json`).
- **Unattended operation: not safe** — 36 failing PR CI, `agents_live: 0`, six of eight goal-directed runners not live, 57 open swarm gaps, 1 preflight failure + 8 skipped.
- **SDK auth OK** — `CURSOR_API_KEY` set; programmatic heal can dispatch agents.
- **DB error noise dominates** — 739/807 `error` rows (24h) have **null `completion`** (reconcile/preempt bookkeeping); true leaf failures are a small fraction with structured `completion.gaps`.
- **Execution stress** — 38% error rate on last 30 terminal runs (grade sample); parallel heap dispatch at 12:43–12:50Z correlates multi-agent `error`/`running` flips.
- **Gap orchestration (orch-r3): complete** — ingest + apply re-run; three `missing_package` gaps → `pending` in `ecosystem-package-backlog.md`; orch-r3 plan/registry rows **closed**; swarm-observer backlog **5/5 done**.
- **Programmatic observer:** `retry_counts: {}`, `stopped_agents: []`; remediations `implementation_gaps` + `workspace_sweeper`; local `swarm_health.healthy: true` with **goal_mismatch** only.
- **Stale Supabase report:** `control_plane_reports.is_latest` still **2026-05-25** — use DB `agent_runs` + `li-cursor-agents/data/control-plane/state.json` for live posture.

---

## Deliverable / findings

### Findings table

| Agent / area | Symptom | Evidence | Severity |
|--------------|---------|----------|----------|
| **Swarm execution** | 38% error rate on last 30 terminal runs | `benchmarks/data/latest/ecosystem-quality-report.json` | critical |
| **DB reconcile noise** | 739/807 `error` rows (24h) null `completion` | Supabase `agent_runs` | high |
| **Parallel dispatch** | 12:43–12:50Z burst: 10+ agents `error`/`running` within minutes | `agent_runs` ORDER BY `started_at` | high |
| **Ecosystem** | 36 failing PR CI, 95 open PRs | `benchmarks/data/latest/agent-briefing.json` | high |
| **Goal-directed** | 6 runners stopped, `agents_live: 0` | `lic/data/goal-directed-agents/snapshot.json` | high |
| **Gap registry** | 57 open gaps (3 package, 19 plan_debt, 5 ui_ux, 30 competitor) | `lic/data/swarm-gap-registry/registry.yaml` | high |
| **Briefing drift** | Top recommended not in recent runs (`goal_mismatch`) | `li-cursor-agents/data/control-plane/state.json` | medium |
| **Preflight** | `org_agent_kit_audit` exit 1 (28 repos need kit) | `agent-briefing.preflight_runs` | medium |
| **Dashboard** | `control_plane_reports` stale 4 days | Supabase `control_plane_reports` | medium |
| **SDK premature** | `tools=0`, `output too short` | `li-cursor-agents/data/runs/docs_maintainer-*.json` | medium |
| **Workspace sweep** | systemd restart `li-agents-async-swarm.service` failed | `workspace_sweeper` digest 12:45Z | low |

### Error classification (sampled)

| Root cause | Evidence | Notes |
|------------|----------|-------|
| Reconcile / preempt (bookkeeping) | 739 null `completion` on `status=error` (24h) | Exclude from leaf `error_rate`; tag `unregistered_running_reconciled` |
| Parallel dispatch collision | Correlated errors across heap agents 12:43Z | Cap concurrent SDK dispatches per tick |
| SDK premature end | `completion.gaps`: premature; `tools=0` | Retry budget; session lock / min-output guard |
| Stale preflight | Briefing 12:27Z vs observer 12:58Z | Full audit on meta/degraded ticks (no `--skip-slow`) |
| Deliverable gap | PR agents without PR URL | `pr_branch_opener` completion sample |

### Self-heal actions taken (programmatic observer)

| Action | Status |
|--------|--------|
| Auto-retry (`observer.retry_counts`) | **Empty** |
| `stopped_agents` | **[]** |
| Remediations (local state) | `dispatch_healer: implementation_gaps`, `retry_agent: workspace_sweeper` |
| Gap ingest + apply | **Executed** this pass |
| Meta observer | This pass (`swarm_coverage` / orch-r3) |

### Gap orchestration (`swarm_coverage` / orch-r3)

| Metric | Value |
|--------|-------|
| Open gaps | 57 (3 `missing_package`, 19 `plan_debt`, 5 `ui_ux`, 30 `competitor_feature`) |
| Package backlog | `pkg-line-profiler`, `pkg-std-summary`, `pkg-std-plot` → **pending** |
| Orch-r3 registry | `gap-plan-pending-swarm-observer-orch-r3-missing-package-sweep` → **closed** |
| Swarm-observer plan | **5/5 completed** (`orch-r0`…`orch-r4`) |
| Note | `lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r3-missing-package-sweep.md` |

### Recommended control-plane fixes

| Area | Change | Path |
|------|--------|------|
| Error metrics | Classify reconcile rows; exclude from `swarm_execution` grade | `li-cursor-agents/src/observer/`, `benchmarks/scripts/ecosystem-quality-grade.py` |
| Dispatch | Per-tick concurrency cap for heap agents | `li-cursor-agents/src/supervisor/` |
| Reports | Upsert `control_plane_reports` each supervisor tick | `li-cursor-agents/src/control-plane/build-report.ts` |
| Preflight | Full audit on meta/degraded ticks | `benchmarks/scripts/agent-briefing.py` |
| Running runs | Reconcile stale `running` > N hours | `li-cursor-agents/src/db/reconcile-stale-runs.ts` |
| SDK session | Investigate `tools=0` premature runs | `li-cursor-agents/src/backends/cursor-sdk-backend.js` |

### Human-only blockers

- **lic** studio waves PRs #374–391 — governance review; no auto-merge.
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
| fix(ci): li-demo PR #15 agent-kit sync | li-demo | `bug`, `ecosystem-ci` |
| refactor(agents): exclude reconcile errors from swarm_execution grade | li-cursor-agents | `control-plane` |
| feat(supervisor): cap parallel heap SDK dispatches per tick | li-cursor-agents | `control-plane` |
| chore(benchmarks): refresh org agent-kit audit preflight on main | benchmarks | `ecosystem`, `agent:ci_maintainer` |

---

## Deferred

- Observer metric + dispatch-cap PR on `li-cursor-agents` (`npm test` evidence)
- Plan-debt master_plan rows without runner backlog mapping (apply script defers)
- Tier-1 yellow bench (`matmul_blocked`) — `bench_improver` via implement goals
- `issue_planner` package tracking issues from pending backlog rows
