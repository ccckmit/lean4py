"""Tests for extended stacks module (v1.16)."""
import pytest
from lean4py.stacks import (
    CechCohomology, CechComplex, SheafCohomologyGroups, DerivedPushforward,
    SpectralSequenceConvergence, LeraySpectralSequence, GrothendieckHigherDirectImage,
    CartesianMorphism, StackModuli, PicardStack, StabilityCondition,
    GeometricInvariantTheory, FormalSmoothMorphisms, FormalUnramified
)


class TestCechCohomology:
    def test_creation(self):
        c = CechCohomology("sheaf", [{1}, {2}])
        assert c.sheaf == "sheaf"
        assert len(c.cover) == 2

    def test_Hn(self):
        c = CechCohomology("sheaf", [{1}, {2}])
        result = c.Hn(0)
        assert isinstance(result, set)


class TestCechComplex:
    def test_creation(self):
        cc = CechComplex("sheaf", [{1}, {2}])
        assert cc.sheaf == "sheaf"

    def test_differential(self):
        cc = CechComplex("sheaf", [{1}, {2}])
        d = cc.differential(0)
        assert callable(d)

    def test_cohomology(self):
        cc = CechComplex("sheaf", [{1}, {2}])
        result = cc.cohomology(0)
        assert isinstance(result, set)


class TestSheafCohomologyGroups:
    def test_creation(self):
        sh = SheafCohomologyGroups("sheaf")
        assert sh.sheaf == "sheaf"

    def test_H0(self):
        sh = SheafCohomologyGroups("sheaf")
        assert isinstance(sh.H0(), set)

    def test_H1(self):
        sh = SheafCohomologyGroups("sheaf")
        assert isinstance(sh.H1(), set)


class TestDerivedPushforward:
    def test_creation(self):
        dp = DerivedPushforward("morphism")
        assert dp.morphism == "morphism"

    def test_compute(self):
        dp = DerivedPushforward("morphism")
        result = dp.compute("sheaf", 0)
        assert result == "sheaf"


class TestSpectralSequenceConvergence:
    def test_abuts_to(self):
        result = SpectralSequenceConvergence.abuts_to("cohomology", set())
        assert result is True

    def test_filtered_complex_has_ss(self):
        result = SpectralSequenceConvergence.filtered_complex_has_ss(set())
        assert result is True


class TestLeraySpectralSequence:
    def test_creation(self):
        lss = LeraySpectralSequence("base", "fiber")
        assert lss.base == "base"
        assert lss.fiber == "fiber"

    def test_compute_E2(self):
        lss = LeraySpectralSequence("base", "fiber")
        result = lss.compute_E2()
        assert isinstance(result, dict)


class TestCartesianMorphism:
    def test_creation(self):
        cm = CartesianMorphism("src", "tgt")
        assert cm.source == "src"
        assert cm.target == "tgt"

    def test_is_cartesian(self):
        cm = CartesianMorphism("src", "tgt")
        assert cm.is_cartesian() is True


class TestStackModuli:
    def test_creation(self):
        sm = StackModuli("curves")
        assert sm.moduli_type == "curves"


class TestPicardStack:
    def test_creation(self):
        ps = PicardStack()
        assert ps.base_space is None


class TestStabilityCondition:
    def test_creation(self):
        sc = StabilityCondition()
        assert sc.heart is None

    def test_is_stable(self):
        sc = StabilityCondition()
        assert sc.is_stable("obj") is True


class TestGeometricInvariantTheory:
    def test_creation(self):
        git = GeometricInvariantTheory("action")
        assert git.action == "action"

    def test_hilbert_mumford(self):
        git = GeometricInvariantTheory("action")
        result = git.hilbert_mumford_criterion("x")
        assert result == "stable"


class TestFormalSmoothMorphisms:
    def test_is_formally_smooth(self):
        assert FormalSmoothMorphisms.is_formally_smooth("f") is True

    def test_is_etale(self):
        assert FormalSmoothMorphisms.is_etale("f") is False

    def test_is_unramified(self):
        assert FormalSmoothMorphisms.is_unramified("f") is False


class TestFormalUnramified:
    def test_check_smoothness(self):
        result = FormalUnramified.check_smoothness("f", "point")
        assert result is True


def test_import_from_package():
    from lean4py import (
        CechCohomology, CechComplex, LeraySpectralSequence,
        StackModuli, StabilityCondition, GeometricInvariantTheory
    )
    assert CechCohomology is not None
    assert LeraySpectralSequence is not None
    assert StackModuli is not None
    assert StabilityCondition is not None