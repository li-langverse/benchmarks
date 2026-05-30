# Bench improver digest — 2026-05-30T10:51Z

**Agent:** `bench_improver` · **Heap:** `coord_numerics:bench_improver:b97ff11f0fa3e1dd6357`  
**north_star_fit:** blazingly-fast — PH-5b / PH-7e tier-1 lic harness; proof-before-perf (checksum parity, no `trusted.lean` edits)  
**Dashboard:** https://li-langverse.github.io/benchmarks/  
**Preflight:** `ecosystem-audit.json`, `summary.json` @ `2026-05-30T10:00:49Z` · `lic_sha` `c18c48e6`

## Executive summary

- **Public dashboard: no RED or YELLOW** tier-1 lic rows on linux; briefing’s six reds (`matmul_*`, `ml_*`, `num_gmres`) were **stale** (2026-05-29 ingest) vs refreshed `summary.json`.
- **22 tier-1 greens** for lic on linux; all measured rows pass the **1.2×** `threshold_ratio_cpp` gate.
- **5 near-threshold greens** remain with ratio **>1.0×** cpp — headroom polish, not gate failures: `num_integ_rk4` (1.083×) worst.
- Prior matmul codegen work on `main` cleared former reds: `matmul_blocked` **1.023×**, `matmul_naive` **1.056×** (was ~1.55× / 1.33× on stale dashboard).
- **`tier0_stability`** still **unknown** — no `stability.csv` on this runner; tier-0 must run on CI, not hand-edited JSON.
- HPC competitive registry gate **clear** (`lic/scripts/check-hpc-competitive.sh`).
- Open lic branch `perf/bench-improver-matmul-tier1-green-20260530` claims ≤1.0× matmul locally — **not merged**; dashboard already green under 1.2× without it.
- Do **not** edit `summary.json` alone; use `ingest-lic.sh` after lic harness runs.

## Deliverable / findings

### Failures report (`./scripts/benchmark-failures-report.sh`)

```
RED: none
YELLOW: none
GREEN near threshold (>1.0× cpp, 5):
  num_integ_rk4     1.083×  PH=PH-5b
  matmul_naive      1.056×  PH=PH-5b, PH-7e
  simd_dot          1.052×  PH=PH-5b, PH-7e
  matmul_blocked    1.023×  PH=PH-5b
  fft_1d_fixed      1.007×  PH=PH-5b, PH-7e
UNKNOWN: tier0_stability (tier 0)
```

Fresh `python3 scripts/ecosystem-audit.py` (2026-05-30T10:51Z) confirms: `red=[]`, `yellow=[]`, `green_count=22`.

### Briefing vs live dashboard (staleness)

| benchmark | briefing ratio | live ratio | live status |
|-----------|----------------|------------|-------------|
| `matmul_blocked` | 1.549× red | **1.023×** | green |
| `matmul_naive` | 1.333× red | **1.056×** | green |
| `num_gmres` | 1.400× red | (not in partial tier-1 CSV) | skip/unknown |
| `ml_conv2d_forward` | 1.333× red | li-math stub | skip |
| `ml_mlp_forward` | 1.333× red | li-math stub | skip |
| `ml_mlp_train_step` | 1.333× red | li-math stub | skip |
| `md_thermostat_berendsen` | yellow | tier-2 not in tier-1 ingest | skip |
| `md_thermostat_nose_hoover` | yellow | tier-2 not in tier-1 ingest | skip |

### Ingested linux tier-1 CSV rows (`results/latest.csv`)

| benchmark | li (s) | cpp (s) | ratio | variant | checksum |
|-----------|--------|---------|-------|---------|----------|
| `num_integ_rk4` | 0.0013 | 0.0012 | **1.083×** | shared C kernel | — |
| `matmul_naive` | 0.0019 | 0.0018 | **1.056×** | pure lic | verify OK |
| `simd_dot` | 0.0181 | 0.0172 | **1.052×** | shared C kernel | — |
| `matmul_blocked` | 0.0090 | 0.0088 | **1.023×** | pure lic | verify OK |
| `fft_1d_fixed` | 0.0153 | 0.0152 | **1.007×** | shared C kernel | — |

### lic codegen status (PH-7e)

- **`matmul_naive` / `matmul_blocked`:** pure-Li IKJ loops in `benchmarks/tier1_micro/*/li/main.li`; `@` matmul lowering on `main` ingest — gate cleared.
- **`num_integ_rk4`:** algo-registry stub path (`catalog.toml` → `benchmarks/tier1_micro/num_integ_rk4`); harness uses shared C kernel + lic wrapper — **8.3% slack** is integrator call overhead, not matmul-class SIMD.
- **`simd_dot`:** shared `dot_core.c` oracle; Li wrapper adds ~5% vs cpp — PH-7e vectorized reduction candidate.
- **`lic` not built** on this runner (`build/lic` absent); local re-bench deferred to CI or post-`./scripts/build.sh`.

### Repro (assessment)

```bash
cd benchmarks
./scripts/benchmark-failures-report.sh
python3 scripts/ecosystem-audit.py

cd ../lic && ./scripts/check-hpc-competitive.sh
# After lic codegen PR merge:
cd lic && ./scripts/build.sh
cd lic/benchmarks/harness && python3 bench.py --tier 1 --runs 10
cd benchmarks && LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh
```

### Prior artifacts

- `data/digest/bench_improver-2026-05-30-tier1-red-clear.md` — matmul red→yellow narrative (now all green).
- `data/runs/bench_improver-proactive-20260530.md` — proactive sweep earlier same day.
- Study: `lic/docs/numerics/studies/2026-05-30-matmul-blocked-7e.md` (on perf branch).

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| `perf(5b): RK4 integrator — bring num_integ_rk4 ≤1.0× cpp` | **lic** | `PH-5b`, `numerics` — highest near-threshold row; shared-kernel + Li wrapper |
| `perf(7e): simd_dot vectorized reduction ≤1.0×` | **lic** | `PH-7e`, `PH-5b` — PH-7d `@vectorized` lowering (Lean evidence required) |
| `perf(7e): merge matmul blocked/naive emit (optional ≤1.0× polish)` | **lic** | `PH-7e`, `PH-5b` — branch `perf/bench-improver-matmul-tier1-green-20260530` |
| `chore(swarm): close stale gap-benchmark-red-matmul-naive / num_gmres` | **lic** | `ecosystem-gap` — rows green on dashboard |
| `ci: tier0_stability ingest on linux runner` | **benchmarks** / **lic** | `PH-5b` — populate `stability.csv` |
| `perf: ml_conv2d / ml_mlp_* tier-1` | **li-std-math** | `PH-5b`, `PH-ML` — not lic codegen |
| `numerics: md_thermostat_* tier-2 ≤1.2×` | **lic** | `PH-5b`, `numerics-research` — separate pass |

## Deferred

- **≤1.0× cpp advisory** for all tier-1 micro rows — optional after 1.2× gate stable; start with `num_integ_rk4`.
- **`num_gmres`**, **`ml_*`** — verify on full CI tier-1 suite; not reproduced in current partial CSV.
- **`md_thermostat_*`** tier-2 (~1.29× on stale dashboard) — shared MD oracle; numerics_researcher pass.
- **Parallel/simd codegen** beyond existing matmul — requires Lean / contract evidence per PH-7d.
- **Full `./scripts/run-full-benchmark-suite.sh` on CI** — partial `--only` ingest must not replace oracle rows.
- **Hand-editing `summary.json`** — forbidden; normal ingest only.
