# PR alignment digest — 2026-05-30T12:50Z

**Agent:** `pr_alignment` · **Source:** proactive ecosystem sweep · **North star:** proof → easy → fast (PH-5b, PH-7e, Phase 2i, PH-H httpd)

## Executive summary

- **130 open org PRs** (`ecosystem-audit.json`); merge-queue JSON lists **7** mirror-tier rows — **3 li-demo PRs already closed** since plan generation; REST confirms **4 active queue rows** + **li-net#15** (same docs wave, missing from stale plan).
- **GraphQL rate limit exhausted** during run (`remaining: 0`); alignment comments posted via **REST API**; `gh pr view --json` and label edits via GraphQL failed until REST fallback.
- **Package docs wave aligned:** [li-httpd#17](https://github.com/li-langverse/li-httpd/pull/17), [li-std-core#11](https://github.com/li-langverse/li-std-core/pull/11), [li-std-math#12](https://github.com/li-langverse/li-std-math/pull/12), [li-net#15](https://github.com/li-langverse/li-net/pull/15) — docs_maintainer deliverables; **aligned**, await CI.
- **Httpd feature stack blocked:** [lic#489](https://github.com/li-langverse/lic/pull/489) → [li-httpd#10](https://github.com/li-langverse/li-httpd/pull/10); both **`plan-needed`**; #10 CI red; prior alignment comment on #10 stands.
- **Numerics canonical unchanged:** [lic#499](https://github.com/li-langverse/lic/pull/499) (`numerics-research`) — **aligned, defer** until `build-and-test` green; duplicate matmul stack (#503, #528, #541, #543) not auto-closed (human pick).
- **Feature needs plan:** [lic#517](https://github.com/li-langverse/lic/pull/517) PH-7d GPU decorators — **`plan-needed`** added; prior alignment comment stands.
- **Redundant pair resolved:** li-demo#16 vs #17 (100% overlap) — **both closed**; no close action this run.
- **No merges, no `merge-approved`** (alignment agent mandate); **0 PRs closed** (`prs_safe_close_now=0`).

## Deliverable / findings

### Preflight

| Artifact | `generated_at` | Key signal |
|----------|----------------|------------|
| `pr-merge-queue-plan.json` | 2026-05-30T12:09Z | 7 rows; 3 closed; `merge_sequence=[]`; 1 redundant pair (li-demo) |
| `pr-program-run.json` | 2026-05-30T12:05Z | `all_open=[]` (stale; full `run-pr-program.py` >5m, in flight at digest time) |
| `pr-branch-hygiene.json` | 2026-05-30T12:03Z | 147 branches without PR; `prs_recommended_close=0`, `prs_safe_close_now=0` |
| `issue-feature-triage.json` | 2026-05-30T12:44Z | `needs_plan=42` (lic), 3 candidates |
| `ecosystem-audit.json` | 2026-05-30T12:44Z | `open_prs=130`, `ready_prs=28`, `failed_prs=33` |

**Error (non-fatal):** GitHub GraphQL rate limit blocked `gh pr view`, `gh pr comment`, and `gh pr edit` for part of the run. REST `gh api` succeeded for PR bodies, checks, comments, and labels.

### Per-PR alignment (8 reviewed)

| PR | Plan | PH / PKG | Merge order | Verdict | Action |
|----|------|----------|-------------|---------|--------|
| [li-httpd#10](https://github.com/li-langverse/li-httpd/pull/10) | **needs plan** | PH-H httpd, li-net-httpd mirror | Rank 2; after lic#489 | wait for dependency | `plan-needed` label; prior comment |
| [li-httpd#17](https://github.com/li-langverse/li-httpd/pull/17) | Docs hygiene | PH-Pkg live docs | Rank 3 | aligned | Alignment comment |
| [li-std-core#11](https://github.com/li-langverse/li-std-core/pull/11) | Docs hygiene | PH-Pkg | Rank 6 | aligned | Alignment comment |
| [li-std-math#12](https://github.com/li-langverse/li-std-math/pull/12) | Docs hygiene | PH-Pkg / 2i surface | Rank 7 | aligned | Alignment comment |
| [li-net#15](https://github.com/li-langverse/li-net/pull/15) | Docs hygiene | PH-Pkg | Package tier batch | aligned | Alignment comment |
| [lic#489](https://github.com/li-langverse/lic/pull/489) | **needs plan** | PH-H httpd (#477) | Before li-httpd#10 | needs plan | Comment + `plan-needed` |
| [lic#499](https://github.com/li-langverse/lic/pull/499) | Bench fix | PH-5b, PH-7e | After package wave | aligned, **defer** (CI red) | Prior comments stand |
| [lic#517](https://github.com/li-langverse/lic/pull/517) | **needs plan** | PH-7d, G-par | After lic core | needs plan | `plan-needed` label; prior comment |

### Closed / superseded (no action)

| PR | Status | Note |
|----|--------|------|
| li-demo#15, #16, #17 | **closed** | Merge-queue stale; redundant #16/#17 overlap moot |

### north_star_fit

- **Domain:** Ecosystem packaging + live docs (easy); httpd mirror (PH-H); tier-1 numerics (PH-5b/7e).
- **PH ids:** PH-Pkg governance, PH-H httpd (#477), PH-5b, PH-7e, Phase 2i partial.
- **Proof-before-perf:** lic#517 and httpd stacks blocked on plan gate; no merge-approved added.

## Recommended issues/PRs

| Priority | Repo | Item | Labels / notes |
|----------|------|------|----------------|
| P1 | lic | [#489](https://github.com/li-langverse/lic/pull/489) httpd plan-loop integration | `plan-needed` — unblock li-httpd#10 |
| P1 | li-httpd | [#10](https://github.com/li-langverse/li-httpd/pull/10) mirror split | `plan-needed`, CI fail — after lic#489 |
| P2 | li-httpd / li-std-* / li-net | [#17](https://github.com/li-langverse/li-httpd/pull/17), [#11](https://github.com/li-langverse/li-std-core/pull/11), [#12](https://github.com/li-langverse/li-std-math/pull/12), [#15](https://github.com/li-langverse/li-net/pull/15) | Package docs batch → pr-review-agent |
| P2 | lic | [#499](https://github.com/li-langverse/lic/pull/499) matmul MIR restore | `numerics-research` — fix CI, then pr-review-agent |
| P2 | lic | [#517](https://github.com/li-langverse/lic/pull/517) GPU decorators | `plan-needed` — plan-approved required |
| P2 | lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | `plan-needed` (unchanged) |
| P3 | roadmap | [#19](https://github.com/li-langverse/roadmap/pull/19), [#21](https://github.com/li-langverse/roadmap/pull/21) | `merge-approved` — human merge only |
| Hygiene | org | 147 branches without PR | `pr_branch_opener` backlog |
| Governance | lic | [#476](https://github.com/li-langverse/lic/issues/476) PH-Pkg governance | `plan-needed` |

## Deferred

- Full `run-pr-program.py` completion (org-scale gate enrichment; GraphQL-limited).
- Refresh `pr-merge-queue-plan.json` after GraphQL reset — current file under-counts lic/lip stacks.
- Matmul duplicate stack (#503, #514, #516, #528, #541, #543 vs canonical #499) — human dedupe after #499 CI green.
- **benchmarks** agent digest / workspace-sweep PR backlog — not in mirror merge queue; separate hygiene pass.
- **roadmap** merge-approved PRs — never auto-close; human merge only.
- Adding `merge-approved` — **pr-review-agent** only.
- **Merge execution** — **pr_merger** after human APPROVED.

## Actions log

| Action | Target |
|--------|--------|
| Alignment comment (REST) | li-httpd#17, li-std-core#11, li-std-math#12, li-net#15, lic#489 |
| Label `plan-needed` | li-httpd#10, lic#489, lic#517 |
| Closed | none (0/5 quota) |
