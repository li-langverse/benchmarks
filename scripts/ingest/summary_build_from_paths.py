#!/usr/bin/env python3
"""PH-IO-7 — build summary.json from explicit paths (Li std.summary bridge)."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "ingest"))
import build_summary as bs  # noqa: E402


def build_from_paths(
    catalog_path: Path,
    lic_csv: Path,
    lis_csv: Path,
    stability_csv: Path,
    out_path: Path,
) -> int:
    import tomllib

    catalog_defaults = bs.load_catalog_defaults()
    if catalog_path.name == "catalog.toml" and catalog_path.parent.name == "summary":
        catalog = {}
        raw = tomllib.loads(catalog_path.read_text()).get("benchmark", [])
        for b in raw:
            catalog[b["id"]] = b
        rows = bs.parse_csv(lic_csv)
        stability_index = bs.load_stability_index(stability_csv)
    else:
        catalog = {}
        raw_cat = tomllib.loads(catalog_path.read_text())
        for b in raw_cat.get("benchmark", []):
            catalog[b["id"]] = b
        rows = bs.merge_csv_rows([lic_csv, lis_csv])
        stability_index = bs.load_stability_index(stability_csv)

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
            bench_id, cfg, rows, stability_index, required=required
        )
        chart = bs.build_perf_chart(
            bench_id,
            cfg,
            rows,
            validity_status=validity_status,
            validity_source=validity_source,
        )
        if not chart.get("series") and chart.get("status") != "skip":
            continue
        charts_by_cat[category].append(chart)
        charts_by_pillar[meta["pillar"]].append(chart)
        st = chart["status"]
        tier = str(cfg.get("tier", 0))
        bucket = st if st in ("green", "yellow", "red") else "unknown"
        tier_counts[tier][bucket] += 1
        results.append(
            bs.make_summary_row(
                bench_id=bench_id,
                cfg=cfg,
                chart=chart,
                validity_status=validity_status,
                validity_source=validity_source,
                os_name=chart.get("os", "linux"),
                category=category,
                metric=cfg.get("metric", "wall_time"),
                status=st,
                raw_rows=rows,
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
        "sources": {
            "catalog": str(catalog_path.resolve()),
            "lic_csv": str(lic_csv.resolve()),
            "lis_csv": str(lis_csv.resolve()),
        },
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
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out_path} ({len(results)} rows)")
    return 0


def main() -> int:
    if len(sys.argv) != 6:
        print(
            "usage: summary_build_from_paths.py <catalog> <lic.csv> <lis.csv> <stability.csv> <out.json>",
            file=sys.stderr,
        )
        return 2
    cat = Path(sys.argv[1])
    lic = Path(sys.argv[2])
    lis = Path(sys.argv[3])
    stab = Path(sys.argv[4]) if sys.argv[4] else Path("/dev/null")
    out = Path(sys.argv[5])
    if not cat.is_file() or not lic.is_file():
        print("summary_build_from_paths: missing catalog or lic csv", file=sys.stderr)
        return 1
    if not lis.is_file():
        lis = lic
    if stab != Path("/dev/null") and not stab.is_file():
        stab = Path("/dev/null")
    return build_from_paths(cat, lic, lis, stab, out)


if __name__ == "__main__":
    raise SystemExit(main())
