"""Tests for enhanced differential geometry module."""

import pytest
from lean4py.differential_geometry_enhanced import (
    GeodesicEquation, SectionalCurvature, RicciCurvature, GaussBonnet
)
import math


class TestGeodesicEquation:
    """Test geodesic equation."""

    def test_christoffel_symbols(self):
        metric = [[1.0, 0.0], [0.0, 1.0]]  # Euclidean
        symbols = GeodesicEquation.christoffel_symbols(metric, dim=2)
        assert len(symbols) == 2
        assert len(symbols[0]) == 2
        assert len(symbols[0][0]) == 2

    def test_geodesic_equation(self):
        dx_dtau = [1.0, 0.0]
        christoffel = [[[0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0]]]
        result = GeodesicEquation.geodesic_equation(dx_dtau, christoffel)
        assert len(result) == 2

    def test_solve_geodesic(self):
        initial_pos = [0.0, 0.0]
        initial_vel = [1.0, 1.0]
        path = GeodesicEquation.solve_geodesic(initial_pos, initial_vel, steps=10)
        assert len(path) == 11


class TestSectionalCurvature:
    """Test sectional curvature."""

    def test_compute(self):
        metric = [[1.0, 0.0], [0.0, 1.0]]
        riemann = [[[[0.0]*2 for _ in range(2)] for _ in range(2)] for _ in range(2)]
        vector1 = [1.0, 0.0]
        vector2 = [0.0, 1.0]
        K = SectionalCurvature.compute(metric, riemann, vector1, vector2)
        assert isinstance(K, float)


class TestRicciCurvature:
    """Test Ricci curvature."""

    def test_compute(self):
        riemann = [[[[0.0]*2 for _ in range(2)] for _ in range(2)] for _ in range(2)]
        ricci = RicciCurvature.compute(riemann, dim=2)
        assert len(ricci) == 2
        assert len(ricci[0]) == 2

    def test_scalar_curvature(self):
        ricci = [[1.0, 0.0], [0.0, 1.0]]
        R = RicciCurvature.scalar_curvature(ricci)
        assert isinstance(R, float)


class TestGaussBonnet:
    """Test Gauss-Bonnet theorem."""

    def test_euler_characteristic(self):
        assert GaussBonnet.euler_characteristic(genus=0) == 2
        assert GaussBonnet.euler_characteristic(genus=1) == 0

    def test_total_curvature(self):
        assert GaussBonnet.total_curvature(genus=0) == pytest.approx(4 * math.pi, abs=1e-10)

    def test_is_sphere(self):
        assert GaussBonnet.is_sphere(curvature=1.0, area=4*math.pi) is True
