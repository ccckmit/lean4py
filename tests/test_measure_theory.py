"""Tests for measure_theory module."""

import pytest
from lean4py.measure_theory import (
    SigmaAlgebra, MeasurableSpace, Measure, LebesgueMeasure,
    MeasurableFunction, SimpleFunction, LebesgueIntegral,
    ProbabilityMeasure, BorelSigmaAlgebra
)
from lean4py.topology import TopologicalSpace


class TestSigmaAlgebra:
    """Test σ-algebra."""

    def test_creation(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        assert len(sigma.sets) >= 2

    def test_is_in(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        assert sigma.is_in(set()) is True
        assert sigma.is_in({1, 2, 3}) is True

    def test_complement(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        complement = sigma.complement({1})
        assert 1 not in complement
        assert 2 in complement

    def test_is_sigma_algebra(self):
        universe = {1, 2}
        sigma = SigmaAlgebra(universe)
        assert sigma.is_sigma_algebra() is True

    def test_union(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        result = sigma.union({1}, {2})
        assert result is not None

    def test_intersection(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        result = sigma.intersection({1, 2}, {2, 3})
        assert result is not None


class TestMeasurableSpace:
    """Test measurable space."""

    def test_creation(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        space = MeasurableSpace(universe, sigma)
        assert space.sigma_algebra is sigma

    def test_is_measurable(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        space = MeasurableSpace(universe, sigma)
        assert space.is_measurable(set()) is True


class TestMeasure:
    """Test measure."""

    def test_creation(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        space = MeasurableSpace(universe, sigma)
        measure = Measure(space)
        assert measure(space.universe) >= 0

    def test_empty_set(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        space = MeasurableSpace(universe, sigma)
        measure = Measure(space)
        assert measure(set()) == 0.0

    def test_is_measure(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        space = MeasurableSpace(universe, sigma)
        measure = Measure(space)
        assert measure.is_measure() is True

    def test_is_finite(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        space = MeasurableSpace(universe, sigma)
        measure = Measure(space)
        assert measure.is_finite() is True


class TestLebesgueMeasure:
    """Test Lebesgue measure."""

    def test_creation(self):
        lebesgue = LebesgueMeasure()
        assert lebesgue is not None

    def test_interval_length(self):
        lebesgue = LebesgueMeasure()
        # Use points that exist in the LebesgueMeasure's universe
        interval = {0, 1}
        length = lebesgue(interval)
        assert length >= 0

    def test_empty_set(self):
        lebesgue = LebesgueMeasure()
        assert lebesgue(set()) == 0.0


class TestMeasurableFunction:
    """Test measurable functions."""

    def test_creation(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        domain = MeasurableSpace(universe, sigma)
        codomain = MeasurableSpace({10, 20, 30}, sigma)
        f = lambda x: x * 10
        func = MeasurableFunction(domain, codomain, f)
        assert func.func(1) == 10

    def test_is_measurable(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        domain = MeasurableSpace(universe, sigma)
        codomain = MeasurableSpace(universe, sigma)
        f = lambda x: x
        func = MeasurableFunction(domain, codomain, f)
        assert func.is_measurable() is True


class TestSimpleFunction:
    """Test simple functions."""

    def test_creation(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        space = MeasurableSpace(universe, sigma)
        pairs = [(1.0, {1}), (2.0, {2, 3})]
        sf = SimpleFunction(pairs, space)
        assert sf.evaluate(1) == 1.0

    def test_evaluate(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        space = MeasurableSpace(universe, sigma)
        pairs = [(1.0, {1}), (2.0, {2, 3})]
        sf = SimpleFunction(pairs, space)
        assert sf.evaluate(2) == 2.0

    def test_is_measurable(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        space = MeasurableSpace(universe, sigma)
        pairs = [(1.0, {1}), (2.0, {2, 3})]
        sf = SimpleFunction(pairs, space)
        assert sf.is_measurable() is True


class TestLebesgueIntegral:
    """Test Lebesgue integral."""

    def test_of_simple(self):
        universe = {1, 2}
        sigma = SigmaAlgebra(universe)
        space = MeasurableSpace(universe, sigma)
        pairs = [(1.0, {1}), (2.0, {2})]
        sf = SimpleFunction(pairs, space)
        integral = LebesgueIntegral.of_simple(sf)
        assert integral >= 0

    def test_of_positive(self):
        universe = {1, 2}
        sigma = SigmaAlgebra(universe)
        space = MeasurableSpace(universe, sigma)
        f = lambda x: 1.0 if x == 1 else 2.0
        integral = LebesgueIntegral.of_positive(f, space, [{1}, {2}])
        assert integral >= 0


class TestProbabilityMeasure:
    """Test probability measure."""

    def test_creation(self):
        universe = {1, 2, 3}
        sigma = SigmaAlgebra(universe)
        space = MeasurableSpace(universe, sigma)
        prob = ProbabilityMeasure(space, lambda s: len(s) / 3.0)
        assert prob(space.universe) == 1.0


class TestBorelSigmaAlgebra:
    """Test Borel σ-algebra."""

    def test_from_topology(self):
        points = {1, 2, 3}
        open_sets = {frozenset(), frozenset({1}), frozenset(points)}
        topo = TopologicalSpace(points, open_sets)
        borel = BorelSigmaAlgebra.from_topology(topo)
        assert borel is not None
