#!/usr/bin/env bash
# Commit dirty git roots under workspace paths with a simple one-line message.
# Usage:
#   commit-all-repos.sh [--message "one liner"] [--dry-run] [workspace_root ...]
# If --message is omitted, each repo gets an auto one-liner from its changes.

set -euo pipefail

message=""
dry_run=0
roots=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --message|-m)
      message="$2"
      shift 2
      ;;
    --dry-run)
      dry_run=1
      shift
      ;;
    *)
      roots+=("$1")
      shift
      ;;
  esac
done

if [[ ${#roots[@]} -eq 0 ]]; then
  roots+=("$(pwd)")
fi

git_roots=()
for base in "${roots[@]}"; do
  if [[ -d "$base/.git" ]]; then
    git_roots+=("$(cd "$base" && pwd)")
  fi
  while IFS= read -r d; do
    [[ -z "$d" ]] && continue
    git_roots+=("$(cd "$(dirname "$d")" && pwd)")
  done < <(find "$base" -maxdepth 4 -type d -name .git 2>/dev/null || true)
done

unique=()
for r in "${git_roots[@]}"; do
  dup=0
  for u in "${unique[@]+"${unique[@]}"}"; do
    if [[ "$u" == "$r" ]]; then
      dup=1
      break
    fi
  done
  if [[ $dup -eq 0 ]]; then
    unique+=("$r")
  fi
done
git_roots=("${unique[@]+"${unique[@]}"}")

if [[ ${#git_roots[@]} -eq 0 ]]; then
  echo "No git roots found under: ${roots[*]}" >&2
  exit 1
fi

auto_message() {
  local root="$1"
  local names
  names="$(git -C "$root" status --porcelain 2>/dev/null | awk '{print $2}' | sed 's|^||' | head -20)"
  if echo "$names" | grep -q '^taskmark/' && ! echo "$names" | grep -qv '^taskmark/'; then
    echo "update taskmark board"
    return
  fi
  local first
  first="$(echo "$names" | head -1 | sed 's|/$||')"
  if [[ -z "$first" ]]; then
    echo "update project"
    return
  fi
  # simplify path to a short phrase
  first="$(echo "$first" | awk -F/ '{if (NF>=2) print $1"/"$2; else print $1}')"
  echo "update ${first}"
}

committed=0
skipped=0
failed=0

for r in "${git_roots[@]}"; do
  name="$(basename "$r")"
  if [[ -z "$(git -C "$r" status --porcelain 2>/dev/null)" ]]; then
    echo "SKIP  $name (clean)"
    skipped=$((skipped + 1))
    continue
  fi

  msg="$message"
  if [[ -z "$msg" ]]; then
    msg="$(auto_message "$r")"
  fi
  # force single line
  msg="$(echo "$msg" | head -1 | tr '\n' ' ' | sed 's/[[:space:]]*$//')"

  if [[ $dry_run -eq 1 ]]; then
    echo "DRY   $name -> $msg"
    continue
  fi

  if ! (
    cd "$r"
    git add -A
    git commit -m "$msg"
  ); then
    echo "FAIL  $name" >&2
    failed=$((failed + 1))
    continue
  fi

  sha="$(git -C "$r" rev-parse --short HEAD)"
  echo "OK    $name $sha $msg"
  committed=$((committed + 1))
done

echo "Done. committed=$committed skipped=$skipped failed=$failed"
if [[ $failed -gt 0 ]]; then
  exit 1
fi
