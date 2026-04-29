"""Tests for topos module (v1.18)."""
import pytest
from lean4py.topos import (
    Topos, SheafTopos, BooleanTopos, AbelianCategory, Monomorphism, Epimorphism,
    ProjectiveObject, InjectiveObject, Generator, Cogenerator, ExactFunctor,
    LeftExactFunctor, RightExactFunctor, Kernel, Cokernel, Image, ExactSequence
)


class TestTopos:
    def test_creation(self):
        t = Topos()
        assert t.sheaves == []

    def test_creation_with_sheaves(self):
        t = Topos(["sheaf1", "sheaf2"])
        assert len(t.sheaves) == 2

    def test_subobject_classifier(self):
        t = Topos()
        assert True in t.subobject_classifier

    def test_has_exponentials(self):
        t = Topos()
        assert t.has_exponentials() is True

    def test_is_cartesian_closed(self):
        t = Topos()
        assert t.is_cartesian_closed() is True

    def test_power_object(self):
        t = Topos()
        result = t.power_object("X")
        assert result == "X"

    def test_subobject(self):
        t = Topos()
        result = t.subobject("X")
        assert isinstance(result, list)


class TestSheafTopos:
    def test_creation(self):
        st = SheafTopos()
        assert st.space is None

    def test_creation_with_space(self):
        st = SheafTopos("space")
        assert st.space == "space"

    def test_is_grothendieck_topos(self):
        st = SheafTopos()
        assert st.is_grothendieck_topos() is True


class TestBooleanTopos:
    def test_creation(self):
        bt = BooleanTopos()
        assert bt.sheaves == []

    def test_is_boolean(self):
        bt = BooleanTopos()
        assert bt.is_boolean() is True

    def test_law_of_excluded_middle(self):
        bt = BooleanTopos()
        assert bt.law_of_excluded_middle() is True


class TestAbelianCategory:
    def test_creation(self):
        ac = AbelianCategory()
        assert ac.objects == []

    def test_creation_with_objects(self):
        ac = AbelianCategory(["A", "B", "C"])
        assert len(ac.objects) == 3

    def test_add_object(self):
        ac = AbelianCategory()
        ac.add_object("X")
        assert "X" in ac.objects

    def test_zero_object(self):
        ac = AbelianCategory(["A"])
        assert ac.zero_object() == "A"

    def test_zero_object_empty(self):
        ac = AbelianCategory()
        assert ac.zero_object() is None

    def test_kernel(self):
        ac = AbelianCategory()
        k = ac.kernel(lambda x: x)
        assert isinstance(k, Monomorphism)

    def test_cokernel(self):
        ac = AbelianCategory()
        ck = ac.cokernel(lambda x: x)
        assert isinstance(ck, Epimorphism)

    def test_is_abelian(self):
        ac = AbelianCategory()
        assert ac.is_abelian() is True

    def test_hom(self):
        ac = AbelianCategory()
        result = ac.hom("A", "B")
        assert isinstance(result, list)


class TestMonomorphism:
    def test_creation(self):
        m = Monomorphism("A", "B", lambda x: x)
        assert m.source == "A"
        assert m.target == "B"

    def test_is_mono(self):
        m = Monomorphism("A", "B", lambda x: x)
        assert m.is_mono() is True


class TestEpimorphism:
    def test_creation(self):
        e = Epimorphism("A", "B", lambda x: x)
        assert e.source == "A"
        assert e.target == "B"

    def test_is_epi(self):
        e = Epimorphism("A", "B", lambda x: x)
        assert e.is_epi() is True


class TestProjectiveObject:
    def test_creation(self):
        p = ProjectiveObject("P")
        assert p.obj == "P"
        assert p.category is None

    def test_is_projective(self):
        p = ProjectiveObject("P")
        assert p.is_projective() is True

    def test_project_cover(self):
        p = ProjectiveObject("P")
        result = p.projective_cover()
        assert isinstance(result, ProjectiveObject)


class TestInjectiveObject:
    def test_creation(self):
        i = InjectiveObject("I")
        assert i.obj == "I"
        assert i.category is None

    def test_is_injective(self):
        i = InjectiveObject("I")
        assert i.is_injective() is True

    def test_injective_envelope(self):
        i = InjectiveObject("I")
        result = i.injective_envelope()
        assert isinstance(result, InjectiveObject)


class TestGenerator:
    def test_creation(self):
        g = Generator("G")
        assert g.obj == "G"

    def test_is_generator(self):
        g = Generator("G")
        assert g.is_generator() is True


class TestCogenerator:
    def test_creation(self):
        c = Cogenerator("C")
        assert c.obj == "C"

    def test_is_cogenerator(self):
        c = Cogenerator("C")
        assert c.is_cogenerator() is True


class TestExactFunctor:
    def test_creation(self):
        ef = ExactFunctor()
        assert ef.source is None

    def test_is_exact(self):
        ef = ExactFunctor()
        assert ef.is_exact() is True

    def test_is_left_exact(self):
        ef = ExactFunctor()
        assert ef.is_left_exact() is True

    def test_is_right_exact(self):
        ef = ExactFunctor()
        assert ef.is_right_exact() is True

    def test_apply_to_object(self):
        ef = ExactFunctor()
        result = ef.apply_to_object("X")
        assert result == "X"


class TestLeftExactFunctor:
    def test_is_left_exact(self):
        lef = LeftExactFunctor()
        assert lef.is_left_exact() is True

    def test_is_right_exact(self):
        lef = LeftExactFunctor()
        assert lef.is_right_exact() is False


class TestRightExactFunctor:
    def test_is_left_exact(self):
        ref = RightExactFunctor()
        assert ref.is_left_exact() is False

    def test_is_right_exact(self):
        ref = RightExactFunctor()
        assert ref.is_right_exact() is True


class TestKernel:
    def test_creation(self):
        k = Kernel(lambda x: x, "ker")
        assert k.kernel_obj == "ker"

    def test_universal_property(self):
        k = Kernel(lambda x: x, "ker")
        assert k.universal_property() is True


class TestCokernel:
    def test_creation(self):
        ck = Cokernel(lambda x: x, "coker")
        assert ck.cokernel_obj == "coker"

    def test_universal_property(self):
        ck = Cokernel(lambda x: x, "coker")
        assert ck.universal_property() is True


class TestImage:
    def test_creation(self):
        img = Image(lambda x: x, "im")
        assert img.image_obj == "im"

    def test_is_image(self):
        img = Image(lambda x: x, "im")
        assert img.is_image() is True


class TestExactSequence:
    def test_creation(self):
        es = ExactSequence(["A", "B", "C"], [lambda x: x, lambda x: x])
        assert len(es.objects) == 3

    def test_is_exact_at_valid(self):
        es = ExactSequence(["A", "B", "C"], [lambda x: x, lambda x: x])
        assert es.is_exact_at(1) is True

    def test_is_exact_at_boundary(self):
        es = ExactSequence(["A", "B", "C"], [lambda x: x, lambda x: x])
        assert es.is_exact_at(0) is False

    def test_is_exact(self):
        es = ExactSequence(["A", "B", "C"], [lambda x: x, lambda x: x])
        assert es.is_exact_at(1) is True