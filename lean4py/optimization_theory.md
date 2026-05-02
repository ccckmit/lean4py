# 优化理论 (Optimization Theory)

> 本文档基于 `lean4py/optimization_theory.py` 模块，阐述约束优化、非线性规划与对偶理论的核心数学原理。

---

## 1. 约束优化概述

约束优化问题（Constrained Optimization）指在给定约束条件下寻找目标函数最优解的数学规划问题。其标准形式为：

```
min  f(x)                # 目标函数
s.t. g_i(x) ≤ 0  (i=1,...,m)    # 不等式约束
     h_j(x) = 0  (j=1,...,p)    # 等式约束
     x ∈ ℝⁿ
```

### 1.1 约束优化的分类

| 类型 | 特点 |
|------|------|
| **线性规划 (LP)** | 目标函数和约束均为线性 |
| **二次规划 (QP)** | 目标函数为二次型，约束为线性 |
| **非线性规划 (NLP)** | 目标或约束含有非线性函数 |
| **整数规划 (IP)** | 决策变量受整数约束 |

---

## 2. KKT 条件（Karush-Kuhn-Tucker Conditions）

KKT 条件是非线性规划中最优性的核心必要条件，相当于约束优化问题中的拉格朗日乘数法推广。

### 2.1 标准形式

考虑非线性规划问题：

```
min f(x)
s.t. g_i(x) ≤ 0,  i = 1,...,m
     h_j(x) = 0,  j = 1,...,p
```

### 2.2 KKT 条件详解

设 $x^*$ 为局部最优解，在一定正则性条件下，存在拉格朗日乘数 $\lambda_i \geq 0$ 和 $\mu_j$ 使得：

#### (1) 平稳性条件 (Stationarity)

$$\nabla f(x^*) + \sum_{i=1}^{m} \lambda_i \nabla g_i(x^*) + \sum_{j=1}^{p} \mu_j \nabla h_j(x^*) = 0$$

#### (2) 原问题可行性 (Primal Feasibility)

$$g_i(x^*) \leq 0, \quad i = 1,...,m$$
$$h_j(x^*) = 0, \quad j = 1,...,p$$

#### (3) 对偶可行性 (Dual Feasibility)

$$\lambda_i \geq 0, \quad i = 1,...,m$$

#### (4) 互补松弛条件 (Complementary Slackness)

$$\lambda_i \cdot g_i(x^*) = 0, \quad i = 1,...,m$$

### 2.5 KKT 条件的几何意义

- 当约束 $g_i(x^*) < 0$（严格不等式）时，$\lambda_i = 0$（约束未激活）
- 当约束 $g_i(x^*) = 0$（边界上）时，$\lambda_i > 0$（约束激活）

---

## 3. 对偶理论 (Duality Theory) 与拉格朗日函数

### 3.1 拉格朗日函数

对于原问题：

```
min f(x)
s.t. g_i(x) ≤ 0, h_j(x) = 0
```

拉格朗日函数定义为：

$$L(x, \lambda, \mu) = f(x) + \sum_{i=1}^{m} \lambda_i g_i(x) + \sum_{j=1}^{p} \mu_j h_j(x)$$

其中：
- $\lambda = (\lambda_1, ..., \lambda_m)$：不等式约束的拉格朗日乘数（$\lambda_i \geq 0$）
- $\mu = (\mu_1, ..., \mu_p)$：等式约束的拉格朗日乘数（无符号限制）

### 3.2 拉格朗日对偶函数

$$g(\lambda, \mu) = \inf_{x \in \mathbb{R}^n} L(x, \lambda, \mu) = \inf_{x \in \mathbb{R}^n} \left[ f(x) + \sum_{i} \lambda_i g_i(x) + \sum_{j} \mu_j h_j(x) \right]$$

**性质**：无论原问题是否凸，对偶函数 $g(\lambda, \mu)$ 总是凹函数。

### 3.3 对偶问题

```
max g(λ, μ)
s.t. λ ≥ 0
```

- **弱对偶性**：$p^* \geq d^*$，其中 $p^*$ 为原问题最优值，$d^*$ 为对偶问题最优值
- **强对偶性**：若原问题满足某些约束规范（如 Slater 条件），则 $p^* = d^*$

---

## 4. 凸分析 (Convex Analysis)

### 4.1 凸集 (Convex Set)

**定义**：集合 $C \subseteq \mathbb{R}^n$ 为凸集，当且仅当：

$$\forall x, y \in C, \forall t \in [0,1]: \quad t x + (1-t) y \in C$$

**几何意义**：凸集中任意两点之间的线段完全落在集合内。

**常见凸集**：
- $\mathbb{R}^n$（整个空间）
- 超平面：$\{x \mid a^T x = b\}$
- 半空间：$\{x \mid a^T x \leq b\}$
- 多面体、球、椭球

### 4.2 凸函数 (Convex Function)

**定义**：函数 $f: \mathbb{R}^n \rightarrow \mathbb{R}$ 为凸函数，当且仅当：

