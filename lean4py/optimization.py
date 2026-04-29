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


def lagrange_multiplier(
    f: Callable[[List[float]], float],
    constraints: List[Tuple[Callable[[List[float]], float], float]],
    x0: List[float]
) -> Tuple[List[float], float, List[float]]:
    """Lagrange multiplier method for equality-constrained optimization.
    
    Minimize f(x) subject to g_i(x) = target_i for all i.
    
    Args:
        f: Objective function
        constraints: List of (g_i, target_i) pairs
        x0: Initial guess
        
    Returns:
        (x_opt, f_opt, lambda_opt)
    """
    # Simple implementation using gradient descent on augmented Lagrangian
    import random
    x = x0[:]
    n = len(x0)
    m = len(constraints)
    lam = [0.0] * m
    lr = 0.01
    rho = 0.1  # Penalty parameter
    
    for _ in range(1000):
        # Compute constraint violations
        violations = []
        for g, target in constraints:
            violations.append(g(x) - target)
        
        # Check convergence
        if all(abs(v) < 1e-6 for v in violations):
            break
        
        # Gradient descent step on augmented Lagrangian
        # L = f(x) + Σ λ_i * (g_i(x) - target_i) + (rho/2) * Σ (g_i(x) - target_i)^2
        # Simplified: numerical gradient
        h = 1e-5
        grad_f = [(f([x[j] + (h if j==i else x[j]) for j in range(n)]) - f(x)) / h
                  for i in range(n)]
        
        grad_L = grad_f[:]
        for i, (g, target) in enumerate(constraints):
            # ∂L/∂x = ∇f + Σ λ_i * ∇g_i + rho * (g_i - target) * ∇g_i
            grad_g = [(g([x[j] + (h if j==k else x[j]) for j in range(n)]) - g(x)) / h
                      for k in range(n)]
            for j in range(n):
                grad_L[j] += lam[i] * grad_g[j] + rho * violations[i] * grad_g[j]
        
        x = [x[j] - lr * grad_L[j] for j in range(n)]
        
        # Update Lagrange multipliers
        for i, (g, target) in enumerate(constraints):
            lam[i] += rho * violations[i]
    
    return x, f(x), lam


def penalty_method(
    f: Callable[[List[float]], float],
    inequalities: List[Tuple[Callable[[List[float]], float], float]],
    x0: List[float],
    mu: float = 10.0,
    max_iter: int = 100
) -> Tuple[List[float], float]:
    """Penalty method for inequality-constrained optimization.
    
    Minimize f(x) subject to g_i(x) <= 0 for all i.
    
    Args:
        f: Objective function
        inequalities: List of (g_i, _) pairs (g_i(x) <= 0)
        x0: Initial guess
        mu: Penalty parameter
        max_iter: Maximum iterations
        
    Returns:
        (x_opt, f_opt)
    """
    x = x0[:]
    n = len(x0)
    
    for iter in range(max_iter):
        # Augmented objective: f(x) + (mu/2) * Σ max(0, g_i(x))^2
        def augmented(x_val):
            total = f(x_val)
            for g, _ in inequalities:
                violation = max(0, g(x_val))
                total += (mu / 2) * violation ** 2
            return total
        
        # Check convergence
        max_violation = max(max(0, g(x)) for g, _ in inequalities)
        if max_violation < 1e-6:
            break
        
        # Gradient descent on augmented function
        h = 1e-5
        grad = [(augmented([x[j] + (h if j==i else x[j]) for j in range(n)]) - 
                  augmented(x)) / h
                  for i in range(n)]
        
        learning_rate = 0.01
        x = [x[j] - learning_rate * grad[j] for j in range(n)]
        
        mu *= 2  # Increase penalty
    
    return x, f(x)


