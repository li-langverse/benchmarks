type HonestyCalloutProps = {
  variant: string | null | undefined;
};

const CALLOUTS: Record<string, { title: string; body: string }> = {
  pure_li: {
    title: "pure_li — Li-only codegen",
    body:
      "This row measures the pure-Li compilation path (PH-7e). A red status is compiler performance debt, not a missing proof closure. Green does not mean Lean verification for this kernel.",
  },
  shared_c_kernel: {
    title: "shared_c_kernel — shared numerics kernel",
    body:
      "Li and C++ may share a C numerics kernel. Throughput here is not evidence of pure-Li SIMD/codegen competitiveness — cite PH-7e only on pure_li rows.",
  },
};

export function HonestyCallout({ variant }: HonestyCalloutProps) {
  if (!variant) return null;
  const callout = CALLOUTS[variant];
  if (!callout) return null;

  return (
    <aside className="honesty-callout" role="note">
      <strong>{callout.title}</strong>
      <p>{callout.body}</p>
    </aside>
  );
}
