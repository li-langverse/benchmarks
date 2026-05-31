#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/ingest"))
import build_summary as bs  # noqa: E402

p = Path("/mnt/c/Users/Julian/Documents/Programming/li/lic/benchmarks/results/stability.csv")
print("exists", p.is_file())
if p.is_file():
    print("content", p.read_text()[:200])
c = bs.build_stability_chart(p)
print("chart", bool(c), c.get("status") if c else None)
