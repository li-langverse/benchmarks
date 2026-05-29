# Proof gap researcher digest — 2026-05-29 (cycle 14)

**Agent:** `proof_gap_researcher` · **Run:** `proof_gap_researcher-2026-05-29-net-trusted-codegen-drift`  
**Goal:** `provability_holes` · **north_star_fit:** ecosystem, PH-2f, PH-H — trusted Net seam honesty (G-net / G-trust)

## Executive summary

- **Focus:** **G-net / G-trust** — triple ABI drift on recv/send: `emit.cpp` legacy C ptr symbols vs `trusted.lean` `Net Nat` stubs vs `seam.li` slot/buffer procs.
- **Verified:** `emit.cpp:1352-1354` predeclares `tcp_recv(conn,max) -> i8*` and `tcp_send(conn, i8*)`; `trusted.lean:33-36` axiomatizes byte-count `tcp_*_stub : Nat → Nat → Net Nat`.
- **Verified:** `seam.li:79-90,520-527` exposes `tcp_recv_slot` / `tcp_recv_nb_i` / `tcp_send_buf` — no plain `tcp_recv`/`tcp_send` in Li surface; zero Li call sites to legacy symbols.
- **Verified:** `tcp_listen`/`tcp_accept`/`tcp_close` align across emit, trusted stubs, and seam (listen/accept policy retest via harness).
- **Related gap:** `tcp_recv_nb_i` / `tcp_send_nb_i` omit `raises Net` in seam while performing syscall I/O — effect propagation hole (documented, not harnessed this pass).
- **Harness:** `net_trusted_codegen_drift.sh` added; wired into `check-w0-bytes-io.sh`; run → ok.
- **No `trusted.lean` edits.**

## Deliverable / findings

### 1. Compiler / semantics gaps

| Item | Evidence |
|------|----------|
| Legacy recv ptr ABI in codegen | `emit.cpp:1352-1354` — `tcp_recv` returns `i8_ptr` |
| Legacy send C-string ABI in codegen | `emit.cpp:1349-1351` — `tcp_send(conn, i8_ptr)` |
| C runtime matches legacy ptr recv | `li_rt_net.c:581-598` — `malloc` + `recv` → `const char*` |
| No Li lowering to legacy symbols | `rg tcp_recv(` over `li-tests/`, `std/`, `packages/` → no matches |
| Listen/accept/close codegen matches seam | `emit.cpp:1345-1357`; `seam.li:49-62` |

### 2. Contract gaps

- **Lean vs codegen:** Proofs against `Li.Trusted.tcp_recv_stub` model **byte counts**; codegen still declares **pointer-return** C ABI — no MIR↔Lean linking path for recv/send (G-meta / G-net).
- **Seam vs trusted:** Accepted RFC v1 lists TcpConn send/recv/close; seam uses slot/buffer variants not named in `trusted.lean` axioms (`tcp_recv_slot`, `tcp_send_buf`, …).
- **Effect tier:** `tcp_recv_nb_i` / `tcp_send_nb_i` lack `raises Net` (`seam.li:520-527`) while `li-net-httpd` calls them from `raises Net` handlers — callers without `raises Net` could invoke nb procs without compile-time rejection (`borrowck.cpp:467-469` only fires when callee declares effect).

### 3. Trusted surface

- `trusted.lean:26-39` — v1 TcpListen/TcpConn stubs unchanged (human-approved RFC scope).
- Drift is **implementation seam alignment**, not unapproved axiom growth.
- `security/trusted-c-audit.toml:107-109` audits C `tcp_recv` — audit target is legacy C symbol, not `tcp_recv_stub` Lean model.

### 4. External trust boundaries

- Aligning emit predecls with seam + trusted models requires **lic** codegen + seam RFC amendment — human review; **no trusted.lean edit** without RFC.
- httpd production path uses `tcp_recv_slot` / `tcp_recv_nb_i` (C in `li_rt_net.c`) — runtime trust boundary stays in audited `li_rt_net.c`.

### 5. Evidence pack

| G-* | File:line / repro |
|-----|-------------------|
| **G-net** | `emit.cpp:1352-1354` vs `trusted.lean:36` |
| **G-net** | `seam.li:79` — `tcp_recv_slot`; no `tcp_recv` |
| **G-trust** | `trusted.lean:33-36` — `tcp_send_stub` / `tcp_recv_stub` |
| **G-net** (C seam) | `li_rt_net.c:581-598` — ptr recv impl |
| **G-net** (effects) | `seam.li:520-527` — nb procs without `raises Net` |
| **Harness** | `bash li-tests/tooling/net_trusted_codegen_drift.sh` → ok |
| **Gate** | `bash scripts/check-w0-bytes-io.sh` (includes drift harness) |
| **Policy retest** | `lic check li-tests/net_trusted/seam_policy_ok.li` → ok |

**Hypothesis outcomes**

- `HYPOTHESIS: verified — emit.cpp declares legacy ptr-ABI tcp_recv while trusted.lean axiomatizes Nat byte count | evidence: emit.cpp:1352-1354; trusted.lean:36; net_trusted_codegen_drift.sh`
- `HYPOTHESIS: verified — seam.li uses tcp_recv_slot not tcp_recv (triple drift) | evidence: seam.li:79; harness rg scan`
- `HYPOTHESIS: verified — no Li source calls legacy tcp_recv symbol | evidence: rg over li-tests/std/packages; net_trusted_codegen_drift.sh`
- `HYPOTHESIS: verified — tcp_send has same emit ptr-ABI vs trusted Nat-count drift | evidence: emit.cpp:1349-1351; trusted.lean:33; net_trusted_codegen_drift.sh`
- `HYPOTHESIS: verified — tcp_listen/accept/close remain aligned across layers | evidence: emit.cpp:1345-1357; seam.li:49-62; seam_policy_ok lic check`
- `HYPOTHESIS: verified — tcp_recv_nb_i omits raises Net despite syscall I/O | evidence: seam.li:520-525; borrowck.cpp:467-469`
- `HYPOTHESIS: falsified — seam.li exposes plain extern tcp_recv matching emit.cpp | evidence: grep seam.li; net_trusted_codegen_drift.sh`
- `HYPOTHESIS: deferred — close emit↔seam↔Lean recv/send alignment | evidence: requires RFC + emit.cpp refactor; human trusted.lean review if axioms change`

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| refactor(G-net): drop legacy emit tcp_recv/tcp_send predecls; align with seam slot/buffer ABI | **lic** | `PH-2f`, G-net, codegen |
| feat(G-net): add raises Net to tcp_recv_nb_i / tcp_send_nb_i + compile_fail policy test | **lic** | G-net, effects |
| docs: provability-gaps G-net — document recv/send triple drift + nb effect gap | **lic** | provability-gaps |
| test(provability): net_trusted_codegen_drift regression harness | **lic** | G-net, research |
| RFC amendment: map trusted.lean stubs to seam.li proc names (TcpConn v1) | **lic** | G-trust, RFC |

## Deferred

- **G-par** `disjoint_elem` + `buf[0]` (cycle 10 — not retested).
- **G-dec** `@parallel` decorator-for elaboration (cycle 8 — not retested).
- **G-test-verify** manifest `prove_lean_ok` split (cycle 13 — not retested).
- **G-vc** `sqrt_open_bound` P-float closure (cycle 6 — not retested).
- **G-bnd** guarded refinement VCs (cycle 11 — not retested).
- Publish to **research-findings** whitepaper (`publish_subdir` not injected this run).
