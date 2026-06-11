#!/usr/bin/env python3
"""Patch committed summary.json from local oracle CSV without full re-ingest.

Updates tier-5 HTTP rows/charts from vendor/lis-tier5 CSV and appends catalog
planned rows. Preserves all other summary rows unchanged.
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
    return str(ch.get("base_id") or ch.get("id") or "").split("@", 1)[0]


def load_raw() -> list[dict]:
    paths = [
        ROOT / "vendor/lis-tier5/results/latest.csv",
        ROOT / "results/latest.csv",
    ]
    return bs.merge_csv_rows([p for p in paths if p.is_file()])


def rebuild_http_chart(
    bench_id: str,
    cfg: dict,
    raw: list[dict],
    *,
    os_tag: str = "linux",
) -> dict | None:
    required = bs.validity_required_for(cfg, bs.load_catalog_defaults())
    validity_status, validity_source = bs.validity_for_benchmark(
        bench_id, cfg, raw, {}, required=required
    )
    chart = bs.build_perf_chart(
        bench_id,
        cfg,
        raw,
        validity_status=validity_status,
        validity_source=validity_source,
        os_tag=os_tag,
        chart_id=bs.chart_id_for_os(bench_id, os_tag, multi=False),
        has_csv=True,
    )
    if not chart.get("series"):
        return None
    return chart


def patch_http_rows(summary: dict, catalog: dict[str, dict], raw: list[dict]) -> int:
    changed = 0
    rows_by_bench: dict[str, list[dict]] = defaultdict(list)
    for row in summary.get("rows") or []:
        rows_by_bench[row["benchmark"]].append(row)

    charts_by_base: dict[str, list[dict]] = defaultdict(list)
    for cat in (summary.get("categories") or {}).values():
        for ch in cat.get("charts") or []:
            charts_by_base[chart_base_id(ch)].append(ch)

    for bench_id, cfg in catalog.items():
        if str(cfg.get("category") or "").lower() != "http":
            continue
        if cfg.get("catalog_lifecycle") == "planned":
            continue
        if not bs.has_csv_rows(raw, bench_id, cfg):
            continue
        chart = rebuild_http_chart(bench_id, cfg, raw, os_tag="linux")
        if not chart:
            continue
        chart["id"] = bs.chart_id_for_os(bench_id, "linux", multi=True)
        chart["os"] = "linux"

        # Update linux chart in categories
        for cat in (summary.get("categories") or {}).values():
            for i, ch in enumerate(cat.get("charts") or []):
                cid = str(ch.get("id") or "")
                if chart_base_id(ch) == bench_id and (
                    bs.normalize_os(ch.get("os")) == "linux" or cid.endswith("@linux")
                ):
                    cat["charts"][i] = chart
                    changed += 1

        # Update linux summary row
        row_group = rows_by_bench.get(bench_id, [])
        linux_row = next(
            (r for r in row_group if bs.normalize_os(r.get("os")) == "linux"),
            row_group[0] if row_group else None,
        )
        if linux_row:
            new_row = bs.make_summary_row(
                bench_id=bench_id,
                cfg=cfg,
                chart=chart,
                validity_status=chart.get("validity_status", "pass"),
                validity_source=chart.get("validity_source", "latest.csv:perf_present"),
                os_name="linux",
                category=cfg.get("category", "http"),
                metric=chart.get("metric", cfg.get("metric", "rps")),
                status=chart.get("status", "unknown"),
                raw_rows=bs.rows_for_bench_os(raw, bench_id, cfg, "linux"),
            )
            idx = summary["rows"].index(linux_row)
            summary["rows"][idx] = new_row
            changed += 1

    return changed


def append_planned_rows(summary: dict, catalog: dict[str, dict]) -> int:
    catalog_defaults = bs.load_catalog_defaults()
    existing = {r["benchmark"] for r in summary.get("rows") or []}
    charts_by_cat: dict[str, list[dict]] = defaultdict(list)
    charts_by_pillar: dict[str, list[dict]] = defaultdict(list)
    tier_counts: dict[str, dict[str, int]] = defaultdict(
        lambda: {"green": 0, "yellow": 0, "red": 0, "unknown": 0}
    )
    results: list[dict] = []

    added = 0
    for bench_id, cfg in catalog.items():
        if cfg.get("catalog_lifecycle") != "planned":
            continue
        if bench_id in existing:
            continue
        bs.append_pending_row(
            bench_id=bench_id,
            cfg=cfg,
            category=cfg.get("category", "micro"),
            metric=cfg.get("metric", "wall_time"),
            charts_by_cat=charts_by_cat,
            charts_by_pillar=charts_by_pillar,
            tier_counts=tier_counts,
            results=results,
            catalog_defaults=catalog_defaults,
        )
        added += 1

    if not results:
        return 0

    summary["rows"].extend(results)
    summary["rows"] = sorted(
        summary["rows"], key=lambda r: (r["tier"], r["benchmark"], r.get("os", ""))
    )
    for cat_name, cat_data in charts_by_cat.items():
        bucket = summary.setdefault("categories", {}).setdefault(
            cat_name,
            {"label": bs.CATEGORY_LABELS.get(cat_name, cat_name), "charts": []},
        )
        bucket["charts"].extend(cat_data)
        bucket["charts"] = sorted(bucket["charts"], key=lambda c: c["id"])

    pillars_map: dict[str, list[dict]] = defaultdict(list)
    for cat in summary.get("categories", {}).values():
        for ch in cat.get("charts", []):
            pillars_map[ch.get("pillar", "numerics")].append(ch)
    summary["pillars"] = bs.build_pillars(dict(pillars_map))

    tc = summary.setdefault("tier_counts", {})
    for tier, counts in tier_counts.items():
        merged = tc.setdefault(tier, {"green": 0, "yellow": 0, "red": 0, "unknown": 0})
        for k, v in counts.items():
            merged[k] = merged.get(k, 0) + v

    return added


def main() -> int:
    if not SUMMARY.is_file():
        print(f"missing {SUMMARY}", file=sys.stderr)
        return 1

    catalog = bs.load_catalog()
    raw = load_raw()
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    http_changed = patch_http_rows(summary, catalog, raw)
    planned_added = append_planned_rows(summary, catalog)
    summary["generated_at"] = datetime.now(timezone.utc).isoformat()

    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(
        f"patch-summary-oracle-csv: http_patched={http_changed} "
        f"planned_added={planned_added} rows={len(summary.get('rows', []))}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
