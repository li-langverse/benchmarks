#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
rows = json.loads((ROOT / "data/latest/summary.json").read_text())["rows"]
sk = [r for r in rows if r.get("status") == "skip" and r.get("os") == "linux"]
csv_b = set()
with (ROOT / "results/latest.csv").open(newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        csv_b.add(row["benchmark"])
doc = tomllib.loads((ROOT / "catalog.toml").read_text(encoding="utf-8"))
by_id = {b["id"]: b for b in doc["benchmark"]}
for r in sk:
    bid = r.get("benchmark") or "?"
    cfg = by_id.get(bid, {})
    in_csv = bid in csv_b or (cfg.get("base_id") or bid) in csv_b
    print(bid, "tier", r.get("tier"), "pkg", r.get("package"), "csv" if in_csv else "NO_CSV", cfg.get("size_label", ""))
