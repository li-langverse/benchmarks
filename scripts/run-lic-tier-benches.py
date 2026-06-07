#!/usr/bin/env python3
"""Run lic tier-1 and tier-2 harness benches; parallel when BENCH_JOBS>1."""

from __future__ import annotations

import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
from bench_tier2_groups import TIER2_GROUPS


def _lic_root() -> Path:
    root = os.environ.get("LIC_ROOT") or os.environ.get("LI_REPO_ROOT")
    if not root:
        raise SystemExit("LIC_ROOT or LI_REPO_ROOT must be set")
    return Path(root).resolve()


def _default_jobs() -> int:
    raw = os.environ.get("BENCH_JOBS", "").strip()
    if raw:
        return max(1, int(raw))
    return max(1, os.cpu_count() or 1)


def _bench_harness_dir() -> Path:
    root = Path(__file__).resolve().parents[1]
    h = root / "harness"
    if h.is_dir():
        return h
    lic = _lic_root()
    return lic / "benchmarks" / "harness"


def _run_one_bench(payload: tuple[str, int, str, str]) -> tuple[str, list[dict[str, object]] | None, str | None]:
    spec_name, runs, lic_root, out_s = payload
    os.environ["BENCHMARKS_CSV"] = out_s
    os.environ.setdefault("LIC_ROOT", lic_root)
    os.environ.setdefault("LI_REPO_ROOT", lic_root)
    harness = str(_bench_harness_dir())
    if harness not in sys.path:
        sys.path.insert(0, harness)
    from csv_bench_io import apply_bench_timing_env

    apply_bench_timing_env(os.environ)
    from bench import TIER1_BENCHES, TIER2_BENCHES, run_benchmark

    by_name = {s.name: s for s in (*TIER1_BENCHES, *TIER2_BENCHES)}
    spec = by_name.get(spec_name)
    if spec is None:
        return spec_name, None, f"unknown benchmark {spec_name!r}"
    try:
        rows = run_benchmark(spec, runs=runs)
        return spec_name, rows, None
    except Exception as exc:  # noqa: BLE001
        return spec_name, None, str(exc)


def _benchmark_complete(merged: list[dict[str, str]], name: str) -> bool:
    harness = str(_bench_harness_dir())
    if harness not in sys.path:
        sys.path.insert(0, harness)
    from csv_bench_io import benchmark_sample_runs_parity_ok
    from timing_stats import equalize_runs_enabled

    return benchmark_sample_runs_parity_ok(
        merged, name, equalize=equalize_runs_enabled()
    )


def run_specs(
    specs: tuple,
    *,
    runs: int,
    lic_root: Path,
    out: Path,
    jobs: int,
    resume: bool,
    label: str,
) -> int:
    harness = _bench_harness_dir()
    sys.path.insert(0, str(harness))
    from bench import merge_rows, read_csv, write_csv
    from csv_bench_io import merge_benchmark_csv_locked

    merged = read_csv(out)
    todo = [s for s in specs if not (resume and _benchmark_complete(merged, s.name))]
    skipped = len(specs) - len(todo)
    if skipped:
        print(f"resume: skipping {skipped} benchmarks already in {out}", flush=True)

    failed: list[str] = []
    if not todo:
        print(f"nothing to run — {out} already has {label} rows", flush=True)
        return 0

    lic_s = str(lic_root)
    out_s = str(out)
    tasks = [(s.name, runs, lic_s, out_s) for s in todo]

    if jobs <= 1:
        from bench import run_benchmark

        for spec in todo:
            try:
                rows = run_benchmark(spec, runs=runs)
                merge_benchmark_csv_locked(
                    out,
                    rows,
                    benchmark=spec.name,
                    read_csv=read_csv,
                    merge_rows=merge_rows,
                    write_csv=write_csv,
                )
                print(f"ok {spec.name}", flush=True)
            except Exception as exc:  # noqa: BLE001
                failed.append(spec.name)
                print(f"WARN skip {spec.name}: {exc}", file=sys.stderr, flush=True)
    else:
        print(f"parallel: jobs={jobs} benchmarks={len(todo)} ({label})", flush=True)
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            futures = {pool.submit(_run_one_bench, task): task[0] for task in tasks}
            for fut in as_completed(futures):
                name, rows, err = fut.result()
                if err:
                    failed.append(name)
                    print(f"WARN skip {name}: {err}", file=sys.stderr, flush=True)
                    continue
                assert rows is not None
                merge_benchmark_csv_locked(
                    out,
                    rows,
                    benchmark=name,
                    read_csv=read_csv,
                    merge_rows=merge_rows,
                    write_csv=write_csv,
                )
                print(f"ok {name}", flush=True)

    if failed:
        print(f"{label}: {len(failed)} skipped: {', '.join(failed)}", file=sys.stderr)
    print(f"updated {out}")
    return 1 if failed else 0


def _filter_tier2(group: str | None) -> tuple:
    harness = _bench_harness_dir()
    sys.path.insert(0, str(harness))
    from bench import TIER2_BENCHES

    if not group:
        return TIER2_BENCHES
    key = group.removeprefix("tier2-") if group.startswith("tier2-") else group
    names = TIER2_GROUPS.get(key)
    if names is None:
        raise SystemExit(f"unknown tier2 group {group!r}; expected md, pde, mech")
    specs = tuple(s for s in TIER2_BENCHES if s.name in names)
    missing = names - {s.name for s in specs}
    if missing:
        raise SystemExit(f"tier2 group {key} missing bench specs: {sorted(missing)}")
    return specs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=int(os.environ.get("BENCH_RUNS", "6")))
    parser.add_argument("--jobs", type=int, default=_default_jobs())
    parser.add_argument("--tier", choices=("1", "2", "all"), default="all")
    parser.add_argument("--tier2-group", choices=sorted(TIER2_GROUPS))
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()

    lic_root = _lic_root()
    os.environ.setdefault("LIC_ROOT", str(lic_root))
    harness = _bench_harness_dir()
    sys.path.insert(0, str(harness))
    from bench import TIER1_BENCHES, results_csv

    out = results_csv()
    os.environ["BENCHMARKS_CSV"] = str(out)
    jobs = max(1, args.jobs)
    resume = not args.no_resume and os.environ.get("BENCH_RESUME", "1").strip().lower() not in (
        "0",
        "false",
        "no",
    )

    rc = 0
    tier = "2" if args.tier2_group else args.tier
    if tier in ("1", "all"):
        rc = max(
            rc,
            run_specs(
                TIER1_BENCHES,
                runs=args.runs,
                lic_root=lic_root,
                out=out,
                jobs=jobs,
                resume=resume,
                label="tier-1",
            ),
        )
    if tier in ("2", "all"):
        specs = _filter_tier2(args.tier2_group)
        rc = max(
            rc,
            run_specs(
                specs,
                runs=args.runs,
                lic_root=lic_root,
                out=out,
                jobs=jobs,
                resume=resume,
                label=f"tier-2-{args.tier2_group or 'all'}",
            ),
        )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
