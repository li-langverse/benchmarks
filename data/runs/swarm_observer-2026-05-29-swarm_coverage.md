# Swarm observer digest — `swarm_coverage`

> Meta-audit · 2026-05-29T19:10Z · north_star_fit: ecosystem + ai orchestration

## Executive summary

- **Health: degraded.** Grade **D** (66.3); not unattended-safe.
- **Swarm execution failing** — 31 stuck `running` rows (24h); observer idle; control-plane report stale (2026-05-25).
- **53 open registry gaps** — apply pipeline ran; 21 backlog patches this cycle.
- **6 red benchmarks** — numerics lane active (`bench_improver` ×3 running).
- **6 goal runners stopped** — httpd active on wrk soak todo.
- **Briefing drift: low** — recommended agents match heap priorities.
- **Primary error class:** SDK premature/error (not auth — `CURSOR_API_KEY` set).
- **Next:** orch-r4 ui_ux signals + stuck-run finalize control-plane fix.

## Deliverable / findings

Full report: [swarm_observer-1780081782468.md](./swarm_observer-1780081782468.md)

Detailed orch report: [lic/data/runs/swarm_observer-orch-r4-stuck-run-finalize.md](../../../lic/data/runs/swarm_observer-orch-r4-stuck-run-finalize.md)

Orchestrator note: [lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r4-stuck-run-finalize.md](../../../lic/docs/ecosystem/orchestrator-notes/2026-05-29-orch-r4-stuck-run-finalize.md)

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| fix(observer): finalize stuck SDK runs after timeout | li-cursor-agents | swarm, control-plane |
| fix(supervisor): refresh control_plane_reports each tick | li-cursor-agents | swarm, dashboard |
| fix(gap-ingest): httpd plan_pending vs registry closed dedupe | lic | swarm, plan-debt |
| research: PH-7e tier-1 matmul / gmres red rows | lic | numerics |

## Deferred

- `orch-r4-ui-ux-signals`
- Master-plan plan_debt without backlog mapping
- HPC competitor research (handoff-only)
