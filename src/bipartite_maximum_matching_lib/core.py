"""Maximum-cardinality matching in a bipartite graph.

The algorithm is the classical augmenting-path method (Hopcroft-Karp
without the BFS layering, i.e. plain Kuhn's algorithm).  We chose the
simpler DFS-only variant because the graphs this library targets are
small enough that the extra bookkeeping of a layered BFS is not worth
the added surface area.  The running time is O(V * E) in the worst
case, which is fine for the intended use.

Vertices on the left and right are identified by hashable Python
objects.  The graph stores adjacency from left vertices to right
vertices only; the matching is returned as a dict mapping left
vertices to their matched right vertex.  A left vertex that is not
matched does not appear in the result.
"""

from __future__ import annotations

from collections.abc import Hashable, Iterable
from typing import Dict, Generic, List, Optional, Set, Tuple, TypeVar

L = TypeVar("L", bound=Hashable)
R = TypeVar("R", bound=Hashable)


class BipartiteGraph(Generic[L, R]):
    """A bipartite graph with left and right vertex sets.

    Edges are directed from left to right.  Adding an edge whose left
    endpoint has not been seen before creates that left vertex; the
    same is true for the right endpoint.  This keeps the construction
    API to a single call and avoids a separate ``add_vertex`` step that
    callers would otherwise have to remember.
    """

    def __init__(self) -> None:
        self._adj: Dict[L, List[R]] = {}
        self._right_seen: Set[R] = set()

    def add_edge(self, left: L, right: R) -> None:
        """Add a directed edge ``left -> right``.

        Duplicate edges are ignored.  We keep the adjacency list in
        insertion order so that the matching produced by
        ``maximum_matching`` is deterministic for a given insertion
        order; this matters for tests and for users who want to
        reproduce a run.
        """
        neighbours = self._adj.setdefault(left, [])
        if right not in neighbours:
            neighbours.append(right)
        self._right_seen.add(right)

    def left_vertices(self) -> List[L]:
        """Return the left vertices in insertion order."""
        return list(self._adj.keys())

    def right_vertices(self) -> List[R]:
        """Return the right vertices in insertion order."""
        return list(self._right_seen)

    def neighbours(self, left: L) -> List[R]:
        """Return the right neighbours of ``left`` in insertion order.

        Unknown left vertices have no neighbours; we return an empty
        list rather than raising so that callers can probe the graph
        without a membership check.
        """
        return list(self._adj.get(left, ()))

    def __contains__(self, left: L) -> bool:
        return left in self._adj

    def __len__(self) -> int:
        """Number of left vertices."""
        return len(self._adj)


def maximum_matching(graph: BipartiteGraph[L, R]) -> Dict[L, R]:
    """Return a maximum-cardinality matching as a left-to-right dict.

    The algorithm repeatedly looks for an augmenting path starting at
    an unmatched left vertex.  A DFS marks right vertices as visited
    within a single augmentation attempt so that the search does not
    loop; the mark is cleared between attempts.  Because each
    successful attempt increases the matching size by exactly one, the
    loop terminates after at most ``min(|L|, |R|)`` augmentations.

    The result maps each matched left vertex to its matched right
    vertex.  Unmatched left vertices are absent.  The matching is not
    necessarily unique; the insertion order of edges determines which
    of several maximum matchings is returned.
    """
    match_right: Dict[R, L] = {}

    def try_augment(left: L, visited: Set[R]) -> bool:
        for right in graph.neighbours(left):
            if right in visited:
                continue
            visited.add(right)
            current = match_right.get(right)
            if current is None or try_augment(current, visited):
                match_right[right] = left
                return True
        return False

    for left in graph.left_vertices():
        try_augment(left, set())

    return {left: right for right, left in match_right.items()}