$$\forall x, y \in \text{dom}(f), \forall t \in [0,1]: \quad f(tx + (1-t)y) \leq t f(x) + (1-t) f(y)$$

**几何意义**：函数图像上任意两点之间的弦位于函数图像上方。

**严格凸函数**：不等式在 $t \in (0,1)$ 时严格成立。

### 4.3 凸函数判定

一阶条件：若 $f$ 可微，$f$ 凸当且仅当

$$f(y) \geq f(x) + \nabla f(x)^T (y - x)$$

二阶条件：若 $f$ 二阶可微，$f$ 凸当且仅当其 Hessian 矩阵半正定：

$$\nabla^2 f(x) \succeq 0$$

### 4.4 共轭函数 (Fenchel Conjugate)

函数 $f$ 的 Fenchel 共轭定义为：

$$f^*(y) = \sup_{x \in \text{dom}(f)} \{ y^T x - f(x) \}$$

**性质**：
- $f^*$ 总是凸函数（无论 $f$ 是否凸）
- 若 $f$ 凸且闭，则 $f^{**} = f$
- Fenchel 共轭是对称且可逆的（对于闭凸函数）

**示例**：对于二次函数 $f(x) = \frac{1}{2} x^T Q x$，其共轭为

$$f^*(y) = \frac{1}{2} y^T Q^{-1} y$$

---

## 5. 对偶问题详解

### 5.1 原问题与对偶问题的关系

| 概念 | 原问题 (Primal) | 对偶问题 (Dual) |
|------|----------------|----------------|
| 问题 | $\min f(x)$ | $\max g(\lambda, \mu)$ |
| 变量 | $x \in \mathbb{R}^n$ | $\lambda \geq 0, \mu \in \mathbb{R}^p$ |
| 约束 | $g_i(x) \leq 0, h_j(x) = 0$ | 无显示约束 |

### 5.2 弱对偶性定理

对于任意原始可行解 $x$ 和对偶可行解 $(\lambda, \mu)$：

$$f(x) \geq g(\lambda, \mu)$$

**推论**：$p^* \geq d^*$

### 5.3 强对偶性定理

若原问题为凸问题（即 $f, g_i$ 凸，$h_j$ 线性），且满足 Slater 条件（存在严格可行点），则：

$$p^* = d^*$$

---

## 6. Slater 条件

Slater 条件是保证强对偶性的约束规范之一。

**定义**：存在一点 $x$ 使得所有不等式约束严格成立：

$$g_i(x) < 0, \quad i = 1,...,m$$
$$h_j(x) = 0, \quad j = 1,...,p$$

对于凸问题，Slater 条件是强对偶性的充分条件。

---

## 7. 敏感性分析 (Sensitivity Analysis)

敏感性分析研究最优解如何随参数变化而变化。

### 7.1 对偶变量与影子价格

在原问题：

```
min f(x)
s.t. g_i(x) ≤ 0
```

中，对偶变量 $\lambda_i$（KKT 乘子）具有重要经济含义：

$$\lambda_i^* = \frac{\partial p^*}{\partial b_i}$$

即第 $i$ 个约束右边常数增加一个单位时，最优值的变化率。

### 7.2 互补松弛的敏感性含义

$$\lambda_i \cdot g_i(x^*) = 0$$

- 当 $g_i(x^*) < 0$（约束未紧）时，$\lambda_i = 0$，该约束对最优解无影响
- 当 $g_i(x^*) = 0$（约束活跃）时，$\lambda_i$ 反映目标函数对该约束的敏感程度

### 7.3 扰动分析

考虑扰动后的原问题：

```
min f(x)
s.t. g_i(x) ≤ u_i
     h_j(x) = v_j
```

设 $p(u, v)$ 为扰动问题的最优值，则：

$$\frac{\partial p(0,0)}{\partial u_i} = -\lambda_i^*, \quad \frac{\partial p(0,0)}{\partial v_j} = -\mu_j^*$$

这给出了参数微小变化对最优值的精确估计。

---

## 8. 模块代码对照

| 类名 | 作用 | 核心方法 |
|------|------|---------|
| `ConvexSet` | 凸集判定与操作 | `is_convex()`, `convex_hull()` |
| `ConvexFunction` | 凸函数判定 | `is_convex()`, `is_strictly_convex()` |
| `LagrangeMultiplier` | 拉格朗日乘数法 | `lagrangian()`, `solve()` |
| `KKTConditions` | KKT 条件验证 | `check()`, `is_optimal()` |
| `Duality` | 对偶理论 | `lagrange_dual()`, `is_strong_duality()`, `weak_duality()` |
| `SlaterCondition` | Slater 条件检验 | `holds()` |

---

## 9. 参考数学文献

- Rockafellar, R. T. - *Convex Analysis*
- Boyd, S. & Vandenberghe, L. - *Convex Optimization*
- Nocedal, J. & Wright, S. - *Numerical Optimization*
- Bertsekas, D. - *Constrained Optimization and Lagrange Multiplier Methods*

---

*本文档版本：1.34.0 | 最后更新：2026-05-02*