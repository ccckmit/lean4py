"""Tests for symplectic_geometry module."""
import pytest
from lean4py.symplectic_geometry import (
    SymplecticManifold,
    SymplecticForm,
    HamiltonianVectorField,
    PoissonBracket,
    MomentMap,
    Symplectomorphism,
    LagrangianSubmanifold,
    HamiltonianSystem,
    DarbouxCoordinates,
    ContactManifold,
    ReebVectorField,
)


class TestSymplecticManifold:
    def test_creation(self):
        sm = SymplecticManifold(4)
        assert sm.dimension == 4
        assert sm.half_dim == 2

    def test_even_dimension_required(self):
        with pytest.raises(ValueError):
            SymplecticManifold(3)

    def test_add_chart(self):
        sm = SymplecticManifold(4)
        sm.add_chart(["q1", "p1", "q2", "p2"])
        assert len(sm.charts) == 1

    def test_is_symplectic(self):
        sm = SymplecticManifold(4)
        assert sm.is_symplectic() is True

    def test_dimension_of(self):
        sm = SymplecticManifold(6)
        assert sm.dimension_of() == 6


class TestSymplecticForm:
    def test_creation(self):
        sm = SymplecticManifold(4)
        omega = SymplecticForm(sm)
        assert omega.manifold is sm

    def test_components(self):
        sm = SymplecticManifold(4)
        omega = SymplecticForm(sm)
        assert len(omega.components) > 0

    def test_evaluate(self):
        sm = SymplecticManifold(4)
        omega = SymplecticForm(sm)
        X = [1.0, 0.0, 0.0, 0.0]
        Y = [0.0, 0.0, 1.0, 0.0]
        val = omega.evaluate(X, Y)
        assert isinstance(val, float)

    def test_is_closed(self):
        sm = SymplecticManifold(4)
        omega = SymplecticForm(sm)
        assert omega.is_closed() is True

    def test_is_nondegenerate(self):
        sm = SymplecticManifold(4)
        omega = SymplecticForm(sm)
        assert omega.is_nondegenerate() is True


class TestHamiltonianVectorField:
    def test_creation(self):
        sm = SymplecticManifold(4)
        H = lambda x: x[0]
        Hvf = HamiltonianVectorField(sm, H)
        assert Hvf.manifold is sm

    def test_vector_at(self):
        sm = SymplecticManifold(4)
        H = lambda x: sum(x)
        Hvf = HamiltonianVectorField(sm, H)
        vec = Hvf.vector_at([1.0, 2.0, 3.0, 4.0])
        assert len(vec) == 4

    def test_flow(self):
        sm = SymplecticManifold(4)
        H = lambda x: 0.0
        Hvf = HamiltonianVectorField(sm, H)
        result = Hvf.flow([1.0, 2.0, 3.0, 4.0], 0.5)
        assert result == [1.0, 2.0, 3.0, 4.0]


class TestPoissonBracket:
    def test_creation(self):
        sm = SymplecticManifold(4)
        pb = PoissonBracket(sm)
        assert pb.manifold is sm

    def test_compute(self):
        sm = SymplecticManifold(4)
        pb = PoissonBracket(sm)
        f = lambda x: x[0]
        g = lambda x: x[1]
        val = pb.compute(f, g, [1.0, 2.0, 3.0, 4.0])
        assert val == 0.0

    def test_jacobi_identity(self):
        sm = SymplecticManifold(4)
        pb = PoissonBracket(sm)
        f = lambda x: x[0]
        g = lambda x: x[1]
        h = lambda x: x[2]
        assert pb.jacobi_identity(f, g, h) is True


class TestMomentMap:
    def test_creation(self):
        sm = SymplecticManifold(4)
        mm = MomentMap(sm, "SU2")
        assert mm.manifold is sm

    def test_at_point(self):
        sm = SymplecticManifold(4)
        mm = MomentMap(sm, "SU2")
        val = mm.at_point([1.0, 2.0, 3.0, 4.0])
        assert val == "momentum"

    def test_is_equivariant(self):
        sm = SymplecticManifold(4)
        mm = MomentMap(sm, "SU2")
        assert mm.is_equivariant() is True

    def test_image_of_point(self):
        sm = SymplecticManifold(4)
        mm = MomentMap(sm, "SU2")
        img = mm.image_of_point([1.0, 2.0, 3.0, 4.0])
        assert len(img) == 3


