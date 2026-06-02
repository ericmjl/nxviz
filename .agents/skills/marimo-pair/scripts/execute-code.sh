#!/usr/bin/env bash
# Execute code in a running marimo session's scratchpad.
# No marimo installation required — talks directly to the HTTP API.
# Usage:
#   execute-code.sh [--port PORT] [--session ID] -c "code"   # inline code
#   execute-code.sh [--port PORT] [--session ID] script.py    # code from file
#   execute-code.sh [--port PORT] [--session ID] <<< "code"   # stdin (here-string)
#   execute-code.sh [--port PORT] [--session ID] <<'EOF'       # stdin (heredoc)
#     code
#   EOF
#   execute-code.sh --url URL [--session ID] -c "code"        # skip discovery, hit URL directly
#
# Auth: set MARIMO_TOKEN env var (preferred) or pass --token TOKEN (visible in ps).
set -euo pipefail

# Optional eval logging: set EXECUTE_CODE_LOG to a file path to record each call
if [[ -n "${EXECUTE_CODE_LOG:-}" ]]; then
  echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$EXECUTE_CODE_LOG"
fi

port=""
code=""
url=""
token="${MARIMO_TOKEN:-}"
session=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --port)    port="$2"; shift 2 ;;
    --url)     url="$2"; shift 2 ;;
    --token)   token="$2"; shift 2 ;;
    --session) session="$2"; shift 2 ;;
    -c)        code="$2"; shift 2 ;;
    -*)      echo "Unknown option: $1" >&2; exit 1 ;;
    *)       break ;;
  esac
done

if [[ -n "$code" ]]; then
  : # set via -c
elif [[ $# -gt 0 ]]; then
  code=$(cat "$1")
elif [[ ! -t 0 ]]; then
  code=$(cat)
else
  echo "Usage: execute-code.sh [--port PORT | --url URL] -c 'code'" >&2
  echo "       execute-code.sh [--port PORT | --url URL] script.py" >&2
  echo "       echo 'code' | execute-code.sh [--port PORT | --url URL]" >&2
  echo "Auth:  set MARIMO_TOKEN env var (preferred) or pass --token TOKEN" >&2
  exit 1
fi

if [[ -n "$url" ]]; then
  base="${url%/}"
  # Warn when connecting to a non-local server (data exfiltration risk)
  url_host="${url#*://}"
  url_host="${url_host%%[:/]*}"
  case "$url_host" in
    localhost|127.0.0.1|::1|0.0.0.0) ;;
    *) echo "Warning: connecting to non-local server '${url_host}'. Ensure this is trusted." >&2 ;;
  esac
else
  # Locate the servers directory
  is_windows=false
  if [[ "$OSTYPE" == msys* || "$OSTYPE" == cygwin* ]]; then
    is_windows=true
    servers_dir="$HOME/.marimo/servers"
  else
    servers_dir="${XDG_STATE_HOME:-$HOME/.local/state}/marimo/servers"
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

  # Find a live registry entry
  entry=""
  count=0
  for f in "$servers_dir"/*.json; do
    [[ -e "$f" ]] || continue

    if ! check_live "$f"; then
      # On Windows the HTTP probe can fail transiently (slow start, busy server),
      # so keep the entry; only POSIX `kill -0` is reliable enough to delete on.
      [[ "$is_windows" == false ]] && rm -f "$f"
      continue
    fi

    e=$(cat "$f")

    if [[ -n "$port" ]]; then
      e_port=$(echo "$e" | jq -r '.port')
      if [[ "$e_port" == "$port" ]]; then
        entry="$e"
        count=1
        break
      fi
      continue
    fi

    entry="$e"
    count=$((count + 1))
  done

  if [[ $count -eq 0 ]]; then
    echo "No running marimo instances found." >&2
    exit 1
  fi

  if [[ $count -gt 1 ]]; then
    echo "Multiple instances found. Use --port to specify:" >&2
    for f in "$servers_dir"/*.json; do
      [[ -e "$f" ]] || continue
      check_live "$f" || continue
      jq -r '.server_id' "$f" >&2
    done
    exit 1
  fi

  host=$(echo "$entry" | jq -r '.host')
  e_port=$(echo "$entry" | jq -r '.port')
  base_url=$(echo "$entry" | jq -r '.base_url')
  base="http://${host}:${e_port}${base_url}"
fi

# Build optional auth header
auth_args=()
if [[ -n "$token" ]]; then
  auth_args+=(-H "Authorization: Bearer ${token}")
fi

# Discover session ID
if [[ -n "$session" ]]; then
  session_id="$session"
else
  sessions_resp=$(curl -sf "${auth_args[@]+"${auth_args[@]}"}" "${base}/api/sessions") || {
    echo "Failed to connect to marimo server at ${base}" >&2
    exit 1
  }

  session_ids=$(echo "$sessions_resp" | jq -r 'keys[]')

  if [[ -z "$session_ids" ]]; then
    echo "No active sessions on the server. Make sure a notebook is open in the browser." >&2
    exit 1
  fi

  session_count=$(echo "$session_ids" | wc -l | tr -d ' ')

  if [[ $session_count -gt 1 ]]; then
    echo "Multiple sessions on server. Cannot auto-select:" >&2
    echo "$sessions_resp" | jq -r 'to_entries[] | "\(.key)  \(.value.filename // "")"' >&2
    exit 1
  fi

  session_id=$(echo "$session_ids" | head -1)
fi

# Execute code via SSE stream
# Events: stdout/stderr stream as JSON {"data":"..."}, done is final result.
exit_code=0
current_event=""
done_received=false
while IFS= read -r line && [[ "$done_received" == false ]]; do
  case "$line" in
    event:*)
      current_event="${line#event: }"
      ;;
    data:*)
      payload="${line#data: }"
      case "$current_event" in
        stdout)
          echo "$payload" | jq -jr '.data'
          ;;
        stderr)
          echo "$payload" | jq -jr '.data' >&2
          ;;
        done)
          if echo "$payload" | jq -e '.success == false' >/dev/null 2>&1; then
            echo "$payload" | jq -r '.error.msg' >&2
            exit_code=1
          else
            echo "$payload" | jq -r '.output.data // empty'
          fi
          done_received=true
          ;;
      esac
      ;;
  esac
done < <(curl -sN -X POST "${base}/api/kernel/execute" \
  -H "Content-Type: application/json" \
  -H "Marimo-Session-Id: ${session_id}" \
  ${auth_args[@]+"${auth_args[@]}"} \
  -d "$(jq -n --arg c "$code" '{code: $c}')" \
)

exit "$exit_code"
