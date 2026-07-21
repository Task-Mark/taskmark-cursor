#!/usr/bin/env bash
# Ensure Taskmark board location matches workspace mode and refresh REPOS.md.
#
# Single git product root: board is <project>/taskmark/ (uses project git).
# Multiple product roots: sibling <common>-taskmark git repo IS the board root
# (INDEX.md, epics/, … at repo root — no nested taskmark/ folder).
# Never copy the board into product repos.
#
# Usage:
#   sync-taskmark-repos.sh [--name COMMON] [--migrate] [--canonical /path]
#                          [workspace_root ...]
#
# Exit 2 if multi mode and common name is ambiguous (pass --name).

set -euo pipefail

canonical=""
common_name=""
migrate=0
roots=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --canonical)
      canonical="$2"
      shift 2
      ;;
    --name)
      common_name="$2"
      shift 2
      ;;
    --migrate)
      migrate=1
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

is_board_repo() {
  local base
  base="$(basename "$1")"
  [[ "$base" == *-taskmark ]]
}

# Board content directory for a git root:
#   dedicated *-taskmark repo → repo root (flat)
#   product repo → <root>/taskmark
board_dir() {
  if is_board_repo "$1"; then
    echo "$1"
  else
    echo "$1/taskmark"
  fi
}

has_board() {
  [[ -f "$(board_dir "$1")/INDEX.md" ]]
}

# --- discover git roots ---
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

product_roots=()
board_roots=()
for r in "${git_roots[@]}"; do
  if is_board_repo "$r"; then
    board_roots+=("$r")
  else
    product_roots+=("$r")
  fi
done

