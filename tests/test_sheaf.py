"""Tests for sheaf module."""
import pytest
from lean4py.sheaf import (
    TopologicalSpace, Presheaf, Sheaf, SheafCohomology,
    AffineScheme, Spec, ClosedSubscheme, OpenSubscheme
)


class TestTopologicalSpace:
    def test_creation(self):
        points = {1, 2, 3}
        opens = [{1}, {2}, {1, 2}]
        ts = TopologicalSpace(points, opens)
        assert len(ts.points) == 3
        assert len(ts.open_sets) == 3

    def test_is_open(self):
        ts = TopologicalSpace({1, 2}, [{1}, {2}])
        assert ts.is_open({1}) is True
        assert ts.is_open({3}) is False

    def test_open_cover(self):
        points = {1, 2, 3}
        opens = [{1, 2}, {2, 3}]
        ts = TopologicalSpace(points, opens)
        cover = ts.open_cover({1, 2, 3})
        assert isinstance(cover, list)


class TestPresheaf:
    def test_creation(self):
        ts = TopologicalSpace({1}, [{1}])
        ps = Presheaf[int](ts)
        assert ps.space == ts

    def test_add_section(self):
        ts = TopologicalSpace({1, 2}, [{1}, {2}, {1, 2}])
        ps = Presheaf[int](ts)
        ps.add_section({1}, 42)
        assert ps.get_section({1}) == 42

    def test_get_section_missing(self):
        ts = TopologicalSpace({1}, [{1}])
        ps = Presheaf[int](ts)
        assert ps.get_section({1}) is None

    def test_restrict(self):
        ts = TopologicalSpace({1, 2}, [{1, 2}])
        ps = Presheaf[int](ts)
        ps.add_section({1, 2}, 100)
        result = ps.restrict({1, 2}, {1})
        assert result == 100 or result is None


class TestSheaf:
    def test_creation(self):
        ts = TopologicalSpace({1}, [{1}])
        sh = Sheaf[int](ts)
        assert isinstance(sh, Presheaf)

    def test_global_section(self):
        ts = TopologicalSpace({1, 2}, [{1, 2}])
        sh = Sheaf[int](ts)
        sh.add_section({1, 2}, 999)
        assert sh.global_section() == 999


class TestSheafCohomology:
    def test_creation(self):
        ts = TopologicalSpace({1}, [{1}])
        sh = Sheaf(ts)
        cov = [{1}]
        sc = SheafCohomology(sh, ts, cov)
        assert sc.sheaf == sh

    def test_compute_H0(self):
        ts = TopologicalSpace({1}, [{1}])
        sh = Sheaf[str](ts)
        sh.add_section({1}, "global")
        cov = [{1}]
        sc = SheafCohomology(sh, ts, cov)
        H0 = sc.compute_H0()
        assert isinstance(H0, set)


class TestAffineScheme:
    def test_creation(self):
        scheme = AffineScheme("R")
        assert scheme.ring == "R"

    def test_is_affine(self):
        scheme = AffineScheme("R")
        assert scheme.is_affine() is True

    def test_structure_sheaf(self):
        scheme = AffineScheme("R")
        sheaf = scheme.structure_sheaf()
        assert isinstance(sheaf, Sheaf)


class TestSpec:
    def test_spec_of(self):
        result = Spec.of("R")
        assert isinstance(result, list)

    def test_maximal_spectrum(self):
        result = Spec.maximal_spectrum("R")
        assert isinstance(result, list)


class TestSubschemes:
    def test_closed_subscheme(self):
        scheme = AffineScheme("R")
        cs = ClosedSubscheme(scheme, "I")
        assert cs.scheme == scheme

    def test_open_subscheme(self):
        scheme = AffineScheme("R")
        os = OpenSubscheme(scheme, "f")
        assert os.scheme == scheme


def test_import_from_package():
    from lean4py import TopologicalSpace, Presheaf, Sheaf, AffineScheme, Spec
    assert TopologicalSpace is not None
    assert Presheaf is not None
    assert Sheaf is not None
    assert AffineScheme is not None
    assert Spec is not None