"""Tests for higher_category_theory module."""
import pytest
from lean4py.higher_category_theory import (
    InfinityCategory,
    KanComplex,
    NCategory,
    WeakEquivalence,
    HomotopyPushout,
    HomotopyPullback,
    SegalCategory,
    CompleteSegalSpace,
    Anima,
    InfinityTopos,
)


class TestInfinityCategory:
    def test_creation(self):
        ic = InfinityCategory("C")
        assert ic.name == "C"
        assert ic.objects == []

    def test_add_object(self):
        ic = InfinityCategory()
        ic.add_object("X")
        assert "X" in ic.objects

    def test_hom_space(self):
        ic = InfinityCategory()
        ic.add_object("X")
        ic.add_object("Y")
        hs = ic.hom_space("X", "Y")
        assert isinstance(hs, KanComplex)

    def test_compose(self):
        ic = InfinityCategory()
        f = lambda x: x + 1
        g = lambda x: x * 2
        comp = ic.compose(f, g)
        assert comp(3) == 8

    def test_identity(self):
        ic = InfinityCategory()
        ic.add_object("X")
        idi = ic.identity("X")
        assert idi(5) == 5

    def test_is_fibrant(self):
        ic = InfinityCategory()
        assert ic.is_fibrant() is True

    def test_joyal_model_structure(self):
        ic = InfinityCategory()
        result = ic.joyal_model_structure()
        assert "Joyal" in result


class TestKanComplex:
    def test_creation(self):
        kc = KanComplex()
        assert kc.dimension == 0

    def test_add_simplex(self):
        kc = KanComplex()
        kc.add_simplex(2, "simplex_2d")
        assert kc.n_simplifies(2) == ["simplex_2d"]
        assert kc.dimension == 2

    def test_n_simplifies(self):
        kc = KanComplex()
        kc.add_simplex(1, "edge")
        assert kc.n_simplifies(1) == ["edge"]
        assert kc.n_simplifies(0) == []

    def test_face_map(self):
        kc = KanComplex()
        simplex = [0, 1, 2]
        fm = kc.face_map(simplex, 0)
        assert fm == simplex

    def test_degeneracy_map(self):
        kc = KanComplex()
        simplex = [0, 1]
        dm = kc.degeneracy_map(simplex, 0)
        assert dm == simplex

    def test_horn_lambda(self):
        kc = KanComplex()
        assert kc.horn_lambda(3, 1) is None

    def test_filler_exists(self):
        kc = KanComplex()
        assert kc.filler_exists("horn", 3) is True

    def test_is_kan(self):
        kc = KanComplex()
        assert kc.is_kan() is True

    def test_homotopy_groups(self):
        kc = KanComplex()
        hpg = kc.homotopy_groups()
        assert 0 in hpg
        assert 1 in hpg

    def test_fundamental_groupoid(self):
        kc = KanComplex()
        fg = kc.fundamental_groupoid()
        assert fg == "fundamental groupoid"


class TestNCategory:
    def test_creation(self):
        nc = NCategory(3)
        assert nc.n == 3

    def test_add_object(self):
        nc = NCategory(2)
        nc.add_object("X")
        assert "X" in nc.objects

    def test_hom_category(self):
        nc = NCategory(2)
        nc.add_object("X")
        nc.add_object("Y")
        hom = nc.hom_category("X", "Y")
        assert hom is not None
        assert hom.n == 1

    def test_hom_category_n1(self):
        nc = NCategory(1)
        hom = nc.hom_category("X", "Y")
        assert hom is None

    def test_is_strict(self):
        nc = NCategory(2)
        assert nc.is_strict() is True

    def test_is_weak(self):
        nc = NCategory(2)
        assert nc.is_weak() is False

    def test_coherence_theorem(self):
        nc = NCategory(2)
        assert nc.coherence_theorem() is True


class TestWeakEquivalence:
    def test_creation(self):
        we = WeakEquivalence("X", "Y", lambda x: x)
        assert we.source == "X"
        assert we.target == "Y"

    def test_is_weak_equivalence(self):
        we = WeakEquivalence("X", "Y", lambda x: x)
        assert we.is_weak_equivalence() is True

    def test_homotopy_inverse(self):
        we = WeakEquivalence("X", "Y", lambda x: x)
        assert we.homotopy_inverse() is None

    def test_two_out_of_three(self):
        we1 = WeakEquivalence("X", "Y", lambda x: x)
        we2 = WeakEquivalence("Y", "Z", lambda x: x)
        assert we1.two_out_of_three(we2) is True


