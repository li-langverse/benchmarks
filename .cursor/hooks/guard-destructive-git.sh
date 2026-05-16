#!/usr/bin/env bash
# Cursor beforeShellExecution — block force push and other destructive git unless LI_HOOK_ALLOW=1.
set -euo pipefail
input="$(cat)"
cmd="$(echo "$input" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('command',''))" 2>/dev/null || true)"
[[ -n "$cmd" ]] || exit 0
if [[ "${LI_HOOK_ALLOW:-}" == "1" ]]; then
  exit 0
fi

cmd_lower="$(printf '%s' "$cmd" | tr '[:upper:]' '[:lower:]')"

# Force push (any common form)
if [[ "$cmd_lower" == *"git push"*"--force"* ]] \
  || [[ "$cmd_lower" == *"git push"*" -f "* ]] \
  || [[ "$cmd_lower" == *"git push -f"* ]] \
  || [[ "$cmd_lower" == *"git push"*" -f" ]] \
  || [[ "$cmd_lower" == *"+push"*"--force"* ]]; then
  cat >&2 <<'EOF'
blocked: force push — use a normal push to your feature branch instead.

  git fetch origin
  git rebase origin/main   # or your PR base branch
  git push origin HEAD

If history rewrite is truly required, get human approval and use
  LI_HOOK_ALLOW=1 git push --force-with-lease origin <your-branch>
See docs/ecosystem/git-workflow.md
EOF
  exit 2
fi

case "$cmd" in
  *"git reset --hard"*|*"git commit"*"--no-verify"*)
    echo "blocked: destructive git (set LI_HOOK_ALLOW=1 if intentional)" >&2
    exit 2
    ;;
esac
exit 0
