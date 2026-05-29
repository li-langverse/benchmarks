import Link from "next/link";
import { GpuChipDiagram } from "@/components/gpu/gpu-chip-diagram";
import { GpuMatrixTable } from "@/components/gpu/gpu-matrix-table";
import { formatTimingSec, loadLigGpuMatrix } from "@/lib/lig-gpu-matrix";

export default function GpuMatrixPage() {
  const matrix = loadLigGpuMatrix();
  const summary = matrix.summary;
  const pilot = matrix.honest_pilot;
  const gpuName =
    (matrix.gpu as { name?: string } | undefined)?.name ?? "NVIDIA GPU";

  return (
    <main>
      <section className="placeholder gpu-matrix-page">
        <h2>GPU backend matrix — CUDA · Li native · Vulkan</h2>
        <p style={{ color: "var(--muted)", maxWidth: "52rem" }}>
          Every catalog workload is enumerated for GPU backends (CUDA, Vulkan/WebGPU,
          HIP, Metal). CPU timing is Li native host reference; GPU timing requires LKIR
          emit and lab hardware. Blocked cells are shown honestly — no fabricated GPU
          numbers.
        </p>

        <p className="mono ingest-meta" style={{ marginTop: "0.75rem" }}>
          Ingest: {matrix.generated_at} · {String(summary.dashboard_workloads)} workloads ·
          CPU timed: {String(summary.timed_cpu_rows)} · CUDA timed:{" "}
          {String(summary.timed_cuda_rows)} · Vulkan timed:{" "}
          {String(summary.timed_vulkan_rows)}
        </p>

        {pilot?.gpu_timing_ns != null ? (
          <aside className="gpu-pilot-strip mono" role="status">
            <strong>CUDA pilot:</strong> {formatTimingSec(Number(pilot.gpu_timing_ns) / 1e9)}{" "}
            device matmul 2×2 ({pilot.status})
            {pilot.note ? ` — ${pilot.note}` : null}
          </aside>
        ) : null}

        <section className="gpu-chip-grid" aria-label="Per-chip timing diagrams">
          <h3 className="bench-panel-heading">Diagrams by chip</h3>
          <div className="gpu-chip-grid-inner">
            {matrix.chips.map((chip) => {
              const diagramKey =
                chip.chip_id === "host_cpu"
                  ? "host_cpu"
                  : chip.chip_id === "nvidia_lab"
                    ? "nvidia_gpu"
                    : chip.chip_id === "amd_lab"
                      ? "amd_gpu"
                      : chip.chip_id === "apple_lab"
                        ? "apple_gpu"
                        : null;
              const diagram = diagramKey ? matrix.diagrams[diagramKey] : null;
              if (!diagram) return null;
              return (
                <GpuChipDiagram
                  key={chip.chip_id}
                  diagram={diagram}
                  chipLabel={chip.label}
                  emptyMessage={
                    chip.visible === false
                      ? `No ${chip.label} on this lab host — awaiting hardware node.`
                      : undefined
                  }
                />
              );
            })}
            <GpuChipDiagram
              diagram={matrix.diagrams.vulkan_gpu}
              chipLabel={`${gpuName} (Vulkan path)`}
              emptyMessage="Vulkan compute timing not measured yet — SPIR-V dispatch stub only."
            />
          </div>
        </section>

        <section style={{ marginTop: "2rem" }}>
          <h3 className="bench-panel-heading">Full workload matrix</h3>
          <p className="mono" style={{ color: "var(--muted)", marginBottom: "1rem" }}>
            Primary columns: CPU vs GPU timing and validity. HIP and Metal columns are in
            the source JSON; expand when AMD/Apple lab nodes land.
          </p>
          <GpuMatrixTable rows={matrix.rows} />
        </section>

        {matrix.funding_gaps && matrix.funding_gaps.length > 0 ? (
          <section className="gpu-funding-gaps" style={{ marginTop: "2rem" }}>
            <h3 className="bench-panel-heading">Blockers &amp; funding gaps</h3>
            <ul className="mono">
              {matrix.funding_gaps.map((g) => (
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
      </section>
    </main>
  );
}
