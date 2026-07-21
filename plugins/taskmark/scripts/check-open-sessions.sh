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
from datetime import datetime, timedelta, timezone

raw = sys.argv[1]
try:
    payload = json.loads(raw)
except Exception:
    print("{}")
    raise SystemExit(0)

if payload.get("status") != "completed":
    print("{}")
    raise SystemExit(0)

if int(payload.get("loop_count") or 0) > 0:
    print("{}")
    raise SystemExit(0)

roots = payload.get("workspace_roots") or []
if not roots:
    roots = [os.getcwd()]

row_re = re.compile(
    r"^\|\s*\d+\s*\|\s*(\S+)\s*\|\s*([^|]+?)\|\s*([—\-–]?|\s*)\s*\|",
    re.MULTILINE,
)
id_re = re.compile(r"(?m)^id:\s*([ETSB]-\d+)\s*$")

def parse_ts(s):
    s = s.strip()
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z"):
        try:
            if fmt.endswith("%z") and s.endswith("Z"):
                s2 = s[:-1] + "+0000"
                return datetime.strptime(s2, "%Y-%m-%dT%H:%M:%S%z").astimezone(timezone.utc)
            if fmt.endswith("Z"):
                return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None

def idle_deadline(started):
    # 12:00 UTC on the UTC calendar day after Started's date
    d = started.astimezone(timezone.utc).date() + timedelta(days=1)
    return datetime(d.year, d.month, d.day, 12, 0, 0, tzinfo=timezone.utc)

now = datetime.now(timezone.utc)
open_items = []
idle_items = []

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
            m_id = id_re.search(text)
            item_id = m_id.group(1) if m_id else os.path.relpath(path, taskmark)
            for m in row_re.finditer(text):
                actor, started_s, ended_s = m.group(1), m.group(2), m.group(3)
                ended_s = (ended_s or "").strip()
                if ended_s and ended_s not in ("—", "-", "–", ""):
                    continue
                # open session
                if actor.startswith("agent"):
                    open_items.append(item_id)
                started = parse_ts(started_s)
                if started and now > idle_deadline(started):
                    idle_items.append(item_id)

def uniq(seq):
    seen, out = set(), []
    for x in seq:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out

open_items = uniq(open_items)
idle_items = uniq(idle_items)

if not open_items and not idle_items:
    print("{}")
    raise SystemExit(0)

parts = []
if open_items:
    ids = ", ".join(open_items[:12])
    more = "" if len(open_items) <= 12 else f" (+{len(open_items) - 12} more)"
    parts.append(
        f"Open agent session(s) for {ids}{more}: run complete-work or sync-status."
    )
if idle_items:
    ids = ", ".join(idle_items[:12])
    more = "" if len(idle_items) <= 12 else f" (+{len(idle_items) - 12} more)"
    parts.append(
        f"Idle-cap due for {ids}{more}: run sync-status to auto-close at next-day 12:00 UTC "
        "(do not count calendar idle months)."
    )

msg = "Taskmark: " + " ".join(parts)
print(json.dumps({"followup_message": msg}))
PY
