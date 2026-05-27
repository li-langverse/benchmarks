# Swarm observer report — li-langverse

**Run date:** 2026-05-27  
**Research goal:** `swarm_coverage` — Swarm gap orchestration — registry, backlog apply, handoffs  
**north_star_fit:** Swarm gap orchestration — registry, backlog apply, handoffs — domains: ecosystem, ai

---

## Executive summary

- **Overall:** **Degraded**; **not safe to run unattended** (`overall_score=67.9`, grade **D**, `unattended_safe: false`) — evidence: `data/latest/ecosystem-quality-report.json`
- **Main drivers:** failing PR CI + repos missing CI on main + benchmark red rows + preflight failures — evidence: `data/latest/ecosystem-quality-report.json` → `findings[]`
- **Swarm execution signal:** many runs still marked “running” (possible stuck SDK bookkeeping), plus non-trivial incomplete rate — evidence: `data/latest/ecosystem-quality-report.json` → `findings` (`swarm-many-running`, `swarm-incomplete-rate`)
- **Gap pipeline:** ingest/apply succeeded; open gaps now **49** with **22 competitor_feature** rows, but `verticals.toml` stub ingest is effectively blocked — evidence: `data/latest/swarm-gap-actions.json`, `../lic/data/swarm-gap-registry/registry.yaml`
- **Control-plane observability:** on-disk `data/control-plane/latest-report.json` + `data/control-plane/state.json` are **absent** in this workspace; DB “latest report” appears stale (only 2026-05-25), and `retry_counts/stopped_agents` are `null` — evidence: MCP `li-control-plane-db` queries (see Findings)
- **Can it run unattended?** **No** — too many CI failures + missing CI + preflight failures; also ambiguous “running” bookkeeping makes auto-heal riskier.

---

## Deliverable / findings

### Swarm health findings (table)

| Agent / subsystem | Symptom | Evidence path | Severity |
|---|---|---|---|
| `control-plane` (disk artifacts) | Expected `data/control-plane/latest-report.json` + `data/control-plane/state.json` missing from `benchmarks/data/` | Workspace scan: `benchmarks/data/` contains no `control-plane/` directory | High |
| `control-plane` (DB) | “Latest report” appears stale; only row is 2026-05-25 and still flagged `is_latest=true` | MCP `li-control-plane-db`: `SELECT ... FROM control_plane_reports ORDER BY generated_at DESC LIMIT 5;` | High |
| `control_plane_state` (DB) | `observer.retry_counts` and `stopped_agents` missing (`null`) | MCP `li-control-plane-db`: `SELECT payload->'observer'... FROM control_plane_state WHERE id=1;` | Medium |
| `swarm_execution` (scorecard) | Many runs still marked running; incomplete rate 40% | `data/latest/ecosystem-quality-report.json` → findings `swarm-many-running`, `swarm-incomplete-rate` | Medium |
| `gap pipeline` | `verticals.toml` stub ingest produced 0 additions → competitor-stub expansion is blocked | `../lic/docs/ecosystem/orchestrator-notes/2026-05-27-orch-r2-competitor-stubs.md` and registry gap `gap-infra-verticals-toml-missing-benchmarks-main` | High |
| `ecosystem posture` | CI is the dominant drag: 56 failing PRs; 33 repos missing CI on main | `data/latest/ecosystem-quality-report.json` → `findings[]` | High |
| `benchmarks` | 2 red rows remain (PH-5b/PH-7e) | `data/latest/ecosystem-quality-report.json` → `benchmark-red-rows` | High |
| `preflight` | 2 preflight scripts exited non-zero | `data/latest/ecosystem-quality-report.json` → `preflight-failures` | High |

### Recommended agents vs observed runs (drift check)

- **Recommended in scorecard**: `swarm_observer`, `ci_maintainer`, `plan_verifier`, `workspace_sweeper`, `implementation_gaps` — evidence: `data/latest/ecosystem-quality-report.json` → `recommended_agents[]`
- **Observed (DB vs disk mismatch)**: DB shows many recent runs but their `run_id` JSON isn’t present on disk in `li-cursor-agents/data/runs/` for some entries, and many are still flagged `running` even with a `finished_at` value — evidence: MCP query `agent_runs` (see “Control-plane fixes”)

Interpretation: the “what actually ran” signal is currently inconsistent across **disk**, **DB**, and the scorecard’s run sampling; this is a core “swarm degraded” indicator because self-heal decisions depend on accurate run status.

---

## Self-heal actions taken (this cycle)

