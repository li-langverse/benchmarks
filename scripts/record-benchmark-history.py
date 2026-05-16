#!/usr/bin/env python3
"""Append summary snapshot to data/history/ and compute deltas vs previous."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/latest/summary.json"
HISTORY_DIR = ROOT / "data/history"
INDEX = HISTORY_DIR / "index.json"


def row_key(r: dict) -> str:
    return r["benchmark"]


def main() -> int:
    if not SUMMARY.is_file():
        print(f"missing {SUMMARY}", file=sys.stderr)
        return 1

    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    snap_path = HISTORY_DIR / f"{ts}.json"
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    snap_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    index: dict = {"snapshots": [], "latest_deltas": []}
    if INDEX.is_file():
        index = json.loads(INDEX.read_text(encoding="utf-8"))

    prev_path = index["snapshots"][-1]["path"] if index.get("snapshots") else None
    deltas: list[dict] = []
    if prev_path:
        prev = json.loads((ROOT / prev_path).read_text(encoding="utf-8"))
        prev_by = {row_key(r): r for r in prev.get("rows", [])}
        for r in summary.get("rows", []):
            k = row_key(r)
            p = prev_by.get(k)
            if not p:
                continue
            if r.get("status") != p.get("status"):
                deltas.append(
                    {
                        "benchmark": k,
                        "field": "status",
                        "from": p.get("status"),
                        "to": r.get("status"),
                    }
                )
            if r.get("ratio_vs_cpp") is not None and p.get("ratio_vs_cpp") is not None:
                dr = round(r["ratio_vs_cpp"] - p["ratio_vs_cpp"], 4)
                if abs(dr) >= 0.01:
                    deltas.append(
                        {
                            "benchmark": k,
                            "field": "ratio_vs_cpp",
                            "from": p["ratio_vs_cpp"],
                            "to": r["ratio_vs_cpp"],
                            "delta": dr,
                            "improved": dr < 0,
                        }
                    )

    index["snapshots"].append(
        {"at": summary.get("generated_at", ts), "path": str(snap_path.relative_to(ROOT))}
    )
    index["snapshots"] = index["snapshots"][-120:]
    index["latest_deltas"] = deltas
    index["updated_at"] = datetime.now(timezone.utc).isoformat()
    INDEX.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    print(f"recorded {snap_path.name} ({len(deltas)} deltas vs previous)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
