#!/usr/bin/env python3
"""Find first history snapshot where a benchmark ratio crossed a threshold."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "data/history/index.json"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--benchmark", required=True)
    p.add_argument("--os", default="linux")
    p.add_argument("--threshold", type=float, default=1.2)
    args = p.parse_args()
    if not INDEX.is_file():
        print("no history index", file=__import__("sys").stderr)
        return 1
    index = json.loads(INDEX.read_text())
    prev_ratio = None
    for snap in index.get("snapshots", []):
        path = ROOT / snap["path"]
        if not path.is_file():
            continue
        doc = json.loads(path.read_text())
        prov = doc.get("provenance", {})
        for row in doc.get("rows", []):
            if row.get("benchmark") != args.benchmark:
                continue
            if row.get("os", "linux") != args.os:
                continue
            ratio = row.get("ratio_vs_cpp")
            if ratio is None:
                continue
            if ratio >= args.threshold and (prev_ratio is None or prev_ratio < args.threshold):
                print(
                    json.dumps(
                        {
                            "at": snap.get("at"),
                            "lic_sha": prov.get("lic_sha"),
                            "ratio_vs_cpp": ratio,
                            "path": snap.get("path"),
                        },
                        indent=2,
                    )
                )
                return 0
            prev_ratio = ratio
    print("no regression crossing found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
