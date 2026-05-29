# Swarm observer — meta audit (`swarm_coverage`)

**Run id:** `swarm_observer-2026-05-29-swarm-coverage`  
**Generated:** 2026-05-29T10:12Z  
**Research goal:** `swarm_coverage`  
**north_star_fit:** ecosystem, ai — gap registry, backlog apply, handoffs  
**Briefing hash:** `e5fad788e09b81ca` (compact snapshot 2026-05-29T10:05Z)

---

## Executive summary

- **Posture: degraded → critical** after fresh grade: **F (59.0)**, `unattended_safe: false` (`benchmarks/data/latest/ecosystem-quality-report.json`).
- **Unattended operation: not safe** — 35 failing PRs, 6/8 goal-directed runners not live, preflight `--skip-slow` hides triage/PR program.
- **Dominant “errors” are orchestration artifacts:** 548/742 DB errors are `unregistered_running_reconciled` (supervisor restarted lane while SDK runs were in-flight); not SDK auth (`CURSOR_API_KEY` is set).
- **Briefing alignment:** Heap + recommended agents match active dispatch (`proof_gap_researcher`, `workspace_sweeper`, platform maintainers); `swarm_observer` invoked correctly via `swarm_execution` &lt; 75.
- **Gap orchestration (orch-r3):** 3 open `missing_package` gaps patched to `ecosystem-package-backlog.md`; ingest/apply re-run this cycle.
- **Programmatic observer:** `retry_counts` empty, `stopped_agents` [] — no auto-retries this tick; latest `control_plane_reports` still **2026-05-25** (`swarm_health.healthy: true` stale).
- **Self-heal:** Mass re-dispatch at 10:11Z after 10:09Z reconcile wave; prior tick runs marked error without leaf failure.
- **Human blockers:** Failing lic studio PRs (#367–378), governance merges, registry/backlog drift on closed `std.io`/`std.csv` gaps.

---

## Findings

| Agent / area | Symptom | Evidence | Severity |
|--------------|---------|----------|----------|
| **All lanes** | `unregistered_running_reconciled` burst | `agent_runs.error` (548 total); runs `*-178004933*` at 10:09Z | high |
| **Supervisor / reports** | Stale `swarm_health` | `control_plane_reports` latest `2026-05-25`, `needs_meta_observer: false` | high |
| **Ecosystem** | 35 open PRs failing CI | `agent-briefing.json` → `ecosystem_audit.failed_prs` | high |
| **Goal-directed** | 6 runners stopped, `agents_live: 0` | `lic/data/goal-directed-agents/snapshot.json` | high |
| **Preflight** | `org_agent_kit_audit` exit 1 | `agent-briefing.preflight_runs` | medium |
| **Preflight** | 8 scripts `--skip-slow` | same | medium |
| **httpd runner** | Plan log stale ~65h | snapshot `httpd.status_note` | medium |
| **Package backlog** | `pkg-std-io`/`pkg-std-csv` pending but gaps **closed** | registry.yaml vs `ecosystem-package-backlog.md` | medium |
| **benchmarks** | `verticals.toml` missing on main | `gap-infra-verticals-toml-missing-benchmarks-main` | medium |
| **docs_maintainer / ci_maintainer** | Historical terminal errors (sampled file runs) | `ecosystem-quality-report` top_error_agents | low |

### Error classification (sampled `*-178004933*`)

| Root cause | Count (this wave) | Notes |
|------------|-------------------|-------|
| Supervisor reconcile (`unregistered_running_reconciled`) | ~15 agents | Preempted at tick boundary; some produced partial output (e.g. `workspace_sweeper` md) |
| SDK auth | 0 this wave | `CURSOR_API_KEY=set` |
| Stale preflight | Partial | Briefing 10:05Z; mass dispatch 10:09Z |
| Repo conflict | N/A in wave | Dirty lic/benchmarks per briefing |

---

## Self-heal actions taken (programmatic observer)

| Action | Status |
|--------|--------|
| Auto-retry failed agents (`observer.retry_counts`) | **None** — `{}` at `control_plane_state` 2026-05-29T10:11:04Z |
| Stopped agents | **None** |
| Healer dispatch (`bug_fixer`, `workspace_sweeper`, `implementation_gaps`) | Supervisor re-queued at 10:11Z (runs now `running`) |
| Gap ingest + apply | **Executed this audit** — 18 backlog patches |
| `swarm_degraded` surface | Grade script recommends `swarm_observer` + `ecosystem_grader` |

---

## Gap orchestration (`swarm_coverage` / orch-r3)

**Registry:** `lic/data/swarm-gap-registry/registry.yaml` — 54 open (3 `missing_package`, 21 `plan_debt`, 30 `competitor_feature`)  
**Apply log:** `benchmarks/data/latest/swarm-gap-actions.json`  
**Orchestrator note:** `lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r3-missing-package-sweep.md`

### Open `missing_package` → handoffs

| Gap | Backlog todo | Handoff |
|-----|--------------|---------|
| `gap-line-profiler-001` | `pkg-line-profiler` | `issue_planner` |
| `gap-missing-std-std-summary` | `pkg-std-summary` | `issue_planner`, `package_architect` |
| `gap-missing-std-std-plot` | `pkg-std-plot` | `issue_planner`, `package_architect` |

**Drift:** `pkg-std-io`, `pkg-std-csv` still `pending` while registry gaps **closed** — route to `issue_planner` to complete or re-open.

---

## Recommended control-plane fixes

| Area | Change | Path |
|------|--------|------|
| Error metrics | Exclude `unregistered_running_reconciled` / `stale_running_reconciled` from `error_rate` | `li-cursor-agents/src/observer/` |
| Reports freshness | Write `control_plane_reports` each supervisor tick | `li-cursor-agents/src/supervisor/` |
| Preflight | Run `ci_bug_triage`, `pr_program` on meta-audit ticks (not `--skip-slow`) | `benchmarks/scripts/agent-briefing.py` |
| Deliverable gate | Enable `LI_CURSOR_AGENTS_ENABLED=1` for `agent_deliverable_gate` | env / briefing |
| Reconcile UX | Set `meta.error_reason` on reconcile | `li-cursor-agents/src/lanes/research-lane.ts` |

No new agent registry ids. No lic systemd plan loops.

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| chore(ecosystem): reconcile pkg-std-io / pkg-std-csv backlog vs closed gaps | lic | `ecosystem`, `agent:issue_planner` |
| feat(package): seed li-line-profiler tracking issue (WP-B) | lic or lip | `ecosystem`, `PH-7e` |
| chore(benchmarks): add competitive/verticals.toml on main | benchmarks | `ecosystem`, `agent:docs_maintainer` |
| chore(agent-kit): fix org_agent_kit_audit preflight (exit 1) | benchmarks | `ecosystem-ci` |
| fix(ci): li-demo PR #15 agent-kit sync | li-demo | `ecosystem-ci`, `bug` |

---

## Human-only blockers

- Merge/review **lic** PRs #367–378 (studio waves) — do not auto-merge.
- **roadmap** governance PRs — human review only.
- **workspace_sweeper** `systemctl --user try-restart li-agents-async-swarm.service` failed on host — ops, not agent code.
- Registry/backlog closure for std.io/csv — human or `issue_planner` judgment.

---

## Agent deliverable checklist

- [x] Ecosystem quality report read/regenerated
- [x] Control-plane DB queried (`agent_runs`, `control_plane_state`, `control_plane_reports`)
- [x] Gap ingest + apply executed
- [x] Orchestrator note `orch-r3-missing-package-sweep`
- [x] This digest under `benchmarks/data/runs/`
- [ ] PR on `li-cursor-agents` for observer metric fix (deferred — recommend only)
- [ ] No PRs merged by observer

---

## Deferred

- `orch-r2-competitor-stubs` — vertical stub backlog patches (see `2026-05-29-orch-r2-competitor-stubs.md`)
- `orch-r4-ui-ux-signals` — studio-ui-ux plan linkage
- `orch-r1-plan-debt-sync` — httpd dedupe (mostly closed in registry)
- Observer PR for reconcile-error filtering
- Tier-1 red bench rows — `bench_improver` / `numerics_researcher` via implement goals, not this pass
