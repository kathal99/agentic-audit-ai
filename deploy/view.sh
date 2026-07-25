#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

if [ ! -d venv ]; then
  echo "Creating Python virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r backend/requirements.txt

pushd frontend > /dev/null
npm install
popd > /dev/null

mkdir -p .tmp
BACKEND_LOG=".tmp/backend.log"
FRONTEND_LOG=".tmp/frontend.log"
BACKEND_PID_FILE=".tmp/view-backend.pid"
FRONTEND_PID_FILE=".tmp/view-frontend.pid"

start_process() {
  local name="$1"
  local pid_file="$2"
  local command="$3"
  local log_file="$4"
  if [ -f "$pid_file" ] && kill -0 "$(cat "$pid_file")" >/dev/null 2>&1; then
    echo "$name already running (PID $(cat "$pid_file"))"
  else
    nohup bash -lc "$command" >"$log_file" 2>&1 &
    echo $! >"$pid_file"
    echo "Started $name with PID $(cat "$pid_file")"
  fi
}

start_process "backend" "$BACKEND_PID_FILE" "source venv/bin/activate && uvicorn backend.server:app --reload --port 8000" "$BACKEND_LOG"
start_process "frontend" "$FRONTEND_PID_FILE" "cd frontend && npm run dev -- --host 127.0.0.1 --port 5173" "$FRONTEND_LOG"

sleep 2

echo
cat <<EOF
Your local dashboard should be available at:
  http://127.0.0.1:5173

Backend logs: $BACKEND_LOG
Frontend logs: $FRONTEND_LOG
EOF

if command -v xdg-open >/dev/null 2>&1 && [ -n "${DISPLAY-}" ]; then
  xdg-open http://127.0.0.1:5173 >/dev/null 2>&1 || true
fi
