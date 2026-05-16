#!/usr/bin/env python3
"""Build data/latest/summary.json from lic CSV exports and catalog.toml."""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_catalog() -> dict[str, dict]:
    import tomllib

    catalog: dict[str, dict] = {}
    raw = tomllib.loads((ROOT / "catalog.toml").read_text())
    for b in raw.get("benchmark", []):
        catalog[b["id"]] = b
    return catalog


def parse_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows = []
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def status_for_ratio(ratio: float | None, threshold: float) -> str:
    if ratio is None:
        return "unknown"
    if ratio <= threshold:
        return "green"
    if ratio <= threshold * 1.1:
        return "yellow"
    return "red"


def main() -> int:
    lic_root = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "li"
    csv_path = (
        Path(sys.argv[2])
        if len(sys.argv) > 2
        else lic_root / "benchmarks/results/latest.csv"
    )
    catalog = load_catalog()
    raw = parse_csv(csv_path)

    by_bench: dict[str, list[dict]] = defaultdict(list)
    for row in raw:
        by_bench[row["benchmark"]].append(row)

    results = []
    tier_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"green": 0, "yellow": 0, "red": 0, "unknown": 0}
    )

    for bench_id, cfg in catalog.items():
        rows = by_bench.get(bench_id, [])
        li_rows = [r for r in rows if r.get("lang") == "li" and r.get("metric") == cfg.get("metric", "wall_time")]
        cpp_rows = [r for r in rows if r.get("lang") == "cpp" and r.get("metric") == cfg.get("metric", "wall_time")]
        li_val = float(li_rows[0]["value"]) if li_rows else None
        cpp_val = float(cpp_rows[0]["value"]) if cpp_rows else None
        ratio = (li_val / cpp_val) if li_val and cpp_val and cpp_val > 0 else None
        threshold = float(cfg.get("threshold_ratio_cpp", 1.2))
        st = status_for_ratio(ratio, threshold)
        tier = str(cfg.get("tier", 0))
        tier_counts[tier][st] += 1
        results.append(
            {
                "benchmark": bench_id,
                "repo": cfg.get("repo", "lic"),
                "tier": cfg.get("tier", 0),
                "metric": cfg.get("metric", "wall_time"),
                "li_value": li_val,
                "cpp_value": cpp_val,
                "ratio_vs_cpp": round(ratio, 4) if ratio is not None else None,
                "unit": li_rows[0].get("unit") if li_rows else cpp_rows[0].get("unit") if cpp_rows else None,
                "variant": cfg.get("variant", li_rows[0].get("variant") if li_rows else None),
                "status": st,
                "ph_ids": cfg.get("ph_ids", []),
                "path": cfg.get("path", ""),
                "threshold_ratio_cpp": threshold,
                "ci_url": "",
            }
        )

    for bench_id in sorted(by_bench.keys()):
        if bench_id in catalog:
            continue
        tier_counts["?"]["unknown"] += 1

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_csv": str(csv_path),
        "tier_counts": dict(tier_counts),
        "rows": sorted(results, key=lambda r: (r["tier"], r["benchmark"])),
    }

    out_dir = ROOT / "data/latest"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(f"wrote {out_dir / 'summary.json'} ({len(results)} catalog rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
