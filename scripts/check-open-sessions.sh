#!/usr/bin/env bash
# Fail-open: on any error, emit {} so the agent stop is never blocked.
set -u

emit_empty() {
  printf '%s\n' '{}'
  exit 0
}

trap emit_empty ERR

input="$(cat || true)"
if [[ -z "${input}" ]]; then
  emit_empty
fi

if ! command -v python3 >/dev/null 2>&1; then
  emit_empty
fi

python3 - "$input" <<'PY'
import json, os, re, sys

raw = sys.argv[1]
try:
    payload = json.loads(raw)
except Exception:
    print("{}")
    raise SystemExit(0)

if payload.get("status") != "completed":
    print("{}")
    raise SystemExit(0)

# Only nudge once per conversation turn chain
if int(payload.get("loop_count") or 0) > 0:
    print("{}")
    raise SystemExit(0)

roots = payload.get("workspace_roots") or []
if not roots:
    cwd = os.getcwd()
    roots = [cwd]

open_items = []
# Match work-log rows: | N | agent | timestamp | — |
row_re = re.compile(
    r"^\|\s*\d+\s*\|\s*agent(?:[:\w-]*)?\s*\|\s*([^|]+)\|\s*[—\-–]?\s*\|",
    re.MULTILINE,
)
id_re = re.compile(r"(?m)^id:\s*([ETSB]-\d+)\s*$")

for root in roots:
    taskmark = os.path.join(root, "taskmark")
    if not os.path.isdir(taskmark):
        continue
    for dirpath, _, filenames in os.walk(taskmark):
        for name in filenames:
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            try:
                text = open(path, encoding="utf-8").read()
            except OSError:
                continue
            if "## Work log" not in text:
                continue
            if not row_re.search(text):
                continue
            m = id_re.search(text)
            item_id = m.group(1) if m else os.path.relpath(path, taskmark)
            open_items.append(item_id)

# Dedupe preserving order
seen = set()
unique = []
for i in open_items:
    if i not in seen:
        seen.add(i)
        unique.append(i)

if not unique:
    print("{}")
    raise SystemExit(0)

ids = ", ".join(unique[:12])
more = "" if len(unique) <= 12 else f" (+{len(unique) - 12} more)"
msg = (
    "Taskmark: open agent work session(s) still unmarked as ended "
    f"for {ids}{more}. Run complete-work (or /complete-work) on those items "
    "to close the Work log Ended column and sync-status, then stop."
)
print(json.dumps({"followup_message": msg}))
PY
