# Swarm observer — meta audit (`swarm_coverage`)

**Run id:** `swarm_observer-2026-05-29-swarm-coverage-r3`  
**Generated:** 2026-05-29T11:20Z  
**Research goal:** `swarm_coverage`  
**north_star_fit:** ecosystem, ai — gap registry, backlog apply, handoffs  
**Briefing hash:** `411fc1de96d0dd94` (compact snapshot 2026-05-29T10:36Z)  
**Orchestrator note:** `lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r3-missing-package-sweep.md`

---

## Executive summary

- **Posture: degraded** — ecosystem grade **D (64.0)**, `unattended_safe: false` (`benchmarks/data/latest/ecosystem-quality-report.json`, regenerated this pass; up from 60.3 as reconcile noise dropped in terminal sample).
- **Unattended operation: not safe** — 35 open PRs with failing CI, `agents_live: 0`, six of eight goal-directed runners not live, eight preflight scripts on `--skip-slow`.
- **SDK auth OK** — `CURSOR_API_KEY` set; recent DB `error` rows are predominantly `unregistered_running_reconciled` (supervisor tick preemption), not auth failures.
- **Swarm execution improving** — grade dimension 55 (was 40): 22 terminal runs sampled, 7 errors (32% → reconcile-dominated); 101 runs still `running` in files (stuck-SDK risk).
- **Briefing vs runs:** Heap prioritizes `pr_alignment`, governance agents; programmatic observer queued `implementation_gaps` + `proof_gap_researcher` retry (`li-cursor-agents/data/control-plane/state.json`).
- **Gap orchestration (orch-r3):** All three `missing_package` gaps patched to `pending` in `ecosystem-package-backlog.md`; registry orch-r3 row **closed**; handoff to `issue_planner` / `package_architect`.
- **Programmatic observer:** `retry_counts: {}`, `stopped_agents: []` — no auto-retry budget consumed; `needs_meta_observer: true` in local state.
- **Stale Supabase report:** `control_plane_reports.is_latest` still **2026-05-25** (`healthy: true`, 0 runs) — do not trust for live posture; use DB `agent_runs` + disk runs.

---

## Deliverable / findings

### Findings table

| Agent / area | Symptom | Evidence | Severity |
|--------------|---------|----------|----------|
| **Supervisor** | Mass `unregistered_running_reconciled` at ~10:51–10:53Z | `agent_runs.error` last 6h | high |
| **Ecosystem** | 35 failing PR CI | `benchmarks/data/latest/agent-briefing.json` | high |
| **Goal-directed** | 6 runners stopped, `agents_live: 0` | `lic/data/goal-directed-agents/snapshot.json` | high |
| **Gap registry** | 53 open gaps (3 package, 20 plan_debt, 30 competitor) | `registry.yaml`, `swarm-gap-actions.json` | medium |
| **Preflight** | `org_agent_kit_audit` exit 1 | `agent-briefing.preflight_runs` | medium |
| **Preflight** | 8× `--skip-slow` | same | medium |
| **agent_kit_maintainer** | Rollout succeeded (28 PRs); DB shows reconcile error on duplicate row | `agent_kit_maintainer-1780052164622.json` (finished) | low |
| **bug_fixer** | SDK `status: error` after long lic PR #319 attempt | `bug_fixer-1780051882294.json` | medium |
| **Dashboard** | `control_plane_reports` stale 4 days | Supabase `control_plane_reports` | medium |

### Error classification (sampled)

| Root cause | Evidence | Notes |
|------------|----------|-------|
| Supervisor reconcile / preempt | `error_snippet: unregistered_running_reconciled` | Exclude from leaf `error_rate` in observer |
| SDK run error (leaf) | `bug_fixer-1780051882294` — workspace/repo mismatch | Prompt: bind workspace repo to triage target |
| Stale preflight | Briefing 10:36Z, tick 11:19Z | Drop `--skip-slow` on degraded/meta ticks |
| Mock/finished mismatch | `agent_kit_maintainer` finished in JSON, error in DB | Reconcile status write order |

### Self-heal actions taken (programmatic observer)

| Action | Status |
|--------|--------|
| Auto-retry (`observer.retry_counts`) | **Empty** |
| `stopped_agents` | **[]** |
| Remediations | `dispatch_healer: implementation_gaps`, `retry_agent: proof_gap_researcher` |
| Gap ingest + apply | **Executed** — orch-r3 package todos confirmed `pending` |
| Meta observer dispatch | Quality report recommends `swarm_observer`, `gap_explorer`, `ecosystem_grader` |

### Gap orchestration (`swarm_coverage` / orch-r3)

| Metric | Value |
|--------|-------|
| Open gaps | 53 (3 `missing_package`, 20 `plan_debt`, 30 `competitor_feature`) |
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

- **lic** studio waves PRs #367–378 — governance review; no auto-merge.
- **roadmap** agent-kit PR #25 — human merge only.
- **28 agent-kit rollout PRs** — review + CI before merge (li-demo #15 red).
- **trusted.lean** / provability policy — human-approved issues only.

### Agent deliverable checklist

- [x] Ecosystem quality report regenerated (64.0, grade D)
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
