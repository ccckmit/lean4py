import pytest
from lean4py.optimization import augmented_lagrange


class TestAugmentedLagrange:
    def test_minimize_x2_y2(self):
        """Minimize x^2 + y^2 subject to x + y = 1."""
        f = lambda x: x[0]**2 + x[1]**2
        # Equality: x + y - 1 = 0
        g = lambda x: x[0] + x[1]
        eq_constraints = [(g, 1.0)]
        # No inequality constraints
        ineq_constraints = []
        x0 = [0.5, 0.5]  # Start at solution
        x_opt, f_opt, lam, mu = augmented_lagrange(
            f, eq_constraints, ineq_constraints, x0)
        # Should stay near solution
        assert abs(x_opt[0] + x_opt[1] - 1.0) < 0.1
        assert abs(f_opt - 0.5) < 0.1

    def test_minimize_xy(self):
        """Minimize xy subject to x + y = 10."""
        f = lambda x: x[0] * x[1]
        g = lambda x: x[0] + x[1]
        eq_constraints = [(g, 10.0)]
        ineq_constraints = []
        x0 = [5.0, 5.0]
        x_opt, f_opt, lam, mu = augmented_lagrange(
            f, eq_constraints, ineq_constraints, x0)
        assert abs(x_opt[0] + x_opt[1] - 10.0) < 0.1
