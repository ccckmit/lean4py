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
