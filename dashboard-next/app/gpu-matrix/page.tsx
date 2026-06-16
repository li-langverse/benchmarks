import { GpuMatrixClient } from "@/components/gpu/gpu-matrix-client";
import { loadLigGpuMatrix } from "@/lib/lig-gpu-matrix";

export default function GpuMatrixPage() {
  const matrix = loadLigGpuMatrix();

  return (
    <main data-testid="benchmarks-gpu-matrix-page">
      <section className="placeholder gpu-matrix-page">
        <h2>GPU chip matrix</h2>
        <p style={{ color: "var(--muted)", maxWidth: "52rem" }}>
          Each donated machine is ingested separately — pick a chip to see CPU vs GPU timing and
          validity for CUDA, Metal, Vulkan, and HIP backends. Blocked cells stay honest; no
          fabricated numbers.
        </p>
        <GpuMatrixClient matrix={matrix} />
      </section>
    </main>
  );
}
