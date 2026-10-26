#!/usr/bin/env bash
# Install the "notify-profile" workflow and its secret in all your repositories.
#
#   ./scripts/install_notify.sh            # dry run: only lists what it would do
#   ./scripts/install_notify.sh --apply    # actually does it
#
# Requirements:
#   - GitHub CLI logged in with the workflow scope:  gh auth refresh -s workflow
#   - PROFILE_DISPATCH_TOKEN exported in your shell (see SETUP.md)
# Works on macOS (bash 3.2) and Linux.
set -euo pipefail

USER_NAME="andrei-borcea"
PROFILE_REPO="andrei-borcea"
WORKFLOW_PATH=".github/workflows/notify-profile.yml"
SNIPPET="$(cd "$(dirname "$0")/.." && pwd)/snippets/notify-profile.yml"
APPLY=false
[ "${1:-}" = "--apply" ] && APPLY=true

if $APPLY && [ -z "${PROFILE_DISPATCH_TOKEN:-}" ]; then
  echo "PROFILE_DISPATCH_TOKEN is not set (see SETUP.md)" >&2
  exit 1
fi

CONTENT_B64="$(base64 < "$SNIPPET" | tr -d '\n')"

# Own repos only: no forks, no archived, not the profile repo itself
gh repo list "$USER_NAME" --source --no-archived --limit 200 --json name --jq '.[].name' |
while read -r repo; do
  [ "$repo" = "$PROFILE_REPO" ] && continue

  if ! $APPLY; then
    echo "[dry-run] would install $WORKFLOW_PATH + secret in $USER_NAME/$repo"
    continue
  fi

  # sha is needed to overwrite an existing file
  sha="$(gh api "repos/$USER_NAME/$repo/contents/$WORKFLOW_PATH" --jq .sha 2>/dev/null || true)"
  args=(-X PUT "repos/$USER_NAME/$repo/contents/$WORKFLOW_PATH"
        -f message="ci: notify profile README on push"
        -f content="$CONTENT_B64")
  [ -n "$sha" ] && args+=(-f sha="$sha")

  if gh api "${args[@]}" --silent && \
     printf '%s' "$PROFILE_DISPATCH_TOKEN" | gh secret set PROFILE_DISPATCH_TOKEN --repo "$USER_NAME/$repo"; then
    echo "ok     $repo"
  else
    echo "FAILED $repo (empty repo or missing permissions?)" >&2
  fi
done
