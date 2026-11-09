"""Public API for bipartite_maximum_matching_lib.

Exports the graph type and the maximum matching function.  The
implementation lives in ``core`` so that the package namespace stays
small and the import graph obvious.
"""

from .core import BipartiteGraph, maximum_matching

__all__ = ["BipartiteGraph", "maximum_matching"]
