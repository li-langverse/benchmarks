# Ecosystem grader — proactive sweep

**Run id:** `ecosystem_grader-2026-05-29-proactive`  
**Generated:** 2026-05-29T11:19Z  
**Source:** proactive  
**north_star_fit:** ecosystem, provable (PH-2i, PH-7d/e), ai-first — orchestration before implementers; proof → easy → fast  
**Briefing:** `agent-briefing.json` @ 2026-05-29T11:05Z  
**Scorecard:** `data/latest/ecosystem-quality-report.json` @ 2026-05-29T11:19:09Z (regenerated this pass)

---

## Executive summary

- **Grade D · overall 64.0 / 100** — `unattended_safe: false` ([scorecard](data/latest/ecosystem-quality-report.json)).
- **Swarm execution is the binding constraint** (55.0): **32% error rate** on 22 terminal SDK runs; **98** runs still `running` (stuck-reconcile risk).
- **Ecosystem posture weak** (57.0): **92** open PRs, **35** with failing CI, **0** red tier-1 benchmarks but heavy PR debt.
- **Goal-directed loops starved** (70.0): **6/8** runners not live, `agents_live: 0`, **25/90** plan todos pending; only **httpd** supervisor active.
- **Gap pressure elevated** (70.0): **53** open registry gaps (3 `missing_package`, 20 `plan_debt`, 30 `competitor_feature`).
- **Briefing health moderate** (77.0): briefing present; **1** preflight fail (`org_agent_kit_audit`), **8** slow preflights skipped.
- **Do not dispatch implementers until meta lane runs** — scorecard orders `swarm_observer` → `gap_explorer`; briefing P0 still needs `workspace_sweeper` + governance agents.
- **Benchmarks lane is green for tier-1** (`benchmark_red_count: 0`); perf work is yellow/near-threshold, not blocking orchestration.

---

## Dimension drill-down

### briefing_health (77.0 · weight 0.15)

Preflight produced a usable briefing (`briefing_present: true`, **12** recommended agents). Signal quality is reduced: **`org_agent_kit_audit` exit 1** (28 repos missing/drifted kit; canonical `1.3.5+6018e18bf2ed91f4`), and **eight** audits were skipped under `--skip-slow` (`plan_audit`, `ci_bug_triage`, `pr_program`, etc.). That leaves plan/PR/CI triage stale relative to the 11:05Z snapshot — governance agents should run with full preflight on the next meta tick, not assume skipped sections are green.

### ecosystem_posture (57.0 · weight 0.25)

Org surface area is busy but not benchmark-broken: **0** red benchmark rows, **55** green, **1** yellow (`matmul_blocked`). PR and CI debt dominate: **92** open PRs, **35** failing CI, **10** repos without live docs pages. CI audit shows **31** repos OK on `main`; **`lidb`** is **gated** (`default_branch: feat/ph-db-2-liorm-liq`, WP-H0) — counts toward “missing CI on main” in the scorecard metric. Failed PR sample includes stacked **lic** studio/ML/httpd waves — implementers will thrash until **pr_alignment** thins the stack.

### goal_directed_health (70.0 · weight 0.20)

Snapshot present (`lic/data/goal-directed-agents/snapshot.json`). **8** runners configured; **6** stopped (`compiler-studio`, `sim-algo`, `studio-ui-ux`, `sim-md-research`, `sim-chem-research`, `security-research`); **httpd** alone has `running: true` with **2** pending todos (`gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk`). **`agents_live: 0`** — no Cursor agent attached to any loop. **25** pending todos of **90** total. Research/proof work is landing in handoffs and snapshot files, not live loops — restart stopped runners or route through `code_implementer` on explicit branches.

### swarm_execution (55.0 · weight 0.25)

Sampled **120** local run JSON files; **22** terminal, **98** still `running`. Among terminal runs: **7** errors (**31.8%**), **3** incomplete (**13.6%**). Top error agents: **`bug_fixer` (3)**, **`code_implementer` (2)**, **`pr_merger` (1)**. Supabase `agent_runs` shows a broader **error** history (supervisor tick preemption at ~10:51Z); many rows have `briefing_hash: null`. Treat high DB error counts as **orchestration/reconcile**, not necessarily leaf logic failure — but unattended dispatch remains unsafe until `swarm_observer` clears stuck `running` rows and tightens tick boundaries.

