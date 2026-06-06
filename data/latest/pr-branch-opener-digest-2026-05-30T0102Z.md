# PR branch opener digest — 2026-05-30T01:02Z (proactive run)

**Agent:** `pr_branch_opener` · **Run:** `pr_branch_opener-1780102681201` · **North star:** proof → easy → fast · **PH context:** PH-DB-4 registry/docs, ecosystem governance, Vision-LLM · **Preflight:** `pr-branch-hygiene.json` @ 2026-05-30T01:00Z (155 branches needing PR, 12 repos scanned) · **merge_plan / pr_program:** open_prs=0, merge_approved=0

## Executive summary

- Refreshed `pr-branch-hygiene.py` and merge-queue preflight; hygiene reports **155** remote branches ahead of default with no detected open PR.
- Opened **6** PRs this run (cap); **0** errors; duplicate check via REST API (`repos/.../pulls?head=`) before create.
- **GraphQL rate limit** exhausted mid-run (`gh pr list` / `gh pr view --head` unusable); fell back to REST API for duplicate detection and PR creation.
- Many hygiene rows **already had open PRs** when verified via REST (e.g. top PH-DB lis/lip/roadmap branches) — hygiene false positives likely from `gh pr list --limit 50` pagination or GraphQL saturation.
- Targets selected: production registry docs, ecosystem stats, org CI branch protection, liq token-efficiency cross-link, goal-scaffold docs, def-syntax sync.
- No merges, no `merge-approved`, no pushes to protected defaults.
- **~149** branches remain flagged by hygiene for future opener passes (prioritize `feat/*`, `cursor/*`; skip `bot/*` automation unless policy requires).

## Deliverable / findings

### Branches opened

| Repo | Branch | Base | Ahead | PR |
|------|--------|------|------:|-----|
| lis | `feat/production-registry-docs` | main | 2 | https://github.com/li-langverse/lis/pull/21 |
| roadmap | `feat/ecosystem-overview-stats` | main | 3 | https://github.com/li-langverse/roadmap/pull/36 |
| roadmap | `feat/org-ci-branch-protection` | main | 1 | https://github.com/li-langverse/roadmap/pull/37 |
| roadmap | `feat/liq-token-efficiency-xlink` | main | 1 | https://github.com/li-langverse/roadmap/pull/38 |
| li-language | `feat/goal-scaffold-v1-docs` | main | 16 | https://github.com/li-langverse/li-language/pull/13 |
| lit | `cursor/sync-def-syntax-57b4` | main | 1 | https://github.com/li-langverse/lit/pull/16 |

All PR bodies include `<!-- li-agent -->` and the standard **Agent deliverable** checklist.

### Skipped (this run)

| Reason | Count | Examples |
|--------|------:|----------|
| Already has open PR (REST verified) | 8 | `lis/feat/ph-db-4-lidb-liorm-wire` → #18, `lip/feat/ph-db-4-registry-openapi` → #24, `li-httpd/cursor/httpd-plan-continue` |
| Not selected (6/6 quota used) | 147+ | remaining hygiene rows including `bot/fuzz-corpus-*`, `chore/agent-*-digest`, large `li-language/feat/*` stacks |
| Empty vs base / merge-only | 0 | — |
| Permission error | 0 | — |

### Errors

None on PR create. **Note:** GraphQL API rate limit hit (`remaining: 0`) during preflight; REST core API remained available (1215+ calls).

## Recommended issues/PRs

**Next opener pass (REST-verified no PR yet):**

| Repo | Branch | Ahead | Suggested focus | Labels |
|------|--------|------:|-----------------|--------|
| li-language | `feat/tier2-physics-suite-expansion` | 47 | tier-2 physics suite | `plan-needed` |
| li-language | `feat/composable-by-default` | 40 | composable-by-default design | `plan-needed` |
| li-language | `feat/hpc-competitive-intelligence` | 38 | HPC competitive intel | `plan-needed` |
| li-language | `feat/phase-2f-discharge-corpus` | 22 | Phase 2f provability | `plan-needed`, Phase-2f |
| benchmarks | `chore/agent-kit-sync-benchmarks` | 1 | agent-kit sync | `plan-approved` (chore) |
| li-net | `chore/agent-kit-sync-li-net` | 3 | agent-kit sync | `plan-approved` (chore) |

**Opened this run — route to `pr_alignment`:**

| PR | Labels to add (human/agent) |
|----|----------------------------|
| [lis#21](https://github.com/li-langverse/lis/pull/21) | `plan-needed`, PH-DB-4 |
| [roadmap#36–38](https://github.com/li-langverse/roadmap/pulls) | `plan-needed` (governance/docs) |
| [li-language#13](https://github.com/li-langverse/li-language/pull/13) | `plan-needed`, Vision-LLM |
| [lit#16](https://github.com/li-langverse/lit/pull/16) | chore / easy-syntax sync |

## Deferred

- **149+** hygiene rows not opened (6/6 quota); includes **14** `lic/bot/fuzz-corpus-*` and **1** `benchmarks/bot/nightly-summary-*` — confirm bot batch policy vs individual PRs.
- **Hygiene false positives:** increase `gh pr list --limit` or paginate in `pr-branch-hygiene.py` to avoid re-reporting branches with existing PRs.
- **GraphQL rate limit:** defer bulk `gh pr view` until reset; prefer REST head-filter for opener agent.
- **pr_alignment:** run `review-pr-alignment` checklist on newly opened PRs before `merge-approved`.
- **li-language** large feature stacks (40–47 commits ahead) — defer merge until plan-approved and dependency CI green.
