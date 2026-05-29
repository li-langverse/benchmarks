# Ecosystem grader — proactive sweep

**Run id:** `ecosystem_grader-1780082990753`  
**Generated:** 2026-05-29T19:30Z  
**Source:** proactive  
**north_star_fit:** ecosystem orchestration — proof → easy → fast (PH-2i, PH-5b, PH-7e); meta lane before implementers  
**Briefing:** `data/latest/agent-briefing.json` @ 2026-05-29T19:05Z  
**Scorecard:** `data/latest/ecosystem-quality-report.json` @ 2026-05-29T19:29:34Z (regenerated this pass)

---

## Executive summary

- **Grade C · overall 70.9 / 100** — `unattended_safe: false` ([scorecard](../latest/ecosystem-quality-report.json)).
- **Swarm execution is the binding constraint** (55.0): **28% error rate** on 25 terminal SDK runs; **95** runs still `running` (stuck-reconcile risk).
- **Ecosystem posture mixed** (67.0): **0** open PRs / **0** failed CI on main audit, but **6 red** tier-1 benchmark rows and stale ingest (07:01Z vs local harness).
- **Goal-directed loops starved** (70.0): **6/8** runners stopped or idle, `agents_live: 0`, **25/90** plan todos pending; only **httpd** + **swarm-observer** shells show `running: true`.
- **Gap pressure manageable** (92.0): **27** open registry gaps (5 `missing_package`, 22 `plan_debt`); apply pipeline last ran 2026-05-25.
- **Briefing health good** (84.0): briefing present; **2** preflight fails (`org_agent_kit_audit`, `security_cwe_audit`); `agent_deliverable_gate` skipped (`LI_CURSOR_AGENTS_ENABLED` unset).
- **Dispatch meta before implementers** — scorecard orders `swarm_observer` first; briefing P0 still needs `workspace_sweeper` + governance (`plan_verifier`, `implementation_gaps`).
- **Numerics lane active but ingest-lagged** — autoresearch + `bench_improver` branches show local greens; dashboard still lists 6 reds until re-ingest.

---

## Dimension drill-down

### briefing_health (84.0 · weight 0.15)

Preflight produced a usable briefing (`briefing_present: true`, **12** recommended agents). Two scripts exited non-zero: **`org_agent_kit_audit`** (9 repos missing kit, 3 drift — canonical `1.3.5+6018e18bf2ed91f4`) and **`security_cwe_audit`** (`JSONDecodeError` on empty input — CWE feed sync succeeded separately with **19** Top-25 CWEs missing from catalog). **`agent_deliverable_gate`** was skipped because `li-cursor-agents` scan is disabled locally. Plan audit, ecosystem audit, and merge-plan scripts all passed — governance agents can run, but security catalog completeness should be fixed before unattended `security_auditor` waves.

### ecosystem_posture (67.0 · weight 0.25)

PR surface is quiet (**0** open, **0** failed per briefing) and org CI audit reports **0** repos missing CI on `main`. Benchmark posture regressed on paper: **6 red** tier-1 rows (`matmul_blocked`, `matmul_naive`, `ml_conv2d_forward`, `ml_mlp_forward`, `ml_mlp_train_step`, `num_gmres`) at ratios 1.33–1.55× vs C++. Local harness + autoresearch digest show **matmul_naive** and **num_gmres** already green on active branches — ingest at 07:01Z is stale. **8** repos lack live docs pages; **129** branches pushed without open PRs (`pr_branch_hygiene`). **11** CI/bug queue items remain in triage JSON.

### goal_directed_health (70.0 · weight 0.20)

Snapshot present (`lic/data/goal-directed-agents/snapshot.json`). **8** runners; **6** not actively progressing (`compiler-studio`, `sim`, `studio-ui-ux`, `sim-md-research`, `sim-chem-research`, `security-research` — all `supervisor off`, logs 12–96h stale). **httpd** has `running: true` but supervisor idle (log 779s stale) with **2** pending todos (wrk soak, streaming wrk). **swarm-observer** shell process is snapshot refresh only — **2** orchestration todos pending (`orch-r3-missing-package-sweep`, `orch-r4-ui-ux-signals`). **`agents_live: 0`**. Pending todos: **25/90**. Proof and sim work is frozen in snapshot handoffs (`sim-p1-num-dot-axpy`, `wave-d-gui-scaffold`, research loops) — restart supervisors or route explicit branches via `code_implementer`.

