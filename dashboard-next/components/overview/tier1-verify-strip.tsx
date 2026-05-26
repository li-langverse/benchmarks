import Link from "next/link";
import type { Tier1VerifyStats } from "@/lib/tier1-verify";

type Tier1VerifyStripProps = {
  stats: Tier1VerifyStats;
};

export function Tier1VerifyStrip({ stats }: Tier1VerifyStripProps) {
  if (stats.total === 0) return null;

  return (
    <section
      className="tier1-verify-strip bento-full"
      aria-labelledby="tier1-verify-heading"
    >
      <h2 id="tier1-verify-heading">Tier-1 correctness</h2>
      <p>
        Measured tier-1 rows: <strong>{stats.total}</strong> — validity{" "}
        <strong>{stats.pass}</strong> pass, <strong>{stats.fail}</strong> fail,{" "}
        <strong>{stats.unknown}</strong> unknown. Analytical ULP:{" "}
        <strong>{stats.within1ulp}</strong> within 1 ULP,{" "}
        <strong>{stats.over1ulp}</strong> over 1 ULP
        {stats.noNumeric > 0 ? (
          <>
            , <strong>{stats.noNumeric}</strong> without numeric oracle rows in CSV
          </>
        ) : null}
        .
      </p>
      <p className="tier1-verify-links">
        <Link href="/matrix/?tier=1">Tier-1 matrix</Link>
        {" · "}
        <Link href="/matrix/?tier=1&validity=fail">Validity fail</Link>
        {" · "}
        <Link href="/matrix/?tier=1&within_1ulp=0">ULP &gt; 1</Link>
        {" · "}
        <Link href="/matrix/?tier=1&oracle=analytical">Analytical oracle</Link>
      </p>
    </section>
  );
}
