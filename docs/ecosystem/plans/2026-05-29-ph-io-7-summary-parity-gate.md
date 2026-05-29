# PH-IO-7: summary.json Li/Python parity gate until std.summary ships (REQ-BENCH-INGEST-7)

> **Issue:** [#53](https://github.com/li-langverse/benchmarks/issues/53) · **Repo:** li-langverse/benchmarks (+ **lic** `std.summary`)  
> **Vision:** **easy**, **ai-first** (deterministic ingest) · **Learned from:** [PH-IO release notes](../release-notes/2026-05-16-ingest-summary-ph-io-7.md), `scripts/ingest/summary-compare-gate.sh`, [lic#13](https://github.com/li-langverse/lic/issues/13) (std.io/csv/summary/plot), [ARCHITECTURE.md](../../dashboard/ARCHITECTURE.md)

## Goal

Keep **`build_summary.py`** as an auditable reference while `build_summary.li` matures, but enforce a **fail-closed parity gate** in CI: Li fixture output must match Python on benchmark **status** fields for the fixture catalog. When **lic** ships `std.summary`, switch ingest primary path to Li and tighten gate to numeric tolerance where defined.

## Non-goals

- New Python ingest features beyond parity comparison.
- Removing Python fallback before `std.summary` compiles on `lic` `main`.
- Dashboard-only work without ingest contract.

## Dependencies

| ID | Owner | Notes |
|----|-------|-------|
| **PH-IO-7** | lic | `std.summary` module |
| **PH-IO-4** | lic | `std.csv` / `std.io` (prerequisite chain) |
| lic#13 | lic | Parent tracking issue for std modules |
| Gate scripts | benchmarks | `summary-compare-gate.sh`, `compare_summary_outputs.py` — **exist** |

## Current state (2026-05-29)

- CI runs `./scripts/ingest/summary-compare-gate.sh` after building **lic** (`.github/workflows/ci.yml`).
- Gate **skips** (exit 0) when lic not built or `std.summary` missing — correct for now, but issue asks for explicit parity policy documentation and stricter future behavior.

## Sub-phases

| Sub | Deliverable | Exit gate |
|-----|-------------|-----------|
| A | Document parity contract in `docs/dashboard/INVARIANTS.md` + this plan | Agents know skip vs fail rules |
| B | `compare_summary_outputs.py`: optional `--strict-numeric` flag (default off until std.summary) | Unit test with fixture JSON |
| C | When lic `std.summary` lands: `build-summary-li.sh` primary in `ingest-lic.sh`; gate must **fail** on status mismatch (no silent skip) | CI red on divergence |
| D | Remove `python-fallback` heuristic from explorer once Li path default | `ecosystem-explorer.json` updated |
| E | Close #53; keep lic#13 open until full std/plot | Labels |

## Tests / benches

| Test | Path |
|------|------|
| Parity gate | `scripts/ingest/summary-compare-gate.sh` |
| Fixture | `scripts/ingest/fixtures/summary/`, `build_summary_fixture.li` |
| Compare | `scripts/ingest/compare_summary_outputs.py` |
| CI | `ingest-smoke` job in `.github/workflows/ci.yml` |

No tier-1 perf bench; ingest correctness only.

## Provability

- **G-meta** — ingest scripts are outside proof certificate; honesty via CI gate, not Lean.
- Do not claim “proved ingest” — document as test-gated pipeline.

## Rollout

1. **benchmarks** PR (docs + optional compare flag): after `plan-approved`.
2. **lic** PR: `std.summary` + flip ingest primary (blocked on lic#13 / PH-IO-7).
3. Post issue comment on #53 and cross-link lic#13.

## Human-only

- Maintainer `plan-approved` on benchmarks plan before tightening CI skip behavior.