### gap_pressure (70.0 · weight 0.15)

Gap report present; **53** open gaps per `swarm-gap-actions.json` (ingest/apply last at 10:55Z). **3** `missing_package` (`std.summary`, `std.plot`, line-profiler) patched to backlog — hand off to **`issue_planner`** / **`package_architect`**. **20** `plan_debt` rows mostly deferred without runner mapping. **30** `competitor_feature` stubs — research backlog only; do not block CI fixes. **`gap_explorer`** + **`swarm_observer`** apply pipeline should run before new explorer ingest.

---

## Deliverable / findings

### Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|------------------------|
| `swarm-error-rate` | critical | `li-cursor-agents/data/runs/` | `swarm_observer` |
| `failed-pr-ci` | high | `agent-briefing.json` → `ecosystem_audit.metrics.failed_prs` | `bug_fixer`, `pr_alignment` |
| `repos-missing-ci` | high | `ecosystem-audit` / `org-repo-ci-audit.json` (`lidb` gated) | `ci_maintainer` |
| `goal-runners-stopped` | high | `lic/data/goal-directed-agents/snapshot.json` | plan loops / `code_implementer` |
| `swarm-gap-backlog` | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| `preflight-failures` | medium | `agent-briefing.preflight_runs.org_agent_kit_audit` | `agent_kit_maintainer` |
| `preflight-skipped` | medium | `agent-briefing.preflight_runs` (--skip-slow) | orchestrator config |
| `swarm-many-running` | medium | `li-cursor-agents/data/runs/` | `swarm_observer` |
| `repos-missing-live-docs` | low | `ecosystem-audit.metrics.repos_without_live_pages` | `docs_maintainer` |

### Coordinator lane health

| Coordinator | Heap priority | Status | Notes |
|-------------|---------------|--------|-------|
| `coord_pull_requests` | 10 | **degraded** | 10 PRs flagged supersede/close; 35 red CI |
| `coord_governance` | 30 | **weak** | Plan audit skipped; 64 master-plan open items |
| `coord_ecosystem` | 40 | **active** | 2 missing std modules; gaps ingested |
| `coord_platform` | 50 | **degraded** | 28 agent-kit drifts; lidb CI gated |

### Recommended dispatch order

Merged **scorecard** (`ecosystem-quality-report.json` → `recommended_agents`) with **briefing P0** (`recommended_agents` + `heap_plan.flat_tasks`). Do not skip briefing P0.

