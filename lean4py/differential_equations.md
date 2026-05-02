# 微分方程模块 (Differential Equations)

## 概述

本模块实现了常微分方程（ODE）的基本理论与数值方法，模仿 mathlib4 的 `Mathlib.Analysis.ODE` 结构。包含存在性与唯一性定理、解析解法（线性方程、可分离方程）以及数值方法（Euler 法、RK4）。

---

## 1. ODE 基本形式

### 标准形式

**一阶常微分方程**的标准形式为：

$$\frac{dy}{dt} = f(t, y)$$

其中：
- $t$ 为自变量（通常表示时间）
- $y$ 为未知函数
- $f(t, y)$ 为给定的二元函数

### 初值问题 (IVP)

初值问题是在给定初始条件下求解 ODE：

$$\frac{dy}{dt} = f(t, y), \quad y(t_0) = y_0$$

---

## 2. 存在性与唯一性定理 (Picard-Lindelöf)

### 定理陈述

设 $f(t, y)$ 满足：
1. **连续性**：$f(t, y)$ 在矩形区域 $R = \{(t, y) : |t - t_0| \leq a, |y - y_0| \leq b\}$ 上连续
2. **Lipschitz 条件**：$f$ 关于 $y$ 满足 Lipschitz 条件，即存在常数 $L > 0$ 使得

$$|f(t, y_1) - f(t, y_2)| \leq L |y_1 - y_2|$$

则初值问题在区间 $|t - t_0| \leq \min(a, b/M)$ 上存在唯一解，其中 $M = \max_{(t,y) \in R} |f(t, y)|$。

### Lipschitz 条件

函数 $f$ 满足 Lipschitz 条件的几何意义是：$f$ 随 $y$ 变化的速率被某个常数 $L$ 所bound。形式化地：

$$|f(t, y_1) - f(t, y_2)| \leq L \sum_{i} |y_{1i} - y_{2i}|$$

### Picard 迭代

Picard 迭代提供了一种构造性方法来证明解的存在性：

$$y_0(t) = y_0$$
$$y_{n+1}(t) = y_0 + \int_{t_0}^{t} f(s, y_n(s)) \, ds$$

---

## 3. 一阶线性 ODE

### 标准形式

$$\frac{dy}{dt} + p(t) y = q(t)$$

### 解的结构

对应的齐次方程为：

$$\frac{dy}{dt} + p(t) y = 0$$

其通解为：

$$y_h(t) = C e^{-\int p(t) dt}$$

### 非齐次方程的通解

$$y(t) = e^{-\int p(t) dt} \left( \int e^{\int p(t) dt} q(t) \, dt + C \right)$$

---

## 4. 积分因子法

### 方法原理

对于一阶线性 ODE $\frac{dy}{dt} + p(t)y = q(t)$，乘以积分因子 $\mu(t) = e^{\int p(t) dt}$ 后，左边变为全导数：

$$\mu(t) \frac{dy}{dt} + \mu(t) p(t) y = \frac{d}{dt}(\mu(t) y)$$

因此：

$$\frac{d}{dt}(\mu(t) y) = \mu(t) q(t)$$

积分得：

$$y(t) = \frac{1}{\mu(t)} \int \mu(t) q(t) \, dt$$

---

## 5. 可分离方程

### 标准形式

$$\frac{dy}{dt} = g(y) h(t)$$

### 解法

将变量分离：

$$\frac{dy}{g(y)} = h(t) \, dt$$

两边积分：

$$\int \frac{dy}{g(y)} = \int h(t) \, dt + C$$

---

## 6. 二阶线性 ODE

### 标准形式

$$y'' + p(t) y' + q(t) y = r(t)$$

### 齐次方程

当 $r(t) = 0$ 时为齐次方程：

$$y'' + p(t) y' + q(t) y = 0$$

### 特征方程（常系数情形）

若 $p, q$ 为常数，设 $y = e^{\lambda t}$，得特征方程：

$$\lambda^2 + p \lambda + q = 0$$

特征根的三种情形：
1. **两个实根** $\lambda_1, \lambda_2$：$y = C_1 e^{\lambda_1 t} + C_2 e^{\lambda_2 t}$
2. **重根** $\lambda$：$y = (C_1 + C_2 t) e^{\lambda t}$
3. **共轭复根** $\lambda = \alpha \pm \beta i$：$y = e^{\alpha t}(C_1 \cos \beta t + C_2 \sin \beta t)$

---

## 7. 齐次 vs 非齐次

### 齐次方程的性质

- 解的叠加原理：若 $y_1, y_2$ 是齐次方程的解，则 $c_1 y_1 + c_2 y_2$ 也是解
- 基础解系：由两个线性无关的特解组成
- 通解结构：$y_h = C_1 y_1 + C_2 y_2$

