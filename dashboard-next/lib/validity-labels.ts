/** Plain-language labels for harness validity_source codes (UX-B02). */

const VALIDITY_SOURCE_PLAIN: Record<string, string> = {
  "latest.csv:passed": "Harness reported passed=true for Li in latest.csv.",
  "latest.csv:verify_within_1ulp": "Li checksum within 1 ULP of the analytical oracle.",
  "latest.csv:verify_ulps": "ULP distance from analytical oracle recorded in latest.csv.",
  "latest.csv:perf_present": "Wall-clock row exists only — no explicit correctness signal yet.",
  "stability.csv": "Tier-0 stability export marked this benchmark passed.",
  "metric:verify_pass": "Dedicated verify_pass metric in CSV.",
  "metric:pass_rate": "Pass-rate metric in CSV.",
  validity_not_required: "Catalog marked validity optional for this row.",
  none: "No correctness signal in this ingest.",
};

export function plainValiditySource(source: string | undefined): string {
  if (!source) return VALIDITY_SOURCE_PLAIN.none;
  return VALIDITY_SOURCE_PLAIN[source] ?? `Source code: ${source}`;
}
