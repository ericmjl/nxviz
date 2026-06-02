#!/usr/bin/env bash
set -euo pipefail

DOCS_DIR="docs"
SITE_DIR="site"
NOTEBOOKS_DIR="$SITE_DIR/notebooks"

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
    python -m marimo export md "$nb" -o "$md"
    echo "Exported $nb -> $md"
  fi
done

python -m zensical build

mkdir -p "$NOTEBOOKS_DIR"

for nb in "${NOTEBOOKS[@]}"; do
  if [ -f "$nb" ]; then
    stem=$(basename "${nb%.py}")
    html="$NOTEBOOKS_DIR/${stem}.html"
    python -m marimo export html "$nb" -o "$html" --sandbox --include-code \
      && echo "Exported $nb -> $html" \
      || echo "Warning: $nb failed to execute, skipping HTML export"
  fi
done

for nb in "${NOTEBOOKS[@]}"; do
  if [ -f "$nb" ]; then
    dest="$SITE_DIR/${nb#$DOCS_DIR/}"
    mkdir -p "$(dirname "$dest")"
    cp "$nb" "$dest"
    echo "Copied $nb -> $dest"
  fi
done

for nb in "${NOTEBOOKS[@]}"; do
  if [ -f "$nb" ]; then
    stem=$(basename "${nb%.py}")
    html_target="../../notebooks/${stem}.html"
    page_dir="$SITE_DIR/${nb#$DOCS_DIR/}"
    page_dir="${page_dir%.py}"
    mkdir -p "$page_dir"
    title=$(echo "$stem" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++)$i=toupper(substr($i,1,1))tolower(substr($i,2))}1')
    cat > "$page_dir/index.html" <<HTMLEOF
<!DOCTYPE html>
<html><head>
<meta http-equiv="refresh" content="0;url=${html_target}">
<title>${title}</title>
</head><body>
<p>Redirecting to <a href="${html_target}">executed notebook</a>...</p>
</body></html>
HTMLEOF
    echo "Created redirect $page_dir/index.html -> $html_target"
  fi
done
