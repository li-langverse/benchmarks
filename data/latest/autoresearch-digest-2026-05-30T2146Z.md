# autoresearch proactive digest — 2026-05-30T21:46Z

Run: proactive · Agent: `autoresearch` · Briefing: `2026-05-30T21:46Z` · Ingest: `2026-05-30T15:32Z`  
**north_star_fit:** scientific computing / compiler numerics — **PH-5b**, **PH-7e**, **G-math** (partial)

---

## Executive summary

- **No tier-1/2 red rows** after ingest (`ecosystem-audit.json` @ 21:45Z); autoresearch trigger is **yellow + near-threshold**, not dashboard reds.
- **Single yellow row:** `matmul_blocked` **1.202×** vs cpp (~1.6% over 1.2× cap) — PH-7e blocked IKJ codegen, not missing numerics recipe.
- **Harness drift on agent workspace (`3710a3c7`):** `matmul_blocked/li` uses **64×64×512-rep micro-GEMM** vs C **512×512** oracle — local Li/cpp **0.05× is invalid**; do not publish perf from this branch without syncing `mm_blocked_512` driver from sibling `lic`.
- **`bench.py --verify` broken:** `TypeError: TimingStats * float` at DCE guard (line 736) — file **`ecosystem-gap`** before autoresearch kernel PRs.
- **Near-threshold greens unchanged:** `matmul_naive` 1.105×, `simd_dot` 1.039×, `fft_1d_fixed` 1.007× — Mode A (`bench_improver` / `numerics_researcher`).
- **`horner_pure_li` dashboard green (0.80×)**; local spot-check 2.8× on agent branch — codegen variance, not novel Horner.
- **7/8 recent control-plane `autoresearch` runs errored** before this run; orchestration hygiene still open.
- **Negative novel result:** no `docs/numerics/algorithms/*.md` or kernel PR this cycle.

---

## Deliverable / findings

### Dashboard signals (linux, ingest @ 15:32Z)

| Bench | Status | Li/cpp | Threshold | Notes |
|-------|--------|--------|-----------|-------|
| `matmul_blocked` | **yellow** | **1.202** | 1.2 | Pure-Li blocked GEMM |
| `matmul_naive` | green (near) | 1.105 | 1.2 | MIR FMA IKJ |
| `horner_pure_li` | green | 0.80 | 1.2 | Prior autoresearch negative closed |
| `simd_dot` | green (near) | 1.039 | 1.2 | `@vectorized` epilogue |
| `fft_1d_fixed` | green (near) | 1.007 | 1.2 | FFTW oracle variant |

### Local spot-check (workspace @ `3710a3c7`, `--skip-verify`)

| Bench | cpp (s) | li (s) | li/cpp | Trust |
|-------|---------|--------|--------|-------|
| `matmul_blocked` | 0.0086 | 0.0004 | 0.05× | **No** — wrong problem size |
| `matmul_naive` | 0.0018 | 0.0004 | 0.22× | Partial — MIR hook |
| `horner_pure_li` | 0.0005 | 0.0014 | 2.80× | Variance vs ingest |
| `simd_dot` | 0.0186 | 0.0180 | 0.97× | OK |
| `fft_1d_fixed` | 0.0152 | 0.0153 | 1.01× | OK |

Evidence: `lic/benchmarks/results/latest.csv`; study `lic/docs/numerics/studies/2026-05-30-autoresearch-proactive-sweep-v3.md`.

### Mode decision

| Target | Mode | Rationale |
|--------|------|-----------|
| `matmul_blocked` | **A (codegen)** | Goto/BLIS in cpp oracle; ~1.6% Li emit gap |
| `matmul_naive`, `simd_dot`, `fft_1d_fixed` | **A** | Standard recipes; PH-7e lowering |
| `horner_pure_li` | **Closed** | Green on dashboard; prior negative study |
| Agent-branch matmul harness | **Blocked** | Oracle mismatch — sync from `dev` first |

### Hypotheses rejected (novel)

- Li-specific blocking scheme beyond Goto/BLIS — **reject** (SOTA sufficient).
- 64³ rep-tile as performance strategy — **reject** (invalid oracle; honesty violation).
- New Horner scheme — **reject** (closed negative).

### Control-plane (`agent_runs`, last 8 `autoresearch`)

| run_id | status |
|--------|--------|
| `autoresearch-1780177654969` | running (this pass) |
| `autoresearch-1780177261937` … 7 others | error |

### Agent deliverable checklist

```markdown
<!-- li-agent -->
## Agent deliverable
- [x] li-tests or lit test id: N/A — study-only triage
- [x] Bench row / benchmarks path: `data/latest/ecosystem-audit.json`; `lic/benchmarks/results/latest.csv` @ 3710a3c7
- [x] Lean/contracts path documented or N/A — N/A; no trusted.lean changes
- [x] Negative result documented — yes; harness drift + novel hypotheses rejected
```

---

## Recommended issues/PRs

| Title | Repo | Labels |
|-------|------|--------|
| PH-7e: `matmul_blocked` ≤1.2× — blocked IKJ micro-kernel (~1.6% win) | **lic** | `PH-7e`, `PH-5b`, `numerics-research` |
| Sync agent workspace `matmul_blocked/li` to `mm_blocked_512` oracle driver | **lic** | `ecosystem-gap`, `benchmark-harness` |
| Fix `bench.py` verify DCE guard (`TimingStats.mean`) | **lic** | `ecosystem-gap`, `benchmark-harness` |
| Mode A near-threshold squeeze: `matmul_naive`, `simd_dot`, `fft_1d_fixed` | **lic** | `numerics-research` → **bench_improver** |
| Terminalize stuck `autoresearch` SDK runs (7 errors today) | **li-cursor-agents** | `ecosystem-meta`, `swarm_observer` |
| Increase pure_li catalog variants for PH-7e codegen proof | **benchmarks** | `catalog`, `PH-5b` |

**Whitepaper:** defer until lic PR proves `matmul_blocked` ≤1.2× with oracle parity — link PH-7e publish subdir per `research-verticals.md`.

---

## Deferred

- `docs/numerics/algorithms/*.md` — only after proven novel win with full evidence pack.
- Tier-2 physics autoresearch — catalog harness gaps remain.
- `python3 scripts/numerics-evidence-checklist.py --novel` — after first matmul_blocked evidence PR.
- Merge / self-merge — human `pr_reviewer` + `pr_merger` only.

---

## Commands (next agent with synced lic checkout)

```bash
cd lic && ./scripts/build.sh
export LIC=$PWD/build/compiler/lic/lic
cd benchmarks/harness
python3 bench.py --tier 1 --only matmul_blocked --runs 20 --verify
LI_TIER1_PERF_STRICT=1 ../../scripts/check-tier1-li-vs-cpp.sh

cd ../../benchmarks
LIC_ROOT=../lic ./scripts/ingest/ingest-lic.sh
./scripts/benchmark-failures-report.sh
```
