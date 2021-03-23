"""Ways to draw edges as lines."""


from typing import Dict, Iterable, List

from matplotlib.patches import Path, PathPatch, Patch
import pandas as pd


def circos(
    et: pd.DataFrame,
    pos: Dict,
    edge_color: Iterable,
    alpha: Iterable,
    lw: Iterable,
    edge_kwargs: Dict,
) -> List[Patch]:
    patches = []
    for r, d in et.iterrows():
        verts = [pos[d["source"]], (0, 0), pos[d["target"]]]
        codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        path = Path(verts, codes)
        patch = PathPatch(
            path, edgecolor=edge_color[r], alpha=alpha[r], lw=lw[r], **edge_kwargs
        )
        patches.append(patch)
    return patches


def line(
    et: pd.DataFrame,
    pos: Dict,
    edge_color: Iterable,
    alpha: Iterable,
    lw: Iterable,
    edge_kwargs: Dict,
):
    patches = []
    for r, d in et.iterrows():
        start = d["source"]
        end = d["target"]
        verts = [pos[start], pos[end]]
        codes = [Path.MOVETO, Path.LINETO]
        path = Path(verts, codes)
        patch = PathPatch(
            path, edgecolor=edge_color[r], alpha=alpha[r], lw=lw[r], **edge_kwargs
        )
        patches.append(patch)
    return patches