"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { Badge } from "@/components/ui/badge";
import type { SummaryRow } from "@/lib/summary";

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
  return false;
}

export function BenchmarkSearch({ rows }: BenchmarkSearchProps) {
  const [query, setQuery] = useState("");
  const filtered = useMemo(
    () => rows.filter((row) => rowMatchesQuery(row, query)),
    [rows, query],
  );

  return (
    <section id="search" className="bench-search">
      <h2>Benchmarks</h2>
      <p className="bench-search-hint">
        Filter by id, PH id, package, pillar, OS, or SOTA lang (client-side).
      </p>
      <label className="bench-search-label" htmlFor="bench-filter">
        Search
      </label>
      <input
        id="bench-filter"
        type="search"
        className="bench-search-input"
        placeholder="e.g. horner, PH-5b, lic, numerics"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        autoComplete="off"
      />
      <p className="mono bench-search-count">
        {filtered.length} of {rows.length} benchmarks
      </p>
      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>Benchmark</th>
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
