#!/usr/bin/env python3
"""Run lic tier-1 and tier-2 harness benches; parallel when BENCH_JOBS>1."""

from __future__ import annotations

import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path


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


def _run_one_bench(payload: tuple[str, int, str]) -> tuple[str, list[dict[str, object]] | None, str | None]:
    spec_name, runs, lic_root = payload
    os.environ.setdefault("LIC_ROOT", lic_root)
    harness = str(_bench_harness_dir())
    if harness not in sys.path:
        sys.path.insert(0, harness)
    from bench import TIER1_BENCHES, TIER2_BENCHES, run_benchmark

    by_name = {s.name: s for s in (*TIER1_BENCHES, *TIER2_BENCHES)}
    spec = by_name.get(spec_name)
    if spec is None:
        return spec_name, None, f"unknown benchmark {spec_name!r}"
    try:
        rows = run_benchmark(spec, runs=runs)
        return spec_name, rows, None
    except Exception as exc:  # noqa: BLE001 — collect and continue suite
        return spec_name, None, str(exc)


def _benchmark_complete(merged: list[dict[str, str]], name: str) -> bool:
    """True when latest.csv already has li wall_time for this benchmark."""
    for row in merged:
        if row.get("benchmark") != name:
            continue
        if row.get("metric") == "wall_time" and row.get("lang") == "li":
            return True
    return False


def run_specs(
    specs: tuple,
    *,
    runs: int,
    lic_root: Path,
    out: Path,
    jobs: int,
    resume: bool,
) -> int:
    harness = _bench_harness_dir()
    sys.path.insert(0, str(harness))
    from bench import read_csv, write_csv, merge_rows

    merged = read_csv(out)
    todo = [s for s in specs if not (resume and _benchmark_complete(merged, s.name))]
    skipped = len(specs) - len(todo)
    if skipped:
        print(f"resume: skipping {skipped} benchmarks already in {out}", flush=True)

    failed: list[str] = []
    if not todo:
        print(f"nothing to run — {out} already has tier rows", flush=True)
        return 0

    lic_s = str(lic_root)
    tasks = [(s.name, runs, lic_s) for s in todo]

    if jobs <= 1:
        from bench import run_benchmark

        for spec in todo:
            try:
                rows = run_benchmark(spec, runs=runs)
                merged = merge_rows(merged, rows, benchmark=spec.name)
                write_csv(out, merged)
                print(f"ok {spec.name}", flush=True)
            except Exception as exc:  # noqa: BLE001
                failed.append(spec.name)
                print(f"WARN skip {spec.name}: {exc}", file=sys.stderr, flush=True)
    else:
        print(f"parallel: jobs={jobs} benchmarks={len(todo)}", flush=True)
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            futures = {pool.submit(_run_one_bench, task): task[0] for task in tasks}
            for fut in as_completed(futures):
                name, rows, err = fut.result()
                if err:
                    failed.append(name)
                    print(f"WARN skip {name}: {err}", file=sys.stderr, flush=True)
                    continue
                assert rows is not None
                merged = merge_rows(merged, rows, benchmark=name)
                write_csv(out, merged)
                print(f"ok {name}", flush=True)

    if failed:
        print(f"tier12: {len(failed)} skipped: {', '.join(failed)}", file=sys.stderr)
    print(f"updated {out}")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=int(os.environ.get("BENCH_RUNS", "6")))
    parser.add_argument("--jobs", type=int, default=_default_jobs())
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Re-run every benchmark even if latest.csv already has li wall_time",
    )
    args = parser.parse_args()

    lic_root = _lic_root()
    os.environ.setdefault("LIC_ROOT", str(lic_root))
    harness = _bench_harness_dir()
    sys.path.insert(0, str(harness))
    from bench import TIER1_BENCHES, TIER2_BENCHES, RESULTS_CSV

    out = RESULTS_CSV
    jobs = max(1, args.jobs)
    resume = not args.no_resume and os.environ.get("BENCH_RESUME", "1").strip().lower() not in (
        "0",
        "false",
        "no",
    )

    rc1 = run_specs(
        TIER1_BENCHES, runs=args.runs, lic_root=lic_root, out=out, jobs=jobs, resume=resume
    )
    rc2 = run_specs(
        TIER2_BENCHES, runs=args.runs, lic_root=lic_root, out=out, jobs=jobs, resume=resume
    )
    return max(rc1, rc2)


if __name__ == "__main__":
    raise SystemExit(main())