class TestHomotopyPushout:
    def test_creation(self):
        hp = HomotopyPushout(["A", "B", "C"])
        assert len(hp.diagram) == 3

    def test_universal_property(self):
        hp = HomotopyPushout(["A", "B", "C"])
        assert hp.universal_property() is True

    def test_compute_pushout(self):
        hp = HomotopyPushout(["A", "B", "C"])
        assert hp.compute_pushout() == "C"

    def test_compute_pushout_short(self):
        hp = HomotopyPushout(["A"])
        assert hp.compute_pushout() is None

    def test_is_homotopy_colimit(self):
        hp = HomotopyPushout(["A", "B", "C"])
        assert hp.is_homotopy_colimit() is True


class TestHomotopyPullback:
    def test_creation(self):
        hp = HomotopyPullback(["A", "B", "C"])
        assert len(hp.diagram) == 3

    def test_universal_property(self):
        hp = HomotopyPullback(["A", "B", "C"])
        assert hp.universal_property() is True

    def test_compute_pullback(self):
        hp = HomotopyPullback(["A", "B", "C"])
        assert hp.compute_pullback() == "C"

    def test_homotopy_fiber(self):
        hp = HomotopyPullback(["A", "B", "C"])
        fiber = hp.homotopy_fiber(lambda x: x, "base")
        assert fiber == "base"


class TestSegalCategory:
    def test_creation(self):
        sc = SegalCategory("SegC")
        assert sc.name == "SegC"
        assert sc.spaces == {}

    def test_add_space(self):
        sc = SegalCategory()
        sc.add_space(1, "X1")
        assert sc.n_space(1) == "X1"

    def test_n_space(self):
        sc = SegalCategory()
        sc.add_space(2, "X2")
        assert sc.n_space(2) == "X2"
        assert sc.n_space(0) is None

    def test_segal_map(self):
        sc = SegalCategory()
        sm = sc.segal_map(2)
        assert sm("x") == "x"

    def test_is_segal(self):
        sc = SegalCategory()
        assert sc.is_segal() is True

    def test_homotopy_category(self):
        sc = SegalCategory()
        hc = sc.homotopy_category()
        assert hc == "homotopy category"


class TestCompleteSegalSpace:
    def test_creation(self):
        css = CompleteSegalSpace("CSS")
        assert css.name == "CSS"

    def test_add_space(self):
        css = CompleteSegalSpace()
        css.add_space(1, "W1")
        assert css.spaces[1] == "W1"

    def test_is_complete(self):
        css = CompleteSegalSpace()
        assert css.is_complete() is True

    def test_is_segal(self):
        css = CompleteSegalSpace()
        assert css.is_segal() is True

    def test_DK_equivalence(self):
        css1 = CompleteSegalSpace()
        css2 = CompleteSegalSpace()
        assert css1.DK_equivalence(css2) is True


class TestAnima:
    def test_creation(self):
        a = Anima("A")
        assert a.name == "A"

    def test_is_kan(self):
        a = Anima()
        assert a.is_kan() is True

    def test_is_discrete(self):
        a = Anima()
        assert a.is_discrete() is True

    def test_fundamental_group(self):
        a = Anima()
        assert a.fundamental_group() is None

    def test_homotopy_colimit(self):
        a1 = Anima("A1")
        a2 = Anima("A2")
        result = a1.homotopy_colimit([a2])
        assert isinstance(result, Anima)


class TestInfinityTopos:
    def test_creation(self):
        it = InfinityTopos("site")
        assert it.underlying_site == "site"

    def test_sheafify(self):
        it = InfinityTopos("site")
        presheaf = lambda x: "presheaf"
        result = it.sheafify(presheaf)
        assert result == presheaf

    def test_n_topos(self):
        it = InfinityTopos("site")
        result = it.n_topos(1)
        assert result is it

    def test_is_logical(self):
        it = InfinityTopos("site")
        assert it.is_logical() is True

    def test_left_exact_localization(self):
        it = InfinityTopos("site")
        result = it.left_exact_localization({"object"})
        assert result is not None

    def test_cohesive_structure(self):
        it = InfinityTopos("site")
        assert it.cohesive_structure() is True