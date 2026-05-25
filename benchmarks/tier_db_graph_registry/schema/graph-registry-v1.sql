-- Graph registry bench v1 — dependency edges on registry packages (PH-DB-G1).
-- Apply after tier_db_registry/schema/registry-v1.sql.

CREATE TABLE IF NOT EXISTS package_deps (
  from_package_id BIGINT NOT NULL REFERENCES packages (id) ON DELETE CASCADE,
  to_package_id   BIGINT NOT NULL REFERENCES packages (id) ON DELETE CASCADE,
  CONSTRAINT package_deps_no_self CHECK (from_package_id <> to_package_id),
  PRIMARY KEY (from_package_id, to_package_id)
);

CREATE INDEX IF NOT EXISTS idx_package_deps_to
  ON package_deps (to_package_id);

CREATE INDEX IF NOT EXISTS idx_package_deps_from
  ON package_deps (from_package_id);
