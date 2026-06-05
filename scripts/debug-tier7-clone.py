#!/usr/bin/env python3
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
os.environ.setdefault("LIC_ROOT", str(ROOT.parent / "lic"))
os.environ["BENCHMARKS_CSV"] = str(ROOT / "results" / "latest.csv")
sys.path.insert(0, str(ROOT / "harness"))

from bench import RESULTS, read_csv
from bench_registry import clone_template_csv_rows, registry_alias_specs

print("RESULTS", RESULTS)
print("csv exists", (RESULTS / "latest.csv").is_file())
rows = read_csv(RESULTS / "latest.csv")
print("rows", len(rows))
benches = {r["benchmark"] for r in rows}
print("has matmul_naive", "matmul_naive" in benches)
print("has heat_equation_2d", "heat_equation_2d" in benches)
specs = registry_alias_specs()
print("specs", len(specs))
rc = clone_template_csv_rows(specs, out=RESULTS / "latest.csv")
print("rc", rc)
