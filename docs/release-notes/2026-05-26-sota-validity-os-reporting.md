# SOTA-relative ratios, validity gate, and per-OS reporting

## Summary

`summary.json` and dashboard-next now report Li vs best competitor (SOTA, never Li), gate perf status on validity (tier0/stability/CSV `passed`), and surface host `os` per row with overview OS breakdown.

## Agent continuation

1. **Read:** `docs/honesty/benchmark-dashboard.md`, `schema/bench-result.json`, `catalog.toml` oracle comments, `scripts/ingest/build_summary.py`.
2. **Run:** `python3 scripts/ingest/build_summary_fixture.py`; `python3 scripts/ingest/compare_summary_outputs.py build/compare/summary_li.json build/compare/summary_py.json` (after Li gate); `cd dashboard-next && npm ci && npm run build`; `LIC_ROOT=../lic python3 scripts/ingest/build_summary.py ../lic ../lis` when lic sibling exists.
3. **Then (lic/lis):** add `os` + `passed` to `latest.csv` writers; document machine matrix in bench README; re-run full ingest so validity unknown count drops.
4. **Blocked on:** Per-OS duplicate summary rows when one benchmark runs on linux+darwin in the same CSV — ingest currently picks primary OS (Li row preferred); multi-OS split rows are a follow-up.

## Changed

| Area | Paths |
|------|--------|
| Schema | `schema/bench-result.json` — `sota_lang`, `ratio_vs_sota`, `validity_status`, `validity_source`, `os`, `passed` |
| Ingest | `scripts/ingest/build_summary.py` — SOTA pick (excludes `li`), validity merge, `apply_validity_gate`, `reporting` block |
| Fixture gate | `scripts/ingest/build_summary_fixture.py`, `scripts/ingest/fixtures/summary/*` |
| Catalog | `catalog.toml` — `validity_required`, compare_oracle vs SOTA policy comments |
| Dashboard | `dashboard-next/lib/summary.ts`, `lib/validity.ts`, `lib/overview.ts`, bench/overview components |
| Honesty | `docs/honesty/benchmark-dashboard.md` |

## Not changed

- Catalog **threshold_ratio_cpp** values (no greenwash).
- **lic/lis** harness measurements (only ingest interpretation + doc’d CSV gaps).
- GitHub Pages cutover (still Vite until WP8).
- Agent control plane UI in **li-cursor-agents**.

## Breaking

N/A for consumers that ignored new fields. Agents/scripts that assumed `status` reflected raw wall time only must treat **validity fail** as non-claimable perf (forced red).

## Security

N/A — reporting only; no trusted creep.

## Performance

N/A — no new harness runs in this PR; evidence is fixture ingest + optional local `build_summary.py` when lic CSV present.

## Downstream

| Repo | Need |
|------|------|
| **lic** | Export `os`, `passed` on `benchmarks/results/latest.csv`; keep `stability.csv` tier0 passes |
| **lis** | Same columns on `results/latest.csv` when tier-5 RPS pipeline is live |
| **benchmarks** | Re-ingest after producer CSVs land to shrink validity-unknown pillar counts |