### swarm_execution (55.0 · weight 0.25)

Sampled **120** local run JSON files; **25** terminal, **95** still `running`. Among terminal runs: **7** errors (**28%**), **3** incomplete (**12%**). Top error agents in sample: **`pr_alignment` (1)**, **`ci_maintainer` (1)**, **`pr_merger` (1)**. Recent failures (19:18–19:29Z batch) are predominantly **SDK premature termination** (`SDK run status: error`, 1 tool call, no deliverable section) — not product logic failures. Supabase `agent_runs`: **3032** historical `error`, **17** `running`, **135** `finished` — treat DB error mass as orchestration/reconcile debt. Unattended dispatch remains unsafe until `swarm_observer` reconciles stuck `running` rows and hardens tick/session boundaries.

### gap_pressure (92.0 · weight 0.15)

Gap report present; **27** open gaps per `swarm-gap-actions.json` (ingest last **2026-05-25**). **5** `missing_package` (`std.io`, `std.csv`, `std.summary`, `std.plot`, line-profiler) — explorer notes **std.io** / **std.csv** may already exist on disk; reconcile registry vs filesystem before new package PRs. **22** `plan_debt` rows mostly deferred without runner mapping (master-plan partial phases 2i, 7d, 7e, 8p). Score is high because absolute gap count is modest; **`gap_explorer`** should still refresh ingest and close stale `missing_package` rows.

---

## Deliverable / findings

### Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|------------------------|
| `swarm-error-rate` | critical | `li-cursor-agents/data/runs/` | `swarm_observer` |
| `preflight-failures` | high | `agent-briefing.json` → `preflight_runs` | `agent_kit_maintainer`, `security_auditor` |
| `benchmark-red-rows` | high | `ecosystem-audit.json` → `benchmarks.red` | `bench_improver`, `numerics_researcher` |
| `goal-runners-stopped` | high | `lic/data/goal-directed-agents/snapshot.json` | plan loops / `plan_verifier` |
| `swarm-many-running` | medium | `li-cursor-agents/data/runs/` | `swarm_observer` |
| `repos-missing-live-docs` | low | `ecosystem-audit.metrics.repos_without_live_pages` | `docs_maintainer` |
| `swarm-gap-backlog` | low | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |

### Coordinator lane health

| Coordinator | Heap priority | Status | Notes |
|-------------|---------------|--------|-------|
| `coord_numerics` | 20 | **active** | 6 red rows; `bench_improver` branch on `lic`; ingest stale |
| `coord_governance` | 30 | **weak** | 64 master-plan open items; plan audit passed but 40 open checkboxes |
| `coord_ecosystem` | 40 | **moderate** | 2 missing std modules in briefing; 27 registry gaps |
| `coord_platform` | 50 | **degraded** | 9 agent-kit drifts; security CWE audit broken |

### Recommended dispatch order

Merged **scorecard** (`recommended_agents`) with **briefing P0** (`recommended_agents` + `heap_plan.flat_tasks`). Briefing P0 agents appear after scorecard meta unless noted.

| Step | Agent | Rationale |
|------|-------|-----------|
| 1 | `swarm_observer` | Scorecard P0: `swarm_execution` 55 — reconcile 95 `running`, 28% terminal errors |
| 2 | `workspace_sweeper` | Briefing P0: dirty **lic** + **benchmarks** (7 + 2 changed files) |
| 3 | `plan_verifier` | Briefing P0 + heap: 64 plan-completion findings |
| 4 | `implementation_gaps` | Briefing P0: cross-check PH trackers vs implementation |
| 5 | `ci_maintainer` | Scorecard: ecosystem_posture weak signal; fix `security_cwe_audit` input |
| 6 | `gap_explorer` | Briefing: 2 missing std modules; refresh 27-gap registry |
| 7 | `agent_kit_maintainer` | Preflight exit 1 — 9 repos missing/drifted kit |
| 8 | `numerics_researcher` → `bench_improver` | Heap P20: red rows; merge lic #418 + re-ingest before claiming green |
| 9 | `bug_fixer` → `code_implementer` | CI queue (11 items) — **after** steps 1–3 |
| 10 | `docs_maintainer` | 8 repos without live pages |
| 11 | `pr_branch_opener` | 129 branches without PR — low urgency while open_prs=0 |
| 12 | `security_auditor` | Top-25 catalog gaps=19 — after CWE audit script fix |

