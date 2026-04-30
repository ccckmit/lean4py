"""Tests for topology module."""

import pytest
from lean4py.topology import (
    TopologicalSpace, MetricSpace, ContinuousFunction,
    Compactness, Connectedness, HausdorffSpace, OpenMap, ClosedMap
)


class TestTopologicalSpace:
    """Test general topology."""

    def test_creation(self):
        points = {1, 2, 3}
        open_sets = {frozenset(), frozenset({1}), frozenset(points)}
        space = TopologicalSpace(points, open_sets)
        assert len(space.points) == 3

    def test_is_open(self):
        points = {1, 2, 3}
        open_sets = {frozenset(), frozenset({1}), frozenset(points)}
        space = TopologicalSpace(points, open_sets)
        assert space.is_open({1}) is True
        assert space.is_open({2}) is False

    def test_interior(self):
        points = {1, 2, 3}
        open_sets = {frozenset(), frozenset({1}), frozenset(points)}
        space = TopologicalSpace(points, open_sets)
        interior = space.interior({1, 2})
        assert 1 in interior
        assert 2 not in interior

    def test_closure(self):
        points = {1, 2, 3}
        open_sets = {frozenset(), frozenset({1}), frozenset(points)}
        space = TopologicalSpace(points, open_sets)
        closure = space.closure({2})
        assert 2 in closure

    def test_boundary(self):
        points = {1, 2, 3}
        open_sets = {frozenset(), frozenset({1}), frozenset(points)}
        space = TopologicalSpace(points, open_sets)
        boundary = space.boundary({1})
        assert 1 in boundary

    def test_is_closed(self):
        points = {1, 2, 3}
        open_sets = {frozenset(), frozenset({1}), frozenset(points)}
        space = TopologicalSpace(points, open_sets)
        assert space.is_closed({2, 3}) is True

    def test_is_hausdorff(self):
        points = {1, 2}
        open_sets = {frozenset(), frozenset({1}), frozenset({2}), frozenset(points)}
        space = TopologicalSpace(points, open_sets)
        assert space.is_hausdorff() is True

    def test_is_connected(self):
        points = {1, 2, 3}
        open_sets = {frozenset(), frozenset(points)}
        space = TopologicalSpace(points, open_sets)
        assert space.is_connected() is True

    def test_is_compact_finite(self):
        points = {1, 2, 3}
        space = TopologicalSpace(points)
        assert space.is_compact() is True


class TestMetricSpace:
    """Test metric spaces."""

    def test_creation(self):
        points = {(0,), (1,), (2,)}
        def dist(x, y):
            return abs(x[0] - y[0])
        space = MetricSpace(points, dist)
        assert len(space.points) == 3

    def test_ball(self):
        points = {(0,), (1,), (2,)}
        def dist(x, y):
            return abs(x[0] - y[0])
        space = MetricSpace(points, dist)
        ball = space.ball((0,), 1.5)
        assert (0,) in ball
        assert (1,) in ball
        assert (2,) not in ball

    def test_is_metric(self):
        points = {(0,), (1,), (2,)}
        def dist(x, y):
            return abs(x[0] - y[0])
        space = MetricSpace(points, dist)
        assert space.is_metric() is True

    def test_diameter(self):
        points = {(0,), (3,), (5,)}
        def dist(x, y):
            return abs(x[0] - y[0])
        space = MetricSpace(points, dist)
        assert space.diameter() == 5.0

    def test_to_topological_space(self):
        points = {(0,), (1,), (2,)}
        def dist(x, y):
            return abs(x[0] - y[0])
        space = MetricSpace(points, dist)
        topo = space.to_topological_space()
        assert topo is not None


class TestContinuousFunction:
    """Test continuous functions."""

    def test_creation(self):
        points = {1, 2, 3}
        space = TopologicalSpace(points)
        codomain = TopologicalSpace(points)
        f = lambda x: x
        func = ContinuousFunction(space, codomain, f)
        assert func.func(1) == 1

    def test_image(self):
        points = {1, 2, 3}
        space = TopologicalSpace(points)
        codomain = TopologicalSpace({10, 20, 30})
        f = lambda x: x * 10
        func = ContinuousFunction(space, codomain, f)
        image = func.image({1, 2})
        assert 10 in image and 20 in image

    def test_preimage(self):
        points = {1, 2, 3}
        space = TopologicalSpace(points)
        codomain = TopologicalSpace({10, 20, 30})
        f = lambda x: x * 10
        func = ContinuousFunction(space, codomain, f)
        preimage = func.preimage({20, 30})
        assert 2 in preimage and 3 in preimage


class TestCompactness:
    """Test compactness properties."""

    def test_is_compact(self):
        points = {1, 2, 3}
        space = TopologicalSpace(points)
        assert Compactness.is_compact(space) is True

    def test_heine_borel(self):
        points = {(0,), (1,), (2,)}
        def dist(x, y):
            return abs(x[0] - y[0])
        space = MetricSpace(points, dist)
        assert Compactness.heine_borel(space) is True


class TestConnectedness:
    """Test connectedness properties."""

    def test_is_connected(self):
        points = {1, 2, 3}
        space = TopologicalSpace(points)
        assert Connectedness.is_connected(space) is True


class TestHausdorffSpace:
    """Test Hausdorff spaces."""

    def test_creation(self):
        points = {1, 2}
        open_sets = {frozenset(), frozenset({1}), frozenset({2}), frozenset(points)}
        space = HausdorffSpace(points, open_sets)
        assert space.is_hausdorff() is True

    def test_not_hausdorff_raises(self):
        points = {1, 2}
        open_sets = {frozenset(), frozenset(points)}
        with pytest.raises(ValueError):
            HausdorffSpace(points, open_sets)


class TestOpenMap:
    """Test open maps."""

    def test_is_open_map(self):
        points = {1, 2}
        open_sets = {frozenset(), frozenset({1}), frozenset(points)}
        domain = TopologicalSpace(points, open_sets)
        codomain = TopologicalSpace(points, open_sets)
        f = lambda x: x
        func = ContinuousFunction(domain, codomain, f)
        assert OpenMap.is_open_map(func) is True


class TestClosedMap:
    """Test closed maps."""

    def test_is_closed_map(self):
        points = {1, 2}
        open_sets = {frozenset(), frozenset({1}), frozenset(points)}
        domain = TopologicalSpace(points, open_sets)
        codomain = TopologicalSpace(points, open_sets)
        f = lambda x: x
        func = ContinuousFunction(domain, codomain, f)
        assert ClosedMap.is_closed_map(func) is True
