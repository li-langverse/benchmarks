# Autoresearch digest — 2026-05-29

**Agent:** `autoresearch` · **Run:** `autoresearch-1780056266456` · **Source:** proactive  
**Workspace:** `lic` @ `chore/agent-bench_improver-55869194` (clean, aligned with `main`)  
**north_star_fit:** PH-5b, PH-7e — pure-Li codegen discipline; defer novel physics until SOTA implementation path exhausted

## Executive summary

- **Preflight (2026-05-29T10:43Z):** **0 red** benchmark rows; **1 yellow** (`matmul_blocked` @ **1.253×** cpp ingest); **5** tier-2 near-threshold (1.06–1.20×).
- **Catalog `pure_li` variant:** only **`horner_pure_li`** — no other tier-1 `*_pure_li` red trigger for autoresearch.
- **Novel-algorithm PR:** **not opened** — negative survey; SOTA Horner/blocked GEMM sufficient; gaps are **codegen + ingest**, not missing discretizations.
- **Local tier-1 (built `lic`, `bench.py`):** `horner_pure_li` **0.67×** cpp (fast) but **verify FAIL** (Li `x=0.999999` vs oracle `x=1.1`); `matmul_blocked` **1.27×**, checksum **PASS**.
- **Sibling agent:** `bench_improver` fusion pass today (~3.5% closer on `matmul_blocked`); coordinate PR, do not duplicate.
- **MD vertical:** `numerics_researcher` SOTA complete — **algo 105** cell list is **implementation**, not autoresearch invention this pass.
- **131+ unknown rows:** harness/ingest gap — route to `gap_explorer` / ingest, not autoresearch.
- **Control plane:** prior `autoresearch` runs reconciled `error` (`unregistered_running_reconciled`); this run documents sweep only.

## Deliverable / findings

**Study (lic):** `docs/numerics/studies/2026-05-29-autoresearch-proactive-sweep.md`

| Target | Autoresearch action | Result |
|--------|---------------------|--------|
| `horner_pure_li` | Invent new Horner scheme? | **No** — MIR FMA/const-loop already fast; fix **oracle/harness x** alignment for validity |
| `matmul_blocked` | Novel GEMM? | **No** — PH-7e LLVM fusion (`bench_improver`); ~**5%** to ≤1.2× |
| `reduce_sum` | Pure-Li kernel? | **N/A** — not `pure_li` catalog variant; uses `li_reduce_sum_*` runtime |
| Tier-2 `md_lennard_jones` etc. | New integrator/limiter? | **Deferred** — shared C oracle; follow `md-r2-neighbor-list-gap` |
| `three_body_pure` | Listed unknown | Harness/oracle stub — not codegen-bound pure-Li |

**Hypothesis H1 rejected** with evidence: org audit `red: []`, local horner speed green, validity blocked on known oracle mismatch.

**Commands (repro):**

```bash
cd lic && ./scripts/build.sh
cd benchmarks/harness
python3 bench.py --tier 1 --only horner_pure_li,matmul_blocked --runs 5 --skip-verify
python3 bench.py --tier 1 --only horner_pure_li,matmul_blocked --runs 3 --verify-results
```

## Recommended issues/PRs

| Title | Repo | Labels / notes |
|-------|------|----------------|
| perf(7e): fuse tier-1 `matmul_blocked` pure-Li kernel (init+GEMM+sink) | **lic** | `PH-7e`, `numerics` — land `bench_improver` branch `chore/agent-bench_improver-50434717` |
| fix(bench): align `horner_pure_li` tier-1 verify oracle with Li `x=0.999999` | **lic** | `autoresearch`, `numerics` — close validity gap without threshold gaming |
| Implement `md_neighbor_cell_list` (algo 105) with checksum parity | **lic** | `numerics-research`, `PH-5b` — after numerics_researcher contract |
| Ingest tier-1 matrix (`horner_pure_li`, `reduce_sum`, `matmul_naive`) | **benchmarks** | normal `ingest-lic.sh` — clears **unknown** dashboard cells |
| [explorer-finding] OpenMP prescriptive vs descriptive rubric (PH-7e) | **lic** | #124 — plan-needed; informs codegen, not novel physics |
| Close G-math slice when `matmul_blocked` ≤1.2× on CI | **lic** | master-plan **7e-b** / issue #27 |

## Deferred

- **Novel-algorithm** PR until a falsifiable physics/codegen hypothesis beats SOTA on **all locked axes** (stability + accuracy default).
- **Tier-2 autoresearch** (limiters, split schemes) until `md_neighbor_cell_list` reaches oracle parity.
- **`matmul_blocked_N1024`**, **`reduce_sum`** ingest + strict `LI_TIER1_PERF_STRICT=1` matrix on CI runners.
- **Lean `trusted.lean`** / full float Props for fused matmul — human-approved track only.
- **Whitepaper / research-findings** publish — no `goal_id` numerics win this pass.

<!-- li-agent -->
## Agent deliverable
- [x] li-tests or lit test id: N/A — survey-only; existing `horner_pure_li` harness + tier-1 `bench.py` repro
- [x] Bench row / benchmarks path: `lic/benchmarks/results/latest.csv`; ingest via `benchmarks/scripts/ingest/ingest-lic.sh`
- [x] Lean/contracts path documented or N/A with reason: N/A — no compiler proof changes; PH-7e advisory perf only
- [x] Negative result documented if hypothesis rejected: `lic/docs/numerics/studies/2026-05-29-autoresearch-proactive-sweep.md`
