"""Tests for model_category module (v1.19)."""
import pytest
from lean4py.model_category import (
    ModelCategory, QuillenAdjunction, HomotopyCategory, HomotopyEquivalence,
    CWComplex, SimplicialModelCategory, WhiteheadTheorem, Cofibration, Fibration,
    WeakEquivalence, WeakFactorizationSystem, AnodyneExtension, HomotopyCoherent
)


class TestModelCategory:
    def test_creation(self):
        mc = ModelCategory()
        assert mc.objects == []

    def test_creation_with_objects(self):
        mc = ModelCategory(["A", "B"])
        assert len(mc.objects) == 2

    def test_add_weak_equivalence(self):
        mc = ModelCategory()
        mc.add_weak_equivalence("A", "B")
        assert mc.is_weak_equivalence("A", "B") is True

    def test_add_cofibration(self):
        mc = ModelCategory()
        mc.add_cofibration("A", "B")
        assert mc.is_cofibration("A", "B") is True

    def test_add_fibration(self):
        mc = ModelCategory()
        mc.add_fibration("A", "B")
        assert mc.is_fibration("A", "B") is True

    def test_has_lifting_property(self):
        mc = ModelCategory()
        assert mc.has_lifting_property("A", "B") is True

    def test_factorize(self):
        mc = ModelCategory()
        result = mc.factorize("A", "B")
        assert len(result) == 3

    def test_homotopy_category(self):
        mc = ModelCategory()
        hc = mc.homotopy_category()
        assert isinstance(hc, HomotopyCategory)


class TestCofibration:
    def test_creation(self):
        c = Cofibration("A", "B", lambda x: x)
        assert c.source == "A"
        assert c.target == "B"

    def test_is_cofibration(self):
        c = Cofibration("A", "B", lambda x: x)
        assert c.is_cofibration() is True

    def test_is_acyclic(self):
        c = Cofibration("A", "B", lambda x: x)
        assert c.is_acyclic() is False


class TestFibration:
    def test_creation(self):
        f = Fibration("A", "B", lambda x: x)
        assert f.source == "A"
        assert f.target == "B"

    def test_is_fibration(self):
        f = Fibration("A", "B", lambda x: x)
        assert f.is_fibration() is True

    def test_is_acyclic(self):
        f = Fibration("A", "B", lambda x: x)
        assert f.is_acyclic() is False


class TestWeakEquivalence:
    def test_creation(self):
        w = WeakEquivalence("A", "B", lambda x: x)
        assert w.source == "A"
        assert w.target == "B"

    def test_is_weak_equivalence(self):
        w = WeakEquivalence("A", "B", lambda x: x)
        assert w.is_weak_equivalence() is True


class TestQuillenAdjunction:
    def test_creation(self):
        qa = QuillenAdjunction(lambda x: x, lambda x: x)
        assert qa.left_adjoint is not None

    def test_preserves_cofibrations(self):
        qa = QuillenAdjunction(lambda x: x, lambda x: x)
        assert qa.preserves_cofibrations() is True

    def test_is_quillen_adjunction(self):
        qa = QuillenAdjunction(lambda x: x, lambda x: x)
        assert qa.is_quillen_adjunction() is True

    def test_derived_left_adjoint(self):
        qa = QuillenAdjunction(lambda x: x, lambda x: x)
        result = qa.derived_left_adjoint()
        assert callable(result)

    def test_derived_right_adjoint(self):
        qa = QuillenAdjunction(lambda x: x, lambda x: x)
        result = qa.derived_right_adjoint()
        assert callable(result)


class TestHomotopyCategory:
    def test_creation(self):
        mc = ModelCategory()
        hc = HomotopyCategory(mc)
        assert hc.model_category == mc

    def test_localize_at_W(self):
        mc = ModelCategory()
        hc = HomotopyCategory(mc)
        result = hc.localize_at_W()
        assert isinstance(result, HomotopyCategory)

    def test_hom_set(self):
        mc = ModelCategory()
        hc = HomotopyCategory(mc)
        result = hc.hom_set("A", "B")
        assert isinstance(result, list)


class TestHomotopyEquivalence:
    def test_creation(self):
        he = HomotopyEquivalence(lambda x: x, lambda x: x)
        assert he.forward is not None

    def test_is_homotopy_equivalence(self):
        he = HomotopyEquivalence(lambda x: x, lambda x: x)
        assert he.is_homotopy_equivalence() is True

    def test_inverse(self):
        he = HomotopyEquivalence(lambda x: x, lambda x: x)
        inv = he.inverse()
        assert isinstance(inv, HomotopyEquivalence)


class TestWeakFactorizationSystem:
    def test_creation(self):
        wfs = WeakFactorizationSystem([lambda x: x], [lambda x: x])
        assert len(wfs.left_class) == 1

    def test_factor_map(self):
        wfs = WeakFactorizationSystem([lambda x: x], [lambda x: x])
        result = wfs.factor_map(lambda x: x)
        assert len(result) == 2

    def test_has_lifting(self):
        wfs = WeakFactorizationSystem([lambda x: x], [lambda x: x])
        assert wfs.has_lifting() is True


class TestCWComplex:
    def test_creation(self):
        cwc = CWComplex()
        assert cwc.dimension == 0

    def test_add_cell(self):
        cwc = CWComplex()
        cwc.add_cell(2, "cell")
        assert 2 in cwc.cells
        assert cwc.dimension == 2

    def test_attach_cell(self):
        cwc = CWComplex()
        cwc.attach_cell(2, lambda x: x)
        assert 2 in cwc.attachments

    def test_homology(self):
        cwc = CWComplex()
        result = cwc.homology(0)
        assert isinstance(result, str)

    def test_euler_characteristic(self):
        cwc = CWComplex()
        result = cwc.euler_characteristic()
        assert isinstance(result, int)


class TestHomotopyCoherent:
    def test_creation(self):
        hc = HomotopyCoherent("category")
        assert hc.category == "category"

    def test_n_skeleton(self):
        hc = HomotopyCoherent("category")
        result = hc.n_skeleton(3)
        assert isinstance(result, str)

    def test_geometric_realization(self):
        hc = HomotopyCoherent("category")
        result = hc.geometric_realization()
        assert result == "geometric_realization"


class TestAnodyneExtension:
    def test_creation(self):
        ae = AnodyneExtension("A", "B")
        assert ae.source == "A"
        assert ae.target == "B"

    def test_is_anodyne(self):
        ae = AnodyneExtension("A", "B")
        assert ae.is_anodyne() is True


class TestSimplicialModelCategory:
    def test_creation(self):
        smc = SimplicialModelCategory()
        assert smc.objects == []

    def test_mapping_space(self):
        smc = SimplicialModelCategory()
        result = smc.mapping_space("X", "Y")
        assert result is not None

    def test_tensor(self):
        smc = SimplicialModelCategory()
        result = smc.tensor("X", "K")
        assert result == "X"

    def test_cotensor(self):
        smc = SimplicialModelCategory()
        result = smc.cotensor("X", "K")
        assert result == "X"


class TestWhiteheadTheorem:
    def test_from_CW_to_CW(self):
        from lean4py.model_category import CWComplex
        cwc1 = CWComplex(3)
        cwc2 = CWComplex(3)
        result = WhiteheadTheorem.from_CW_to_CW(lambda x: x, cwc1, cwc2)
        assert isinstance(result, bool)