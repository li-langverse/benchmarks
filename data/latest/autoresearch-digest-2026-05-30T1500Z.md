# autoresearch proactive digest — 2026-05-30T15:00Z

Run: proactive · Agent: `autoresearch` · Briefing: `2026-05-30T14:02Z`  
**north_star_fit:** scientific computing / compiler numerics — **PH-5b**, **PH-7e**, **G-math** (partial)

---

## Executive summary

- **No tier-1/2 red rows** in `ecosystem-audit.json` (ingest @ 09:25Z); autoresearch is **not** triggered by `*_pure_li` dashboard reds this cycle.
- **Primary codegen debt:** `matmul_blocked` **1.24×** and `matmul_naive` **1.22×** vs cpp (yellow, threshold 1.2×) — pure-Li drivers in `lic`, not novel discretizations.
- **`horner_pure_li` is green** (0.80× cpp @ linux); prior autoresearch negative study (2026-05-17) superseded by PH-7e / observable-sink fixes — do not reopen Horner unless regression.
- **Near-threshold greens** (`num_integ_rk4` 1.08×, `simd_dot` 1.05×, `fft_1d_fixed` 1.01×) — **Mode A (SOTA/harness)** first; autoresearch deferred unless `numerics_researcher` closes SOTA gap.
- **Open lic perf PRs** [#499](https://github.com/li-langverse/lic/pull/499), [#550](https://github.com/li-langverse/lic/pull/550) target matmul MIR — CI red; coordinate before parallel autoresearch kernels.
- **Control-plane:** 7+ recent `autoresearch` runs ended `error` (`unregistered_running_reconciled`); no shipped numerics evidence this wave — execution hygiene blocks publish path.
- **117 catalog rows** lack `lic` harness paths — autoresearch must not invent physics there until `numerics_researcher` + harness exist (`ecosystem-gap` if measurement missing).
- **This pass:** digest + ranked hypotheses only — **no lic kernel PR** (proof-before-perf; failed upstream CI).

---

## Deliverable / findings

### Dashboard signals (linux, `data/latest/summary.json`)

| Bench | Status | Li/cpp | Threshold | Variant / notes |
|-------|--------|--------|-----------|-----------------|
| `matmul_blocked` | yellow | **1.244** | 1.2 | Pure-Li `mm_blocked_512` MIR; PH-5b |
| `matmul_naive` | yellow | **1.222** | 1.2 | Pure-Li 256³; PH-5b, PH-7e |
| `horner_pure_li` | green | 0.80 | 1.2 | `catalog.toml` `variant = "pure_li"` |
| `num_integ_rk4` | green | 1.083 | 1.2 | near threshold |
| `simd_dot` | green | 1.052 | 1.2 | near threshold |
| `fft_1d_fixed` | green | 1.007 | 1.2 | near threshold |

Tier-1 matrix report: all micro rows **skip** locally (no fresh `bench.py` in workspace) — ratios from last ingest, not re-run this pass.

### Mode decision (methodology)

| Target | Mode | Rationale |
|--------|------|-----------|
| `matmul_*` | **B candidate** (codegen) | SOTA blocking (Goto/BLIS) already in cpp oracle; gap is **Li MIR → LLVM**, not missing algorithm |
| `num_integ_rk4`, `simd_dot`, `fft_1d_fixed` | **A** | Standard RK4 / dot / FFT recipes; no `novel-algorithm` until SOTA survey + harness parity |
| `horner_pure_li` | **Closed** | Green; see `docs/numerics/studies/2026-05-17-horner-pure-li-autoresearch-negative.md` |
| Catalog-only IDs (117) | **Blocked** | No `lic/benchmarks/...` path — file `ecosystem-gap` before autoresearch |

### Ranked hypotheses (next implementation pass in **lic**)

| ID | Hypothesis | Falsifiable metric | Novel? |
|----|------------|-------------------|--------|
| **H-matmul-1** | `mm_blocked_512` / naive Li loops lack cpp-grade **micro-kernel + FMA** vectorization (PH-7e). | `matmul_blocked@linux` Li/cpp ≤ **1.20**; tier-0 checksum vs `matmul_blocked_core.c` | No — match Goto SOTA |
| **H-matmul-2** | Register/LUT init (`mm_lut_a`) pollutes hot path or blocks LICM. | Isolate init vs GEMM via bench split or `volatile_sink` on sum only | No |
| **H-simd-1** | `simd_dot` gap is **@vectorized** width / reduction epilogue, not new dot product. | Li/cpp ≤ 1.05 without accuracy regression | No |
| **H-rk4-1** | RK4 stub uses scalar stages; fused Butcher tableau in MIR could win ≤8%. | `num_integ_rk4` Li/cpp ≤ 1.05 + tier-0 invariant | Maybe — needs algorithm note if fusion changes stability |

**Rejected this cycle (negative / defer):**

- Inventing a new blocking scheme beyond Goto/BLIS for org oracles — **no** (threshold gaming / oracle mismatch).
- Relaxing `threshold_ratio_cpp` for matmul — **no** (human approval only).
- Physics-tier autoresearch without harness — **deferred** (catalog gaps).

### Evidence already in repo

- `docs/numerics/studies/2026-05-17-horner-pure-li-autoresearch-negative.md` — negative (DCE / measurement).
- `docs/numerics/studies/2026-05-17-near-threshold-tier12.md` — Mode A cluster (pre-matmul pure-Li migration).
- `docs/numerics/research-methodology.md` — Mode A/B gates.

### Agent deliverable checklist (this digest only)

```markdown
<!-- li-agent -->
## Agent deliverable
- [ ] li-tests or lit test id: `…` — **deferred** (no lic PR this pass)
- [x] Bench row / benchmarks path: `data/latest/summary.json` — `matmul_blocked`, `matmul_naive`, near-threshold rows
- [x] Lean/contracts path documented or N/A with reason — N/A: digest-only; codegen work cites **G-math** partial, no `trusted.lean`
- [x] Negative result documented if hypothesis rejected — Horner cluster closed (green); matmul/RK4 not tested this pass
```

### Control-plane sample (`agent_runs`, last 8 `autoresearch`)

| run_id | status | error |
|--------|--------|-------|
| `autoresearch-1780153055162` | running | — |
| `autoresearch-1780151421916` | error | `unregistered_running_reconciled` (+ partial digest) |
| `autoresearch-1780151296280` … | error | `unregistered_running_reconciled` |

Swarm execution drift: see `data/runs/ecosystem_grader-1780152735271.md` — fix terminalization before relying on autoresearch PR pipeline.

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| PH-7e: pure-Li `matmul_blocked` / `matmul_naive` ≤1.2× cpp (MIR micro-kernel, no catalog threshold change) | **lic** | `PH-7e`, `numerics-research`, bench-improvement |
| Unblock / supersede matmul bench PRs: restore tier-1 MIR fast paths | **lic** | PR [#499](https://github.com/li-langverse/lic/pull/499), [#550](https://github.com/li-langverse/lic/pull/550) — fix CI, then re-ingest |
| Tag `matmul_*` catalog rows `variant = "pure_li"` for briefing autoresearch trigger | **benchmarks** | `catalog`, `PH-5b` |
| Mode A sweep: near-threshold `simd_dot`, `num_integ_rk4`, `fft_1d_fixed` | **lic** | `numerics-research` (delegate **numerics_researcher**) |
| Terminalize stuck `autoresearch` SDK runs; reconcile CP status | **li-cursor-agents** | `ecosystem-meta`, `swarm_observer` |
| Close or sync stale `chore/agent-autoresearch-*` digest branches (no open PR) | **benchmarks** | `pr-branch-hygiene` |

**Optional whitepaper (research-findings):** only after lic PR proves matmul ≤1.2× — link to goal `G-math` / PH-7e publish subdir per `research-verticals.md`.

---

## Deferred

- Local `bench.py --tier 1` repro on this host (matrix all **skip** — needs `LIC_ROOT` build + ingest refresh).
- New `docs/numerics/algorithms/*.md` — required only if **H-rk4-1** ships fused RK4 with stability argument.
- Tier-2 physics autoresearch — blocked by 117 missing harness paths.
- `python3 scripts/numerics-evidence-checklist.py --novel` — run after first lic matmul evidence PR, not on digest-only pass.
- Merge / self-merge any PR — human `pr_reviewer` + `pr_merger` path only.

---

## Commands (next agent with lic checkout)

```bash
cd ../lic/benchmarks/harness
python3 bench.py --tier 1 --bench matmul_blocked,matmul_naive --runs 5

cd ../../benchmarks
LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh
python3 scripts/numerics-evidence-checklist.py \
  --study docs/numerics/studies/YYYY-MM-DD-matmul-pure-li-ph7e.md \
  [--novel]
```
