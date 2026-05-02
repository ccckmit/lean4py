# 微分方程测试文档 (test_differential_equations.py)

## 概述

本测试文件验证 `lean4py.differential_equations` 模块中常微分方程（ODE）的核心功能，包括初值问题构造、数值解法、存在唯一性定理以及稳定性分析。

---

## 1. 测试验证内容

### ODEProblem 类测试 (`TestODEProblem`)

**数学原理：** ODEProblem 表示初值问题（Initial Value Problem）：

$$
\frac{dy}{dt} = f(t, y), \quad y(t_0) = y_0
$$

- **test_creation**：验证 ODEProblem 正确存储方程右侧函数 $f$、初始时间 $t_0$ 和初始值 $y_0$
- **test_euler_step_scalar**：验证 Euler 法单步计算，公式为：

$$
y_{n+1} = y_n + \Delta t \cdot f(t_n, y_n)
$$

对于 $f(t, y) = y$（指数增长方程），步长 $\Delta t = 0.1$ 时：

$$
y_{n+1} = 1.0 + 0.1 \times 1.0 = 1.1
$$

---

## 2. ODE 数值解法测试

### Euler 法 (Euler Method)

**数学原理：** Euler 法是最简单的一阶显式数值方法，局部截断误差为 $O(\Delta t^2)$，整体误差为 $O(\Delta t)$。

对于纯量问题 $dy/dt = f(t, y)$：

$$
y_{n+1} = y_n + \Delta t \cdot f(t_n, y_n)
$$

对于向量问题（系统）：

$$
y_{i,n+1} = y_{i,n} + \Delta t \cdot f_i(t_n, y_n)
$$

### Runge-Kutta 4 方法 (RK4)

**数学原理：** RK4 是四阶显式方法，局部截断误差为 $O(\Delta t^5)$，整体误差为 $O(\Delta t^4)$。每步计算四个斜率估计：

$$
k_1 = f(t_n, y_n)
$$
$$
k_2 = f(t_n + \frac{\Delta t}{2}, y_n + \frac{\Delta t}{2} k_1)
$$
$$
k_3 = f(t_n + \frac{\Delta t}{2}, y_n + \frac{\Delta t}{2} k_2)
$$
$$
k_4 = f(t_n + \Delta t, y_n + \Delta t \cdot k_3)
$$

最终更新：

$$
y_{n+1} = y_n + \frac{\Delta t}{6}(k_1 + 2k_2 + 2k_3 + k_4)
$$

---

## 3. Lipschitz 条件测试 (`TestLipschitzCondition`)

### 数学原理

**Lipschitz 条件**是 Picard-Lindelöf 定理的关键前提。

函数 $f: \mathbb{R} \times \mathbb{R}^n \to \mathbb{R}^n$ 在区域 $D$ 上关于 $y$ 满足 Lipschitz 条件，若存在常数 $L \geq 0$ 使得：

$$
\| f(t, y_1) - f(t, y_2) \| \leq L \| y_1 - y_2 \|
$$

对所有 $(t, y_1), (t, y_2) \in D$ 成立。

- **test_is_lipschitz**：验证 $f(t, y) = y$ 在给定区域满足 Lipschitz 条件（Lipschitz 常数 $L = 1$）
- **test_lipschitz_constant**：计算 Lipschitz 常数 $L$，验证 $L \geq 0$

---

## 4. Picard-Lindelöf 定理测试 (`TestPicardLindelof`)

### 数学原理

**Picard-Lindelöf 定理**（存在唯一性定理）：

若 $f(t, y)$ 在区域 $R = [t_0-a, t_0+a] \times [y_0-b, y_0+b]$ 上满足：
1. **连续性**：$f$ 关于 $t$ 连续
2. **Lipschitz 条件**：关于 $y$ 满足 Lipschitz 条件

则初值问题在区间 $|t - t_0| \leq \min(a, b/M)$ 上有唯一解，其中 $M = \max_{(t,y) \in R} \|f(t, y)\|$。