def augmented_lagrange(
    f: Callable[[List[float]], float],
    eq_constraints: List[Tuple[Callable[[List[float]], float], float]],
    ineq_constraints: List[Tuple[Callable[[List[float]], float], float]],
    x0: List[float],
    max_iter: int = 100,
    tol: float = 1e-6
) -> Tuple[List[float], float, List[float], List[float]]:
    """Augmented Lagrange method.
    
    Minimize f(x) subject to:
        g_i(x) = eq_target_i  (equality)
        h_j(x) <= ineq_target_j  (inequality)
    
    Returns:
        (x_opt, f_opt, lambda_opt, mu_opt)
    """
    import math
    
    x = [float(v) for v in x0]
    n = len(x0)
    m_eq = len(eq_constraints)
    m_ineq = len(ineq_constraints)
    
    lam = [0.0] * m_eq
    mu = [0.0] * m_ineq
    rho = 1.0
    
    for iteration in range(max_iter):
        # Define augmented Lagrangian with stable computation
        def L_aug(x_val):
            total = f(x_val)
            # Equality constraints
            for i, (g, target) in enumerate(eq_constraints):
                violation = g(x_val) - target
                # Use log-barrier style for stability: avoid squaring large values
                if abs(violation) > 1e3:
                    total += lam[i] * violation + rho * 1e3 * abs(violation)
                else:
                    total += lam[i] * violation + (rho/2) * violation**2
            # Inequality constraints
            for j, (h, target) in enumerate(ineq_constraints):
                violation = h(x_val) - target
                if violation > 0:  # Active inequality
                    if violation > 1e3:
                        total += mu[j] * violation + rho * 1e3 * violation
                    else:
                        total += mu[j] * violation + (rho/2) * violation**2
            return total
        
        # Gradient descent with adaptive learning rate
        learning_rate = 0.1
        for _ in range(10):  # Inner loop for minimization
            # Compute gradient using finite differences
            grad = []
            f0 = L_aug(x)
            for i in range(n):
                x_pert = x[:]
                x_pert[i] += 1e-6
                f1 = L_aug(x_pert)
                grad.append((f1 - f0) / 1e-6)
            
            # Check for invalid gradients
            if any(math.isnan(g) or math.isinf(g) for g in grad):
                break
            
            # Update x
            x_new = [x[i] - learning_rate * grad[i] for i in range(n)]
            
            # Check if improvement
            if L_aug(x_new) < f0:
                x = x_new
                learning_rate = min(learning_rate * 1.1, 1.0)
            else:
                learning_rate *= 0.5
            
            if learning_rate < 1e-10:
                break
        
        # Update multipliers
        for i, (g, target) in enumerate(eq_constraints):
            violation = g(x) - target
            lam[i] += rho * violation
            # Bound lambda
            lam[i] = max(-1e6, min(1e6, lam[i]))
        
        for j, (h, target) in enumerate(ineq_constraints):
            violation = max(0, h(x) - target)
            mu[j] = max(0, mu[j] + rho * violation)
            # Bound mu
            mu[j] = min(mu[j], 1e6)
        
        # Check convergence
        eq_violations = [abs(g(x) - target) for g, target in eq_constraints]
        ineq_violations = [max(0, h(x) - target) for h, target in ineq_constraints]
        max_viol = max(eq_violations + ineq_violations, default=0)
        
        if max_viol < tol:
            break
        
        # Increase penalty
        rho = min(rho * 2.0, 1e4)
    
    return x, f(x), lam, mu


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


def bfgs(
    f: Callable[[List[float]], float],
    x0: List[float],
    max_iter: int = 100,
    tol: float = 1e-6
) -> Tuple[List[float], float]:
    """BFGS quasi-Newton optimization."""
    import math
    
    x = [float(v) for v in x0]
    n = len(x0)
    
    # Initial inverse Hessian = identity
    H = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    
    def compute_gradient(x, h=1e-6):
        f0 = f(x)
        return [(f([x[k] + (h if k==i else x[k]) for k in range(n)]) - f0) / h 
                for i in range(n)]
    
    for iteration in range(max_iter):
        grad = compute_gradient(x)
        
        # Check convergence
        grad_norm = math.sqrt(sum(g**2 for g in grad))
        if grad_norm < tol:
            break
        
        # Search direction: p = -H @ grad
        p = [-sum(H[i][j] * grad[j] for j in range(n)) for i in range(n)]
        
        # Simple backtracking line search
        alpha = 1.0
        fx = f(x)
        
        for _ in range(50):
            x_new = [x[i] + alpha * p[i] for i in range(n)]
            fx_new = f(x_new)
            if fx_new < fx:
                break
            alpha *= 0.5
        else:
            # Line search failed, try gradient descent
            x_new = [x[i] - 0.1 * grad[i] for i in range(n)]
            if f(x_new) >= fx:
                break
        
        grad_new = compute_gradient(x_new)
        
        # s = x_new - x, y = grad_new - grad
        s = [x_new[i] - x[i] for i in range(n)]
        y = [grad_new[i] - grad[i] for i in range(n)]
        
        # BFGS update for inverse Hessian
        yTs = sum(y[i] * s[i] for i in range(n))
        if abs(yTs) < 1e-12:
            x = x_new
            continue
        
        # BFGS formula: H_new = H + (1 + yT H y / yTs) * s s^T / yTs - (s yT H + H y s^T) / yTs
        Hy = [sum(H[i][j] * y[j] for j in range(n)) for i in range(n)]
        yHy = sum(y[i] * Hy[i] for i in range(n))
        
        for i in range(n):
            for j in range(n):
                H[i][j] += (1.0 + yHy / yTs) * s[i] * s[j] / yTs \
                           - (s[i] * Hy[j] + Hy[i] * s[j]) / yTs
        
        x = x_new
    
    return x, f(x)


