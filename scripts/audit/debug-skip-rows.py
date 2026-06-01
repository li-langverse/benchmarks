#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/ingest"))
import build_summary as bs  # noqa: E402

raw = bs.parse_csv(ROOT / "results/latest.csv")
for bid in ("matmul_naive_N1024", "matmul_blocked_N1024", "tier0_stability"):
    cfg = bs.load_catalog()[bid]
    rows = bs.rows_for_bench(raw, bid, cfg)
    print(bid, "rows", len(rows), "cfg", cfg.get("base_id"), cfg.get("problem_size"))
    chart = bs.build_stability_chart(ROOT.parent / "lic/benchmarks/results/stability.csv") if bid == "tier0_stability" else None
    if chart:
        print("  stability chart ok")
