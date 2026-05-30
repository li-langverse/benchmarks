# Bench improver — tier-1 red clear (2026-05-30)

**Run:** `bench_improver` · **heap:** `coord_numerics:b97ff11f`  
**north_star_fit:** blazingly-fast — PH-5b / PH-7e tier-1 lic harness

## Executive summary

- **Dashboard RED → none** after fresh tier-1 ingest; prior **`horner_pure_li` 3.0×** was stale CSV + cold `lic` (live **0.8×**).
- Merged **`e6fcf17f`** matmul codegen into `compiler/codegen/emit.cpp` (4-wide FMA gather/scatter, blocked IKJ tile reset, `runtime_team_size` API preserved).
- **`matmul_blocked`** / **`matmul_naive`** now **yellow** (~1.24× / 1.22×), not red — within advisory band but still above strict 1.2× cap.
- Preflight **six briefing reds** (ML/gmres/matmul) were **not reproduced** on current harness partial tier-1 CSV.
- Study: `lic/docs/numerics/studies/2026-05-30-bench-improver-tier1-red.md`.
- **`tier0_stability`** remains unknown/skip on this runner.
- Do **not** hand-edit `summary.json`; ingest path used.
- Open lic PR for emit merge; human triage duplicate matmul agent PR stack.

## Deliverable / findings

### Before / after (ingested `summary.json` @ 2026-05-30T09:25Z)

| benchmark | ratio vs cpp | status (before) | status (after) |
|-----------|--------------|-----------------|----------------|
| `horner_pure_li` | **0.80×** | red 3.0× | **green** |
| `matmul_naive` | 1.22× | red (briefing) | yellow |
| `matmul_blocked` | 1.24× | red (briefing) | yellow |
| `simd_dot` | 1.05× | green | green |

### Root cause — `horner_pure_li`

`HornerConstLoopF64` (trip ≥ 65536, const `x`) already on `main`; red row used **old** `latest.csv` (`li=0.0015s`) without rebuilt compiler. Fresh `./scripts/build.sh` + `bench.py` → **0.0004–0.0005s**.

### Root cause — matmul

Ported perf-branch emit; **`matmul_blocked` still ~1.30×** on `11ef5e37` base vs **~0.98×** on full `perf/bench-improver-matmul-simd-j-20260530` — suggests remaining MIR/`lower.cpp` stack alignment (deferred).

### Repro

```bash
cd lic && ./scripts/build.sh
cd lic/benchmarks/harness && python3 bench.py --tier 1 --runs 6
cd benchmarks && cp ../lic/benchmarks/results/latest.csv results/latest.csv
LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh
./scripts/benchmark-failures-report.sh
```

## Recommended issues/PRs

| Repo | Title | Labels |
|------|-------|--------|
| **lic** | `perf(7e): merge matmul blocked/naive emit from perf/bench-improver-matmul-simd-j` | `PH-7e`, `PH-5b`, `numerics` |
| **lic** | `perf(7e): align lower.cpp matmul MIR with blocked emit (≤1.2× matmul_blocked)` | `PH-7e`, `G-math` |
| **benchmarks** | `chore: ingest tier-1 bench_improver 2026-05-30` | `benchmarks` |
| **li-math** | `perf: ml_conv2d / ml_mlp_* tier-1 (li-math repo)` | `PH-5b`, `PH-ML` |

## Deferred

- **`matmul_blocked` ≤1.2×** strict cap — yellow 1.24×; full perf branch stack or autoresearch.
- Briefing **`num_gmres`**, **`ml_*`** reds — not in partial tier-1 harness CSV; verify on CI full suite.
- **`md_thermostat_*`** tier-2 yellow (~1.29×) — separate numerics pass.
- **`tier0_stability`** — run tier-0 on CI runner with `stability.csv`.
