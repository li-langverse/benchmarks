#!/usr/bin/env bash
# Print red/yellow/near-threshold rows from data/latest/summary.json (for agents + Cursor Automations).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SUMMARY="${ROOT}/data/latest/summary.json"

if [[ ! -f "$SUMMARY" ]]; then
  echo "missing $SUMMARY — run ./scripts/ingest/ingest-lic.sh" >&2
  exit 1
fi

python3 - "$SUMMARY" <<'PY'
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text())
print("=== Benchmark failures report ===")
print(f"Dashboard: https://li-langverse.github.io/benchmarks/")
print(f"generated_at: {data.get('generated_at', '?')}")
print()

rows = data.get("rows", [])
reds = [r for r in rows if r.get("status") == "red"]
yellows = [r for r in rows if r.get("status") == "yellow"]
near = [
    r
    for r in rows
    if r.get("status") == "green"
    and r.get("ratio_vs_cpp") is not None
    and r["ratio_vs_cpp"] > 1.0
]
unknown = [r for r in rows if r.get("status") == "unknown"]

def line(r):
    ratio = r.get("ratio_vs_cpp")
    rs = f"{ratio:.3f}×" if ratio is not None else "—"
    ph = ",".join(r.get("ph_ids") or [])
    return f"  {r['benchmark']:28} tier={r.get('tier')}  {rs:>8}  {r.get('repo','')}  PH={ph}"

if reds:
    print(f"RED ({len(reds)}):")
    for r in sorted(reds, key=lambda x: x.get("ratio_vs_cpp") or 0, reverse=True):
        print(line(r))
else:
    print("RED: none")

if yellows:
    print(f"\nYELLOW ({len(yellows)}):")
    for r in yellows:
        print(line(r))

if near:
    print(f"\nGREEN near threshold (>1.0× cpp, {len(near)}):")
    for r in sorted(near, key=lambda x: x["ratio_vs_cpp"], reverse=True)[:8]:
        print(line(r))

if unknown:
    print(f"\nUNKNOWN / no data ({len(unknown)}):")
    for r in unknown:
        print(f"  {r['benchmark']:28} tier={r.get('tier')}  {r.get('repo','')}")

idx = Path(sys.argv[1]).parent.parent / "history" / "index.json"
if idx.is_file():
    hist = json.loads(idx.read_text())
    deltas = hist.get("latest_deltas") or []
    if deltas:
        print(f"\nSince last snapshot ({len(deltas)} deltas):")
        for d in deltas[:15]:
            print(f"  {d}")
PY
