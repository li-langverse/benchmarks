import Link from "next/link";
import { notFound } from "next/navigation";
import { Header } from "@/components/shell/header";
import { StatusBadge } from "@/components/ui/badge";
import { findRow, loadSummary } from "@/lib/summary";

export function generateStaticParams() {
  const summary = loadSummary();
  return summary.rows.map((r) => ({ id: r.benchmark }));
}

export default async function BenchPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const summary = loadSummary();
  const row = findRow(summary, id);
  if (!row) notFound();

  return (
    <>
      <Header subtitle={row.benchmark} />
      <main className="mx-auto max-w-6xl px-6 py-8">
        <dl className="grid gap-3 sm:grid-cols-2">
          <div>
            <dt className="text-sm text-[var(--muted)]">Status</dt>
            <dd>
              <StatusBadge status={row.status}>{row.status}</StatusBadge>
            </dd>
          </div>
          <div>
            <dt className="text-sm text-[var(--muted)]">Tier</dt>
            <dd className="mono">{row.tier}</dd>
          </div>
          <div>
            <dt className="text-sm text-[var(--muted)]">Ratio vs reference</dt>
            <dd className="mono">
              {row.ratio_vs_cpp != null ? `${row.ratio_vs_cpp.toFixed(4)}×` : "—"}
            </dd>
          </div>
          <div>
            <dt className="text-sm text-[var(--muted)]">Threshold</dt>
            <dd className="mono">{row.threshold_ratio_cpp}×</dd>
          </div>
          <div>
            <dt className="text-sm text-[var(--muted)]">Repo / path</dt>
            <dd className="mono text-sm">
              {row.repo} — {row.path}
            </dd>
          </div>
          <div>
            <dt className="text-sm text-[var(--muted)]">PH ids</dt>
            <dd className="mono text-sm">{row.ph_ids.join(", ") || "—"}</dd>
          </div>
        </dl>
        {row.variant && (
          <p className="mt-4 text-sm text-[var(--muted)]">
            Variant: <span className="mono text-[var(--text)]">{row.variant}</span> — see{" "}
            <a href="https://github.com/li-langverse/benchmarks/blob/main/docs/honesty/benchmark-dashboard.md">
              honesty labels
            </a>
            .
          </p>
        )}
        <p className="mt-8">
          <Link href="/">← Overview</Link>
        </p>
      </main>
    </>
  );
}
