# Package architect digest — 2026-05-29

**Agent:** `package_architect` · **Briefing:** `2026-05-29T08:40Z` · **Mode:** plan (no product code)

## Executive summary

- Cleared **5** `pending_placement` handoffs via MCP `record_placement_decision`; swarm scorecard `pending_placement` is now **0**.
- **stdlib_ecosystem** → `create_monorepo` **`packages/linalg`** in **lic** (AL-10; prelude owns GEMM, LAPACK-class APIs missing).
- **chem_sim_algorithms** → **extend** `packages/li-sim-scientific` in **lic** (qm_dft SCF smoke 418; integrals 401–404 first).
- **robotics_systems** → **extend** `packages/li-sim-robotics` in **lic** (wire `robo_plan_rrt` harness; catalog paths are stubs today).
- **provability_holes** (×2 handoffs) → **extend** lic compiler + `docs/verification` + `li-tests/contracts_verify` (PH-2e/PH-2f).
- **2** implementation handoffs already `pending` with `target_repo: lic` (chem, robotics) — now aligned with placement.
- Secondary work (not blocking placement): `li-std-math` contract parity, `benchmarks` catalog path fixes, tier-0 verify README.
- **North star:** proof → easy → fast; no `trusted.lean` edits from this pass.

## Deliverable / findings

### Placement decisions (recorded in control plane)

| Handoff | Goal | Action | Target | Path |
|---------|------|--------|--------|------|
| `d23a0516…` | `stdlib_ecosystem` | `create_monorepo` | `lic` | `packages/linalg` |
| `813f6ec5…` | `chem_sim_algorithms` | `extend_existing` | `lic` | `packages/li-sim-scientific` |
| `0f6a2539…` | `robotics_systems` | `extend_existing` | `lic` | `packages/li-sim-robotics` |
| `472cbfa9…` | `provability_holes` | `extend_existing` | `lic` | `compiler/lic`, `docs/verification`, `li-tests/contracts_verify` |
| `71d7ff43…` | `provability_holes` | `extend_existing` | `lic` | same (superseded by session `97b0a884`) |

### Per-goal rationale (condensed)

**stdlib_ecosystem** — Cycle 1 ([stdlib_ecosystem-cycle.md](https://github.com/li-langverse/lic/blob/main/docs/ecosystem/research-sessions/stdlib_ecosystem-cycle.md)): 25 `std/**` modules; only `bytes` + `runtime.seam` are real; dense LA is prelude/compiler. Build `PKG-li-linalg` before `std.tensor` / `std.sparse` facades. Wave A still blocks WP0-B collections runtime.

**chem_sim_algorithms** — Cycle 1: all 32 `qm_*` catalog rows unknown; `run_algo_registry_stub` checksum 1.001. v1 = `chem-r2-dft-scf-gap` on registry id 418 with Psi4 oracle; defer `li-physics-quantum` org package until smoke green.

**robotics_systems** — `robo_*` ids exist in `benchmarks/catalog.toml` but paths point at wrong harnesses; `li-sim-robotics` already has smoke ticks. v1 = one deterministic bench slice, not new algorithms.

**provability_holes** — `lic build` now emits AutoVC; G-meta/G-lean Partial. Migrate high-value `verify_ok` → `prove_lean_ok`; MIR.lean precursor; document tier-0 `--allow-open-vc` downgrade in benchmarks README.

### Follow-on implementer queue (from research, not re-placed)

| P | Item | Repo | Agent |
|---|------|------|-------|
| 2 | Pure-Li `simd_dot` tier-1 bench | `lic` | `code_implementer` |
| 3 | `matmul_blocked` / `horner_pure_li` strict perf | `lic` | `bench_improver` |
| 4 | `li-std-math` vec3_dot contract parity | `li-std-math` | `code_implementer` |
| — | Fix `robo_*` catalog `path` fields | `benchmarks` | `bench_improver` |
| — | `verticals.toml` qm_dft honesty | `benchmarks` | after lic smoke |

## Recommended issues/PRs

| Repo | Title | Labels |
|------|-------|--------|
| `lic` | feat(linalg): scaffold AL-10 package + composable import smoke | `pillar:provable`, `AL-10` |
| `lic` | chem-r2: qm_dft_scf_energy harness + Psi4 oracle (418) | `numerics-research`, `bench` |
| `lic` | robo: wire robo_plan_rrt composable + deterministic seed | `robotics`, `bench` |
| `lic` | feat(verify): migrate contracts_verify rows to prove_lean_ok | `pillar:provable`, `PH-2f` |
| `lic` | feat(semantics): MIR.lean preservation sketch (G-meta precursor) | `pillar:provable`, `PH-2e` |
| `benchmarks` | chore(bench): fix robo_* catalog paths + document tier-0 verify downgrade | `pillar:provable` |
| `li-std-math` | fix: align vec3_dot ensures with packages/li-math | `ecosystem` |

## Deferred

- `std.tensor` / `std.sparse` / `std.summary` / `std.plot` — after `packages/linalg` and Wave A unblock.
- `li-physics-quantum` org package (`chem-r3`) — after chem-r2 smoke.
- `trusted.lean` edits — human-approved issues only.
- ROS2 / hardware I/O bridges for robotics — dedicated researcher agent later.
- G-meta full compiler ≡ Lean proof — blocked on MIR.lean + preservation.

## Error

None this run.
