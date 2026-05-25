# Dashboard invariants (regression gates)

These rules are enforced in CI via `scripts/check-dashboard-invariants.py` and `scripts/check-dashboard-static-routes.sh`. A PR that breaks any invariant must be fixed before merge — do not weaken checks without human approval.

## Must never break

| # | Invariant | Rationale |
|---|-----------|-----------|
| 1 | **Li is never SOTA** | `sota_lang` must never be `li`; `reporting.sota_policy` = `best_competitor_lang_excludes_li` |
| 2 | **Validity before perf** | Rows include `validity_status`; fail/unknown must not show green perf without pass |
| 3 | **Minimum row coverage** | `summary.json` `rows.length` ≥ **150** and equals `catalog.toml` benchmark count |
| 4 | **Catalog ↔ summary ids** | Every catalog `id` has exactly one summary row (`benchmark` field) |
| 5 | **No package-only stubs** | Banned ids: `lig_viewport_stub`, `li_math_gemm_stub`; no new `*_stub` catalog ids |
| 6 | **Sized benches labeled** | Catalog rows with `problem_size` must have non-empty `size_label` on matching chart/row |
| 7 | **Pillars present** | `summary.json` `pillars` includes all nine: numerics, compiler, server, physics, proofs, security, database, graphics, tooling |
| 8 | **SOTA fields on branch** | Each row has `validity_status`, `ratio_vs_sota` keys (value may be null until measured) |
| 9 | **Pages artifact** | After build: `out/index.html`, `out/matrix/index.html`, bench pages ≥ row count − 5 |

## Verify locally

```bash
# From repo root — fast invariant gate (no lic build)
python3 scripts/check-dashboard-invariants.py

# After dashboard-next build
cd dashboard-next && npm ci && npm run build
# Copy JSON like CI/Pages
mkdir -p out/latest
for f in summary.json release-index.json benchmark-matrix.json proof-posture.json; do
  [ -f "../data/latest/$f" ] && cp "../data/latest/$f" out/latest/
done
bash ../scripts/check-dashboard-static-routes.sh

# Full ingest + invariants (siblings lic/lis)
LIC_ROOT=../lic LIS_ROOT=../lis ./scripts/ingest/ingest-lic.sh
python3 scripts/check-dashboard-invariants.py

# Fixture refresh (CI parity)
python3 scripts/ingest/build_summary_fixture.py
python3 scripts/check-dashboard-invariants.py
```

## CI wiring

- **Job:** `dashboard-build` → `Dashboard invariants` on **committed** `data/latest/summary.json` (catalog parity); then Next build; then `Dashboard static routes`.
- **Job:** `ingest-smoke` → ingest + compare gate only (measured CSV may be fewer rows than catalog).

## When an invariant fails

| Failure | Typical fix |
|---------|-------------|
| Row count &lt; catalog | Run `build_summary_fixture.py` or ingest; commit `data/latest/summary.json` |
| Missing catalog id | Add ingest row in `build_summary.py` / fixture path |
| Banned stub id | Remove from `catalog.toml`; use real package harness ids (`viz_*`, `ml_*`) |
| Missing pillars | Regenerate summary; check `build_pillars()` |
| Static routes low | Rebuild after updating `summary.json`; check `generateStaticParams` |

## Related

- [ARCHITECTURE.md](./ARCHITECTURE.md) — data flow
- [benchmark-dashboard honesty](../honesty/benchmark-dashboard.md) — label semantics
- [coverage-gap-analysis.md](./coverage-gap-analysis.md) — intentional `path=unknown` debt
