#!/usr/bin/env python3
"""Registry OLTP harness — lidb embed vs Postgres 15+ (PH-DB-5 / WP-C).

Honest modes:
  validate      — tier layout only (CI default via run-db-registry-bench.sh)
  sqlite_stub   — SQLite timing plumbing (status unknown; not parity evidence)
  postgres_only — Postgres 15+ oracle on registry-v1.sql (lidb null until compare)
  compare       — lidb_embed + Postgres P95 ratio (PH-DB-5 gate when all scenarios green)

Env: POSTGRES_URL, LIDB_ROOT, LIDB_EMBED, LIDB_DATA_DIR, BENCH_DB_REGISTRY_THRESHOLD (1.2).
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
import tomllib
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

TIER_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_IDS = (
    "registry_publish",
    "registry_read_by_name",
    "registry_read_latest",
)
POSTGRES_SCHEMA = TIER_ROOT / "schema/registry-v1.sql"
SQLITE_SCHEMA = TIER_ROOT / "schema/registry-sqlite-v1.sql"
SEED_FIXTURE = TIER_ROOT / "fixtures/seed.toml"
RESULTS_CSV = TIER_ROOT / "results/latest.csv"
DEFAULTS_TOML = TIER_ROOT / "defaults.toml"


@dataclass(frozen=True)
class SeedData:
    publisher: str
    package: str
    versions: list[tuple[str, str, float, str]]
    attestation_kind: str
    attestation_payload: str


@dataclass(frozen=True)
class TimingResult:
    p50_ms: float
    p95_ms: float


def load_seed() -> SeedData:
    raw = tomllib.loads(SEED_FIXTURE.read_text(encoding="utf-8"))
    versions = [tuple(row) for row in raw["versions"]["rows"]]
    return SeedData(
        publisher=raw["publisher"]["name"],
        package=raw["package"]["name"],
        versions=versions,
        attestation_kind=raw["attestation"]["kind"],
        attestation_payload=raw["attestation"]["payload_json"],
    )


def load_defaults() -> dict:
    return tomllib.loads(DEFAULTS_TOML.read_text(encoding="utf-8"))


def threshold_ratio() -> float:
    env = os.environ.get("BENCH_DB_REGISTRY_THRESHOLD", "").strip()
    if env:
        return float(env)
    defaults = load_defaults()
    return float(defaults.get("targets", {}).get("threshold_ratio_vs_postgres", 1.2))


def validate_tier_layout() -> list[str]:
    errors: list[str] = []
    for rel in ("suite.toml", "defaults.toml"):
        if not (TIER_ROOT / rel).is_file():
            errors.append(f"missing {rel}")
    if not POSTGRES_SCHEMA.is_file():
        errors.append("missing schema/registry-v1.sql")
    if not SQLITE_SCHEMA.is_file():
        errors.append("missing schema/registry-sqlite-v1.sql")
    if not SEED_FIXTURE.is_file():
        errors.append("missing fixtures/seed.toml")
    for sid in SCENARIO_IDS:
        bench = TIER_ROOT / "scenarios" / sid / "bench.toml"
        if not bench.is_file():
            errors.append(f"missing scenario {sid}/bench.toml")
            continue
        data = tomllib.loads(bench.read_text(encoding="utf-8"))
        if data.get("name") != sid:
            errors.append(f"{sid}: name mismatch in bench.toml")
        if "load" not in data or data["load"].get("metric") != "latency_p95":
            errors.append(f"{sid}: expected load.metric = latency_p95")
    suite = tomllib.loads((TIER_ROOT / "suite.toml").read_text(encoding="utf-8"))
    for sid in SCENARIO_IDS:
        if sid not in suite.get("default", {}).get("include", []):
            errors.append(f"suite.toml default.include missing {sid}")
    return errors


def p95_ms(samples_ms: list[float]) -> float:
    if not samples_ms:
        return 0.0
    if len(samples_ms) == 1:
        return samples_ms[0]
    ordered = sorted(samples_ms)
    idx = max(0, int(round(0.95 * (len(ordered) - 1))))
    return ordered[idx]


def time_scenario(fn: Callable[[], None], *, warmup: int, measure: int) -> TimingResult:
    for _ in range(warmup):
        fn()
    samples: list[float] = []
    for _ in range(measure):
        t0 = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - t0) * 1000.0)
    return TimingResult(
        p50_ms=statistics.median(samples),
        p95_ms=p95_ms(samples),
    )


def profile_iters(profile: str) -> tuple[int, int]:
    defaults = load_defaults()
    load = defaults.get("load", {})
    warmup = int(load.get("warmup_iters", 100))
    measure = int(load.get("measure_iters", 1000))
    if profile == "ci":
        warmup = min(warmup, 5)
        measure = min(measure, 20)
    return warmup, measure


def resolve_lidb_root() -> Path | None:
    env = os.environ.get("LIDB_ROOT", "").strip()
    if env:
        root = Path(env)
        return root if root.is_dir() else None
    sibling = TIER_ROOT.parent.parent.parent / "lidb"
    return sibling if sibling.is_dir() else None


def resolve_lidb_embed(lidb_root: Path | None) -> Path | None:
    override = os.environ.get("LIDB_EMBED", "").strip()
    if override:
        p = Path(override)
        return p if p.is_file() else None
    if not lidb_root:
        return None
    for candidate in (
        lidb_root / "build" / "smoke" / "lidb_embed",
        lidb_root / "build" / "bench" / "lidb_embed",
        lidb_root / "build" / "lidb_embed",
    ):
        if candidate.is_file():
            return candidate
    return None


def build_lidb_embed(lidb_root: Path) -> Path | None:
    if not shutil.which("cmake"):
        return None
    build_dir = lidb_root / "build" / "bench"
    build_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["cmake", "-S", str(lidb_root), "-B", str(build_dir), "-DCMAKE_BUILD_TYPE=Release"],
        capture_output=True,
        check=False,
    )
    subprocess.run(
        ["cmake", "--build", str(build_dir), "--target", "lidb_embed", "-j"],
        capture_output=True,
        check=False,
    )
    return resolve_lidb_embed(lidb_root)


class EngineBackend(ABC):
    name: str

    @abstractmethod
    def setup(self, seed: SeedData) -> None: ...

    @abstractmethod
    def teardown(self) -> None: ...

    @abstractmethod
    def run_once(self, scenario_id: str, counter: dict[str, int]) -> None: ...


class PostgresBackend(EngineBackend):
    name = "postgres"

    def __init__(self, url: str) -> None:
        self.url = url
        self._conn: Any = None
        self._pkg_id: int | None = None

    def _connect(self) -> Any:
        try:
            import psycopg  # type: ignore

            return psycopg.connect(self.url)
        except ImportError:
            pass
        try:
            import psycopg2  # type: ignore

            return psycopg2.connect(self.url)
        except ImportError as exc:
            raise RuntimeError(
                "postgres backend requires psycopg or psycopg2 "
                "(pip install 'psycopg[binary]' for local real bench)"
            ) from exc

    def setup(self, seed: SeedData) -> None:
        self._conn = self._connect()
        self._conn.autocommit = True
        cur = self._conn.cursor()
        cur.execute(f"DROP SCHEMA IF EXISTS tier_db_registry_bench CASCADE")
        cur.execute("CREATE SCHEMA tier_db_registry_bench")
        cur.execute("SET search_path TO tier_db_registry_bench")
        ddl = POSTGRES_SCHEMA.read_text(encoding="utf-8")
        cur.execute(ddl)
        cur.execute(
            "INSERT INTO publishers (name) VALUES (%s) RETURNING id",
            (seed.publisher,),
        )
        pub_id = cur.fetchone()[0]
        cur.execute(
            "INSERT INTO packages (name, publisher_id) VALUES (%s, %s) RETURNING id",
            (seed.package, pub_id),
        )
        self._pkg_id = cur.fetchone()[0]
        for version, proof, coverage, tree in seed.versions:
            cur.execute(
                """
                INSERT INTO package_versions
                  (package_id, version, proof_digest, coverage_pct, tree_digest)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (self._pkg_id, version, proof, coverage, tree),
            )
            pv_id = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO attestations (package_version_id, kind, payload)
                VALUES (%s, %s, %s::jsonb)
                """,
                (pv_id, seed.attestation_kind, seed.attestation_payload),
            )
        cur.close()

    def teardown(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def run_once(self, scenario_id: str, counter: dict[str, int]) -> None:
        assert self._conn is not None
        cur = self._conn.cursor()
        cur.execute("SET search_path TO tier_db_registry_bench")
        seed_name = load_seed().publisher
        if scenario_id == "registry_publish":
            counter["n"] += 1
            n = counter["n"]
            suffix = f"-{n}"
            cur.execute(
                "INSERT INTO publishers (name) VALUES (%s) ON CONFLICT DO NOTHING",
                (seed_name + suffix,),
            )
            cur.execute(
                "SELECT id FROM publishers WHERE name = %s",
                (seed_name + suffix,),
            )
            pub_id = cur.fetchone()[0]
            pkg_name = f"{load_seed().package}{suffix}"
            cur.execute(
                "INSERT INTO packages (name, publisher_id) VALUES (%s, %s)",
                (pkg_name, pub_id),
            )
            cur.execute("SELECT id FROM packages WHERE name = %s", (pkg_name,))
            pkg_id = cur.fetchone()[0]
            ver = f"0.0.{n}"
            cur.execute(
                """
                INSERT INTO package_versions
                  (package_id, version, proof_digest, coverage_pct, tree_digest)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """,
                (pkg_id, ver, f"sha256:proof{n}", 90.0, f"sha256:tree{n}"),
            )
            pv_id = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO attestations (package_version_id, kind, payload)
                VALUES (%s, %s, '{}'::jsonb)
                """,
                (pv_id, load_seed().attestation_kind),
            )
        elif scenario_id == "registry_read_by_name":
            cur.execute(
                "SELECT id, name, publisher_id, created_at FROM packages WHERE name = %s LIMIT 1",
                (load_seed().package,),
            )
            cur.fetchone()
        else:
            cur.execute(
                """
                SELECT pv.id, pv.version, pv.proof_digest, pv.published_at
                FROM package_versions pv
                JOIN packages p ON p.id = pv.package_id
                WHERE p.name = %s
                ORDER BY pv.published_at DESC
                LIMIT 1
                """,
                (load_seed().package,),
            )
            cur.fetchone()
        cur.close()


