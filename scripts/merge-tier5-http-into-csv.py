#!/usr/bin/env python3
"""Merge tier-5 HTTP CSVs into benchmarks results/latest.csv (ingest prep)."""
from __future__ import annotations

import csv
import os
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 3:
        print(
            "usage: merge-tier5-http-into-csv.py <benchmarks-root> <lic-root>",
            file=sys.stderr,
        )
        return 2

    root = Path(sys.argv[1])
    lic = Path(sys.argv[2])
    latest = Path(os.environ.get("BENCHMARKS_CSV", root / "results/latest.csv"))
    tier5_vendor = root / "vendor/lis-tier5/results/latest.csv"
    tier5_extra = lic / "benchmarks/results/http_tier5.csv"

    import tomllib

    catalog = tomllib.loads((root / "catalog.toml").read_text(encoding="utf-8"))
    http_ids = {b["id"] for b in catalog.get("benchmark", []) if b.get("category") == "http"}

    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    if latest.is_file():
        with latest.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            header = list(reader.fieldnames or [])
            rows = [row for row in reader if row.get("benchmark") not in http_ids]

    seen_http: set[tuple[str, str, str, str]] = set()

    def extend_csv(path: Path, *, supplemental: bool = False) -> None:
        nonlocal header
        if not path.is_file():
            return
        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return
            header = header or list(reader.fieldnames)
            for row in reader:
                bid = row.get("benchmark") or ""
                lang = row.get("lang") or ""
                variant = row.get("variant") or ""
                metric = row.get("metric") or ""
                key = (bid, lang, variant, metric)
                if supplemental:
                    if bid != "proxy_loopback":
                        continue
                    if key in seen_http:
                        continue
                    if lang == "li" and variant not in ("c_epoll", "li_epoll"):
                        continue
                    if lang == "nginx":
                        continue
                else:
                    seen_http.add(key)
                rows.append(row)

    extend_csv(tier5_vendor)
    extend_csv(tier5_extra, supplemental=True)
    if not header:
        print("merge-tier5-http: no rows to write", file=sys.stderr)
        return 0

    latest.parent.mkdir(parents=True, exist_ok=True)
    with latest.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
    vendor_name = tier5_vendor.name if tier5_vendor.is_file() else "—"
    print(f"merged tier5 ({vendor_name} + extra) into {latest}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
