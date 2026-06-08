# Benchmark dashboard honesty labels

The [public dashboard](https://li-langverse.github.io/benchmarks/) and `data/latest/summary.json` report **two ratio axes** and a **validity gate**. Li is **never** labeled state-of-the-art (SOTA) in JSON or UI.

## Ratio axes

| Field | Meaning |
|-------|---------|
| `ratio_vs_cpp` / `ratio_vs_reference` | Li vs catalog `compare_oracle` (usually `cpp`; tier-5 HTTP uses `nginx`; database uses `postgres`). Drives **green/yellow/red** against `threshold_ratio_cpp`. |
| `ratio_vs_sota` | Li **relative speed** vs best competitor (`sota_lang`): **1.0 = SOTA speed**, higher is better (e.g. `0.85` = 85% of SOTA). Diagram bars use the same scale; not the threshold oracle. |
| `sota_lang` | Competitor language with the best metric in the row set. **Never `li`.** Diagram pins this lang at **1.0**. |
| `series[].relative_perf` | Per-language relative speed vs `sota_lang` (SOTA point = 1.0). |

Ingest policy: `scripts/ingest/build_summary.py` — `reporting.sota_policy = best_competitor_lang_excludes_li`.

## Validity gate

| `validity_status` | Perf claim | Dashboard `status` |
|-------------------|------------|---------------------|
| **pass** | Allowed when ratio is within threshold | Normal green/yellow/red from `compare_oracle` ratio |
| **fail** | **Not claimable** — speed without correctness is useless | Forced **red** even if wall time looks good |
| **unknown** | **Not claimable** until producers export pass signals | Forced **unknown** |

Sources (`validity_source`): `stability.csv`, `latest.csv:passed`, `metric:verify_pass`, `none`.

Catalog default: `validity_required = true` in [`catalog.toml`](../../catalog.toml) (per-benchmark override supported).

## Status colors (after validity gate)

| Status | Meaning | Agent action |
|--------|---------|--------------|
| **green** | Validity pass **and** `ratio_vs_cpp` ≤ `threshold_ratio_cpp` | Maintain; investigate regressions |
| **yellow** | Validity pass; between threshold and org alert band | Compiler/harness work in **lic** |
| **red** | Above threshold **or** validity fail | **lic** codegen, kernel, or correctness — not threshold tweaks here |
| **unknown** | Missing ingest, failed run, smoke-only row, or **unknown validity** | Fix harness/CSV; do not publish perf claims |

## Host OS

| Field | Meaning |
|-------|---------|
| `os` on summary rows | Primary host OS for the benchmark (`linux`, `darwin`, `windows`, or `unknown`) |
| `reporting.os_values` | Distinct OS tags in the current ingest (overview strip + search filter) |
| `os` on series points | Per-language OS when CSV exports include an `os` column |

## Variants (catalog)

| `variant` | Honest label |
|-----------|----------------|
| `default` | Li vs C++ on shared problem size; may use shared build flags |
| `shared_c_kernel` | Numerics may share C kernel — **not** pure-Li proof |
| `pure_li` | Li-only codegen path — cite **PH-7e**; red here is compiler work |
| `async_stub` | Tooling smoke — not HPC competitive |

## HPC reference library pins

SOTA stacks (Eigen, Kokkos, PETSc, Chapel) move on active release trains. Baseline versions for reference C++ builds, quarterly bump triggers, and AI-tooling parity notes live in [hpc-reference-library-cadence.md](../ecosystem/hpc-reference-library-cadence.md) ([benchmarks#27](https://github.com/li-langverse/benchmarks/issues/27)).

## Proof vs performance

- **G-*** rows in [provability-gaps.md](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) describe **proof wiring**, not bench color.
- A **green** row does **not** imply `lic build` discharges Lean for that kernel.
- A **red** `pure_li` row (e.g. `horner_pure_li`) is **performance debt**, not a missing G-* closure.

## Writing release notes / ADRs

Use: “dashboard **green** at ratio *r* vs `compare_oracle` on commit *sha*, validity **pass**, ratio vs SOTA *s* vs `{sota_lang}`” — not “proved fast”, “Li is SOTA”, or “beats SOTA” without study citations ([numerics methodology](../numerics/research-methodology.md)).

## HTTP tier-5 vs nginx (catalog)

Tier-5 throughput rows use `compare_oracle = "nginx"` and metric **`rps`**. SOTA among `{nginx, apache, lighttpd, …}` is computed separately; Li is never SOTA.

**Today:** [`lis`](https://github.com/li-langverse/lis) may still be stub for some scenarios; dashboard **unknown** + empty `series` means **no measured comparison** — not “Li is slower than nginx.”

## Local vs CI ingest

- **Local:** Clone **lic** and **lis** as siblings of **benchmarks**, then `./scripts/ingest/ingest-lic.sh`.
- **CI:** PR/push **Benchmarks CI** checks out `lic` + `lis` and runs the same ingest path.

## Downstream CSV producers (lic / lis)

Required for honest reporting (see `schema/bench-result.json`):

| Column | Producer | Purpose |
|--------|----------|---------|
| `os` | `lic` / `lis` `latest.csv` | Per-row and per-language OS breakdown |
| `passed` | `lic` harness / tier0 export | Validity gate (`true`/`false`) |
| `verify_ulps`, `verify_within_1ulp` | `lic` harness after `--verify` | Analytical-oracle deviation; `within_1ulp=1` ⇒ ≤1 float64 ULP |
| `verify_analytical`, `verify_checksum` | same | Closed-form reference vs measured checksum |
| `oracle_kind` | same | `analytical` or `iterative` |
| `benchmark`, `lang`, `metric`, `value` | Existing | Unchanged |

**lic:** extend `benchmarks/results/latest.csv` writer and tier0 `stability.csv` (already has `passed`; add `os` on export).

**lis:** tier-5 HTTP bench CSV should mirror columns when RPS pipeline lands.

## `li-local-ci` vs dashboard data

**[`li-local-ci`](https://github.com/li-langverse/li-local-ci)** records PR verification when GitHub Actions is missing — it **does not** replace CSV ingest or update `summary.json`.
