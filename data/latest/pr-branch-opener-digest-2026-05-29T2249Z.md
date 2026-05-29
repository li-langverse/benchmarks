# PR branch opener digest — 2026-05-29T22:49Z (run 2)

**Agent:** `pr_branch_opener` · **Queued:** `rec:pr_branch_opener:dcef3d6b86696dfaed9f` · **North star:** proof → easy → fast · **Preflight:** `pr-branch-hygiene.json` @ 2026-05-29T22:49Z (77 branches needing PR, 12 repos scanned)

## Executive summary

- Refreshed hygiene scan: **77** remote branches ahead of default with **no open PR** (briefing snapshot had 132; delta from merged/closed branches and scan refresh).
- Opened **6** PRs this run (cap); **0** errors; **0** duplicate PRs (all passed `gh pr view --head`).
- Prioritized **PH-DB / roadmap governance** branches over **7** `bot/fuzz-corpus-*` automation stubs at list head.
- **lip** (2), **lis** (2), **roadmap** (2) — ecosystem DB/registry coverage for human review.
- **71** branches remain without PR for a future opener pass.
- **10** draft PRs flagged for close/supersede in hygiene (`prs_recommended_close`); route to `pr_alignment` — not touched here.
- No merges, no `merge-approved`, no pushes to protected defaults.

## Deliverable / findings

### Branches opened

| Repo | Branch | Base | PR |
|------|--------|------|-----|
| lip | `feat/ph-db-4-registry-e2e-automated` | main | https://github.com/li-langverse/lip/pull/28 |
| lip | `feat/production-registry-validate` | main | https://github.com/li-langverse/lip/pull/29 |
| lis | `feat/ph-db-3-lis-bundle-stub` | main | https://github.com/li-langverse/lis/pull/17 |
| lis | `feat/ph-db-4-lidb-liorm-wire` | main | https://github.com/li-langverse/lis/pull/18 |
| roadmap | `feat/ph-db-roadmap-gaps` | main | https://github.com/li-langverse/roadmap/pull/32 |
| roadmap | `feat/lidb-native-plan` | main | https://github.com/li-langverse/roadmap/pull/33 |

All PR bodies include `<!-- li-agent -->` and the standard **Agent deliverable** checklist.

### Skipped (this run)

| Reason | Count | Examples |
|--------|------:|----------|
| `bot/*` automation — deferred (quota used on PH-DB) | 7+ | `bot/fuzz-corpus-26325164908`, … |
| Not selected (quota / defer to next run) | 71 | remaining `chore/agent-*`, `bot/*`, `feat/*` across org |
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
| lis | `feat/ph-db-4-registry-routes` | 7 | PH-DB registry routes |
| roadmap | `feat/docs-hpc-ai-north-star` | 1 | north-star docs alignment |
| li-language | `feat/vision-llm-agent-diagnostics` | 42 | Vision-LLM / PH governance |

**Opened this run — label for alignment (`pr_alignment`):**

| PR | Labels to add (human/agent) |
|----|----------------------------|
| [lip#28](https://github.com/li-langverse/lip/pull/28) | `plan-needed`, PH-DB-4 |
| [lip#29](https://github.com/li-langverse/lip/pull/29) | `plan-needed`, PH-DB |
| [lis#17](https://github.com/li-langverse/lis/pull/17) | `plan-needed`, PH-DB-3 |
| [lis#18](https://github.com/li-langverse/lis/pull/18) | `plan-needed`, PH-DB-4 |
| [roadmap#32](https://github.com/li-langverse/roadmap/pull/32) | `plan-needed`, PH-DB |
| [roadmap#33](https://github.com/li-langverse/roadmap/pull/33) | `plan-needed`, lidb |

## Deferred

- **7+** `bot/fuzz-corpus-*` branches at head of hygiene list — confirm batch bot workflow vs individual PRs.
- **71** feature/agent branches not opened (6/6 quota used).
- **pr_alignment:** 10 draft PRs recommended for close/supersede per hygiene — separate agent pass.
- **li-language** large feature stacks (`feat/composable-by-default`, `feat/tier2-physics-suite-expansion`, etc.) — defer until PH-DB stack lands or human triage.
