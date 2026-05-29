# PR alignment digest — 2026-05-29

**Agent:** `pr_alignment` · **North star:** proof → easy → fast (platform hygiene before lic feature stacks)

## Executive summary

- Preflight completed: `pr-merge-queue-plan.py`, `pr-branch-hygiene.py`, `run-pr-program.py`, `issue-feature-triage.py` (≈11 min).
- **Queued PR `li-httpd#13`:** **aligned** — rank-1 mirror-tier agent-kit sync; CI green; `merge-approved`; blocked on GitHub review approval only.
- Reviewed **8** PRs from merge-order ranks 1–8; **5 aligned**, **1 needs plan**, **1 defer (CI)**, **1 wait (merge-approved pending)**.
- **0** PRs closed (`prs_safe_close_now: 0`); no supersede closes this run.
- **10** PRs flagged for future close review (drafts + `lic#376` after `#384`); all `safe_now: false`.
- `benchmarks#131` superseded by `#132` — **defer close** until `#132` merges.
- Posted alignment comments: **li-httpd#13**, **li-httpd#10**.
- **No merges**; did not add `merge-approved` (pr-review-agent scope).

## Deliverable / findings

### li-httpd#13 (queued)

| Check | Result |
|-------|--------|
| Feature without plan? | No — chore agent-kit |
| Redundant / superseded? | No |
| Merge order | Rank 1 ✓ (httpd before benchmarks/lic) |
| Title/body vs scope | Minor: body cites 1.3.4, branch at 1.3.5 |
| Traceability | Swarm `agent_kit_maintainer`; N/A PH |
| Duplicate? | No (`#10` is separate feature stack) |
| **Verdict** | **aligned** |

Comment: https://github.com/li-langverse/li-httpd/pull/13#issuecomment-4573989891

### Top 8 merge-order PRs

| PR | Verdict | Notes |
|----|---------|-------|
| li-httpd#13 | aligned | See above |
| li-net#12 | aligned | Same agent-kit wave; CI green; `merge-approved`; review required |
| li-demo#15 | defer | CI fail; no `merge-approved` |
| li-std-core#8 | aligned | Agent-kit; CI green; review required |
| li-std-math#9 | aligned | Agent-kit; CI green; review required |
| benchmarks#134 | wait | Tier-1 matmul fix; needs `merge-approved` after review |
| lic#369 | wait | Agent-kit 1.3.5 rule; no `merge-approved` yet |
| lic#373 | wait | Agent-kit studio worktree; no `merge-approved` |

### li-httpd#10 (feature, not in top-8)

- **needs plan** — `feat(li-net-httpd)` without `plan-approved`; merge after #13 + lic plan-loop.
- Comment: https://github.com/li-langverse/li-httpd/pull/10#issuecomment-4574005051

### Hygiene / redundant (no action)

- `prs_recommended_close`: 10 (drafts + `lic#376` ⊂ `#384`); **`safe_now: 0`**
- `merge_sequence`: empty (no `gate_ready` PRs)
- 14 redundant lic/benchmarks pairs — human pick/rebase; do not auto-close

## Recommended issues/PRs

| Repo | PR / issue | Labels / action |
|------|------------|-----------------|
| li-httpd | [#13](https://github.com/li-langverse/li-httpd/pull/13) | `merge-approved` → **pr-review-agent** / human APPROVED |
| li-net | [#12](https://github.com/li-langverse/li-net/pull/12) | Same hygiene wave after #13 |
| li-std-core | [#8](https://github.com/li-langverse/li-std-core/pull/8) | Agent-kit sync |
| li-std-math | [#9](https://github.com/li-langverse/li-std-math/pull/9) | Agent-kit sync |
| benchmarks | [#132](https://github.com/li-langverse/benchmarks/pull/132) | Merge before closing #131 |
| benchmarks | [#134](https://github.com/li-langverse/benchmarks/pull/134) | Add `merge-approved` after tier-1 review |
| li-httpd | [#10](https://github.com/li-langverse/li-httpd/pull/10) | **plan-needed** / `plan-approved` + fix CI |
| lic | [#376](https://github.com/li-langverse/lic/pull/376) | Close after #384 merges (not now) |

## Deferred

- **benchmarks#131** — close after **#132** merges (redundant overlap).
- **Draft PRs** (lic#364–365, benchmarks#123–128,135–137, roadmap#26) — confirm abandoned before close.
- **lic studio stack** (#376→#377, #384 vs #375/#376) — human resolution.
- **li-demo#15** — fix CI before alignment re-check.
- **All gate-ready merges** — blocked on `REVIEW_REQUIRED` across hygiene wave.
