# PR reviewer digest — 2026-05-30T10:51Z

**Agent:** `pr_reviewer` · **Run id:** `pr_reviewer-1780138247551` · **Source:** proactive ecosystem sweep · **north_star_fit:** platform CI + tier-1 numerics (PH-5b, PH-7e, Phase 2i/7e) — proof → easy → fast

## Executive summary

- **Preflight refreshed:** `pr-merge-queue-plan.json` and `pr-program-run.json` at 10:51Z report **`open_prs=0`** — GraphQL enumeration starved; REST search shows **239 open** org PRs (false empty in gate scripts).
- **P0 queue cleared:** [lip#32](https://github.com/li-langverse/lip/pull/32), [lit#18](https://github.com/li-langverse/lit/pull/18), [li-net#12](https://github.com/li-langverse/li-net/pull/12), [lic-docs#1](https://github.com/li-langverse/lic-docs/pull/1) **merged** since 09:56Z pass.
- **New P0:** [lip#35](https://github.com/li-langverse/lip/pull/35) — CI green, platform LLVM 22 + Pages deploy; **`merge-approved` added** this run; needs human **APPROVED** → pr_merger.
- **Best numerics candidate:** [lic#524](https://github.com/li-langverse/lic/pull/524) — tier-1 `matmul_blocked` harness, release notes, CI green; **defer `merge-approved`** until [lic#499](https://github.com/li-langverse/lic/pull/499) MIR restore is green (stack order).
- **Numerics canonical blocked:** lic#499 — `build-and-test` **failure** (2 failing checks); do not weaken `catalog.toml` (6 red bench rows in briefing).
- **Infra priority:** [benchmarks#215](https://github.com/li-langverse/benchmarks/pull/215) — GraphQL CI fallback for ecosystem-audit; CI green but **merge conflicts** — resolve before review.
- **Feature gates:** [lic#517](https://github.com/li-langverse/lic/pull/517) (PH-7d GPU), [lic#495](https://github.com/li-langverse/lic/pull/495) (CAD v1) — `plan-needed` / no `plan-approved`; CI fail or plan block.
- **Error (non-fatal):** GraphQL quota exhausted — `pr-merge-gate.py` returns `pr_not_found`; REST `gh api` used for this digest.

## Deliverable / findings

### Preflight artifacts

| Artifact | `generated_at` | Signal |
|----------|----------------|--------|
| `pr-merge-queue-plan.json` | 2026-05-30T10:51Z | Empty `merge_sequence`; `open_prs=0` ⚠️ GraphQL artifact |
| `pr-program-run.json` | 2026-05-30T10:51Z | `all_open=[]`, `ci_green=0` ⚠️ same |
| `pr-branch-hygiene.json` | 2026-05-30T09:35Z | 11 draft PRs → close candidates, **`safe_now=0`** |
| `ecosystem-audit.json` | 2026-05-30T10:42Z | Bench red: `matmul_blocked` 1.55×, `matmul_naive` 1.33×, ML×3, `num_gmres` 1.4× |
| REST org search | 2026-05-30T10:51Z | **239 open** PRs (authoritative vs GraphQL scripts) |

### Standards checklist (REST-verified CI-green sample)

| PR | Vision / PH | Strict / proof | Security | Performance | Release notes | Verdict |
|----|-------------|----------------|----------|-------------|---------------|---------|
| lip#35 | Platform CI | chore | N/A | N/A | waive (chore) | **aligned** — `merge-approved` **added** |
| lic#524 | PH-5b, PH-7e | Harness only | N/A | Evidence ≤1.2× local | ✅ release-notes | **aligned, defer** (after #499) |
| lic#499 | PH-5b, PH-7e | MIR restore | N/A | Bench evidence | ✅ study doc | **aligned, CI red** |
| benchmarks#215 | Ecosystem CI | Audit fix | N/A | N/A | Digest only | **aligned, conflicts** |
| benchmarks#221 | Workspace sweep | chore | N/A | N/A | waive | **aligned** — low priority chore |
| lic#495 | PH-CAD | Feature | TBD | N/A | likely yes | **needs plan** — `plan-needed` |
| lic#517 | PH-7d | Feature | review surface | N/A | TBD | **needs plan** — CI fail + conflicts |
| li-std-* #11–12, li-httpd#17, li-net#15 | Docs / Pages | chore | N/A | N/A | docs | **defer** — merge conflicts, no CI |

### Gate script

```text
pr-merge-gate.py (GraphQL): pr_not_found for lic#524, lic#499, benchmarks#215
REST verification:
  lip#35:   merge-approved ✓ (added)  CI_GREEN  mergeable true
  lic#524:  no label  CI_GREEN  mergeable unknown
  lic#499:  numerics-research  CI_FAIL
  benchmarks#215:  CI_GREEN  mergeable false (conflicts)
```

### Actions taken

| Action | Target | Result |
|--------|--------|--------|
| Review comment + checklist | [lip#35](https://github.com/li-langverse/lip/pull/35#issuecomment-4582583983) | Posted |
| Label `merge-approved` | [lip#35](https://github.com/li-langverse/lip/pull/35) | **Added** |
| Label `merge-approved` | lic#524, benchmarks#215 | **Deferred** (stack / conflicts) |
| Merge | — | **None** (pr_reviewer mandate) |

## Recommended issues/PRs

| Priority | Repo | Item | Labels / next step |
|----------|------|------|-------------------|
| P0 | lip | [#35](https://github.com/li-langverse/lip/pull/35) fix(ci) LLVM 22 + Pages | `merge-approved` — **human APPROVED** → pr_merger |
| P1 | lic | [#499](https://github.com/li-langverse/lic/pull/499) matmul MIR restore | Fix `build-and-test` → pr-review-agent |
| P1 | lic | [#524](https://github.com/li-langverse/lic/pull/524) matmul_blocked harness | After #499 green; then `merge-approved` |
| P1 | benchmarks | [#215](https://github.com/li-langverse/benchmarks/pull/215) ecosystem-audit GraphQL fallback | Resolve conflicts → review → `merge-approved` |
| P2 | lic | [#495](https://github.com/li-langverse/lic/pull/495) CAD v1 | `plan-approved` required |
| P2 | lic | [#517](https://github.com/li-langverse/lic/pull/517) GPU decorators | `plan-approved` + fix CI |
| P2 | li-std-core, li-std-math, li-httpd, li-net | Docs Pages PRs #11–17 | Resolve conflicts; trigger CI |
| Hygiene | org | 11 draft PRs (lic#430–432, benchmarks#128–209, roadmap#26) | Human confirm abandoned → close |
| Governance | roadmap | [#43–45](https://github.com/li-langverse/roadmap/pulls) | **Human merge only** |

## Deferred

- Full `run-pr-program.py` org enumeration until **GraphQL rate limit resets**.
- `merge-approved` on lic#524 until lic#499 is CI green (stack order per pr_alignment).
- **Merge execution** — pr_merger only after `reviewDecision: APPROVED`.
- **roadmap** / governance repos — human merge per policy.
- Re-run `pr-merge-gate.py --json` on lip#35 after GraphQL recovery for authoritative `ready: true`.
- Docs maintainer wave (lic#529–534, benchmarks#216–221) — dedupe after platform/numerics land.

## Error

**GitHub GraphQL rate limit exhausted** (`GraphQL: API rate limit already exceeded for user ID 207167228`) during `gh pr list` and `pr-merge-gate.py`. Symptom: preflight scripts report `open_prs=0`; gate returns `pr_not_found`. **Mitigation:** REST `gh api` / search API used for this digest. **Stack trace:** N/A (API 403 on GraphQL, not Python exception).
