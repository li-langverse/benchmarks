"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { GpuChipDiagram } from "@/components/gpu/gpu-chip-diagram";
import { GpuChipPicker, GpuCrossChipCompare } from "@/components/gpu/gpu-chip-picker";
import { GpuMatrixTable } from "@/components/gpu/gpu-matrix-table";
import { chipPanelId, chipTabId } from "@/lib/gpu-chip-tab-ids";
import type { LigGpuMatrix } from "@/lib/lig-gpu-matrix-types";
import { formatTimingSec } from "@/lib/lig-gpu-matrix-types";

type GpuMatrixClientProps = {
  matrix: LigGpuMatrix;
};

export function GpuMatrixClient({ matrix }: GpuMatrixClientProps) {
  const [selectedSlug, setSelectedSlug] = useState(matrix.contributions[0]?.chip_slug ?? "");

  const selected = useMemo(
    () => matrix.contributions.find((c) => c.chip_slug === selectedSlug) ?? matrix.contributions[0],
    [matrix.contributions, selectedSlug],
  );

  if (!selected) {
    return (
      <p className="mono" style={{ color: "var(--muted)" }}>
        No GPU chip contributions yet. See{" "}
        <a href={matrix.contribution_policy_url}>how to donate your chip</a>.
      </p>
    );
  }

  const summary = selected.summary;
  const pilot = selected.honest_pilot;
  const hw = selected.hardware ?? {};

  return (
    <>
      <aside className="gpu-donate-banner" role="note">
        <div>
          <strong>Donate a chip</strong> — one command from the benchmarks repo:{" "}
          <code className="mono">./scripts/donate-gpu-chip.sh &lt;chip-slug&gt;</code>
          {" "}(builds lic, runs suite, creates <code>data/gpu-contributions/</code>).
        </div>
        {matrix.contribution_policy_url ? (
          <a href={matrix.contribution_policy_url} target="_blank" rel="noopener noreferrer">
            Contribution rules →
          </a>
        ) : null}
      </aside>

      <p className="mono ingest-meta" style={{ marginTop: "0.75rem" }}>
        Ingest: {matrix.generated_at} · {String(matrix.summary.contribution_count)} chip
        {Number(matrix.summary.contribution_count) === 1 ? "" : "s"} ·{" "}
        {String(matrix.summary.open_slot_count)} open slot
        {Number(matrix.summary.open_slot_count) === 1 ? "" : "s"}
      </p>

      <GpuChipPicker
        contributions={matrix.contributions}
        openSlots={matrix.open_slots}
        selectedSlug={selected.chip_slug}
        onSelect={setSelectedSlug}
        policyUrl={matrix.contribution_policy_url}
      />

      <section
        className="gpu-selected-chip-panel"
        role="tabpanel"
        id={chipPanelId(selected.chip_slug)}
        aria-labelledby={chipTabId(selected.chip_slug)}
        tabIndex={0}
      >
        <h3 id="selected-chip-heading" className="bench-panel-heading">
          {selected.label}
        </h3>
        <dl className="mono gpu-chip-meta-grid">
          <dt>Slug</dt>
          <dd>{selected.chip_slug}</dd>
          <dt>Host OS</dt>
          <dd>{selected.host_os ?? "—"}</dd>
          <dt>Primary backend</dt>
          <dd>{selected.primary_backend}</dd>
          <dt>GPU</dt>
          <dd>{String(hw.gpu_name ?? "—")}</dd>
          <dt>Driver / CC</dt>
          <dd>
            {String(hw.driver_version ?? "—")}
            {hw.compute_capability ? ` · CC ${String(hw.compute_capability)}` : ""}
          </dd>
          <dt>Submitted</dt>
          <dd>{selected.submitted_at ?? "—"}</dd>
          <dt>Workloads</dt>
          <dd>
            CPU timed {String(summary.timed_cpu_rows ?? 0)} · CUDA{" "}
            {String(summary.timed_cuda_rows ?? 0)} · Vulkan{" "}
            {String(summary.timed_vulkan_rows ?? 0)}
          </dd>
        </dl>

        {pilot?.gpu_timing_ns != null ? (
          <aside className="gpu-pilot-strip mono" role="status">
            <strong>Pilot timing:</strong> {formatTimingSec(Number(pilot.gpu_timing_ns) / 1e9)}{" "}
            ({pilot.status}){pilot.note ? ` — ${pilot.note}` : null}
          </aside>
        ) : null}

        <div className="gpu-chip-grid-inner">
          {selected.diagrams.host_cpu ? (
            <GpuChipDiagram
              diagram={selected.diagrams.host_cpu}
              chipLabel={`${selected.label} — host CPU`}
            />
          ) : null}
          {selected.diagrams.primary_gpu ? (
            <GpuChipDiagram
              diagram={selected.diagrams.primary_gpu}
              chipLabel={`${selected.label} — ${selected.primary_backend.toUpperCase()}`}
            />
          ) : null}
          {selected.diagrams.vulkan_gpu ? (
            <GpuChipDiagram
              diagram={selected.diagrams.vulkan_gpu}
              chipLabel={`${selected.label} — Vulkan`}
              emptyMessage="Vulkan compute timing not measured yet."
            />
          ) : null}
        </div>
      </section>

      <GpuCrossChipCompare contributions={matrix.contributions} crossChip={matrix.cross_chip} />

      <section style={{ marginTop: "2rem" }}>
        <h3 className="bench-panel-heading">Workload matrix — {selected.label}</h3>
        <GpuMatrixTable rows={selected.rows} primaryBackend={selected.primary_backend} />
      </section>

      {selected.funding_gaps && selected.funding_gaps.length > 0 ? (
        <section className="gpu-funding-gaps" style={{ marginTop: "2rem" }}>
          <h3 className="bench-panel-heading">Blockers on this host</h3>
          <ul className="mono">
            {selected.funding_gaps.map((g) => (
              <li key={g.id}>
                <strong>{g.title}</strong>: {g.reason}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <p style={{ marginTop: "1.25rem" }}>
        <Link href="/pillar/graphics/">← Graphics pillar</Link>
        {" · "}
        <Link href="/">Overview</Link>
      </p>
    </>
  );
}
