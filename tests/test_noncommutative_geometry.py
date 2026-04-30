"""Tests for noncommutative_geometry module."""
import pytest
from lean4py.noncommutative_geometry import (
    NoncommutativeSpace,
    SpectralTriple,
    DiracOperator,
    FredholmIndex,
    HochschildCohomology,
    CyclicCohomology,
    KHomology,
    FredholmModule,
    PseudodifferentialOperator,
    ConnesChernCharacter,
)


class TestNoncommutativeSpace:
    def test_creation(self):
        ns = NoncommutativeSpace("C*_alg", 100)
        assert ns.algebra == "C*_alg"
        assert ns.hilbert_space_dim == 100

    def test_set_spectral_triple(self):
        ns = NoncommutativeSpace("C*_alg", 100)
        triple = SpectralTriple("C*_alg", "H", lambda x: x)
        ns.set_spectral_triple(triple)
        assert ns.spectral_triple is triple

    def test_dimension(self):
        ns = NoncommutativeSpace("C*_alg", 100)
        assert ns.dimension() == 0
        triple = SpectralTriple("C*_alg", "H", lambda x: x)
        ns.set_spectral_triple(triple)
        assert ns.dimension() == 0

    def test_is_spectral(self):
        ns = NoncommutativeSpace("C*_alg", 100)
        assert ns.is_spectral() is False
        triple = SpectralTriple("C*_alg", "H", lambda x: x)
        ns.set_spectral_triple(triple)
        assert ns.is_spectral() is True


class TestSpectralTriple:
    def test_creation(self):
        alg = "C*_alg"
        H = "Hilbert"
        D = lambda x: x
        st = SpectralTriple(alg, H, D)
        assert st.algebra == alg
        assert st.hilbert_space == H
        assert st.dirac_operator == D

    def test_dimension(self):
        st = SpectralTriple("A", "H", lambda x: x)
        assert st.dimension() == 0

    def test_get_dirac_operator(self):
        D = lambda x: x + 1
        st = SpectralTriple("A", "H", D)
        assert st.get_dirac_operator() == D

    def test_apply_dirac(self):
        st = SpectralTriple("A", "H", lambda x: x * 2)
        assert st.apply_dirac(5) == 10

    def test_commutator(self):
        st = SpectralTriple("A", "H", lambda x: x * 2)
        a = lambda psi: psi + 3
        comm = st.commutator(a)
        assert comm(5) == 3

    def test_order_one_condition(self):
        st = SpectralTriple("A", "H", lambda x: x)
        assert st.order_one_condition() is True

    def test_finiteness_condition(self):
        st = SpectralTriple("A", "H", lambda x: x)
        assert st.finiteness_condition() is True

    def test_absolute_continuity(self):
        st = SpectralTriple("A", "H", lambda x: x)
        assert st.absolute_continuity() is True

    def test_zeta_function(self):
        st = SpectralTriple("A", "H", lambda x: x)
        st._spectrum = [1.0, 2.0, 3.0]
        zeta = st.zeta_function(2.0)
        assert zeta > 0


class TestDiracOperator:
    def test_creation(self):
        D = DiracOperator("manifold", lambda x: x)
        assert D.manifold == "manifold"

    def test_kernel_dim(self):
        D = DiracOperator("manifold", lambda x: x)
        assert D.kernel_dim() == 0

    def test_cokernel_dim(self):
        D = DiracOperator("manifold", lambda x: x)
        assert D.cokernel_dim() == 0

    def test_apply(self):
        D = DiracOperator("manifold", lambda x: x * 3)
        assert D.apply(4) == 12


class TestFredholmIndex:
    def test_creation(self):
        op = lambda x: x
        idx = FredholmIndex(op)
        assert idx.operator == op

    def test_compute(self):
        op = lambda x: x
        idx = FredholmIndex(op)
        idx.kernel_dim = 2
        idx.cokernel_dim = 1
        assert idx.compute() == 1

    def test_is_fredholm(self):
        idx = FredholmIndex(lambda x: x)
        assert idx.is_fredholm() is True

    def test_Atkinson_theorem(self):
        idx = FredholmIndex(lambda x: x)
        assert idx.Atkinson_theorem() is True

    def test_perturbation_invariance(self):
        idx = FredholmIndex(lambda x: x)
        idx.kernel_dim = 1
        idx.cokernel_dim = 1
        result = idx.perturbation_invariance(lambda x: x)
        assert result == 0


