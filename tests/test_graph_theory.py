import pytest
from lean4py.graph_theory import (
    Graph, Vertex, Edge,
    bfs, dfs, shortest_path, dijkstra, bellman_ford,
    is_connected, is_bipartite, connected_components,
    has_cycle, topological_sort,
    eulerian_path, spanning_tree, minimum_spanning_tree,
    is_complete, graph_clique, is_eulerian,
    graph_coloring, complement_graph,
    adjacency_list, adjacency_matrix,
    has_hamiltonian_path,
)

class TestGraphInit:
    def test_graph_empty(self):
        g = Graph()
        assert len(g.vertices) == 0

    def test_graph_vertices(self):
        g = Graph(vertices=[1, 2, 3])
        assert len(g.vertices) == 3

    def test_graph_edges(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)])
        assert len(g.vertices) == 3

    def test_graph_weighted(self):
        g = Graph(weighted_edges=[(1, 2, 3.0), (2, 3, 4.0)])
        assert len(g.vertices) == 3
        assert g.weights[(1, 2)] == 3.0

class TestGraphOperations:
    def test_add_vertex(self):
        g = Graph()
        g.add_vertex(1)
        assert 1 in g.vertices

    def test_add_edge(self):
        g = Graph(vertices=[1, 2])
        g.add_edge(1, 2)
        assert 2 in g.neighbors(1)

    def test_remove_vertex(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)])
        g.remove_vertex(2)
        assert 2 not in g.vertices

    def test_remove_edge(self):
        g = Graph(vertices=[1, 2], edges=[(1, 2)])
        g.remove_edge(1, 2)
        assert 2 not in g.neighbors(1)

    def test_degree(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (1, 3)])
        assert g.degree(1) == 2

class TestAdjacency:
    def test_adjacency_list(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)])
        adj = adjacency_list(g)
        assert 1 in adj[2]
        assert 3 in adj[2]

    def test_adjacency_matrix(self):
        g = Graph(vertices=[1, 2], edges=[(1, 2)])
        vertices, matrix = adjacency_matrix(g)
        assert matrix[0][1] == 1
        assert matrix[1][0] == 1

class TestBFS:
    def test_bfs_simple(self):
        g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (2, 3), (3, 4)])
        result = bfs(g, 1)
        assert result == [1, 2, 3, 4]

    def test_bfs_disconnected(self):
        g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (3, 4)])
        result = bfs(g, 1)
        assert result == [1, 2]

class TestDFS:
    def test_dfs_simple(self):
        g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (2, 3), (3, 4)])
        result = dfs(g, 1)
        assert result == [1, 2, 3, 4]

class TestShortestPath:
    def test_shortest_path(self):
        g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (2, 3), (3, 4)])
        result = shortest_path(g, 1, 4)
        assert result == [1, 2, 3, 4]

    def test_shortest_path_direct(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (1, 3)])
        result = shortest_path(g, 1, 3)
        assert result == [1, 3]

class TestDijkstra:
    def test_dijkstra(self):
        g = Graph(weighted_edges=[(1, 2, 1.0), (2, 3, 2.0), (1, 3, 4.0)])
        path, dist = dijkstra(g, 1, 3)
        assert path == [1, 2, 3]
        assert abs(dist - 3.0) < 1e-10

    def test_dijkstra_no_path(self):
        g = Graph(weighted_edges=[(1, 2, 1.0)])
        result = dijkstra(g, 1, 3)
        assert result is None

class TestBellmanFord:
    def test_bellman_ford(self):
        g = Graph(weighted_edges=[(1, 2, 1.0), (2, 3, 2.0)])
        dist = bellman_ford(g, 1)
        assert dist is not None
        assert dist[1] == 0.0
        assert dist[2] == 1.0
        assert dist[3] == 3.0

class TestIsConnected:
    def test_connected(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)])
        assert is_connected(g)

    def test_not_connected(self):
        g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (3, 4)])
        assert not is_connected(g)

class TestIsBipartite:
    def test_bipartite(self):
        g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 3), (2, 4)])
        assert is_bipartite(g)

    def test_not_bipartite(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (3, 1)])
        assert not is_bipartite(g)

class TestConnectedComponents:
    def test_connected_components(self):
        g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (3, 4)])
        components = connected_components(g)
        assert len(components) == 2

class TestHasCycle:
    def test_cycle(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (3, 1)])
        assert has_cycle(g)

    def test_no_cycle(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)])
        assert not has_cycle(g)

class TestTopologicalSort:
    def test_topological_sort(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (1, 3)], directed=True)
        result = topological_sort(g)
        assert result is not None
        assert result.index(1) < result.index(2)
        assert result.index(1) < result.index(3)

