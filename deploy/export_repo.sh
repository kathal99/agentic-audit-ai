#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."
OUTPUT="$(pwd)/agentic-audit-ai-export-$(date +%Y%m%d-%H%M%S).zip"
EXCLUDES=(
  "*/.git/*"
  "venv/*"
  "frontend/node_modules/*"
  "node_modules/*"
  "*.zip"
)

if command -v zip >/dev/null 2>&1; then
  echo "Packaging repository into: $OUTPUT"
  zip -r "$OUTPUT" . "${EXCLUDES[@]}"
else
  echo "zip not found, using Python's zipfile module"
  python3 - <<'PY'
import os, zipfile
root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
out = os.path.join(root, f'agentic-audit-ai-export-{__import__('datetime').datetime.now().strftime("%Y%m%d-%H%M%S")}.zip')
excludes = {'.git', 'venv', 'node_modules', 'frontend/node_modules'}
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
    for base, dirs, files in os.walk(root):
        rel = os.path.relpath(base, root)
        if any(rel == ex or rel.startswith(ex + os.sep) for ex in excludes):
            continue
        for f in files:
            if f.endswith('.zip') and base == root:
                continue
            full = os.path.join(base, f)
            zf.write(full, os.path.relpath(full, root))
print(out)
PY
  exit 0
fi

echo "Done. Share the generated ZIP file from the project directory."
