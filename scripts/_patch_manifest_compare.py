#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "scripts/ingest/write-tier-db-registry-manifest.py"
t = p.read_text(encoding="utf-8")

if "scenario_from_compare_row" in t:
    print("already patched")
    raise SystemExit(0)

insert_fn = '''

def scenario_from_compare_row(row: dict) -> dict:
    ratio = row.get("ratio_vs_postgres")
    status = row.get("status") or "unknown"
    if ratio is not None and status not in ("passed", "failed"):
        status = "passed" if ratio <= THRESHOLD else "failed"
    return {
        "id": row["benchmark"],
        "metric": "latency_p95",
        "unit": "ms",
        "lower_is_better": True,
        "threshold_ratio_vs_postgres": THRESHOLD,
        "status": status,
        "engines": {
            "lidb": {"p95_ms": row.get("lidb_p95_ms"), "p50_ms": row.get("lidb_p50_ms")},
            "postgres": {"p95_ms": row.get("postgres_p95_ms")},
        },
        "ratio_vs_postgres": ratio,
        "ph_ids": [PH_GATE],
        "ph_dependencies": PH_DEPENDENCIES,
        "notes": NOTES.get(row["benchmark"], ""),
    }

'''

t = t.replace("\n\ndef build_manifest(", insert_fn + "\n\ndef build_manifest(")

old = """        scenarios = [
            scenario_from_harness_row(sid, by_id[sid])
            if sid in by_id
            else scenario_stub(sid, status="unknown")
            for sid in SCENARIO_IDS
        ]
        engine_mode = harness.get("engine_mode", "sqlite_local_stub")"""

new = """        if harness.get("engine_mode") in ("lidb_vs_postgres", "lidb_only"):
            scenarios = [
                scenario_from_compare_row(by_id[sid])
                if sid in by_id
                else scenario_stub(sid, status="unknown")
                for sid in SCENARIO_IDS
            ]
        else:
            scenarios = [
                scenario_from_harness_row(sid, by_id[sid])
                if sid in by_id
                else scenario_stub(sid, status="unknown")
                for sid in SCENARIO_IDS
            ]
        engine_mode = harness.get("engine_mode", "sqlite_local_stub")"""

t = t.replace(old, new)

old_main = """    ap.add_argument(
        "--from-harness",
        type=Path,
        help="Harness JSON from registry_oltp_stub.py (--run-timing)",
    )
    args = ap.parse_args()

    harness: dict | None = None
    if args.from_harness:
        harness = json.loads(args.from_harness.read_text(encoding="utf-8"))"""

new_main = """    ap.add_argument(
        "--from-harness",
        type=Path,
        help="Harness JSON from registry_oltp_stub.py (--run-timing)",
    )
    ap.add_argument(
        "--from-compare",
        type=Path,
        help="Compare JSON from lidb/scripts/bench/registry_oltp_compare.py",
    )
    args = ap.parse_args()

    harness: dict | None = None
    if args.from_compare:
        harness = json.loads(args.from_compare.read_text(encoding="utf-8"))
    elif args.from_harness:
        harness = json.loads(args.from_harness.read_text(encoding="utf-8"))"""

t = t.replace(old_main, new_main)

old_status = """    if args.status:
        status = args.status
    elif args.stub or harness is None:
        status = "stub"
    else:
        status = "unknown"

    manifest = build_manifest(profile=args.profile, status=status, harness=harness)"""

new_status = """    if args.status:
        status = args.status
    elif args.stub or harness is None:
        status = "stub"
    elif harness and harness.get("engine_mode") == "lidb_vs_postgres":
        rows = harness.get("rows") or []
        if rows and all(r.get("status") == "passed" for r in rows if r.get("ratio_vs_postgres") is not None):
            status = "passed"
        elif any(r.get("ratio_vs_postgres") is not None for r in rows):
            status = "failed"
        else:
            status = "unknown"
    else:
        status = "unknown"

    manifest = build_manifest(profile=args.profile, status=status, harness=harness)"""

t = t.replace(old_status, new_status)
p.write_text(t, encoding="utf-8")
print("patched write-tier-db-registry-manifest.py")
