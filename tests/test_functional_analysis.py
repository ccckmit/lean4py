"""Tests for functional_analysis module."""

import pytest
import math
from lean4py.functional_analysis import (
    NormedSpace, BanachSpace, InnerProductSpace, HilbertSpace,
    BoundedOperator, DualSpace, OperatorNorm
)
from lean4py.topology import MetricSpace


class TestNormedSpace:
    """Test normed spaces."""

    def test_creation(self):
        space = NormedSpace(3)
        assert space.dim == 3

    def test_norm(self):
        space = NormedSpace(2)
        x = (3.0, 4.0)
        assert abs(space.norm(x) - 5.0) < 1e-10

    def test_is_normed(self):
        space = NormedSpace(2)
        x = (1.0, 0.0)
        y = (0.0, 1.0)
        assert space.is_normed(x, y) is True

    def test_is_complete(self):
        space = NormedSpace(2)
        assert space.is_complete() is True

    def test_to_topological_space(self):
        space = NormedSpace(2)
        topo = space.to_topological_space()
        assert topo is not None


class TestBanachSpace:
    """Test Banach spaces."""

    def test_creation(self):
        space = BanachSpace(3)
        assert space.dim == 3

    def test_is_banach(self):
        space = BanachSpace(2)
        assert space.is_banach() is True


class TestInnerProductSpace:
    """Test inner product spaces."""

    def test_creation(self):
        space = InnerProductSpace(3)
        assert space.dim == 3

    def test_inner(self):
        space = InnerProductSpace(2)
        x = (1.0, 2.0)
        y = (3.0, 4.0)
        assert space.inner(x, y) == 11.0  # 1*3 + 2*4

    def test_norm_from_inner(self):
        space = InnerProductSpace(2)
        x = (3.0, 4.0)
        assert abs(space.norm(x) - 5.0) < 1e-10

    def test_is_inner_product(self):
        space = InnerProductSpace(2)
        x = (1.0, 0.0)
        y = (0.0, 1.0)
        z = (1.0, 1.0)
        assert space.is_inner_product(x, y, z) is True

    def test_angle(self):
        space = InnerProductSpace(2)
        x = (1.0, 0.0)
        y = (0.0, 1.0)
        assert abs(space.angle(x, y) - math.pi/2) < 1e-10


class TestHilbertSpace:
    """Test Hilbert spaces."""

    def test_creation(self):
        space = HilbertSpace(3)
        assert space.dim == 3

    def test_is_hilbert(self):
        space = HilbertSpace(2)
        assert space.is_hilbert() is True

    def test_projection(self):
        space = HilbertSpace(2)
        x = (3.0, 4.0)
        basis = [(1.0, 0.0)]
        proj = space.projection(x, basis)
        assert len(proj) == 2

    def test_gram_schmidt(self):
        space = HilbertSpace(2)
        vectors = [(1.0, 1.0), (1.0, 0.0)]
        result = space.gram_schmidt(vectors)
        assert len(result) >= 1


class TestBoundedOperator:
    """Test bounded linear operators."""

    def test_creation(self):
        domain = NormedSpace(2)
        codomain = NormedSpace(2)
        op = BoundedOperator(domain, codomain)
        assert op.domain is domain
        assert op.codomain is codomain

    def test_apply(self):
        domain = NormedSpace(2)
        codomain = NormedSpace(2)
        op = BoundedOperator(domain, codomain)
        x = (2.0, 3.0)
        result = op.apply(x)
        assert len(result) == 2

    def test_operator_norm(self):
        domain = NormedSpace(2)
        codomain = NormedSpace(2)
        op = BoundedOperator(domain, codomain)
        norm = op.operator_norm()
        assert norm >= 0

    def test_is_bounded(self):
        domain = NormedSpace(2)
        codomain = NormedSpace(2)
        op = BoundedOperator(domain, codomain)
        assert op.is_bounded() is True


class TestDualSpace:
    """Test dual spaces."""

    def test_riesz_representation(self):
        space = HilbertSpace(2)
        functional = lambda x: x[0] if len(x) > 0 else 0.0
        result = DualSpace.riesz_representation(space, functional)
        assert len(result) == 2


class TestOperatorNorm:
    """Test operator norm properties."""

    def test_is_norm(self):
        domain = NormedSpace(2)
        codomain = NormedSpace(2)
        op = BoundedOperator(domain, codomain)
        assert OperatorNorm.is_norm(op) is True
