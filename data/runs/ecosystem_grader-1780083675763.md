# Ecosystem grader — proactive sweep

**Run id:** `ecosystem_grader-1780083675763`  
**Generated:** 2026-05-29T19:41Z  
**Source:** proactive  
**north_star_fit:** ecosystem orchestration — proof → easy → fast (PH-2i, PH-5b, PH-7e); meta lane before implementers  
**Briefing:** `data/latest/agent-briefing.json` @ 2026-05-29T19:05Z  
**Scorecard:** `data/latest/ecosystem-quality-report.json` @ 2026-05-29T19:41:42Z

---

## Executive summary

- **Grade D · overall 67.6 / 100** — `unattended_safe: false` ([scorecard](../latest/ecosystem-quality-report.json)).
- **Swarm execution is the binding constraint** (55.0): **27%** error rate on 26 terminal runs; **94** runs still `running` (stuck-reconcile risk); finding `swarm-error-rate` escalated to **critical**.
- **Gap pressure regressed** (70.0): **53** open registry gaps (3 `missing_package`, 20 `plan_debt`, 30 `competitor_feature`) after orch-r3 ingest — up from 27 prior pass.
- **Goal-directed loops starved** (70.0): **6/8** runners stopped or idle, `agents_live: 0`, **24/90** plan todos pending; only **httpd** + **swarm-observer** shells show `running: true`.
- **Ecosystem posture mixed** (67.0): **0** open PRs / **0** failed CI on main audit, but **6 red** tier-1 benchmark rows (ingest @ 07:01Z).
- **Briefing health good** (84.0): **2** preflight fails (`org_agent_kit_audit`, `security_cwe_audit`); `agent_deliverable_gate` skipped (`LI_CURSOR_AGENTS_ENABLED` unset).
- **Dispatch meta before implementers** — scorecard orders `swarm_observer` + `gap_explorer` first; briefing P0 still needs `workspace_sweeper` + governance (`plan_verifier`, `implementation_gaps`).
- **Numerics lane active** — `bench_improver` / `code_implementer` runs on `lic` branches; dashboard reds persist until re-ingest after merges.

---

## Dimension drill-down

### briefing_health (84.0 · weight 0.15)

Preflight produced a usable briefing (`briefing_present: true`, **12** recommended agents). Two scripts exited non-zero: **`org_agent_kit_audit`** (9 repos missing kit, 3 drift — canonical `1.3.5+6018e18bf2ed91f4`) and **`security_cwe_audit`** (`JSONDecodeError: Expecting value` on empty input — CWE feed sync succeeded separately with **19** Top-25 CWEs missing from catalog). **`agent_deliverable_gate`** was skipped because `li-cursor-agents` scan is disabled locally. Plan audit, ecosystem audit, and merge-plan scripts all passed — governance agents can run, but security catalog completeness should be fixed before unattended `security_auditor` waves.

### ecosystem_posture (67.0 · weight 0.25)

PR surface is quiet (**0** open, **0** failed per briefing) and org CI audit reports **0** repos missing CI on `main`. Benchmark posture shows **6 red** tier-1 rows (`matmul_blocked`, `matmul_naive`, `ml_conv2d_forward`, `ml_mlp_forward`, `ml_mlp_train_step`, `num_gmres`) at ratios 1.33–1.55× vs C++. Active `bench_improver` branches may already green some rows locally — ingest at 07:01Z is stale. **8** repos lack live docs pages; **129** branches pushed without open PRs (`pr_branch_hygiene`). **11** CI/bug queue items remain in triage JSON.

### goal_directed_health (70.0 · weight 0.20)

Snapshot present (`lic/data/goal-directed-agents/snapshot.json`). **8** runners; **6** not actively progressing (`compiler-studio`, `sim`, `studio-ui-ux`, `sim-md-research`, `sim-chem-research`, `security-research` — all `supervisor off`, logs 12–96h stale). **httpd** has `running: true` but supervisor idle (log ~1458s stale) with **2** pending todos (`gap-phase2-perf-wrk-soak`, `gap-phase2-streaming-wrk`). **swarm-observer** shell process is snapshot refresh only — **1** orchestration todo pending (`orch-r4-ui-ux-signals`). **`agents_live: 0`**. Pending todos: **25/90**. Proof and sim work is frozen in snapshot handoffs (`sim-p1-num-dot-axpy`, `wave-d-gui-scaffold`, research loops) — restart supervisors or route explicit branches via `code_implementer`.

### swarm_execution (55.0 · weight 0.25)

