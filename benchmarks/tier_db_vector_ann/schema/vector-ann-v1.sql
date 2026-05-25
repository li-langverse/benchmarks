-- Vector ANN bench v1 — embedding rows keyed to registry package versions (PH-DB-8).

CREATE TABLE IF NOT EXISTS embedding_corpus (
  id                 BIGSERIAL PRIMARY KEY,
  package_version_id BIGINT REFERENCES package_versions (id) ON DELETE SET NULL,
  dim                INT NOT NULL CHECK (dim > 0),
  embedding          BYTEA NOT NULL,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_embedding_corpus_pkg_ver
  ON embedding_corpus (package_version_id);