class LidbBackend(EngineBackend):
    name = "lidb"

    def __init__(self, embed: Path, data_dir: Path) -> None:
        self.embed = embed
        self.data_dir = data_dir
        self._seed = load_seed()
        self._base_pkg = load_seed().package

    def _run(self, *args: str, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.embed), *args],
            input=stdin,
            capture_output=True,
            text=True,
            check=False,
        )

    @staticmethod
    def _flatten_sql(sql: str) -> str:
        return " ".join(line.strip() for line in sql.splitlines() if line.strip())

    def _exec_json(self, sql: str, params: list[Any]) -> list[dict[str, Any]]:
        proc = self._run(
            "exec-json",
            str(self.data_dir),
            self._flatten_sql(sql),
            stdin=json.dumps([str(p) for p in params]),
        )
        if proc.returncode:
            detail = (proc.stderr or proc.stdout or "").strip()
            raise RuntimeError(detail or "lidb_embed exec-json failed")
        return json.loads(proc.stdout or "{}").get("rows", [])

    def setup(self, seed: SeedData) -> None:
        self._seed = seed
        if self._run("open", str(self.data_dir)).returncode:
            raise RuntimeError("lidb_embed open failed")
        if self._run("migrate", str(self.data_dir)).returncode:
            raise RuntimeError("lidb_embed migrate failed")
        pub = str(uuid.uuid4())
        pkg = str(uuid.uuid4())
        self._exec_json(
            "INSERT INTO publishers (id, name, public_key) VALUES (?, ?, ?)",
            [pub, seed.publisher, "00"],
        )
        self._exec_json(
            "INSERT INTO packages (id, name, description) VALUES (?, ?, ?)",
            [pkg, seed.package, "tier_db_registry bench seed"],
        )
        for version, proof, coverage, tree in seed.versions:
            ver_id = str(uuid.uuid4())
            self._exec_json(
                """
                INSERT INTO package_versions
                  (id, package_id, version, tree_digest, proof_digest, coverage_pct, publisher_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                [ver_id, pkg, version, tree, proof, str(coverage), pub],
            )
            self._exec_json(
                "INSERT INTO attestations (id, package_version_id, kind, digest) VALUES (?, ?, ?, ?)",
                [str(uuid.uuid4()), ver_id, seed.attestation_kind, f"sha256:{version}"],
            )

    def teardown(self) -> None:
        shutil.rmtree(self.data_dir, ignore_errors=True)

    def run_once(self, scenario_id: str, counter: dict[str, int]) -> None:
        if scenario_id == "registry_publish":
            counter["n"] += 1
            n = counter["n"]
            pub = str(uuid.uuid4())
            pkg = str(uuid.uuid4())
            ver = str(uuid.uuid4())
            suffix = f"-{n}"
            self._exec_json(
                "INSERT INTO publishers (id, name, public_key) VALUES (?, ?, ?)",
                [pub, self._seed.publisher + suffix, "00"],
            )
            self._exec_json(
                "INSERT INTO packages (id, name, description) VALUES (?, ?, ?)",
                [pkg, f"{self._base_pkg}{suffix}", "bench publish"],
            )
            self._exec_json(
                """
                INSERT INTO package_versions
                  (id, package_id, version, tree_digest, coverage_pct, publisher_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [ver, pkg, f"0.0.{n}", f"sha256:tree{n}", "90.0", pub],
            )
            self._exec_json(
                "INSERT INTO attestations (id, package_version_id, kind, digest) VALUES (?, ?, ?, ?)",
                [str(uuid.uuid4()), ver, self._seed.attestation_kind, f"sha256:proof{n}"],
            )
        elif scenario_id == "registry_read_by_name":
            self._exec_json(
                "SELECT id, name, description, created_at FROM packages WHERE name = ? LIMIT 1",
                [self._seed.package],
            )
        else:
            self._exec_json(
                "SELECT pv.id, pv.version, pv.proof_digest, pv.published_at "
                "FROM package_versions pv "
                "JOIN packages p ON p.id = pv.package_id "
                "WHERE p.name = ? "
                "ORDER BY pv.published_at DESC LIMIT 1",
                [self._seed.package],
            )


class SqliteStubBackend(EngineBackend):
    """SQLite subset — harness plumbing only (not PH-DB-5 evidence)."""

    name = "sqlite_stub"

    def __init__(self) -> None:
        import sqlite3

        self._sqlite3 = sqlite3
        self._conn: sqlite3.Connection | None = None
        self._seed = load_seed()

    def setup(self, seed: SeedData) -> None:
        self._seed = seed
        self._conn = self._sqlite3.connect(":memory:")
        self._conn.executescript(SQLITE_SCHEMA.read_text(encoding="utf-8"))
        self._conn.row_factory = self._sqlite3.Row
        self._seed_sqlite(self._conn, seed)

    @staticmethod
    def _seed_sqlite(conn: Any, seed: SeedData) -> None:
        conn.execute("INSERT INTO publishers (name) VALUES (?)", (seed.publisher,))
        pub_id = conn.execute(
            "SELECT id FROM publishers WHERE name = ?", (seed.publisher,)
        ).fetchone()["id"]
        conn.execute(
            "INSERT INTO packages (name, publisher_id) VALUES (?, ?)",
            (seed.package, pub_id),
        )
        pkg_id = conn.execute(
            "SELECT id FROM packages WHERE name = ?", (seed.package,)
        ).fetchone()["id"]
        for version, proof, coverage, tree in seed.versions:
            conn.execute(
                """
                INSERT INTO package_versions
                  (package_id, version, proof_digest, coverage_pct, tree_digest)
                VALUES (?, ?, ?, ?, ?)
                """,
                (pkg_id, version, proof, coverage, tree),
            )
            pv_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.execute(
                """
                INSERT INTO attestations (package_version_id, kind, payload)
                VALUES (?, ?, ?)
                """,
                (pv_id, seed.attestation_kind, seed.attestation_payload),
            )
        conn.commit()

    def teardown(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None

    def run_once(self, scenario_id: str, counter: dict[str, int]) -> None:
        assert self._conn is not None
        if scenario_id == "registry_publish":
            counter["n"] += 1
            n = counter["n"]
            suffix = f"-{n}"
            self._conn.execute(
                "INSERT OR IGNORE INTO publishers (name) VALUES (?)",
                (self._seed.publisher + suffix,),
            )
            pub_id = self._conn.execute(
                "SELECT id FROM publishers WHERE name = ?",
                (self._seed.publisher + suffix,),
            ).fetchone()["id"]
            pkg_name = f"{self._seed.package}{suffix}"
            self._conn.execute(
                "INSERT INTO packages (name, publisher_id) VALUES (?, ?)",
                (pkg_name, pub_id),
            )
            pkg_id = self._conn.execute(
                "SELECT id FROM packages WHERE name = ?", (pkg_name,)
            ).fetchone()["id"]
            self._conn.execute(
                """
                INSERT INTO package_versions
                  (package_id, version, proof_digest, coverage_pct, tree_digest)
                VALUES (?, ?, ?, ?, ?)
                """,
                (pkg_id, f"0.0.{n}", f"sha256:proof{n}", 90.0, f"sha256:tree{n}"),
            )
            pv_id = self._conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            self._conn.execute(
                """
                INSERT INTO attestations (package_version_id, kind, payload)
                VALUES (?, ?, ?)
                """,
                (pv_id, self._seed.attestation_kind, self._seed.attestation_payload),
            )
            self._conn.commit()
        elif scenario_id == "registry_read_by_name":
            self._conn.execute(
                "SELECT id, name, publisher_id, created_at FROM packages WHERE name = ? LIMIT 1",
                (self._seed.package,),
            ).fetchone()
        else:
            self._conn.execute(
                """
                SELECT pv.id, pv.version, pv.proof_digest, pv.published_at
                FROM package_versions pv
                JOIN packages p ON p.id = pv.package_id
                WHERE p.name = ?
                ORDER BY pv.published_at DESC
                LIMIT 1
                """,
                (self._seed.package,),
            ).fetchone()


def bench_engine(
    backend: EngineBackend,
    *,
    profile: str,
) -> dict[str, TimingResult]:
    seed = load_seed()
    warmup, measure = profile_iters(profile)
    backend.setup(seed)
    results: dict[str, TimingResult] = {}
    try:
        for sid in SCENARIO_IDS:
            counter: dict[str, int] = {"n": 0}

            def run_once() -> None:
                backend.run_once(sid, counter)

            results[sid] = time_scenario(run_once, warmup=warmup, measure=measure)
    finally:
        backend.teardown()
    return results


def lidb_available() -> tuple[Path, Path] | None:
    root = resolve_lidb_root()
    if not root:
        return None
    embed = resolve_lidb_embed(root) or build_lidb_embed(root)
    if not embed:
        return None
    return embed, root


def postgres_url() -> str | None:
    url = os.environ.get("POSTGRES_URL", "").strip()
    return url or None


def resolve_engine_mode(requested: str) -> str:
    if requested != "auto":
        return requested
    pg = postgres_url()
    lidb = lidb_available()
    if lidb and pg:
        return "compare"
    if pg:
        return "postgres_only"
    if lidb:
        return "lidb_only"
    if os.environ.get("BENCH_DB_REGISTRY_ALLOW_SQLITE_STUB", "").strip() in (
        "1",
        "true",
        "yes",
    ):
        return "sqlite_stub"
    return "stub"


@dataclass
class ScenarioBench:
    scenario_id: str
    lidb: TimingResult | None
    postgres: TimingResult | None
    sqlite_stub: TimingResult | None

    def ratio_vs_postgres(self) -> float | None:
        if self.lidb is None or self.postgres is None:
            return None
        if self.postgres.p95_ms <= 0:
            return None
        return round(self.lidb.p95_ms / self.postgres.p95_ms, 4)

    def scenario_status(self, threshold: float) -> str:
        ratio = self.ratio_vs_postgres()
        if ratio is not None:
            if ratio <= threshold:
                return "green"
            return "red"
        if self.sqlite_stub is not None:
            return "unknown"
        if self.postgres is not None or self.lidb is not None:
            return "unknown"
        return "stub"


def run_benchmarks(*, profile: str, engine_mode: str) -> tuple[str, list[ScenarioBench], list[dict]]:
    seed = load_seed()
    threshold = threshold_ratio()
    benches: list[ScenarioBench] = []
    csv_rows: list[dict] = []

    lidb_timings: dict[str, TimingResult] | None = None
    pg_timings: dict[str, TimingResult] | None = None
    sqlite_timings: dict[str, TimingResult] | None = None

    if engine_mode in ("compare", "postgres_only"):
        url = postgres_url()
        if not url:
            raise RuntimeError("postgres_only/compare requires POSTGRES_URL")
        pg = PostgresBackend(url)
        pg_timings = bench_engine(pg, profile=profile)

    if engine_mode in ("compare", "lidb_only"):
        lidb_info = lidb_available()
        if not lidb_info:
            raise RuntimeError("lidb compare/only requires built lidb_embed (set LIDB_ROOT)")
        embed, _root = lidb_info
        data_dir = Path(
            os.environ.get("LIDB_DATA_DIR", tempfile.mkdtemp(prefix="tier-db-registry-lidb-"))
        )
        if not os.environ.get("LIDB_DATA_DIR"):
            os.environ["LIDB_DATA_DIR"] = str(data_dir)
        lb = LidbBackend(embed, data_dir)
        lidb_timings = bench_engine(lb, profile=profile)

    if engine_mode == "sqlite_stub":
        sqlite_timings = bench_engine(SqliteStubBackend(), profile=profile)

    for sid in SCENARIO_IDS:
        bench = ScenarioBench(
            scenario_id=sid,
            lidb=lidb_timings.get(sid) if lidb_timings else None,
            postgres=pg_timings.get(sid) if pg_timings else None,
            sqlite_stub=sqlite_timings.get(sid) if sqlite_timings else None,
        )
        benches.append(bench)
        if bench.lidb:
            csv_rows.append(
                {
                    "benchmark": sid,
                    "lang": "lidb",
                    "metric": "latency_p95",
                    "value": round(bench.lidb.p95_ms, 4),
                    "unit": "ms",
                    "variant": "registry_oltp",
                }
            )
        if bench.postgres:
            csv_rows.append(
                {
                    "benchmark": sid,
                    "lang": "postgres",
                    "metric": "latency_p95",
                    "value": round(bench.postgres.p95_ms, 4),
                    "unit": "ms",
                    "variant": "registry_oltp",
                }
            )
        if bench.sqlite_stub:
            csv_rows.append(
                {
                    "benchmark": sid,
                    "lang": "sqlite_stub",
                    "metric": "latency_p95",
                    "value": round(bench.sqlite_stub.p95_ms, 4),
                    "unit": "ms",
                    "variant": "registry_oltp",
                }
            )

    _ = seed
    _ = threshold
    return engine_mode, benches, csv_rows


def manifest_status(engine_mode: str, benches: list[ScenarioBench], threshold: float) -> str:
    if engine_mode == "stub":
        return "stub"
    statuses = {b.scenario_status(threshold) for b in benches}
    if "red" in statuses:
        return "fail"
    if statuses == {"green"}:
        return "pass"
    return "unknown"


def build_harness_json(
    *,
    profile: str,
    engine_mode: str,
    benches: list[ScenarioBench],
) -> dict[str, Any]:
    threshold = threshold_ratio()
    scenarios: list[dict[str, Any]] = []
    for b in benches:
        engines: dict[str, Any] = {"lidb": None, "postgres": None}
        if b.lidb:
            engines["lidb"] = {
                "p50_ms": round(b.lidb.p50_ms, 4),
                "p95_ms": round(b.lidb.p95_ms, 4),
            }
        if b.postgres:
            engines["postgres"] = {
                "p50_ms": round(b.postgres.p50_ms, 4),
                "p95_ms": round(b.postgres.p95_ms, 4),
            }
        if b.sqlite_stub:
            engines["sqlite_stub"] = {
                "p50_ms": round(b.sqlite_stub.p50_ms, 4),
                "p95_ms": round(b.sqlite_stub.p95_ms, 4),
            }
        scenarios.append(
            {
                "id": b.scenario_id,
                "metric": "latency_p95",
                "unit": "ms",
                "lower_is_better": True,
                "threshold_ratio_vs_postgres": threshold,
                "status": b.scenario_status(threshold),
                "engines": engines,
                "ratio_vs_postgres": b.ratio_vs_postgres(),
                "ph_ids": ["PH-DB-5"],
                "ph_dependencies": ["PH-DB-1", "PH-DB-4"],
            }
        )
    return {
        "engine_mode": engine_mode,
        "profile": profile,
        "threshold_ratio_vs_postgres": threshold,
        "status": manifest_status(engine_mode, benches, threshold),
        "scenarios": scenarios,
        "ph_ids": ["PH-DB-5"],
        "ph_dependencies": ["PH-DB-1", "PH-DB-4"],
        "notes": _engine_mode_note(engine_mode),
    }


def _engine_mode_note(engine_mode: str) -> str:
    notes = {
        "compare": "Measured lidb_embed vs Postgres 15+ on registry workloads",
        "postgres_only": "Postgres oracle only — lidb ratio pending compare mode",
        "lidb_only": "lidb_embed timings only — set POSTGRES_URL for ratio (PH-DB-5 gate)",
        "sqlite_stub": "SQLite stub timing only — not PH-DB-5 parity evidence",
        "stub": "Harness not run — layout validation only",
    }
    return notes.get(engine_mode, engine_mode)


def write_csv(rows: list[dict]) -> Path:
    RESULTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["benchmark", "lang", "metric", "value", "unit", "variant"]
    with RESULTS_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)
    return RESULTS_CSV


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--profile", default="ci", choices=("ci", "nightly"))
    ap.add_argument(
        "--engine",
        default=os.environ.get("BENCH_DB_REGISTRY_ENGINE", "auto"),
        choices=(
            "auto",
            "compare",
            "postgres_only",
            "lidb_only",
            "sqlite_stub",
            "validate",
            "stub",
        ),
    )
    ap.add_argument("--validate-only", action="store_true")
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()

    errors = validate_tier_layout()
    if errors:
        for e in errors:
            print(f"registry_oltp: {e}", file=sys.stderr)
        return 1

    if args.validate_only or args.engine == "validate":
        print(
            f"registry_oltp: OK (profile={args.profile}, scenarios={len(SCENARIO_IDS)})"
        )
        return 0

    engine_mode = resolve_engine_mode(args.engine)
    if engine_mode == "stub":
        print(
            "registry_oltp: no engines (set POSTGRES_URL and/or LIDB_ROOT; "
            "or BENCH_DB_REGISTRY_ALLOW_SQLITE_STUB=1)",
            file=sys.stderr,
        )
        return 2

    try:
        engine_mode, benches, csv_rows = run_benchmarks(
            profile=args.profile, engine_mode=engine_mode
        )
    except RuntimeError as exc:
        print(f"registry_oltp: {exc}", file=sys.stderr)
        return 1

    if csv_rows:
        csv_path = write_csv(csv_rows)
        print(
            f"registry_oltp: wrote {csv_path} ({len(csv_rows)} rows, engine_mode={engine_mode})"
        )

    harness = build_harness_json(
        profile=args.profile, engine_mode=engine_mode, benches=benches
    )
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(harness, indent=2) + "\n", encoding="utf-8")
        print(f"registry_oltp: wrote {args.json_out} (status={harness['status']})")

    return 0 if harness["status"] != "fail" else 1


if __name__ == "__main__":
    raise SystemExit(main())
