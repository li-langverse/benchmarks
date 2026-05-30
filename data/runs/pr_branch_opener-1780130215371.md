# PR branch opener digest — 2026-05-30

**Agent:** `pr_branch_opener` · **Source:** recommended · **Run:** `pr_branch_opener-1780130215371` · **North star:** proof → easy → fast (platform PH-db lanes)

## Executive summary

- **Preflight:** `pr-branch-hygiene.py` OK — **39** branches needing PR (down from briefing **133**; stale `--skip-slow` count).
- **Opened 6 PRs** (max/run) — all **lis** PH-db / cursor work branches → [#25](https://github.com/li-langverse/lis/pull/25)–[#30](https://github.com/li-langverse/lis/pull/30).
- **Skipped 2** — **lic** bench_improver branches already had open PRs ([#380](https://github.com/li-langverse/lic/pull/380), [#388](https://github.com/li-langverse/lic/pull/388)); `gh pr view --head` false negative, `gh pr create` caught duplicate.
- **Remaining backlog:** **33** branches still without PR per fresh hygiene JSON.
- **No merge** — governance PRs for human review only.
- **merge_plan / pr_program:** 0 open PRs in briefing snapshot (may be stale); alignment pass still recommended after GraphQL reset.
- **north_star_fit:** domain=platform · PH-db (lis bundle/registry/CI/containers) · pillars: secure, provable

## Deliverable / findings

### Preflight

| Artifact | Value |
|----------|-------|
| `pr-branch-hygiene.json` | `2026-05-30T08:46Z`, 12 repos, **39** `branches_needing_pr` |
| `merge_plan` | `open_prs=0` (briefing) |
| `pr_program` | `open_prs=0` (briefing) |

### Branches opened

| Repo | Branch | Base | PR |
|------|--------|------|-----|
| lis | `cursor/wp-b-ph-db-3-lis-db` | main | https://github.com/li-langverse/lis/pull/25 |
| lis | `cursor/wp-g-ph-db-ci` | main | https://github.com/li-langverse/lis/pull/26 |
| lis | `cursor/wp-h-ph-db-containers` | main | https://github.com/li-langverse/lis/pull/27 |
| lis | `feat/ph-db-3-lis-bundle-stub` | main | https://github.com/li-langverse/lis/pull/28 |
| lis | `feat/ph-db-4-lidb-liorm-wire` | main | https://github.com/li-langverse/lis/pull/29 |
| lis | `feat/ph-db-4-registry-routes` | main | https://github.com/li-langverse/lis/pull/30 |

PR bodies include `<!-- li-agent -->` and **Agent deliverable** checklist.

### Skipped

| Repo | Branch | Reason |
|------|--------|--------|
| lic | `chore/agent-bench_improver-41443459` | PR already exists → [#380](https://github.com/li-langverse/lic/pull/380) |
| lic | `chore/agent-bench_improver-50434717` | PR already exists → [#388](https://github.com/li-langverse/lic/pull/388) |

### Errors

None blocking. Duplicate-create stderr on lic branches is expected when hygiene scan lags merged/open PR state.

## Recommended issues/PRs

| Priority | Repo | Item | Labels / action |
|----------|------|------|-----------------|
| P1 | lis | [#25](https://github.com/li-langverse/lis/pull/25)–[#30](https://github.com/li-langverse/lis/pull/30) | `plan-needed` until PH-db scope reviewed; verify CI |
| P2 | roadmap | `fix/live-development-overview`, `chore/ph-db-status-refresh` | Next opener batch (governance) |
| P2 | benchmarks | `chore/agent-*-digest` branches (14–39 ahead) | Opener batch after lis wave |
| hygiene | lic | `bench/improver-matmul-tier1-*` + agent chore branches | Re-run hygiene; many may already have PRs |
| align | org | Open PRs vs `merge_first` | `pr_alignment` after GraphQL reset |

## Deferred

- **33** remaining `branches_needing_pr` — next `pr_branch_opener` run (6/run cap).
- **bot/nightly-summary-*** — skip or automate separately (not opened).
- **benchmarks** digest branches (`chore/agent-autoresearch-*`, agent_kit_maintainer) — defer until lis PH-db stack reviewed.
- **roadmap** `fix/pages-progress-root`, agent-kit sync — human governance review.
- Reconcile hygiene false negatives (`gh pr view --head` vs `gh pr create` duplicate detection).
- **133** count in stale briefing — ignore; use `data/latest/pr-branch-hygiene.json`.

**north_star_fit:** domain=platform · PH-db · PKG lis bundle/registry
