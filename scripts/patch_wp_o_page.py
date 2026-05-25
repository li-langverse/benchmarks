#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parents[1] / "dashboard-next/app/page.tsx"
text = p.read_text()
old_import = """import {
  countStatusesByPillar,
  countValidityUnknownByPillar,
  packageFreshnessRows,
  regressionRows,
  topBenchmarksByStatus,
} from "@/lib/overview";
import {
  hasIndexedReleases,
  loadReleaseIndex,
} from "@/lib/release-index";
import { releaseFreshnessBanner } from "@/lib/release-freshness";
import { COVERAGE_GAP_DOC, coverageHonesty, splitTierCounts } from "@/lib/coverage";"""
new_import = """import { COVERAGE_GAP_DOC, coverageHonesty } from "@/lib/coverage";
import {
  countPillarOverview,
  countValidityUnknownByPillar,
  packageFreshnessRows,
  regressionRows,
  splitTierCounts,
  topBenchmarksByStatus,
  topPendingBenchmarks,
} from "@/lib/overview";
import {
  hasIndexedReleases,
  loadReleaseIndex,
} from "@/lib/release-index";
import { releaseFreshnessBanner } from "@/lib/release-freshness";"""
if old_import not in text:
    raise SystemExit("import block missing")
text = text.replace(old_import, new_import)
text = text.replace(
    "  const pillarCounts = countStatusesByPillar(summary.rows);",
    "  const pillarOverview = countPillarOverview(summary.rows);",
)
text = text.replace(
    "          <strong>{honesty.pending}</strong> are catalog placeholders until harness runs\n          produce CSV.",
    "          <strong>{honesty.pending}</strong> are pending (catalog placeholders or harness without\n          wall-clock CSV in this ingest).",
)
text = text.replace("catalog pending", "pending")
text = text.replace(
    "{m.unknown > 0 ? <span className=\"u\">{m.unknown} ?</span> : null}",
    """{m.unknown > 0 ? (
                  <span className="u" title="Wall-clock present; validity or status unresolved">
                    {m.unknown} validity ?
                  </span>
                ) : null}""",
)
text = text.replace(
    """            const counts = pillarCounts[pillarId] ?? {
              green: 0,
              yellow: 0,
              red: 0,
              unknown: 0,
            };""",
    """            const overview = pillarOverview[pillarId] ?? {
              measured: { green: 0, yellow: 0, red: 0, unknown: 0 },
              pending: 0,
            };
            const counts = overview.measured;""",
)
text = text.replace(
    "counts.green + counts.yellow + counts.red + counts.unknown;",
    "counts.green + counts.yellow + counts.red + counts.unknown + overview.pending;",
)
text = text.replace(
    """            const unknownIds = topBenchmarksByStatus(
              summary.rows,
              pillarId,
              "unknown",
            );""",
    "            const pendingIds = topPendingBenchmarks(summary.rows, pillarId);",
)
text = text.replace(
    """                <div className="counts pillar-counts">
                  <span className="g">{counts.green} ok</span>
                  <span className="y">{counts.yellow} warn</span>
                  <span className="r">{counts.red} fail</span>
                  <span className="u">{counts.unknown} ?</span>
                </div>""",
    """                <div className="counts pillar-counts">
                  <span className="g">{counts.green} ok</span>
                  <span className="y">{counts.yellow} warn</span>
                  <span className="r">{counts.red} fail</span>
                  {counts.unknown > 0 ? (
                    <span className="u">{counts.unknown} validity ?</span>
                  ) : null}
                  {overview.pending > 0 ? (
                    <span className="p">{overview.pending} pending</span>
                  ) : null}
                </div>""",
)
text = text.replace("unknownIds", "pendingIds")
text = text.replace('key={`u-${id}`}', 'key={`p-${id}`}')
text = text.replace(
    '<Badge status="unknown" />',
    '<span className="badge badge-unknown badge-pending">pending</span>',
)
p.write_text(text)
print("page.tsx ok")
