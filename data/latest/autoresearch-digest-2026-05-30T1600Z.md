# autoresearch proactive digest — 2026-05-30T16:00Z

Run: proactive · Agent: `autoresearch` · Briefing: `2026-05-30T14:02Z` · Ingest: `2026-05-30T15:32Z`  
**north_star_fit:** scientific computing / compiler numerics — **PH-5b**, **PH-7e**, **G-math** (partial)

---

## Executive summary

- **No tier-1/2 red rows** after fresh ingest (`ecosystem-audit.json` @ 15:32Z); `*_pure_li` does **not** trigger autoresearch via dashboard reds this cycle.
- **Single yellow row:** `matmul_blocked` **1.202×** vs cpp (threshold 1.2×) — **~1.6%** codegen gap; pure-Li blocked GEMM in **lic**, not a missing discretization.
- **`matmul_naive` flipped green** since last sweep (**1.222× → 1.105×**) via `bench_improver` static workspace / MIR (`data/runs/bench_improver-1780154862474.md`); coordinate open lic PR before parallel autoresearch kernels.
- **`horner_pure_li` stays green** (~0.80×); do not reopen unless regression — negative study `docs/numerics/studies/2026-05-17-horner-pure-li-autoresearch-negative.md`.
- **Near-threshold greens:** `matmul_naive` 1.11×, `simd_dot` 1.04×, `fft_1d_fixed` 1.01× — **Mode A (SOTA/codegen)** via `numerics_researcher` / `bench_improver`; not `novel-algorithm` until SOTA gap documented.
- **Control-plane:** 6/8 recent `autoresearch` runs `error` (`unregistered_running_reconciled`); publish path blocked until `swarm_observer` terminalizes SDK runs.
- **117 catalog rows** still lack `lic` harness paths — physics-tier autoresearch **blocked** (`ecosystem-gap` first).
- **This pass:** refreshed signals + ranked hypotheses — **no lic kernel PR** (delegate remaining **1.202×** blocked win to `bench_improver` / PH-7e codegen).

---

## Deliverable / findings

### Dashboard signals (linux, ingest @ 15:32Z)

| Bench | Status | Li/cpp | Threshold | Notes |
|-------|--------|--------|-----------|-------|
| `matmul_blocked` | **yellow** | **1.202** | 1.2 | Pure-Li `mm_blocked_512`; strict gate GAP |
| `matmul_naive` | green (near) | 1.105 | 1.2 | Was yellow; bench_improver pass |
| `horner_pure_li` | green | ~0.80 | 1.2 | `catalog.toml` `variant = "pure_li"` |
| `simd_dot` | green (near) | 1.039 | 1.2 | `@vectorized` / reduction epilogue |
| `fft_1d_fixed` | green (near) | 1.007 | 1.2 | FFTW oracle variant |
| `num_integ_rk4` | green | — | 1.2 | Dropped from near-threshold cluster |

Source: `data/latest/ecosystem-audit.json`, `data/latest/summary.json`, `data/runs/bench_improver-1780154862474.md`.

### Mode decision (methodology)

| Target | Mode | Rationale |
|--------|------|-----------|
| `matmul_blocked` | **B candidate** (codegen) | Goto/BLIS already in cpp oracle; gap is Li MIR → LLVM micro-kernel |
| `matmul_naive`, `simd_dot`, `fft_1d_fixed` | **A** | Standard recipes; squeeze via PH-7e lowering, not new numerics |
| `horner_pure_li` | **Closed** | Green; prior autoresearch negative superseded |
| Catalog-only (117) | **Blocked** | No `lic/benchmarks/...` path |

### Ranked hypotheses (next **lic** pass — not novel algorithms)

| ID | Hypothesis | Falsifiable metric | Novel? |
|----|------------|-------------------|--------|
| **H-blocked-1** | Blocked IKJ lacks cpp-grade register blocking / FMA tile (PH-7e). | `matmul_blocked@linux` Li/cpp ≤ **1.20**; tier-0 vs `matmul_blocked_core.c` | No |
| **H-blocked-2** | Module-static workspace helps naive but blocked hot loop still scalar-bound. | Isolate `mm_blocked_512_acc` vs full driver; `LI_TIER1_PERF_STRICT=1` | No |
| **H-simd-1** | `simd_dot` gap is vector width / reduction epilogue. | Li/cpp ≤ 1.05, no accuracy regression | No |
| **H-fft-1** | Li FFT stub vs FFTW reference — vendor parity, not new transform. | Mode A study only | No |

