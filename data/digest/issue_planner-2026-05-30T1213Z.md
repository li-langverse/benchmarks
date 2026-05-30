# Issue feature planner digest — 2026-05-30T12:13Z

**Agent:** issue_planner · **Repo scope:** benchmarks (org-wide triage)  
**north_star_fit:** HPC/scientific · PH-2i, PH-5b, PH-7d, PH-7e, PH-8p, Vision-LLM · proof → easy → fast

---

## Executive summary

- Org sweep: **6 repos** scanned, **42** `plan-needed`, **3** lic `feature` candidates (studio-ui).
- **benchmarks:** all **11** open `plan-needed` issues already have `li-agent-plan-v2` plan comments + draft PRs (#135, #136, #137, #183, #198) — no duplicate plans filed this run.
- **lic:** **3 new plans** drafted for highest-priority unplanned master-plan gaps (#425 Vision-LLM, #385 PH-8p, #387 PH-7d/G-par).
- **proof_gap_researcher handoff:** #387 sub-phase C catalogs **G-par** Lean obligations before `trusted.lean` edits; complements planned #472 and #526.
- **Deferred:** #462 (length-1 broadcast tests) subsumed by #526 plan PR #532; #463 (tier-1 red rows) → `bench_improver`/`numerics_researcher`; #19 benchmarks tier-2 gaming stale.
- **Human-only:** **`plan-approved`** required on all draft plan PRs before implementation agents run; do not self-merge roadmap/governance PRs.
- **No code implementation** this run (no issue had `plan-approved` + linked plan for codegen).

---

## Deliverable / findings

### Issues scanned

| Repo | needs_plan | candidates | planned this run |
|------|------------|------------|------------------|
| **lic** | 30 | 3 | 3 (#425, #385, #387) |
| **benchmarks** | 11 | 0 | 0 (all pre-planned) |
| **lip** | 0 | 0 | — |
| **lit** | 0 | 0 | — |
| **lis** | — (gh empty) | 0 | — |
| **roadmap** | — (gh empty) | 0 | — |

Triage artifact: `data/latest/issue-feature-triage.json` (`generated_at`: 2026-05-30T12:13Z).

### Plans drafted (this run)

| Issue | Repo | Plan path | Draft PR |
|-------|------|-----------|----------|
| [#425](https://github.com/li-langverse/lic/issues/425) Vision-LLM Done gates | lic | `docs/superpowers/plans/2026-05-30-vision-llm-done-gates.md` | [lic#538](https://github.com/li-langverse/lic/pull/538) |
| [#385](https://github.com/li-langverse/lic/issues/385) PH-8p-b/d exit gates | lic | `docs/superpowers/plans/2026-05-30-ph-8p-exit-gates.md` | [lic#539](https://github.com/li-langverse/lic/pull/539) |
| [#387](https://github.com/li-langverse/lic/issues/387) PH-7d / G-par MIR tags | lic | `docs/superpowers/plans/2026-05-30-ph-7d-mir-proc-tags-g-par.md` | [lic#540](https://github.com/li-langverse/lic/pull/540) |

### Benchmarks backlog (pre-existing plans — verified)

| Issue | Draft PR | PH / theme |
|-------|----------|------------|
| #179 catalog path reconciliation (117 gaps) | [benchmarks#183](https://github.com/li-langverse/benchmarks/pull/183) | PH-5b, PH-7e |
| #18 tier-1 FFT micro-bench | [benchmarks#136](https://github.com/li-langverse/benchmarks/pull/136) | PH-5b |
| #51/#52 FFT vendor rubrics | [benchmarks#198](https://github.com/li-langverse/benchmarks/pull/198) | PH-5b, G-math |
| #20/#25/#28/#29/#54 LIC_ROOT honesty | [benchmarks#135](https://github.com/li-langverse/benchmarks/pull/135) | PH-IO |
| #53 PH-IO-7 summary parity | [benchmarks#137](https://github.com/li-langverse/benchmarks/pull/137) | PH-IO-7 |

### Issues blocked / deferred

| Issue | Reason |
|-------|--------|
| **benchmarks#19** | Stale — tier-2 dirs exist on lic@dev; close or relabel duplicate |
| **lic#462** | Subsumed by **#526** plan (length-1 broadcast + NumPy defer) — PR #532 |
| **lic#463**, **#424** | Implementation/perf honesty — queue `bench_improver`, not new plan |
| **lic#399/#398/#394** | Studio-ui CI/features — lower priority vs master-plan gaps; defer |
| **lic sim runners** (#521–#523, #478, #477) | Goal-directed supervisor idle — human runner config |
| **roadmap/lis** | No open `plan-needed` issues fetched |

### proof_gap_researcher handoff (provability_holes)

- **Primary:** [lic#387](https://github.com/li-langverse/lic/issues/387) plan sub-phase **C** — **G-par** Lean discharge for structured `disjoint=` + proc-tag lowering.
- **Related planned:** #472 (P-linalg loop ≡ ensures), #526 (broadcast reject gate), #527 (for/range parse+typecheck).
- **Ecosystem context:** 13 partial + 4 missing **G-*** rows per briefing; 6 tier-1 **red** bench rows (PH-5b/7e) — perf work separate from proof plan.

---

## Recommended issues/PRs

**Await maintainer `plan-approved` (plan review merge queue):**

- lic [PR #538](https://github.com/li-langverse/lic/pull/538) — Vision-LLM Done gates (#425)
- lic [PR #539](https://github.com/li-langverse/lic/pull/539) — PH-8p exit gates (#385)
- lic [PR #540](https://github.com/li-langverse/lic/pull/540) — PH-7d / G-par (#387)
- benchmarks [PR #183](https://github.com/li-langverse/benchmarks/pull/183) — catalog path reconciliation (#179)
- benchmarks [PR #136](https://github.com/li-langverse/benchmarks/pull/136) — tier-1 FFT (#18)

**Implementation queue (after plan-approved):**

- `proof_gap_researcher` → lic#387 G-par corpus
- `bench_improver` / `numerics_researcher` → tier-1 red rows (matmul, ml_*, num_gmres)
- `code_implementer` → lic#13 std.summary/plot (PH-IO)

---

## Deferred

- Weakening `threshold_ratio_cpp` to green benchmarks — rejected per vision filter.
- New org repos — requires [governance checklist](https://github.com/li-langverse/roadmap/blob/main/docs/ecosystem/governance.md).
- Self-merge of roadmap/governance plan PRs — blocked.
- GitHub Actions `schedule:` cron — not added.
