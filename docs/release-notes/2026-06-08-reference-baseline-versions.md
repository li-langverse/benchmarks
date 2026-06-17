# Release notes: 2026-06-08 — HPC reference baseline version policy

**Status:** Ready for review  
**Repo:** li-langverse/benchmarks  
**Issue:** [benchmarks#27](https://github.com/li-langverse/benchmarks/issues/27)  
**PH / REQ:** PH-5b, PH-7e, G-math  
**Author:** code_implementer (`b377faf9`)

---

## Summary (one sentence)

Adds normative **SOTA version pins** and bump cadence for Eigen, Kokkos, PETSc, and Chapel plus an **agent tooling parity** rubric (Chapel CLS / `chplcheck` vs Li Vision-LLM / `lic diagnose`).

## Changed

| Area | What |
|------|------|
| Policy | `docs/honesty/reference-baseline-versions.md` — pin table, quarterly + 30-day bump rules, reference C++ scope honesty |
| Handbook | Cross-link under Benchmark honesty |
| Explorer | HPC rubric link + refresh workflow in `docs/ecosystem/ecosystem-explorer.md` |

## Agent continuation

1. After merge: close #27 with `org-close-issue.py --reason already_implemented`.
2. **lic** follow-up: optional CMake pins for vendor oracles — separate issue; cite this doc when landing.

## Not changed

- Catalog thresholds or ingest logic
- **lic** reference build CMake (deferred per triage)

## Tests

- Docs-only PR; `python3 -m pytest tests/ -q` (repo unit tests)

## CHANGELOG entry (Unreleased)

- **Docs:** HPC reference baseline version policy for Eigen/Kokkos/PETSc/Chapel (#27).
