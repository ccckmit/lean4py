# 偏微分方程（Partial Differential Equations）模塊

## 概述

本模塊實現了常見偏微分方程（PDE）的數值解法，包括熱方程、波方程、拉普拉斯方程和泊松方程。這些方程在物理學、工程學和數學中都有廣泛應用。

## 1. PDE 基礎理論

### 定義

偏微分方程是包含未知函數及其偏導數的方程。與常微分方程不同，PDE 涉及多個自變量（通常是空間和時間）。

**一般形式**：
$$F(x_1, x_2, \ldots, x_n, u, \frac{\partial u}{\partial x_1}, \ldots, \frac{\partial^2 u}{\partial x_i \partial x_j}, \ldots) = 0$$

### 術語說明

- **階（Order）**：方程中最高階導數的階數
- **線性 PDE**：方程對未知函數及其導數是線性的
- **非線性 PDE**：包含未知函數的非線性項

---

## 2. PDE 分類

根據特徵值和系數矩陣的性質，PDE 可分為三類：

### 2.1 橢圓型（Elliptic）

- **標準形式**：$au_{xx} + 2bu_{xy} + cu_{yy} = f(x,y)$
- **判別式**：$b^2 - 4ac < 0$
- **特性**：描述穩態過程，無特徵線
- **典型方程**：拉普拉斯方程、泊松方程

### 2.2 拋物型（Parabolic）

- **判別式**：$b^2 - 4ac = 0$
- **特性**：描述擴散和熱傳導過程
- **典型方程**：熱方程

### 2.3 雙曲型（Hyperbolic）

- **判別式**：$b^2 - 4ac > 0$
- **特性**：描述波的傳播，有兩個實特徵線
- **典型方程**：波動方程

---

## 3. 熱方程（Heat Equation）

### 數學形式

$$\frac{\partial u}{\partial t} = \alpha \nabla^2 u$$

其中：
- $u = u(x, t)$ 是溫度分佈
- $\alpha > 0$ 是熱擴散係數
- $\nabla^2$ 是拉普拉斯算子

### 物理意義

熱方程描述熱量在介質中的傳播過程，是典型的拋物型方程。

### 數值解法：顯式有限差分法

本模塊使用顯式有限差分方法：

```
u_new[i] = u[i] + r * (u[i+1] - 2*u[i] + u[i-1])
```

其中 $r = \alpha \frac{\Delta t}{\Delta x^2}$

### 穩定性條件

**Von Neumann 穩定性條件**：$r \leq 0.5$

當 $r > 0.5$ 時，數值解會發散，這是顯式方法的主要限制。

### 邊界條件

本實現使用齊次狄利克雷邊界條件：$u(0,t) = u(L,t) = 0$

---

## 4. 波動方程（Wave Equation）

### 數學形式

$$\frac{\partial^2 u}{\partial t^2} = c^2 \nabla^2 u$$

其中：
- $u = u(x, t)$ 是位移
- $c$ 是波速

### 物理意義

波動方程描述波的傳播，如弦振動、聲波、光波等，是典型的雙曲型方程。

### 數值解法：中心差分法

時間導數使用二階中心差分：

$$u_{tt} \approx \frac{u^{n+1} - 2u^n + u^{n-1}}{\Delta t^2}$$

空間導數使用二階中心差分：

$$u_{xx} \approx \frac{u_{i+1} - 2u_i + u_{i-1}}{\Delta x^2}$$

更新公式：

```
u_next[i] = 2*u_curr[i] - u_prev[i] + r * (u_curr[i+1] - 2*u_curr[i] + u_curr[i-1])
```

其中 $r = (c \cdot \Delta t / \Delta x)^2$

### 穩定性條件

**CFL 條件**：$r \leq 1$，即 $\Delta t \leq \frac{\Delta x}{c}$

### 初始條件

需要兩個初始條件：
- $u(x, 0) = u_0(x)$：初始位移
- $u_t(x, 0) = v_0(x)$：初始速度

---

## 5. 拉普拉斯方程（Laplace's Equation）

### 數學形式

$$\nabla^2 u = 0$$

或寫成：

$$\frac{\partial^2 u}{\partial x^2} + \frac{\partial^2 u}{\partial y^2} = 0$$

### 物理意義

拉普拉斯方程描述無源穩態場，如：
- 靜電場的電勢
- 不可壓縮流體的勢流
- 二維熱平衡

### 數值解法：雅可比迭代法

採用五點差分格式：

$$u_{i,j} = \frac{1}{4}(u_{i+1,j} + u_{i-1,j} + u_{i,j+1} + u_{i,j-1})$$

這實際上是對拉普拉斯算子的離散近似：

$$\nabla^2 u \approx \frac{u_{i+1,j} - 2u_{i,j} + u_{i-1,j}}{\Delta x^2} + \frac{u_{i,j+1} - 2u_{i,j} + u_{i,j-1}}{\Delta y^2} = 0$$

### 收斂性

迭代法收斂速度較慢，但簡單穩定。收斂準則：

$$\max|u_{new} - u_{old}| < \text{tol}$$

---

## 6. 泊松方程（Poisson's Equation）

### 數學形式

$$\nabla^2 u = f(x, y)$$

這是拉普拉斯方程的推廣，右端不為零。

### 物理意義

泊松方程描述有源穩態場，如：
- 帶電體的電勢分佈（其中 $f$ 與電荷密度成正比）
- 彈性膜的靜撓度

### 數值解法：有限差分迭代

離散形式：

