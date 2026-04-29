from typing import Callable, Tuple, List, Optional


def gradient_descent(
    f: Callable[[float], float],
    x0: float,
    learning_rate: float = 0.01,
    max_iter: int = 1000,
    tol: float = 1e-6
) -> Tuple[float, float]:
    """Gradient descent optimization (numerical gradient).
    
    Args:
        f: Objective function f(x)
        x0: Initial point
        learning_rate: Step size
        max_iter: Maximum iterations
        tol: Convergence tolerance on |x_new - x|
        
    Returns:
        (x_opt, f_opt): Optimal point and function value
    """
    x = x0
    h = 1e-5  # For numerical derivative
    
    for _ in range(max_iter):
        # Numerical gradient
        grad = (f(x + h) - f(x - h)) / (2 * h)
        x_new = x - learning_rate * grad
        
        if abs(x_new - x) < tol:
            return x_new, f(x_new)
        x = x_new
    
    return x, f(x)


def newton_method(
    f: Callable[[float], float],
    x0: float,
    max_iter: int = 100,
    tol: float = 1e-6
) -> Tuple[float, float]:
    """Newton's method for optimization (second-order).
    
    Args:
        f: Objective function
        x0: Initial point
        max_iter: Maximum iterations
        tol: Convergence tolerance on |x_new - x|
        
    Returns:
        (x_opt, f_opt): Optimal point and value
    """
    x = x0
    h = 1e-5
    
    for _ in range(max_iter):
        # First derivative
        f_prime = (f(x + h) - f(x - h)) / (2 * h)
        # Second derivative
        f_double = (f(x + h) - 2*f(x) + f(x - h)) / (h ** 2)
        
        if abs(f_double) < 1e-10:
            break
            
        x_new = x - f_prime / f_double
        
        if abs(x_new - x) < tol:
            return x_new, f(x_new)
        x = x_new
    
    return x, f(x)


def conjugate_gradient(
    A: Callable[[List[float]], List[float]],
    b: List[float],
    x0: Optional[List[float]] = None,
    max_iter: int = 1000,
    tol: float = 1e-6
) -> List[float]:
    """Conjugate Gradient method for solving Ax = b.
    
    Args:
        A: Function that computes A @ x (linear operator)
        b: Right-hand side vector
        x0: Initial guess (zeros if None)
        max_iter: Maximum iterations
        tol: Convergence tolerance on residual norm
        
    Returns:
        Solution vector x
    """
    n = len(b)
    if x0 is None:
        x = [0.0] * n
    else:
        x = x0[:]
    
    # Initial residual r = b - Ax
    Ax = A(x)
    r = [b[i] - Ax[i] for i in range(n)]
    r_dot_r = sum(r[i] * r[i] for i in range(n))
    
    # If b = 0, solution is x = 0
    if r_dot_r < tol:
        return x
    
    p = r[:]  # Initial search direction
    
    for _ in range(min(max_iter, n)):
        Ap = A(p)
        pAp = sum(p[i] * Ap[i] for i in range(n))
        if pAp < 1e-15:
            return x
        alpha = r_dot_r / pAp
        
        x = [x[i] + alpha * p[i] for i in range(n)]
        r_new = [r[i] - alpha * Ap[i] for i in range(n)]
        
        r_new_dot = sum(r_new[i] * r_new[i] for i in range(n))
        if r_new_dot ** 0.5 < tol:
            return x
        
        beta = r_new_dot / r_dot_r
        p = [r_new[i] + beta * p[i] for i in range(n)]
        r = r_new
        r_dot_r = r_new_dot
    
    return x
    
    return x


def linear_programming(
    c: List[float],
    A: List[List[float]],
    b: List[float],
    method: str = 'simplex'
) -> Optional[Tuple[float, List[float]]]:
    """Linear programming: minimize c^T x subject to Ax <= b.
    
    Uses scipy if available, otherwise raises ImportError.
    
    Args:
        c: Cost vector (minimize c^T x)
        A: Constraint matrix (Ax <= b)
        b: Constraint bounds
        method: 'simplex' or 'interior-point'
        
    Returns:
        (optimal_value, optimal_x) or None if infeasible
    """
    try:
        import numpy as np
        from scipy.optimize import linprog
        result = linprog(c, A_ub=A, b_ub=b, method='highs')
        if result.success:
            return result.fun, list(result.x)
        return None
    except ImportError:
        raise ImportError("scipy is required for linear_programming()")
