#!/usr/bin/env bash
# Copy this plugin package to ~/.cursor/plugins/local/taskmark
# Usage: rsync-plugin-local.sh [source_plugin_dir]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEFAULT_SRC="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC="${1:-$DEFAULT_SRC}"
DEST="${HOME}/.cursor/plugins/local/taskmark"

if [[ ! -f "$SRC/.cursor-plugin/plugin.json" ]]; then
  echo "Not a Taskmark plugin package (missing .cursor-plugin/plugin.json): $SRC" >&2
  exit 1
fi

mkdir -p "$(dirname "$DEST")"
if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete "$SRC/" "$DEST/"
else
  rm -rf "$DEST"
  cp -R "$SRC" "$DEST"
fi

echo "Synced: $SRC -> $DEST"
test -f "$DEST/.cursor-plugin/plugin.json"
