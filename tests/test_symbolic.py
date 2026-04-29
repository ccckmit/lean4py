import pytest
from lean4py.symbolic import symbolic_derivative, symbolic_integral, symbolic_simplify


class TestSymbolicDerivative:
    def test_power_rule(self):
        result = symbolic_derivative("x**2")
        assert "2*x" in result or "2*x" in result.replace(" ", "")

    def test_linear(self):
        result = symbolic_derivative("3*x + 5")
        assert "3" in result

    def test_constant(self):
        result = symbolic_derivative("42")
        assert "0" in result

    def test_sin(self):
        try:
            import sympy
            result = symbolic_derivative("sin(x)")
            assert "cos" in result.lower()
        except ImportError:
            pytest.skip("sympy not available")


class TestSymbolicIntegral:
    def test_power_rule(self):
        result = symbolic_integral("x**2")
        assert "x**3" in result or "x**3/3" in result

    def test_linear(self):
        result = symbolic_integral("3*x")
        assert "3*x**2/2" in result or "1.5*x**2" in result

    def test_constant(self):
        result = symbolic_integral("5")
        assert "5*x" in result


class TestSymbolicSimplify:
    def test_combine_like_terms(self):
        result = symbolic_simplify("x**2 + 2*x**2 + 3*x")
        # sympy may factor: 3*x**2 + 3*x -> 3*x*(x + 1)
        assert "3*x" in result

    def test_cancel_terms(self):
        result = symbolic_simplify("x + x**2 - x")
        assert "x**2" in result
