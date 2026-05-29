# PR branch opener digest — 2026-05-29T22:52Z (run 3)

**Agent:** `pr_branch_opener` · **Queued:** `rec:pr_branch_opener:dcef3d6b86696dfaed9f` · **North star:** proof → easy → fast · **Preflight:** `pr-branch-hygiene.json` @ 2026-05-29T22:51Z (72 branches needing PR, 12 repos scanned)

## Executive summary

- Refreshed hygiene scan: **72** remote branches ahead of default with **no open PR** (down from 132 in briefing snapshot; prior runs opened 12 PRs).
- Opened **6** PRs this run (cap); **0** errors; **0** duplicate PRs (all passed `gh pr view --head`).
- Prioritized **PH-DB / Vision-LLM / ecosystem** feature branches over **7** `bot/fuzz-corpus-*` automation stubs at list head.
- Coverage: **lis** (1), **roadmap** (2), **li-language** (1), **benchmarks** (1), **lip** (1).
- **66** branches remain without PR for a future opener pass.
- **10** draft PRs flagged for close/supersede in hygiene (`prs_recommended_close`); route to `pr_alignment` — not touched here.
- No merges, no `merge-approved`, no pushes to protected defaults.

## Deliverable / findings

### Branches opened

| Repo | Branch | Base | PR |
|------|--------|------|-----|
| lis | `feat/ph-db-4-registry-routes` | main | https://github.com/li-langverse/lis/pull/19 |
| roadmap | `feat/ph-db-0-lidb-proposal` | main | https://github.com/li-langverse/roadmap/pull/34 |
| roadmap | `feat/docs-hpc-ai-north-star` | main | https://github.com/li-langverse/roadmap/pull/35 |
| li-language | `feat/vision-llm-agent-diagnostics` | main | https://github.com/li-langverse/li-language/pull/12 |
| benchmarks | `chore/agent-gap_explorer-2026-05-20` | main | https://github.com/li-langverse/benchmarks/pull/170 |
| lip | `cursor/lip-git-install-lis-cli-3861` | main | https://github.com/li-langverse/lip/pull/30 |

All PR bodies include `<!-- li-agent -->` and the standard **Agent deliverable** checklist.

### Skipped (this run)

| Reason | Count | Examples |
|--------|------:|----------|
| `bot/*` automation — deferred (quota used on feature work) | 7+ | `bot/fuzz-corpus-26325164908`, `bot/nightly-summary-26507175087`, … |
| Not selected (quota / defer to next run) | 66 | remaining `chore/agent-*`, `bot/*`, `feat/*` across org |
| Already has open PR | 0 | — |
| Empty vs base / merge-only | 0 | — |

### Errors

None.

## Recommended issues/PRs

**Next opener pass (high signal, no PR yet):**

| Repo | Branch | Ahead | Suggested focus |
|------|--------|------:|-----------------|
| lic | `bot/fuzz-corpus-26325164908` | 1 | fuzz corpus bot — batch policy? |
| lic | `chore/agent-bench_improver-42289450` | 2 | PH-5b / tier-1 bench improver |
| lis | `cursor/wp-i-ph-db-lis-service` | 4 | PH-DB lis service wiring |
| lis | `feat/production-registry-docs` | 2 | production registry docs |
| roadmap | `feat/ecosystem-overview-stats` | 3 | ecosystem overview stats |
| li-language | `feat/composable-by-default` | 40 | composable-by-default docs |

**Opened this run — label for alignment (`pr_alignment`):**

| PR | Labels to add (human/agent) |
|----|----------------------------|
| [lis#19](https://github.com/li-langverse/lis/pull/19) | `plan-needed`, PH-DB-4 |
| [roadmap#34](https://github.com/li-langverse/roadmap/pull/34) | `plan-needed`, PH-DB-0 |
| [roadmap#35](https://github.com/li-langverse/roadmap/pull/35) | `plan-needed`, vision |
| [li-language#12](https://github.com/li-langverse/li-language/pull/12) | `plan-needed`, Vision-LLM |
| [benchmarks#170](https://github.com/li-langverse/benchmarks/pull/170) | agent digest — review for merge |
| [lip#30](https://github.com/li-langverse/lip/pull/30) | `plan-needed`, ecosystem |

## Deferred

- **7+** `bot/fuzz-corpus-*` branches at head of hygiene list — confirm batch bot workflow vs individual PRs.
- **66** feature/agent branches not opened (6/6 quota used).
- **pr_alignment:** 10 draft PRs recommended for close/supersede per hygiene — separate agent pass.
- **li-language** large feature stacks (`feat/tier2-physics-suite-expansion`, `fix/ci-dev-pr3-sync`, etc.) — defer until Vision-LLM / PH-DB stack lands or human triage.
