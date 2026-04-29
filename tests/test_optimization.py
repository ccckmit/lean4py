import pytest
from lean4py.optimization import gradient_descent, linear_programming


class TestGradientDescent:
    def test_minimize_x_squared(self):
        """f(x) = x^2, minimum at x=0."""
        f = lambda x: x ** 2
        x_opt, f_opt = gradient_descent(f, x0=5.0, learning_rate=0.1, max_iter=1000)
        assert abs(x_opt) < 0.1
        assert abs(f_opt) < 0.01

    def test_minimize_quadratic(self):
        """f(x) = (x-3)^2 + 2, minimum at x=3."""
        f = lambda x: (x - 3) ** 2 + 2
        x_opt, f_opt = gradient_descent(f, x0=0.0, learning_rate=0.1, max_iter=1000)
        assert abs(x_opt - 3.0) < 0.1
        assert abs(f_opt - 2.0) < 0.1

    def test_convergence_tol(self):
        """Should stop when tolerance met."""
        f = lambda x: x ** 2
        x_opt, f_opt = gradient_descent(f, x0=10.0, learning_rate=0.01, tol=1e-3, max_iter=10000)
        assert f_opt < 1e-2  # Should be close to 0


class TestLinearProgramming:
    def test_simple_lp(self):
        """Minimize x + y subject to x + y >= 1, x >= 0, y >= 0."""
        try:
            import scipy
            c = [1, 1]  # Minimize x + y
            A = [[-1, -1]]  # -x - y <= -1  =>  x + y >= 1
            b = [-1]
            result = linear_programming(c, A, b)
            if result:
                opt_val, opt_x = result
                assert opt_val == pytest.approx(1.0, abs=0.1)
        except ImportError:
            pytest.skip("scipy not available")

    def test_lp_infeasible(self):
        """No solution: x >= 2 and x <= 1."""
        try:
            import scipy
            c = [1]
            A = [[1], [-1]]  # x <= 1, -x <= -2 => x >= 2
            b = [1, -2]
            result = linear_programming(c, A, b)
            assert result is None
        except ImportError:
            pytest.skip("scipy not available")
