"use client";

import { useCallback, useRef, type KeyboardEvent } from "react";
import type { GpuChipContribution, GpuOpenSlot } from "@/lib/lig-gpu-matrix-types";
import { backendLabel, formatTimingSec, vendorBadgeClass } from "@/lib/lig-gpu-matrix-types";

export function gpuChipTabId(slug: string): string {
  return `gpu-chip-tab-${slug}`;
}

export function gpuChipPanelId(slug: string): string {
  return `gpu-chip-panel-${slug}`;
}

type GpuChipPickerProps = {
  contributions: GpuChipContribution[];
  openSlots: GpuOpenSlot[];
  selectedSlug: string;
  onSelect: (slug: string) => void;
  policyUrl?: string;
};

export function GpuChipPicker({
  contributions,
  openSlots,
  selectedSlug,
  onSelect,
  policyUrl,
}: GpuChipPickerProps) {
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([]);
  const selectableSlugs = contributions.map((c) => c.chip_slug);
  const selectedIndex = selectableSlugs.indexOf(selectedSlug);

  const focusTab = useCallback(
    (index: number) => {
      const slug = selectableSlugs[index];
      if (slug == null) return;
      tabRefs.current[index]?.focus();
      onSelect(slug);
    },
    [onSelect, selectableSlugs],
  );

  const handleTabListKeyDown = useCallback(
    (event: KeyboardEvent<HTMLDivElement>) => {
      const count = selectableSlugs.length;
      if (count === 0) return;

      const currentIndex = selectedIndex >= 0 ? selectedIndex : 0;
      let nextIndex = currentIndex;

      switch (event.key) {
        case "ArrowRight":
        case "ArrowDown":
          event.preventDefault();
          nextIndex = (currentIndex + 1) % count;
          break;
        case "ArrowLeft":
        case "ArrowUp":
          event.preventDefault();
          nextIndex = (currentIndex - 1 + count) % count;
          break;
        case "Home":
          event.preventDefault();
          nextIndex = 0;
          break;
        case "End":
          event.preventDefault();
          nextIndex = count - 1;
          break;
        default:
          return;
      }

      focusTab(nextIndex);
    },
    [focusTab, selectableSlugs.length, selectedIndex],
  );

  return (
    <section className="gpu-chip-picker" aria-label="Select GPU chip">
      <div className="gpu-chip-picker-header">
        <h3 className="bench-panel-heading">Chips in the matrix</h3>
        {policyUrl ? (
          <a href={policyUrl} target="_blank" rel="noopener noreferrer" className="gpu-donate-link">
            Donate your chip →
          </a>
        ) : null}
      </div>
      <div className="gpu-chip-cards">
        <div
          className="gpu-chip-tablist"
          role="tablist"
          aria-label="Contributed GPUs"
          onKeyDown={handleTabListKeyDown}
        >
          {contributions.map((c, index) => {
            const active = c.chip_slug === selectedSlug;
            const s = c.summary;
            return (
              <button
                key={c.chip_slug}
                ref={(el) => {
                  tabRefs.current[index] = el;
                }}
                id={gpuChipTabId(c.chip_slug)}
                type="button"
                role="tab"
                aria-selected={active}
                aria-controls={gpuChipPanelId(c.chip_slug)}
                tabIndex={active ? 0 : -1}
                className={`gpu-chip-card ${vendorBadgeClass(c.vendor)} ${active ? "gpu-chip-card-active" : ""}`}
                onClick={() => onSelect(c.chip_slug)}
              >
                <span className="gpu-chip-card-vendor">{c.vendor ?? "gpu"}</span>
                <strong className="gpu-chip-card-title">{c.label}</strong>
                <span className="mono gpu-chip-card-meta">
                  {c.host_os} · {backendLabel(c.primary_backend)}
                </span>
                <span className="mono gpu-chip-card-stats">
                  CPU {String(s.timed_cpu_rows ?? 0)} · GPU {String(
                    (s.timed_cuda_rows as number) ||
                      (s.timed_metal_rows as number) ||
                      (s.timed_hip_rows as number) ||
                      0,
                  )}{" "}
                  timed
                </span>
              </button>
            );
          })}
        </div>
        {openSlots.map((slot) => (
          <div
            key={slot.chip_slug}
            className={`gpu-chip-card gpu-chip-card-open ${vendorBadgeClass(slot.vendor)}`}
            aria-disabled="true"
          >
            <span className="gpu-chip-card-vendor">{slot.vendor}</span>
            <strong className="gpu-chip-card-title">{slot.label}</strong>
            <span className="mono gpu-chip-card-meta">
              {slot.host_os} · {backendLabel(slot.primary_backend)}
            </span>
            <span className="gpu-chip-card-open-badge">Open slot</span>
            {policyUrl ? (
              <a href={policyUrl} target="_blank" rel="noopener noreferrer" className="gpu-chip-card-donate">
                How to contribute
              </a>
            ) : null}
          </div>
        ))}
      </div>
    </section>
  );
}

type GpuCrossChipCompareProps = {
  contributions: GpuChipContribution[];
  crossChip: import("@/lib/lig-gpu-matrix-types").CrossChipRow[];
};

export function GpuCrossChipCompare({ contributions, crossChip }: GpuCrossChipCompareProps) {
  if (contributions.length < 2) {
    return (
      <section className="gpu-cross-chip gpu-cross-chip-empty">
        <h3 className="bench-panel-heading">Cross-chip compare</h3>
        <p className="mono" style={{ color: "var(--muted)" }}>
          Add a second chip contribution to see side-by-side GPU timing here. We need M1, RTX
          3090, and more lab nodes — see the donation guide.
        </p>
      </section>
    );
  }

  if (crossChip.length === 0) {
    return (
      <section className="gpu-cross-chip gpu-cross-chip-empty">
        <h3 className="bench-panel-heading">Cross-chip compare</h3>
        <p className="mono" style={{ color: "var(--muted)" }}>
          Multiple chips ingested, but no workloads with timing on more than one chip yet.
        </p>
      </section>
    );
  }

  const slugs = contributions.map((c) => c.chip_slug);

  return (
    <section className="gpu-cross-chip">
      <h3 className="bench-panel-heading">Cross-chip compare</h3>
      <p className="mono gpu-cross-chip-hint">
        Workloads measured on 2+ donated machines — primary backend GPU time per chip.
      </p>
      <div className="gpu-matrix-table-wrap">
        <table className="gpu-matrix-table mono">
          <thead>
            <tr>
              <th>Workload</th>
              {contributions.map((c) => (
                <th key={c.chip_slug}>{c.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {crossChip.map((row) => (
              <tr key={row.workload_id}>
                <td>{row.workload_id}</td>
                {slugs.map((slug) => {
                  const cell = row.chips[slug];
                  return (
                    <td key={slug}>
                      {cell?.gpu_sec != null ? (
                        formatTimingSec(cell.gpu_sec)
                      ) : cell?.cpu_sec != null ? (
                        <span title="CPU only">{formatTimingSec(cell.cpu_sec)} CPU</span>
                      ) : (
                        "—"
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
