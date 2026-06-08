# PR branch opener digest — 2026-05-30T15:29Z (proactive run)

**Agent:** `pr_branch_opener` · **Run:** `pr_branch_opener-1780153770649` · **Source:** proactive  
**North star:** proof → easy → fast · **PH context:** Phase 2i (linalg), PH-DB-0/4 (lidb/lip), Phase 2f provability, HPC competitive intel  
**Preflight:** `pr-branch-hygiene.json` @ 2026-05-30T15:29Z (12 repos, 0 branches needing PR) · **merge_plan / pr_program:** stale @ 15:07–15:09Z (`open_prs=0` — REST exhausted; ~92 open PRs via `gh pr list`)

## Executive summary

- Refreshed `pr-branch-hygiene.py` across **12 org repos**; hygiene reports **0** branches ahead of default without an open PR (down from 139 at 14:56Z after prior opener pass).
- **0 PRs opened** this run — no orphan feature branches in scope; duplicate check not required.
- Prior opener pass (14:58Z) opened **6** PRs (lip#46–48, roadmap#48, li-language#20–21); `pr_alignment` applied `plan-needed` labels at 15:15Z.
- **16** draft PRs flagged for human close review (11 lic, 4 benchmarks, 1 roadmap); **`prs_safe_close_now: 0`** — no auto-closes.
- `pr-merge-queue-plan.py` / `run-pr-program.py` **hung >5m** (REST rate limit); used existing merge_plan snapshot + live `gh pr list` counts.
- No merges, no `merge-approved`, no pushes to protected defaults.
- Route existing open PRs to **`pr_alignment`** before merge queue; opener quota unused.

## Deliverable / findings

### Branches opened

None this run.

| Repo | Branch | Base | PR |
|------|--------|------|-----|
| — | — | — | — |

### Skipped

| Reason | Count | Detail |
|--------|------:|--------|
| No branches needing PR (hygiene empty) | 12 repos | All scanned remote branches either have open PRs or are not ahead of default |
| Already opened (prior run 14:58Z) | 6 | lip#46–48, roadmap#48, li-language#20–21 |
| Empty vs base / merge-only | 0 | — |
| Permission error | 0 | — |
| Quota unused (0/6) | — | No candidates to open |

### Errors

```
pr-merge-queue-plan.py and run-pr-program.py did not complete within 5m (background shell 623055 / 233563).
Likely cause: GitHub REST API rate limit exhausted (core 0/5000 per pr-alignment digest 15:15Z).
Existing merge_plan @ 2026-05-30T15:09Z reports open_prs=0 while live counts show:
  lip=4, li-language=8, roadmap=10, lic=30, benchmarks=30, lis=10 (92 sampled).
Workaround: pr-branch-hygiene.py completed successfully via gh API; no PR create attempted.
```

## Recommended issues/PRs

**Opened earlier today — route to `pr_alignment` (labels applied):**

| PR | Repo | Focus | Labels |
|----|------|-------|--------|
| [#46–48](https://github.com/li-langverse/lip/pulls) | lip | PH-DB-4 publish/registry/e2e | `plan-needed`, PH-DB-4 |
| [#48](https://github.com/li-langverse/roadmap/pull/48) | roadmap | PH-DB-0 lidb proposal | `plan-needed`, PH-DB-0 |
| [#20](https://github.com/li-langverse/li-language/pull/20) | li-language | HPC competitive intel | `plan-needed`, HPC |
| [#21](https://github.com/li-langverse/li-language/pull/21) | li-language | Phase 2f discharge corpus | `plan-needed`, Phase-2f |

**Hygiene close candidates (human confirm — not acted on):**

| Repo | PRs | Reason |
|------|-----|--------|
| lic | #430–#432, #530–#532, #536–#540 | draft — confirm abandoned; **#530–#532** carry `merge-approved` |
| benchmarks | #182, #183, #209, #230 | draft — confirm abandoned |
| roadmap | #26 | draft — confirm abandoned |

**Next opener pass (when hygiene repopulates):**

| Repo | Branch | Notes |
|------|--------|-------|
| benchmarks | `chore/agent-docs_ui_tester-proactive-20260530T1408Z-digest` | current agent digest branch (if pushed ahead of main) |
| li-language | remaining `feat/*` stacks | only if REST-verified no open PR |

## Deferred

- **Merge plan refresh:** re-run `pr-merge-queue-plan.py` and `run-pr-program.py` after REST rate limit reset (~15:18Z UTC per prior alignment run).
- **Draft PR cleanup (16):** defer to `pr_alignment` with human confirmation; never close `merge-approved` drafts (#530–#532).
- **Hygiene pagination:** `--limit 50` on `gh pr list` may miss heads when repo has >50 open PRs (lic=30, benchmarks=30) — monitor for false positives on future passes.
- **133+ historical hygiene rows:** cleared by 14:58Z opener batch; re-scan after new feature branch pushes.
