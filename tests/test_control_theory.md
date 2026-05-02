# 控制理论测试文档 (test_control_theory.py)

本文档说明 `test_control_theory.py` 测试文件中各测试用例所验证的控制理论数学原理。

---

## 1. 测试验证内容概述

本测试文件针对 `lean4py.control_theory` 模块中的以下核心类进行验证：

| 测试类 | 功能 |
|--------|------|
| `TestLyapunovStability` | Lyapunov 稳定性分析 |
| `TestStateSpaceRepresentation` | 状态空间模型表示 |
| `TestControllability` | 系统能控性判别 |
| `TestObservability` | 系统能观性判别 |
| `TestOptimalControl` | 最优控制（极小值原理） |
| `TestKalmanFilter` | 卡尔曼滤波器 |

---

## 2. 状态空间测试 (TestStateSpaceRepresentation)

### 数学原理

状态空间表示是现代控制理论的基础，用一组一阶微分方程描述系统：

```
dx/dt = Ax + Bu
y = Cx + Du
```

其中：
- **x**: 状态向量 (n 维)
- **u**: 输入向量 (p 维)
- **y**: 输出向量 (q 维)
- **A**: 系统矩阵 (n×n)
- **B**: 输入矩阵 (n×p)
- **C**: 输出矩阵 (q×n)
- **D**: 前馈矩阵 (q×p)

### 测试用例

```python
A = [[0.0, 1.0], [-1.0, -1.0]]
B = [[0.0], [1.0]]
sys = StateSpaceRepresentation(A, B)
assert sys.system_dim() == 2  # 状态维度 n=2
assert sys.input_dim() == 1   # 输入维度 p=1
```

此系统表示一个二阶线性系统，矩阵 A 的特征值决定系统固有特性。

---

## 3. 能控性测试 (TestControllability)

### 数学原理

**能控性** (Controllability) 指的是：对于任意初始状态 x(0) 和任意目标状态 x₁，存在某个有限时间 T 和适当控制输入 u(t)，使得系统从 x(0) 转移到 x(T) = x₁。

**Gramian 能控性矩阵**（Kalmann 能控性判据）：

```
W_c = [B, AB, A²B, ..., A^(n-1)B]
```

系统完全能控当且仅当 W_c 的秩为 n（满秩）。

测试中使用的系统：
```
A = [[0, 1], [-1, -1]], B = [[0], [1]]
```

能控性矩阵：
```
W_c = [B, AB] = [[0, 1], [1, -1]]
```
行列式 = -1 ≠ 0，故系统能控。

---

## 4. 能观性测试 (TestObservability)

### 数学原理

**能观性** (Observability) 指的是：通过在有限时间内的输出测量 y(t)，能够唯一确定系统的初始状态 x(0)。

**Gramian 能观性矩阵**：

```
W_o = [C; CA; CA²; ...; CA^(n-1)]ᵀ
```

系统完全能观当且仅当 W_o 的秩为 n（满秩）。

测试用例：
```python
A = [[0, 1], [-1, -1]]
C = [[1, 0]]  # 只测量第一个状态
```

能观性矩阵：
```
W_o = [C; CA] = [[1, 0], [0, 1]]
```
行列式 = 1 ≠ 0，故系统能观。

---

## 5. 稳定性测试 (TestLyapunovStability)

### 数学原理

**Lyapunov 稳定性理论**提供了一种无需求解微分方程即可判断系统稳定性的方法。

**定义**：对于非线性系统 ẋ = f(x)，若存在连续可微函数 V(x) 满足：
1. V(0) = 0，V(x) > 0（正定）当 x ≠ 0
2. dV/dt = ∂V/∂x · f(x) < 0（负定）当 x ≠ 0

则平衡点 x = 0 **渐近稳定**。

### 测试用例分析

```python
V = lambda y: y * y        # V(y) = y²，正定
dV_dt = lambda y: -2.0 * y * y  # dV/dt = -2y²，负定
assert LyapunovStability.is_asymptotically_stable(V, dV_dt) is True
```

