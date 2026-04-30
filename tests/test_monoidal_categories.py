"""Tests for monoidal_categories module."""
import pytest
from lean4py.monoidal_categories import (
    MonoidalCategory,
    SymmetricMonoidalCategory,
    ClosedMonoidalCategory,
    BraidedMonoidalCategory,
    RigidCategory,
    TensorProduct,
    DualObject,
    EnrichedCategory,
    CoCartesianMonoidalCategory,
    CartesianMonoidalCategory,
    MonoidalFunctor,
    LaxMonoidalFunctor,
)


class TestMonoidalCategory:
    def test_creation(self):
        mc = MonoidalCategory()
        assert mc.objects == []

    def test_add_object(self):
        mc = MonoidalCategory()
        mc.add_object("A")
        assert "A" in mc.objects

    def test_tensor_product(self):
        mc = MonoidalCategory()
        result = mc.tensor_product("A", "B")
        assert result == "A⊗B"

    def test_unit_object(self):
        mc = MonoidalCategory()
        assert mc.unit_object() == "I"

    def test_associator(self):
        mc = MonoidalCategory()
        alpha = mc.associator("A", "B", "C")
        assert alpha("test") == "test"

    def test_left_unitor(self):
        mc = MonoidalCategory()
        lam = mc.left_unitor("A")
        assert lam("x") == "x"

    def test_right_unitor(self):
        mc = MonoidalCategory()
        rho = mc.right_unitor("A")
        assert rho("x") == "x"

    def test_is_monoidal(self):
        mc = MonoidalCategory()
        assert mc.is_monoidal() is True

    def test_tensor_of_morphisms(self):
        mc = MonoidalCategory()
        f = lambda x: x + 1
        g = lambda x: x * 2
        h = mc.tensor_of_morphisms(f, g)
        assert h(5) == (6, 10)


class TestSymmetricMonoidalCategory:
    def test_creation(self):
        smc = SymmetricMonoidalCategory()
        assert smc.objects == []

    def test_braiding(self):
        smc = SymmetricMonoidalCategory()
        sigma = smc.braiding("A", "B")
        assert sigma("x") == "x"

    def test_set_braiding(self):
        smc = SymmetricMonoidalCategory()
        custom = lambda x: f"braided({x})"
        smc.set_braiding("A", "B", custom)
        assert smc.braiding("A", "B")("x") == "braided(x)"

    def test_is_symmetric(self):
        smc = SymmetricMonoidalCategory()
        assert smc.is_symmetric() is True

    def test_hexagon_identity(self):
        smc = SymmetricMonoidalCategory()
        assert smc.hexagon_identity() is True


class TestClosedMonoidalCategory:
    def test_creation(self):
        cmc = ClosedMonoidalCategory()
        assert cmc.internal_hom == {}

    def test_internal_hom_object(self):
        cmc = ClosedMonoidalCategory()
        ih = cmc.internal_hom_object("A")
        assert "A" in ih

    def test_evaluation_map(self):
        cmc = ClosedMonoidalCategory()
        ev = cmc.evaluation_map("A", "B")
        assert ev("x") == "x"

    def test_currying(self):
        cmc = ClosedMonoidalCategory()
        f = lambda x, y: x + y
        curried = cmc.currying(f)
        assert curried(2)(3) == 5

    def test_is_closed(self):
        cmc = ClosedMonoidalCategory()
        assert cmc.is_closed() is True


class TestBraidedMonoidalCategory:
    def test_creation(self):
        bmc = BraidedMonoidalCategory()
        assert bmc.objects == []

    def test_hexagon_1(self):
        bmc = BraidedMonoidalCategory()
        assert bmc.hexagon_1() is True

    def test_hexagon_2(self):
        bmc = BraidedMonoidalCategory()
        assert bmc.hexagon_2() is True


