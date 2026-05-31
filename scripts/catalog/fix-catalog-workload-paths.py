#!/usr/bin/env python3
"""Normalize catalog.toml workload paths to benchmarks/workloads/* on disk."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.toml"


def main() -> int:
    text = CATALOG.read_text(encoding="utf-8")
    updated = text.replace(
        'path = "benchmarks/tier', 'path = "benchmarks/workloads/tier'
    ).replace(
        'path = "benchmarks/viewport/', 'path = "benchmarks/workloads/tier1_micro/'
    )
    if updated == text:
        print("catalog.toml: paths already normalized")
        return 0
    CATALOG.write_text(updated, encoding="utf-8")
    print("catalog.toml: normalized tier/viewport paths -> benchmarks/workloads/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