**Defer stacked implementer waves** until `swarm_observer` clears the 19:18Z error batch and workspace sweep isolates clones.

### Human-only blockers

| Blocker | Evidence | Action |
|---------|----------|--------|
| **`security_cwe_audit` JSON parse** | `preflight_runs.security_cwe_audit` stderr | Human/fix script: empty JSON input to decoder |
| **`LI_CURSOR_AGENTS_ENABLED=0`** | `agent_deliverable_gate` skipped | Enable for deliverable gate scans in CI/automation |
| **Goal-directed supervisor restart** | 6 runners `supervisor off`, 4-day stale logs | Human: restart plan loops or accept manual branch work |
| **Benchmark ingest freshness** | Audit @ 07:01Z vs local greens | Human/CI: `LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh` after lic merges |
| **`trusted.lean` edits** | Swarm mandate | Human-approved issues only |
| **129 orphan branches** | `pr_branch_hygiene` | Human triage before mass `pr_branch_opener` |

### Agent deliverable checklist (this run)

- [x] Regenerated `data/latest/ecosystem-quality-report.json`
- [x] Narrative under `data/runs/ecosystem_grader-1780082990753.md`
- [x] Cited scorecard fields (no manual re-score)
- [x] Dispatch order aligned with scorecard + briefing P0
- [ ] Control-plane prompt PR (`li-cursor-agents`) — delegate to `swarm_observer` if reconcile rules need code change
- [ ] Did not merge PRs or push to protected branches

### Handoff to meta-agents

| Signal | Delegate |
|--------|----------|
| 28% terminal error rate + 95 `running` | `swarm_observer` |
| 27 open gaps / plan_debt | `gap_explorer` + `swarm_observer` apply |
| 6 red benchmarks (ingest-lagged) | `bench_improver`, `numerics_researcher` via `coord_numerics` |
| 6 stopped goal runners / plan_pending | Relevant plan loop or `plan_verifier` |

---

## Recommended issues/PRs

| Title | Repo | Labels / agent |
|-------|------|----------------|
| fix(preflight): `security_cwe_audit` empty JSON input | **benchmarks** | `ci`, `security` → `ci_maintainer` |
| Re-ingest tier-1 after lic matmul merge | **benchmarks** | `numerics`, PH-7e — clears stale dashboard reds |
| perf(7e): matmul_naive via `C = A @ B` | **lic** | [#418](https://github.com/li-langverse/lic/pull/418) — `bench_improver` |
| perf(7e): matmul_blocked LLVM emit tuning | **lic** | `bench_improver`, PH-7e — largest remaining pure-Li red |
| Sync agent-kit to canonical 1.3.5 | **li-demo**, **li-httpd**, **li-std-*** | `agent_kit_maintainer` |
| Restart goal-directed `sim` / `compiler-studio` supervisors | **lic** | human ops — unblocks `sim-p1-num-dot-axpy`, `wave-d-gui-scaffold` |
| Reconcile registry `std.io` / `std.csv` closed vs explorer | **lic** | `gap_explorer` |
| Swarm stuck-run reconcile + SDK session timeout | **li-cursor-agents** | `swarm_observer` — PR + `npm test` |

---

## Deferred

- **`pr_branch_opener` mass run** — 129 branches; wait until PR program has review bandwidth (open_prs=0 today).
- **`docs_maintainer` for 8 repos** — P2 while numerics + swarm meta blocked.
- **Novel-algorithm research** — autoresearch negative on all 6 reds; route to SOTA codegen only.
- **Tier-2 yellow MD thermostats** — extern wrappers sufficient until tier-1 green + ingest.
- **Whitepaper / research-findings publish** — no ecosystem-grade win this pass.
- **Lean `trusted.lean` for fused matmul** — human-approved track only.

<!-- li-agent -->
## Agent deliverable
- [x] Scorecard regenerated: `data/latest/ecosystem-quality-report.json` (grade C, 70.9)
- [x] Run narrative: `data/runs/ecosystem_grader-1780082990753.md`
- [x] Control-plane SQL sampled (`agent_runs` status histogram)
- [x] Goal-directed snapshot cited: `lic/data/goal-directed-agents/snapshot.json`
- [ ] `li-cursor-agents` prompt PR — delegated to `swarm_observer` if reconcile code change needed
