import Link from "next/link";
import { Header } from "@/components/shell/header";
import { StatusBadge } from "@/components/ui/badge";
import { loadSummary } from "@/lib/summary";
import { PILLARS } from "@/lib/pillars";

export default function HomePage() {
  const summary = loadSummary();
  const redRows = summary.rows.filter((r) => r.status === "red");

  return (
    <>
      <Header subtitle={`Generated ${summary.generated_at}`} />
      <main className="mx-auto max-w-6xl px-6 py-8">
        {redRows.length > 0 && (
          <section className="mb-8 rounded-lg border border-[var(--red)] bg-[var(--surface)] p-4">
            <h2 className="mt-0 text-lg text-[var(--red)]">Regressions ({redRows.length})</h2>
            <ul className="m-0 list-inside list-disc text-sm">
              {redRows.slice(0, 8).map((r) => (
                <li key={r.benchmark}>
                  <Link href={`/bench/${r.benchmark}/`}>{r.benchmark}</Link>
                  {r.ratio_vs_cpp != null ? ` — ${r.ratio_vs_cpp.toFixed(3)}×` : ""}
                </li>
              ))}
            </ul>
          </section>
        )}

        <section className="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {PILLARS.map((p) => {
            const rows = summary.rows.filter(
              (r) => r.category && p.id !== "proofs" && r.category === (p.id === "numerics" ? "micro" : p.id),
            );
            const counts = { green: 0, yellow: 0, red: 0, unknown: 0 };
            for (const r of rows) {
              const s = r.status as keyof typeof counts;
              if (s in counts) counts[s]++;
            }
            return (
              <Link
                key={p.id}
                href={`/pillar/${p.id}/`}
                className="block rounded-lg border border-[var(--border)] bg-[var(--surface)] p-4 transition hover:border-[var(--accent)]"
              >
                <h3 className="m-0 text-base font-semibold">{p.label}</h3>
                <p className="mt-1 text-sm text-[var(--muted)]">{p.description}</p>
                <div className="mt-3 flex flex-wrap gap-2 text-xs">
                  <StatusBadge status="green">{counts.green} ok</StatusBadge>
                  <StatusBadge status="yellow">{counts.yellow} warn</StatusBadge>
                  <StatusBadge status="red">{counts.red} fail</StatusBadge>
                  <StatusBadge status="unknown">{counts.unknown} ?</StatusBadge>
                </div>
              </Link>
            );
          })}
        </section>

        <section>
          <h2 className="text-lg">All benchmarks</h2>
          <div className="overflow-x-auto rounded-lg border border-[var(--border)]">
            <table className="w-full border-collapse text-sm">
              <thead className="bg-[var(--surface)] text-left text-[var(--muted)]">
                <tr>
                  <th className="p-2">Benchmark</th>
                  <th className="p-2">Tier</th>
                  <th className="p-2">Ratio</th>
                  <th className="p-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {summary.rows.map((r) => (
                  <tr key={r.benchmark} className="border-t border-[var(--border)]">
                    <td className="p-2">
                      <Link href={`/bench/${r.benchmark}/`}>{r.benchmark}</Link>
                    </td>
                    <td className="mono p-2">{r.tier}</td>
                    <td className="mono p-2">
                      {r.ratio_vs_cpp != null ? `${r.ratio_vs_cpp.toFixed(3)}×` : "—"}
                    </td>
                    <td className="p-2">
                      <StatusBadge status={r.status}>{r.status}</StatusBadge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </>
  );
}
