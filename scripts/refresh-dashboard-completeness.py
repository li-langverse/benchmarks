#!/usr/bin/env python3
"""Refresh committed summary.json with multi-OS skip charts and catalog size labels.

Use when a full lic CSV re-ingest is unavailable locally (Windows sprint host).
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data/latest/summary.json"

sys.path.insert(0, str(ROOT / "scripts/ingest"))
import build_summary as bs  # noqa: E402


def chart_base_id(ch: dict) -> str:
    bid = str(ch.get("base_id") or ch.get("id") or "")
    return bid.split("@", 1)[0]


def chart_os(ch: dict) -> str:
    plat = bs.normalize_os(ch.get("os"))
    if plat != "unknown":
        return plat
    cid = str(ch.get("id") or "")
    if "@" in cid:
        return cid.split("@", 1)[1]
    return "linux"


def refresh(summary: dict, catalog: dict[str, dict], catalog_defaults: dict) -> dict:
    rows = summary.get("rows") or []
    row_by_bench = {r["benchmark"]: r for r in rows}

    new_categories: dict[str, dict] = {}
    charts_by_pillar: dict[str, list[dict]] = defaultdict(list)

    for cat_name, cat_data in (summary.get("categories") or {}).items():
        charts_out: list[dict] = []
        by_base: dict[str, list[dict]] = defaultdict(list)
        for ch in cat_data.get("charts") or []:
            by_base[chart_base_id(ch)].append(ch)

        for base, group in sorted(by_base.items()):
            cfg = catalog.get(base)
            if not cfg:
                stub_cfg = {
                    "id": base,
                    "category": cat_name,
                    "tier": 99,
                }
                platforms = list(bs.PLATFORM_ORDER)
                multi = True
                for plat in platforms:
                    ch = bs.build_platform_skip_chart(
                        base,
                        stub_cfg,
                        plat,
                        chart_id=bs.chart_id_for_os(base, plat, multi=multi),
                        multi=multi,
                        validity_source="catalog:non_catalog_chart",
                    )
                    charts_out.append(ch)
                    charts_by_pillar[ch.get("pillar", cat_name)].append(ch)
                continue

            platforms = bs.catalog_platforms(cfg, catalog_defaults)
            multi = len(platforms) > 1
            existing: dict[str, dict] = {}
            for ch in group:
                existing[chart_os(ch)] = ch

            for plat in platforms:
                if plat in existing:
                    ch = dict(existing[plat])
                    has_csv = bool(ch.get("series"))
                    sizes = bs.effective_size_meta(cfg, has_csv=has_csv)
                    ch.update({k: v for k, v in sizes.items() if v is not None})
                    ch["os"] = plat
                    if ch.get("pending") or not has_csv:
                        ch["validity_status"] = "skip"
                        ch["validity_source"] = ch.get("validity_source") or "platform_not_measured"
                        ch["status"] = "skip"
                    elif ch.get("validity_status") in (None, "", "unknown"):
                        row = row_by_bench.get(base)
                        if row and row.get("validity_status") in ("pass", "fail", "skip", "advisory"):
                            ch["validity_status"] = row["validity_status"]
                            ch["validity_source"] = row.get("validity_source") or "summary.row"
                    if ch.get("status") in (None, "", "unknown") and ch.get("validity_status") == "skip":
                        ch["status"] = "skip"
                    charts_out.append(ch)
                    charts_by_pillar[ch.get("pillar", "numerics")].append(ch)
                    continue

                skip = bs.build_platform_skip_chart(
                    base,
                    cfg,
                    plat,
                    chart_id=bs.chart_id_for_os(base, plat, multi=multi),
                    multi=multi,
                    validity_source=f"platform:{plat}:not_measured",
                )
                charts_out.append(skip)
                charts_by_pillar[skip["pillar"]].append(skip)

        new_categories[cat_name] = {
            **cat_data,
            "charts": sorted(charts_out, key=lambda c: c["id"]),
        }

    for r in rows:
        cfg = catalog.get(r["benchmark"])
        if not cfg:
            continue
        has_csv = r.get("li_value") is not None
        sizes = bs.effective_size_meta(cfg, has_csv=has_csv)
        r.update({k: v for k, v in sizes.items() if v is not None})
        if r.get("pending") or r.get("li_value") is None:
            r["validity_status"] = "skip"
            r["validity_source"] = r.get("validity_source") or "catalog:pending"
            r["status"] = "skip"
        elif r.get("status") in (None, "", "unknown") and r.get("validity_status") == "skip":
            r["status"] = "skip"

    summary["categories"] = new_categories
    summary["pillars"] = bs.build_pillars(dict(charts_by_pillar))
    summary["generated_at"] = datetime.now(timezone.utc).isoformat()
    os_values = sorted(
        {
            chart_os(ch)
            for cat in new_categories.values()
            for ch in cat.get("charts", [])
            if ch.get("os")
        }
    )
    reporting = summary.setdefault("reporting", {})
    reporting["os_values"] = os_values
    reporting["size_labels"] = sorted(
        {
            str(ch["size_label"])
            for cat in new_categories.values()
            for ch in cat.get("charts", [])
            if ch.get("size_label")
        }
    )
    return summary


def main() -> int:
    if not SUMMARY.is_file():
        print(f"missing {SUMMARY}", file=sys.stderr)
        return 1
    catalog = bs.load_catalog()
    catalog_defaults = bs.load_catalog_defaults()
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    refreshed = refresh(summary, catalog, catalog_defaults)
    SUMMARY.write_text(json.dumps(refreshed, indent=2) + "\n", encoding="utf-8")
    charts = sum(len(c.get("charts", [])) for c in refreshed.get("categories", {}).values())
    print(f"refresh-dashboard-completeness: wrote {SUMMARY} ({charts} charts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
