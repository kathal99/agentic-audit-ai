#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

if [ ! -d venv ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r backend/requirements.txt

pushd frontend > /dev/null
npm install
popd > /dev/null

echo "All dependencies installed."

echo "To run the backend: source venv/bin/activate && uvicorn backend.server:app --reload --port 8000"
echo "To run the frontend: cd frontend && npm run dev"
