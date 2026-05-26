#!/usr/bin/env python3
"""Backward-compatible entry — delegates to registry_oltp.py (PH-DB-5 / WP-C).

CI validate-only and optional SQLite stub timing use this path name.
Real lidb vs Postgres runs: registry_oltp.py or run-db-registry-bench.sh with RUN_HARNESS=1.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

from registry_oltp import (  # noqa: E402
    SCENARIO_IDS,
    build_harness_json,
    resolve_engine_mode,
    run_benchmarks,
    validate_tier_layout,
    write_csv,
)

TIER_ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--profile", default="ci", choices=("ci", "nightly"))
    ap.add_argument(
        "--validate-only",
        action="store_true",
        help="Check suite/scenarios/schema/fixtures (CI dry-run)",
    )
    ap.add_argument(
        "--run-timing",
        action="store_true",
        help="SQLite stub timings only (not lidb/postgres parity)",
    )
    ap.add_argument("--warmup", type=int, default=100)
    ap.add_argument("--measure", type=int, default=1000)
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()

    errors = validate_tier_layout()
    if errors:
        for e in errors:
            print(f"registry_oltp_stub: {e}", file=sys.stderr)
        return 1

    if args.validate_only:
        print(
            f"registry_oltp_stub: OK (profile={args.profile}, "
            f"scenarios={len(SCENARIO_IDS)}, schema=sqlite+postgres paths)"
        )
        return 0

    if not args.run_timing:
        print("registry_oltp_stub: validation OK (use --run-timing for SQLite dry-run)")
        return 0

    import os

    os.environ["BENCH_DB_REGISTRY_ALLOW_SQLITE_STUB"] = "1"
    engine_mode, benches, csv_rows = run_benchmarks(
        profile=args.profile, engine_mode="sqlite_stub"
    )
    csv_path = write_csv(csv_rows)
    print(
        f"registry_oltp_stub: wrote {csv_path} ({len(csv_rows)} rows, engine=sqlite_stub)"
    )

    if args.json_out:
        harness = build_harness_json(
            profile=args.profile, engine_mode=engine_mode, benches=benches
        )
        harness["rows"] = csv_rows
        harness["results_csv"] = str(
            csv_path.relative_to(TIER_ROOT.parent.parent)
        )
        harness["notes"] = (
            "SQLite stub only — use registry_oltp.py with POSTGRES_URL + LIDB_ROOT "
            "for PH-DB-5 evidence"
        )
        args.json_out.write_text(
            __import__("json").dumps(harness, indent=2) + "\n", encoding="utf-8"
        )
        print(f"registry_oltp_stub: wrote {args.json_out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
