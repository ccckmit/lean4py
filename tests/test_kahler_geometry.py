"""Tests for kahler_geometry module (v1.17)."""
import pytest
from lean4py.kahler_geometry import (
    ComplexManifold, AlmostComplexStructure, HermitianMetric, KahlerManifold,
    KahlerMetric, ChernConnection, FirstChernClass, HolomorphicSection,
    ComplexProjectiveSpace, HermitianEinsteinMetric, CalabiYauManifold,
    ComplexSubmanifold, CohomologyRing, HolomorphicVectorBundle
)


class TestComplexManifold:
    def test_creation(self):
        cm = ComplexManifold(3)
        assert cm.dimension == 3

    def test_add_chart(self):
        cm = ComplexManifold(2)
        cm.add_chart({"U": 1})
        assert len(cm.charts) == 1

    def test_is_complex(self):
        cm = ComplexManifold(2)
        assert cm.is_complex() is True

    def test_complex_dimension(self):
        cm = ComplexManifold(3)
        assert cm.complex_dimension() == 3


class TestAlmostComplexStructure:
    def test_creation(self):
        acs = AlmostComplexStructure()
        assert acs.manifold is None

    def test_creation_with_operator(self):
        acs = AlmostComplexStructure(operator=lambda v: (1, 1))
        assert acs.operator is not None

    def test_is_integrable(self):
        acs = AlmostComplexStructure()
        assert acs.is_integrable() is True


class TestHermitianMetric:
    def test_creation(self):
        hm = HermitianMetric()
        assert hm._metric == {}

    def test_set_metric_component(self):
        hm = HermitianMetric()
        hm.set_metric_component(1, 2, lambda: 1.0)
        assert hm.get_metric_component(1, 2) == 1.0

    def test_get_metric_component_default(self):
        hm = HermitianMetric()
        assert hm.get_metric_component(1, 2) == 0.0

    def test_is_hermitian(self):
        hm = HermitianMetric()
        assert hm.is_hermitian() is True

    def test_christoffel_symbols(self):
        hm = HermitianMetric()
        result = hm.christoffel_symbols()
        assert len(result) == 1


class TestKahlerManifold:
    def test_creation(self):
        km = KahlerManifold(3)
        assert km.dimension == 3
        assert km.metric is None

    def test_set_kahler_metric(self):
        km = KahlerManifold(2)
        metric = HermitianMetric()
        km.set_kahler_metric(metric)
        assert km.metric is metric

    def test_kahler_condition(self):
        km = KahlerManifold(2)
        assert km.kahler_condition() is True

    def test_ricci_curvature(self):
        km = KahlerManifold(2)
        result = km.ricci_curvature()
        assert isinstance(result, dict)

    def test_scalar_curvature(self):
        km = KahlerManifold(2)
        result = km.scalar_curvature()
        assert isinstance(result, float)

    def test_first_chern_class(self):
        km = KahlerManifold(2)
        c1 = km.first_chern_class()
        assert isinstance(c1, FirstChernClass)


class TestKahlerMetric:
    def test_creation(self):
        km = KahlerMetric()
        assert km.kahler_potential is not None

    def test_creation_with_potential(self):
        km = KahlerMetric(lambda z: z[0] if z else 0)
        assert km.kahler_potential is not None

    def test_metric_from_potential(self):
        km = KahlerMetric()
        result = km.metric_from_potential()
        assert isinstance(result, dict)

    def test_is_kahler(self):
        km = KahlerMetric()
        assert km.is_kahler() is True


class TestChernConnection:
    def test_creation(self):
        cc = ChernConnection()
        assert cc.bundle is None
        assert cc.metric is None

    def test_connection_matrix(self):
        cc = ChernConnection()
        result = cc.connection_matrix()
        assert isinstance(result, list)

    def test_curvature_form(self):
        cc = ChernConnection()
        result = cc.curvature_form()
        assert result is None

    def test_chern_curvature(self):
        cc = ChernConnection()
        result = cc.chern_curvature()
        assert isinstance(result, dict)


class TestFirstChernClass:
    def test_creation(self):
        c1 = FirstChernClass(3)
        assert c1.dimension == 3
        assert c1.manifold is None

    def test_evaluate_on_surface(self):
        c1 = FirstChernClass(2)
        result = c1.evaluate_on_surface("surface")
        assert isinstance(result, int)

    def test_is_positive(self):
        c1 = FirstChernClass(2)
        assert c1.is_positive() is True


