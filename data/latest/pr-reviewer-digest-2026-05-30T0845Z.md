# PR reviewer digest — 2026-05-30T08:45Z

**Agent:** `pr_reviewer` · **Source:** proactive ecosystem sweep · **Run:** `pr_reviewer-1780130208229` · **North star:** proof → easy → fast (PH-5b, PH-7e, Phase 2i)

## Executive summary

- **166 open org PRs** (`ecosystem-audit.json`); **70 CI-green** (`ready_prs`); **47 CI-red** — no PR passes full `pr-merge-gate.py` (`ready: true`) this tick.
- **`merge_sequence` empty** — `pr-merge-queue-plan.json` reports 0 gate-ready auto-merge candidates; only **2** open PRs carry `merge-approved` in merge-queue repos (`lic#437`, `benchmarks#132`), both **CONFLICTING** + **REVIEW_REQUIRED**.
- **P0 human unblock:** Package/tooling wave already labeled — [lip#32](https://github.com/li-langverse/lip/pull/32), [lit#18](https://github.com/li-langverse/lit/pull/18), [lic-docs#1](https://github.com/li-langverse/lic-docs/pull/1), [li-net#12](https://github.com/li-langverse/li-net/pull/12), [li-httpd#13](https://github.com/li-langverse/li-httpd/pull/13), [li-std-core#8](https://github.com/li-langverse/li-std-core/pull/8), [li-std-math#9](https://github.com/li-langverse/li-std-math/pull/9) — CI green + `merge-approved`; **sole gate blocker:** `review_approved` (human APPROVED). `lip`/`lit` also flagged by gate for missing release notes (CI-only diff; consider `fix(ci)` chore exemption or one-line CHANGELOG).
- **Numerics (proof → fast):** [lic#437](https://github.com/li-langverse/lic/pull/437) PH-5b/7e matmul ≤1.2× — aligned, `merge-approved`, CI green, **merge conflicts** + review; supersession risk vs [lic#499](https://github.com/li-langverse/lic/pull/499) (CI **fail**, no label) and open bench-improver stack (#469, #504, #513).
- **Benchmark reds unchanged:** `matmul_blocked`, `matmul_naive`, ML forwards, `num_gmres` >1.2× cpp — do not weaken `catalog.toml`; land numerics on green CI only.
- **Feature defer:** [lic#495](https://github.com/li-langverse/lic/pull/495) CAD v1 — CI green but **`plan-needed` without `plan-approved`**; do not add `merge-approved`.
- **Hygiene:** ~18+ open `chore(benchmarks): workspace sweep fallback` PRs (CI green, no label) — redundant; close after canonical sweep. **133** branches without PR per briefing.
- **No new `merge-approved` labels** this pass (blockers on conflicts, review, plan, CI). **No merges** (pr_merger deferred).

## Deliverable / findings

### Preflight

| Artifact | `generated_at` | Key signal |
|----------|----------------|------------|
| `pr-merge-queue-plan.json` | 2026-05-30T08:07Z | `open_prs=0` in summary (plan script still enriching or stale; REST audit shows 166) |
| `pr-program-run.json` | 2026-05-30T07:59Z | `ci_green=0`, `merge_first=null` |
| `ecosystem-audit.json` | 2026-05-30T08:38Z | `open_prs=166`, `ready_prs=70`, `failed_prs=47` |

`pr-merge-queue-plan.py` + `run-pr-program.py` re-run **killed** after >5m (per-PR `pr-merge-gate` enrichment is slow at org scale). Gate probes below use targeted `pr-merge-gate.py --repo … --pr …`.

### Gate-ready status

**None.** Closest candidates:

| Repo | PR | CI | `merge-approved` | Mergeable | Blockers |
|------|-----|-----|------------------|-----------|----------|
| lip | [#32](https://github.com/li-langverse/lip/pull/32) | ✓ | ✓ | MERGEABLE | review; release_notes (gate) |
| lit | [#18](https://github.com/li-langverse/lit/pull/18) | ✓ | ✓ | MERGEABLE | review; release_notes (gate) |
| lic-docs | [#1](https://github.com/li-langverse/lic-docs/pull/1) | ✓ | ✓ | MERGEABLE | review |
| li-net | [#12](https://github.com/li-langverse/li-net/pull/12) | ✓ | ✓ | MERGEABLE | review |
| li-httpd | [#13](https://github.com/li-langverse/li-httpd/pull/13) | ✓ | ✓ | MERGEABLE | review |
| li-std-core | [#8](https://github.com/li-langverse/li-std-core/pull/8) | ✓ | ✓ | MERGEABLE | review |
| li-std-math | [#9](https://github.com/li-langverse/li-std-math/pull/9) | ✓ | ✓ | MERGEABLE | review |
| lic | [#437](https://github.com/li-langverse/lic/pull/437) | ✓ | ✓ | **CONFLICTING** | review; resolve conflicts (`resolve-merge-conflicts`) |
| benchmarks | [#132](https://github.com/li-langverse/benchmarks/pull/132) | ✓ | ✓ | **CONFLICTING** | review; release_notes |

### Checklist (sampled CI-green / high-signal)

| Gate | lip/lit/lic-docs/agent-kit | lic#437 matmul | lic#495 CAD | Agent digests (benchmarks) |
|------|---------------------------|----------------|---------------|----------------------------|
| Vision / PH | Ecosystem CI order (package before lic) | PH-5b, PH-7e cited in body | AL-4 / PH-CAD — needs `plan-approved` | N/A — close redundant |
| Strict by default | Workflow/scripts only | Codegen + bench evidence doc | Types/doc stub | No trusted creep |
| Security | N/A | N/A | N/A | N/A |
| Performance | N/A | Bench study + tier-1 check — **do not merge on conflict** | N/A | Do not weaken thresholds |
| Release notes | Gate false-negative on `fix(ci)`? | Study doc present | N/A | Missing — chore OK to skip if labeled chore |
| Ecosystem-first | Use `gh pr review --approve` + `pr_merger` | Rebase on `main`, dedupe vs #499 | Comment `plan-needed` path | Bulk close sweeps |

### Alignment verdicts (no GitHub comments posted — digest only)

| PR | Verdict | Action path |
|----|---------|-------------|
| lip#32, lit#18, lic-docs#1 | **aligned** | Human `gh pr review --approve`; `pr_merger` when gate green |
| li-net#12 … li-std-math#9 | **aligned** | Same (vision merge order: mirrors before lic) |
| lic#437 | **aligned, blocked** | Resolve conflicts; human approve; verify not superseded by #499 |
| lic#499 | **defer** | Fix CI (`build-and-test`); then review for `merge-approved` |
| lic#495 | **needs plan** | Add `plan-approved` or narrow scope; no `merge-approved` |
| lic#469, #504, #513 | **superseded / defer** | Bench-improver stack — consolidate before merge |
| benchmarks#197–#207 sweeps | **superseded** | Close duplicates; keep one canonical digest if any |
| roadmap#* | **governance** | Human merge only — never `pr-auto-merge` |

### Control-plane

- Concurrent `pr_reviewer` / `pr_merger` runs at 08:37Z (`running`); prior ticks `error` (likely GraphQL exhaustion — see 07:56Z digest).
- **Red bench rows:** `matmul_blocked` 1.55×, `matmul_naive` 1.33×, ML suite 1.33×, `num_gmres` 1.4× vs cpp.

## Recommended issues/PRs

| Priority | Repo | PR / issue | Labels / notes |
|----------|------|------------|----------------|
| P0 | lip | [#32](https://github.com/li-langverse/lip/pull/32) fix(ci) LLVM 22 | `merge-approved` — **human approve** |
| P0 | lit | [#18](https://github.com/li-langverse/lit/pull/18) fix(ci) LLVM 22 | `merge-approved` — **human approve** |
| P0 | lic-docs | [#1](https://github.com/li-langverse/lic-docs/pull/1) org ci.yml | `merge-approved` — **human approve** |
| P1 | li-net, li-httpd, li-std-core, li-std-math | #12, #13, #8, #9 agent-kit sync | `merge-approved` — approve wave after P0 |
| P1 | lic | [#437](https://github.com/li-langverse/lic/pull/437) perf(7e) matmul | `merge-approved` — **rebase + approve** |
| P2 | lic | [#499](https://github.com/li-langverse/lic/pull/499) fix(bench) matmul MIR | CI red — `bench_improver` / `code_implementer` |
| P2 | benchmarks | [#132](https://github.com/li-langverse/benchmarks/pull/132) macOS tier profile | `merge-approved` — conflicts + release_notes |
| Hygiene | benchmarks, lic | workspace sweep PRs | `superseded` — close stack |
| Hygiene | org | branches without PR | `pr_branch_opener` |

## Deferred

- Full org `run-pr-program.py` completion (long-running gate enrichment).
- `plan_audit` / `pr_program` slow paths (`--skip-slow` in briefing preflight).
- **roadmap** repo PRs — human merge only.
- **lic#500** PH-ML JobGraph, **lic#496** PH-CAD — CI fail / feature scope; after plan + CI.
- **li-demo** docs PRs (#15–#18) — CI fail; fix Pages workflow first.
- **li-httpd#10** feature split — CI fail; not merge queue.
- Adding `merge-approved` to implementer-owned PRs (#499, #495, agent bench runs) — reviewer/agent separation.
- Auto-merge execution — **`pr_merger`** after human APPROVED + conflict resolution.

---

**north_star_fit:** numerics / PH-5b, PH-7e (tier-1 matmul), Phase 2i linalg partial; ecosystem CI/agent-kit (easy, provable CI gates).
