"""
lean4py v1.3 Demo - 约束优化、ODE 求解、非参数检验
"""

import sys
# sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')
sys.path.insert(0, './')

print("=== lean4py v1.3 Demo ===\n")

# 1. 拉格朗日乘子法
print("1. 约束优化 (拉格朗日乘子)")
from lean4py.optimization import lagrange_multiplier

# 最小化 x^2 + y^2，约束 x + y = 1
f = lambda x: x[0]**2 + x[1]**2
g = lambda x: x[0] + x[1]
constraints = [(g, 1.0)]
x0 = [0.5, 0.5]
x_opt, f_opt, lam = lagrange_multiplier(f, constraints, x0)
print(f"  最小化 x^2 + y^2，约束 x + y = 1")
print(f"  最优解: x = {x_opt[0]:.3f}, y = {x_opt[1]:.3f}")
print(f"  最优值: {f_opt:.3f}\n")

# 2. ODE 求解器
print("2. 常微分方程求解")
from lean4py.real_analysis import euler_method, runge_kutta_4
import math

# dy/dt = y, y(0) = 1，解析解: y = e^t
f = lambda t, y: [y[0]]
t_vals, y_vals = runge_kutta_4(f, [1.0], (0.0, 1.0), dt=0.01)
y_final = y_vals[-1][0]
print(f"  dy/dt = y, y(0)=1, 求解到 t=1")
print(f"  Runge-Kutta 4: y(1) = {y_final:.4f}")
print(f"  解析解 e^1 = {math.e:.4f}")
print(f"  误差: {abs(y_final - math.e):.4f}\n")

# 3. 非参数检验
print("3. 非参数检验")
from lean4py.statistics import mann_whitney_u, kruskal_wallis

# Mann-Whitney U 检验
group1 = [1, 2, 3, 4, 5]
group2 = [6, 7, 8, 9, 10]
U, p = mann_whitney_u(group1, group2)
print(f"  Mann-Whitney U 检验: U = {U:.1f}, p = {p:.4f}")
print(f"  两组分离，p 应很小\n")

# Kruskal-Wallis 检验
groups = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
H, p = kruskal_wallis(groups)
print(f"  Kruskal-Wallis 检验: H = {H:.3f}, p = {p:.4f}")
print(f"  三组分离，p 应很小\n")

print("=== Demo 完成 ===")
