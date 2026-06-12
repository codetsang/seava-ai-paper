#!/usr/bin/env bash
# Export Pencil frames to report PNG assets. Requires: pencil login (or PENCIL_CLI_KEY).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PEN="$ROOT/design/report-figures.pen"
OUT="$ROOT/src/assets/figures"
TMP="$ROOT/design/export-tmp"

if ! command -v pencil >/dev/null 2>&1; then
  echo "Pencil CLI not found. Run: npm install -g @pencil.dev/cli"
  exit 1
fi

if ! pencil status 2>&1 | grep -q "Authenticated"; then
  echo "Not logged in to Pencil. Run: pencil login"
  exit 1
fi

if [[ ! -f "$PEN" ]]; then
  echo "Missing $PEN — run: npm run generate:pen"
  exit 1
fi

mkdir -p "$TMP" "$OUT"

printf '%s\n' \
  'export_nodes({ nodeIds: ["fig4Experiment", "fig5Teaching"], outputDir: "'"$TMP"'", format: "png", scale: 2 })' \
  'save()' \
  'exit()' \
  | pencil interactive -i "$PEN" -o "$PEN"

mv -f "$TMP/fig4Experiment.png" "$OUT/fig4-experiment-flow.png"
mv -f "$TMP/fig5Teaching.png" "$OUT/fig5-teaching-flow.png"
rmdir "$TMP" 2>/dev/null || true

echo "Exported PNGs to $OUT"
