#!/usr/bin/env python3
"""Build summary.json from ingest fixtures (for Li/Python compare gate)."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIX = ROOT / "scripts/ingest/fixtures/summary"

# Reuse build_summary helpers
sys.path.insert(0, str(ROOT / "scripts/ingest"))
import build_summary as bs  # noqa: E402


def main() -> int:
    catalog = {}
    import tomllib

    for b in tomllib.loads((FIX / "catalog.toml").read_text()).get("benchmark", []):
        catalog[b["id"]] = b
    raw = bs.parse_csv(FIX / "lic.csv")
    out = ROOT / "build/compare/summary_py.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    tier_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"green": 0, "yellow": 0, "red": 0, "unknown": 0}
    )
    charts_by_cat: dict[str, list] = defaultdict(list)
    results = []

    for bench_id, cfg in catalog.items():
        category = cfg.get("category", "micro")
        chart = bs.build_perf_chart(bench_id, cfg, raw)
        charts_by_cat[category].append(chart)
        li_val = next((s["value"] for s in chart["series"] if s["lang"] == "li"), None)
        ref = chart["reference_lang"]
        ref_val = next((s["value"] for s in chart["series"] if s["lang"] == ref), None)
        ratio = chart.get("ratio_vs_reference")
        st = chart["status"]
        tier = str(cfg.get("tier", 0))
        tier_counts[tier][st] += 1
        results.append(
            {
                "benchmark": bench_id,
                "repo": cfg.get("repo", "lic"),
                "tier": cfg.get("tier", 0),
                "category": category,
                "metric": cfg.get("metric", "wall_time"),
                "ratio_vs_cpp": ratio,
                "reference_lang": ref,
                "unit": "×",
                "variant": None,
                "status": st,
                "ph_ids": cfg.get("ph_ids", []),
                "path": cfg.get("path", ""),
                "threshold_ratio_cpp": float(cfg.get("threshold_ratio_cpp", 1.2)),
                "ci_url": "",
            }
        )

    categories = {}
    for cat in bs.CATEGORY_ORDER:
        if cat not in charts_by_cat:
            continue
        categories[cat] = {
            "label": bs.CATEGORY_LABELS.get(cat, cat),
            "charts": sorted(charts_by_cat[cat], key=lambda c: c["id"]),
        }

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources": {"fixture": str(FIX)},
        "tier_counts": dict(tier_counts),
        "categories": categories,
        "rows": sorted(results, key=lambda r: (r["tier"], r["benchmark"])),
    }
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
