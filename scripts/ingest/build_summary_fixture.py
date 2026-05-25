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

sys.path.insert(0, str(ROOT / "scripts/ingest"))
import build_summary as bs  # noqa: E402


def main() -> int:
    import tomllib

    catalog_defaults = bs.load_catalog_defaults()
    catalog = {}
    for b in tomllib.loads((FIX / "catalog.toml").read_text()).get("benchmark", []):
        catalog[b["id"]] = b
    raw = bs.parse_csv(FIX / "lic.csv")
    stability_index = bs.load_stability_index(FIX / "stability.csv")
    out = ROOT / "build/compare/summary_py.json"
    out.parent.mkdir(parents=True, exist_ok=True)

    tier_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"green": 0, "yellow": 0, "red": 0, "unknown": 0}
    )
    charts_by_cat: dict[str, list] = defaultdict(list)
    charts_by_pillar: dict[str, list] = defaultdict(list)
    results = []

    for bench_id, cfg in catalog.items():
        category = cfg.get("category", "micro")
        meta = bs.row_meta(cfg)
        required = bs.validity_required_for(cfg, catalog_defaults)
        validity_status, validity_source = bs.validity_for_benchmark(
            bench_id, cfg, raw, stability_index, required=required
        )
        chart = bs.build_perf_chart(
            bench_id,
            cfg,
            raw,
            validity_status=validity_status,
            validity_source=validity_source,
        )
        charts_by_cat[category].append(chart)
        charts_by_pillar[meta["pillar"]].append(chart)
        st = chart["status"]
        tier = str(cfg.get("tier", 0))
        tier_counts[tier][st] += 1
        results.append(
            bs.make_summary_row(
                bench_id=bench_id,
                cfg=cfg,
                chart=chart,
                validity_status=validity_status,
                validity_source=validity_source,
                os_name=chart.get("os", "unknown"),
                category=category,
                metric=cfg.get("metric", "wall_time"),
                status=st,
            )
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
        "reporting": {
            "sota_policy": "best_competitor_lang_excludes_li",
            "validity_required_default": bool(
                catalog_defaults.get("validity_required", True)
            ),
            "os_values": sorted({r.get("os", "unknown") for r in results}),
        },
        "tier_counts": dict(tier_counts),
        "categories": categories,
        "pillars": bs.build_pillars(charts_by_pillar),
        "rows": sorted(results, key=lambda r: (r["tier"], r["benchmark"])),
    }
    out.write_text(json.dumps(summary, indent=2) + "\n")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