| Step | Agent | Rationale |
|------|-------|-----------|
| 1 | `workspace_sweeper` | Briefing P0: dirty **lic** + **benchmarks** clones block isolated workflow |
| 2 | `swarm_observer` | Scorecard P0: `swarm_execution` 55 — reconcile stuck runs, tick errors |
| 3 | `pr_alignment` | Heap P10: 10 PRs need close/supersede before CI burn |
| 4 | `gap_explorer` | Scorecard + heap: registry + 2 missing std modules |
| 5 | `plan_verifier` | Governance: plan-completion audit (re-run with `plan_audit`) |
| 6 | `implementation_gaps` | Governance: cross-check PH trackers vs code |
| 7 | `agent_kit_maintainer` | Preflight exit 1 — 28 repos |
| 8 | `ci_maintainer` | lidb WP-H0 + org CI hygiene |
| 9 | `bug_fixer` → `code_implementer` | After meta lane — CI queue (lic#319, httpd#10, etc.) |
| 10 | `docs_maintainer` | 10 repos without live pages (low urgency) |

**Research lane (parallel, non-blocking):** `proof_gap_researcher` (provability_holes) — only after step 1–3 if API budget allows.

**Defer implementer waves** on stacked **lic** PRs (#367–#378) until `pr_alignment` publishes a single canonical branch per stack.

### Human-only blockers

| Blocker | Evidence | Action |
|---------|----------|--------|
| **lidb default branch** | `org-repo-ci-audit.json` — WP-H0 | Human: set `main` default before CI gate on default branch |
| **lic PR stacks** | `merge_plan` — 16 redundant pairs, human pick warnings | Human: choose one PR per stack (#377 vs #374, etc.) |
| **`merge-approved` / merge queue** | `gate_ready: 0`, `merge_approved: 9` but no auto-merge | Human label + review |
| **`trusted.lean` edits** | Swarm mandate | Human-approved issues only |
| **Dashboard report stale** | `control_plane_reports` latest **2026-05-25** | Human or `li-cursor-agents` deploy — not blocking local scorecard |

### Agent deliverable checklist (this run)

- [x] Regenerated `data/latest/ecosystem-quality-report.json`
- [x] Narrative + JSON sidecar under `data/runs/`
- [x] Cited scorecard fields (no manual re-score)
- [x] Dispatch order aligned with scorecard + briefing P0
- [ ] Control-plane prompt PR (`li-cursor-agents`) — delegate to `swarm_observer` if reconcile rules need code change
- [ ] Did not merge PRs or push to protected branches

### Handoff to meta-agents

| Signal | Delegate |
|--------|----------|
| 32% terminal error rate + 98 `running` | `swarm_observer` |
| 53 open gaps / plan_debt | `gap_explorer` + `swarm_observer` apply |
| 0 red benchmarks; yellow matmul | `bench_improver` (after CI green) |
| 6 stopped runners, httpd todos pending | `code_implementer` on `cursor/httpd-plan-continue` or restart loops |

---

## Recommended issues/PRs

| Repo | Item | Labels / notes |
|------|------|----------------|
| **lic** | [#386](https://github.com/li-langverse/lic/issues/386) PH-2i: reconcile length-1 broadcast tracker | `master-plan-gap`, `plan-needed` |
| **lic** | [#387](https://github.com/li-langverse/lic/issues/387) PH-7d MIR proc tags + Lean G-par | `master-plan-gap`, `plan-needed` |
| **lic** | [#385](https://github.com/li-langverse/lic/issues/385) PH-8p parallel workspace pool | `master-plan-gap`, `plan-needed` |
| **lic** | [PR #378](https://github.com/li-langverse/lic/pull/378) benchmarks repo tier-1/2 harness | CI fail — align with #367 stack after human pick |
| **li-httpd** | [PR #10](https://github.com/li-langverse/li-httpd/pull/10) plan-loop split | CI fail — `bug_fixer` after httpd soak todo |
| **li-demo** | [PR #15](https://github.com/li-langverse/li-demo/pull/15) agent-kit sync | CI fail — `agent_kit_maintainer` |
| **lidb** | (no PR) default branch WP-H0 | Human governance — `ci_maintainer` prepares PR after branch policy |

---

## Deferred

- **Full preflight** (`plan_audit`, `ci_bug_triage`, `pr_program`, `security_cwe_audit`) — run on next non–skip-slow briefing tick.
- **Bench tightening** — `matmul_blocked` yellow, five near-threshold rows; no tier-1 red.
- **Competitor_feature gap closure** — backlog/docs only; not P0 for CI.
- **CWE catalog Top25** (19 missing in catalog) — `security_auditor` after governance lane.
- **93 branches without PR** — `pr_branch_opener` deferred until alignment reduces open PR noise.
- **Control-plane dashboard sync** — Supabase report hash stale vs local briefing; ops follow-up.

---

## Evidence index

- `benchmarks/data/latest/ecosystem-quality-report.json`
- `benchmarks/data/latest/agent-briefing.json`
- `benchmarks/data/latest/swarm-gap-actions.json`
- `benchmarks/data/latest/org-repo-ci-audit.json`
- `lic/data/goal-directed-agents/snapshot.json`
- `li-cursor-agents/data/runs/` (terminal + stuck running sample)
- Supabase `agent_runs`, `control_plane_reports` (read-only MCP)
