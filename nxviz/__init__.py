"""Top-level nxviz API."""
from .api import (
    arc,
    hive,
    circos,
    parallel,
    matrix,
    geo,
    ArcPlot,
    HivePlot,
    MatrixPlot,
    CircosPlot,
)

import warnings


warnings.warn(
    """
nxviz has a new API! Version 0.7.4 onwards, the old class-based API is being
deprecated in favour of a new API focused on advancing a grammar of network
graphics. If your plotting code depends on the old API, please consider
pinning nxviz at version 0.7.4, as the new API will break your old code.

To check out the new API, please head over to the docs at
https://ericmjl.github.io/nxviz/ to learn more. We hope you enjoy using it!

(This deprecation message will go away in version 1.0.)
"""
)