class TestHolomorphicSection:
    def test_creation(self):
        hs = HolomorphicSection("bundle")
        assert hs.line_bundle == "bundle"

    def test_creation_with_function(self):
        hs = HolomorphicSection("bundle", lambda z: z)
        assert hs.function is not None

    def test_is_holomorphic(self):
        hs = HolomorphicSection("bundle")
        assert hs.is_holomorphic() is True

    def test_zeros_divisor(self):
        hs = HolomorphicSection("bundle")
        result = hs.zeros_divisor()
        assert isinstance(result, list)

    def test_section_norm(self):
        hs = HolomorphicSection("bundle")
        metric = HermitianMetric()
        result = hs.section_norm(metric)
        assert isinstance(result, float)


class TestComplexProjectiveSpace:
    def test_creation(self):
        cpp = ComplexProjectiveSpace(2)
        assert cpp.n == 2
        assert cpp.complex_dimension == 2

    def test_homogeneous_coordinates(self):
        cpp = ComplexProjectiveSpace(2)
        coords = cpp.homogeneous_coordinates()
        assert len(coords) == 3
        assert coords == ["x0", "x1", "x2"]

    def test_fubini_study_metric(self):
        cpp = ComplexProjectiveSpace(2)
        metric = cpp.fubini_study_metric()
        assert isinstance(metric, KahlerMetric)

    def test_hyperplane_section_class(self):
        cpp = ComplexProjectiveSpace(2)
        hs = cpp.hyperplane_section_class()
        assert isinstance(hs, HolomorphicSection)

    def test_chern_classes(self):
        cpp = ComplexProjectiveSpace(2)
        classes = cpp.chern_classes()
        assert 1 in classes


class TestHermitianEinsteinMetric:
    def test_creation(self):
        km = KahlerManifold(2)
        he = HermitianEinsteinMetric(km)
        assert he.manifold is km

    def test_is_einstein(self):
        km = KahlerManifold(2)
        he = HermitianEinsteinMetric(km)
        assert he.is_einstein(0.0) is True

    def test_existence_theorem(self):
        km = KahlerManifold(2)
        he = HermitianEinsteinMetric(km)
        assert he.existence_theorem() is True


class TestCalabiYauManifold:
    def test_creation(self):
        cy = CalabiYauManifold(3)
        assert cy.dimension == 3
        assert cy._holomorphic_volume_form is None

    def test_set_holomorphic_volume_form(self):
        cy = CalabiYauManifold(3)
        cy.set_holomorphic_volume_form("Omega")
        assert cy._holomorphic_volume_form == "Omega"

    def test_is_calabi_yau(self):
        cy = CalabiYauManifold(3)
        assert cy.is_calabi_yau() is True

    def test_yau_solution(self):
        cy = CalabiYauManifold(3)
        initial = KahlerMetric()
        result = cy.yau_solution(initial)
        assert isinstance(result, KahlerMetric)


class TestComplexSubmanifold:
    def test_creation(self):
        cm = ComplexManifold(4)
        cs = ComplexSubmanifold(cm, [lambda x: 0])
        assert cs.ambient is cm
        assert len(cs.defining_functions) == 1

    def test_dimension(self):
        cm = ComplexManifold(4)
        cs = ComplexSubmanifold(cm, [lambda x: 0, lambda x: 0])
        assert cs.dimension() == 2

    def test_is_closed(self):
        cm = ComplexManifold(3)
        cs = ComplexSubmanifold(cm, [])
        assert cs.is_closed() is True


class TestCohomologyRing:
    def test_creation(self):
        cm = ComplexManifold(3)
        cr = CohomologyRing(cm)
        assert cr.manifold is cm

    def test_betti_number(self):
        cm = ComplexManifold(3)
        cr = CohomologyRing(cm)
        result = cr.betti_number(0)
        assert isinstance(result, int)

    def test_hodge_numbers(self):
        cm = ComplexManifold(3)
        cr = CohomologyRing(cm)
        result = cr.hodge_numbers()
        assert isinstance(result, dict)


class TestHolomorphicVectorBundle:
    def test_creation(self):
        cm = ComplexManifold(3)
        vb = HolomorphicVectorBundle(cm, 2)
        assert vb.base is cm
        assert vb.rank == 2

    def test_add_chern_class(self):
        cm = ComplexManifold(3)
        vb = HolomorphicVectorBundle(cm, 2)
        vb.add_chern_class(1, FirstChernClass(3))
        assert 1 in vb.chern_classes

    def test_euler_characteristic(self):
        cm = ComplexManifold(3)
        vb = HolomorphicVectorBundle(cm, 2)
        result = vb.euler_characteristic()
        assert isinstance(result, int)