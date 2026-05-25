"use client";

import Link from "next/link";
import { useMemo } from "react";
import { useSearchParams } from "next/navigation";
import { CoverageStatusBadge } from "@/components/coverage-status-badge";
import type { MatrixRow } from "@/lib/matrix";
import type { SummaryRow } from "@/lib/summary";

type MatrixCatalogTableProps = {
  rows: MatrixRow[];
  summaryById?: Record<string, SummaryRow>;
};

function rowSizeLabel(row: MatrixRow): string {
  return row.size_label ?? row.problem_size ?? "—";
}

export function MatrixCatalogTable({ rows, summaryById = {} }: MatrixCatalogTableProps) {
  const searchParams = useSearchParams();
  const tierFilter = searchParams.get("tier");
  const sizeFilter = searchParams.get("size");

  const sizeOptions = useMemo(() => {
    const labels = new Set<string>();
    for (const row of rows) {
      const label = row.size_label ?? row.problem_size;
      if (label) labels.add(label);
    }
    return [...labels].sort();
  }, [rows]);

  const filtered = useMemo(() => {
    return rows.filter((row) => {
      if (tierFilter && String(row.tier) !== tierFilter) return false;
      if (!sizeFilter) return true;
      const label = row.size_label ?? row.problem_size ?? "";
      return label === sizeFilter;
    });
  }, [rows, tierFilter, sizeFilter]);

  return (
    <section>
      {sizeOptions.length > 0 ? (
        <p className="mono" style={{ marginBottom: "0.75rem" }}>
          Size filter:{" "}
          <Link href="/matrix/">all</Link>
          {sizeOptions.map((label) => (
            <span key={label}>
              {" · "}
              <Link
                href={
                  tierFilter
                    ? `/matrix/?tier=${tierFilter}&size=${encodeURIComponent(label)}`
                    : `/matrix/?size=${encodeURIComponent(label)}`
                }
              >
                {label}
              </Link>
            </span>
          ))}
          {tierFilter ? (
            <span style={{ color: "var(--muted)" }}> (tier {tierFilter})</span>
          ) : null}
        </p>
      ) : null}
      <p className="mono bench-search-count">
        {filtered.length} of {rows.length} catalog rows
      </p>
      <div className="table-wrap">
        <table className="data-table matrix-catalog-table">
          <thead>
            <tr>
              <th>Benchmark</th>
              <th>Size</th>
              <th>Tier</th>
              <th>Category</th>
              <th>Metric</th>
              <th>Ratio</th>
              <th>Perf</th>
              <th>Validity</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((row) => {
              const summaryRow = summaryById[row.id];
              return (
                <tr key={row.id}>
                  <td>
                    <Link href={`/bench/${row.id}/`}>{row.id}</Link>
                    {row.base_id ? (
                      <span className="mono" style={{ color: "var(--muted)" }}>
                        {" "}
                        ← {row.base_id}
                      </span>
                    ) : null}
                  </td>
                  <td className="mono">{rowSizeLabel(row)}</td>
                  <td>{row.tier}</td>
                  <td>{row.category}</td>
                  <td>{row.metric}</td>
                  <td className="mono">
                    {row.ratio_vs_reference != null
                      ? `${row.ratio_vs_reference.toFixed(3)}×`
                      : "—"}
                  </td>
                  <td>
                    {summaryRow ? (
                      <CoverageStatusBadge row={summaryRow} showPerfStatus />
                    ) : (
                      <span className="badge badge-unknown badge-pending">pending</span>
                    )}
                  </td>
                  <td>
                    {summaryRow ? (
                      <CoverageStatusBadge row={summaryRow} showPerfStatus={false} />
                    ) : (
                      <span className="badge badge-unknown">—</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {filtered.length === 0 ? (
          <p className="bench-search-empty">No rows match tier/size filters.</p>
        ) : null}
      </div>
    </section>
  );
}
