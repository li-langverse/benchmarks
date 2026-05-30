# PR reviewer digest — 2026-05-30T09:05Z

**Agent:** `pr_reviewer` · **Source:** proactive ecosystem sweep · **Run:** `pr_reviewer-1780131661769` · **North star:** proof → easy → fast (PH-5b, PH-7e, Phase 2i)

## Executive summary

- **172 open org PRs**, **73 CI-green** (`ecosystem-audit.json` @ 09:02Z); **47 CI-red** — no PR verified `ready: true` via `pr-merge-gate.py` this tick.
- **Error (GraphQL):** GitHub API rate limit exceeded for org token — `gh pr list` / merge-plan scripts return **`open_prs=0`** (silent empty); use REST (`gh api`, `gh search prs`) or retry after reset.
- **P0 human unblock:** [lip#32](https://github.com/li-langverse/lip/pull/32), [lit#18](https://github.com/li-langverse/lit/pull/18), [lic-docs#1](https://github.com/li-langverse/lic-docs/pull/1) — `merge-approved`, CI pass in audit, REST `mergeable_state: blocked` (needs **human APPROVED**).
- **Agent-kit wave:** [li-net#12](https://github.com/li-langverse/li-net/pull/12), [li-httpd#13](https://github.com/li-langverse/li-httpd/pull/13), [li-std-core#8](https://github.com/li-langverse/li-std-core/pull/8), [li-std-math#9](https://github.com/li-langverse/li-std-math/pull/9) — `merge-approved`, blocked on review; vision order before `lic`.
- **Numerics:** [lic#499](https://github.com/li-langverse/lic/pull/499) canonical matmul MIR (PH-5b/7e) — **CI fail**; do not add `merge-approved`. [lic#437](https://github.com/li-langverse/lic/pull/437) labeled `merge-approved` but **CONFLICTING** — rebase + dedupe vs #499 before merge.
- **Feature blocked:** [lic#495](https://github.com/li-langverse/lic/pull/495) CAD v1 — `plan-needed` without `plan-approved`; no `merge-approved`.
- **Hygiene:** ~18+ duplicate `chore(benchmarks): workspace sweep fallback` PRs (CI green) — close after canonical sweep; **133** branches without PR (briefing).
- **No new `merge-approved` labels**; **no merges**; **no PR comments** (rate limit + digest-only pass).

## Deliverable / findings

### Preflight

| Artifact | `generated_at` | Key signal |
|----------|----------------|------------|
| `pr-merge-queue-plan.json` | 2026-05-30T09:05Z | `open_prs=0` — **stale** (GraphQL rate limit) |
| `pr-program-run.json` | 2026-05-30T09:05Z | `ci_green=0`, `merge_first=null` — same root cause |
| `ecosystem-audit.json` | 2026-05-30T09:02Z | `open_prs=172`, `ready_prs=73`, `failed_prs=47` |

`pr-merge-queue-plan.py` + `run-pr-program.py` re-run succeeded but enumerated **zero** PRs because per-repo `gh pr list` hit GraphQL limits. Prior pass (08:45Z) gate probes remain directionally valid; REST spot-checks below.

### Error

```
GraphQL: API rate limit already exceeded for user ID 207167228.
```

Impact: merge-queue scripts, `pr-merge-gate.py` (`pr_not_found`), and bulk review comments blocked. **Mitigation:** wait for rate-limit reset; prefer `gh api repos/…/pulls/N` (REST) for P0 probes; stagger gate enrichment.

### Gate-ready status

**None confirmed.** Closest candidates (ecosystem-audit CI pass + labels; REST mergeable):

| Repo | PR | CI (audit) | `merge-approved` | Mergeable (REST) | Blockers |
|------|-----|------------|------------------|------------------|----------|
| lip | [#32](https://github.com/li-langverse/lip/pull/32) | pass | ✓ | clean, **blocked** | human `review_approved`; gate script N/A (rate limit) |
| lit | [#18](https://github.com/li-langverse/lit/pull/18) | pass | ✓ | clean, **blocked** | human approve |
| lic-docs | [#1](https://github.com/li-langverse/lic-docs/pull/1) | pass | ✓ | **clean** | human approve |
| li-net | [#12](https://github.com/li-langverse/li-net/pull/12) | pass | ✓ | clean, **blocked** | human approve |
| li-httpd | [#13](https://github.com/li-langverse/li-httpd/pull/13) | pass | ✓ | (not re-probed) | human approve |
| li-std-core | [#8](https://github.com/li-langverse/li-std-core/pull/8) | pass | ✓ | (not re-probed) | human approve |
| li-std-math | [#9](https://github.com/li-langverse/li-std-math/pull/9) | pass | ✓ | (not re-probed) | human approve |
| lic | [#437](https://github.com/li-langverse/lic/pull/437) | — | ✓ | **dirty** (conflicts) | resolve conflicts; reconcile vs #499 |
| benchmarks | [#132](https://github.com/li-langverse/benchmarks/pull/132) | (prior pass) | ✓ | CONFLICTING (08:45Z) | conflicts + release_notes |

### Checklist (sampled high-signal)

| Gate | lip/lit/lic-docs | lic#499 matmul | lic#495 CAD | Sweep PRs |
|------|------------------|----------------|-------------|-----------|
| Vision / PH | Ecosystem CI order (package before lic) | PH-5b, PH-7e in title/body | AL-4 / PH-CAD — **needs `plan-approved`** | N/A — close redundant |
| Strict by default | Workflow/scripts only | MIR fast-path restore | Types/doc stub | No trusted creep |
| Security | N/A | N/A | N/A | N/A |
| Performance | N/A | Tier-1 matmul — **do not weaken `catalog.toml`** | N/A | N/A |
| Release notes | `fix(ci)` — gate may false-negative | Evidence in PR body | N/A | Chore — skip if labeled |
| Ecosystem-first | `gh pr review --approve` + `pr_merger` | Fix CI first; alignment closed #504–#508 | Comment `plan-needed` path | Bulk close |

### Alignment verdicts

| PR | Verdict | Action path |
|----|---------|-------------|
| lip#32, lit#18, lic-docs#1 | **aligned** | Human approve → `pr_merger` |
| li-net#12 … li-std-math#9 | **aligned** | Same (after P0) |
| lic#437 | **aligned, blocked** | Rebase; verify not superseded by #499 |
| lic#499 | **aligned, defer** | Fix `build-and-test`; then request review |
| lic#495 | **needs plan** | Add `plan-approved`; no `merge-approved` |
| lic#509–#516, #503 | **superseded / defer** | Bench-improver stack — consolidate on #499 |
| benchmarks#196–#207 sweeps | **superseded** | Close duplicates |
| lic#517 Studio GPU | **defer** | CI fail; feature scope |
| roadmap#* | **governance** | Human merge only |

### Control-plane

- `pr_reviewer-1780131661769` **running**; prior ticks `error` (`unregistered_running_reconciled`) — concurrent swarm + GraphQL exhaustion.
- **Red bench rows (unchanged):** `matmul_blocked` 1.55×, `matmul_naive` 1.33×, ML suite 1.33×, `num_gmres` 1.4× vs cpp.

### north_star_fit

Numerics PH-5b/PH-7e (tier-1 matmul restoration); ecosystem CI ordering (lip/lit/lic-docs before lic); governance (`plan-needed` on CAD); platform agent-kit sync (easy, provable CI gates).

## Recommended issues/PRs

| Priority | Repo | PR / issue | Labels / notes |
|----------|------|------------|----------------|
| P0 | lip | [#32](https://github.com/li-langverse/lip/pull/32) fix(ci) LLVM 22 | `merge-approved` — **human approve** |
| P0 | lit | [#18](https://github.com/li-langverse/lit/pull/18) fix(ci) LLVM 22 | `merge-approved` — **human approve** |
| P0 | lic-docs | [#1](https://github.com/li-langverse/lic-docs/pull/1) org ci.yml | `merge-approved` — **human approve** |
| P1 | li-net, li-httpd, li-std-core, li-std-math | #12, #13, #8, #9 agent-kit sync | `merge-approved` — after P0 |
| P1 | lic | [#499](https://github.com/li-langverse/lic/pull/499) matmul MIR restore | `numerics-research` — fix CI, then review |
| P1 | lic | [#437](https://github.com/li-langverse/lic/pull/437) perf matmul | `merge-approved` — **rebase + approve** |
| P2 | benchmarks | [#132](https://github.com/li-langverse/benchmarks/pull/132) macOS tier profile | conflicts + release_notes |
| P2 | lic | [#463](https://github.com/li-langverse/lic/issues/463) tier-1 red benchmarks | master-plan-gap |
| Hygiene | benchmarks, lic | workspace sweep PRs | `superseded` — close stack |
| Hygiene | org | branches without PR | `pr_branch_opener` |
| Ops | — | GraphQL rate limit | Stagger `pr-merge-gate` / merge-plan refresh |

## Deferred

- Full org `run-pr-program.py` + `pr-merge-gate.py` enrichment until GraphQL reset.
- `plan_audit`, `pr_branch_hygiene`, `issue_hygiene` (`--skip-slow` in briefing).
- **roadmap** repo PRs — human merge only.
- **lic#500** PH-ML JobGraph, **lic#517** Studio GPU — CI fail / feature scope.
- **li-demo** docs PRs (#15–#18) — CI fail.
- **li-httpd#10** feature split — CI fail.
- Adding `merge-approved` to implementer-owned PRs (#499, #495, bench runs).
- Auto-merge — **`pr_merger`** after human APPROVED + conflict resolution.
- GitHub review comments this pass (rate limit).

---

**Actions this pass:** Refreshed `pr-merge-queue-plan.json` + `pr-program-run.json` (degraded enumeration). No labels, merges, or comments.
