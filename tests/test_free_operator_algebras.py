"""Tests for free_operator_algebras module (v1.17)."""
import pytest
from lean4py.free_operator_algebras import (
    FreeGroup, FreeGroupCStarAlgebra, ReducedFreeGroupCStar,
    FreeGroupVonNeumannAlgebra, II1Factor, FreeProductCStarAlgebra,
    AmalgamatedFreeProduct, ReducedFreeProduct, FourierTransformOnGroups,
    PlancherelTheorem, GroupCStarAlgebra, CrossedProduct
)


class TestFreeGroup:
    def test_creation(self):
        fg = FreeGroup(3)
        assert fg.rank == 3
        assert len(fg.generators) == 3

    def test_reduced_word_empty(self):
        fg = FreeGroup(2)
        assert fg.reduced_word([]) == []

    def test_reduced_word_no_reduction(self):
        fg = FreeGroup(2)
        result = fg.reduced_word(["g1", "g2"])
        assert result == ["g1", "g2"]

    def test_reduced_word_with_inverse_cancel(self):
        fg = FreeGroup(2)
        result = fg.reduced_word(["g1", "g1-1"])
        assert result == []

    def test_word_length(self):
        fg = FreeGroup(2)
        assert fg.word_length(["g1", "g2", "g1-1"]) == 3
        assert fg.word_length(["g1", "g1-1", "g2"]) == 1

    def test_inverse(self):
        fg = FreeGroup(2)
        result = fg.inverse(["g1", "g2"])
        assert len(result) == 2


class TestFreeGroupCStarAlgebra:
    def test_creation(self):
        fg = FreeGroup(3)
        cstar = FreeGroupCStarAlgebra(fg)
        assert cstar.free_group.rank == 3

    def test_is_full(self):
        fg = FreeGroup(2)
        cstar = FreeGroupCStarAlgebra(fg)
        assert cstar.is_full() is True

    def test_unitary_generator(self):
        fg = FreeGroup(3)
        cstar = FreeGroupCStarAlgebra(fg)
        result = cstar.unitary_generator(1)
        assert result == "u_1"

    def test_reduced_c_star_algebra(self):
        fg = FreeGroup(2)
        cstar = FreeGroupCStarAlgebra(fg)
        result = cstar.reduced_c_star_algebra()
        assert isinstance(result, ReducedFreeGroupCStar)

    def test_maximal_regular_representation(self):
        fg = FreeGroup(2)
        cstar = FreeGroupCStarAlgebra(fg)
        result = cstar.maximal_regular_representation()
        assert result == "λ_F"


class TestReducedFreeGroupCStar:
    def test_creation(self):
        fg = FreeGroup(2)
        rcstar = ReducedFreeGroupCStar(fg)
        assert rcstar.free_group.rank == 2

    def test_left_regular_representation(self):
        fg = FreeGroup(2)
        rcstar = ReducedFreeGroupCStar(fg)
        result = rcstar.left_regular_representation(["g1", "g2"])
        assert isinstance(result, str)


class TestFreeGroupVonNeumannAlgebra:
    def test_creation(self):
        fg = FreeGroup(2)
        vn = FreeGroupVonNeumannAlgebra(fg)
        assert vn.free_group.rank == 2

    def test_has_property_T_true(self):
        fg = FreeGroup(2)
        vn = FreeGroupVonNeumannAlgebra(fg)
        assert vn.has_property_T() is True

    def test_has_property_T_false(self):
        fg = FreeGroup(1)
        vn = FreeGroupVonNeumannAlgebra(fg)
        assert vn.has_property_T() is False

    def test_is_hermitian(self):
        fg = FreeGroup(2)
        vn = FreeGroupVonNeumannAlgebra(fg)
        assert vn.is_hermitian() is True

    def test_commutant(self):
        fg = FreeGroup(2)
        vn = FreeGroupVonNeumannAlgebra(fg)
        result = vn.commutant()
        assert isinstance(result, FreeGroupVonNeumannAlgebra)


