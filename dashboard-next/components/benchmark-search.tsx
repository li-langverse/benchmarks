"use client";

import Link from "next/link";
import { useMemo, useState } from "react";
import { CoverageStatusBadge } from "@/components/coverage-status-badge";
import {
  formatOsSummary,
  groupByBenchmark,
  groupMatchesQuery,
  rowForOs,
} from "@/lib/benchmark-groups";
import { rowOracleKind, rowWithin1Ulp } from "@/lib/oracle";
import {
  rowMatchesOracleFilter,
  rowMatchesValidityFilter,
  rowMatchesWithin1UlpFilter,
} from "@/lib/row-filters";
import type { SummaryRow } from "@/lib/summary";
import { rowValidityStatus } from "@/lib/validity";

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

function rowMatchesSize(row: SummaryRow, size: string): boolean {
  if (!size) return true;
  const label = row.size_label ?? row.problem_size ?? "";
  return label === size;
}

export function BenchmarkSearch({ rows }: BenchmarkSearchProps) {
  const [query, setQuery] = useState("");
  const [sizeFilter, setSizeFilter] = useState("");
  const [osFilter, setOsFilter] = useState("");
  const [validityFilter, setValidityFilter] = useState("");
  const [oracleFilter, setOracleFilter] = useState("");
  const [withinFilter, setWithinFilter] = useState("");
  const groups = useMemo(() => groupByBenchmark(rows), [rows]);
  const sizeOptions = useMemo(() => uniqueSizeLabels(rows), [rows]);
  const osOptions = useMemo(() => {
    const tags = new Set<string>();
    for (const row of rows) {
      if (row.os && row.os !== "unknown") tags.add(row.os);
    }
    return [...tags].sort();
  }, [rows]);

  const filtered = useMemo(
    () =>
      groups.filter((group) => {
        if (!groupMatchesQuery(group, query)) return false;
        const display = rowForOs(group, osFilter || null);
        if (!rowMatchesSize(display, sizeFilter)) return false;
        if (!rowMatchesValidityFilter(display, validityFilter || null)) return false;
        if (!rowMatchesOracleFilter(display, oracleFilter || null)) return false;
        if (!rowMatchesWithin1UlpFilter(display, withinFilter || null)) return false;
        if (osFilter && !group.variants.some((v) => v.os === osFilter)) return false;
        return true;
      }),
    [groups, query, sizeFilter, osFilter, validityFilter, oracleFilter, withinFilter],
  );

  return (
    <section id="search" className="bench-search" data-testid="benchmark-search">
      <h2>Benchmarks</h2>
      <p className="bench-search-hint">
        One row per benchmark — OS breakdown on the drill-down page. Filter by id, PH id,
        package, pillar, validity, oracle, ULP gate, or problem size (client-side).
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
      <div className="bench-search-filters">
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
        {osOptions.length > 0 ? (
          <>
            <label className="bench-search-label" htmlFor="bench-os-filter">
              OS (drill-down slice)
            </label>
            <select
              id="bench-os-filter"
              className="bench-search-input"
              value={osFilter}
              onChange={(e) => setOsFilter(e.target.value)}
            >
              <option value="">Primary measured OS</option>
              {osOptions.map((os) => (
                <option key={os} value={os}>
                  {os}
                </option>
              ))}
            </select>
          </>
        ) : null}
        <label className="bench-search-label" htmlFor="bench-validity-filter">
          Validity
        </label>
        <select
          id="bench-validity-filter"
          className="bench-search-input"
          value={validityFilter}
          onChange={(e) => setValidityFilter(e.target.value)}
        >
          <option value="">Any validity</option>
          <option value="pass">pass</option>
          <option value="fail">fail</option>
          <option value="unknown">unknown</option>
          <option value="skip">skip (platform not measured)</option>
        </select>
        <label className="bench-search-label" htmlFor="bench-oracle-filter">
          Oracle
        </label>
        <select
          id="bench-oracle-filter"
          className="bench-search-input"
          value={oracleFilter}
          onChange={(e) => setOracleFilter(e.target.value)}
        >
          <option value="">Any oracle</option>
          <option value="analytical">analytical</option>
          <option value="iterative">iterative</option>
          <option value="pending">pending / not measured</option>
        </select>
        <label className="bench-search-label" htmlFor="bench-ulp-filter">
          Within 1 ULP
        </label>
        <select
          id="bench-ulp-filter"
          className="bench-search-input"
          value={withinFilter}
          onChange={(e) => setWithinFilter(e.target.value)}
        >
          <option value="">Any ULP</option>
          <option value="1">yes (≤1 ULP)</option>
          <option value="0">no (&gt;1 ULP)</option>
        </select>
      </div>
      <p className="mono bench-search-count">
        {filtered.length} of {groups.length} benchmarks
      </p>
      <div className="table-wrap">
        <table className="data-table">
          <thead>
            <tr>
              <th>Benchmark</th>
              <th>Size</th>
              <th>Tier</th>
              <th>Oracle</th>
              <th>ULP</th>
              <th>Pillar</th>
              <th>Package</th>
              <th>Platforms</th>
              <th>SOTA</th>
              <th>Validity</th>
              <th>PH ids</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((group) => {
              const row = rowForOs(group, osFilter || null);
              const oracle = rowOracleKind(row);
              const ulp = row.numeric_validity?.ulps;
              const within = rowWithin1Ulp(row);
              const platforms =
                group.variants.length > 1 ? formatOsSummary(group.variants) : row.os ?? "—";
              return (
                <tr key={group.benchmark}>
                  <td>
                    <Link href={`/bench/${group.benchmark}/`}>{group.benchmark}</Link>
                  </td>
                  <td className="mono">
                    {row.size_label ?? row.problem_size ?? "—"}
                  </td>
                  <td>{row.tier}</td>
                  <td className="mono">{oracle}</td>
                  <td className="mono">
                    {ulp != null ? (
                      <>
                        {ulp}
                        {within === true ? " ✓" : within === false ? " ✗" : ""}
                      </>
                    ) : (
                      "—"
                    )}
                  </td>
                  <td>{row.pillar ?? "—"}</td>
                  <td>{row.package ?? "—"}</td>
                  <td className="mono matrix-platforms-cell" title={platforms}>
                    {platforms}
                  </td>
                  <td className="mono">{row.sota_lang ?? "—"}</td>
                  <td>
                    <CoverageStatusBadge row={row} showPerfStatus={false} />
                    <span className="sr-only">{rowValidityStatus(row)}</span>
                  </td>
                  <td className="mono">{row.ph_ids.join(", ") || "—"}</td>
                  <td>
                    <CoverageStatusBadge row={row} showPerfStatus />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {filtered.length === 0 ? (
          <p className="bench-search-empty">No benchmarks match this filter.</p>
        ) : null}
      </div>
    </section>
  );
}
