# PR branch opener digest — 2026-05-30T10:55Z (proactive run)

**Agent:** `pr_branch_opener` · **Run:** `pr_branch_opener-1780138366116` · **North star:** proof → easy → fast · **PH context:** PH-DB-4 registry/lip client, PH-5b/7e tier-1 numerics, tier-2 physics suite · **Preflight:** `pr-branch-hygiene.json` @ 2026-05-30T10:54Z (143 branches needing PR, 12 repos scanned) · **merge_plan / pr_program:** open_prs=0, merge_approved=0

## Executive summary

- Refreshed `pr-branch-hygiene.py`, `pr-merge-queue-plan.py`, and `run-pr-program.py`; hygiene now reports **143** remote branches ahead of default with no detected open PR (up from stale briefing snapshot of 0).
- Opened **6** PRs this run (cap); **0** create errors after REST fallback; duplicate check via REST `repos/.../pulls?head=` before create.
- **GraphQL rate limit** exhausted (`remaining: 0`); `gh pr create` / `gh pr view --head` failed — fell back to REST API for duplicate detection and PR creation (core API: 3915+ remaining).
- Many hygiene rows **already had open PRs** when verified via REST 422 response (e.g. `lic/bench/improver-matmul-tier1-20260530`, lis PH-DB branches) — hygiene false positives from `gh pr list --limit 50` pagination.
- Targets selected: PH-DB-4 lip registry/docs, tier-2 physics suite expansion, PH-DB roadmap status refresh.
- No merges, no `merge-approved`, no pushes to protected defaults.
- **~137** branches remain flagged by hygiene for future opener passes (prioritize `feat/*`, `cursor/*`, `bench/*`; skip `bot/*` unless policy requires).

## Deliverable / findings

### Branches opened

| Repo | Branch | Base | Ahead | PR |
|------|--------|------|------:|-----|
| lip | `feat/ph-db-4-registry-openapi` | main | 3 | https://github.com/li-langverse/lip/pull/36 |
| lip | `feat/ph-db-e2e-integration-doc` | main | 3 | https://github.com/li-langverse/lip/pull/37 |
| lip | `feat/ph-db-4-lip-publish-client` | main | 2 | https://github.com/li-langverse/lip/pull/38 |
| lip | `feat/ph-db-4-registry-e2e-automated` | main | 2 | https://github.com/li-langverse/lip/pull/39 |
| li-language | `feat/tier2-physics-suite-expansion` | main | 47 | https://github.com/li-langverse/li-language/pull/15 |
| roadmap | `chore/ph-db-status-refresh` | main | 3 | https://github.com/li-langverse/roadmap/pull/46 |

All PR bodies include `<!-- li-agent -->` and the standard **Agent deliverable** checklist.

### Skipped (this run)

| Reason | Count | Examples |
|--------|------:|----------|
| Already has open PR (REST 422 / duplicate check) | 15+ | `lic/bench/improver-matmul-tier1-20260530`, `lis/feat/ph-db-4-lidb-liorm-wire`, `li-httpd/cursor/httpd-plan-continue`, `benchmarks/chore/agent-bench_improver-20260530-tier1-red-clear` |
| GraphQL rate limit on `gh pr create` (retried via REST) | 6 | first batch — all resolved via REST fallback |
| Not selected (6/6 quota used) | 137 | remaining hygiene rows including `chore/agent-*-digest`, `bot/nightly-summary-*`, large `li-language/feat/*` stacks |
| Empty vs base / merge-only | 0 | — |
| Permission error | 0 | — |

### Errors

None on final PR create. **Note:** GraphQL API rate limit hit (`remaining: 0`, reset pending); REST core API remained available (~3900+ calls).

## Recommended issues/PRs

**Next opener pass (REST-verified no PR yet):**

| Repo | Branch | Ahead | Suggested focus | Labels |
|------|--------|------:|-----------------|--------|
| li-language | `feat/composable-by-default` | 40 | composable-by-default design | `plan-needed` |
| li-language | `feat/hpc-competitive-intelligence` | 38 | HPC competitive intel | `plan-needed` |
| li-language | `feat/vision-llm-agent-diagnostics` | 42 | Vision-LLM agent diagnostics | `plan-needed`, Vision-LLM |
| li-language | `feat/phase-2f-discharge-corpus` | 22 | Phase 2f provability | `plan-needed`, Phase-2f |
| li-net | `chore/agent-kit-sync-li-net` | 3 | agent-kit sync | `plan-approved` (chore) |
| benchmarks | `chore/agent-bench_improver-proactive-20260530-digest` | 32 | bench improver digest | `plan-needed`, PH-5b |

**Opened this run — route to `pr_alignment`:**

| PR | Labels to add (human/agent) |
|----|----------------------------|
| [lip#36–39](https://github.com/li-langverse/lip/pulls) | `plan-needed`, PH-DB-4 |
| [li-language#15](https://github.com/li-langverse/li-language/pull/15) | `plan-needed`, tier-2 physics |
| [roadmap#46](https://github.com/li-langverse/roadmap/pull/46) | `plan-needed`, PH-DB governance |

## Deferred

- **137** hygiene rows not opened (6/6 quota); includes **1** `benchmarks/bot/nightly-summary-*` — confirm bot batch policy vs individual PRs.
- **Hygiene false positives:** increase `gh pr list --limit` or paginate in `pr-branch-hygiene.py` to avoid re-reporting branches with existing PRs (143 reported vs many already open).
- **GraphQL rate limit:** defer bulk `gh pr view` until reset; prefer REST head-filter for opener agent.
- **pr_alignment:** run `review-pr-alignment` checklist on newly opened PRs before `merge-approved`.
- **li-language** large feature stacks (38–47 commits ahead) — defer merge until plan-approved and dependency CI green.
