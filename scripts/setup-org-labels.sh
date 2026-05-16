#!/usr/bin/env bash
# Create planning labels on li-langverse repos (idempotent).
set -euo pipefail

ORG=li-langverse
REPOS=(benchmarks lic lip lit lis roadmap)

create_label() {
  local repo="$1" name="$2" color="$3" description="$4"
  # gh --force updates label metadata only (not git force push)
  gh label create "$name" --repo "$ORG/$repo" --color "$color" --description "$description" --force 2>/dev/null \
    || gh label edit "$name" --repo "$ORG/$repo" --color "$color" --description "$description" 2>/dev/null \
    || true
}

for repo in "${REPOS[@]}"; do
  echo "==> $repo"
  create_label "$repo" "plan-needed" "FBCA04" "Feature accepted; automation will draft vision-aligned plan"
  create_label "$repo" "plan-approved" "0E8A16" "Plan linked; implementation may proceed"
  create_label "$repo" "feature" "A2EEEF" "New capability (use feature request template)"
  create_label "$repo" "merge-approved" "5319E7" "Standards review passed; auto-merge workflow may merge"
  create_label "$repo" "do-not-merge" "B60205" "Block automated and routine merges"
  create_label "$repo" "ecosystem-gap" "F9D0C4" "Missing/broken shared tooling — planner extends catalog"
done

echo "Done."
