import subprocess
import sys
from pathlib import Path

docs_dir = Path("docs")

marimo_files = [
    docs_dir / "api" / "high-level-api.py",
    docs_dir / "api" / "mid-level-api.py",
    docs_dir / "api" / "low-level-api.py",
    docs_dir / "api" / "object-oriented-api.py",
    docs_dir / "api" / "facet-api.py",
    docs_dir / "developers" / "new-plots.py",
    docs_dir / "examples" / "matrix.py",
    docs_dir / "examples" / "geo.py",
    docs_dir / "examples" / "arc_node_labels.py",
    docs_dir / "examples" / "circos_node_labels.py",
    docs_dir / "examples" / "matrix_node_labels.py",
]

for py_file in marimo_files:
    md_file = py_file.with_suffix(".md")
    if py_file.exists():
        subprocess.run(
            [sys.executable, "-m", "marimo", "export", "md", str(py_file), "-o", str(md_file)],
            check=True,
        )
        print(f"Exported {py_file} -> {md_file}")
    else:
        print(f"Skipping {py_file} (not found)")

subprocess.run([sys.executable, "-m", "zensical", "build"], check=True)
