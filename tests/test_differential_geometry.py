"""Tests for differential_geometry module (v1.20)."""
import pytest
from lean4py.differential_geometry import (
    Manifold, TangentSpace, TangentBundle, VectorField, Connection,
    RiemannianMetric, Geodesic, LeviCivitaConnection, CurvatureTensor,
    RiemannianManifold, Submanifold
)


class TestManifold:
    def test_creation(self):
        m = Manifold(3, "S^3")
        assert m.dimension == 3
        assert m.name == "S^3"

    def test_add_chart(self):
        m = Manifold(2)
        m.add_chart({1, 2}, lambda x: x)
        assert len(m.charts) == 1

    def test_dimension_of(self):
        m = Manifold(4)
        assert m.dimension_of() == 4

    def test_is_smooth(self):
        m = Manifold(2)
        assert m.is_smooth() is True


class TestTangentSpace:
    def test_creation(self):
        m = Manifold(2)
        ts = TangentSpace(m, "p")
        assert ts.manifold == m
        assert ts.point == "p"

    def test_dimension_of(self):
        m = Manifold(3)
        ts = TangentSpace(m, "p")
        assert ts.dimension_of() == 3

    def test_add_basis_vector(self):
        m = Manifold(2)
        ts = TangentSpace(m, "p")
        ts.add_basis_vector([1.0, 0.0])
        assert len(ts.basis) == 1

    def test_get_basis(self):
        m = Manifold(2)
        ts = TangentSpace(m, "p")
        basis = ts.get_basis()
        assert len(basis) == 2


class TestTangentBundle:
    def test_creation(self):
        m = Manifold(3)
        tb = TangentBundle(m)
        assert tb.manifold == m

    def test_dimension(self):
        m = Manifold(2)
        tb = TangentBundle(m)
        assert tb.dimension() == 4

    def test_projection(self):
        m = Manifold(3)
        tb = TangentBundle(m)
        assert tb.projection("v") == m

    def test_add_vector_field(self):
        m = Manifold(2)
        tb = TangentBundle(m)
        tb.add_vector_field("X", lambda x: x)
        assert "X" in tb.sections


class TestVectorField:
    def test_creation(self):
        m = Manifold(2)
        vf = VectorField(m)
        assert vf.manifold == m

    def test_set_value(self):
        m = Manifold(2)
        vf = VectorField(m)
        vf.set_value("p", [1.0, 2.0])
        assert vf.get_value("p") == [1.0, 2.0]

    def test_get_value_default(self):
        m = Manifold(2)
        vf = VectorField(m)
        assert vf.get_value("q") == [0.0, 0.0]

    def test_lie_bracket(self):
        m = Manifold(2)
        X = VectorField(m)
        Y = VectorField(m)
        Z = X.lie_bracket(Y)
        assert Z.manifold == m


class TestConnection:
    def test_creation(self):
        m = Manifold(2)
        c = Connection(m)
        assert c.manifold == m

    def test_set_christoffel(self):
        m = Manifold(2)
        c = Connection(m)
        c.set_christoffel(0, 1, 0, 0.5)
        assert c.get_christoffel(0, 1, 0) == 0.5

    def test_get_christoffel_default(self):
        m = Manifold(2)
        c = Connection(m)
        assert c.get_christoffel(0, 1, 0) == 0.0

    def test_covariant_derivative(self):
        m = Manifold(2)
        c = Connection(m)
        X = VectorField(m)
        Y = VectorField(m)
        result = c.covariant_derivative(X, Y)
        assert result.manifold == m

    def test_torsion(self):
        m = Manifold(2)
        c = Connection(m)
        X = VectorField(m)
        Y = VectorField(m)
        T = c.torsion(X, Y)
        assert T.manifold == m


