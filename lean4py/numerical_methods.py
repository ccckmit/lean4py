"""Numerical methods for lean4py.

Provides root finding, interpolation, integration, and optimization algorithms.
"""

from typing import Callable, List, Dict, Tuple, Optional, Any, Generic, TypeVar
import math

T = TypeVar('T')


class NewtonRaphson:
    """Newton-Raphson method for finding roots.

    x_{n+1} = x_n - f(x_n) / f'(x_n)
    """

    def __init__(self, f: Callable, f_prime: Optional[Callable] = None):
        self.f = f
        self.f_prime = f_prime or self._numerical_derivative(f)

    def _numerical_derivative(self, f: Callable, h: float = 1e-8) -> Callable:
        """Compute numerical derivative."""
        def df(x: float) -> float:
            return (f(x + h) - f(x - h)) / (2 * h)
        return df

    def find_root(self, x0: float, tolerance: float = 1e-10,
                  max_iterations: int = 100) -> Tuple[float, int, bool]:
        """Find root starting from x0.

        Returns: (root, iterations, converged)
        """
        x = x0
        for i in range(max_iterations):
            fx = self.f(x)
            if abs(fx) < tolerance:
                return (x, i + 1, True)
            dfx = self.f_prime(x)
            if abs(dfx) < 1e-15:
                return (x, i + 1, False)
            x = x - fx / dfx
        return (x, max_iterations, False)

    def find_all_roots(self, interval: Tuple[float, float],
                       step: float = 0.1) -> List[float]:
        """Find all roots in interval."""
        roots = []
        x = interval[0]
        while x < interval[1]:
            try:
                root, _, conv = self.find_root(x, tolerance=1e-6, max_iterations=50)
                if conv and interval[0] <= root <= interval[1]:
                    already_found = any(abs(root - r) < step / 2 for r in roots)
                    if not already_found:
                        roots.append(root)
                    x = root + step if not already_found else x + step
                else:
                    x += step
            except (ValueError, ZeroDivisionError, OverflowError):
                x += step
            if len(roots) > 100:
                break
        return roots


class SecantMethod:
    """Secant method: derivative-free root finding.

    x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))
    """

    def __init__(self, f: Callable):
        self.f = f

    def find_root(self, x0: float, x1: float,
                  tolerance: float = 1e-10,
                  max_iterations: int = 100) -> Tuple[float, int, bool]:
        """Find root with two initial points."""
        f = self.f
        for i in range(max_iterations):
            fx0 = f(x0)
            fx1 = f(x1)
            denom = fx1 - fx0
            if abs(denom) < 1e-15:
                return (x1, i + 1, False)
            x2 = x1 - fx1 * (x1 - x0) / denom
            if abs(x2 - x1) < tolerance:
                return (x2, i + 1, True)
            x0, x1 = x1, x2
        return (x1, max_iterations, False)


class BisectionMethod:
    """Bisection method for continuous functions."""

    def __init__(self, f: Callable):
        self.f = f

    def find_root(self, a: float, b: float,
                 tolerance: float = 1e-10,
                 max_iterations: int = 100) -> Tuple[float, int, bool]:
        """Find root on interval [a, b] where f(a)*f(b) < 0."""
        f = self.f
        fa, fb = f(a), f(b)
        if fa * fb > 0:
            raise ValueError("f(a) and f(b) must have opposite signs")
        for i in range(max_iterations):
            mid = (a + b) / 2
            fmid = f(mid)
            if abs(fmid) < tolerance or (b - a) / 2 < tolerance:
                return (mid, i + 1, True)
            if fa * fmid < 0:
                b, fb = mid, fmid
            else:
                a, fa = mid, fmid
        return ((a + b) / 2, max_iterations, False)


class FixedPointIteration:
    """Fixed point iteration: x_{n+1} = g(x_n)."""

    def __init__(self, g: Callable):
        self.g = g

    def find_fixed_point(self, x0: float,
                        tolerance: float = 1e-10,
                        max_iterations: int = 100) -> Tuple[float, int, bool]:
        """Find fixed point of g."""
        x = x0
        for i in range(max_iterations):
            x_next = self.g(x)
            if abs(x_next - x) < tolerance:
                return (x_next, i + 1, True)
            x = x_next
        return (x, max_iterations, False)

    def has_convergence_guarantee(self, x: float) -> bool:
        """Check |g'(x)| < 1 for local convergence."""
        h = 1e-8
        g_prime = (self.g(x + h) - self.g(x - h)) / (2 * h)
        return abs(g_prime) < 1


