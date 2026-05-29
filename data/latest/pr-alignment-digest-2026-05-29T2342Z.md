# PR alignment digest — 2026-05-29T23:42Z

**Agent:** `pr_alignment` · **Queued:** `heap:coord_pull_requests:pr_alignment:7606059aaf933d62440a` · **North star:** proof → easy → fast · **PH context:** Phase 2i (partial), PH-5b/7e tier-1 reds, PH-DB stack · **Preflight:** `pr-branch-hygiene.json` @ 23:30Z, `pr-merge-queue-plan.json` @ 23:06Z (stale gate scan), `issue-feature-triage.json` @ 23:35Z

## Executive summary

- Reviewed **8** PRs (cap): hygiene close queue + newly opened high-signal PRs; **0** merges, **0** auto-closes (`prs_safe_close_now: 0`).
- **10** draft PRs in `prs_recommended_close` are **intentional plan/agent drafts** — keep open pending maintainer ack, not abandoned junk.
- **Merge queue empty** for non-draft PRs (`open_prs: 0` in plan/program) because scripts skip drafts and require `merge-approved` + gate-ready.
- **Duplicate matmul stack** on `lic`: 10+ open `bench_improver` PRs — recommend **#446** as canonical after CI; supersede #418–#439 when picked.
- Posted alignment comments on **lis#20**, **lic#446**, **lic#432**, **lic#418**, **roadmap#26**; added `plan-needed` on **lis#20**.
- **roadmap#26** deferred — never auto-close per policy; confirm abandoned before close.
- **54** branches still without PR; **60** in hygiene (down from 132) — `pr_branch_opener` owns.
- Preflight `pr-merge-queue-plan.py` / `run-pr-program.py` re-run **timed out** (>120s, gate script per PR); used on-disk JSON + live `gh` queries.

## Deliverable / findings

### Per-PR verdicts (8 reviewed)

| PR | Repo | Verdict | Action taken |
|----|------|---------|--------------|
| [#26](https://github.com/li-langverse/roadmap/pull/26) | roadmap | **defer** | Comment — draft vision snapshot; do not close without human |
| [#432](https://github.com/li-langverse/lic/pull/432) | lic | **aligned** | Comment — plan-only draft for #424 / PH-7e |
| [#431](https://github.com/li-langverse/lic/pull/431) | lic | **aligned** | — plan-only draft for #429 / PH-7d |
| [#430](https://github.com/li-langverse/lic/pull/430) | lic | **aligned** | — plan-only draft for #428 / PH-8p-a |
| [#135](https://github.com/li-langverse/benchmarks/pull/135) | benchmarks | **aligned** | — plan-only draft (LIC_ROOT honesty) |
| [#20](https://github.com/li-langverse/lis/pull/20) | lis | **needs plan** | Comment + `plan-needed` label |
| [#446](https://github.com/li-langverse/lic/pull/446) | lic | **needs plan** | Comment — PH-5b/7e; duplicate stack note |
| [#418](https://github.com/li-langverse/lic/pull/418) | lic | **superseded** (pending) | Comment — close after #446 canonical |

### Hygiene close queue (10 drafts — not closed)

| PR | Reason in hygiene | Alignment |
|----|-------------------|-----------|
| lic#430–432 | draft PR | **Keep** — active plan deliverables for #428–#424 |
| benchmarks#123–124, #128, #135–137 | draft PR | **Keep** #135–137 plans; **defer** #123–128 for maintainer abandon check |
| roadmap#26 | draft PR | **Defer** — governance snapshot |

### Merge order / vision

- **Vision order:** package CI/mirrors → benchmarks → lic → lip/lit/lis → roadmap (roadmap last).
- **No wrong-order** violations in reviewed set; **lis#20** correctly after lic numerics land.
- **North star fit:** PH-5b/7e work serves **provable** tier-1 ≤1.2× before perf claims; PH-DB serves ecosystem **easy** agent hosting.

### Labels

- Added: `plan-needed` on **lis#20**
- Not added: `merge-approved` (reserved for `pr-review-agent`)
- `plan-needed` on **lic#446** — `gh pr edit` failed (GraphQL Projects classic deprecation); comment documents need

### Closes this run

**0** — all `safe_now: false`; roadmap#26 protected; no PR in `merge_sequence`.

## Recommended issues/PRs

| Title | Repo | Labels / next step |
|-------|------|-------------------|
| perf(tier1): matmul @ lowering + prezeroed C | **lic** [#446](https://github.com/li-langverse/lic/pull/446) | `plan-approved` after #424 ack; then `pr-review-agent` |
| feat(PH-DB): lis db supervisor | **lis** [#20](https://github.com/li-langverse/lis/pull/20) | `plan-needed` ✓ — link PH-DB issue, `plan-approved` |
| docs(plan): PH-7e tier-1 red reconciliation | **lic** [#432](https://github.com/li-langverse/lic/pull/432) | Maintainer → `plan-approved` on #424 |
| docs(ecosystem): vision status snapshot | **roadmap** [#26](https://github.com/li-langverse/roadmap/pull/26) | Human: refresh or close with pointer |
| Close matmul duplicate stack | **lic** #418,#420,#427,#435,#437,#439 | After #446 CI green — supersede with comment |
| plan-needed issues (30) | **lic** + org | `issue-feature-triage.json` — `plan_verifier` / human ack |

## Deferred

- **7** remaining hygiene draft PRs not individually commented (same verdict as #432).
- **Matmul duplicate PRs** (#407–#439 except #446) — close batch after maintainer picks canonical.
- **54+** branches without open PR — `pr_branch_opener`.
- **roadmap#20–21** with `merge-approved` — do not touch in alignment pass; `pr_merger` / human.
- Preflight script re-run — retry when gate script latency acceptable.
- **benchmarks** agent digest PRs (#155–#172) — CI/docs churn; low merge priority, no alignment blockers identified in sample.

## Errors

- **Preflight timeout:** `pr-merge-queue-plan.py` + `run-pr-program.py` exceeded 120s (background PID 606975). Used cached `data/latest/*.json` + live `gh`.
- **Label API:** `gh pr edit --add-label plan-needed` on lic#446 failed: `GraphQL: Projects (classic) is being deprecated…` — documented in comment only.