Lyapunov 函数 V(y) = y² 是正定的，其导数 dV/dt = -2y² 是负定的，故系统渐近稳定。

**lyapunov_function** 测试验证构造 V(y) = ||y||²（欧几里得范数的平方）作为候选 Lyapunov 函数。

---

## 6. 最优控制测试 (TestOptimalControl)

### 数学原理

**Pontryagin 极小值原理** (Pontryagin's Minimum Principle) 是最优控制的核心。

对于系统：
```
ẋ = f(x, u, t)
J = φ(x(T)) + ∫₀ᵀ L(x, u, t) dt
```

**Hamiltonian 函数**定义为：
```
H(x, u, λ, t) = L(x, u, t) + λᵀ f(x, u, t)
```

最优控制满足：
```
∂H/∂u = 0  (或 H 取最小值)
λ̇ = -∂H/∂x (协态方程)
```

### 测试用例

```python
state = (1.0,)
control = (0.5,)
costate = (1.0,)
dynamics = lambda x, u: (u[0],)
H = OptimalControl.hamiltonian(state, control, costate, dynamics)
```

计算：H = λᵀ f(x,u) = 1.0 × u₀ = 0.5

---

## 7. 卡尔曼滤波器测试 (TestKalmanFilter)

### 数学原理

卡尔曼滤波器是线性系统的最优状态估计器，分为**预测**和**更新**两步。

**预测步骤**：
```
x̂⁻ = A x̂
P⁻ = A P Aᵀ + Q
```

**更新步骤**：
```
K = P⁻ Hᵀ (H P⁻ Hᵀ + R)⁻¹
x̂ = x̂⁻ + K (z - H x̂⁻)
P = (I - K H) P⁻
```

其中：
- **Q**: 过程噪声协方差矩阵
- **R**: 测量噪声协方差矩阵
- **P**: 状态估计误差协方差矩阵
- **K**: 卡尔曼增益

### 测试用例分析

```python
# 预测
A = [[1.0, 0.1], [0.0, 1.0]]  # 状态转移矩阵
Q = [[0.01, 0.0], [0.0, 0.01]]  # 过程噪声
new_state, P = KalmanFilter.predict(state, A, Q)
```

```python
# 更新
z = (1.1,)        # 观测值
H = [[1.0, 0.0]]  # 观测矩阵
R = [[0.1]]       # 测量噪声
new_state, new_P = KalmanFilter.update(state, P, z, H, R)
```

---

## 8. 测试覆盖矩阵

| 测试项 | 验证内容 | 数学概念 |
|--------|----------|----------|
| `test_is_stable` | 稳定性判别 | V > 0, dV/dt < 0 |
| `test_lyapunov_function` | Lyapunov 函数构造 | V(y) = \|\|y\|\|² |
| `test_is_asymptotically_stable` | 渐近稳定性 | V > 0, dV/dt < 0 (严格负定) |
| `test_creation` | 状态空间创建 | A, B 矩阵维度 |
| `test_output_dim` | 输出维度 | C 矩阵行数 |
| `test_is_controllable` | 能控性判别 | 秩条件 |
| `test_controllability_matrix` | 能控性矩阵 | W_c = [B,AB,...,Aⁿ⁻¹B] |
| `test_is_observable` | 能观性判别 | 秩条件 |
| `test_observability_matrix` | 能观性矩阵 | W_o = [C;CA;...;CAⁿ⁻¹] |
| `test_hamiltonian` | Hamilton 函数 | H = λᵀ f(x,u) |
| `test_optimal_control` | 最优控制 | 极小值原理 |
| `test_predict` | 预测步骤 | x̂⁻ = Ax̂, P⁻ = APAᵀ+Q |
| `test_update` | 更新步骤 | K, x̂, P 更新公式 |

---

## 9. 参考文献

- Lyapunov, A.M. "The General Problem of the Stability of Motion" (1892)
- Kalman, R.E. "On the General Theory of Control Systems" (1960)
- Pontryagin, L.S. "The Mathematical Theory of Optimal Processes" (1962)
- Kalman, R.E. "A New Approach to Linear Filtering and Prediction Problems" (1960)