class TestSpanningTree:
    def test_spanning_tree(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (1, 3)])
        tree = spanning_tree(g, 1)
        assert tree is not None
        assert len(tree.vertices) == len(g.vertices)

class TestMST:
    def test_mst(self):
        g = Graph(weighted_edges=[(1, 2, 1.0), (2, 3, 2.0), (1, 3, 5.0)])
        mst = minimum_spanning_tree(g)
        assert mst is not None
        assert len(mst.vertices) == len(g.vertices)

class TestIsComplete:
    def test_complete_graph(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (1, 3)])
        assert is_complete(g)

    def test_not_complete(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)])
        assert not is_complete(g)

class TestDirectedGraph:
    def test_directed_in_out_degree(self):
        g = Graph(vertices=[1, 2], edges=[(1, 2)], directed=True)
        assert g.out_degree(1) == 1
        assert g.in_degree(2) == 1

    def test_directed_bfs(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3)], directed=True)
        result = bfs(g, 1)
        assert result == [1, 2, 3]


class TestEulerian:
    def test_eulerian_circuit(self):
        # Triangle with all vertices degree 2
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (3, 1)])
        result, type_ = is_eulerian(g)
        assert result is True
        assert type_ == "circuit"

    def test_eulerian_path(self):
        # Path: 1-2-3-4 (vertices 2 and 3 have degree 2, 1 and 4 have degree 1)
        g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 2), (2, 3), (3, 4)])
        result, type_ = is_eulerian(g)
        assert result is True
        assert type_ == "path"

    def test_not_eulerian(self):
        # Graph with 4 vertices having odd degree (no Eulerian path or circuit)
        # Vertex 1: degree 3, Vertex 2: degree 3, Vertex 3: degree 2, Vertex 4: degree 2
        g = Graph(vertices=[1,2,3,4,5], edges=[(1,2),(2,3),(3,1),(1,4),(2,5)])
        result, type_ = is_eulerian(g)
        assert result is False
        assert type_ == "none"

    def test_eulerian_empty(self):
        g = Graph(vertices=[])
        result, type_ = is_eulerian(g)
        assert result is True
        assert type_ == "circuit"


class TestGraphColoring:
    def test_coloring_bipartite(self):
        # Bipartite graph K2,2
        g = Graph(vertices=[1, 2, 3, 4], edges=[(1, 3), (1, 4), (2, 3), (2, 4)])
        colors = graph_coloring(g)
        # Adjacent vertices should have different colors
        for u in g.vertices:
            for v in g.neighbors(u):
                if u < v:  # Avoid duplicate checks
                    assert colors[u] != colors[v]
        # Should use at most 2 colors
        assert len(set(colors.values())) <= 2

    def test_coloring_complete(self):
        # Complete graph K3 needs 3 colors
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (3, 1)])
        colors = graph_coloring(g)
        assert len(set(colors.values())) == 3

    def test_coloring_single_vertex(self):
        g = Graph(vertices=[1])
        colors = graph_coloring(g)
        assert colors[1] == 0

    def test_coloring_empty(self):
        g = Graph(vertices=[])
        colors = graph_coloring(g)
        assert colors == {}


class TestGraphClique:
    def test_clique_single(self):
        g = Graph(vertices=[1])
        result = graph_clique(g)
        assert result == [1]

    def test_clique_triangle(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2), (2, 3), (3, 1)])
        result = graph_clique(g)
        assert len(result) == 3

    def test_clique_empty(self):
        g = Graph(vertices=[])
        result = graph_clique(g)
        assert result == []


class TestComplementGraph:
    def test_complement_simple(self):
        g = Graph(vertices=[1, 2, 3], edges=[(1, 2)])
        comp = complement_graph(g)
        # Check that edge 2-3 or 3-2 is in complement's adjacency
        assert 3 in comp.adjacency.get(1, set()) or 1 in comp.adjacency.get(3, set())
class TestHamiltonianPath:
    def test_complete_graph(self):
        g = Graph(["A", "B", "C"])
        for u, v in [("A","B"), ("B","C"), ("A","C")]:
            g.add_edge(u, v)
        assert has_hamiltonian_path(g) == True

    def test_single_vertex(self):
        g = Graph(["A"])
        assert has_hamiltonian_path(g) == True

    def test_two_vertices_no_edge(self):
        g = Graph(["A", "B"])
        # Dirac: deg < n/2 = 1, so False
        assert has_hamiltonian_path(g) == False

    def test_line_graph(self):
        g = Graph([1, 2, 3, 4])
        for i in range(3):
            g.add_edge(i+1, i+2)
        # Each vertex has degree 1 or 2, n=4, n/2=2
        # Endpoints have degree 1 < 2, so False
        assert has_hamiltonian_path(g) == False
