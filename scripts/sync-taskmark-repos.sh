#!/usr/bin/env bash
# Sync taskmark/ from a canonical git root into other git roots.
# Usage:
#   sync-taskmark-repos.sh [--canonical /path/to/repo] [workspace_root ...]
# If no workspace roots are given, uses the current directory.

set -euo pipefail

canonical=""
roots=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --canonical)
      canonical="$2"
      shift 2
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

# Dedupe without associative arrays (macOS Bash 3.2)
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

if [[ -z "$canonical" ]]; then
  for r in "${git_roots[@]}"; do
    if [[ -f "$r/taskmark/INDEX.md" ]]; then
      canonical="$r"
      break
    fi
  done
fi
if [[ -z "$canonical" ]]; then
  canonical="${git_roots[0]}"
fi

if [[ ! -d "$canonical/taskmark" ]]; then
  echo "Canonical $canonical has no taskmark/ — run taskmark-init first." >&2
  exit 1
fi

now="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
repos_md="$canonical/taskmark/REPOS.md"
{
  echo "# Linked repositories"
  echo
  echo "Canonical: $(basename "$canonical")"
  echo
  echo "| Name | Path | Git | Last synced (UTC) |"
  echo "|------|------|-----|-------------------|"
  for r in "${git_roots[@]}"; do
    echo "| $(basename "$r") | $r | yes | $now |"
  done
} > "$repos_md"

for r in "${git_roots[@]}"; do
  if [[ "$r" == "$canonical" ]]; then
    continue
  fi
  mkdir -p "$r"
  rm -rf "$r/taskmark"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a "$canonical/taskmark/" "$r/taskmark/"
  else
    cp -R "$canonical/taskmark" "$r/taskmark"
  fi
  echo "Synced taskmark/ -> $r"
done

echo "Canonical: $canonical"
echo "Linked ${#git_roots[@]} git root(s)."
