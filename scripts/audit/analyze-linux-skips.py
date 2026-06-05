#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import tomllib
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUMMARY = ROOT / "data/latest/summary.json"
CSV_PATH = ROOT / "results/latest.csv"
CATALOG = ROOT / "catalog.toml"


def csv_keys() -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out.add((row["benchmark"], (row.get("os") or "linux").lower()))
    return out


def main() -> None:
    rows = json.loads(SUMMARY.read_text())["rows"]
    sk = [r for r in rows if r.get("status") == "skip"]
    csv_k = csv_keys()
    doc = tomllib.loads(CATALOG.read_text(encoding="utf-8"))
    by_id = {b["id"]: b for b in doc.get("benchmark", [])}

    linux_sk = [r for r in sk if r.get("os") == "linux"]
    print("linux skips", len(linux_sk))
    reasons: Counter[str] = Counter()
    for r in linux_sk:
        bid = r.get("benchmark") or r.get("id") or "?"
        cfg = by_id.get(bid, {})
        sl = cfg.get("size_label", "")
        if sl == "harness pending":
            reasons["harness_pending"] += 1
        elif (bid, "linux") not in csv_k and (cfg.get("base_id") or bid, "linux") not in csv_k:
            reasons["no_csv"] += 1
        else:
            reasons["csv_but_skip"] += 1
    print("linux skip reasons", dict(reasons))
    print("os skips", Counter(r.get("os") for r in sk))

    pending = [b["id"] for b in doc["benchmark"] if b.get("size_label") == "harness pending"]
    print("harness pending ids", len(pending), "sample", pending[:10])


if __name__ == "__main__":
    main()
