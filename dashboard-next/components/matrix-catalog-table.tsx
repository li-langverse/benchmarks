"use client";

import Link from "next/link";
import { useMemo } from "react";
import { useSearchParams } from "next/navigation";
import { Badge } from "@/components/ui/badge";
import type { MatrixRow } from "@/lib/matrix";

type MatrixCatalogTableProps = {
  rows: MatrixRow[];
};

function parseTierFilter(raw: string | null): number | null {
  if (raw == null || raw.trim() === "") return null;
  const tier = Number(raw);
  return Number.isFinite(tier) ? tier : null;
}

export function MatrixCatalogTable({ rows }: MatrixCatalogTableProps) {
  const searchParams = useSearchParams();
  const tierFilter = parseTierFilter(searchParams.get("tier"));

  const filtered = useMemo(() => {
    if (tierFilter == null) return rows;
    return rows.filter((row) => row.tier === tierFilter);
  }, [rows, tierFilter]);

  return (
    <section>
      <h3 className="section-heading">Catalog sections</h3>
      {tierFilter != null ? (
        <p className="mono matrix-filter-meta" role="status">
          Tier {tierFilter} filter: {filtered.length} of {rows.length} rows.{" "}
          <Link href="/matrix/">Show all tiers</Link>
        </p>
      ) : null}
      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>Id</th>
              <th>Tier</th>
              <th>Category</th>
              <th>Repo</th>
              <th>Metric</th>
              <th>Status</th>
              <th>Ratio</th>
              <th>PH ids</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((row) => (
              <tr key={`${row.category}-${row.id}`}>
                <td>
                  <Link href={`/bench/${row.id}/`}>{row.id}</Link>
                </td>
                <td>{row.tier}</td>
                <td>{row.category}</td>
                <td>{row.repo}</td>
                <td>{row.metric}</td>
                <td>
                  <Badge status={row.status} />
                </td>
                <td className="mono">
                  {row.ratio_vs_reference != null
                    ? row.ratio_vs_reference.toFixed(4)
                    : "—"}
                </td>
                <td className="mono">{row.ph_ids.join(", ") || "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 ? (
          <p className="bench-search-empty">
            No matrix rows for tier {tierFilter}.{" "}
            <Link href="/matrix/">Clear filter</Link>
          </p>
        ) : null}
      </div>
    </section>
  );
}