**Picard 迭代**是构造性证明方法：

$$
y_0(t) = y_0
$$
$$
y_{n+1}(t) = y_0 + \int_{t_0}^{t} f(s, y_n(s)) \, ds
$$

- **test_has_unique_solution**：验证初值问题满足存在唯一性条件
- **test_picard_iteration**：执行 $n$ 次 Picard 迭代逼近真解

---

## 5. 流性质测试 (`TestFlowProperty`)

### 数学原理

**流（Flow）** 是 ODE 解的算子 $\phi: \mathbb{R} \times \mathbb{R}^n \to \mathbb{R}^n$，满足：

$$
\phi(t_0, y_0) = y_0, \quad \frac{d}{dt}\phi(t, y_0) = f(t, \phi(t, y_0))
$$

**半群性质（Semigroup Property）**：

$$
\phi(t_2, \phi(t_1, y_0)) = \phi(t_1 + t_2, y_0)
$$

这体现了时间平移不变性。

- **test_is_flow**：验证解算子构成合法的流
- **test_semigroup_property**：验证半群性质 $\phi(t_2, \phi(t_1, y_0)) = \phi(t_1 + t_2, y_0)$

---

## 6. 相图分析测试 (`TestPhasePortrait`)

### 数学原理

**不动点（Fixed Point）**：满足 $f(y^*) = 0$ 的点 $y^*$，此时系统处于平衡状态。

**线性稳定性判据**：对不动点 $y^*$，计算 Jacobi 矩阵 $J = \frac{\partial f}{\partial y}(y^*)$：
- 若所有特征值 $\lambda_i$ 满足 $\text{Re}(\lambda_i) < 0$，则**渐近稳定**
- 若存在 $\text{Re}(\lambda_i) > 0$，则**不稳定**
- 若特征值符号混合，则为**鞍点**

- **test_fixed_points**：在给定定义域内搜索满足 $f(y) = 0$ 的点
- **test_is_stable**：根据 Jacobi 矩阵特征值判断稳定性

---

## 7. 稳定性分析测试 (`TestStabilityAnalysis`)

### 数学原理

**线性稳定性分类**：
根据 Jacobi 矩阵的特征值 $\lambda_i$ 分类：
- **stable（稳定）**：$\forall i, \text{Re}(\lambda_i) < 0$
- **unstable（不稳定）**：$\exists i, \text{Re}(\lambda_i) > 0$
- **saddle（鞍点）**：既有正实部特征值也有负实部特征值

**Lyapunov 稳定性**：

若存在正定函数 $V: \mathbb{R}^n \to \mathbb{R}$（Lyapunov 函数）使得 $\dot{V}(y) = \nabla V \cdot f(y) \leq 0$，则平衡点稳定。

- **test_linear_stability**：基于 Jacobi 矩阵特征值分类
- **test_lyapunov_stability**：使用 Lyapunov 函数 $V(y) = y^2$ 验证 $y' = -y$ 的稳定性

---

## 8. 测试覆盖的方程示例

| 测试方程 | 形式 | 解析解 |
|---------|------|--------|
| 指数增长 | $y' = y$ | $y(t) = y_0 e^t$ |
| 指数衰减 | $y' = -y$ | $y(t) = y_0 e^{-t}$ |

---

## 9. 模块对应关系

| 测试类 | 源模块类 | 功能 |
|--------|---------|------|
| TestODEProblem | ODEProblem | 初值问题构造与 Euler 步进 |
| TestLipschitzCondition | LipschitzCondition | Lipschitz 条件验证 |
| TestPicardLindelof | PicardLindelof | 存在唯一性定理 |
| TestFlowProperty | FlowProperty | 流与半群性质 |
| TestPhasePortrait | PhasePortrait | 相图与不动点 |
| TestStabilityAnalysis | StabilityAnalysis | 线性与 Lyapunov 稳定性 |