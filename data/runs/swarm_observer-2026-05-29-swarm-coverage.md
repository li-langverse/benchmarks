# Swarm observer — meta audit (`swarm_coverage`)

**Run id:** `swarm_observer-2026-05-29-swarm-coverage`  
**Generated:** 2026-05-29T10:54Z  
**Research goal:** `swarm_coverage`  
**north_star_fit:** ecosystem, ai — gap registry, backlog apply, handoffs  
**Briefing hash:** `411fc1de96d0dd94` (compact snapshot 2026-05-29T10:36Z)

---

## Executive summary

- **Posture: degraded** — ecosystem grade **D (60.3)**, `unattended_safe: false` (`benchmarks/data/latest/ecosystem-quality-report.json`, regenerated this pass).
- **Unattended operation: not safe** — 35 open PRs with failing CI, 6/8 goal-directed runners not live (`agents_live: 0`), eight preflight scripts on `--skip-slow`.
- **SDK auth OK** — `CURSOR_API_KEY` set; dominant failures are supervisor tick preemption and historical SDK timeouts, not missing API key.
- **DB vs disk:** Supabase shows **860** `error` rows vs **19** terminal file runs in grade sample — most errors are reconcile/preemption at tick boundaries (`10:51Z` wave), not leaf agent logic failures.
- **Briefing alignment:** Heap prioritizes `pr_alignment`, governance (`plan_verifier`, `implementation_gaps`), ecosystem maintainers; research lane dispatches `proof_gap_researcher` and this `swarm_observer` pass correctly.
- **Gap orchestration (orch-r2):** Ingest/apply re-run; **30** open `competitor_feature` gaps; **8** vertical-stub rows appended to `sim-md-research-backlog.md`; orchestrator note written.
- **Programmatic observer:** `control_plane/state.json` reports `healthy: true`, `retry_counts: {}`, remediations include `retry_agent: proof_gap_researcher` and `dispatch_healer: implementation_gaps` at `2026-05-29T10:53:07Z`.
- **Stale dashboard report:** `control_plane_reports` latest row still **2026-05-25** — local `latest-report.json` is e2e fixture; do not treat as production swarm_health.

---

## Deliverable / findings

### Findings table

| Agent / area | Symptom | Evidence | Severity |
|--------------|---------|----------|----------|
| **Supervisor** | Mass `error` at tick start (~10:51Z) | `agent_runs` recent rows; runs `*-178005178*` | high |
| **swarm_observer** | Prior SDK timeout (~8.2h, 0 tools) | `li-cursor-agents/data/runs/swarm_observer-1779968173877.json` | medium |
| **Ecosystem** | 35 failing PR CI | `benchmarks/data/latest/agent-briefing.json` → `ecosystem_audit` | high |
| **Goal-directed** | 6 runners stopped | `lic/data/goal-directed-agents/snapshot.json` | high |
| **Preflight** | `org_agent_kit_audit` exit 1 | `agent-briefing.preflight_runs` | medium |
| **Preflight** | 8× `--skip-slow` | same | medium |
| **Gap registry** | 54 open gaps | `registry.yaml`, `swarm-gap-actions.json` | medium |
| **httpd runner** | Plan log stale ~65h | snapshot `httpd.log_age_sec` | medium |
| **workspace_sweeper** | `systemctl try-restart` failed | sweep digest in run `workspace_sweeper-1780051891568` | low |

### Error classification (sampled)

| Root cause | Evidence | Notes |
|------------|----------|-------|
| Supervisor reconcile / preempt | DB errors at identical `started_at`; prior run still `running` in JSON | Not counted in refreshed grade terminal sample (19 runs, 26% error_rate) |
| SDK timeout | `swarm_observer-1779968173877` — `duration_ms=29453368`, `tools=0` | Add max-duration watchdog in `cursor-sdk-backend` |
| Stale preflight | Briefing 10:36Z, dispatch 10:51Z | Enable slow preflights on meta-audit ticks |
| Repo conflict | Dirty lic + benchmarks per briefing | `workspace_sweeper` opened/updated sweep PRs |

### Self-heal actions taken (programmatic observer)

