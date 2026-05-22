# Benchmark dashboard honesty labels

The [public dashboard](https://li-langverse.github.io/benchmarks/) and `data/latest/summary.json` report **ratios only** vs a catalog reference (**`cpp` = 1.00×** for micro/physics; tier-5 HTTP uses **nginx** or another `compare_oracle` when set). **Absolute wall times are not published** on the site. Each ingest records **hardware** (`cpu_model`, flags, host uname, git shas) in `summary.json` → `hardware`. Not formal proof or correctness certificates.

## Status colors

| Status | Meaning | Agent action |
|--------|---------|--------------|
| **green** | `ratio_vs_cpp` ≤ `threshold_ratio_cpp` in [`catalog.toml`](../../catalog.toml) | Maintain; investigate regressions |
| **yellow** | Between threshold and org alert band (ingest policy) | Compiler/harness work in **lic** |
| **red** | Above threshold | **lic** codegen or kernel — not threshold tweaks here |
| **unknown** | Missing ingest, failed run, or smoke-only row | Fix harness path or ingest; do not publish perf claims |

## Variants (catalog)

| `variant` | Honest label |
|-----------|----------------|
| `default` | Li vs C++ on shared problem size; may use shared build flags |
| `shared_c_kernel` | Numerics may share C kernel — **not** pure-Li proof |
| `pure_li` | Li-only codegen path — cite **PH-7e**; red here is compiler work |
| `async_stub` | Tooling smoke — not HPC competitive |

## Proof vs performance

- **G-*** rows in [provability-gaps.md](https://github.com/li-langverse/lic/blob/main/docs/verification/provability-gaps.md) describe **proof wiring**, not bench color.
- A **green** row does **not** imply `lic build` discharges Lean for that kernel.
- A **red** `pure_li` row (e.g. `horner_pure_li`) is **performance debt**, not a missing G-* closure.

## Writing release notes / ADRs

Use: “dashboard **green** at *r*× vs **cpp** on *cpu_model* / commit *sha*” — not absolute seconds, “proved fast”, or “beats SOTA” without study citations ([numerics methodology](../numerics/research-methodology.md)).

## Local publish (no Actions)

```bash
LIC_ROOT=../lic ./scripts/refresh-live-sites.sh
```

See skill **`run-local-pages-benchmarks`** in **lic** `.cursor/skills/`.

## HTTP tier-5 vs nginx (catalog)

Tier-5 rows `static_small` and `keepalive_pipelining` use `compare_oracle = "nginx"` and metric **`rps`** in [`catalog.toml`](../../catalog.toml). `scripts/ingest/build_summary.py` treats **nginx** as the reference language for those charts (same ratio machinery as C++, with an inversion so higher Li RPS is “better” vs the threshold).

**Today:** [`lis`](https://github.com/li-langverse/lis) `benchmarks/tier5_http/harness/bench_http.py` is still **TOML validation / stub** until `li-httpd` and the wrk/nginx baseline pipeline land; there is no checked-in `lis/results/latest.csv` producer yet. Dashboard **unknown** + empty `series` for `keepalive_pipelining` means **no measured RPS comparison** — not “Li is slower than nginx.” Product intent vs nginx (agent gateway, streaming, schema-driven config, proof-backed core) is described in **lis** `docs/plan.md`, separate from dashboard throughput rows.

## Local vs CI ingest

- **Local:** Clone **lic** and **lis** as siblings of **benchmarks** (or set `LIC_ROOT` / `LIS_ROOT`), then run `./scripts/ingest/ingest-lic.sh` from the benchmarks repo. `build_summary.py` merges `lic/benchmarks/results/latest.csv` and `lis/results/latest.csv`.
- **CI:** PR/push **Benchmarks CI** (`.github/workflows/ci.yml`) checks out `lic` + `lis`, builds `lic`, and runs the same ingest path so `build_summary.li` / Python fallback see a real `lis/` tree.
- **Manual ingest workflow** (`.github/workflows/ingest.yml`): checks out `lic` + `lis`, copies dispatch artifact `artifacts/latest.csv` into `lic/benchmarks/results/latest.csv` when present, then runs `ingest-lic.sh`.

## `li-local-ci` vs dashboard data

**[`li-local-ci`](https://github.com/li-langverse/li-local-ci)** (driven from benchmarks via `scripts/local-ci-sweep.py`) records PR verification when **GitHub Actions** is missing, skipped, or red (minutes/quota). Results land in `data/latest/local-ci-results.json` and are read by `scripts/pr-merge-gate.py` as a **merge gate** signal — they **do not** replace `lis` CSV ingest or update `summary.json` / Pages. Use local-ci for “did this PR pass the same checks locally?”; use ingest + `lis` bench artifacts for “what does the public dashboard show?”