Sampled **120** local run JSON files; **26** terminal, **94** still `running`. Among terminal runs: **7** errors (**27%**), **1** incomplete (**3.8%**). Top error agents in sample: **`bug_fixer` (1)**, **`code_implementer` (1)**, **`bench_improver` (1)**. Recent failures (19:33–19:40Z batch) include a **10-agent simultaneous error burst** (`plan_verifier`, `implementation_gaps`, `workspace_sweeper`, etc.) — likely SDK supersede/session collision, not product logic. `code_implementer-1780083322950` ran 35 tool calls then SDK error after push rejection on stale branch ref. Supabase `agent_runs`: historical error mass dominated by orchestration debt (`pr_reviewer` 175, `implementation_gaps` 172). Unattended dispatch remains unsafe until `swarm_observer` reconciles stuck `running` rows and hardens tick/session boundaries.

### gap_pressure (70.0 · weight 0.15)

Gap report present; **53** open gaps per `swarm-gap-actions.json` (ingest **2026-05-29T19:35:50Z**). **3** `missing_package` (`std.summary`, `std.plot`, line-profiler seed) — `std.io` / `std.csv` closed in registry but briefing still cites "2 missing std modules". **20** `plan_debt` rows mostly deferred without runner mapping (master-plan partial phases 2i, 7d, 7e, 8p). **30** `competitor_feature` rows from verticals.toml / explorer ingest. Score dropped from 92.0 because absolute gap count nearly doubled after orch-r2/r3 competitor ingest — **`gap_explorer`** must reconcile registry vs filesystem and close stale rows before new package PRs.

---

## Deliverable / findings

### Top findings

| id | severity | evidence path | suggested owner agent |
|----|----------|---------------|------------------------|
| `swarm-error-rate` | critical | `li-cursor-agents/data/runs/` | `swarm_observer` |
| `swarm-gap-backlog` | high | `data/latest/swarm-gap-actions.json` | `gap_explorer`, `swarm_observer` |
| `preflight-failures` | high | `agent-briefing.json` → `preflight_runs` | `agent_kit_maintainer`, `ci_maintainer` |
| `benchmark-red-rows` | high | `ecosystem-audit.json` → `benchmarks.red` | `bench_improver`, `numerics_researcher` |
| `goal-runners-stopped` | high | `lic/data/goal-directed-agents/snapshot.json` | plan loops / `plan_verifier` |
| `swarm-many-running` | medium | `li-cursor-agents/data/runs/` | `swarm_observer` |
| `repos-missing-live-docs` | low | `ecosystem-audit.metrics.repos_without_live_pages` | `docs_maintainer` |

### Coordinator lane health

| Coordinator | Heap priority | Status | Notes |
|-------------|---------------|--------|-------|
| `coord_numerics` | 20 | **active** | 6 red rows; `bench_improver` branch on `lic`; ingest stale |
| `coord_governance` | 30 | **weak** | 64 master-plan open items; plan audit passed but 40 open checkboxes |
| `coord_ecosystem` | 40 | **degraded** | 53 registry gaps; briefing/explorer mismatch on std modules |
| `coord_platform` | 50 | **degraded** | 9 agent-kit drifts; security CWE audit broken |

### Recommended dispatch order

Merged **scorecard** (`recommended_agents`) with **briefing P0** (`recommended_agents` + `heap_plan.flat_tasks`). Scorecard meta agents lead; briefing P0 follows without contradiction.

| Step | Agent | Rationale |
|------|-------|-----------|
| 1 | `swarm_observer` | Scorecard P0: `swarm_execution` 55 — reconcile 94 `running`, 27% terminal errors, 19:33Z batch |
| 2 | `gap_explorer` | Scorecard P0: `gap_pressure` 70 — reconcile 53-gap registry vs explorer/briefing |
| 3 | `workspace_sweeper` | Briefing P0: dirty **lic** + **benchmarks** (7 + 2 changed files) |
| 4 | `plan_verifier` | Briefing P0 + heap: 64 plan-completion findings |
| 5 | `implementation_gaps` | Briefing P0: cross-check PH trackers vs implementation |
| 6 | `ci_maintainer` | Scorecard + preflight: fix `security_cwe_audit` empty JSON input |
| 7 | `agent_kit_maintainer` | Preflight exit 1 — 9 repos missing/drifted kit |
| 8 | `numerics_researcher` → `bench_improver` | Heap P20: red rows; re-ingest after lic merges |
| 9 | `bug_fixer` → `code_implementer` | CI queue (11 items) — **after** steps 1–5 |
| 10 | `docs_maintainer` | 8 repos without live pages |
| 11 | `pr_branch_opener` | 129 branches without PR — low urgency while open_prs=0 |
| 12 | `security_auditor` | Top-25 catalog gaps=19 — after CWE audit script fix |

