# Swarm observer — meta audit (`swarm_coverage` / orch-r4)

**Run id:** `swarm_observer-2026-05-29-swarm-coverage-r6`  
**Generated:** 2026-05-29T12:50Z  
**Research goal:** `swarm_coverage`  
**north_star_fit:** ecosystem, ai — gap registry, backlog apply, handoffs  
**Briefing hash:** `6dafd0f997c09105` (preflight 2026-05-29T12:43Z)  
**Orchestrator note:** `lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r4-ui-ux-signals.md`

---

## Executive summary

- **Posture: critical** — ecosystem grade **D (64.0)**, `unattended_safe: false` (`benchmarks/data/latest/ecosystem-quality-report.json`).
- **Unattended operation: not safe** — 36 failing PR CI, `agents_live: 0`, 52+ open swarm gaps, UX harness covers only `lic-docs` on Linux.
- **SDK auth OK** — `CURSOR_API_KEY` set; programmatic heal can dispatch agents.
- **orch-r4 complete** — five new `ui_ux` registry rows; studio wave 1 done; harness coverage gaps routed to `gui_ux_tester` / `studio_ui_ux_builder`.
- **Reconcile noise** — 739/806 `error` rows (24h) have null `completion` (preempt/bookkeeping); exclude from leaf failure rate.
- **Programmatic observer** — `retry_counts: {}`, `stopped_agents: []`; remediations `implementation_gaps` + `workspace_sweeper`; local `swarm_health.healthy: true` with **goal_mismatch**.
- **Stale Supabase report** — `control_plane_reports.is_latest` still **2026-05-25**; use DB `agent_runs` + `li-cursor-agents/data/control-plane/state.json`.
- **Next:** wave 2 studio plan todos (apply-actions) + full `ux-targets.json` audit run on Linux CI.

---

## Deliverable / findings

### Findings table

| Agent / area | Symptom | Evidence | Severity |
|--------------|---------|----------|----------|
| **Swarm execution** | 31% error rate on last 16 terminal runs (grade sample) | `benchmarks/data/latest/ecosystem-quality-report.json` | critical |
| **DB reconcile** | 739/806 `error` (24h) null `completion` | Supabase `agent_runs` | high |
| **UX harness** | 1 target audited; 5+ configured targets skipped | `ui-audit.json`, `ux-targets.json` | high |
| **Ecosystem** | 36 failing PR CI, 95 open PRs | `agent-briefing.json` | high |
| **Goal-directed** | `agents_live: 0`; studio-ui-ux stopped (wave 1 done) | `lic/data/goal-directed-agents/snapshot.json` | medium |
| **Gap registry** | 56 open gaps (4 `ui_ux` new) | `lic/data/swarm-gap-registry/registry.yaml` | high |
| **Briefing drift** | `goal_mismatch`: gap_explorer, agent_kit_maintainer not recent | `li-cursor-agents/data/control-plane/state.json` | medium |
| **Preflight** | 1 failure + 8 skipped (`--skip-slow`) | `agent-briefing.preflight_runs` | medium |
| **Dashboard** | `control_plane_reports` stale 4 days | Supabase | medium |
| **gui_ux_tester** | 17 errors / 24h, null completion | `agent_runs` | low (reconcile) |

### Error classification (sampled)

| Root cause | Evidence | Notes |
|------------|----------|-------|
| Reconcile / preempt | 739 null `completion` on `status=error` | Exclude from leaf `error_rate` |
| Parallel dispatch | 12:43–12:45Z correlated errors across heap | Cap concurrent SDK dispatches |
| UX harness gap | Only `lic-docs` in audit JSON | Not SDK failure — coverage |
| Stale dashboard report | `control_plane_reports` 2026-05-25 | Upsert each supervisor tick |

### Self-heal actions taken (programmatic observer)

| Action | Status |
|--------|--------|
| Auto-retry (`observer.retry_counts`) | **Empty** |
| `stopped_agents` | **[]** |
| Remediations | `dispatch_healer: implementation_gaps`, `retry_agent: workspace_sweeper` |
| Gap ingest + apply | **Executed** (orch-r4 `ui_ux` rows) |
| Meta observer | This pass |

### Gap orchestration (`swarm_coverage` / orch-r4)

| Metric | Value |
|--------|-------|
| Open gaps | **56** (4 `ui_ux`, 3 `missing_package`, 19 `plan_debt`, 30 `competitor_feature`) |
| New `ui_ux` | `gap-ux-audit-native-studio`, `gap-ux-audit-agents-dashboard`, `gap-ux-audit-world-studio-demo`, `gap-ux-studio-wave2-plan`, `gap-ux-cinematic-studio-handoff` |
| Studio wave 1 | **Complete** (11/11 todos) |
| Orch-r4 registry | `gap-plan-pending-swarm-observer-orch-r4-ui-ux-signals` → **closed** |
| Note | `lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r4-ui-ux-signals.md` |

### Recommended control-plane fixes

| Area | Change | Path |
|------|--------|------|
| UX preflight | Run full `ux-targets.json` on Linux meta ticks (not docs-only) | `benchmarks/scripts/agent-briefing.py` |
| Error metrics | Classify reconcile rows | `li-cursor-agents/src/observer/`, `ecosystem-quality-grade.py` |
| Reports | Upsert `control_plane_reports` each tick | `li-cursor-agents/src/control-plane/build-report.ts` |
| Gap ingest | Auto-ingest `ui_ux` from ui/ux-audit delta | `lic/scripts/swarm-gap-ingest.py` |

### Human-only blockers

- **lic** studio waves PRs #374–391 — governance review.
- **28 agent-kit rollout PRs** — human review before merge.
- **trusted.lean** — human-approved issues only.

### Agent deliverable checklist

- [x] Ecosystem quality report regenerated (64.0, grade D)
- [x] Control-plane DB queried
- [x] Local `state.json` + error classification
- [x] Gap ingest + apply (orch-r4 `ui_ux`)
- [x] Orchestrator note `orch-r4-ui-ux-signals`
- [x] Digest + JSON under `benchmarks/data/runs/`
- [ ] PR on `li-cursor-agents` for reconcile-aware grade + UX preflight expansion
- [x] No PRs merged by observer

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| chore(ecosystem): orch-r4 — ui_ux harness gaps + studio wave 2 todos | lic | `ecosystem`, `agent:swarm_observer` |
| feat(ux-harness): audit agents-dashboard + world-studio on Linux CI | li-cursor-agents | `ux`, `agent:gui_ux_tester` |
| feat(studio): wave 2 plan — native capture + dashboard friction | lic-studio-ui | `studio`, `agent:studio_ui_ux_builder` |
| refactor(agents): exclude reconcile errors from swarm_execution grade | li-cursor-agents | `control-plane` |
| fix(ci): li-demo PR #15 agent-kit sync | li-demo | `bug`, `ecosystem-ci` |

---

## Deferred

- Observer metric + dispatch-cap PR on `li-cursor-agents` (`npm test` evidence)
- Plan-debt master_plan rows without runner backlog mapping (apply defers)
- `lic-tetris`, `gui-gen-fixture`, `tui-app-fixture` harness targets (lower priority)
- Tier-1 yellow bench (`matmul_blocked`) — `bench_improver`
