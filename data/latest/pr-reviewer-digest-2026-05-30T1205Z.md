# PR reviewer digest — 2026-05-30T12:05Z

**Agent:** `pr_reviewer` · **Run id:** `pr_reviewer-1780142707959` · **Source:** proactive ecosystem sweep · **north_star_fit:** plan governance (PH-2i/2h/2f/7e, PH-8p) + agent-kit sync + tier-1 numerics stack (PH-5b, PH-7e) — proof → easy → fast

## Executive summary

- **Preflight refreshed:** `pr-merge-queue-plan.json` and `pr-program-run.json` at 12:05Z report **`open_prs=0`** — GraphQL quota exhausted (`remaining=0`, reset ~12:09Z); REST search shows **≥50 open** org PRs (false empty in gate scripts).
- **Since last pass (11:51Z):** [benchmarks#226](https://github.com/li-langverse/benchmarks/pull/226) and [lic#535](https://github.com/li-langverse/lic/pull/535) **merged** — P0 handbook/audit queue cleared.
- **New `merge-approved` (CI green):** [lic#530](https://github.com/li-langverse/lic/pull/530), [#531](https://github.com/li-langverse/lic/pull/531), [#532](https://github.com/li-langverse/lic/pull/532) — plan docs for PH-2i/2h/2f; [li-language#16](https://github.com/li-langverse/li-language/pull/16) — agent-kit 1.3.5 sync.
- **Numerics stack blocked:** [lic#499](https://github.com/li-langverse/lic/pull/499) fails `build-and-test` + macOS; [lic#524](https://github.com/li-langverse/lic/pull/524) CI green but **defer `merge-approved`** until #499 lands.
- **Feature gate:** [lic#517](https://github.com/li-langverse/lic/pull/517) (PH-7d GPU) — CI fail + conflicts; needs `plan-approved`.
- **Stale `merge-approved`:** lic#437, benchmarks#132, roadmap#19–21 — CI green but **merge conflicts** (`mergeable_state=dirty`); resolve or close if superseded.
- **Governance:** roadmap PRs require **human merge** per policy; do not auto-merge.
- **Error (non-fatal):** GraphQL quota exhausted — `pr-merge-gate.py` returns `pr_not_found`; REST `gh api` used for verification and review actions.

## Deliverable / findings

### Preflight artifacts

| Artifact | `generated_at` | Signal |
|----------|----------------|--------|
| `pr-merge-queue-plan.json` | 2026-05-30T12:05Z | Empty `merge_sequence`; `open_prs=0` ⚠️ GraphQL artifact |
| `pr-program-run.json` | 2026-05-30T12:05Z | `all_open=[]`, `ci_green=0` ⚠️ same |
| REST org search | 2026-05-30T12:05Z | **≥50 open** PRs (search API sample) |
| Ecosystem audit (briefing) | 2026-05-30T12:03Z | 6 red bench rows (matmul_blocked/naive, ml_*, num_gmres); PH-5b |

### Standards checklist (REST-verified CI-green sample)

| PR | Vision / PH | Strict / proof | Security | Performance | Release notes | Verdict |
|----|-------------|----------------|----------|-------------|---------------|---------|
| lic#530 | PH-2i/2f/7e plan (#472) | Plan doc only | N/A | N/A | N/A | **aligned** — `merge-approved` **added** |
| lic#531 | PH-2h / G-math-syn (#527) | Plan doc only | N/A | N/A | N/A | **aligned** — `merge-approved` **added** |
| lic#532 | PH-2i-b broadcast defer (#526) | Plan doc only | N/A | N/A | N/A | **aligned** — `merge-approved` **added** |
| li-language#16 | Agent-kit sync | Cursor policy | N/A | N/A | waive (chore) | **aligned** — `merge-approved` **added** |
| lic#524 | PH-5b, PH-7e | Harness only | N/A | Evidence path | ✅ | **aligned, defer** (after #499) |
| lic#499 | PH-5b, PH-7e | MIR restore | N/A | Bench evidence | ✅ study doc | **aligned, CI red** |
| lic#536 | PH-8p-c plan (#525) | Plan doc | N/A | N/A | N/A | **defer** — CI pending/fail |
| lic#537 | PH-Pkg governance (#476) | Plan doc | N/A | N/A | N/A | **defer** — CI pending/fail |
| lic#517 | PH-7d | Feature | review surface | N/A | TBD | **needs plan** — CI fail + conflicts |
| lic#437 | PH-5b/7e | perf | N/A | bench | ✅ | **stale label** — conflicts |
| roadmap#46 | Governance | chore | N/A | N/A | waive | **human merge only** |
| lip#41 | Platform CI | chore | N/A | N/A | waive | **defer** — conflicts |

### Gate script

```text
pr-merge-gate.py (GraphQL): pr_not_found for all sampled PRs
REST verification:
  lic#530-532: merge-approved ✓ (added)  CI_GREEN (6/6)  mergeable behind
  li-language#16: merge-approved ✓ (added)  CI_GREEN (9/9)  mergeable blocked (review)
  lic#524: no label  CI_GREEN  mergeable behind  defer comment posted
  lic#499: numerics-research  CI_FAIL (build-and-test, macOS)
  lic#517: no label  CI_FAIL  mergeable dirty
```

### Actions taken

| Action | Target | Result |
|--------|--------|--------|
| Review comment + checklist | [lic#530](https://github.com/li-langverse/lic/pull/530#issuecomment-4582770846) | Posted |
| Label `merge-approved` | [lic#530](https://github.com/li-langverse/lic/pull/530) | **Added** |
| Review comment + checklist | [lic#531](https://github.com/li-langverse/lic/pull/531#issuecomment-4582770894) | Posted |
| Label `merge-approved` | [lic#531](https://github.com/li-langverse/lic/pull/531) | **Added** |
| Review comment + checklist | [lic#532](https://github.com/li-langverse/lic/pull/532#issuecomment-4582770940) | Posted |
| Label `merge-approved` | [lic#532](https://github.com/li-langverse/lic/pull/532) | **Added** |
| Review comment + checklist | [li-language#16](https://github.com/li-langverse/li-language/pull/16#issuecomment-4582770873) | Posted |
| Label `merge-approved` | [li-language#16](https://github.com/li-langverse/li-language/pull/16) | **Added** |
| Defer comment (stack order) | [lic#524](https://github.com/li-langverse/lic/pull/524#issuecomment-4582770888) | Posted |
| Merge | — | **None** (pr_reviewer mandate) |

## Recommended issues/PRs

| Priority | Repo | Item | Labels / next step |
|----------|------|------|-------------------|
| P0 | lic | [#499](https://github.com/li-langverse/lic/pull/499) matmul MIR restore | Fix `build-and-test` + macOS → pr-review-agent |
| P0 | lic | [#530–532](https://github.com/li-langverse/lic/pulls) plan docs PH-2i/2h | `merge-approved` — **human APPROVED** → pr_merger |
| P0 | li-language | [#16](https://github.com/li-langverse/li-language/pull/16) agent-kit 1.3.5 sync | `merge-approved` — **human APPROVED** → pr_merger |
| P1 | lic | [#524](https://github.com/li-langverse/lic/pull/524) matmul_blocked harness | After #499 green; then `merge-approved` |
| P1 | lic | [#536](https://github.com/li-langverse/lic/pull/536), [#537](https://github.com/li-langverse/lic/pull/537) plan docs | CI green → review → `merge-approved` |
| P1 | lip | [#41](https://github.com/li-langverse/lip/pull/41) LLVM 22 bootstrap | Resolve conflicts → CI → review |
| P2 | lic | [#517](https://github.com/li-langverse/lic/pull/517) GPU decorators | `plan-approved` + fix CI |
| P2 | lic | [#437](https://github.com/li-langverse/lic/pull/437) matmul naive+blocked | Stale `merge-approved` — resolve conflicts or close if superseded by #524 |
| P2 | benchmarks | [#132](https://github.com/li-langverse/benchmarks/pull/132) macOS nightly CI | Stale `merge-approved` — resolve conflicts |
| Hygiene | org | 147 branches without PR | `pr_branch_opener` wave |
| Governance | roadmap | [#19–21, #43, #46](https://github.com/li-langverse/roadmap/pulls) | **Human merge only** — conflicts on #19–21 |

## Deferred

- Full `run-pr-program.py` org enumeration until **GraphQL rate limit resets** (~2026-05-30T12:09Z).
- `merge-approved` on lic#524 until lic#499 is CI green (stack order per pr_alignment).
- lic#536/#537 until CI fully green.
- **Merge execution** — pr_merger only after `reviewDecision: APPROVED`.
- **roadmap** / governance repos — human merge per policy.
- Docs maintainer wave duplicates (lic#533, li-std-* #11–15 dirty) — dedupe after #535 merge (done).
- Reconcile stale `merge-approved` on lic#437 vs lic#524 numerics stack (close superseded if redundant).

## Error

**GitHub GraphQL rate limit exhausted** (`graphql.remaining=0`, reset ~2026-05-30T12:09Z) during `gh pr list` and `pr-merge-gate.py`. Symptom: preflight scripts report `open_prs=0`; gate returns `pr_not_found`. **Mitigation:** REST `gh api` + search API used for verification, comments, and labels. **Stack trace:** N/A (API quota, not Python exception).