### 非齐次方程的通解

$$y(t) = y_h(t) + y_p(t)$$

其中 $y_h$ 是齐次方程的通解，$y_p$ 是非齐次方程的一个特解。

---

## 8. 待定系数法 (Method of Undetermined Coefficients)

### 适用情形

当 $r(t)$ 是特定形式的函数（多项式、指数函数、正弦/余弦函数或其组合）时使用。

### 试探解的形式

| $r(t)$ 形式 | 试探解 $y_p$ 形式 |
|-------------|------------------|
| $P_n(t)$ | $t^s P_n(t)$ |
| $e^{\alpha t} P_n(t)$ | $t^s e^{\alpha t} P_n(t)$ |
| $e^{\alpha t} \sin \beta t$ | $t^s e^{\alpha t}(A \cos \beta t + B \sin \beta t)$ |

其中 $s$ 是使得试探解与齐次解无重复的最小非负整数。

---

## 9. 参数变分法 (Variation of Parameters)

### 方法原理

已知齐次方程的基础解 $y_1, y_2$，设非齐次方程的特解为：

$$y_p = u_1(t) y_1(t) + u_2(t) y_2(t)$$

满足条件：

$$u_1' y_1 + u_2' y_2 = 0$$

则：

$$u_1' = -\frac{y_2 r}{W(y_1, y_2)}, \quad u_2' = \frac{y_1 r}{W(y_1, y_2)}$$

其中 Wronskian 行列式为：

$$W(y_1, y_2) = \begin{vmatrix} y_1 & y_2 \\ y_1' & y_2' \end{vmatrix} = y_1 y_2' - y_1' y_2$$

---

## 10. 数值方法

### Euler 方法

**显式 Euler 公式**：

$$y_{n+1} = y_n + dt \cdot f(t_n, y_n)$$

- **局部截断误差**：$O(dt^2)$
- **整体截断误差**：$O(dt)$
- **一阶方法**

### Runge-Kutta 4 (RK4)

**四阶 Runge-Kutta 公式**：

$$k_1 = f(t_n, y_n)$$
$$k_2 = f(t_n + \frac{dt}{2}, y_n + \frac{dt}{2} k_1)$$
$$k_3 = f(t_n + \frac{dt}{2}, y_n + \frac{dt}{2} k_2)$$
$$k_4 = f(t_n + dt, y_n + dt \cdot k_3)$$
$$y_{n+1} = y_n + \frac{dt}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

- **局部截断误差**：$O(dt^5)$
- **整体截断误差**：$O(dt^4)$
- **四阶方法**，精度高，稳定性好

---

## 11. 相线分析 (Phase Line Analysis)

### 自治系统

形如 $\frac{dy}{dt} = f(y)$ 的方程称为自治系统，其中 $f$ 不显含 $t$。

### 定点 (Fixed Points)

定点是满足 $f(y) = 0$ 的点。定点处解恒等于该常数（平衡解）。

### 稳定性分类

设 $y^*$ 为定点，$f'(y^*)$ 决定稳定性：

| $f'(y^*)$ | 稳定性 |
|------------|--------|
| $< 0$ | 渐近稳定 (Asymptotically Stable) |
| $= 0$ | 需要高阶分析 |
| $> 0$ | 不稳定 (Unstable) |

### 相图绘制

1. 在相线上标出所有定点
2. 根据 $f(y)$ 的符号确定箭头方向
3. 标注稳定/不稳定定点

---

## 模块类结构

| 类名 | 功能 |
|------|------|
| `ODEProblem` | 初值问题定义，包含 Euler 和 RK4 步骤 |
| `LipschitzCondition` | Lipschitz 条件检验 |
| `PicardLindelof` | Picard-Lindelöf 定理实现 |
| `FlowProperty` | 流性质（半群性） |
| `PhasePortrait` | 相图分析（定点、稳定姓） |
| `StabilityAnalysis` | 稳定性分析（Jacobian、Lyapunov） |

---

## 使用示例

```python
from lean4py.differential_equations import ODEProblem, PhasePortrait

# 定义 dy/dt = f(t, y)
f = lambda t, y: y  # dy/dt = y

# 创建初值问题
prob = ODEProblem(f, t0=0.0, y0=1.0)

# RK4 数值解
t, y = 0.0, 1.0
dt = 0.01
for _ in range(100):
    y = prob.runge_kutta_4_step(t, y, dt)
    t += dt

# 相图分析
fixed_pts = PhasePortrait.fixed_points(lambda y: y - y**3, domain=[-2, -1, 0, 1, 2])
```