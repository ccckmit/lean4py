"""Tests for algebraic_geometry module (v1.19)."""
import pytest
from lean4py.algebraic_geometry import (
    ProjectiveSpace, AlgebraicCurve, RiemannRochResult, Divisor, LineBundle,
    EllipticCurve, Grassmannian, RationalNormalCurve, blowing_up, SheafCohomologyAlgebraic
)


class TestProjectiveSpace:
    def test_creation(self):
        ps = ProjectiveSpace(2)
        assert ps.dimension == 2

    def test_creation_with_field(self):
        ps = ProjectiveSpace(3, "R")
        assert ps.field == "R"

    def test_homogeneous_coordinates(self):
        ps = ProjectiveSpace(2)
        coords = ps.homogeneous_coordinates()
        assert len(coords) == 3

    def test_chart(self):
        ps = ProjectiveSpace(2)
        chart = ps.chart(0)
        assert isinstance(chart, dict)

    def test_is_smooth(self):
        ps = ProjectiveSpace(3)
        assert ps.is_smooth() is True

    def test_Picard_group(self):
        ps = ProjectiveSpace(2)
        assert ps.Picard_group() == "Z"

    def test_divisor_class(self):
        ps = ProjectiveSpace(2)
        d = ps.divisor_class(3)
        assert isinstance(d, Divisor)

    def test_betti_numbers(self):
        ps = ProjectiveSpace(2)
        bn = ps.betti_numbers()
        assert len(bn) == 5


class TestAlgebraicCurve:
    def test_creation(self):
        ac = AlgebraicCurve(2)
        assert ac.genus == 2

    def test_creation_with_equation(self):
        ac = AlgebraicCurve(1, "y^2 = x^3 + x")
        assert ac.equation == "y^2 = x^3 + x"

    def test_genus_formula(self):
        ac = AlgebraicCurve(3)
        assert ac.genus_formula() == 3

    def test_canonical_divisor(self):
        ac = AlgebraicCurve(3)
        k = ac.canonical_divisor()
        assert isinstance(k, Divisor)
        assert k.degree == 4

    def test_riemann_roch(self):
        ac = AlgebraicCurve(2)
        D = Divisor("D", 3)
        result = ac.riemann_roch(D)
        assert isinstance(result, RiemannRochResult)


class TestRiemannRochResult:
    def test_creation(self):
        rr = RiemannRochResult(0, 0, 3, 2)
        assert rr.deg_D == 3
        assert rr.genus == 2

    def test_compute(self):
        rr = RiemannRochResult(0, 0, 3, 2)
        result = rr.compute()
        assert result == 2


class TestDivisor:
    def test_creation(self):
        d = Divisor("D", 3)
        assert d.name == "D"
        assert d.degree == 3

    def test_add_point(self):
        d = Divisor("D", 0)
        d.add_point("P", 2)
        assert d.points["P"] == 2

    def test_is_effective(self):
        d1 = Divisor("D", 1)
        d1.add_point("P", 2)
        assert d1.is_effective() is True

    def test_linear_equivalence_class(self):
        d = Divisor("D", 3)
        result = d.linear_equivalence_class()
        assert "D" in result

    def test_degree_check(self):
        d = Divisor("D", 5)
        assert d.degree_check() == 5

    def test_intersection_number(self):
        d = Divisor("D", 3)
        result = d.intersection_number(Divisor("E", 2))
        assert isinstance(result, int)


class TestLineBundle:
    def test_creation(self):
        lb = LineBundle("variety")
        assert lb.base == "variety"

    def test_add_section(self):
        lb = LineBundle("variety")
        lb.add_section("U", "section")
        assert "U" in lb.sections

    def test_global_sections_dim(self):
        lb = LineBundle("variety")
        lb.add_section("X", "s")
        assert lb.global_sections_dim() == 1

    def test_degree(self):
        lb = LineBundle("variety")
        assert lb.degree() == 0

    def test_is_very_ample(self):
        lb = LineBundle("variety")
        for i in range(3):
            lb.add_section(f"U{i}", f"s{i}")
        assert lb.is_very_ample() is True

    def test_pullback(self):
        lb = LineBundle("variety")
        result = lb.pullback(lambda x: x)
        assert isinstance(result, LineBundle)


class TestEllipticCurve:
    def test_creation(self):
        ec = EllipticCurve()
        assert ec.genus == 1

    def test_creation_with_j(self):
        ec = EllipticCurve(j_invariant=1728.0)
        assert ec.j_invariant == 1728.0

    def test_group_add(self):
        ec = EllipticCurve()
        result = ec.group_add("P", "Q")
        assert isinstance(result, str)

    def test_negation(self):
        ec = EllipticCurve()
        result = ec.negation("P")
        assert isinstance(result, str)

    def test_is_supersingular(self):
        ec = EllipticCurve()
        assert ec.is_supersingular() is False


class TestGrassmannian:
    def test_creation(self):
        g = Grassmannian(2, 5)
        assert g.k == 2
        assert g.n == 5

    def test_dimension(self):
        g = Grassmannian(2, 5)
        assert g.dimension == 6

    def test_plucker_embedding(self):
        g = Grassmannian(1, 3)
        ps = g.plucker_embedding()
        assert isinstance(ps, ProjectiveSpace)

    def test_schubert_cell(self):
        g = Grassmannian(1, 4)
        result = g.schubert_cell([1, 2])
        assert "Schubert" in result


class TestRationalNormalCurve:
    def test_creation(self):
        rnc = RationalNormalCurve(3)
        assert rnc.degree == 3
        assert rnc.dimension == 3

    def test_is_algorithmically_rational(self):
        rnc = RationalNormalCurve(4)
        assert rnc.is_algorithmically_rational() is True

    def test_projection_map(self):
        rnc = RationalNormalCurve(3)
        proj = rnc.projection_map(0)
        assert callable(proj)


class TestBlowingUp:
    def test_creation(self):
        bu = blowing_up("variety", "center")
        assert bu.variety == "variety"
        assert bu.center == "center"

    def test_exceptional_divisor(self):
        bu = blowing_up("variety", "center")
        E = bu.exceptional_divisor()
        assert isinstance(E, Divisor)
        assert E.name == "E"

    def test_strict_transform(self):
        bu = blowing_up("variety", "center")
        result = bu.strict_transform("subvariety")
        assert "subvariety" in result

    def test_resolution_of_singularities(self):
        bu = blowing_up("variety", "center")
        assert bu.resolution_of_singularities() is True


class TestSheafCohomologyAlgebraic:
    def test_creation(self):
        sc = SheafCohomologyAlgebraic("variety")
        assert sc.variety == "variety"

    def test_H0(self):
        sc = SheafCohomologyAlgebraic("variety")
        result = sc.H0("sheaf")
        assert isinstance(result, int)

    def test_H1(self):
        sc = SheafCohomologyAlgebraic("variety")
        result = sc.H1("sheaf")
        assert isinstance(result, int)

    def test_RiemannRoch_for_curves(self):
        sc = SheafCohomologyAlgebraic("curve")
        c = AlgebraicCurve(2)
        l = LineBundle("variety")
        result = sc.RiemannRoch_for_curves(c, l)
        assert isinstance(result, int)