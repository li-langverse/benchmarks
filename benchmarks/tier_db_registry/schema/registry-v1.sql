-- Registry OLTP schema v1 (shared by lidb, lip, tier_db_registry bench).
-- Postgres 15+ compatible subset; lidb implements same tables for parity runs.

CREATE TABLE IF NOT EXISTS publishers (
  id         BIGSERIAL PRIMARY KEY,
  name       TEXT NOT NULL UNIQUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS packages (
  id          BIGSERIAL PRIMARY KEY,
  name        TEXT NOT NULL UNIQUE,
  publisher_id BIGINT NOT NULL REFERENCES publishers(id),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS package_versions (
  id            BIGSERIAL PRIMARY KEY,
  package_id    BIGINT NOT NULL REFERENCES packages(id),
  version       TEXT NOT NULL,
  proof_digest  TEXT,
  coverage_pct  REAL,
  tree_digest   TEXT,
  published_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (package_id, version)
);

CREATE TABLE IF NOT EXISTS attestations (
  id                 BIGSERIAL PRIMARY KEY,
  package_version_id BIGINT NOT NULL REFERENCES package_versions(id),
  kind               TEXT NOT NULL,
  payload            JSONB NOT NULL DEFAULT '{}',
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS yanks (
  package_version_id BIGINT PRIMARY KEY REFERENCES package_versions(id),
  reason             TEXT NOT NULL,
  yanked_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS blocklist (
  id         BIGSERIAL PRIMARY KEY,
  pattern    TEXT NOT NULL UNIQUE,
  reason     TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_package_versions_package_id
  ON package_versions (package_id);

CREATE INDEX IF NOT EXISTS idx_package_versions_published_at
  ON package_versions (published_at DESC);
