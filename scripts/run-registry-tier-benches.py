#!/usr/bin/env python3
"""Run tier-7 algo_registry alias benches; parallel CI shards + optional in-job jobs."""

from __future__ import annotations

import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT = _SCRIPT_DIR.parent
_HARNESS = _ROOT / "harness"
if str(_HARNESS) not in sys.path:
    sys.path.insert(0, str(_HARNESS))


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


def _run_one_registry(payload: tuple[str, int, str, str]) -> tuple[str, list[dict[str, object]] | None, str | None]:
    spec_name, runs, lic_root, out_s = payload
    os.environ["BENCHMARKS_CSV"] = out_s
    os.environ.setdefault("LIC_ROOT", lic_root)
    os.environ.setdefault("LI_REPO_ROOT", lic_root)
    harness = str(_HARNESS)
    if harness not in sys.path:
        sys.path.insert(0, harness)
    from csv_bench_io import apply_bench_timing_env

    apply_bench_timing_env(os.environ)
    from bench import run_benchmark
    from bench_registry import registry_spec_by_name

    spec = registry_spec_by_name(spec_name)
    if spec is None:
        return spec_name, None, f"unknown registry alias {spec_name!r}"
    try:
        rows = run_benchmark(spec, runs=runs)
        return spec_name, rows, None
    except Exception as exc:  # noqa: BLE001
        return spec_name, None, str(exc)


def _benchmark_complete(merged: list[dict[str, str]], name: str) -> bool:
    harness = str(_HARNESS)
    if harness not in sys.path:
        sys.path.insert(0, harness)
    from csv_bench_io import benchmark_sample_runs_parity_ok
    from timing_stats import equalize_runs_enabled

    return benchmark_sample_runs_parity_ok(
        merged, name, equalize=equalize_runs_enabled()
    )


def run_registry_specs(
    specs: tuple,
    *,
    runs: int,
    lic_root: Path,
    out: Path,
    jobs: int,
    resume: bool,
    label: str,
) -> int:
    from bench import merge_rows, read_csv, write_csv
    from csv_bench_io import merge_benchmark_csv_locked

    merged = read_csv(out)
    todo = [s for s in specs if not (resume and _benchmark_complete(merged, s.name))]
    skipped = len(specs) - len(todo)
    if skipped:
        print(f"resume: skipping {skipped} registry aliases already in {out}", flush=True)

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
        print(f"parallel: jobs={jobs} registry_aliases={len(todo)} ({label})", flush=True)
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            futures = {pool.submit(_run_one_registry, task): task[0] for task in tasks}
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runs", type=int, default=int(os.environ.get("BENCH_RUNS", "6")))
    parser.add_argument("--jobs", type=int, default=_default_jobs())
    parser.add_argument("--registry-shard", type=int, default=None)
    parser.add_argument(
        "--registry-shard-count",
        type=int,
        default=int(os.environ.get("REGISTRY_SHARD_COUNT", "1")),
    )
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()

    if os.environ.get("REGISTRY_RUN_TIMINGS", "").strip() not in ("1", "true", "yes"):
        from bench_registry import clone_template_csv_rows, registry_alias_specs, shard_registry_alias_specs
        from bench import results_csv

        specs = registry_alias_specs()
        shard = args.registry_shard
        if shard is not None:
            specs = shard_registry_alias_specs(
                specs, shard=shard, shard_count=max(1, args.registry_shard_count)
            )
        out = results_csv()
        return clone_template_csv_rows(specs, out=out)

    from bench_registry import registry_alias_specs, shard_registry_alias_specs
    from bench import results_csv

    lic_root = _lic_root()
    os.environ.setdefault("LIC_ROOT", str(lic_root))
    os.environ.setdefault("LI_REPO_ROOT", str(lic_root))
    out = results_csv()
    os.environ["BENCHMARKS_CSV"] = str(out)

    specs = registry_alias_specs()
    shard = args.registry_shard
    shard_count = max(1, args.registry_shard_count)
    if shard is not None:
        specs = shard_registry_alias_specs(specs, shard=shard, shard_count=shard_count)
    if not specs:
        print("registry: no alias specs in shard scope", file=sys.stderr)
        if os.environ.get("BENCH_NIGHTLY", "").strip() in ("1", "true", "yes"):
            return 1
        return 0

    label = "registry-family"
    if shard is not None and shard_count > 1:
        label = f"registry-family-shard-{shard}/{shard_count}"

    resume = not args.no_resume and os.environ.get("BENCH_RESUME", "1").strip().lower() not in (
        "0",
        "false",
        "no",
    )
    return run_registry_specs(
        specs,
        runs=args.runs,
        lic_root=lic_root,
        out=out,
        jobs=max(1, args.jobs),
        resume=resume,
        label=label,
    )


if __name__ == "__main__":
    raise SystemExit(main())
