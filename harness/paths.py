"""Benchmarks-repo vs legacy lic-repo layout for harness drivers."""
from __future__ import annotations

import os
from pathlib import Path

_HARNESS = Path(__file__).resolve().parent
BENCH_REPO = _HARNESS.parent
WORKLOADS = BENCH_REPO / "benchmarks" / "workloads"
RESULTS = BENCH_REPO / "results"


def lic_root() -> Path:
    raw = os.environ.get("LIC_ROOT") or os.environ.get("LI_REPO_ROOT")
    if raw:
        return Path(raw).resolve()
    sibling = BENCH_REPO.parent / "lic"
    if sibling.is_dir():
        return sibling.resolve()
    nested = BENCH_REPO / "lic"
    if nested.is_dir():
        return nested.resolve()
    return BENCH_REPO.resolve()


def lic_compiler_bin(root: Path | None = None) -> Path:
    """Built lic driver (lic.exe on MSYS2/Windows, lic elsewhere)."""
    env = os.environ.get("LIC", "").strip()
    if env:
        p = Path(env)
        if p.is_file():
            return p.resolve()
    base = (root or lic_root()).resolve()
    d = base / "build" / "compiler" / "lic"
    for name in ("lic.exe", "lic"):
        p = d / name
        if p.is_file():
            return p.resolve()
    return (d / "lic").resolve()


def tier_dirs() -> tuple[Path, Path, Path]:
    if (WORKLOADS / "tier1_micro").is_dir():
        return (
            WORKLOADS / "tier1_micro",
            WORKLOADS / "tier1_stdlib",
            WORKLOADS / "tier2_physics",
        )
    lic = lic_root()
    return (
        lic / "benchmarks" / "tier1_micro",
        lic / "benchmarks" / "tier1_stdlib",
        lic / "benchmarks" / "tier2_physics",
    )


def tier3_ecosystem_dir() -> Path:
    p = WORKLOADS / "tier3_ecosystem"
    if p.is_dir():
        return p
    return lic_root() / "benchmarks" / "tier3_ecosystem"


def tier5_http_dir() -> Path:
    p = WORKLOADS / "tier5_http"
    if p.is_dir():
        return p
    return lic_root() / "benchmarks" / "tier5_http"


def competitive_registry_path() -> Path:
    for p in (
        WORKLOADS / "competitive" / "algo_registry.json",
        BENCH_REPO / "benchmarks" / "competitive" / "algo_registry.json",
        lic_root() / "benchmarks" / "competitive" / "algo_registry.json",
    ):
        if p.is_file():
            return p
    return WORKLOADS / "competitive" / "algo_registry.json"


def results_csv() -> Path:
    env = os.environ.get("BENCHMARKS_CSV", "").strip()
    if env:
        return Path(env).resolve()
    RESULTS.mkdir(parents=True, exist_ok=True)
    return RESULTS / "latest.csv"
