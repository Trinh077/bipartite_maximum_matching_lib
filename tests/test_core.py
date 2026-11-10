import unittest

from bipartite_maximum_matching_lib import BipartiteGraph, maximum_matching


class TestBipartiteGraph(unittest.TestCase):
    def test_empty_graph_has_no_left_vertices(self):
        g = BipartiteGraph()
        self.assertEqual(g.left_vertices(), [])
        self.assertEqual(g.right_vertices(), [])
        self.assertEqual(len(g), 0)

    def test_add_edge_registers_both_endpoints(self):
        g = BipartiteGraph()
        g.add_edge("a", 1)
        self.assertEqual(g.left_vertices(), ["a"])
        self.assertEqual(g.right_vertices(), [1])
        self.assertIn("a", g)
        self.assertNotIn("b", g)

    def test_duplicate_edges_are_ignored(self):
        g = BipartiteGraph()
        g.add_edge("a", 1)
        g.add_edge("a", 1)
        self.assertEqual(g.neighbours("a"), [1])

    def test_neighbours_of_unknown_left_vertex_is_empty(self):
        g = BipartiteGraph()
        self.assertEqual(g.neighbours("missing"), [])

    def test_neighbours_preserve_insertion_order(self):
        g = BipartiteGraph()
        g.add_edge("a", 3)
        g.add_edge("a", 1)
        g.add_edge("a", 2)
        self.assertEqual(g.neighbours("a"), [3, 1, 2])


class TestMaximumMatching(unittest.TestCase):
    def test_empty_graph(self):
        g = BipartiteGraph()
        self.assertEqual(maximum_matching(g), {})

    def test_single_edge(self):
        g = BipartiteGraph()
        g.add_edge("a", 1)
        self.assertEqual(maximum_matching(g), {"a": 1})

    def test_perfect_matching_on_path(self):
        g = BipartiteGraph()
        g.add_edge("a", 1)
        g.add_edge("a", 2)
        g.add_edge("b", 2)
        result = maximum_matching(g)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], 2)

    def test_augmenting_path_required(self):
        # a -> 1, b -> 1, b -> 2.  Greedy assignment of a to 1 forces
        # an augmenting path a -> 1 -> b -> 2 to reach size 2.
        g = BipartiteGraph()
        g.add_edge("a", 1)
        g.add_edge("b", 1)
        g.add_edge("b", 2)
        result = maximum_matching(g)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"], 2)

    def test_unmatched_left_vertex_is_absent(self):
        g = BipartiteGraph()
        g.add_edge("a", 1)
        g.add_edge("b", 1)
        result = maximum_matching(g)
        self.assertEqual(len(result), 1)
        self.assertIn(result, [{"a": 1}, {"b": 1}])

    def test_empty_right_side(self):
        g = BipartiteGraph()
        # No edges, so no right vertices either; this is the same as
        # the empty graph but exercises the loop over left vertices.
        self.assertEqual(maximum_matching(g), {})

    def test_disconnected_components(self):
        g = BipartiteGraph()
        g.add_edge("a", 1)
        g.add_edge("b", 2)
        g.add_edge("c", 3)
        result = maximum_matching(g)
        self.assertEqual(result, {"a": 1, "b": 2, "c": 3})

    def test_cycle_of_length_four(self):
        g = BipartiteGraph()
        g.add_edge("a", 1)
        g.add_edge("a", 2)
        g.add_edge("b", 1)
        g.add_edge("b", 2)
        result = maximum_matching(g)
        self.assertEqual(len(result), 2)
        self.assertEqual(set(result.keys()), {"a", "b"})
        self.assertEqual(set(result.values()), {1, 2})

    def test_complete_bipartite_k33(self):
        g = BipartiteGraph()
        for left in ("a", "b", "c"):
            for right in (1, 2, 3):
                g.add_edge(left, right)
        result = maximum_matching(g)
        self.assertEqual(len(result), 3)
        self.assertEqual(set(result.keys()), {"a", "b", "c"})
        self.assertEqual(set(result.values()), {1, 2, 3})

    def test_more_left_than_right(self):
        g = BipartiteGraph()
        g.add_edge("a", 1)
        g.add_edge("b", 1)
        g.add_edge("c", 1)
        result = maximum_matching(g)
        self.assertEqual(len(result), 1)
        self.assertEqual(set(result.values()), {1})

    def test_more_right_than_left(self):
        g = BipartiteGraph()
        g.add_edge("a", 1)
        g.add_edge("a", 2)
        g.add_edge("a", 3)
        result = maximum_matching(g)
        self.assertEqual(len(result), 1)
        self.assertEqual(result["a"], 1)

    def test_non_string_hashable_vertices(self):
        g = BipartiteGraph()
        g.add_edge(0, "x")
        g.add_edge(1, "y")
        self.assertEqual(maximum_matching(g), {0: "x", 1: "y"})


if __name__ == "__main__":
    unittest.main()
