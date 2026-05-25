# Fix tier-5 HTTP summary unknown rows (macOS li-httpd blocker)

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**PR:** feat/fix-tier5-summary  
**PH / REQ:** PH-H, WP-T5  
**Author:** agent

---

## Summary (one sentence)

Tier-5 HTTP catalog rows with nginx/node CSV but no `li-httpd` on darwin ingest as **yellow** with explicit `no_li` / `no_li_httpd_bin` validity instead of blank **unknown**.

## Agent continuation (required)

1. **Read:** `scripts/ingest/build_summary.py` (`http_validity_from_csv`, `perf_status_for_benchmark`), `docs/ecosystem/lic-httpd-bench-compat.md`, `vendor/lis-tier5/results/latest.csv`.
2. **Run:** `LIC_ROOT=../lic LIS_ROOT=../lis python3 scripts/ingest/build_summary.py ../lic ../lis`; `python3 scripts/check-summary-measurement-coverage.py`; merge **lis** PR #12 then `LIS_ROOT=../lis ./scripts/sync-lis-tier5-vendor.sh`.
3. **Then:** On **Linux** with `LI_HTTPD_BIN=../lic/build/li-httpd`, refresh CSV for green/yellow/red `lang=li` RPS; ingest `tier5_http_exploits` when exploit_report lands.
4. **Blocked on:** **lis** PR #12 merge for canonical `benchmarks/results/latest.csv` in-repo.

## Changed (specific)

| Area | What | Evidence |
|------|------|----------|
| Ingest | HTTP validity before `verify_pass`; `latest.csv:oracle_only` / blocker flags; oracle-only **yellow** perf | `tier_counts["5"].unknown` 10→1; `total unknown` 39→25 |
| Ingest | Merge `lis` `benchmarks/results/latest.csv` + `results/latest.csv` | `sources.lis_csv` in `summary.json` |
| Vendor | `vendor/lis-tier5/results/latest.csv` from **lis** `feat/tier5-csv-full` | 29 rows, nginx/node wrk on arm |
| Docs | macOS li-httpd blocker table | `docs/ecosystem/lic-httpd-bench-compat.md` |

## Not changed (scope fence)

- **lic** `li-net-httpd` Linux build — oracle binary path only documented.
- **lis** harness source — synced vendor copy; merge via PR #12.
- `tier5_http_exploits` — still **unknown** until exploit CSV exists.
- Tier-6 database stubs — unchanged (19 unknown).

## Breaking changes

None — `status` may change from `unknown` to `yellow` for HTTP rows with oracle CSV.

## Security

N/A — ingest-only.

## Performance

N/A — dashboard ingest CPU only.

## Downstream

| Repo | Action |
|------|--------|
| **lis** | Merge PR #12; Linux re-bench for `lang=li` rows |
| **lic** | Ship linux `li-httpd` on main for CI tier-5 |

## CHANGELOG entry (paste into Unreleased)

```markdown
### Fixed
- **Tier-5 HTTP ingest:** macOS `no_li_httpd_bin` / oracle-only rows → yellow + explicit validity (WP-T5); merge `lis` `benchmarks/results/latest.csv` — [2026-05-25-fix-tier5-summary-unknowns.md](docs/release-notes/2026-05-25-fix-tier5-summary-unknowns.md).
```
