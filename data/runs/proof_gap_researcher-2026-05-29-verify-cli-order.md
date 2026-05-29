# Proof gap researcher digest — 2026-05-29 (cycle 12)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-verify-cli-order`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-2e, PH-2f — certificate honesty (G-vc / G-test-verify)

## Executive summary

- **Focus:** **G-vc / G-test-verify** — `lic verify --lean --strict-lean` CLI argument order vs `sqrt_open_bound` open Float.abs VC.
- **Verified:** `lic verify file --lean --strict-lean` correctly fails (exit 1, `open_vc_goals=1`, `strict-lean failed`).
- **Verified (new hole):** `lic verify --lean --strict-lean file` treats `argv[2]` as path → reads `--lean` as filename → empty module (`procs=0`), emits empty AutoVC, **`--strict-lean` false-passes** (exit 0).
- **Root cause:** `main.cpp:498-516` — verify subcommand does not scan for file path; only `argv[2]` is used.
- **Harness:** `sqrt_open_bound_verify_cli_order.sh` added; wired into `contracts_discharge_corpus.sh`; run → ok.
- **Retest:** `sqrt_open_bound_contract_tier.sh` → ok (P-float ensures still intentionally open).
- **No `trusted.lean` edits.**

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| Verify uses fixed `argv[2]` as input path | `compiler/lic/main.cpp:498-516` |
| Flags-before-file → empty module | `lic verify --lean --strict-lean sqrt_open_bound.li` → `procs=0` |
| File-before-flags → real VCs | `lic verify sqrt_open_bound.li --lean --strict-lean` → `procs=2`, AutoVC `namespace sqrt_open` |
| Build gate unaffected | `lic build sqrt_open_bound.li` still exit 1 without `--allow-open-vc` |

### 2. Contract gaps

- **P-float (`sqrt_open_bound`):** ensures still `Float.abs ((result * result) - x) < 1e-12` with no `_proved` theorem (`AutoVC.lean:13`) — intentional open per **G-vc**.
- **Verify telemetry:** `summarize_vcs` only counts `module.procs` (`vc_summary.cpp:44-51`); when CLI misparses path, telemetry shows zero contracts and misleads agents/CI.

### 3. Trusted surface

- `trusted.lean` unchanged (Net v1 axioms only; `docs/semantics/trusted.lean:1-41`).
- Hole is **CLI / verify orchestration**, not axiom growth.

### 4. External trust boundaries

- Fixing verify argv parsing is a **lic** compiler change (`main.cpp`); human PR — no trusted.lean.
- Usage docs show `lic verify <file> [--lean]` (`main.cpp:38`) but do not warn that flags-before-file is unsound today.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-test-verify** | `main.cpp:498-516` |
| **G-test-verify** | `lic verify --lean --strict-lean li-tests/contracts_verify/sqrt_open_bound.li` → exit 0, `procs=0` |
| **G-test-verify** (control) | `lic verify li-tests/contracts_verify/sqrt_open_bound.li --lean --strict-lean` → exit 1 |
| **G-vc** / **P-float** | `bash li-tests/tooling/sqrt_open_bound_contract_tier.sh` → ok |
| **Harness** | `bash li-tests/tooling/sqrt_open_bound_verify_cli_order.sh` → ok |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — verify --lean --strict-lean with flags before file false-passes strict gate | evidence: exit 0 procs=0; sqrt_open_bound_verify_cli_order.sh`
- `HYPOTHESIS: verified — verify with file before flags fails strict-lean on open sqrt ensures | evidence: exit 1 open_vc_goals=1; sqrt_open_bound_verify_cli_order.sh`
- `HYPOTHESIS: verified — root cause is argv[2] fixed path in verify subcommand | evidence: main.cpp:516`
- `HYPOTHESIS: falsified — verify always emits sqrt_open AutoVC regardless of flag order | evidence: empty AutoVC with flags-first`
- `HYPOTHESIS: falsified — build path shares the same argv bug for --strict-lean | evidence: build parses flags in loop after input (main.cpp:547-571)`
- `HYPOTHESIS: deferred — close P-float sqrt_open_bound ensures | evidence: sqrt_open_bound_contract_tier.sh; P-float open`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| fix(G-test-verify): lic verify accept flags before/after file path | **lic** | `PH-2f`, provability, bug |
| test(provability): sqrt_open_bound_verify_cli_order regression harness | **lic** | G-test-verify, research |
| docs: provability-gaps G-test-verify row — verify CLI ordering hole | **lic** | provability-gaps |
| feat(P-float): discharge sqrt_open Float.abs ensures (sqrt_open_bound) | **lic** | `PH-2e`, `PH-2f` |

## Deferred

- **G-par** `disjoint_elem` + `buf[0]` (cycle 10 — not retested).
- **G-dec** `@parallel` decorator-for policy bypass (cycle 8/10 — not retested).
- **G-bnd** refinement guarded-call AutoVC `True` stub (cycle 11 — not retested).
- **G-meta** mat2 MIR↔Lean codegen drift (cycle 9 — not retested).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
