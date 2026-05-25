import type { ReleaseIndex } from "@/lib/release-index";

export type ReleaseFreshnessBanner = {
  level: "ok" | "warn" | "stale" | "missing";
  message: string;
};

/** Compare release-index ingest stamp to summary ingest (WP5 banner). */
export function releaseFreshnessBanner(
  index: ReleaseIndex,
  summaryGeneratedAt: string,
): ReleaseFreshnessBanner | null {
  if (!index.updated_at) {
    return {
      level: "missing",
      message:
        "No release manifests indexed yet — package freshness uses catalog rows only until package-release dispatch lands.",
    };
  }
  const summaryMs = Date.parse(summaryGeneratedAt);
  const indexMs = Date.parse(index.updated_at);
  if (!Number.isFinite(summaryMs) || !Number.isFinite(indexMs)) {
    return null;
  }
  const ageHours = (summaryMs - indexMs) / (1000 * 60 * 60);
  if (ageHours > 72) {
    return {
      level: "stale",
      message: `Release index is ${Math.floor(ageHours / 24)}d older than this summary ingest — re-run ingest-release-manifests or wait for package-release.`,
    };
  }
  if (ageHours > 24) {
    return {
      level: "warn",
      message: `Release index updated ${Math.floor(ageHours)}h before summary — check package-release workflows if expecting fresher pins.`,
    };
  }
  return {
    level: "ok",
    message: "Release index and summary ingest are aligned.",
  };
}
