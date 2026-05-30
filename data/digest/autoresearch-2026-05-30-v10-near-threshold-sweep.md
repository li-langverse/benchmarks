# Autoresearch — proactive pass v10 (2026-05-30)

**Run:** `autoresearch-1780135392351` · **Source:** proactive ecosystem sweep  
**Goal:** refresh briefing signals; triage near-threshold tier-1 rows for novel numerics vs codegen routing  
**north_star_fit:** provable (PH-5b) + blazingly-fast (PH-7e) — proof before perf; publish only with bench evidence

## Executive summary

- **Dashboard posture:** **0 red**, **0 yellow** tier-1 lic rows on linux (`summary.json` @ 10:00:49Z); **22 greens**, **5 near-threshold** (ratio >1.0×, ≤1.2× cap).
- **No `*_pure_li` red rows:** only catalog `pure_li` variant is `horner_pure_li` (green); matmul benches are pure-Li source but SOTA blocked GEMM already covers them ([matmul negative study](../docs/numerics/studies/2026-05-30-matmul-tier1-autoresearch-negative.md)).
- **Matmul tier-1 cleared:** `matmul_naive` **1.056×**, `matmul_blocked` **1.023×** (was yellow ~1.22–1.24× in earlier briefing); autoresearch negative stands — route remaining headroom to **bench_improver** / lic#499 merge.
- **Top near-threshold:** `num_integ_rk4` **1.083×** — **negative autoresearch** (shared C oracle; classical RK4 is SOTA; rust/julia show same overhead).
- **Swarm gap registry stale:** `gap-benchmark-red-matmul-naive-tier1`, `gap-benchmark-red-num-integ-euler-tier1`, etc. still open while dashboard rows are green — close/repoint, not novel-algorithm work.
- **Control plane:** 14 prior autoresearch runs today ended `error` (digest timeout); this pass completes with v10 digest + RK4 negative study.
- **No novel algorithm PR warranted** this cycle — all actionable headroom is codegen, harness ingest, or pure_li variant prerequisites.

## Deliverable / findings

### Evidence pack

| Artifact | Path |
|----------|------|
| Matmul negative (prior) | `docs/numerics/studies/2026-05-30-matmul-tier1-autoresearch-negative.md` |
| RK4 negative (new) | `docs/numerics/studies/2026-05-30-num-integ-rk4-autoresearch-negative.md` |
| Bench ids surveyed | `num_integ_rk4`, `matmul_naive`, `matmul_blocked`, `simd_dot`, `fft_1d_fixed`, `horner_pure_li` |
| li-tests / lit | N/A — no kernel change shipped (negative results) |
| Lean/contracts | N/A — shared-oracle microbenches; integrator proofs deferred until pure_li kernel exists |

### Near-threshold routing (linux ingest)

| benchmark | ratio vs cpp | Autoresearch? | Route |
|-----------|--------------|---------------|-------|
| `num_integ_rk4` | 1.083× | **No** — shared C RK4; H1 falsified | bench_improver (FFI/emit) |
| `matmul_naive` | 1.056× | **No** — BLIS/Eigen SOTA | bench_improver / lic `perf/bench-improver-matmul-tier1-green-20260530` |
| `simd_dot` | 1.052× | **No** — reduction SIMD is PH-7e | bench_improver + PH-7e lowering |
| `matmul_blocked` | 1.023× | **No** — blocked GEMM SOTA | bench_improver (merge emit PR) |
| `fft_1d_fixed` | 1.007× | **No** — within noise | defer |
| `horner_pure_li` | green | **No** — prior negative 2026-05-17 | closed |

### Hypothesis outcomes (this pass)

| Hypothesis | Result | Evidence |
|------------|--------|----------|
| Novel RK4 scheme closes 1.083× gap | **Falsified** | Shared `num_integ_rk4_core.c`; rust/julia ~1.08× too |
| Tier-1 yellow rows need autoresearch | **Falsified** | All green; matmul improved via codegen not new math |
| SOTA survey adequate for surveyed rows | **Verified** | RK4 + GEMM + Horner citations in studies |
| Stale swarm red gaps reflect live dashboard | **Falsified** | ingest 10:00Z shows green |

### Repro

```bash
cd benchmarks
./scripts/benchmark-failures-report.sh
python3 scripts/ecosystem-audit.py
python3 scripts/numerics-evidence-checklist.py \
  --study docs/numerics/studies/2026-05-30-num-integ-rk4-autoresearch-negative.md
```

## Recommended issues/PRs

| Priority | Repo | Title | Labels |
|----------|------|-------|--------|
| P0 | **lic** | Merge matmul 7e emit branch (`perf/bench-improver-matmul-tier1-green-20260530`) | `PH-7e`, `PH-5b`, `numerics` |
| P1 | **lic** | Trim `LI_EXTRA_C` call overhead for shared-oracle microbenches (`num_integ_rk4`) | `PH-5b`, `bench` |
| P1 | **benchmarks** | Close stale swarm gaps for green tier-1 rows (matmul, num_integ_*, num_gmres) | `ecosystem-gap` |
| P2 | **lic** | numerics_researcher: add `num_integ_rk4_pure_li` catalog variant + harness | `PH-5b`, `numerics-research` |
| P2 | **lic** | PH-7e: simd_dot vectorized reduction ≤1.0× cpp | `PH-7e`, `PH-5b` |
| P2 | **benchmarks** | tier0_stability ingest on linux CI runner | `PH-5b`, `ecosystem-gap` |

**Do not open** `novel-algorithm` PRs for RK4 stage fusion or GEMM shortcuts — negative evidence above.

## Deferred

- **Pure-Li integrator autoresearch** — blocked until `pure_li` RK4 harness exists (currently `algo_registry` + shared C)
- **Tier-2 physics** (`orbit_two_body`, `cloth_swing`, `md_*`) — no tier-2 red on dashboard; separate numerics_researcher pass when red
- **ml_conv2d / ml_mlp / num_gmres harness gaps** — catalog stubs; autoresearch blocked until Mode A harness
- **Algorithm notes** (`docs/numerics/algorithms/`) — not created; negative results only
- **trusted.lean** — no edits

<!-- li-agent -->
## Agent deliverable
- [x] li-tests or lit test id: N/A — negative autoresearch (no kernel change)
- [x] Bench row / benchmarks path: `num_integ_rk4`, near-threshold set — studies under `docs/numerics/studies/2026-05-30-*-autoresearch-negative.md`
- [x] Lean/contracts path documented or N/A with reason: shared-oracle microbenches; pure_li integrator proofs deferred
- [x] Negative result documented if hypothesis rejected: yes — RK4 + prior matmul studies
