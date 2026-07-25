#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

if [ ! -d .git ]; then
  git init
  echo "Initialized git repository."
else
  echo "Git repository already exists."
fi

git config user.name "kathal99"
git config user.email "usr4206996@gmail.com"

if ! git remote | grep -q origin; then
  git remote add origin git@github.com:kathal99/agentic-audit-ai.git
  echo "Added GitHub remote origin."
else
  echo "Remote origin already configured."
fi

git add .
git commit -m "feat: init Agentic Audit AI" || echo "No changes to commit."

git push -u origin main

echo "GitHub setup complete."
