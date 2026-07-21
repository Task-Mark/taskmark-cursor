#!/usr/bin/env bash
# Recompute Taskmark actual_minutes (+ optional sizing calibration).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASKMARK="${1:-}"
shift || true

if [[ -z "${TASKMARK}" ]]; then
  echo "Usage: $0 /path/to/taskmark [--calibrate] [--dry-run]" >&2
  exit 1
fi

exec python3 "${SCRIPT_DIR}/recompute-actuals.py" "${TASKMARK}" "$@"
