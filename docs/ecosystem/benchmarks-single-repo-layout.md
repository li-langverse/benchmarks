# ADR: Benchmark workloads live only in li-langverse/benchmarks

**Status:** Accepted (2026-05-30)  
**Repos:** `benchmarks` (canonical), `lic` (toolchain only)

## Context

Historically tier-1/2 micro/physics workloads and `harness/bench.py` lived under `lic/benchmarks/`, while the public dashboard and `catalog.toml` lived in `li-langverse/benchmarks`. That split confused agents (“fix harness in lic vs ingest in benchmarks”) and duplicated trees.

## Decision

1. **All benchmark workloads and harness drivers** live in **`li-langverse/benchmarks`**:
   - `harness/` — `bench.py`, tier-5 HTTP drivers, verify, stability
   - `benchmarks/workloads/` — `tier1_micro`, `tier1_stdlib`, `tier2_physics`, `tier5_http`, …
   - `results/` — `latest.csv` and artifacts for ingest

2. **`lic` is the language toolchain only** — compiler build, `li-tests`, packages. It does **not** own perf workload trees (legacy `lic/benchmarks/` is deprecated).

3. **Run contract:** install/clone benchmarks next to lic; set `LIC_ROOT=../lic`; run experiments via:
   ```bash
   ./scripts/run-bench.sh --tier 1
   ./scripts/run-full-benchmark-suite.sh
   ./scripts/ingest/ingest-lic.sh
   ```

4. **Catalog `path` values** use benchmarks-repo layout: `benchmarks/workloads/tier1_micro/<id>` (sync via `scripts/catalog/sync-paths-from-lic-tree.py`).

## Consequences

| Before | After |
|--------|--------|
| Edit kernels in `lic/benchmarks/tier*` | Edit `benchmarks/workloads/tier*` |
| `python3 lic/benchmarks/harness/bench.py` | `./scripts/run-bench.sh` |
| Ingest reads `lic/benchmarks/results/latest.csv` | Ingest reads `benchmarks/results/latest.csv` (fallback: legacy lic path) |
| “Never copy harness into benchmarks” | **Harness must not remain in lic** (deprecation period + delete follow-up PR on lic) |

## Migration

- `scripts/sync-workloads-from-lic.py` — one-time/idempotent copy from `LIC_ROOT/benchmarks` into this repo.
- Legacy fallback in `harness/paths.py` warns if workloads are still only under lic.
- Follow-up: remove `lic/benchmarks/` tree in a dedicated **lic** PR after CI uses `BENCHMARKS_ROOT`.

## Out of scope

- Tier-0 correctness proofs remain in `lic/li-tests` (verification, not dashboard perf catalog).
- `lis` vendor HTTP harness under `vendor/lis-tier5` unchanged; tier-5 TOML scenarios now under `benchmarks/workloads/tier5_http`.