def lbfgs(
    f: Callable[[List[float]], float],
    x0: List[float],
    max_iter: int = 100,
    tol: float = 1e-6,
    m: int = 10,
    learning_rate: float = 0.1
) -> Tuple[List[float], float]:
    """Limited-memory BFGS (L-BFGS) optimization.
    
    Uses limited memory to store only the last m (s, y) pairs.
    
    Args:
        f: Objective function to minimize
        x0: Initial point
        max_iter: Maximum iterations
        tol: Gradient tolerance
        m: Memory size (number of past updates to store)
        learning_rate: Step size for line search
        
    Returns:
        (x_opt, f_opt)
    """
    import math
    
    x = x0[:]
    n = len(x0)
    
    # Storage for (s, y) pairs
    s_history = []
    y_history = []
    rho_history = []
    
    def compute_gradient(f, x, h=1e-6):
        """Compute gradient using finite differences."""
        grad = []
        f0 = f(x)
        for i in range(n):
            x_h = x[:]
            x_h[i] += h
            grad.append((f(x_h) - f0) / h)
        return grad
    
    for iteration in range(max_iter):
        grad = compute_gradient(f, x)
        
        # Check convergence
        grad_norm = math.sqrt(sum(g**2 for g in grad))
        if grad_norm < tol:
            break
        
        # Two-loop recursion to compute search direction
        q = grad[:]
        alphas = []
        
        # First loop
        for i in range(len(s_history) - 1, -1, -1):
            alpha = rho_history[i] * sum(s_history[i][j] * q[j] for j in range(n))
            alphas.append(alpha)
            q = [q[j] - alpha * y_history[i][j] for j in range(n)]
        
        # Apply initial Hessian approximation (scaling)
        if s_history:
            last_s = s_history[-1]
            last_y = y_history[-1]
            gamma = sum(last_s[i] * last_y[i] for i in range(n)) / \
                    sum(y * y for y in last_y)
            r = [gamma * q[j] for j in range(n)]
        else:
            r = q[:]
        
        # Second loop
        for i in range(len(s_history)):
            beta = rho_history[i] * sum(y_history[i][j] * r[j] for j in range(n))
            r = [r[j] + s_history[i][j] * (alphas[len(s_history) - 1 - i] - beta) 
                 for j in range(n)]
        
        # Search direction
        p = [-r[j] for j in range(n)]
        
        # Line search
        alpha = learning_rate
        fx = f(x)
        for _ in range(10):
            x_new = [x[i] + alpha * p[i] for i in range(n)]
            fx_new = f(x_new)
            if fx_new < fx:
                break
            alpha *= 0.5
        else:
            x_new = [x[i] - learning_rate * grad[i] for i in range(n)]
        
        # Compute new gradient
        grad_new = compute_gradient(f, x_new)
        
        # Compute s and y
        s = [x_new[i] - x[i] for i in range(n)]
        y = [grad_new[i] - grad[i] for i in range(n)]
        
        # Compute rho
        yTs = sum(y[i] * s[i] for i in range(n))
        if abs(yTs) < 1e-10:
            x = x_new
            continue
        
        rho = 1.0 / yTs
        
        # Update history
        s_history.append(s)
        y_history.append(y)
        rho_history.append(rho)
        
        # Keep only last m pairs
        if len(s_history) > m:
            s_history.pop(0)
            y_history.pop(0)
            rho_history.pop(0)
        
        x = x_new
    
    return x, f(x)


