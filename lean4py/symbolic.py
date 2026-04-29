from typing import Optional

try:
    import sympy
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False


def symbolic_derivative(expr_str: str, var: str = 'x') -> str:
    """Compute symbolic derivative.
    
    Args:
        expr_str: Expression like "x**2 + 3*x"
        var: Variable to differentiate
        
    Returns:
        Derivative as string
        
    Raises:
        ImportError: If sympy is not available
    """
    if not SYMPY_AVAILABLE:
        raise ImportError("sympy is required for symbolic computation. Install with: pip install sympy")
    import sympy as sp
    x = sp.symbols(var)
    expr = sp.sympify(expr_str)
    deriv = sp.diff(expr, x)
    return str(deriv)


def symbolic_integral(expr_str: str, var: str = 'x') -> str:
    """Compute symbolic indefinite integral.
    
    Args:
        expr_str: Expression like "x**2 + 3*x"
        var: Variable to integrate
        
    Returns:
        Indefinite integral as string (includes + C)
        
    Raises:
        ImportError: If sympy is not available
    """
    if not SYMPY_AVAILABLE:
        raise ImportError("sympy is required for symbolic computation. Install with: pip install sympy")
    import sympy as sp
    x = sp.symbols(var)
    expr = sp.sympify(expr_str)
    integral = sp.integrate(expr, x)
    return str(integral) + " + C"


def symbolic_simplify(expr_str: str) -> str:
    """Simplify a symbolic expression.
    
    Args:
        expr_str: Expression like "x**2 + 2*x**2 + 3*x"
        
    Returns:
        Simplified expression as string
    """
    if not SYMPY_AVAILABLE:
        raise ImportError("sympy is required for symbolic computation. Install with: pip install sympy")
    import sympy as sp
    expr = sp.sympify(expr_str)
    simplified = sp.simplify(expr)
    return str(simplified)
