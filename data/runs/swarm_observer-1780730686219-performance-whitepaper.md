# Swarm gap orchestration — performance dimension audit

**Goal id:** `swarm_coverage`  
**Agent:** `swarm_observer`  
**Run id:** `swarm_observer-1780730686219`  
**Generated:** 2026-06-06T08:04Z  
**Domains:** ecosystem, ai  
**north_star_fit:** Proof-before-perf orchestration — route bench gaps through PH-5b/7e discipline  
**Validity grade:** B (audit-only; ingest blocked)

---

## Abstract

This pass audits the Li agent swarm's **performance gap orchestration** under research goal `swarm_coverage`. The ecosystem shows **zero tier-1 red benchmark rows** in the latest audit snapshot but **five near-threshold** entries and **thirty open competitor-feature registry gaps** including eight tier-1 red-class historical rows. Gap ingest is **blocked** by a SyntaxError in `swarm-gap-ingest.py`, leaving the apply pipeline stale since 2026-05-31. Control-plane health artifacts are absent in the current container, limiting programmatic observer visibility.

---

## Method

1. Regenerated `ecosystem-quality-report.json` via `python3 scripts/ecosystem-quality-grade.py`.
2. Read `agent-briefing.json`, `ecosystem-audit.json`, `swarm-gap-actions.json`, `registry.yaml`.
3. Attempted gap ingest/apply (ingest failed).
4. Compared briefing `recommended_agents` vs scorecard recommendations.
5. Mapped performance-related registry rows to swarm goals and handoff targets per `research-verticals.md`.

---

## Results

### Ecosystem quality (2026-06-06)

| Metric | Value |
|--------|-------|
| Overall score | 64.8 |
| Grade | D |
| unattended_safe | false |
| benchmark_red_count | 0 |
| near_threshold_count | 5 |
| unknown_benchmark_count | 95+ |
| open_gaps | 64 |

### Near-threshold benchmarks

| id | ratio_vs_cpp |
|----|--------------|
| simd_dot | 1.1279 |
| md_init_fcc_mb | 1.0199 |
| md_longrange_ewald | 1.0139 |
| md_integrator_verlet | 1.0129 |
| md_neighbor_cell_list | 1.0121 |

`simd_dot` is the highest-leverage near-threshold item — already linked to backlog todo `sim-p1-num-dot-axpy`.

### Registry performance pressure

- **competitor_feature:** 30 open (includes tier-1 red-class, HPC stacks, vertical stubs)
- **plan_debt:** 31 open (includes PH-7e SIMD partial, sim perf todos)
- **missing_package:** 3 open (profiler + std modules — indirect perf tooling)

### Orchestration blockers

1. **Gap ingest SyntaxError** — prevents registry refresh and auto-close of completed plan todos.
2. **36 failing PR CI** — includes benchmarks metrics refresh wave (#353–#373) and li-parallel harness (#370).
3. **Control-plane report missing** — `runs_sampled: 0`; observer auto-heal not auditable.

---

## Recommendations

1. **Fix ingest script** — unblocks entire gap apply pipeline (highest ROI orchestration fix).
2. **Dispatch bench_improver + numerics_researcher** — simd_dot and MD cluster with PH-7e proof gates.
3. **Unblock benchmarks#370** — enables Class A parallel harness evidence for HPC gaps.
4. **Align briefing heap with scorecard** — dispatch `gap_explorer`, `ecosystem_grader`, `plan_verifier` when grade D.
5. **Do not** bypass provability for perf — pillar order proof → easy → fast is non-negotiable.

---

## Artifacts

| Path | Role |
|------|------|
| `/app/data/runs/swarm_observer-1780730686219.md` | Swarm observer digest |
| `/workspace/lic/docs/ecosystem/orchestrator-notes/2026-06-06-orch-r5-performance-gap-orchestration.md` | Orchestrator note |
| `/workspace/benchmarks/data/latest/ecosystem-quality-report.json` | Scorecard |
| `/workspace/benchmarks/data/latest/ecosystem-audit.json` | Benchmark posture |

**Publish target (deferred):** `research-findings/whitepapers/2026-06/swarm_coverage/`
