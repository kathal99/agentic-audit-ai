#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

if [ ! -d venv ]; then
  echo "Virtual environment not found. Run deploy/start_services.sh first."
  exit 1
fi

source venv/bin/activate

echo "Starting backend..."
uvicorn backend.server:app --reload --port 8000 &
BACKEND_PID=$!

echo "Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!

trap 'echo "Stopping services..."; kill $BACKEND_PID $FRONTEND_PID; exit' INT TERM
wait
