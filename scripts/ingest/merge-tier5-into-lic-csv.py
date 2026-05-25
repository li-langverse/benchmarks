#!/usr/bin/env python3
from __future__ import annotations
import csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
HEADER = ["benchmark","lang","variant","threads","metric","value","unit","git_sha","cpu_model","flags"]
def read_csv(p):
    return list(csv.DictReader(p.open())) if p.is_file() else []
def write_csv(p, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER, extrasaction="ignore")
        w.writeheader()
        for r in rows: w.writerow({k: r.get(k,"") for k in HEADER})
def merge(a, b):
    m = {r.get("benchmark",""): [r] for r in a}
    for r in b: m[r.get("benchmark","")] = [r]
    return [x for k in sorted(m) for x in m[k]]
lic = Path(sys.argv[1] if len(sys.argv)>1 else ROOT/"lic")
out = lic/"benchmarks/results/latest.csv"
vendor = ROOT/"vendor/lis-tier5/results/latest.csv"
rows = merge(read_csv(out), read_csv(vendor))
write_csv(out, rows)
print(f"merge-tier5: wrote {len(rows)} row(s) to {out}")
