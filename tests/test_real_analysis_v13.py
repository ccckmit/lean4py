import pytest
import math
from lean4py.real_analysis import euler_method, runge_kutta_4


class TestEulerMethod:
    def test_exp_growth(self):
        """dy/dt = y, y(0)=1, solution: y=e^t."""
        f = lambda t, y: [y[0]]
        t_vals, y_vals = euler_method(f, [1.0], (0.0, 1.0), dt=0.01)
        # y(1) should be close to e
        y_final = y_vals[-1][0]
        assert abs(y_final - math.e) < 0.1

    def test_constant(self):
        """dy/dt = 0, y(0)=5, should stay at 5."""
        f = lambda t, y: [0.0]
        t_vals, y_vals = euler_method(f, [5.0], (0.0, 2.0), dt=0.1)
        for y in y_vals:
            assert abs(y[0] - 5.0) < 1e-6


class TestRungeKutta4:
    def test_exp_growth(self):
        """dy/dt = y, y(0)=1, solution: y=e^t."""
        f = lambda t, y: [y[0]]
        t_vals, y_vals = runge_kutta_4(f, [1.0], (0.0, 1.0), dt=0.1)
        y_final = y_vals[-1][0]
        assert abs(y_final - math.e) < 0.05  # RK4 more accurate

    def test_harmonic_oscillator(self):
        """d²x/dt² = -x, solution: x=cos(t)."""
        # Convert to system: dy0/dt = y1, dy1/dt = -y0
        f = lambda t, y: [y[1], -y[0]]
        t_vals, y_vals = runge_kutta_4(f, [1.0, 0.0], (0.0, 3.14159), dt=0.01)
        x_final = y_vals[-1][0]
        assert abs(x_final - (-1.0)) < 0.1  # cos(π) = -1
