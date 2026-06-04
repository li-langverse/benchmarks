# Catalog repo honesty — PH-5b plan-completion gaps (#266)

## Summary

Triages `catalog.toml` so `plan-completion-audit.py` reports **0 catalog_gaps** without silent row deletion: workloads-backed rows use `repo = "benchmarks"`, competitive vertical stubs defer to `path = unknown` + `catalog_lifecycle = planned`, and lic-only rows (`tier0_stability`, `proxy_loopback`) are explicitly deferred.

## Agent continuation

1. **Run:** `python3 scripts/catalog/triage-catalog-repo-honesty.py --dry-run` then `LIC_ROOT=../lic python3 scripts/plan-completion-audit.py`.
2. **Next:** Implement lic harnesses for deferred competitive verticals; restore `tier0_stability` / `proxy_loopback` when **lic** paths land.

## Changed

| Area | Paths |
|------|--------|
| Catalog | `catalog.toml` — repo/path honesty, 27 stub defers, tier-5 vendor paths |
| Scripts | `scripts/catalog/triage-catalog-repo-honesty.py`, `scripts/plan-completion-audit.py` |
| Audit snapshot | `data/latest/plan-completion-audit.json` |
| Tests | `tests/test_catalog_repo_honesty.py` |

## IDs

**PH-5b**, closes **benchmarks#266** (catalog audit honesty slice).
