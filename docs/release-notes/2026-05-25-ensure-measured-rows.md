# Release notes: 2026-05-25 — ensure-measured-rows

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** feat/ensure-measured-rows  
**PH / REQ:** dashboard ship / honesty  
**Author:** agent

---

## Summary (one sentence)

Adds CI regression gates so `summary.json` cannot ship with all `unknown` tier colors, fixes ingest validity variant fallback, and refreshes committed summary from `lic` CSV (11 measured colors: 10 green, 1 red).

## Agent continuation (required)

1. **Read:** `docs/dashboard/INVARIANTS.md` invariants #10–#12; `scripts/check-summary-measurement-coverage.py`.
2. **Run:** `LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh`; `python3 scripts/check-summary-measurement-coverage.py`; confirm Benchmarks CI `ingest-smoke` + `dashboard-build` green on `main`.
3. **Then:** Expand `lic/benchmarks/results/latest.csv` for `matmul_naive` / `horner_pure_li`; re-ingest and commit.
4. **Blocked on:** none for gate wiring; fuller coverage blocked on lic harness CSV refresh.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Ingest | `build_summary.py` — `li_rows_for_validity` + `latest.csv:perf_present` | Local ingest: 11 colored rows |
| CI gate | `scripts/check-summary-measurement-coverage.py` | `PASS` locally |
| CI | `.github/workflows/ci.yml` — after ingest-smoke + dashboard-build | Benchmarks CI |
| Data | `data/latest/summary.json` — post-ingest colors | `simd_dot` red (validity pass) |
| Docs | `docs/dashboard/INVARIANTS.md` #10–#12 | — |

## Not changed (scope fence)

- **dashboard-next** UI measured/pending strip — separate branch.
- Catalog row count (179) — colors only.
- **lic** PH-IO-7 Li summary build — still Python fallback in CI.

## Breaking changes

None.

## Security

N/A — read-only JSON/CSV checks.

## Performance

N/A — O(n) summary/CSV scan.

## Downstream

| Repo | Action |
|------|--------|
| Pages | Redeploy when `data/latest/summary.json` on `main` |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Added
- **Summary measurement coverage gate:** `scripts/check-summary-measurement-coverage.py`; CI after ingest and on committed summary — [2026-05-25-ensure-measured-rows.md](docs/release-notes/2026-05-25-ensure-measured-rows.md).

### Fixed
- **Summary validity + colors:** `build_summary.py` variant fallback + `perf_present`; refresh `summary.json` from lic CSV ingest — [2026-05-25-ensure-measured-rows.md](docs/release-notes/2026-05-25-ensure-measured-rows.md).
```