if [[ ${#product_roots[@]} -eq 0 ]]; then
  # Only board repo(s) present — treat first as single board host
  product_roots=("${board_roots[@]}")
  board_roots=()
fi

epic_count() {
  local dir
  dir="$(board_dir "$1")/epics"
  # Also count nested legacy layout on board repos
  if [[ ! -d "$dir" && -d "$1/taskmark/epics" ]]; then
    dir="$1/taskmark/epics"
  fi
  if [[ -d "$dir" ]]; then
    find "$dir" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' '
  else
    echo 0
  fi
}

# Resolve directory that currently holds INDEX.md for a root (flat or nested)
board_content_dir() {
  local r="$1"
  if [[ -f "$r/INDEX.md" ]]; then
    echo "$r"
  elif [[ -f "$r/taskmark/INDEX.md" ]]; then
    echo "$r/taskmark"
  else
    echo ""
  fi
}

pick_richest_board_source() {
  local best="" best_n=-1 n content
  for r in "${product_roots[@]}" "${board_roots[@]+"${board_roots[@]}"}"; do
    content="$(board_content_dir "$r")"
    [[ -n "$content" ]] || continue
    n="$(epic_count "$r")"
    if [[ "$n" -gt "$best_n" ]]; then
      best_n="$n"
      best="$r"
    fi
  done
  echo "$best"
}

shared_parent() {
  local first="$1" parent p
  parent="$(dirname "$first")"
  shift
  for p in "$@"; do
    if [[ "$(dirname "$p")" != "$parent" ]]; then
      echo ""
      return 0
    fi
  done
  echo "$parent"
}

derive_prefix_name() {
  local names=() n first i c ok prefix=""
  for n in "$@"; do
    names+=("$(basename "$n")")
  done
  first="${names[0]}"
  for ((i = 0; i < ${#first}; i++)); do
    c="${first:i:1}"
    ok=1
    for n in "${names[@]}"; do
      if [[ "${n:i:1}" != "$c" ]]; then
        ok=0
        break
      fi
    done
    if [[ $ok -eq 1 ]]; then
      prefix+="$c"
    else
      break
    fi
  done
  prefix="${prefix%[-_]}"
  if [[ -z "$prefix" || "$prefix" =~ ^[-_]+$ ]]; then
    echo ""
    return 0
  fi
  for n in "${names[@]}"; do
    if [[ "$n" == "$prefix" ]]; then
      echo ""
      return 0
    fi
  done
  echo "$prefix"
}

repos_md_path() {
  local r="$1"
  if is_board_repo "$r"; then
    echo "$r/REPOS.md"
  else
    echo "$r/taskmark/REPOS.md"
  fi
}

derive_common_name() {
  if [[ -n "$common_name" ]]; then
    echo "$common_name"
    return 0
  fi
  local src cand repos
  src="$(pick_richest_board_source)"
  if [[ -n "$src" ]]; then
    repos="$(repos_md_path "$src")"
    # legacy nested on board repo
    if [[ ! -f "$repos" && -f "$src/taskmark/REPOS.md" ]]; then
      repos="$src/taskmark/REPOS.md"
    fi
    if [[ -f "$repos" ]]; then
      cand="$(grep -E '^Canonical:' "$repos" | head -1 | sed 's/^Canonical:[[:space:]]*//')"
      if [[ "$cand" == *-taskmark ]]; then
        echo "${cand%-taskmark}"
        return 0
      fi
    fi
  fi
  local parent
  parent="$(shared_parent "${product_roots[@]}")"
  if [[ -n "$parent" ]]; then
    basename "$parent"
    return 0
  fi
  local prefix
  prefix="$(derive_prefix_name "${product_roots[@]}")"
  if [[ -n "$prefix" ]]; then
    echo "$prefix"
    return 0
  fi
  echo ""
}

write_repos_md() {
  local board_git="$1"
  shift
  local list=("$@")
  local now repos_md r
  now="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  if is_board_repo "$board_git"; then
    repos_md="$board_git/REPOS.md"
  else
    mkdir -p "$board_git/taskmark"
    repos_md="$board_git/taskmark/REPOS.md"
  fi
  {
    echo "# Linked repositories"
    echo
    echo "Canonical: $(basename "$board_git")"
    echo
    echo "| Name | Path | Git | Last synced (UTC) |"
    echo "|------|------|-----|-------------------|"
    echo "| $(basename "$board_git") | $board_git | yes | $now |"
    for r in "${list[@]}"; do
      if [[ "$r" == "$board_git" ]]; then
        continue
      fi
      echo "| $(basename "$r") | $r | yes | $now |"
    done
  } > "$repos_md"
}

# Copy board *content* into a dedicated *-taskmark repo root (flat).
copy_board_flat() {
  local from_root="$1" to_root="$2"
  local from_content
  from_content="$(board_content_dir "$from_root")"
  if [[ -z "$from_content" ]]; then
    echo "No board content to copy from $from_root" >&2
    return 1
  fi
  mkdir -p "$to_root"
  # Clear prior board files at dest root (keep .git)
  if [[ -d "$to_root/taskmark" ]]; then
    rm -rf "$to_root/taskmark"
  fi
  # If source is nested under dest already, just flatten in place below
  if [[ "$from_content" == "$to_root/taskmark" ]]; then
    return 0
  fi
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude '.git' "$from_content/" "$to_root/"
  else
    # shellcopy excluding .git
    (
      cd "$from_content"
      tar cf - .
    ) | (
      cd "$to_root"
      tar xf -
    )
  fi
}

# Flatten legacy <name>-taskmark/taskmark/ → <name>-taskmark/
flatten_board_repo() {
  local root="$1"
  if [[ -f "$root/INDEX.md" ]]; then
    # Already flat; remove leftover nested folder if present
    if [[ -d "$root/taskmark" ]]; then
      rm -rf "$root/taskmark"
      echo "Removed nested taskmark/ under $root"
    fi
    return 0
  fi
  if [[ -f "$root/taskmark/INDEX.md" ]]; then
    if command -v rsync >/dev/null 2>&1; then
      rsync -a "$root/taskmark/" "$root/"
    else
      (
        cd "$root/taskmark"
        tar cf - .
      ) | (
        cd "$root"
        tar xf -
      )
    fi
    rm -rf "$root/taskmark"
    echo "Flattened $root/taskmark/ -> $root/"
  fi
}

# --- single product root ---
if [[ ${#product_roots[@]} -eq 1 ]]; then
  board="${product_roots[0]}"
  if [[ -n "$canonical" ]]; then
    board="$canonical"
  fi
  # If the only root is already a *-taskmark board repo, keep flat
  if is_board_repo "$board"; then
    flatten_board_repo "$board"
    if [[ ! -f "$board/INDEX.md" ]]; then
      echo "Board repo $board has no INDEX.md — run taskmark-init first." >&2
      exit 1
    fi
    write_repos_md "$board" "$board"
    echo "Mode: single-project (dedicated board repo)"
    echo "Canonical: $board"
    exit 0
  fi
  if [[ ! -d "$board/taskmark" ]]; then
    echo "Single-project root $board has no taskmark/ — run taskmark-init first." >&2
    exit 1
  fi
  write_repos_md "$board" "$board"
  echo "Mode: single-project"
  echo "Canonical: $board"
  echo "Board at $board/taskmark (project git); no sibling -taskmark created."
  exit 0
fi

# --- multi product roots ---
name="$(derive_common_name)"
if [[ -z "$name" ]]; then
  echo "Ambiguous common project name for multi-repo workspace." >&2
  echo "Product roots:" >&2
  for r in "${product_roots[@]}"; do
    echo "  - $r" >&2
  done
  echo "Ask the user for the common name, then re-run with: --name <common>" >&2
  echo "Dedicated folder will be: <common>-taskmark (board files at that repo root)" >&2
  exit 2
fi

parent="$(shared_parent "${product_roots[@]}")"
if [[ -z "$parent" ]]; then
  parent="$(dirname "${product_roots[0]}")"
fi

board_path="$parent/${name}-taskmark"
if [[ -n "$canonical" ]]; then
  board_path="$canonical"
fi

source="$(pick_richest_board_source)"

created=0
if [[ ! -d "$board_path" ]]; then
  mkdir -p "$board_path"
  created=1
fi

if [[ ! -d "$board_path/.git" ]]; then
  git -C "$board_path" init >/dev/null
  echo "Initialized git in $board_path"
fi

# Always flatten legacy nested layout first
flatten_board_repo "$board_path"

if [[ ! -f "$board_path/INDEX.md" ]]; then
  if [[ -n "$source" ]]; then
    copy_board_flat "$source" "$board_path"
    flatten_board_repo "$board_path"
    echo "Promoted board from $source -> $board_path/ (flat)"
  else
    echo "Multi-project board missing at $board_path/ — run taskmark-init there first." >&2
    exit 1
  fi
elif [[ "$migrate" -eq 1 && -n "$source" && "$source" != "$board_path" ]]; then
  src_n="$(epic_count "$source")"
  dst_n="$(epic_count "$board_path")"
  if [[ "$src_n" -gt "$dst_n" ]]; then
    copy_board_flat "$source" "$board_path"
    flatten_board_repo "$board_path"
    echo "Migrated richer board from $source -> $board_path/ (flat)"
  fi
fi

write_repos_md "$board_path" "$board_path" "${product_roots[@]}"

if [[ "$migrate" -eq 1 ]]; then
  for r in "${product_roots[@]}"; do
    if [[ "$r" == "$board_path" ]]; then
      continue
    fi
    if [[ -d "$r/taskmark" ]]; then
      rm -rf "$r/taskmark"
      echo "Removed product copy: $r/taskmark"
    fi
  done
fi

echo "Mode: multi-project"
echo "Common name: $name"
echo "Canonical: $board_path (board at repo root, not $board_path/taskmark)"
echo "Linked ${#product_roots[@]} product root(s); board is not copied into products."
if [[ "$created" -eq 1 ]]; then
  echo "Created: $board_path"
fi
