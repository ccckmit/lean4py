"""Partial differential equations module."""

from typing import Callable, List, Tuple
import math


def solve_heat_equation(
    L: float,
    T: float,
    u0: Callable[[float], float],
    alpha: float = 1.0,
    nx: int = 50,
    nt: int = 100
) -> Tuple[List[float], List[float]]:
    """Solve heat equation u_t = alpha * u_xx with u(0,t)=u(L,t)=0.
    
    Uses explicit finite difference method.
    
    Args:
        L: Length of spatial domain [0, L]
        T: Total time
        u0: Initial condition function u(x,0)
        alpha: Thermal diffusivity
        nx: Number of spatial grid points
        nt: Number of time steps
        
    Returns:
        (x_grid, solution) where solution is last time step
    """
    dx = L / (nx - 1)
    dt = T / nt
    r = alpha * dt / (dx ** 2)
    
    # Stability check
    if r > 0.5:
        print(f"Warning: r={r:.2f} > 0.5, solution may be unstable")
    
    x = [i * dx for i in range(nx)]
    u = [u0(xi) for xi in x]
    
    for _ in range(nt):
        u_new = u[:]
        for i in range(1, nx-1):
            u_new[i] = u[i] + r * (u[i+1] - 2*u[i] + u[i-1])
        u = u_new
    
    return x, u


def solve_wave_equation(
    L: float,
    T: float,
    u0: Callable[[float], float],
    v0: Callable[[float], float],
    c: float = 1.0,
    nx: int = 50,
    nt: int = 100
) -> Tuple[List[float], List[float]]:
    """Solve wave equation u_tt = c^2 * u_xx with u(0,t)=u(L,t)=0.
    
    Uses explicit finite difference method.
    """
    dx = L / (nx - 1)
    dt = T / nt
    r = (c * dt / dx) ** 2
    
    if r > 1.0:
        print(f"Warning: r={r:.2f} > 1.0, solution may be unstable")
    
    x = [i * dx for i in range(nx)]
    u_prev = [u0(xi) for xi in x]
    u_curr = [u_prev[i] + dt * v0(x[i]) for i in range(nx)]
    
    for _ in range(nt-1):
        u_next = u_curr[:]
        for i in range(1, nx-1):
            u_next[i] = 2*u_curr[i] - u_prev[i] + r * (u_curr[i+1] - 2*u_curr[i] + u_curr[i-1])
        u_prev = u_curr
        u_curr = u_next
    
    return x, u_curr

def solve_laplace_equation(
    Lx: float, Ly: float,
    nx: int = 50, ny: int = 50,
    max_iter: int = 1000, tol: float = 1e-6
) -> List[List[float]]:
    """Solve Laplace equation ∇²u = 0 with u=0 on boundary."""
    dx = Lx / (nx - 1)
    dy = Ly / (ny - 1)
    
    u = [[0.0 for _ in range(ny)] for _ in range(nx)]
    
    for _ in range(max_iter):
        u_new = [row[:] for row in u]
        max_diff = 0.0
        
        for i in range(1, nx-1):
            for j in range(1, ny-1):
                u_new[i][j] = 0.25 * (u[i+1][j] + u[i-1][j] + 
                                u[i][j+1] + u[i][j-1])
                max_diff = max(max_diff, abs(u_new[i][j] - u[i][j]))
        
        u = u_new
        if max_diff < tol:
            break
    
    return u


def solve_poisson_equation(
    Lx: float, Ly: float,
    source: Callable[[float, float], float],
    nx: int = 50, ny: int = 50,
    max_iter: int = 1000, tol: float = 1e-6
) -> List[List[float]]:
    """Solve Poisson equation ∇²u = f with u=0 on boundary."""
    dx = Lx / (nx - 1)
    dy = Ly / (ny - 1)
    dx2, dy2 = dx**2, dy**2
    
    u = [[0.0 for _ in range(ny)] for _ in range(nx)]
    
    for _ in range(max_iter):
        u_new = [row[:] for row in u]
        max_diff = 0.0
        
        for i in range(1, nx-1):
            for j in range(1, ny-1):
                x_val = i * dx
                y_val = j * dy
                f_val = source(x_val, y_val)
                u_new[i][j] = (dy2 * (u[i+1][j] + u[i-1][j]) +
                                dx2 * (u[i][j+1] + u[i][j-1]) -
                                dx2 * dy2 * f_val) / (2 * (dx2 + dy2))
                max_diff = max(max_diff, abs(u_new[i][j] - u[i][j]))
        
        u = u_new
        if max_diff < tol:
            break
    
    return u
