#!/usr/bin/env bash
set -euo pipefail

DOCS_DIR="docs"

NOTEBOOKS=(
  "$DOCS_DIR/api/high-level-api.py"
  "$DOCS_DIR/api/mid-level-api.py"
  "$DOCS_DIR/api/low-level-api.py"
  "$DOCS_DIR/api/object-oriented-api.py"
  "$DOCS_DIR/api/facet-api.py"
  "$DOCS_DIR/developers/new-plots.py"
  "$DOCS_DIR/examples/matrix.py"
  "$DOCS_DIR/examples/geo.py"
  "$DOCS_DIR/examples/arc_node_labels.py"
  "$DOCS_DIR/examples/circos_node_labels.py"
  "$DOCS_DIR/examples/matrix_node_labels.py"
)

for nb in "${NOTEBOOKS[@]}"; do
  if [ -f "$nb" ]; then
    md="${nb%.py}.md"
    python -m marimo export md "$nb" -o "$md" --sandbox
    echo "Exported $nb -> $md"
  fi
done

python -m zensical build
