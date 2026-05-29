# PR branch opener digest — 2026-05-29T23:31Z (run 5)

**Agent:** `pr_branch_opener` · **Queued:** `rec:pr_branch_opener:dcef3d6b86696dfaed9f` · **North star:** proof → easy → fast · **PH context:** PH-DB (lis hosting), PH-5b (fuzz corpus) · **Preflight:** `pr-branch-hygiene.json` @ 2026-05-29T23:30Z (60 branches needing PR, 12 repos scanned) · **merge_plan / pr_program:** open_prs=0, merge_approved=0

## Executive summary

- Refreshed `pr-branch-hygiene.py`: **60** branches ahead of default with no open PR (down from 132 in briefing snapshot).
- Opened **6** PRs this run (cap); **0** errors; duplicate check via `gh pr list --head … --state open`.
- **1** cross-repo feature PR (`lis` PH-DB hosting) plus **5** `lic` automation/agent branches from hygiene list head.
- **54** branches remain without open PR for a future opener pass.
- **10** draft PRs flagged for close/supersede in hygiene (`prs_recommended_close`); route to `pr_alignment` — not touched here.
- Several high-signal branches have **closed** (not open) PRs — hygiene still lists them; reopen or supersede in next pass.
- No merges, no `merge-approved`, no pushes to protected defaults.

## Deliverable / findings

### Branches opened

| Repo | Branch | Base | PR |
|------|--------|------|-----|
| lis | `cursor/wp-i-ph-db-lis-service` | main | https://github.com/li-langverse/lis/pull/20 |
| lic | `bot/fuzz-corpus-26622519464` | main | https://github.com/li-langverse/lic/pull/454 |
| lic | `chore/agent-autoresearch-1780082345386` | main | https://github.com/li-langverse/lic/pull/455 |
| lic | `chore/agent-autoresearch-1780083426193` | main | https://github.com/li-langverse/lic/pull/456 |
| lic | `chore/agent-autoresearch-1780084678496` | main | https://github.com/li-langverse/lic/pull/457 |
| lic | `chore/agent-autoresearch-1780094804882-digest` | main | https://github.com/li-langverse/lic/pull/458 |

All PR bodies include `<!-- li-agent -->` and the standard **Agent deliverable** checklist.

### Skipped (this run)

| Reason | Count | Examples |
|--------|------:|----------|
| Not selected (6/6 quota used) | 54 | remaining `chore/agent-bench_improver-*`, `cursor/sync-def-syntax-*`, `ci/pin-lic-main`, `li-language/feat/*` |
| Closed PR exists (no open PR) | 5 | `lis/feat/production-registry-docs` (#11 closed), `roadmap/feat/ecosystem-overview-stats` (#12), `roadmap/chore/ph-db-status-refresh` (#24), `li-language/feat/goal-scaffold-v1-docs` (#8), `roadmap/feat/org-ci-branch-protection` (#7) |
| Already has open PR | 0 | — |
| Empty vs base / merge-only | 0 | — |
| Permission error | 0 | — |

### Errors

None.

## Recommended issues/PRs

**Next opener pass (high signal, no open PR):**

| Repo | Branch | Ahead | Suggested focus |
|------|--------|------:|-----------------|
| lis | `feat/production-registry-docs` | 2 | PH-DB-4 — reopen or supersede closed #11 |
| lis | `cursor/wp-g-ph-db-ci` | 2 | PH-DB WP-G cross-repo gate |
| lis | `cursor/wp-h-ph-db-containers` | 2 | PH-DB WP-H containers |
| roadmap | `feat/ecosystem-overview-stats` | 3 | ecosystem Pages stats — reopen #12 |
| li-language | `feat/goal-scaffold-v1-docs` | 16 | ecosystem scaffolds — reopen #8 |
| lic | `chore/agent-bench_improver-42289450` | 2 | PH-5b tier-1 bench improver |

**Opened this run — label for alignment (`pr_alignment`):**

| PR | Labels to add (human/agent) |
|----|----------------------------|
| [lis#20](https://github.com/li-langverse/lis/pull/20) | `plan-approved`, PH-DB traceability |
| [lic#454–458](https://github.com/li-langverse/lic/pulls) | `plan-needed` or bot/automation policy; verify fuzz corpus / agent digest diffs only |

## Deferred

- **54** remaining branches without open PR (6/6 quota used).
- **5** branches with closed-only PRs — human triage: reopen vs supersede vs close branch.
- **pr_alignment:** 10 draft PRs recommended for close/supersede per hygiene — separate agent pass.
- **li-language** large feature stacks (`feat/composable-by-default`, `feat/tier2-physics-suite-expansion`, etc.) — defer until Vision-LLM / PH-DB stack lands or human triage.