def newton_raphson(
    f: Callable[[List[float]], float],
    x0: List[float],
    max_iter: int = 100,
    tol: float = 1e-6
) -> Tuple[List[float], float]:
    """Newton-Raphson method for optimization."""
    import math
    
    x = [float(v) for v in x0]
    n = len(x0)
    
    def compute_gradient(x, h=1e-6):
        f0 = f(x)
        return [(f([x[k] + (h if k==i else x[k]) for k in range(n)]) - f0) / h 
                for i in range(n)]
    
    def compute_hessian(x, h=1e-6):
        hessian = [[0.0] * n for _ in range(n)]
        
        # Diagonal elements
        for i in range(n):
            x_plus = x[:]; x_plus[i] += h
            x_minus = x[:]; x_minus[i] -= h
            f_plus = f(x_plus)
            f_minus = f(x_minus)
            hessian[i][i] = (f_plus - 2*f(x) + f_minus) / (h**2)
        
        # Off-diagonal elements
        for i in range(n):
            for j in range(i+1, n):
                x_pp = x[:]; x_pp[i] += h; x_pp[j] += h
                x_pm = x[:]; x_pm[i] += h; x_pm[j] -= h
                x_mp = x[:]; x_mp[i] -= h; x_mp[j] += h
                x_mm = x[:]; x_mm[i] -= h; x_mm[j] -= h
                hessian[i][j] = (f(x_pp) - f(x_pm) - f(x_mp) + f(x_mm)) / (4 * h**2)
                hessian[j][i] = hessian[i][j]
        
        return hessian
    
    for iteration in range(max_iter):
        grad = compute_gradient(x)
        
        # Check convergence
        grad_norm = math.sqrt(sum(g**2 for g in grad))
        if grad_norm < tol:
            break
        
        # Compute Hessian
        H = compute_hessian(x)
        
        # Invert Hessian (simple 2x2 or 1x1)
        if n == 1:
            H_inv = [[1.0 / H[0][0]]] if abs(H[0][0]) > 1e-12 else [[1.0]]
        elif n == 2:
            det = H[0][0] * H[1][1] - H[0][1] * H[1][0]
            if abs(det) < 1e-12:
                H_inv = [[1.0, 0.0], [0.0, 1.0]]
            else:
                H_inv = [[H[1][1]/det, -H[0][1]/det], [-H[1][0]/det, H[0][0]/det]]
        else:
            H_inv = [[1.0 if i==j else 0.0 for j in range(n)] for i in range(n)]
        
        # Newton update: x_new = x - H^(-1) * grad
        delta = [-sum(H_inv[i][j] * grad[j] for j in range(n)) for i in range(n)]
        
        # Line search
        alpha = 1.0
        fx = f(x)
        for _ in range(10):
            x_new = [x[i] + alpha * delta[i] for i in range(n)]
            if f(x_new) < fx:
                break
            alpha *= 0.5
        else:
            break
        
        x = x_new
    
    return x, f(x)


def levenberg_marquardt(
    residuals: Callable[[List[float]], List[float]],
    x0: List[float],
    max_iter: int = 100,
    tol: float = 1e-6,
    lambda_init: float = 0.01
) -> Tuple[List[float], List[float]]:
    """Levenberg-Marquardt algorithm for nonlinear least squares."""
    import math
    
    x = [float(v) for v in x0]
    n = len(x0)
    lam = lambda_init
    
    def compute_jacobian(x, h=1e-6):
        r0 = residuals(x)
        m = len(r0)
        J = [[0.0] * n for _ in range(m)]
        
        for j in range(n):
            x_pert = x[:]
            x_pert[j] += h
            r_pert = residuals(x_pert)
            for i in range(m):
                J[i][j] = (r_pert[i] - r0[i]) / h
        
        return J, r0
    
    for iteration in range(max_iter):
        J, r = compute_jacobian(x)
        m = len(r)
        
        # Compute J^T J and J^T r
        JtJ = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                JtJ[i][j] = sum(J[k][i] * J[k][j] for k in range(m))
        
        Jtr = [sum(J[k][i] * r[k] for k in range(m)) for i in range(n)]
        
        # Check convergence
        grad_norm = math.sqrt(sum(g**2 for g in Jtr))
        if grad_norm < tol:
            break
        
        # Add damping
        for i in range(n):
            JtJ[i][i] += lam
        
        # Solve (J^T J + lambda*I) * delta = -J^T r
        if n == 1:
            if abs(JtJ[0][0]) < 1e-12:
                delta = [-Jtr[0]]
            else:
                delta = [-Jtr[0] / JtJ[0][0]]
        elif n == 2:
            det = JtJ[0][0] * JtJ[1][1] - JtJ[0][1] * JtJ[1][0]
            if abs(det) < 1e-12:
                delta = [-Jtr[i] for i in range(2)]
            else:
                delta = [(-JtJ[1][1]*Jtr[0] + JtJ[0][1]*Jtr[1])/det,
                          (JtJ[0][0]*Jtr[1] - JtJ[1][0]*Jtr[0])/det]
        else:
            delta = [-Jtr[i] / (JtJ[i][i]) for i in range(n)]
        
        # Update parameters
        x_new = [x[i] + delta[i] for i in range(n)]
        
        # Check if error decreased
        r_new = residuals(x_new)
        error_new = sum(r**2 for r in r_new)
        error_old = sum(r_i**2 for r_i in r)
        
        if error_new < error_old:
            x = x_new
            lam *= 0.7  # Decrease damping
        else:
            lam *= 2.0  # Increase damping
            if lam > 1e6:
                break
    
    return x, residuals(x)