**Defer stacked implementer waves** until `swarm_observer` clears the 19:33Z error batch and workspace sweep isolates clones.

### Human-only blockers

| Blocker | Evidence | Action |
|---------|----------|--------|
| **`security_cwe_audit` JSON parse** | `preflight_runs.security_cwe_audit` stderr | Human/fix script: empty JSON input to decoder |
| **`LI_CURSOR_AGENTS_ENABLED=0`** | `agent_deliverable_gate` skipped | Enable for deliverable gate scans in CI/automation |
| **Goal-directed supervisor restart** | 6 runners `supervisor off`, 4-day stale logs | Human: restart plan loops or accept manual branch work |
| **Benchmark ingest freshness** | Audit @ 07:01Z vs local greens | Human/CI: `LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh` after lic merges |
| **`trusted.lean` edits** | Swarm mandate | Human-approved issues only |
| **129 orphan branches** | `pr_branch_hygiene` | Human triage before mass `pr_branch_opener` |
| **Push rejection on agent branches** | `code_implementer-1780083322950` post-hook | Human: reconcile concurrent `bench_improver` branch pushes |

### Agent deliverable checklist (this run)

- [x] Cited fresh scorecard fields (no manual re-score)
- [x] Narrative under `data/runs/ecosystem_grader-1780083675763.md`
- [x] Dispatch order aligned with scorecard + briefing P0
- [x] Control-plane SQL sampled (`agent_runs` status histogram, recent errors)
- [x] Goal-directed snapshot cited: `lic/data/goal-directed-agents/snapshot.json`
- [ ] Control-plane prompt PR (`li-cursor-agents`) — delegate to `swarm_observer` if reconcile rules need code change
- [ ] Did not merge PRs or push to protected branches

### Handoff to meta-agents

| Signal | Delegate |
|--------|----------|
| 27% terminal error rate + 94 `running` | `swarm_observer` |
| 53 open gaps / competitor_feature ingest | `gap_explorer` + `swarm_observer` apply |
| 6 red benchmarks (ingest-lagged) | `bench_improver`, `numerics_researcher` via `coord_numerics` |
| 6 stopped goal runners / plan_pending | Relevant plan loop or `plan_verifier` |

---

## Recommended issues/PRs

| Title | Repo | Labels / agent |
|-------|------|----------------|
| fix(preflight): `security_cwe_audit` empty JSON input | **benchmarks** | `ci`, `security` → `ci_maintainer` |
| Re-ingest tier-1 after lic matmul merge | **benchmarks** | `numerics`, PH-7e — clears stale dashboard reds |
| perf(7e): matmul_blocked LLVM emit tuning | **lic** | `bench_improver`, PH-7e — largest remaining pure-Li red |
| Sync agent-kit to canonical 1.3.5 | **li-demo**, **li-httpd**, **li-std-*** | `agent_kit_maintainer` |
| Restart goal-directed `sim` / `compiler-studio` supervisors | **lic** | human ops — unblocks `sim-p1-num-dot-axpy`, `wave-d-gui-scaffold` |
| Reconcile registry closed gaps vs briefing explorer | **lic** / **benchmarks** | `gap_explorer` |
| Swarm stuck-run reconcile + SDK session timeout | **li-cursor-agents** | `swarm_observer` — PR + `npm test` |
| Close orch-r4 ui-ux gap signals | **lic** | `swarm_observer` — pending todo on active runner |

---

## Deferred

- **`pr_branch_opener` mass run** — 129 branches; wait until PR program has review bandwidth (open_prs=0 today).
- **`docs_maintainer` for 8 repos** — P2 while numerics + swarm meta blocked.
- **30 `competitor_feature` gaps** — informational until plan_debt runners mapped; no implementer wave yet.
- **Tier-2 yellow MD thermostats** — extern wrappers sufficient until tier-1 green + ingest.
- **Whitepaper / research-findings publish** — no ecosystem-grade win this pass.
- **Lean `trusted.lean` for fused matmul** — human-approved track only.

<!-- li-agent -->
## Agent deliverable
- [x] Scorecard cited: `data/latest/ecosystem-quality-report.json` (grade D, 67.6)
- [x] Run narrative: `data/runs/ecosystem_grader-1780083675763.md`
- [x] Control-plane SQL sampled (`agent_runs` status histogram)
- [x] Goal-directed snapshot cited: `lic/data/goal-directed-agents/snapshot.json`
- [ ] `li-cursor-agents` prompt PR — delegated to `swarm_observer` if reconcile code change needed