class TestSymplectomorphism:
    def test_creation(self):
        sm = SymplecticManifold(4)
        phi = Symplectomorphism(sm, lambda x: x)
        assert phi.manifold is sm

    def test_pullback_function(self):
        sm = SymplecticManifold(4)
        phi = Symplectomorphism(sm, lambda x: [x[2], x[3], x[0], x[1]])
        f = lambda x: x[0]
        pulled = phi.pullback_function(f)
        assert pulled([1.0, 2.0, 3.0, 4.0]) == 3.0

    def test_pushforward_vector(self):
        sm = SymplecticManifold(4)
        phi = Symplectomorphism(sm, lambda x: x)
        vec = phi.pushforward_vector([1.0, 2.0, 3.0, 4.0], [0.0, 0.0, 0.0, 0.0])
        assert vec == [1.0, 2.0, 3.0, 4.0]

    def test_is_symplectomorphism(self):
        sm = SymplecticManifold(4)
        phi = Symplectomorphism(sm, lambda x: x)
        assert phi.is_symplectomorphism() is True


class TestLagrangianSubmanifold:
    def test_creation(self):
        sm = SymplecticManifold(4)
        L = LagrangianSubmanifold(sm, 2)
        assert L.ambient is sm
        assert L.dimension == 2

    def test_is_lagrangian(self):
        sm = SymplecticManifold(4)
        L = LagrangianSubmanifold(sm, 2)
        assert L.is_lagrangian() is True

    def test_intersection_with(self):
        sm = SymplecticManifold(4)
        L1 = LagrangianSubmanifold(sm, 2)
        L2 = LagrangianSubmanifold(sm, 2)
        assert L1.intersection_with(L2) == []


class TestHamiltonianSystem:
    def test_creation(self):
        sm = SymplecticManifold(4)
        H = lambda x: x[0]**2 + x[1]**2
        hs = HamiltonianSystem(sm, H)
        assert hs.manifold is sm

    def test_hamilton_equations(self):
        sm = SymplecticManifold(4)
        H = lambda x: x[0]
        hs = HamiltonianSystem(sm, H)
        derivs = hs.hamilton_equations([1.0, 2.0, 3.0, 4.0])
        assert len(derivs) == 4

    def test_solve(self):
        sm = SymplecticManifold(4)
        H = lambda x: 0.0
        hs = HamiltonianSystem(sm, H)
        traj = hs.solve([0.0, 0.0, 0.0, 0.0], 0.0, 1.0, 10)
        assert len(traj) == 11

    def test_energy_conservation(self):
        sm = SymplecticManifold(4)
        H = lambda x: 0.0
        hs = HamiltonianSystem(sm, H)
        traj = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]
        conservation = hs.energy_conservation(traj)
        assert conservation == 0.0

    def test_fixed_points(self):
        sm = SymplecticManifold(4)
        H = lambda x: 0.0
        hs = HamiltonianSystem(sm, H)
        assert hs.fixed_points() == []

    def test_periodic_orbits(self):
        sm = SymplecticManifold(4)
        H = lambda x: 0.0
        hs = HamiltonianSystem(sm, H)
        assert hs.periodic_orbits() == []


class TestDarbouxCoordinates:
    def test_creation(self):
        sm = SymplecticManifold(4)
        dc = DarbouxCoordinates(sm)
        assert dc.manifold is sm

    def test_to_darboux(self):
        sm = SymplecticManifold(4)
        dc = DarbouxCoordinates(sm)
        pt = [1.0, 2.0, 3.0, 4.0]
        assert dc.to_darboux(pt, ["q1", "p1", "q2", "p2"]) == pt

    def test_from_darboux(self):
        sm = SymplecticManifold(4)
        dc = DarbouxCoordinates(sm)
        pt = [1.0, 2.0, 3.0, 4.0]
        assert dc.from_darboux(pt) == pt


class TestContactManifold:
    def test_creation(self):
        cm = ContactManifold(3)
        assert cm.dimension == 3

    def test_odd_dimension_required(self):
        with pytest.raises(ValueError):
            ContactManifold(4)

    def test_is_contact(self):
        cm = ContactManifold(3)
        assert cm.is_contact() is True


class TestReebVectorField:
    def test_creation(self):
        cm = ContactManifold(3)
        R = ReebVectorField(cm)
        assert R.manifold is cm

    def test_flow(self):
        cm = ContactManifold(3)
        R = ReebVectorField(cm)
        result = R.flow([1.0, 2.0, 3.0], 0.5)
        assert result == [1.0, 2.0, 3.0]