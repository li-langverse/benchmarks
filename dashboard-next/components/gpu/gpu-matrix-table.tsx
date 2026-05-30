"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import {
  GpuBackendBadge,
  GpuTimingCell,
  GpuValidityCell,
} from "@/components/gpu/gpu-backend-cells";
import type { GpuMatrixRow } from "@/lib/lig-gpu-matrix-types";
import { backendLabel, compareBackends } from "@/lib/lig-gpu-matrix-types";

type GpuMatrixTableProps = {
  rows: GpuMatrixRow[];
  primaryBackend?: string;
};

const KIND_LABELS: Record<string, string> = {
  lig_kernel: "LiG kernel",
  scientific_algo: "Scientific algo",
  tier2_sim: "Tier-2 sim",
};

export function GpuMatrixTable({ rows, primaryBackend = "cuda" }: GpuMatrixTableProps) {
  const [kindFilter, setKindFilter] = useState<string>("all");
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return rows.filter((r) => {
      if (kindFilter !== "all" && r.workload_kind !== kindFilter) return false;
      if (!q) return true;
      return (
        r.workload_id.toLowerCase().includes(q) ||
        r.label.toLowerCase().includes(q)
      );
    });
  }, [rows, kindFilter, query]);

  const gpuLabel = backendLabel(primaryBackend);

  return (
    <section className="gpu-matrix-table-section">
      <div className="gpu-matrix-filters">
        <label className="mono">
          Kind{" "}
          <select
            value={kindFilter}
            onChange={(e) => setKindFilter(e.target.value)}
            aria-label="Filter by workload kind"
          >
            <option value="all">All ({rows.length})</option>
            {Object.entries(KIND_LABELS).map(([k, label]) => (
              <option key={k} value={k}>
                {label} ({rows.filter((r) => r.workload_kind === k).length})
              </option>
            ))}
          </select>
        </label>
        <label className="mono gpu-matrix-search">
          Search{" "}
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="workload id…"
            aria-label="Search workloads"
          />
        </label>
        <span className="mono gpu-matrix-count">
          Showing {filtered.length} workload{filtered.length === 1 ? "" : "s"}
        </span>
      </div>

      <div className="gpu-matrix-table-wrap">
        <table className="gpu-matrix-table mono">
          <thead>
            <tr>
              <th scope="col">Workload</th>
              <th scope="col">Kind</th>
              <th scope="col" className="gpu-col-timing">
                Li native CPU
              </th>
              <th scope="col" className="gpu-col-timing">
                {gpuLabel} GPU
              </th>
              <th scope="col" className="gpu-col-timing">
                Vulkan GPU
              </th>
              <th scope="col">CPU valid</th>
              <th scope="col">{gpuLabel} valid</th>
              <th scope="col">{gpuLabel} status</th>
              <th scope="col">Vulkan status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((row) => {
              const { cpu, cuda, vulkan, primary } = compareBackends(row);
              const gpuCell =
                primaryBackend === "metal"
                  ? row.backends.metal ?? primary
                  : primaryBackend === "hip"
                    ? row.backends.hip ?? primary
                    : cuda ?? primary;
              const benchLink = row.workload_id.startsWith("lig.kernel.")
                ? null
                : `/bench/${row.label}/`;
              return (
                <tr key={`${row.workload_kind}:${row.workload_id}`}>
                  <td className="gpu-workload-id">
                    {benchLink ? (
                      <Link href={benchLink}>{row.workload_id}</Link>
                    ) : (
                      row.workload_id
                    )}
                  </td>
                  <td>{KIND_LABELS[row.workload_kind] ?? row.workload_kind}</td>
                  <td>
                    <GpuTimingCell cell={cpu} mode="cpu" />
                  </td>
                  <td>
                    <GpuTimingCell cell={gpuCell} mode="gpu" />
                  </td>
                  <td>
                    <GpuTimingCell cell={vulkan} mode="gpu" />
                  </td>
                  <td>
                    <GpuValidityCell cell={cpu} />
                  </td>
                  <td>
                    <GpuValidityCell cell={gpuCell} />
                  </td>
                  <td>
                    <GpuBackendBadge cell={gpuCell} />
                  </td>
                  <td>
                    <GpuBackendBadge cell={vulkan} />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </section>
  );
}
