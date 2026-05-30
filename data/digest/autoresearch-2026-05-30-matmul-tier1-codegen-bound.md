# Autoresearch — proactive pass (2026-05-30)

**Run:** `autoresearch-2026-05-30-matmul-tier1-codegen-bound` · **Source:** proactive ecosystem sweep  
**Goal:** tier-1 `*_pure_li` / numerics yellow rows after numerics_researcher SOTA survey  
**north_star_fit:** blazingly-fast (PH-5b, PH-7e) + provable (lic#472 matmul loop witness) — proof before perf

## Executive summary

- **Briefing refresh:** ecosystem audit at 09:45Z shows **0 red** tier-1 numerics rows (down from 6 in stale 08:04Z snapshot); **`matmul_naive`** and **`matmul_blocked`** remain **yellow** at ~1.22–1.24× cpp (linux ingest).
- **SOTA sufficient:** BLIS/Eigen blocked GEMM already documented in Mode A pass (2026-05-17); no novel discretization or solver invention warranted for dense `@` matmul.
- **Hypothesis H1 rejected:** novel Li-only matmul schemes (Strassen, Winograd, custom reorder) cannot beat cpp oracle without PH-7e tile/SIMD lowering — **negative autoresearch**.
- **Hypothesis H2 rejected locally:** `matmul_blocked` Li/cpp **1.62×** on 2-run harness (512×512); cpp uses explicit 3-level blocking in `matmul_blocked_core.c`, Li bench uses single `@` — oracle parity gap, not algorithm gap.
- **Proof discipline:** proof_gap cycle 19 confirms tier-1 `@` loop codegen lacks Lean witness (lic#472); perf wins must stay advisory until P-linalg slice closes.
- **Prior art:** horner autoresearch negative (2026-05-17) — DCE/harness bugs vs codegen; matmul now has `li_rt_volatile_sink_f64` anti-DCE on working branch.
- **Control plane:** 14 prior autoresearch runs today ended `error` (digest-only timeout); this pass completes with study + local bench evidence.
- **Canonical perf path:** lic#499 matmul MIR restore — align bench_improver stacks (#437/#469) after #499 CI green; not autoresearch scope.

## Deliverable / findings

### Evidence pack

| Artifact | Path |
|----------|------|
| Study (negative) | `docs/numerics/studies/2026-05-30-matmul-tier1-autoresearch-negative.md` |
| Bench ids | `matmul_naive`, `matmul_blocked` |
| li-tests / lit | N/A — no kernel change shipped (negative result) |
| Lean/contracts | lic#472 open; cycle 19 digest `data/digest/proof_gap_researcher-2026-05-30-matmul-loop-witness-gap.md` |

### Local bench (2026-05-30)

```text
matmul_naive  cpp=0.0019s  li=0.0021s  ratio≈1.11×
matmul_blocked cpp=0.0082s li=0.0133s ratio≈1.62×
```

Dashboard linux (ingest 09:25Z): naive **1.22×**, blocked **1.24×** — both yellow, threshold 1.2.

### Hypothesis outcomes

| Hypothesis | Result | Evidence |
|------------|--------|----------|
| Novel matmul algorithm closes gap | **Falsified** | SOTA blocked GEMM in cpp core; Li `@` IKJ only; no shipped novel kernel |
| Li `@` matches cpp blocked at N=512 | **Falsified** | Local 1.62×; source-level blocking absent in Li main.li |
| SOTA survey adequate | **Verified** | 2026-05-17 pass + BLIS/Eigen citations |
| Yellow rows need autoresearch not codegen | **Falsified** | Gap maps to PH-7e + bench oracle parity |

## Recommended issues/PRs

| Priority | Repo | Title | Labels |
|----------|------|-------|--------|
| P0 | **lic** | PH-7e: cache-tile `@` matmul lowering or source blocking parity for `matmul_blocked` | `PH-7e`, `G-math`, `performance`, `bench` |
| P0 | **lic** | Fix CI + merge matmul MIR restore (#499) | `PH-5b`, `PH-7e`, `numerics-research` |
| P1 | **lic** | `[P-linalg] witness_matmul2d_ijk_loop + matmul_loop_eval pilot (lic#472)` | `provability`, `G-lean`, `novel-algorithm` (review math) |
| P1 | **lic** | bench_improver: land volatile-sink matmul harness parity on `perf/bench-improver-matmul-at-op-*` | `bench`, `PH-5b` |
| P2 | **benchmarks** | catalog: wire `num_gmres` harness path or mark planned-only | `ecosystem-gap`, `catalog` |
| P2 | **li-math** | `ml_conv2d_forward` tier-1 red follow-up after harness exists | `PH-5b`, `numerics-research` |

**Do not open** `novel-algorithm` PR for new GEMM mathematics — route to **bench_improver** + **proof_gap_researcher**.

## Deferred

- **ml_conv2d_forward**, **ml_mlp_***, **num_gmres** — catalog/harness gaps or li-math package; autoresearch blocked until numerics_researcher Mode A on those rows
- **Novel integrators / preconditioners** — no tier-2 physics red driving autoresearch this cycle
- **Algorithm note** (`docs/numerics/algorithms/`) — not created; negative result, no novel method to document
- **GIF/physics tier-2 visuals** — N/A for tier-1 micro GEMM
- **trusted.lean** — no edits

<!-- li-agent -->
## Agent deliverable
- [x] li-tests or lit test id: N/A — negative autoresearch (no kernel change)
- [x] Bench row / benchmarks path: `matmul_naive`, `matmul_blocked` — study `docs/numerics/studies/2026-05-30-matmul-tier1-autoresearch-negative.md`
- [x] Lean/contracts path documented or N/A with reason: lic#472 / cycle 19 proof_gap digest — loop witness open
- [x] Negative result documented if hypothesis rejected: yes — §5 study + this digest
