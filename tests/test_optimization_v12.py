import pytest
import math
from lean4py.optimization import conjugate_gradient


class TestConjugateGradient:
    def test_solve_identity(self):
        """Solve Ix = b, should give x = b."""
        A = lambda x: x  # Identity operator
        b = [1.0, 2.0, 3.0]
        x = conjugate_gradient(A, b)
        assert all(abs(x[i] - b[i]) < 1e-5 for i in range(len(b)))

    def test_solve_2x2(self):
        """Solve [[2,0],[0,2]]x = [2,4] -> x = [1,2]."""
        A = lambda x: [2*x[0], 2*x[1]]
        b = [2.0, 4.0]
        x = conjugate_gradient(A, b)
        assert abs(x[0] - 1.0) < 1e-5
        assert abs(x[1] - 2.0) < 1e-5

    def test_zero_rhs(self):
        """Zero RHS should give zero solution."""
        A = lambda x: [2*x[0] + x[1], x[0] + 2*x[1]]
        b = [0.0, 0.0]
        x = conjugate_gradient(A, b)
        assert all(abs(xi) < 1e-5 for xi in x)