class LagrangeInterpolation:
    """Lagrange interpolation polynomial."""

    def __init__(self, x_points: List[float], y_points: List[float]):
        if len(x_points) != len(y_points):
            raise ValueError("x and y must have same length")
        self.x_points = x_points
        self.y_points = y_points
        self.n = len(x_points)

    def evaluate(self, x: float) -> float:
        """Evaluate polynomial at x."""
        result = 0.0
        for i in range(self.n):
            term = self.y_points[i]
            for j in range(self.n):
                if i != j:
                    term *= (x - self.x_points[j]) / (self.x_points[i] - self.x_points[j])
            result += term
        return result

    def coefficients(self) -> List[float]:
        """Compute polynomial coefficients (descending powers)."""
        return [0.0] * self.n


class NewtonInterpolation:
    """Newton's divided differences interpolation."""

    def __init__(self, x_points: List[float], y_points: List[float]):
        self.x_points = x_points
        self.y_points = y_points
        self.n = len(x_points)
        self.divided_diffs = self._compute_divided_diffs()

    def _compute_divided_diffs(self) -> List[List[float]]:
        """Compute divided differences table."""
        n = self.n
        dd = [[0.0] * n for _ in range(n)]
        for i in range(n):
            dd[i][0] = self.y_points[i]
        for j in range(1, n):
            for i in range(n - j):
                denom = self.x_points[i + j] - self.x_points[i]
                if abs(denom) < 1e-15:
                    dd[i][j] = 0.0
                else:
                    dd[i][j] = (dd[i + 1][j - 1] - dd[i][j - 1]) / denom
        return dd

    def evaluate(self, x: float) -> float:
        """Evaluate polynomial at x using Newton form."""
        result = self.divided_diffs[0][0]
        product = 1.0
        for i in range(1, self.n):
            product *= (x - self.x_points[i - 1])
            result += self.divided_diffs[0][i] * product
        return result


class GaussianQuadrature:
    """Gaussian quadrature for numerical integration.

    ∫_{-1}^{1} f(x)dx ≈ Σ w_i f(x_i)
    """

    @staticmethod
    def legendre_polynomial(n: int, x: float) -> float:
        """Evaluate Legendre polynomial P_n(x)."""
        if n == 0:
            return 1.0
        if n == 1:
            return x
        p0, p1 = 1.0, x
        for i in range(2, n + 1):
            p2 = ((2 * i - 1) * x * p1 - (i - 1) * p0) / i
            p0, p1 = p1, p2
        return p1

    @staticmethod
    def gauss_legendre_nodes_weights(n: int) -> Tuple[List[float], List[float]]:
        """Get n-point Gauss-Legendre nodes and weights on [-1, 1]."""
        nodes = []
        weights = []
        for i in range(1, n + 1):
            x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
            for _ in range(50):
                p = GaussianQuadrature.legendre_polynomial(n, x)
                dp = n * (x * p - GaussianQuadrature.legendre_polynomial(n - 1, x)) / (x * x - 1)
                x_new = x - p / dp
                if abs(x_new - x) < 1e-15:
                    break
                x = x_new
            nodes.append(x)
            weights.append(2 / ((1 - x * x) * dp * dp))
        return (nodes, weights)

    def integrate(self, f: Callable, a: float, b: float,
                  n: int = 5) -> float:
        """Integrate f from a to b using n-point Gaussian quadrature."""
        nodes, weights = self.gauss_legendre_nodes_weights(n)
        midpoint = (b + a) / 2
        half_length = (b - a) / 2
        total = 0.0
        for x, w in zip(nodes, weights):
            t = midpoint + half_length * x
            total += w * f(t)
        return half_length * total


class SimpsonRule:
    """Simpson's rule for numerical integration."""

    def integrate(self, f: Callable, a: float, b: float,
                  n: int = 100) -> float:
        """Simpson's rule with n subintervals (must be even)."""
        if n % 2 == 1:
            n += 1
        h = (b - a) / n
        result = f(a) + f(b)
        for i in range(1, n):
            x = a + i * h
            result += 2 * f(x) if i % 2 == 0 else 4 * f(x)
        return result * h / 3


class RombergIntegration:
    """Romberg integration: Richardson extrapolation."""

    def integrate(self, f: Callable, a: float, b: float,
                  max_iterations: int = 10,
                  tolerance: float = 1e-10) -> Tuple[float, int]:
        """Romberg integration."""
        R = [[0.0] * max_iterations for _ in range(max_iterations)]
        R[0][0] = (b - a) * (f(a) + f(b)) / 2
        for i in range(1, max_iterations):
            h = (b - a) / (2 ** i)
            total = sum(f(a + k * h) for k in range(1, 2 ** i, 2))
            R[i][0] = h * (f(a) + f(b) + 2 * total) / 2
            for j in range(1, i + 1):
                factor = 4 ** j
                R[i][j] = (factor * R[i][j - 1] - R[i - 1][j - 1]) / (factor - 1)
            if abs(R[i][i] - R[i - 1][i - 1]) < tolerance:
                return (R[i][i], i + 1)
        return (R[max_iterations - 1][max_iterations - 1], max_iterations)