- **Refreshed stale scorecard**: ran `python3 scripts/ecosystem-quality-grade.py` → rewrote `data/latest/ecosystem-quality-report.json` (generated_at `2026-05-27T12:58:53Z`).
- **Gap orchestration (Mode B)**:
  - ran `python3 scripts/swarm-gap-ingest.py` (in `lic`) → updated `lic/data/swarm-gap-registry/registry.yaml`
  - ran `python3 scripts/swarm-gap-apply-actions.py` (in `lic`) → rewrote `benchmarks/data/latest/swarm-gap-actions.json`
  - wrote orchestrator note in `lic`: `docs/ecosystem/orchestrator-notes/2026-05-27-orch-r2-competitor-stubs.md`

---

## Recommended control-plane fixes (self-healing improvements)

### Fix 1 — make control-plane disk artifacts canonical (or stop requiring them)

- **Problem**: this run could not satisfy checklist items (2) and (3) because `benchmarks/data/control-plane/` files do not exist in this repo checkout.
- **Recommendation**: either
  - **write** the generated control-plane report/state into a well-known path inside `benchmarks/data/` during preflight, or
  - **update the swarm_observer prompt** to treat DB as source of truth and only read disk if present.

### Fix 2 — status normalization for “running” bookkeeping

- **Problem**: scorecard flags “many running”; DB sample includes runs where `status='running'` but `finished_at` is populated.
- **Recommendation**: in control plane, normalize status:
  - if `finished_at IS NOT NULL` then status must be terminal (`finished`/`error`) and never `running`
  - add an observer rule: if run is “running” for >N minutes without heartbeats/events, auto-mark `hung` and enqueue a retry up to budget.

### Fix 3 — persist `observer.retry_counts` + `stopped_agents`

- **Problem**: DB `control_plane_state.payload->observer` subfields are `null`, blocking auditability of auto-heal.
- **Recommendation**: ensure supervisor writes these fields every tick; if absent, emit a “state_schema_regressed” intervention.

Evidence (DB queries used):

```sql
SELECT id, briefing_hash, generated_at, is_latest
FROM control_plane_reports
ORDER BY generated_at DESC
LIMIT 5;

SELECT updated_at,
  payload->'observer'->'retry_counts' AS retry_counts,
  payload->'observer'->'stopped_agents' AS stopped_agents
FROM control_plane_state
WHERE id=1
LIMIT 1;

SELECT run_id, agent_id, status, started_at, finished_at
FROM agent_runs
ORDER BY started_at DESC
LIMIT 30;
```

---

## Human-only blockers

- **CI & governance**: fixing “repos missing CI on main” and mass PR CI failures often touches org policy / protected branches and should not be auto-merged.
- **Missing/invalid SDK creds**: if `CURSOR_API_KEY` is missing or invalid, SDK-driven agents will not self-heal; the observer can only surface this.
- **Roadmap/governance edits**: must remain PR-only with human approval.

---

## Recommended issues/PRs

- **(benchmarks)** “Restore canonical `benchmarks/competitive/verticals.toml` on main so swarm-gap ingest can emit competitor stubs”  
  - **labels**: `orchestration`, `competitor_feature`, `swarm_coverage`
  - **evidence**: `../lic/data/swarm-gap-registry/registry.yaml` → `gap-infra-verticals-toml-missing-benchmarks-main`
- **(li-cursor-agents)** “Normalize agent run status: forbid `status=running` when `finished_at` is set; add hung-run sweeper”  
  - **labels**: `control-plane`, `observer`, `swarm_health`
  - **evidence**: MCP `agent_runs` sample + `data/latest/ecosystem-quality-report.json` finding `swarm-many-running`
- **(li-cursor-agents)** “Persist observer audit fields in `control_plane_state.payload.observer` (`retry_counts`, `stopped_agents`)”  
  - **labels**: `control-plane`, `observability`
  - **evidence**: MCP `control_plane_state` query (null fields)
- **(ci_maintainer lane)** “Batch-repair 33 repos missing CI on main; focus on unblock list from ecosystem audit”  
  - **labels**: `ci`, `ecosystem_posture`
  - **evidence**: `data/latest/ecosystem-quality-report.json` finding `repos-missing-ci`

---

## Deferred

- Deep triage of specific leaf-agent error traces: many DB `run_id` JSONs were not present in local `li-cursor-agents/data/runs/`, so I avoided speculative root-cause labeling without trace artifacts.
- Any product-code performance work on red benchmarks (PH-5b/PH-7e): routed as handoffs only (proof-before-perf).

---

## Agent deliverable checklist

- [x] Refreshed `ecosystem_quality_report`
- [x] Ran gap ingest/apply pipeline (`swarm_coverage`)
- [x] Wrote orchestrator note in `lic`
- [x] Wrote this report under `benchmarks/data/runs/`