class TestRigidCategory:
    def test_creation(self):
        rc = RigidCategory()
        assert rc.duals == {}

    def test_dual_of(self):
        rc = RigidCategory()
        assert rc.dual_of("A") == "A*"

    def test_set_dual(self):
        rc = RigidCategory()
        rc.set_dual("A", "Adual")
        assert rc.dual_of("A") == "Adual"

    def test_evaluation(self):
        rc = RigidCategory()
        ev = rc.evaluation("A")
        assert ev("x") == "I"

    def test_coevaluation(self):
        rc = RigidCategory()
        coev = rc.coevaluation("A")
        assert coev("x") == "A⊗A*"

    def test_trace(self):
        rc = RigidCategory()
        tr = rc.trace(lambda x: x)
        assert tr == "trace"


class TestTensorProduct:
    def test_num_factors(self):
        tp = TensorProduct(["A", "B", "C"])
        assert tp.num_factors() == 3

    def test_is_unit(self):
        tp_empty = TensorProduct([])
        assert tp_empty.is_unit() is True
        tp_nonempty = TensorProduct(["A"])
        assert tp_nonempty.is_unit() is False


class TestDualObject:
    def test_creation(self):
        do = DualObject("A", "A*")
        assert do.original == "A"
        assert do.dual == "A*"

    def test_evaluation_map(self):
        do = DualObject("A", "A*")
        ev = do.evaluation_map()
        assert ev("x") == "I"

    def test_coevaluation_map(self):
        do = DualObject("A", "A*")
        coev = do.coevaluation_map()
        assert coev("x") == ("A", "A*")


class TestEnrichedCategory:
    def test_creation(self):
        base = MonoidalCategory()
        ec = EnrichedCategory(base)
        assert ec.base is base
        assert ec.objects == []

    def test_add_object(self):
        base = MonoidalCategory()
        ec = EnrichedCategory(base)
        ec.add_object("X")
        assert "X" in ec.objects

    def test_hom_object_default(self):
        base = MonoidalCategory()
        ec = EnrichedCategory(base)
        assert ec.hom_object("X", "Y") == "I"

    def test_set_hom_object(self):
        base = MonoidalCategory()
        ec = EnrichedCategory(base)
        ec.set_hom_object("X", "Y", "V_XY")
        assert ec.hom_object("X", "Y") == "V_XY"


class TestCoCartesianMonoidalCategory:
    def test_coproduct(self):
        cc = CoCartesianMonoidalCategory()
        assert cc.coproduct("A", "B") == "A⊕B"

    def test_initial_object(self):
        cc = CoCartesianMonoidalCategory()
        assert cc.initial_object() == "0"


class TestCartesianMonoidalCategory:
    def test_product(self):
        cc = CartesianMonoidalCategory()
        assert cc.product("A", "B") == "A×B"

    def test_terminal_object(self):
        cc = CartesianMonoidalCategory()
        assert cc.terminal_object() == "1"


class TestMonoidalFunctor:
    def test_creation(self):
        source = MonoidalCategory()
        target = MonoidalCategory()
        obj_map = lambda x: f"F({x})"
        mor_map = lambda f: f
        mf = MonoidalFunctor(source, target, obj_map, mor_map)
        assert mf.source is source
        assert mf.target is target

    def test_on_objects(self):
        source = MonoidalCategory()
        target = MonoidalCategory()
        mf = MonoidalFunctor(source, target, lambda x: x.upper(), lambda f: f)
        assert mf.on_objects("a") == "A"

    def test_preserves_tensor(self):
        source = MonoidalCategory()
        target = MonoidalCategory()
        mf = MonoidalFunctor(source, target, lambda x: x, lambda f: f)
        assert mf.preserves_tensor() is True


class TestLaxMonoidalFunctor:
    def test_creation(self):
        source = MonoidalCategory()
        target = MonoidalCategory()
        lmf = LaxMonoidalFunctor(source, target, lambda x: x.upper())
        assert lmf.source is source
        assert lmf.target is target

    def test_unit_constraint(self):
        source = MonoidalCategory()
        target = MonoidalCategory()
        lmf = LaxMonoidalFunctor(source, target, lambda x: x)
        assert lmf.unit_constraint()("x") == "x"

    def test_tensor_constraint(self):
        source = MonoidalCategory()
        target = MonoidalCategory()
        lmf = LaxMonoidalFunctor(source, target, lambda x: x)
        assert lmf.tensor_constraint("A", "B")("x") == "x"