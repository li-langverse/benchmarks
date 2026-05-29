# Proof gap researcher digest — 2026-05-29 (cycle 13)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-manifest-verify-ok-honesty`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-2e, PH-2f — certificate honesty (G-test-verify)

## Executive summary

- **Focus:** **G-test-verify** — manifest `verify_ok` conflates compile+Lean typecheck with full property verification; no `prove_lean_ok` outcome yet.
- **Verified:** `run_all.sh:91-98` maps `verify_ok` → plain `lic build` (no `--strict-lean`).
- **Verified:** `index_refinement.li` is `verify_ok`, passes build and `--strict-lean`, but AutoVC `requires := True` — certificate is syntactically closed, semantically empty (**G-bnd / P-refine** interaction).
- **Verified:** `sqrt_open_bound.li` correctly uses `verify_open_ok` (not `verify_ok`); default build fails without `--allow-open-vc`.
- **Harness:** `manifest_verify_ok_honesty_gap.sh` added; wired into `contracts_discharge_corpus.sh`; run → ok.
- **Retest:** `parallel_decorator_policy_capture_gap.sh`, `sqrt_open_bound_verify_cli_order.sh` → ok.
- **No `trusted.lean` edits.**

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| `verify_ok` = `lic build` only | `li-tests/run_all.sh:91-98` |
| Default build skips `--check-open-goals` in lean script | `lean-verify-stub.sh:7-22`; `--strict-lean` adds second open-goal pass via `main.cpp:606-607` |
| True-stub specimens pass strict gate | `index_refinement.li` + `--strict-lean` → exit 0; AutoVC `vc_get_requires_0 := True` |
| Lake absent → build skips Lean with warning | `main.cpp:300-303` (environment-dependent honesty gap) |

### 2. Contract gaps

- **Manifest naming:** `verify_ok` implies verification; `proof-corpus-roadmap.md:95-99` documents need for `prove_compile_ok` + `prove_lean_ok` split — **not implemented** in `manifest.toml`.
- **P-refine:** `index_refinement.li` passes all manifest gates while bounds Props are stubbed `True` — agents reading `PASS verify_ok` may overclaim bounds proved.
- **Tier separation works for open VCs:** `sqrt_open_bound.li` is `verify_open_ok`; default `lic build` fails (open Prop).

### 3. Trusted surface

- `trusted.lean` unchanged (Net v1 axioms only; `docs/semantics/trusted.lean:1-41`).
- Hole is **manifest / CI outcome semantics**, not axiom growth.

### 4. External trust boundaries

- Splitting manifest outcomes (`prove_lean_ok`) is a **lic** harness + manifest change — human PR, no trusted.lean.
- `--strict-lean` alone does not catch True-stub semantic gaps; **P-refine** discharge in `Discharge.lean` required.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-test-verify** | `run_all.sh:91-98` |
| **G-test-verify** | `manifest.toml:229-230` — `index_refinement.li` → `verify_ok` |
| **G-bnd** / **P-refine** | `AutoVC.lean:12-13` — `vc_get_requires_0 := True` |
| **G-vc** / **P-float** | `manifest.toml` — `sqrt_open_bound.li` → `verify_open_ok` |
| **G-par** (retest) | `bash li-tests/tooling/parallel_decorator_policy_capture_gap.sh` → ok |
| **G-test-verify** (retest cycle 12) | `bash li-tests/tooling/sqrt_open_bound_verify_cli_order.sh` → ok |
| **Harness** | `bash li-tests/tooling/manifest_verify_ok_honesty_gap.sh` → ok |
| **Corpus** | `bash li-tests/tooling/contracts_discharge_corpus.sh` → ok |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — verify_ok runs lic build without --strict-lean | evidence: run_all.sh:91-98; manifest_verify_ok_honesty_gap.sh`
- `HYPOTHESIS: verified — prove_lean_ok outcome not in manifest | evidence: manifest.toml grep; manifest_verify_ok_honesty_gap.sh`
- `HYPOTHESIS: verified — index_refinement passes verify_ok and --strict-lean with True stub requires | evidence: AutoVC vc_get_requires_0 := True; manifest_verify_ok_honesty_gap.sh`
- `HYPOTHESIS: verified — sqrt_open_bound uses verify_open_ok not verify_ok | evidence: manifest.toml; manifest_verify_ok_honesty_gap.sh`
- `HYPOTHESIS: falsified — --strict-lean rejects True-stub refinement certificates | evidence: index_refinement --strict-lean exit 0`
- `HYPOTHESIS: falsified — verify_ok specimens with open Props pass default build | evidence: sqrt_open_bound default build exit 1`
- `HYPOTHESIS: deferred — split manifest prove_lean_ok + semantic VC audit | evidence: proof-corpus-roadmap.md G-test-verify row`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| feat(G-test-verify): add prove_lean_ok manifest outcome + run_all wiring | **lic** | `PH-2f`, provability |
| test(provability): manifest_verify_ok_honesty_gap regression harness | **lic** | G-test-verify, research |
| docs: provability-gaps G-test-verify — True-stub verify_ok overclaim | **lic** | provability-gaps |
| feat(P-refine): real Lean Props for Index10 bounds (index_refinement) | **lic** | `PH-2e`, `PH-2f` |

## Deferred

- **G-par** `disjoint_elem` + `buf[0]` (cycle 10 — not retested this pass).
- **G-dec** `@parallel` decorator-for elaboration to OpenMP (cycle 8 — not retested).
- **G-bnd** guarded refinement path VCs (cycle 11 — not retested in depth).
- **G-meta** mat2 MIR↔Lean codegen drift (cycle 9 — not retested).
- **G-net** trusted codegen legacy `tcp_recv` ptr vs `tcp_recv_stub : Net Nat` in emit.cpp (needs dedicated focus).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