class TestRiemannianMetric:
    def test_creation(self):
        m = Manifold(2)
        rm = RiemannianMetric(m)
        assert rm.manifold == m

    def test_set_metric(self):
        m = Manifold(2)
        rm = RiemannianMetric(m)
        rm.set_metric("p", [[1, 0], [0, 1]])
        assert rm.inner_product_at("p", [1, 0], [1, 0]) == 1

    def test_inner_product_at(self):
        m = Manifold(2)
        rm = RiemannianMetric(m)
        rm.set_metric("p", [[1, 0], [0, 1]])
        assert rm.inner_product_at("p", [1, 0], [0, 1]) == 0

    def test_is_riemannian(self):
        m = Manifold(2)
        rm = RiemannianMetric(m)
        assert rm.is_riemannian() is True

    def test_norm(self):
        m = Manifold(2)
        rm = RiemannianMetric(m)
        rm.set_metric("p", [[1, 0], [0, 1]])
        assert abs(rm.norm("p", [3.0, 4.0]) - 5.0) < 1e-6


class TestGeodesic:
    def test_creation(self):
        m = Manifold(2)
        rm = RiemannianMetric(m)
        g = Geodesic(rm, [0.0, 0.0], [1.0, 0.0])
        assert g.metric == rm

    def test_compute_curve(self):
        m = Manifold(2)
        rm = RiemannianMetric(m)
        g = Geodesic(rm, [0.0, 0.0], [1.0, 0.0])
        result = g.compute_curve(1.0)
        assert result == [1.0, 0.0]

    def test_length(self):
        m = Manifold(2)
        rm = RiemannianMetric(m)
        g = Geodesic(rm, [0.0, 0.0], [1.0, 0.0])
        result = g.length(0, 1)
        assert result == 1.0

    def test_energy(self):
        m = Manifold(2)
        rm = RiemannianMetric(m)
        g = Geodesic(rm, [0.0, 0.0], [1.0, 0.0])
        result = g.energy(0, 1)
        assert result == 0.5


class TestLeviCivitaConnection:
    def test_creation(self):
        m = Manifold(2)
        rm = RiemannianMetric(m)
        lc = LeviCivitaConnection(rm)
        assert lc.metric == rm

    def test_is_metric_compatible(self):
        m = Manifold(2)
        rm = RiemannianMetric(m)
        lc = LeviCivitaConnection(rm)
        assert lc.is_metric_compatible() is True


class TestCurvatureTensor:
    def test_creation(self):
        m = Manifold(2)
        c = Connection(m)
        ct = CurvatureTensor(c)
        assert ct.connection == c

    def test_compute_riemann(self):
        m = Manifold(2)
        c = Connection(m)
        ct = CurvatureTensor(c)
        result = ct.compute_riemann(0, 1, 0, 1)
        assert isinstance(result, float)

    def test_ricci_tensor(self):
        m = Manifold(2)
        c = Connection(m)
        ct = CurvatureTensor(c)
        result = ct.ricci_tensor(0, 1)
        assert isinstance(result, float)

    def test_scalar_curvature(self):
        m = Manifold(2)
        c = Connection(m)
        ct = CurvatureTensor(c)
        result = ct.scalar_curvature()
        assert isinstance(result, float)

    def test_section_curvature(self):
        m = Manifold(2)
        c = Connection(m)
        ct = CurvatureTensor(c)
        result = ct.section_curvature([1, 0], [0, 1])
        assert isinstance(result, float)


class TestRiemannianManifold:
    def test_creation(self):
        m = Manifold(2)
        rm = RiemannianManifold(2, RiemannianMetric(m))
        assert rm.dimension == 2
        assert rm.metric is not None

    def test_distance(self):
        rm = RiemannianManifold(2)
        result = rm.distance([0, 0], [3, 4])
        assert abs(result - 5.0) < 1e-6

    def test_laplacian(self):
        rm = RiemannianManifold(2)
        f = lambda x: x[0]**2
        Lf = rm.laplacian(f)
        assert callable(Lf)

    def test_gradient(self):
        rm = RiemannianManifold(2)
        f = lambda x: x[0]
        grad = rm.gradient(f)
        assert grad.manifold == rm


class TestSubmanifold:
    def test_creation(self):
        m = Manifold(3)
        sm = Submanifold(m, lambda x: x)
        assert sm.ambient == m

    def test_codimension(self):
        m = Manifold(3)
        sm = Submanifold(m, lambda x: [1, 2])
        result = sm.codimension()
        assert isinstance(result, int)

    def test_second_fundamental_form(self):
        m = Manifold(2)
        sm = Submanifold(m, lambda x: x)
        result = sm.second_fundamental_form()
        assert isinstance(result, str)