#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

if [ ! -d venv ]; then
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r backend/requirements.txt
cd frontend
npm install

echo "Setup complete. Backend requirements installed and frontend dependencies installed."
