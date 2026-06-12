#!/usr/bin/env bash
# Export flowchart frames from design/design.pen to report PNG assets.
# Requires Pencil MCP or: open design.pen in Pencil canvas, then run via Agent.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PEN="$ROOT/design/design.pen"
OUT="$ROOT/src/assets/figures"

if [[ ! -f "$PEN" ]]; then
  echo "Missing $PEN"
  exit 1
fi

python3 - <<'PY' "$PEN"
import json, sys
pen = json.loads(open(sys.argv[1], encoding="utf-8").read())
for child in pen.get("children", []):
    if child.get("type") == "frame":
        print(f"{child['id']}\t{child.get('name','')}")
PY

echo ""
echo "Open design/design.pen in Pencil, then ask Agent:"
echo '  export_nodes → rename to fig5-teaching-flow.png / fig4-experiment-flow.png'
echo "Output dir: $OUT"
