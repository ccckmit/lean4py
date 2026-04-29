"""Tests for hopf_algebra module (v1.18)."""
import pytest
from lean4py.hopf_algebra import (
    Coalgebra, Bialgebra, HopfAlgebra, GroupAlgebra, QuantumGroup,
    ModuleAlgebra, InvariantTheory, RepresentationOfHopfAlgebra,
    sl2_hopf, sl2_quantized, DualHopfAlgebra, braided_category
)


class TestCoalgebra:
    def test_creation(self):
        c = Coalgebra({"a", "b"}, lambda x: (x, x), lambda x: 1)
        assert "a" in c.carrier

    def test_is_coassociative(self):
        c = Coalgebra({"a"}, lambda x: (x, x), lambda x: 1)
        assert c.is_coassociative() is True

    def test_is_cocommutative(self):
        c = Coalgebra({"a"}, lambda x: (x, x), lambda x: 1)
        assert c.is_cocommutative() is True

    def test_sweedler_notation(self):
        c = Coalgebra({"a"}, lambda x: (x, x), lambda x: 1)
        result = c.Sweedler_notation("a")
        assert "⊗" in result


class TestBialgebra:
    def test_creation(self):
        b = Bialgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1)
        assert "a" in b.carrier

    def test_is_bialgebra(self):
        b = Bialgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1)
        assert b.is_bialgebra() is True

    def test_is_commutative(self):
        b = Bialgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1)
        assert b.is_commutative() is True

    def test_is_cocommutative(self):
        b = Bialgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1)
        assert b.is_cocommutative() is True


class TestHopfAlgebra:
    def test_creation(self):
        h = HopfAlgebra(
            {"a"}, lambda x: x, "1",
            lambda x: (x, x), lambda x: 1, lambda x: x
        )
        assert "a" in h.carrier

    def test_is_hopf(self):
        h = HopfAlgebra(
            {"a"}, lambda x: x, "1",
            lambda x: (x, x), lambda x: 1, lambda x: x
        )
        assert h.is_hopf() is True

    def test_antipode_property(self):
        h = HopfAlgebra(
            {"a"}, lambda x: x, "1",
            lambda x: (x, x), lambda x: 1, lambda x: x
        )
        assert h.antipode_property("a") is True


class TestGroupAlgebra:
    def test_creation(self):
        ga = GroupAlgebra("G")
        assert ga.group == "G"
        assert ga.field == "C"

    def test_creation_with_field(self):
        ga = GroupAlgebra("G", "R")
        assert ga.field == "R"

    def test_comultiplication(self):
        ga = GroupAlgebra("G")
        result = ga.comultiplication("g")
        assert result == ("g", "g")

    def test_counit(self):
        ga = GroupAlgebra("G")
        result = ga.counit("g")
        assert result == 1

    def test_antipode(self):
        ga = GroupAlgebra("G")
        result = ga.antipode("g")
        assert result == "g"

    def test_is_hopf(self):
        ga = GroupAlgebra("G")
        assert ga.is_hopf() is True


class TestQuantumGroup:
    def test_creation(self):
        qg = QuantumGroup("A_1", 0.5)
        assert qg.root_system == "A_1"
        assert qg.q == 0.5

    def test_is_quantized(self):
        qg1 = QuantumGroup("A_1", 0.5)
        qg2 = QuantumGroup("A_1", 1.0)
        assert qg1.is_quantized() is True
        assert qg2.is_quantized() is False

    def test_special_case(self):
        qg = QuantumGroup("A_1", 0.5)
        assert qg.special_case() == "A_1"

    def test_R_matrix(self):
        qg = QuantumGroup("A_1", 0.5)
        result = qg.R_matrix()
        assert result == "R"

    def test_quantum_PBW_basis(self):
        qg = QuantumGroup("A_1", 0.5)
        result = qg.quantum_BPBW_basis()
        assert isinstance(result, list)


class TestModuleAlgebra:
    def test_creation(self):
        ma = ModuleAlgebra("A", "H", lambda x: x)
        assert ma.algebra == "A"
        assert ma.hopf == "H"

    def test_is_module_algebra(self):
        ma = ModuleAlgebra("A", "H", lambda x: x)
        assert ma.is_module_algebra() is True

    def test_invariants(self):
        ma = ModuleAlgebra("A", "H", lambda x: x)
        result = ma.invariants()
        assert isinstance(result, list)


class TestInvariantTheory:
    def test_creation(self):
        it = InvariantTheory("A", "G")
        assert it.algebra == "A"
        assert it.group == "G"

    def test_invariants(self):
        it = InvariantTheory("A", "G")
        result = it.invariants()
        assert result == "invariant_subring"

    def test_noether_normalization(self):
        it = InvariantTheory("A", "G")
        result = it.noether_normalization()
        assert isinstance(result, list)

    def test_hilbert_series(self):
        it = InvariantTheory("A", "G")
        result = it.hilbert_series()
        assert result == "series"

    def test_primary_invariants(self):
        it = InvariantTheory("A", "G")
        result = it.primary_invariants()
        assert isinstance(result, list)

    def test_secondary_invariants(self):
        it = InvariantTheory("A", "G")
        result = it.secondary_invariants()
        assert isinstance(result, list)


class TestRepresentationOfHopfAlgebra:
    def test_creation(self):
        h = HopfAlgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1, lambda x: x)
        rh = RepresentationOfHopfAlgebra(h, "V", lambda x: x)
        assert rh.hopf == h
        assert rh.module == "V"

    def test_is_representation(self):
        h = HopfAlgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1, lambda x: x)
        rh = RepresentationOfHopfAlgebra(h, "V", lambda x: x)
        assert rh.is_representation() is True

    def test_is_simple(self):
        h = HopfAlgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1, lambda x: x)
        rh = RepresentationOfHopfAlgebra(h, "V", lambda x: x)
        assert rh.is_simple() is False

    def test_is_completely_reducible(self):
        h = HopfAlgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1, lambda x: x)
        rh = RepresentationOfHopfAlgebra(h, "V", lambda x: x)
        assert rh.is_completely_reducible() is True


class TestSl2Hopf:
    def test_sl2_hopf(self):
        h = sl2_hopf()
        assert isinstance(h, HopfAlgebra)

    def test_sl2_hopf_is_hopf(self):
        h = sl2_hopf()
        assert h.is_hopf() is True


class TestSl2Quantized:
    def test_sl2_quantized(self):
        h = sl2_quantized(0.5)
        assert isinstance(h, HopfAlgebra)

    def test_sl2_quantized_is_hopf(self):
        h = sl2_quantized(0.5)
        assert h.is_hopf() is True


class TestDualHopfAlgebra:
    def test_creation(self):
        h = HopfAlgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1, lambda x: x)
        dh = DualHopfAlgebra(h)
        assert dh.hopf == h

    def test_dual_multiplication(self):
        h = HopfAlgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1, lambda x: x)
        dh = DualHopfAlgebra(h)
        fn = dh.dual_multiplication()
        assert callable(fn)

    def test_is_hopf(self):
        h = HopfAlgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1, lambda x: x)
        dh = DualHopfAlgebra(h)
        assert dh.is_hopf() is True


class TestBraidedCategory:
    def test_creation(self):
        bc = braided_category()
        assert bc.objects == []

    def test_add_object(self):
        bc = braided_category()
        h = HopfAlgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1, lambda x: x)
        bc.add_object(h)
        assert len(bc.objects) == 1

    def test_braiding(self):
        bc = braided_category()
        h = HopfAlgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1, lambda x: x)
        br = bc.braiding(h, h)
        assert callable(br)