| Action | Status |
|--------|--------|
| Auto-retry (`observer.retry_counts`) | **Empty** — no budget consumed this cycle |
| `stopped_agents` | **[]** |
| Remediations queued | `retry_agent: proof_gap_researcher`, `dispatch_healer: implementation_gaps` |
| `goal_mismatch` finding | Medium — top briefing agents not in recent DB sample |
| Gap ingest + apply | **Executed** — see `orch-r2` note |
| `swarm_degraded` / meta observer | Grade D triggers `swarm_observer` + `gap_explorer` in quality report |

### Gap orchestration (`swarm_coverage` / orch-r2)

| Metric | Value |
|--------|-------|
| Open gaps | 54 (3 `missing_package`, 21 `plan_debt`, 30 `competitor_feature`) |
| Ingest | `verticals_stubs: 0`, `competitor_catalog: 0` (already ingested) |
| Apply | Patches to package + sim backlogs; 8 competitor appends to `sim-md-research-backlog.md` |
| Note | `lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r2-competitor-stubs.md` |
| Closed | `gap-plan-pending-swarm-observer-orch-r2-competitor-stubs` |

**Open `missing_package` handoffs (orch-r3 next):**

| Gap | Backlog todo | Handoff |
|-----|--------------|---------|
| `gap-line-profiler-001` | `pkg-line-profiler` | `issue_planner` |
| `gap-missing-std-std-summary` | `pkg-std-summary` | `issue_planner`, `package_architect` |
| `gap-missing-std-std-plot` | `pkg-std-plot` | `issue_planner`, `package_architect` |

### Recommended control-plane fixes

| Area | Change | Path |
|------|--------|------|
| Error metrics | Exclude reconcile/preempt from `error_rate` | `li-cursor-agents/src/observer/` |
| Reports | Sync `control_plane_reports` each tick | `li-cursor-agents/src/supervisor/` |
| Preflight | Drop `--skip-slow` on meta-audit / degraded ticks | `benchmarks/scripts/agent-briefing.py` |
| SDK | Cap run duration; surface `error_kind` in `completion` | `li-cursor-agents/src/backends/cursor-sdk-backend.js` |
| latest-report.json | Point local default away from e2e fixture | `li-cursor-agents/data/control-plane/` |

### Human-only blockers

- **lic** studio PRs #367–378 — governance review; no auto-merge.
- **roadmap** policy PRs — human only.
- **workspace_sweeper** async-swarm `systemctl --user` restart — host ops.
- Failing **li-demo** / **li-gui** checkout bump PRs — CI fix before merge.

### Agent deliverable checklist

- [x] Ecosystem quality report regenerated (`60.3`, grade D)
- [x] Control-plane DB queried (`agent_runs`, `control_plane_state`, `control_plane_reports`)
- [x] Local `state.json` + error run samples
- [x] Gap ingest + apply
- [x] Orchestrator note `orch-r2-competitor-stubs`
- [x] Digest + JSON under `benchmarks/data/runs/`
- [ ] PR on `li-cursor-agents` for observer metrics (recommended only)
- [x] No PRs merged by observer

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| chore(ecosystem): close orch-r2 — competitor vertical stubs in registry + MD backlog | lic | `ecosystem`, `agent:swarm_observer` |
| chore(benchmarks): add `competitive/verticals.toml` on main | benchmarks | `ecosystem`, `agent:docs_maintainer` |
| chore(agent-kit): fix `org_agent_kit_audit` preflight (exit 1) | benchmarks | `ecosystem-ci` |
| feat(package): tracking issues for std.summary / std.plot / line_profiler | lic | `ecosystem`, `PH-IO` |
| fix(ci): li-demo PR #15 agent-kit sync | li-demo | `bug`, `ecosystem-ci` |
| refactor(agents): exclude reconcile errors from swarm_execution grade | li-cursor-agents | `control-plane` |

---

## Deferred

- `orch-r3-missing-package-sweep` — package backlog sweep + registry closure
- `orch-r4-ui-ux-signals` — studio-ui-ux / `gui_ux_tester` → `ui_ux` gaps
- Observer metric PR on `li-cursor-agents` (`npm test` evidence)
- Plan-debt master_plan rows without runner backlog mapping (deferred by apply script)
- Tier-1 yellow bench (`matmul_blocked`) — `bench_improver` via implement goals
