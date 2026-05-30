# PR branch opener digest — 2026-05-30T01:26Z

**Agent:** `pr_branch_opener` · **Run:** `rec:pr_branch_opener:429eedb2fc9785d9dc68` · **North star:** proof → easy → fast · **PH context:** ecosystem docs visibility (easy pillar), coord_ecosystem · **Preflight:** `pr-branch-hygiene.json` @ 2026-05-30T01:26Z (57 branches needing PR, 12 repos scanned) · **merge_plan / pr_program:** open_prs=0, merge_approved=0

## Executive summary

- Refreshed `pr-branch-hygiene.py`; hygiene reports **57** remote branches ahead of default with no open PR (down from stale briefing count of 133).
- Opened **6** PRs this run (cap); **0** errors; duplicate check via `gh pr view --head` before create.
- All 6 targets are **`chore/agent-docs_maintainer-20260530`** branches across ecosystem repos — aligns with briefing `docs_maintainer` recommendation (8 repos without live docs).
- Skipped **12** stale `lic/chore/agent-bench_improver-*` stubs and large `-digest` agent branches in selection logic (deferred to future passes).
- No merges, no `merge-approved`, no pushes to protected defaults.
- **51** branches remain flagged by hygiene for future opener passes.

## Deliverable / findings

### Branches opened

| Repo | Branch | Base | Ahead | PR |
|------|--------|------|------:|-----|
| roadmap | `chore/agent-docs_maintainer-20260530` | main | 2 | https://github.com/li-langverse/roadmap/pull/39 |
| benchmarks | `chore/agent-docs_maintainer-20260530` | main | 8 | https://github.com/li-langverse/benchmarks/pull/178 |
| lip | `chore/agent-docs_maintainer-20260530` | main | 3 | https://github.com/li-langverse/lip/pull/31 |
| lit | `chore/agent-docs_maintainer-20260530` | main | 3 | https://github.com/li-langverse/lit/pull/17 |
| lis | `chore/agent-docs_maintainer-20260530` | main | 3 | https://github.com/li-langverse/lis/pull/22 |
| li-net | `chore/agent-docs_maintainer-20260530` | main | 1 | https://github.com/li-langverse/li-net/pull/14 |

All PR bodies include `<!-- li-agent -->` and the standard **Agent deliverable** checklist.

### Skipped (this run)

| Reason | Count | Examples |
|--------|------:|----------|
| Not selected (6/6 quota used) | 51 | remaining hygiene rows |
| Stale lic bench_improver stubs (selection filter) | 12 | `lic/chore/agent-bench_improver-*` |
| Large agent digest branches (selection filter) | 3 | `benchmarks/chore/agent-*-digest` (35–39 ahead) |
| Already has open PR | 0 | — |
| Empty vs base / merge-only | 0 | — |
| Permission error | 0 | — |

### Errors

None.

## Recommended issues/PRs

**Next opener pass (no PR yet, high value):**

| Repo | Branch | Ahead | Suggested focus | Labels |
|------|--------|------:|-----------------|--------|
| roadmap | `chore/ph-db-status-refresh` | 2 | PH-DB status refresh | `plan-needed`, governance |
| roadmap | `chore/agent-kit-1.3.3-roadmap` | 1 | agent-kit sync | `plan-approved` (chore) |
| roadmap | `cursor/fix-refresh-workflow-c81e` | 2 | refresh workflow fix | `plan-needed` |
| li-language | `feat/tier2-physics-suite-expansion` | 47 | tier-2 physics suite | `plan-needed` |
| li-language | `feat/composable-by-default` | 40 | composable-by-default design | `plan-needed` |
| li-language | `feat/phase-2f-discharge-corpus` | 22 | Phase 2f provability | `plan-needed`, Phase-2f |

**Opened this run — route to `pr_alignment`:**

| PR | Labels to add (human/agent) |
|----|----------------------------|
| [roadmap#39](https://github.com/li-langverse/roadmap/pull/39) | `plan-approved` (chore/docs) |
| [benchmarks#178](https://github.com/li-langverse/benchmarks/pull/178) | `plan-approved` (chore/docs) |
| [lip#31](https://github.com/li-langverse/lip/pull/31) | `plan-approved` (chore/docs) |
| [lit#17](https://github.com/li-langverse/lit/pull/17) | `plan-approved` (chore/docs) |
| [lis#22](https://github.com/li-langverse/lis/pull/22) | `plan-approved` (chore/docs) |
| [li-net#14](https://github.com/li-langverse/li-net/pull/14) | `plan-approved` (chore/docs) |

**pr_alignment backlog (from hygiene):** 10 draft PRs flagged for close/supersede review (lic #430–432, benchmarks #123–137, roadmap #26).

## Deferred

- **51** hygiene rows not opened (6/6 quota); includes remaining `chore/agent-docs_maintainer-20260530` in li-httpd, li-std-core, li-std-math, li-demo.
- **12** `lic/chore/agent-bench_improver-*` stale agent stubs — likely abandoned; consider branch cleanup vs PR.
- **li-language** large feature stacks (22–47 commits ahead) — defer until `plan-needed` review.
- **benchmarks/bot/nightly-summary-26507175087** — confirm bot batch policy.
- **pr_alignment:** run `review-pr-alignment` checklist on newly opened PRs before `merge-approved`.
