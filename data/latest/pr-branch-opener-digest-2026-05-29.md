# PR branch opener digest — 2026-05-29

**Agent:** `pr_branch_opener` · **Queued:** `rec:pr_branch_opener:1855778aa2a8f643fd03` · **North star:** proof → easy → fast · **Preflight:** `pr-branch-hygiene.json` @ 2026-05-29T18:30Z (95 branches needing PR, 12 repos scanned)

## Executive summary

- Refreshed hygiene scan: **95** remote branches ahead of default with **no open PR** (was 93 in briefing snapshot).
- Opened **6** PRs this run (cap); **0** errors; **0** duplicate PRs (all passed `gh pr view --head`).
- Prioritized **feature/agent** branches; deferred **13** `bot/fuzz-corpus-*` and **1** `bot/nightly-summary-*` automation stubs per feature-branch policy.
- **lic** (3), **lip** (1), **lis** (1), **benchmarks** (1) — cross-repo coverage for human review.
- **89** branches remain without PR for a future opener pass.
- **9** open PRs flagged for close/supersede in hygiene (`prs_recommended_close`); route to `pr_alignment` — not touched here.
- No merges, no `merge-approved`, no pushes to protected defaults.

## Deliverable / findings

### Branches opened

| Repo | Branch | Base | PR |
|------|--------|------|-----|
| lic | `chore/agent-bench_improver-horner-honesty` | main | https://github.com/li-langverse/lic/pull/413 |
| lic | `chore/agent-bug_fixer-68445695` | main | https://github.com/li-langverse/lic/pull/414 |
| lic | `feat/vision-llm-agent-diagnostics` | main | https://github.com/li-langverse/lic/pull/415 |
| lip | `feat/ph-db-4-registry-openapi` | main | https://github.com/li-langverse/lip/pull/24 |
| lis | `cursor/staging-majico-httpd-bridge-3861` | main | https://github.com/li-langverse/lis/pull/15 |
| benchmarks | `chore/agent-kit-sync-benchmarks` | main | https://github.com/li-langverse/benchmarks/pull/145 |

All PR bodies include `<!-- li-agent -->` and the standard **Agent deliverable** checklist.

### Skipped (this run)

| Reason | Count | Examples |
|--------|------:|----------|
| `bot/*` automation — feature-branch policy | 14 | `bot/fuzz-corpus-*`, `bot/nightly-summary-*` |
| Not selected (quota / defer to next run) | 75 | remaining `chore/agent-*`, `feat/ph-db-*`, `cursor/*` across org |
| Already has open PR | 0 | — |
| Empty vs base / merge-only | 0 | — |

### Errors

None.

## Recommended issues/PRs

**Next opener pass (high signal, no PR yet):**

| Repo | Branch | Ahead | Suggested focus |
|------|--------|------:|-----------------|
| lic | `chore/agent-bench_improver-19883836` | 3 | PH-5b / tier-1 bench improver |
| lip | `feat/ph-db-4-registry-e2e-automated` | 1 | PH-DB registry e2e |
| lis | `cursor/wp-g-ph-db-ci` | 2 | PH-DB CI wiring |
| lis | `feat/ph-db-4-lidb-liorm-wire` | — | lidb ↔ liorm |
| benchmarks | `chore/tier-ingest-wp-b5` | 1 | tier ingest |
| roadmap | `feat/vision-llm-agent-diagnostics` | — | governance review (if branch exists) |

**Opened this run — label for alignment (`pr_alignment`):**

| PR | Labels to add (human/agent) |
|----|----------------------------|
| [lic#413](https://github.com/li-langverse/lic/pull/413) | `plan-needed`, numerics |
| [lic#414](https://github.com/li-langverse/lic/pull/414) | `plan-needed`, `bug` |
| [lic#415](https://github.com/li-langverse/lic/pull/415) | `plan-needed`, Vision-LLM / PH |
| [lip#24](https://github.com/li-langverse/lip/pull/24) | `plan-needed`, PH-DB |
| [lis#15](https://github.com/li-langverse/lis/pull/15) | `plan-needed`, PH-DB |
| [benchmarks#145](https://github.com/li-langverse/benchmarks/pull/145) | `chore`, agent-kit |

## Deferred

- **87+** `bot/fuzz-corpus-*` branches on `lic` — consider batch close or dedicated bot workflow instead of 87 individual PRs.
- **75** feature/agent branches not opened (6/6 quota used).
- **pr_alignment:** 9 PRs recommended for close/supersede per hygiene — separate agent pass.
- **Fuzz bot PR policy:** confirm with maintainers whether `bot/fuzz-corpus-*` should ever get human-review PRs or auto-merge bot.
