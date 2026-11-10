# bipartite_maximum_matching_lib

Finds a maximum-cardinality matching in a bipartite graph using augmenting paths via depth-first search.

```python
from bipartite_maximum_matching_lib import BipartiteGraph, maximum_matching

g = BipartiteGraph()
g.add_edge("alice", "task-1")
g.add_edge("alice", "task-2")
g.add_edge("bob", "task-1")

matching = maximum_matching(g)
# {"alice": "task-1", "bob": "task-2"}
```

## Why this exists

A maximum matching is the standard way to assign as many items as
possible when each item can only take one partner and each partner can
only take one item.  The classical solution is an augmenting-path
search: start from an unmatched left vertex, walk alternating edges
until an unmatched right vertex is reached, and flip the path.  The
full Hopcroft-Karp algorithm layers a breadth-first search on top to
get O(E sqrt(V)); this library deliberately stops at the plain DFS
variant.  The trade-off is a worst case of O(V * E) for a much smaller
implementation.  The graphs this library is meant for are small enough
that the asymptotic difference does not matter, and a reader can hold
the whole algorithm in their head.

## API

The package exports exactly two names.

### `BipartiteGraph()`

A bipartite graph with left and right vertex sets.  Left and right
vertices may be any hashable Python object.  Edges are directed from
left to right; there is no `add_vertex`, because adding an edge with a
new endpoint creates that endpoint.

- `add_edge(left, right)` — add the directed edge `left -> right`.
  Duplicate edges are ignored.
- `left_vertices()` — left vertices in insertion order.
- `right_vertices()` — right vertices in insertion order.
- `neighbours(left)` — right neighbours of `left` in insertion order,
  or `[]` if `left` is unknown.
- `left in graph` — membership test for left vertices.
- `len(graph)` — number of left vertices.

### `maximum_matching(graph)`

Returns a `dict` mapping each matched left vertex to its matched right
vertex.  Unmatched left vertices are absent from the result.  The
matching is maximum in cardinality but not necessarily unique; the
insertion order of edges decides which of several maximum matchings is
returned, so the same construction sequence always yields the same
result.

## The awkward edge

The result is a left-to-right mapping only.  There is no reverse map,
and an unmatched left vertex is indistinguishable from a left vertex
that was never added.  If you need to know which left vertices were
left out, compare `graph.left_vertices()` against `matching.keys()`.
