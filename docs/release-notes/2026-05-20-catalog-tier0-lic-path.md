# Catalog: tier0_stability path matches lic layout

**Repo:** benchmarks  
**Audience:** ingest, plan-audit, lic maintainers

## Summary

- **`catalog.toml`**: `tier0_stability.path` → **`li-tests/benchmarks/tier0_correctness`** (directory on **lic** where tier-0 sources live; see `lic/benchmarks/harness/verify.py`).
- **`scripts/ingest/build_summary.py`**: stability chart metadata uses the same path.
- **Docs:** [tier-2 catalog sync plan](../ecosystem/plans/2026-05-18-tier2-catalog-lic-sync.md) updated with 2026-05-20 verification; [game-dev map](../game-dev/README.md) notes tier-0 layout.

## Verification

- `LIC_ROOT=/path/to/lic python3 scripts/plan-completion-audit.py` → **`catalog_gaps`: 0** (with **lic** tree containing `li-tests/benchmarks/tier0_correctness/`).

## Cross-repo

- **lic#24** / **benchmarks#17** — human may close when this ships on `main` and ingest stays green.