**Rejected / defer this cycle:**

- New blocking scheme beyond Goto/BLIS — oracle mismatch.
- Relax `threshold_ratio_cpp` — human approval only.
- Fused RK4 (H-rk4-1) — dropped from near-threshold; reopen only if ratio regresses >1.08×.
- Physics-tier autoresearch — 117 harness gaps.

### Evidence in repo

- `docs/numerics/studies/2026-05-17-horner-pure-li-autoresearch-negative.md`
- `docs/numerics/studies/2026-05-17-near-threshold-tier12.md`
- `lic/docs/numerics/studies/2026-05-30-bench-improver-proactive-sweep.md` (matmul naive green)
- `docs/numerics/research-methodology.md`

### Agent deliverable checklist (digest-only)

```markdown
<!-- li-agent -->
## Agent deliverable
- [ ] li-tests or lit test id: `…` — **deferred** (no lic PR this pass)
- [x] Bench row / benchmarks path: `data/latest/ecosystem-audit.json` — `matmul_blocked`, near-threshold rows
- [x] Lean/contracts path documented or N/A — N/A: digest-only; codegen cites **G-math** partial, no `trusted.lean`
- [x] Negative result documented — Horner closed; matmul blocked not tested in-agent (bench_improver owns)
```

### Control-plane (`agent_runs`, last 8 `autoresearch`)

| run_id | status | error |
|--------|--------|-------|
| `autoresearch-1780155752758` | running | — |
| `autoresearch-1780155584878` … | error | `unregistered_running_reconciled` |

Swarm hygiene: `data/runs/ecosystem_grader-1780152735271.md` — fix terminalization before autoresearch PR pipeline.

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| PH-7e: `matmul_blocked` ≤1.2× — blocked IKJ micro-kernel / clang parity (~1.6% win) | **lic** | `PH-7e`, `PH-5b`, `numerics-research` |
| Merge / unblock bench_improver matmul stack (naive green, blocked 1.202×) | **lic** | PRs [#552](https://github.com/li-langverse/lic/pull/552), [#550](https://github.com/li-langverse/lic/pull/550), [#499](https://github.com/li-langverse/lic/pull/499) — fix CI |
| Tag `matmul_*` catalog `variant = "pure_li"` for briefing autoresearch trigger | **benchmarks** | `catalog`, `PH-5b` |
| Mode A: `simd_dot`, `fft_1d_fixed` near-threshold squeeze | **lic** | `numerics-research` → **numerics_researcher** |
| Terminalize stuck `autoresearch` SDK runs | **li-cursor-agents** | `ecosystem-meta`, `swarm_observer` |
| Close duplicate numerics-research horner issues (#118, #126, …) | **lic** | `issue-hygiene` |

**Whitepaper (research-findings):** only after lic PR proves `matmul_blocked` ≤1.2× — link **G-math** / PH-7e publish subdir per `research-verticals.md`.

---

## Deferred

- Local `bench.py --tier 1` repro (matrix rows **skip** on dev runner without fresh `LIC_ROOT` build).
- `docs/numerics/algorithms/*.md` — only if shipping fused RK4 with stability argument.
- Tier-2 physics autoresearch — 117 missing harness paths.
- `python3 scripts/numerics-evidence-checklist.py --novel` — after first matmul_blocked evidence PR.
- Merge / self-merge — human `pr_reviewer` + `pr_merger` only.

---

## Commands (next agent with lic checkout)

```bash
cd ../lic/benchmarks/harness
python3 bench.py --tier 1 --only matmul_blocked --runs 20
LI_TIER1_PERF_STRICT=1 ../../scripts/check-tier1-li-vs-cpp.sh

cd ../../benchmarks
LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh
./scripts/benchmark-failures-report.sh
```
