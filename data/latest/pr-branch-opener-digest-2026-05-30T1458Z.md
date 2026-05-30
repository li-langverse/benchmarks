# PR branch opener digest — 2026-05-30T14:58Z (proactive run)

**Agent:** `pr_branch_opener` · **Run:** proactive · **North star:** proof → easy → fast · **PH context:** PH-DB-0/4 (lidb proposal, lip publish/registry, e2e docs), Phase 2f provability, HPC competitive intel · **Preflight:** `pr-branch-hygiene.json` @ 2026-05-30T14:56Z (139 branches needing PR, 12 repos scanned) · **merge_plan / pr_program:** open_prs=0, merge_approved=0

## Executive summary

- Refreshed `pr-branch-hygiene.py`; hygiene reports **139** remote branches ahead of default with no detected open PR (briefing stale snapshot had 0 due to `--skip-slow`).
- Opened **6** PRs this run (cap); **0** errors; duplicate check via REST API (`repos/.../pulls?head=`) before create.
- Prioritized `feat/*` PH-DB and li-language provability/HPC branches over stale `chore/agent-bench_improver-*` orphan rows.
- **5** top candidates skipped — already had open PRs when REST-verified (lis PH-DB stack, roadmap gaps, li-language composable-by-default).
- No merges, no `merge-approved`, no pushes to protected defaults.
- **133** hygiene rows remain for future opener passes; route newly opened PRs to `pr_alignment` before merge queue.

## Deliverable / findings

### Branches opened

| Repo | Branch | Base | Ahead | PR |
|------|--------|------|------:|-----|
| lip | `feat/ph-db-4-lip-publish-client` | main | 3 | https://github.com/li-langverse/lip/pull/46 |
| lip | `feat/ph-db-4-registry-openapi` | main | 3 | https://github.com/li-langverse/lip/pull/47 |
| lip | `feat/ph-db-e2e-integration-doc` | main | 3 | https://github.com/li-langverse/lip/pull/48 |
| roadmap | `feat/ph-db-0-lidb-proposal` | main | 3 | https://github.com/li-langverse/roadmap/pull/48 |
| li-language | `feat/hpc-competitive-intelligence` | main | 38 | https://github.com/li-langverse/li-language/pull/20 |
| li-language | `feat/phase-2f-discharge-corpus` | main | 22 | https://github.com/li-langverse/li-language/pull/21 |

All PR bodies include `<!-- li-agent -->` and the standard **Agent deliverable** checklist.

### Skipped (this run)

| Reason | Count | Examples |
|--------|------:|----------|
| Already has open PR (REST verified) | 5 | `lis/feat/ph-db-4-lidb-liorm-wire` → #29, `lis/feat/ph-db-3-lis-bundle-stub` → #28, `roadmap/feat/ph-db-roadmap-gaps` → #32 |
| Not selected (6/6 quota used) | 133+ | remaining hygiene rows including `chore/agent-*-digest`, `lic/chore/agent-bench_improver-*`, large `li-language/feat/*` stacks |
| Empty vs base / merge-only | 0 | — |
| Permission error | 0 | — |

### Errors

None on PR create.

## Recommended issues/PRs

**Next opener pass (REST-verified no PR yet):**

| Repo | Branch | Ahead | Suggested focus | Labels |
|------|--------|------:|-----------------|--------|
| li-language | `feat/tier2-physics-suite-expansion` | 47 | tier-2 physics suite | `plan-needed` |
| li-language | `feat/composable-by-default` | 40 | composable-by-default design | `plan-needed` (PR #19 exists — close hygiene false positive) |
| li-language | `feat/vision-llm-agent-diagnostics` | 42 | Vision-LLM agent diagnostics | `plan-needed`, Vision-LLM |
| lis | `cursor/wp-i-ph-db-lis-service` | 4 | PH-DB lis service | `plan-needed`, PH-DB |
| roadmap | `feat/lidb-native-plan` | 4 | lidb native plan | `plan-needed`, PH-DB-0 |
| benchmarks | `chore/agent-docs_ui_tester-proactive-20260530T1408Z-digest` | — | current agent digest branch | `plan-approved` (chore) |

**Opened this run — route to `pr_alignment`:**

| PR | Labels to add (human/agent) |
|----|----------------------------|
| [lip#46–48](https://github.com/li-langverse/lip/pulls) | `plan-needed`, PH-DB-4 |
| [roadmap#48](https://github.com/li-langverse/roadmap/pull/48) | `plan-needed`, PH-DB-0 |
| [li-language#20](https://github.com/li-langverse/li-language/pull/20) | `plan-needed`, HPC |
| [li-language#21](https://github.com/li-langverse/li-language/pull/21) | `plan-needed`, Phase-2f |

**Hygiene close candidates (not acted on — human confirm):**

| Repo | PR | Reason |
|------|-----|--------|
| lic | #430–#540 (11 drafts) | draft PR — confirm abandoned before close |

## Deferred

- **133+** hygiene rows not opened (6/6 quota); includes **10** `lic/chore/agent-bench_improver-*` and **1** `benchmarks/bot/nightly-summary-*` — confirm bot/chore batch policy vs individual PRs.
- **Hygiene false positives:** lis PH-DB branches and `li-language/feat/composable-by-default` still listed despite open PRs — paginate `gh pr list` in `pr-branch-hygiene.py`.
- **pr_alignment:** run `review-pr-alignment` checklist on newly opened PRs (#46–48, #48, #20–21) before `merge-approved`.
- **li-language** large feature stacks (40–47 commits ahead) — defer merge until plan-approved and dependency CI green.
- **lic draft PRs (#430–540):** defer close to `pr_alignment` agent with human confirmation.
