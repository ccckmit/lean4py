import pytest
from lean4py.graph_theory import Graph, max_flow, min_cut


class TestMaxFlow:
    def test_simple_flow(self):
        """Simple graph: source -> A -> sink."""
        g = Graph(["source", "A", "sink"])
        g.add_edge("source", "A", weight=5.0)
        g.add_edge("A", "sink", weight=3.0)
        flow, residual = max_flow(g, "source", "sink")
        assert flow == 3.0  # Limited by A->sink

    def test_parallel_edges(self):
        """Two paths: source -> A -> sink (cap 4), source -> B -> sink (cap 6)."""
        g = Graph(["s", "A", "B", "t"])
        g.add_edge("s", "A", weight=4.0)
        g.add_edge("A", "t", weight=4.0)
        g.add_edge("s", "B", weight=6.0)
        g.add_edge("B", "t", weight=6.0)
        flow, _ = max_flow(g, "s", "t")
        assert flow == 10.0

    def test_no_path(self):
        """No path from source to sink."""
        g = Graph(["s", "t"])
        # No edges
        flow, _ = max_flow(g, "s", "t")
        assert flow == 0.0


class TestMinCut:
    def test_simple_cut(self):
        """Same as max flow test."""
        g = Graph(["s", "A", "t"])
        g.add_edge("s", "A", weight=5.0)
        g.add_edge("A", "t", weight=3.0)
        flow, S, T = min_cut(g, "s", "t")
        assert flow == 3.0
        assert "s" in S
        assert "A" in S
        assert "t" in T

    def test_cut_partition(self):
        """S and T should partition vertices."""
        g = Graph(["s", "A", "B", "t"])
        g.add_edge("s", "A", weight=4.0)
        g.add_edge("A", "t", weight=4.0)
        g.add_edge("s", "B", weight=6.0)
        g.add_edge("B", "t", weight=6.0)
        flow, S, T = min_cut(g, "s", "t")
        all_vertices = set(g.vertices)
        assert S.union(T) == all_vertices
        assert len(S.intersection(T)) == 0
