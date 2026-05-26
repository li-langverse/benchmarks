-- SQLite subset of registry-v1.sql for local stub harness (not parity oracle).
-- Postgres 15+ DDL remains canonical: schema/registry-v1.sql

CREATE TABLE IF NOT EXISTS publishers (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL UNIQUE,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS packages (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  name         TEXT NOT NULL UNIQUE,
  publisher_id INTEGER NOT NULL REFERENCES publishers(id),
  created_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS package_versions (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  package_id    INTEGER NOT NULL REFERENCES packages(id),
  version       TEXT NOT NULL,
  proof_digest  TEXT,
  coverage_pct  REAL,
  tree_digest   TEXT,
  published_at  TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE (package_id, version)
);

CREATE TABLE IF NOT EXISTS attestations (
  id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  package_version_id INTEGER NOT NULL REFERENCES package_versions(id),
  kind               TEXT NOT NULL,
  payload            TEXT NOT NULL DEFAULT '{}',
  created_at         TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS yanks (
  package_version_id INTEGER PRIMARY KEY REFERENCES package_versions(id),
  reason             TEXT NOT NULL,
  yanked_at          TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS blocklist (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  pattern    TEXT NOT NULL UNIQUE,
  reason     TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_package_versions_package_id
  ON package_versions (package_id);

CREATE INDEX IF NOT EXISTS idx_package_versions_published_at
  ON package_versions (published_at DESC);