class TestII1Factor:
    def test_creation(self):
        f = II1Factor("test")
        assert f.name == "test"

    def test_set_trace(self):
        f = II1Factor()
        f.set_trace(lambda x: 1.0)
        assert f.trace is not None

    def test_trace_property(self):
        f = II1Factor()
        f.set_trace(lambda x: 2.0)
        assert f.trace_property("x") == 2.0

    def test_polar_decomposition(self):
        f = II1Factor()
        u, pos = f.polar_decomposition("x")
        assert u == "x"
        assert pos == "|x|"

    def test_has_gamma_2_property(self):
        f = II1Factor()
        assert f.has_gamma_2_property() is True


class TestFreeProductCStarAlgebra:
    def test_creation(self):
        fp = FreeProductCStarAlgebra("A", "B")
        assert fp.left == "A"
        assert fp.right == "B"

    def test_universal_property(self):
        fp = FreeProductCStarAlgebra("A", "B")
        assert fp.universal_property() is True

    def test_reduced_free_product(self):
        fp = FreeProductCStarAlgebra("A", "B")
        result = fp.reduced_free_product()
        assert isinstance(result, ReducedFreeProduct)


class TestAmalgamatedFreeProduct:
    def test_creation(self):
        afp = AmalgamatedFreeProduct("A", "B", "C")
        assert afp.left == "A"
        assert afp.right == "B"
        assert afp.amalgam == "C"

    def test_is_free(self):
        afp = AmalgamatedFreeProduct("A", "B", "C")
        assert afp.is_free() is True


class TestReducedFreeProduct:
    def test_creation(self):
        rfp = ReducedFreeProduct("A", "B")
        assert rfp.left == "A"
        assert rfp.right == "B"

    def test_conditional_expectation(self):
        rfp = ReducedFreeProduct("A", "B")
        ce = rfp.conditional_expectation()
        assert callable(ce)


class TestFourierTransformOnGroups:
    def test_creation(self):
        ft = FourierTransformOnGroups("G")
        assert ft.group == "G"

    def test_transform(self):
        ft = FourierTransformOnGroups("G")
        f_hat = ft.transform(lambda x: x)
        assert callable(f_hat)

    def test_inverse_transform(self):
        ft = FourierTransformOnGroups("G")
        f = ft.inverse_transform(lambda x: x)
        assert callable(f)

    def test_plankrel_measure(self):
        ft = FourierTransformOnGroups("G")
        result = ft.plankrel_measure()
        assert result == "measure"


class TestPlancherelTheorem:
    def test_creation(self):
        pt = PlancherelTheorem("G")
        assert pt.group == "G"

    def test_is_unimodular(self):
        pt = PlancherelTheorem("G")
        assert pt.is_unimodular() is True

    def test_compute_norm_L2(self):
        pt = PlancherelTheorem("G")
        result = pt.compute_norm_L2(lambda x: x)
        assert isinstance(result, float)

    def test_plankrel_formula(self):
        pt = PlancherelTheorem("G")
        result = pt.plankrel_formula(lambda x: x, lambda x: x)
        assert isinstance(result, float)


class TestGroupCStarAlgebra:
    def test_creation_locally_compact(self):
        gc = GroupCStarAlgebra("G", True)
        assert gc.group == "G"
        assert gc.locally_compact is True

    def test_creation_not_locally_compact(self):
        gc = GroupCStarAlgebra("G", False)
        assert gc.locally_compact is False

    def test_universal_representation(self):
        gc = GroupCStarAlgebra("G")
        result = gc.universal_representation()
        assert result == "λ⊗ρ"

    def test_reduced_representation(self):
        gc = GroupCStarAlgebra("G")
        result = gc.reduced_representation()
        assert result == "λ"


class TestCrossedProduct:
    def test_creation(self):
        cp = CrossedProduct("G", "A", lambda x: x)
        assert cp.group == "G"
        assert cp.algebra == "A"

    def test_covariance_algebra(self):
        cp = CrossedProduct("G", "A", lambda x: x)
        result = cp.covariance_algebra()
        assert result == "A ⋊ G"

    def test_is_outer_action(self):
        cp = CrossedProduct("G", "A", lambda x: x)
        assert cp.is_outer_action() is True