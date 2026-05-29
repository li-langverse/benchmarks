import { loadCatalogAudit } from "@/lib/catalog-audit";

export function CatalogAuditStrip() {
  const audit = loadCatalogAudit();
  if (!audit) return null;
  return (
    <section className="coverage-honesty bento-full" aria-label="Catalog audit">
      <p>
        <strong>{audit.workload_dir_present_count}</strong> workloads on disk ·{" "}
        <strong>{audit.harness_pending_count}</strong> catalog rows still{" "}
        <code>harness pending</code> · <strong>{audit.workload_dir_missing_count}</strong>{" "}
        broken paths
      </p>
      {audit.workload_dir_missing_count > 0 ? (
        <p className="ingest-meta">
          Run <code>python3 scripts/catalog/audit-catalog-coverage.py</code> after adding
          workloads under <code>benchmarks/workloads/</code>.
        </p>
      ) : null}
    </section>
  );
}
