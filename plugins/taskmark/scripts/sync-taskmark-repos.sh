#!/usr/bin/env bash
# Discover the canonical board and generate its local, gitignored REPOS.md.

set -euo pipefail

common_name=""
roots=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      common_name="$2"
      shift 2
      ;;
    *)
      roots+=("$1")
      shift
      ;;
  esac
done
[[ ${#roots[@]} -gt 0 ]] || roots+=("$(pwd)")

git_roots=()
for base in "${roots[@]}"; do
  if root="$(git -C "$base" rev-parse --show-toplevel 2>/dev/null)"; then
    git_roots+=("$root")
  fi
  while IFS= read -r dotgit; do
    [[ -n "$dotgit" ]] && git_roots+=("${dotgit%/.git}")
  done < <(find "$base" -maxdepth 4 -type d -name .git 2>/dev/null || true)
done

unique=()
for root in "${git_roots[@]}"; do
  duplicate=0
  for seen in "${unique[@]+"${unique[@]}"}"; do
    [[ "$seen" == "$root" ]] && duplicate=1 && break
  done
  [[ $duplicate -eq 1 ]] || unique+=("$root")
done
git_roots=("${unique[@]+"${unique[@]}"}")
[[ ${#git_roots[@]} -gt 0 ]] || { echo "No git roots found." >&2; exit 1; }

boards=()
products=()
for root in "${git_roots[@]}"; do
  if [[ "$(basename "$root")" == *-taskmark && -d "$root/epics" ]]; then
    boards+=("$root")
  else
    products+=("$root")
    [[ -d "$root/taskmark/epics" ]] && boards+=("$root/taskmark")
  fi
done

board=""
mode=""
if [[ ${#boards[@]} -eq 1 ]]; then
  board="${boards[0]}"
  [[ "$(basename "$board")" == "taskmark" ]] && mode="single-project" || mode="multi-project"
elif [[ ${#products[@]} -eq 1 ]]; then
  board="${products[0]}/taskmark"
  mode="single-project"
elif [[ ${#products[@]} -gt 1 ]]; then
  parent="$(dirname "${products[0]}")"
  if [[ -z "$common_name" ]]; then
    same_parent=1
    for root in "${products[@]}"; do
      [[ "$(dirname "$root")" == "$parent" ]] || same_parent=0
    done
    [[ $same_parent -eq 1 ]] && common_name="$(basename "$parent")"
  fi
  if [[ -z "$common_name" ]]; then
    echo "Ambiguous common project name; rerun with --name <common>." >&2
    exit 2
  fi
  board="$parent/${common_name}-taskmark"
  mode="multi-project"
else
  echo "Could not determine canonical Taskmark board." >&2
  exit 1
fi

mkdir -p "$board/epics"
if [[ "$mode" == "multi-project" && ! -d "$board/.git" ]]; then
  git -C "$board" init >/dev/null
fi

gitignore="$board/.gitignore"
touch "$gitignore"
if ! grep -qxF "REPOS.md" "$gitignore"; then
  [[ ! -s "$gitignore" || "$(tail -c 1 "$gitignore" 2>/dev/null)" == "" ]] || echo >> "$gitignore"
  echo "REPOS.md" >> "$gitignore"
fi

{
  echo "# Linked repositories"
  echo
  echo "Canonical: $(basename "$board")"
  echo
  echo "| Name | Path | Git |"
  echo "|------|------|-----|"
  echo "| $(basename "$board") | $board | yes |"
  for root in "${products[@]}"; do
    [[ "$root" == "$board" ]] && continue
    echo "| $(basename "$root") | $root | yes |"
  done
} > "$board/REPOS.md"

echo "Mode: $mode"
echo "Canonical: $board"
echo "REPOS.md: local-generated and gitignored"
