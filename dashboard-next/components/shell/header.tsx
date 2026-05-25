import Link from "next/link";

export function Header({ subtitle }: { subtitle?: string }) {
  return (
    <header className="border-b border-[var(--border)] bg-[var(--surface)] px-6 py-4">
      <div className="mx-auto max-w-6xl">
        <h1 className="m-0 text-xl font-semibold">
          <Link href="/">Li benchmarks</Link>
        </h1>
        {subtitle ? (
          <p className="mt-1 text-sm text-[var(--muted)]">{subtitle}</p>
        ) : (
          <p className="mt-1 text-sm text-[var(--muted)]">
            HPC performance vs catalog thresholds — proof is separate from green rows.
          </p>
        )}
      </div>
    </header>
  );
}