$$u_{i,j} = \frac{\Delta y^2(u_{i+1,j} + u_{i-1,j}) + \Delta x^2(u_{i,j+1} + u_{i,j-1}) - \Delta x^2 \Delta y^2 f_{i,j}}{2(\Delta x^2 + \Delta y^2)}$$

---

## 7. 分離變量法（Separation of Variables）

### 基本思想

對於線性 PDE，假設解具有以下形式：

$$u(x, t) = X(x) \cdot T(t)$$

這將偏微分方程轉化為兩個常微分方程。

### 熱方程的例子

假設 $u(x,t) = X(x)T(t)$，代入熱方程：

$$X(x)T'(t) = \alpha X''(x)T(t)$$

除以 $X(x)T(t)$：

$$\frac{T'(t)}{\alpha T(t)} = \frac{X''(x)}{X(x)} = -\lambda$$

得到兩個常微分方程：

$$T'(t) = -\alpha\lambda T(t)$$
$$X''(x) = -\lambda X(x)$$

### 固有函數展開

邊界條件 $u(0,t) = u(L,t) = 0$ 導致：

$$X_n(x) = \sin\left(\frac{n\pi x}{L}\right), \quad \lambda_n = \left(\frac{n\pi}{L}\right)^2$$

完整解：

$$u(x,t) = \sum_{n=1}^{\infty} b_n \sin\left(\frac{n\pi x}{L}\right) e^{-\alpha\lambda_n t}$$

---

## 8. 格林函數（Green's Functions）

### 定義

格林函數 $G(x, \xi)$ 是以下方程的解：

$$\nabla^2 G = \delta(x - \xi)$$

其中 $\delta$ 是狄拉克 delta 函數。

### 物理意義

格林函數提供了線性微分方程的「基本解」。對於非齊次問題：

$$u(x) = \int G(x, \xi) f(\xi) d\xi$$

### 一維格林函數

對於 $[0, L]$ 上的泊松方程，格林函數為：

$$G(x, \xi) = \begin{cases} \frac{x(L-\xi)}{L} & x < \xi \\ \frac{\xi(L-x)}{L} & x \geq \xi \end{cases}$$

---

## 9. 弱解與索伯列夫空間（Weak Solutions and Sobolev Spaces）

### 為什麼需要弱解？

許多重要的 PDE 解可能不在古典意義下連續可微。例如：
- 激波（shock waves）
- 自由邊界問題
- 方程系數不連續

### 索伯列夫空間

定義：

$$H^m(\Omega) = \{u \in L^2(\Omega) : D^\alpha u \in L^2(\Omega), |\alpha| \leq m\}$$

其中 $L^2(\Omega)$ 是平方可積函數空間。

### 弱形式

將 PDE 兩邊乘以測試函數 $\phi \in C_c^\infty(\Omega)$，並在區域上積分：

$$\int_\Omega \nabla u \cdot \nabla \phi \, dx = \int_\Omega f \phi \, dx$$

這就是拉普拉斯方程的**弱形式**或**變分形式**。

### Lax-Milgram 定理

保證弱解的存在性和唯一性的核心定理。

---

## 模塊函數說明

### `solve_heat_equation(L, T, u0, alpha, nx, nt)`

使用顯式有限差分法求解熱方程。

**參數**：
- `L`：空間區間長度 $[0, L]$
- `T`：總模擬時間
- `u0`：初始條件函數 $u(x, 0)$
- `alpha`：熱擴散係數（默認 1.0）
- `nx`：空間格點數
- `nt`：時間步數

**返回**：(x_grid, solution)

### `solve_wave_equation(L, T, u0, v0, c, nx, nt)`

使用顯式有限差分法求解波動方程。

**參數**：
- `L`：空間區間長度
- `T`：總模擬時間
- `u0`：初始位移 $u(x, 0)$
- `v0`：初始速度 $u_t(x, 0)$
- `c`：波速（默認 1.0）
- `nx, nt`：格點和時間步數

### `solve_laplace_equation(Lx, Ly, nx, ny, max_iter, tol)`

使用雅可比迭代法求解拉普拉斯方程。

**參數**：
- `Lx, Ly`：區域邊長
- `nx, ny`：x 和 y 方向的格點數
- `max_iter`：最大迭代次數
- `tol`：收斂容差

**返回**：二維數組表示的數值解

### `solve_poisson_equation(Lx, Ly, source, nx, ny, max_iter, tol)`

使用迭代法求解泊松方程。

**參數**：
- `source`：源函數 $f(x, y)$

---

## 數值方法的穩定性總結

| 方法 | 方程類型 | 穩定性條件 |
|------|----------|-----------|
| 顯式有限差分（熱方程）| 拋物型 | $r = \alpha\Delta t/\Delta x^2 \leq 0.5$ |
| 顯式有限差分（波方程）| 雙曲型 | $r = (c\Delta t/\Delta x)^2 \leq 1$ |
| 雅可比迭代（拉普拉斯）| 橢圓型 | 收斂但可能慢 |

---

## 進一步閱讀

1. **教材**：
   - Evans, L.C. - *Partial Differential Equations*
   - Strauss, W.A. - *Partial Differential Equations: An Introduction*

2. **數值方法**：
   - LeVeque, R.J. - *Finite Difference Methods for ODE and PDE*
   - Johnson, C. - *Numerical Solution of Partial Differential Equations*

3. **數學物理**：
   - Courant, R. & Hilbert, D. - *Methods of Mathematical Physics*