class TestHochschildCohomology:
    def test_creation(self):
        hh = HochschildCohomology("algebra")
        assert hh.algebra == "algebra"

    def test_n_chains(self):
        hh = HochschildCohomology("algebra")
        chains = hh.n_chains(3)
        assert len(chains) == 3

    def test_coboundary(self):
        hh = HochschildCohomology("algebra")
        result = hh.coboundary(2, ["a", "b"])
        assert result == []

    def test_is_cocycle(self):
        hh = HochschildCohomology("algebra")
        assert hh.is_cocycle(2, lambda x: x) is True

    def test_is_coboundary(self):
        hh = HochschildCohomology("algebra")
        assert hh.is_coboundary(2, lambda x: x) is False

    def test_hh_class(self):
        hh = HochschildCohomology("algebra")
        cls = hh.hh_class(2, lambda x: x)
        assert "HH" in cls


class TestCyclicCohomology:
    def test_creation(self):
        cc = CyclicCohomology("algebra")
        assert cc.algebra == "algebra"

    def test_connes_boundary_map(self):
        cc = CyclicCohomology("algebra")
        B = cc.connes_boundary_map(2)
        assert B("x") == "x"

    def test_periodic_cyclic_complex(self):
        cc = CyclicCohomology("algebra")
        result = cc.periodic_cyclic_complex()
        assert len(result) == 2

    def test_is_cyclic(self):
        cc = CyclicCohomology("algebra")
        assert cc.is_cyclic(lambda x: x) is True

    def test_chern_character(self):
        cc = CyclicCohomology("algebra")
        ch = cc.chern_character(lambda x: x)
        assert ch == "Chern character"


class TestKHomology:
    def test_creation(self):
        space = NoncommutativeSpace("C*_alg", 100)
        kh = KHomology(space)
        assert kh.space is space

    def test_add_fredholm_module(self):
        space = NoncommutativeSpace("C*_alg", 100)
        kh = KHomology(space)
        fm = FredholmModule("A", lambda x: x, lambda y: y)
        kh.add_fredholm_module(fm)
        assert len(kh.fredholm_modules) == 1

    def test_index_pairing(self):
        space = NoncommutativeSpace("C*_alg", 100)
        kh = KHomology(space)
        fm = FredholmModule("A", lambda x: x, lambda y: y)
        result = kh.index_pairing(fm, "K_class")
        assert result == 0

    def test_thorn_equality(self):
        space = NoncommutativeSpace("C*_alg", 100)
        kh = KHomology(space)
        assert kh.thorn_equality() is True


class TestFredholmModule:
    def test_creation(self):
        fm = FredholmModule("A", lambda x: x, lambda y: y)
        assert fm.algebra == "A"

    def test_is_even(self):
        fm = FredholmModule("A", lambda x: x, lambda y: y)
        assert fm.is_even() is False

    def test_is_odd(self):
        fm = FredholmModule("A", lambda x: x, lambda y: y)
        assert fm.is_odd() is True

    def test_index(self):
        fm = FredholmModule("A", lambda x: x, lambda y: y)
        assert fm.index() == 0

    def test_pair_with_k_theory(self):
        fm = FredholmModule("A", lambda x: x, lambda y: y)
        result = fm.pair_with_k_theory("K_class")
        assert result == 0j


class TestPseudodifferentialOperator:
    def test_creation(self):
        psiDO = PseudodifferentialOperator(2, lambda x: x)
        assert psiDO.order == 2

    def test_symbol_class(self):
        psiDO = PseudodifferentialOperator(-1, lambda x: x)
        assert psiDO.symbol_class() == "S^-1"

    def test_compose_with_elliptic(self):
        psiDO1 = PseudodifferentialOperator(1, lambda x: x)
        psiDO2 = PseudodifferentialOperator(2, lambda x: x)
        comp = psiDO1.compose_with_elliptic(psiDO2)
        assert comp.order == 3

    def test_transposed_operator(self):
        psiDO = PseudodifferentialOperator(1, lambda x: x)
        trans = psiDO.transposed_operator()
        assert trans.order == psiDO.order


class TestConnesChernCharacter:
    def test_creation(self):
        space = NoncommutativeSpace("C*_alg", 100)
        cc = ConnesChernCharacter(space)
        assert cc.space is space

    def test_compute_character(self):
        space = NoncommutativeSpace("C*_alg", 100)
        cc = ConnesChernCharacter(space)
        fm = FredholmModule("A", lambda x: x, lambda y: y)
        chars = cc.compute_character(fm)
        assert len(chars) == 5

    def test_bounded_perturbation(self):
        space = NoncommutativeSpace("C*_alg", 100)
        cc = ConnesChernCharacter(space)
        assert cc.bounded_perturbation() is True

    def test_morita_invariance(self):
        space = NoncommutativeSpace("C*_alg", 100)
        cc = ConnesChernCharacter(space)
        assert cc.morita_invariance() is True