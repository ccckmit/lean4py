"""Tests for sheaf extensions (Scheme, Site, etc.) in v1.18."""
import pytest
from lean4py.sheaf import (
    SheafOfRings, SheafOfModules, Scheme, SchemeMorphism, AffineMorphisms,
    Site, GrothendieckTopology, Coverage
)


class TestSheafOfRings:
    def test_creation(self):
        sr = SheafOfRings()
        assert sr.space is None

    def test_creation_with_space(self):
        from lean4py.sheaf import TopologicalSpace
        ts = TopologicalSpace({1, 2}, [{1}, {2}, {1, 2}])
        sr = SheafOfRings(ts)
        assert sr.space == ts

    def test_section_ring(self):
        sr = SheafOfRings()
        result = sr.section_ring({1, 2})
        assert result is None

    def test_add_section(self):
        sr = SheafOfRings()
        sr.add_section({1, 2}, "ring")
        assert sr.ring_sections.get(frozenset({1, 2})) == "ring"

    def test_stalks(self):
        sr = SheafOfRings()
        result = sr.stalks(1)
        assert result == "local_ring"

    def test_is_ringed_space(self):
        sr = SheafOfRings()
        assert sr.is_ringed_space() is True


class TestSheafOfModules:
    def test_creation(self):
        sm = SheafOfModules()
        assert sm.sheaf_of_rings is None

    def test_creation_with_sheaf_of_rings(self):
        sr = SheafOfRings()
        sm = SheafOfModules(sr)
        assert sm.sheaf_of_rings == sr

    def test_section_module(self):
        sm = SheafOfModules()
        result = sm.section_module({1, 2})
        assert result is None

    def test_add_section(self):
        sm = SheafOfModules()
        sm.add_section({1, 2}, "module")
        assert sm.module_sections.get(frozenset({1, 2})) == "module"

    def test_is_quasicoherent(self):
        sm = SheafOfModules()
        assert sm.is_quasicoherent() is True

    def test_is_coherent(self):
        sm = SheafOfModules()
        assert sm.is_coherent() is True


class TestScheme:
    def test_creation(self):
        s = Scheme()
        assert s.patches == []

    def test_creation_with_patches(self):
        from lean4py.sheaf import AffineScheme
        aff = AffineScheme("R")
        s = Scheme([aff])
        assert len(s.patches) == 1

    def test_construct_space(self):
        s = Scheme()
        space = s._construct_space()
        from lean4py.sheaf import TopologicalSpace
        assert isinstance(space, TopologicalSpace)

    def test_construct_structure_sheaf(self):
        s = Scheme()
        sf = s._construct_structure_sheaf()
        assert isinstance(sf, SheafOfRings)

    def test_is_affine(self):
        s = Scheme()
        assert s.is_affine() is False

    def test_is_affine_single_patch(self):
        from lean4py.sheaf import AffineScheme
        aff = AffineScheme("R")
        s = Scheme([aff])
        assert s.is_affine() is True

    def test_open_affine(self):
        from lean4py.sheaf import AffineScheme
        aff = AffineScheme("R")
        s = Scheme([aff])
        result = s.open_affine()
        assert result == aff

    def test_open_affine_not_affine(self):
        s = Scheme()
        result = s.open_affine()
        assert result is None

    def test_underlying_space(self):
        s = Scheme()
        result = s.underlying_space()
        from lean4py.sheaf import TopologicalSpace
        assert isinstance(result, TopologicalSpace)

    def test_add_patch(self):
        from lean4py.sheaf import AffineScheme
        s = Scheme()
        aff = AffineScheme("R")
        s.add_patch(aff)
        assert len(s.patches) == 1


class TestSchemeMorphism:
    def test_creation(self):
        sm = SchemeMorphism("source", "target")
        assert sm.source == "source"
        assert sm.target == "target"

    def test_creation_with_maps(self):
        sm = SchemeMorphism("source", "target", lambda x: x, lambda x: x)
        assert sm.map_on_points(1) == 1

    def test_is_morphism(self):
        sm = SchemeMorphism("source", "target")
        assert sm.is_morphism() is True

    def test_is_open_immersion(self):
        sm = SchemeMorphism("source", "target")
        assert sm.is_open_immersion() is False

    def test_is_closed_immersion(self):
        sm = SchemeMorphism("source", "target")
        assert sm.is_closed_immersion() is False

    def test_is_scheme_morphism(self):
        sm = SchemeMorphism("source", "target")
        assert sm.is_scheme_morphism() is True

    def test_pullback(self):
        sm = SchemeMorphism("source", "target")
        result = sm.pullback("y")
        assert result == "y"


class TestAffineMorphisms:
    def test_is_affine(self):
        sm = SchemeMorphism("source", "target")
        result = AffineMorphisms.is_affine(sm)
        assert result is False

    def test_finite(self):
        sm = SchemeMorphism("source", "target")
        result = AffineMorphisms.finite(sm)
        assert result is False

    def test_affine_spec(self):
        result = AffineMorphisms.affine_spec(["R", "S"])
        assert len(result) == 2

    def test_is_separated(self):
        sm = SchemeMorphism("source", "target")
        result = AffineMorphisms.is_separated(sm)
        assert result is True


class TestSite:
    def test_creation(self):
        site = Site()
        assert site.category is None

    def test_creation_with_category(self):
        site = Site("category")
        assert site.category == "category"

    def test_add_covering(self):
        site = Site()
        site.add_covering(["U1", "U2"])
        assert len(site.coverings) == 1

    def test_is_grothendieck(self):
        site = Site()
        assert site.is_grothendieck() is True

    def test_covering_families(self):
        site = Site("category", [["U1", "U2"]])
        result = site.covering_families("X")
        assert len(result) == 1


class TestGrothendieckTopology:
    def test_creation(self):
        gt = GrothendieckTopology()
        assert gt.site is None

    def test_creation_with_site(self):
        site = Site()
        gt = GrothendieckTopology(site)
        assert gt.site == site

    def test_covering_families(self):
        site = Site("category", [["U1"]])
        gt = GrothendieckTopology(site)
        result = gt.covering_families("X")
        assert len(result) == 1

    def test_sieve(self):
        gt = GrothendieckTopology()
        result = gt.sieve("X")
        assert isinstance(result, set)

    def test_is_topology(self):
        gt = GrothendieckTopology()
        assert gt.is_topology() is True


class TestCoverage:
    def test_creation(self):
        cov = Coverage()
        assert cov.families == []

    def test_creation_with_families(self):
        cov = Coverage([(("U1",), ("U2",))])
        assert len(cov.families) == 1

    def test_add_family(self):
        cov = Coverage()
        cov.add_family(("U1", "U2"))
        assert len(cov.families) == 1

    def test_generate_topology(self):
        cov = Coverage([(("U1",), ("U2",))])
        gt = cov.generate_topology()
        assert isinstance(gt, GrothendieckTopology)