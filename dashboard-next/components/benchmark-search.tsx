"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import type { SummaryRow } from "@/lib/summary";

function uniqueSizeLabels(rows: SummaryRow[]): string[] {
  const labels = new Set<string>();
  for (const row of rows) {
    if (row.size_label) labels.add(row.size_label);
    else if (row.problem_size) labels.add(row.problem_size);
  }
  return [...labels].sort();
}

type BenchmarkSearchProps = {
  rows: SummaryRow[];
};

function rowMatchesQuery(row: SummaryRow, q: string): boolean {
  const needle = q.trim().toLowerCase();
  if (!needle) return true;
  if (row.benchmark.toLowerCase().includes(needle)) return true;
  if (row.package?.toLowerCase().includes(needle)) return true;
  if (row.pillar?.toLowerCase().includes(needle)) return true;
  if (row.ph_ids.some((id) => id.toLowerCase().includes(needle))) return true;
  if (row.os?.toLowerCase().includes(needle)) return true;
  if (row.sota_lang?.toLowerCase().includes(needle)) return true;
  if (row.size_label?.toLowerCase().includes(needle)) return true;
  if (row.problem_size?.toLowerCase().includes(needle)) return true;
  if (row.base_id?.toLowerCase().includes(needle)) return true;
  return false;
}

function rowMatchesSize(row: SummaryRow, size: string): boolean {
  if (!size) return true;
  const label = row.size_label ?? row.problem_size ?? "";
  return label === size;
}

export function BenchmarkSearch({ rows }: BenchmarkSearchProps) {
  const [query, setQuery] = useState("");
  const [sizeFilter, setSizeFilter] = useState("");
  const sizeOptions = useMemo(() => uniqueSizeLabels(rows), [rows]);
  const filtered = useMemo(
    () =>
      rows.filter(
        (row) => rowMatchesQuery(row, query) && rowMatchesSize(row, sizeFilter),
      ),
    [rows, query, sizeFilter],
  );

  return (
    <section id="search" className="bench-search">
      <h2>Benchmarks</h2>
      <p className="bench-search-hint">
        Filter by id, PH id, package, pillar, problem size, OS, or SOTA lang (client-side).
      </p>
      <label className="bench-search-label" htmlFor="bench-filter">
        Search
      </label>
      <input
        id="bench-filter"
        type="search"
        className="bench-search-input"
        placeholder="e.g. horner, N=256, PH-5b, lic"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        autoComplete="off"
      />
      {sizeOptions.length > 0 ? (
        <>
          <label className="bench-search-label" htmlFor="bench-size-filter">
            Problem size
          </label>
          <select
            id="bench-size-filter"
            className="bench-search-input"
            value={sizeFilter}
            onChange={(e) => setSizeFilter(e.target.value)}
          >
            <option value="">All sizes</option>
            {sizeOptions.map((label) => (
              <option key={label} value={label}>
                {label}
              </option>
            ))}
          </select>
        </>
      ) : null}
      <p className="mono bench-search-count">
        {filtered.length} of {rows.length} benchmarks
      </p>
      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>Benchmark</th>
              <th>Size</th>
              <th>Tier</th>
              <th>Pillar</th>
              <th>Package</th>
              <th>OS</th>
              <th>SOTA</th>
              <th>Validity</th>
              <th>PH ids</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((row) => (
              <tr key={row.benchmark}>
                <td>
                  <Link href={`/bench/${row.benchmark}/`}>{row.benchmark}</Link>
                </td>
                <td className="mono">
                  {row.size_label ?? row.problem_size ?? "—"}
                </td>
                <td>{row.tier}</td>
                <td>{row.pillar ?? "—"}</td>
                <td>{row.package ?? "—"}</td>
                <td className="mono">{row.os ?? "—"}</td>
                <td className="mono">{row.sota_lang ?? "—"}</td>
                <td className="mono">{row.validity_status ?? "—"}</td>
                <td className="mono">{row.ph_ids.join(", ") || "—"}</td>
                <td>
                  <Badge status={row.status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 ? (
          <p className="bench-search-empty">No benchmarks match this filter.</p>
        ) : null}
      </div>
    </section>
  );
}
