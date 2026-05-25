# Benchmark problem sizes (survey)

**Purpose:** Document where problem **sizes** live today and how the benchmarks catalog/dashboard represent them.

## lic `tier1_micro` (`params.toml` → `N`)

| Bench id | params.toml | Catalog `problem_size` |
|----------|-------------|------------------------|
| `simd_dot` | `N = 10_000_000` | `10000000` |
| `reduce_sum` | `N = 100_000_000` | `100000000` |
| `matmul_naive` | `N = 256` | `256` |
| `matmul_blocked` | `N = 512` | `512` |
| `horner_pure_li` | `steps = 5_000_000` | `steps=5000000` |

## lic `tier2_physics`

| Bench id | Dominant size params |
|----------|---------------------|
| `md_lennard_jones` | `N = 256` |
| `nbody_gravity` | `N = 128` |
| `harmonic_oscillator_chain` | `N = 64` |
| `three_body` | `N = 3` |
| `wave_equation_1d` | `N = 8192` |
| `heat_equation_2d` | `nx=128`, `ny=128`, `steps=20000` |
| `wave_equation_2d` | `nx=128`, `ny=128`, `steps=25000` |
| `wind_field_bc` | `[grid]` section |

## lis `tier5_http` (scenario = payload class)

| Bench id | Size meaning |
|----------|----------------|
| `static_small` | ~1 KiB static `/` |
| `static_large` | 1 MiB `file.bin` (harness auto-generates) |

HTTP rows use **separate benchmark ids** today (`static_small` vs `static_large`), not a CSV `problem_size` column.

## CSV `variant` column (not problem size)

`latest.csv` **`variant`** is **build/oracle class** (`release`, `pure_li`, `shared_c_kernel`, `li_epoll`), not matrix dimension. Ingest still keys Li series on catalog `variant` when set.

## Planned multi-size rows

Use suffixed catalog ids + optional CSV `problem_size`:

- `matmul_naive_N256` (default, matches current harness name `matmul_naive`)
- `matmul_naive_N1024` (`base_id = "matmul_naive"`, `problem_size = "1024"`) when lic exports sized CSV rows

Optional future CSV column: `problem_size` on each row for sweeps without renaming `benchmark`.
