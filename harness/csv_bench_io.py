"""Locked read-modify-write for parallel benchmark CSV shards."""

from __future__ import annotations

import os
import sys
from collections.abc import Callable
from contextlib import contextmanager
from pathlib import Path
from typing import TypeVar

T = TypeVar("T")


@contextmanager
def csv_shard_lock(path: Path):
    """Exclusive lock for one CSV shard (ProcessPoolExecutor workers)."""
    lock_path = path.with_suffix(f"{path.suffix}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lock_path, "a+b") as lock_f:
        if os.name == "nt":
            import msvcrt

            lock_f.seek(0)
            msvcrt.locking(lock_f.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(lock_f.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            if os.name == "nt":
                lock_f.seek(0)
                msvcrt.locking(lock_f.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(lock_f.fileno(), fcntl.LOCK_UN)


def merge_benchmark_csv_locked(
    path: Path,
    new_rows: list[dict[str, object]],
    *,
    benchmark: str,
    read_csv: Callable[[Path], list[dict[str, str]]],
    merge_rows: Callable[..., list[dict[str, object]]],
    write_csv: Callable[[Path, list[dict[str, object]]], None],
) -> None:
    with csv_shard_lock(path):
        merged = read_csv(path)
        merged = merge_rows(merged, new_rows, benchmark=benchmark)
        write_csv(path, merged)


def wall_time_sample_runs(rows: list[dict[str, str]], benchmark: str) -> dict[str, int]:
    runs: dict[str, int] = {}
    for row in rows:
        if row.get("benchmark") != benchmark or row.get("metric") != "wall_time":
            continue
        lang = row.get("lang") or ""
        if lang in ("", "harness"):
            continue
        raw = (row.get("sample_runs") or "").strip()
        if not raw:
            continue
        try:
            n = int(raw)
        except ValueError:
            continue
        if n >= 1:
            runs[lang] = n
    return runs


def benchmark_sample_runs_parity_ok(
    rows: list[dict[str, str]],
    benchmark: str,
    *,
    equalize: bool,
) -> bool:
    """True when li wall_time exists and sample_runs match competitors (BN2 resume gate)."""
    runs = wall_time_sample_runs(rows, benchmark)
    if "li" not in runs:
        return False
    if not equalize:
        return True
    comp = [n for lang, n in runs.items() if lang != "li"]
    if not comp:
        return True
    return runs["li"] >= max(comp)


def apply_bench_timing_env(env: dict[str, str]) -> None:
    """Copy nightly timing env into worker processes (spawn-safe)."""
    keys = (
        "BENCH_EQUALIZE_RUNS",
        "BENCH_RUNS",
        "BENCH_MIN_RUNS",
        "BENCH_SUBSEC_MIN_RUNS",
        "BENCH_ADAPTIVE_RUNS",
        "BENCH_MAX_RUNS",
        "BENCH_TARGET_SAMPLE_SEC",
        "LIC_ROOT",
        "LI_REPO_ROOT",
        "LIC",
    )
    for key in keys:
        val = os.environ.get(key)
        if val is not None and val != "":
            env[key] = val
