# PR branch opener digest — 2026-05-29T22:54Z (run 4)

**Agent:** `pr_branch_opener` · **Queued:** `rec:pr_branch_opener:dcef3d6b86696dfaed9f` · **North star:** proof → easy → fast · **PH context:** Phase 2i / PH-5b (ecosystem bench hygiene) · **Preflight:** `pr-branch-hygiene.json` @ 2026-05-29T22:53Z (66 branches needing PR, 12 repos scanned) · **merge_plan / pr_program:** open_prs=0, merge_approved=0

## Executive summary

- Refreshed `pr-branch-hygiene.py`: **66** branches ahead of default with no open PR (down from 132 in briefing snapshot; prior runs opened feature PRs).
- Opened **6** PRs this run (cap); **0** errors; **0** duplicate PRs (all passed `gh pr view --head`).
- All six targets were **lic** `bot/fuzz-corpus-*` automation branches (1 commit ahead of `main` each).
- **60** branches remain without PR for a future opener pass.
- **10** draft PRs flagged for close/supersede in hygiene (`prs_recommended_close`); route to `pr_alignment` — not touched here.
- No merges, no `merge-approved`, no pushes to protected defaults.
- `gh` emitted local uncommitted-change warnings (benchmarks workspace); PR creation succeeded on GitHub.

## Deliverable / findings

### Branches opened

| Repo | Branch | Base | PR |
|------|--------|------|-----|
| lic | `bot/fuzz-corpus-26325164908` | main | https://github.com/li-langverse/lic/pull/448 |
| lic | `bot/fuzz-corpus-26353962639` | main | https://github.com/li-langverse/lic/pull/449 |
| lic | `bot/fuzz-corpus-26387873141` | main | https://github.com/li-langverse/lic/pull/450 |
| lic | `bot/fuzz-corpus-26436457401` | main | https://github.com/li-langverse/lic/pull/451 |
| lic | `bot/fuzz-corpus-26495740813` | main | https://github.com/li-langverse/lic/pull/452 |
| lic | `bot/fuzz-corpus-26559158116` | main | https://github.com/li-langverse/lic/pull/453 |

All PR bodies include `<!-- li-agent -->` and the standard **Agent deliverable** checklist.

### Skipped (this run)

| Reason | Count | Examples |
|--------|------:|----------|
| Not selected (6/6 quota used) | 60 | `chore/agent-*`, remaining `bot/fuzz-corpus-*`, `cursor/*`, cross-repo feature branches |
| Already has open PR | 0 | — |
| Empty vs base / merge-only | 0 | — |

### Errors

None.

## Recommended issues/PRs

**Next opener pass (high signal, no PR yet):**

| Repo | Branch | Ahead | Suggested focus |
|------|--------|------:|-----------------|
| lic | `chore/agent-bench_improver-42289450` | 2 | PH-5b / tier-1 bench improver |
| lic | `chore/agent-autoresearch-1780094804882-digest` | 1 | autoresearch agent digest |
| lip | `cursor/sync-def-syntax-57b4` | 1 | def-syntax sync |
| lit | `cursor/sync-def-syntax-57b4` | 1 | def-syntax sync |
| lis | `cursor/wp-g-ph-db-ci` | 2 | PH-DB CI wiring |
| lis | `feat/production-registry-docs` | 2 | production registry docs |

**Opened this run — label for alignment (`pr_alignment`):**

| PR | Labels to add (human/agent) |
|----|----------------------------|
| [lic#448–453](https://github.com/li-langverse/lic/pulls) | `plan-needed` or bot/automation policy; verify fuzz corpus diff only |

## Deferred

- **54+** remaining `bot/fuzz-corpus-*` and `bot/nightly-*` branches — confirm batch bot workflow vs individual PRs.
- **60** feature/agent branches not opened (6/6 quota used on fuzz corpus head of list).
- **pr_alignment:** 10 draft PRs recommended for close/supersede per hygiene — separate agent pass.
- **li-language** large feature stacks — defer until Vision-LLM / PH-DB stack lands or human triage.
