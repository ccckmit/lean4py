"""Tests for two_category module (v1.20)."""
import pytest
from lean4py.two_category import (
    TwoCategory, Cat, DoubleCategory, Bicategory, TwoMorphism,
    AdjunctionIn2Category, KanExtension2Category, LaxFunctor, Strict2Category,
    FunctorCategory
)


class TestTwoCategory:
    def test_creation(self):
        tc = TwoCategory()
        assert tc.objects == []

    def test_add_object(self):
        tc = TwoCategory()
        tc.add_object("X")
        assert "X" in tc.objects

    def test_add_one_morphism(self):
        tc = TwoCategory()
        tc.add_one_morphism("X", "Y", "f")
        assert "f" in tc.hom_one("X", "Y")

    def test_hom_two(self):
        tc = TwoCategory()
        result = tc.hom_two("f", "g")
        assert result is None

    def test_vertical_composition(self):
        tc = TwoCategory()
        result = tc.vertical_composition("alpha", "beta")
        assert result == "composition"

    def test_horizontal_composition(self):
        tc = TwoCategory()
        result = tc.horizontal_composition("f", "g")
        assert result == "hcomposition"

    def test_interchange_law(self):
        tc = TwoCategory()
        assert tc.interchange_law() is True


class TestCat:
    def test_creation(self):
        c = Cat()
        assert c.categories == []

    def test_creation_with_categories(self):
        c = Cat(["C", "D"])
        assert len(c.categories) == 2

    def test_add_category(self):
        c = Cat()
        c.add_category("E")
        assert "E" in c.categories

    def test_identity_two_morphism(self):
        c = Cat()
        result = c.identity_two_morphism("F")
        assert "F" in result

    def test_functor_category(self):
        c = Cat()
        fc = c.functor_category("C", "D")
        assert isinstance(fc, FunctorCategory)
        assert fc.source == "C"


class TestFunctorCategory:
    def test_creation(self):
        fc = FunctorCategory("C", "D")
        assert fc.source == "C"
        assert fc.target == "D"

    def test_dimension(self):
        fc = FunctorCategory("C", "D")
        result = fc.dimension()
        assert result == 0


class TestDoubleCategory:
    def test_creation(self):
        dc = DoubleCategory()
        assert dc.objects == []

    def test_add_object(self):
        dc = DoubleCategory()
        dc.add_object("X")
        assert "X" in dc.objects

    def test_add_cell(self):
        dc = DoubleCategory()
        dc.add_cell("cell")
        assert "cell" in dc.cells

    def test_source_and_target(self):
        dc = DoubleCategory()
        dc.add_object("X")
        result = dc.source_and_target("cell")
        assert len(result) == 4


class TestBicategory:
    def test_creation(self):
        b = Bicategory("B")
        assert b.name == "B"
        assert b.objects == []

    def test_add_object(self):
        b = Bicategory()
        b.add_object("X")
        assert "X" in b.objects

    def test_associator(self):
        b = Bicategory()
        result = b.associator("f", "g", "h")
        assert "f" in result and "g" in result and "h" in result

    def test_left_unitor(self):
        b = Bicategory()
        result = b.left_unitor("X", "f")
        assert "f" in result

    def test_right_unitor(self):
        b = Bicategory()
        result = b.right_unitor("f", "X")
        assert "f" in result

    def test_pentagon_identity(self):
        b = Bicategory()
        assert b.pentagon_identity() is True

    def test_triangle_identity(self):
        b = Bicategory()
        assert b.triangle_identity() is True


class TestTwoMorphism:
    def test_creation(self):
        tm = TwoMorphism("f", "g", "alpha")
        assert tm.source == "f"
        assert tm.target == "g"
        assert tm.data == "alpha"

    def test_source_morphism(self):
        tm = TwoMorphism("f", "g", "alpha")
        assert tm.source_morphism() == "f"

    def test_target_morphism(self):
        tm = TwoMorphism("f", "g", "alpha")
        assert tm.target_morphism() == "g"

    def test_is_invertible(self):
        tm = TwoMorphism("f", "g", "alpha")
        assert tm.is_invertible() is False


class TestAdjunctionIn2Category:
    def test_creation(self):
        adj = AdjunctionIn2Category("L", "R", "eta", "eps")
        assert adj.left == "L"
        assert adj.right == "R"

    def test_triangle_identities(self):
        adj = AdjunctionIn2Category("L", "R", "eta", "eps")
        assert adj.triangle_identities() is True

    def test_mate(self):
        adj = AdjunctionIn2Category("L", "R", "eta", "eps")
        result = adj.mate("f")
        assert result == "f"


class TestKanExtension2Category:
    def test_creation(self):
        ke = KanExtension2Category("diagram", "functor")
        assert ke.diagram == "diagram"
        assert ke.functor == "functor"

    def test_left_kan_extension(self):
        ke = KanExtension2Category("diagram", "functor")
        result = ke.left_kan_extension()
        assert "Lan" in result

    def test_right_kan_extension(self):
        ke = KanExtension2Category("diagram", "functor")
        result = ke.right_kan_extension()
        assert "Ran" in result

    def test_universal_property(self):
        ke = KanExtension2Category("diagram", "functor")
        assert ke.universal_property() is True


class TestLaxFunctor:
    def test_creation(self):
        lf = LaxFunctor("C", "D")
        assert lf.source == "C"
        assert lf.target == "D"

    def test_on_objects(self):
        lf = LaxFunctor("C", "D")
        result = lf.on_objects("X")
        assert result == "X"

    def test_on_morphisms(self):
        lf = LaxFunctor("C", "D")
        result = lf.on_morphisms("f")
        assert result == "f"

    def test_on_2morphisms(self):
        lf = LaxFunctor("C", "D")
        result = lf.on_2morphisms("alpha")
        assert result == "alpha"

    def test_preserves_composition(self):
        lf = LaxFunctor("C", "D")
        assert lf.preserves_composition() is True


class TestStrict2Category:
    def test_creation(self):
        sc = Strict2Category()
        assert sc.objects == []

    def test_strict_associativity(self):
        sc = Strict2Category()
        assert sc.strict_associativity() is True

    def test_strict_unitality(self):
        sc = Strict2Category()
        assert sc.strict_unitality() is True