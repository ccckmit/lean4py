import pytest
from lean4py.ml_basics import linear_regression_ml, logistic_regression


class TestLinearRegressionML:
    def test_perfect_fit(self):
        """Perfect linear relationship y = 2x."""
        X = [[1.0], [2.0], [3.0], [4.0], [5.0]]
        y = [2.0, 4.0, 6.0, 8.0, 10.0]
        coeffs, intercept = linear_regression_ml(X, y)
        assert len(coeffs) == 1
        assert abs(coeffs[0] - 2.0) < 0.5
        assert abs(intercept) < 0.5


class TestLogisticRegression:
    def test_separable(self):
        """Linearly separable data."""
        X = [[1.0], [2.0], [3.0], [100.0], [200.0]]
        y = [0, 0, 0, 1, 1]
        beta = logistic_regression(X, y, learning_rate=0.1, max_iter=1000)
        assert len(beta) == 2  # intercept + 1 feature

    def test_constant_features(self):
        """All features same."""
        X = [[1.0], [1.0], [1.0]]
        y = [0, 0, 0]
        beta = logistic_regression(X, y)
        assert len(beta) == 2
