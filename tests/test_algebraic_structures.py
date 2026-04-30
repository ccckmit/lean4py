"""Tests for algebraic_structures module."""

import pytest
from lean4py.algebraic_structures import (
    Module, Algebra, TensorProduct, ExactSequence, FreeModule, SimpleModule
)


class TestModule:
    """Test Module."""

    def test_creation(self):
        mod = Module(ring=0, dimension=3)
        assert mod.dim == 3

    def test_is_module(self):
        mod = Module(ring=0, dimension=2)
        add = lambda x, y: tuple(x_i + y_i for x_i, y_i in zip(x, y))
        scalar_mul = lambda c, v: tuple(c * v_i for v_i in v)
        assert mod.is_module(add, scalar_mul) is True

    def test_basis(self):
        mod = Module(ring=0, dimension=2)
        basis = mod.basis()
        assert len(basis) == 2

    def test_linear_combination(self):
        mod = Module(ring=0, dimension=2)
        coeffs = [2.0, 3.0]
        vectors = [(1.0, 0.0), (0.0, 1.0)]
        result = mod.linear_combination(coeffs, vectors)
        assert len(result) == 2


class TestAlgebra:
    """Test Algebra."""

    def test_creation(self):
        alg = Algebra(field=0, dimension=2)
        assert alg.dim == 2

    def test_multiply(self):
        alg = Algebra(field=0, dimension=2)
        x = (2.0, 3.0)
        y = (1.0, 4.0)
        result = alg.multiply(x, y)
        assert len(result) == 2

    def test_is_algebra(self):
        alg = Algebra(field=0, dimension=1)
        assert alg.is_algebra() is True

    def test_unit(self):
        alg = Algebra(field=0, dimension=2)
        unit = alg.unit()
        assert unit is not None


class TestTensorProduct:
    """Test TensorProduct."""

    def test_creation(self):
        mod1 = Module(ring=0, dimension=2)
        mod2 = Module(ring=0, dimension=3)
        tp = TensorProduct(mod1, mod2)
        assert tp.dim == 6

    def test_tensor(self):
        mod1 = Module(ring=0, dimension=2)
        mod2 = Module(ring=0, dimension=2)
        tp = TensorProduct(mod1, mod2)
        v1 = (1.0, 2.0)
        v2 = (3.0, 4.0)
        result = tp.tensor(v1, v2)
        assert len(result) == 4

    def test_is_bilinear(self):
        mod1 = Module(ring=0, dimension=2)
        mod2 = Module(ring=0, dimension=2)
        tp = TensorProduct(mod1, mod2)
        assert tp.is_bilinear() is True

    def test_dimension(self):
        mod1 = Module(ring=0, dimension=2)
        mod2 = Module(ring=0, dimension=3)
        tp = TensorProduct(mod1, mod2)
        assert tp.dimension() == 6


class TestExactSequence:
    """Test ExactSequence."""

    def test_creation(self):
        mod1 = Module(ring=0, dimension=1)
        mod2 = Module(ring=0, dimension=1)
        maps = [lambda x: x, lambda x: x]
        es = ExactSequence([mod1, mod2], maps)
        assert len(es.modules) == 2

    def test_is_exact_at(self):
        mod1 = Module(ring=0, dimension=1)
        mod2 = Module(ring=0, dimension=1)
        maps = [lambda x: x, lambda x: x]
        es = ExactSequence([mod1, mod2], maps)
        assert es.is_exact_at(0) is True

    def test_is_exact(self):
        mod1 = Module(ring=0, dimension=1)
        mod2 = Module(ring=0, dimension=1)
        maps = [lambda x: x, lambda x: x]
        es = ExactSequence([mod1, mod2], maps)
        assert es.is_exact() is True


class TestFreeModule:
    """Test FreeModule."""

    def test_creation(self):
        fm = FreeModule(ring=0, dimension=3)
        assert fm.dim == 3

    def test_is_free(self):
        fm = FreeModule(ring=0, dimension=2)
        assert fm.is_free() is True

    def test_rank(self):
        fm = FreeModule(ring=0, dimension=3)
        assert fm.rank() == 3


class TestSimpleModule:
    """Test SimpleModule."""

    def test_is_simple_true(self):
        mod = Module(ring=0, dimension=2)
        assert SimpleModule.is_simple(mod, [set(), {0, 1}]) is True

    def test_is_simple_false(self):
        mod = Module(ring=0, dimension=2)
        assert SimpleModule.is_simple(mod, [set(), {0}, {0, 1}]) is False
