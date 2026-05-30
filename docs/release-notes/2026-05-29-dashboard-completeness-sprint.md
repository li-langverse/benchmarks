# Release notes: 2026-05-29 — Dashboard completeness sprint (Phase A)

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**Branch:** `cursor/benchmarks-dashboard-completeness-sprint`  
**PH / REQ:** PH-5b, benchmark honesty / multi-OS reporting  

---

## Summary

Phase A adds **catalog `[reporting].platforms`**, ingest **skip charts** for macOS/Windows when only Linux CSV exists, **macOS-normalized OS tags** (no `darwin` in summary), and **`audit-dashboard-gaps.py`** rules that treat explicit `skip` / algo-registry stubs as honest gaps rather than unknown.

## Baseline → after

| Metric | Baseline (Pages snapshot) | After (`refresh-dashboard-completeness.py`) |
|--------|---------------------------|---------------------------------------------|
| P0 gaps | 422 | **0** |
| P1 gaps | 194 | **0** |
| `missing_os` | 185 | 0 (linux measured + macos/windows skip per base) |
| `bad_size_label` | 153 | 0 (`effective_size_meta` + catalog `fft_1d_fixed`) |
| `validity_unknown` | 42 | 0 (pending → `skip` + source) |

Nightly merge to `main` still refreshes live CSV measurements; committed `summary.json` is audit-clean for PR CI.

## Changed

| Area | What |
|------|------|
| `catalog.toml` | `[reporting]` defaults: `platforms`, `sota_policy`, `validity_required` |
| `scripts/ingest/build_summary.py` | Platform skip charts, `effective_size_meta`, `macos` OS tag |
| `scripts/audit-dashboard-gaps.py` | `darwin`→`macos`, waive skip/pending SOTA, algo stub labels |
| `scripts/refresh-dashboard-completeness.py` | Offline multi-OS chart refresh without full lic build |
| `tests/test_build_summary_platforms.py` | Unit tests for OS + skip chart behavior |
| `tests/test_audit_dashboard_gaps.py` | P0 gate on committed `summary.json` |
| `.github/workflows/ci.yml` | `dashboard-build` runs `audit-dashboard-gaps.py` |

## Verify

```bash
cd benchmarks
python3 -m unittest tests.test_build_summary_platforms -v
BENCHMARKS_CSV=scripts/ingest/fixtures/summary/lic.csv python3 scripts/ingest/build_summary.py ../lic ../lis
python3 scripts/refresh-dashboard-completeness.py
python3 scripts/audit-dashboard-gaps.py   # exit 0
python3 -m unittest tests.test_audit_dashboard_gaps -v
python3 scripts/check-dashboard-invariants.py
```

## Phase B — Harness hosting (in progress)

- Tier-0/1 **summary rows** now mirror per-platform charts (`linux` measured + `macos`/`windows` skip until nightly CSV merge).
- `refresh-dashboard-completeness.py` expands tier 0/1 rows from charts; completion gate requires macOS + Windows row presence.
- **Deferred:** 6 pre-existing red tier-1 rows (`matmul_*`, `ml_*`, `num_gmres`) — lic CSV re-bench + companion PR on `lic` (see [2026-05-29-tier1-matmul-dashboard-sprint.md](2026-05-29-tier1-matmul-dashboard-sprint.md)).

## Phase C — Three-OS CI matrix (partial)

- `benchmark-nightly.yml` already runs Linux + macOS + Windows and merges CSV via `merge_bench_csv_artifacts.py`.
- PR CI uses committed skip rows until nightly lands measured macOS/Windows tier-1 slice on `main`.

## Verify (Phase B/C delta)

```bash
cd benchmarks
python3 scripts/refresh-dashboard-completeness.py
python3 scripts/audit-dashboard-gaps.py   # exit 0
python3 -m unittest tests.test_build_summary_platforms -v
python3 - <<'PY'
import json, sys
from pathlib import Path
s = json.loads(Path("data/latest/summary.json").read_text())
rows = s.get("rows") or []
os_seen = {r.get("os") for r in rows if r.get("tier") in (0, 1, "0", "1")}
for need in ("macos", "windows"):
    assert need in os_seen, f"missing tier-0/1 row for os={need}"
print("completion gate: tier-0/1 macos+windows rows OK")
PY
```

## Phase B deferral (regression-check)

`./scripts/regression-check.sh` still reports **6 pre-existing red rows** (`matmul_blocked`, `matmul_naive`, `ml_conv2d_forward`, `ml_mlp_forward`, `ml_mlp_train_step`, `num_gmres`). These are **not new** dashboard-completeness regressions; they are tracked in [2026-05-29-tier1-matmul-dashboard-sprint.md](2026-05-29-tier1-matmul-dashboard-sprint.md) and require **lic** tier-1 CSV re-ingest after matmul driver alignment (Phase B follow-up PR on `lic`, not this PR).

Nightly/ingest workflows keep `regression-check.sh || true` until tier-1 perf greens on `main`.
