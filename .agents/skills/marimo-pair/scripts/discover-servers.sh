#!/usr/bin/env bash
# List running marimo instances from the server registry.
# Cleans up stale entries (dead PIDs) and outputs live servers as JSON.
# No marimo installation required.
set -euo pipefail

# Locate the servers directory
is_windows=false
if [[ "$OSTYPE" == msys* || "$OSTYPE" == cygwin* ]]; then
  is_windows=true
  servers_dir="$HOME/.marimo/servers"
else
  servers_dir="${XDG_STATE_HOME:-$HOME/.local/state}/marimo/servers"
fi

if [[ ! -d "$servers_dir" ]]; then
  echo "[]"
  exit 0
fi

# Liveness check. On POSIX, `kill -0 $pid` is cheap and reliable. On Windows
# (Git Bash/MSYS2) `kill` operates on Cygwin PIDs, not the native Windows PIDs
# marimo writes, so fall back to an HTTP probe against marimo's /health.
check_live() {
  local f="$1"
  if [[ "$is_windows" == false ]]; then
    local pid
    pid=$(jq -r '.pid' "$f" 2>/dev/null) || return 1
    kill -0 "$pid" 2>/dev/null
  else
    local host port base_url
    host=$(jq -r '.host' "$f" 2>/dev/null) || return 1
    port=$(jq -r '.port' "$f" 2>/dev/null) || return 1
    base_url=$(jq -r '.base_url' "$f" 2>/dev/null) || return 1
    curl -sf --max-time 1 "http://${host}:${port}${base_url}/health" >/dev/null 2>&1
  fi
}

results="[]"
for f in "$servers_dir"/*.json; do
  [[ -e "$f" ]] || continue

  if ! check_live "$f"; then
    # On Windows the HTTP probe can fail transiently (slow start, busy server),
    # so keep the entry; only POSIX `kill -0` is reliable enough to delete on.
    [[ "$is_windows" == false ]] && rm -f "$f"
    continue
  fi

  entry=$(jq '.' "$f" 2>/dev/null) || continue
  results=$(echo "$results" | jq --argjson e "$entry" '. + [$e]')
done

echo "$results" | jq .
