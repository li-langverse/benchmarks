"use client";

import Link from "next/link";
import { useMemo } from "react";
import { useSearchParams } from "next/navigation";
import { CoverageStatusBadge } from "@/components/coverage-status-badge";
import type { MatrixRow } from "@/lib/matrix";
import { oracleLabel, rowOracleKind, rowWithin1Ulp } from "@/lib/oracle";
import {
  rowMatchesOracleFilter,
  rowMatchesValidityFilter,
  rowMatchesWithin1UlpFilter,
} from "@/lib/row-filters";
import type { SummaryRow } from "@/lib/summary";

type MatrixCatalogTableProps = {
  rows: MatrixRow[];
  summaryById?: Record<string, SummaryRow>;
};

const FACET_TIPS: Record<string, string> = {
  Benchmark: "Catalog id — links to per-bench drill-down.",
  Size: "Problem size label from catalog or ingest.",
  Tier: "0=stability, 1=micro correctness, 2+=macro.",
  Oracle: "Analytical closed form vs iterative C loop vs not measured.",
  ULP: "ULPs vs analytical oracle from verify CSV (when present).",
  Validity: "Harness/stability pass — required before green perf claims.",
};

function rowSizeLabel(row: MatrixRow): string {
  return row.size_label ?? row.problem_size ?? "—";
}

function matrixHref(params: Record<string, string | undefined>): string {
  const q = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v) q.set(k, v);
  }
  const s = q.toString();
  return s ? `/matrix/?${s}` : "/matrix/";
}

export function MatrixCatalogTable({ rows, summaryById = {} }: MatrixCatalogTableProps) {
  const searchParams = useSearchParams();
  const tierFilter = searchParams.get("tier");
  const sizeFilter = searchParams.get("size");
  const validityFilter = searchParams.get("validity");
  const oracleFilter = searchParams.get("oracle");
  const withinFilter = searchParams.get("within_1ulp");

  const sizeOptions = useMemo(() => {
    const labels = new Set<string>();
    for (const row of rows) {
      const label = row.size_label ?? row.problem_size;
      if (label) labels.add(label);
    }
    return [...labels].sort();
  }, [rows]);

  const baseParams = {
    tier: tierFilter ?? undefined,
    size: sizeFilter ?? undefined,
    validity: validityFilter ?? undefined,
    oracle: oracleFilter ?? undefined,
    within_1ulp: withinFilter ?? undefined,
  };

  const filtered = useMemo(() => {
    return rows.filter((row) => {
      if (tierFilter && String(row.tier) !== tierFilter) return false;
      if (sizeFilter) {
        const label = row.size_label ?? row.problem_size ?? "";
        if (label !== sizeFilter) return false;
      }
      const summaryRow = summaryById[row.id];
      if (!rowMatchesValidityFilter(summaryRow, validityFilter)) return false;
      if (!rowMatchesOracleFilter(summaryRow, oracleFilter)) return false;
      if (!rowMatchesWithin1UlpFilter(summaryRow, withinFilter)) return false;
      return true;
    });
  }, [
    rows,
    tierFilter,
    sizeFilter,
    validityFilter,
    oracleFilter,
    withinFilter,
    summaryById,
  ]);

  const activeFilters = [
    tierFilter ? `tier ${tierFilter}` : null,
    sizeFilter ? `size ${sizeFilter}` : null,
    validityFilter ? `validity ${validityFilter}` : null,
    oracleFilter ? `oracle ${oracleFilter}` : null,
    withinFilter != null ? `within_1ulp ${withinFilter}` : null,
  ].filter(Boolean);

  return (
    <section>
      <p className="matrix-filter-meta mono">
        Filters:{" "}
        <Link href={matrixHref({})}>clear all</Link>
        {" · "}
        <Link href={matrixHref({ ...baseParams, validity: "fail" })}>validity fail</Link>
        {" · "}
        <Link href={matrixHref({ ...baseParams, oracle: "analytical" })}>analytical</Link>
        {" · "}
        <Link href={matrixHref({ ...baseParams, within_1ulp: "0" })}>ULP &gt; 1</Link>
        {" · "}
        <Link href={matrixHref({ ...baseParams, oracle: "pending" })}>pending</Link>
      </p>
      {sizeOptions.length > 0 ? (
        <p className="mono" style={{ marginBottom: "0.75rem" }}>
          Size:{" "}
          <Link href={matrixHref({ tier: tierFilter ?? undefined })}>all</Link>
          {sizeOptions.map((label) => (
            <span key={label}>
              {" · "}
              <Link
                href={matrixHref({
                  tier: tierFilter ?? undefined,
                  size: label,
                  validity: validityFilter ?? undefined,
                  oracle: oracleFilter ?? undefined,
                  within_1ulp: withinFilter ?? undefined,
                })}
              >
                {label}
              </Link>
            </span>
          ))}
        </p>
      ) : null}
      {activeFilters.length > 0 ? (
        <p className="mono matrix-filter-active">
          Active: {activeFilters.join(" · ")}
        </p>
      ) : null}
      <p className="mono bench-search-count">
        {filtered.length} of {rows.length} catalog rows
      </p>
      <div className="table-wrap">
        <table className="data-table matrix-catalog-table">
          <thead>
            <tr>
              {(
                [
                  "Benchmark",
                  "Size",
                  "Tier",
                  "Category",
                  "Metric",
                  "Ratio",
                  "Oracle",
                  "ULP",
                  "Perf",
                  "Validity",
                ] as const
              ).map((col) => (
                <th key={col} title={FACET_TIPS[col] ?? undefined}>
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map((row) => {
              const summaryRow = summaryById[row.id];
              const oracleKind = summaryRow ? rowOracleKind(summaryRow) : "pending";
              const ulp = summaryRow?.numeric_validity?.ulps;
              const within = summaryRow ? rowWithin1Ulp(summaryRow) : null;
              return (
                <tr key={row.id}>
                  <td>
                    <Link href={`/bench/${row.id}/`} title={row.id}>
                      {row.id}
                    </Link>
                    {row.base_id ? (
                      <span className="mono matrix-base-id"> ← {row.base_id}</span>
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
                  <td className="mono matrix-oracle-cell" title={oracleLabel(oracleKind)}>
                    {oracleKind}
                  </td>
                  <td className="mono">
                    {ulp != null ? (
                      <>
                        {ulp}
                        {within === true ? (
                          <span className="matrix-ulp-ok"> ≤1</span>
                        ) : within === false ? (
                          <span className="matrix-ulp-bad"> &gt;1</span>
                        ) : null}
                      </>
                    ) : (
                      "—"
                    )}
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
          <p className="bench-search-empty">No rows match the current filters.</p>
        ) : null}
      </div>
    </section>
  );
}
