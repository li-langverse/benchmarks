# LIC_ROOT catalog alignment (issues #17–#20, #38)

## Summary

Aligns `catalog.toml` paths with the **lic** tree and vendored tier-5 harness, hardens `plan-completion-audit.py` against phantom gaps, and documents agent-kit sync for **benchmarks#38**.

## Agent continuation

1. **Read:** `catalog.toml` (`tier0_stability`, `rate_limit_429`, `fft_1d_fixed`), `scripts/plan-completion-audit.py`, `docs/ecosystem/agent-kit-sync.md`, `.github/workflows/plan-completion-audit.yml`.
2. **Run:** `LIC_ROOT=../lic python3 scripts/plan-completion-audit.py` — expect `catalog_gaps` = 0 with sibling lic@dev; `python3 scripts/agent-briefing.py --skip-slow`.
3. **Next:** **lic** PR for `benchmarks/tier1_micro/fft_1d_fixed` harness (**#18**, `plan-approved`); `install-agent-kit.sh` if roadmap stamp moves (**#38**).
4. **Blocked:** algo_registry rows with `path = unknown` remain ingest `unknown` until harness dirs land in **lic**.

## Changed

| Area | Paths / IDs |
|------|-------------|
| Catalog | `tier0_stability` → `li-tests/benchmarks/tier0_correctness` (**#17**); `rate_limit_429` → vendor tier-5 path (**#20**); `fft_1d_fixed` planned row (**#18**) |
| Audit | `scripts/plan-completion-audit.py` — multi-repo roots; skip `unknown`/`planned` |
| CI | `.github/workflows/plan-completion-audit.yml`, `ecosystem-audit.yml`, `ecosystem-explorer.yml` — `lic@dev`, absolute `LIC_ROOT` |
| Docs | `docs/ecosystem/plan-cross-links.md`, `docs/ecosystem/agent-kit-sync.md` (**#38**) |
| Tier-2 | Gaming-physics rows match **lic** `dev` tree (**#19**) |

## Not changed

- **lic** harness implementation (FFT kernel, tier-0 measurement CSV).
- `vendor/lis-tier5` harness source (catalog pointer only).
- Agent-kit hook semantics or roadmap governance merge policy.

## Breaking

N/A — catalog path corrections only.

## Security

N/A — no trusted creep.

## Performance

N/A — audit/CI checkout only.

## Downstream

- Close **benchmarks#17, #19, #20** when PR merges; **#18** open until lic harness lands.
- **li-cursor-agents** briefing shows fewer phantom `catalog_gaps` after snapshot refresh.
