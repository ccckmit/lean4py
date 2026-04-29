import pytest
from lean4py.statistics import linear_regression_diagnostics


class TestLinearRegressionDiagnostics:
    def test_basic(self):
        """Simple linear regression diagnostics."""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [2.0, 4.0, 6.0, 8.0, 10.0]  # y = 2x
        diag = linear_regression_diagnostics(x, y)
        assert 'slope' in diag
        assert 'intercept' in diag
        assert abs(diag['slope'] - 2.0) < 0.1
        assert abs(diag['intercept']) < 0.1
        assert 0.9 < diag['r_squared'] <= 1.0

    def test_r_squared(self):
        """Perfect fit should have R² = 1."""
        x = [1.0, 2.0, 3.0]
        y = [2.0, 4.0, 6.0]
        diag = linear_regression_diagnostics(x, y)
        assert abs(diag['r_squared'] - 1.0) < 1e-10

    def test_residuals(self):
        """Residuals should sum to ~0."""
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [2.1, 3.9, 6.2, 7.8, 10.1]
        diag = linear_regression_diagnostics(x, y)
        residuals = diag['residuals']
        assert abs(sum(residuals)) < 0.1
