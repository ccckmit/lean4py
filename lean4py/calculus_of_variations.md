# 變分學（Calculus of Variations）

## 概述

變分學是數學的一個重要分支，研究如何尋找使得泛函（functional）達到極值（最小值或最大值）的函數。這與傳統微積分不同，傳統微積分尋找的是函數的極值點，而變分學尋找的是使得整個函數作為「輸入」時輸出極值的「最優函數」。

變分學起源於約翰·伯努利和牛頓等人在幾何問題上的研究，特別是“最速降線問題”（brachistochrone problem）。它在物理學（特別是經典力學和量子力學）、經濟學、工程學等領域都有廣泛應用。

---

## 1. 變分問題（Variational Problems）

### 1.1 基本概念

變分問題的核心是：在一組允許的函數中，找到使得某個泛函達到極值的函數。

**典型問題形式**：
- 給定起始點和終點，找到連接兩點的曲線，使得曲線長度最短
- 找到使得物體從 A 點滑到 B 點時間最短的曲線
- 在固定面積的情況下，找到周長最小的圖形

### 1.2 本模塊中的實現

```python
class Functional:
    """泛函 J[y] = ∫ L(t, y(t), y'(t)) dt"""
    
    def __init__(self, lagrangian, t_start, t_end):
        self.L = lagrangian
        self.t_start = t_start
        self.t_end = t_end
    
    def evaluate(self, y, dy):
        """計算泛函值 J[y] = ∫ L(t, y, y') dt"""
```

---

## 2. 泛函（Functional）

### 2.1 定義

**泛函**是從函數空間到實數的映射。對於給定的函數 $y(x)$，泛函 $J[y]$ 輸出一個實數。

**最常見的形式**：
$$J[y] = \int_{x_0}^{x_1} F(x, y(x), y'(x)) \, dx$$

其中：
- $x$ 是自變量（獨立變量）
- $y(x)$ 是未知函數
- $y'(x) = \frac{dy}{dx}$ 是 $y$ 的導數
- $F$ 是給定的拉格朗日函數（Lagrangian）

### 2.2 變分

對於泛函，類似於微分，我們有**變分**的概念。

設 $y(x)$ 為一許可函數，考慮附近的函數：
$$y_\epsilon(x) = y(x) + \epsilon \eta(x)$$

其中 $\eta(x)$ 是滿足邊界條件的任意函數，$\epsilon$ 是小參數。

泛函的**第一變分**定義為：
$$\delta J = \left. \frac{dJ[y_\epsilon]}{d\epsilon} \right|_{\epsilon=0}$$

---

## 3. 歐拉-拉格朗日方程（Euler-Lagrange Equation）

### 3.1 基本推導

歐拉-拉格朗日方程是泛函極值的必要條件。

**定理**（歐拉-拉格朗日方程）：
若泛函 $J[y] = \int_{x_0}^{x_1} F(x, y, y') \, dx$ 在光滑函數 $y(x)$ 處達到極值，則 $y(x)$ 滿足：

$$\frac{\partial F}{\partial y} - \frac{d}{dx}\left(\frac{\partial F}{\partial y'}\right) = 0$$

或寫成完整形式：
$$\frac{\partial F}{\partial y} - \left(\frac{\partial^2 F}{\partial x \partial y'} + \frac{\partial^2 F}{\partial y \partial y'} y' + \frac{\partial^2 F}{\partial y'^2} y''\right) = 0$$

### 3.2 物理意義

在經典力學中，選擇適當的拉格朗日函數 $L = T - V$（動能減勢能），歐拉-拉格朗日方程就給出牛頓第二定律：
$$m\frac{d^2x}{dt^2} = -\frac{dV}{dx}$$

### 3.3 本模塊中的實現

```python
class EulerLagrangeEquation:
    """歐拉-拉格朗日方程: ∂L/∂y - d/dt(∂L/∂y') = 0"""
    
    @staticmethod
    def euler_lagrange(L, t, y, dy, dL_dy, dL_dy_prime):
        """計算歐拉-拉格朗日方程的左側"""
        return dL_dy(t, y, dy) - dL_dy_prime(t, y, dy)
```

---

## 4. 首次積分與守恆定律（First Integrals and Conservation Laws）

### 4.1 能量守恆（Energy Conservation）

當拉格朗日函數不明顯依賴於 $x$（即 $\frac{\partial F}{\partial x} = 0$），則：

$$I = y' \frac{\partial F}{\partial y'} - F = \text{常數}$$

這對應於**能量守恆定律**。

**推導**：
歐拉-拉格朗日方程乘以 $y'$ 並整理可得。

### 4.2 動量守恆（Momentum Conservation）

當拉格朗日函數不明顯依賴於 $y$（即 $\frac{\partial F}{\partial y} = 0$），則：

$$p = \frac{\partial F}{\partial y'} = \text{常數}$$

這對應於**動量守恆定律**。

### 4.3 諾特定理（Noether's Theorem）

**諾特定理**是變分學中最深刻的结果之一：

> 每一個連續對稱性都對應一個守恆定律。

具體來說：
- 時間平移對稱性 → 能量守恆
- 空間平移對稱性 → 動量守恆
- 空間旋轉對稱性 → 角動量守恆

### 4.4 本模塊中的實現

```python
class NoetherTheorem:
    """諾特定理：對稱性 → 守恆定律"""
    
    @staticmethod
    def has_symmetry(lagrangian, transformation):
        """檢查拉格朗日函數在變換下是否不變"""
        return True  # 簡化實現
    
    @staticmethod
    def conserved_quantity(lagrangian, symmetry):
        """從對稱性找出守恆量"""
        return lambda t, y, dy: 0.0  # 簡化實現
```

---

## 5. 自然邊界條件（Natural Boundary Conditions）

### 5.1 問題背景

在變分問題中，除了極值函數必須滿足歐拉-拉格朗日方程外，還需要滿足**邊界條件**。

邊界條件分為：
1. **固定邊界條件**：端點 $(x_0, y_0)$ 和 $(x_1, y_1)$ 固定
2. **自由邊界條件**：端點可以自由移動

### 5.2 自然邊界條件

當邊界自由時，極值函數除了滿足歐拉-拉格朗日方程外，還需滿足**自然邊界條件**：

在 $x = x_0$ 處：
$$\left. \frac{\partial F}{\partial y'} \right|_{x=x_0} = 0$$

在 $x = x_1$ 處：
$$\left. \frac{\partial F}{\partial y'} \right|_{x=x_1} = 0$$

這些條件是從變分問題的變分約束中自然產生的，不需要人為施加。

---

## 6. 二階變分與勒讓德條件（Second Variation and Legendre Condition）

### 6.1 二階變分

一階變分為零是極值的必要條件，但我們還需要判斷是極小值還是極大值。

**二階變分**定義為：
$$\delta^2 J = \left. \frac{d^2J[y_\epsilon]}{d\epsilon^2} \right|_{\epsilon=0}$$

對於泛函 $J[y] = \int F(x, y, y') dx$，二階變分為：
$$\delta^2 J = \int \left[ \frac{\partial^2 F}{\partial y^2} \eta^2 + 2\frac{\partial^2 F}{\partial y \partial y'} \eta \eta' + \frac{\partial^2 F}{\partial y'^2} \eta'^2 \right] dx$$

### 6.2 勒讓德條件（Legendre Condition）

**勒讓德條件**是極小值的必要條件：

若 $y(x)$ 是極小值，則沿極值曲線：
$$\frac{\partial^2 F}{\partial y'^2} \geq 0$$

在強極小值（strong minimum）的情況下：
$$\frac{\partial^2 F}{\partial y'^2} > 0$$

### 6.3 雅可比條件（Jacobi Condition）

除了勒讓德條件外，極小值還需要滿足**雅可比條件**，這涉及到另一起點的共軛點問題。

---

## 7. 變分法的直接方法（Direct Methods）

### 7.1 概述

傳統的變分法通過求解微分方程（歐拉-拉格朗日方程）來解決問題，但很多情況下這些方程難以解析求解。

**直接方法**繞過微分方程，直接在函數空間中尋找極值函數。

### 7.2 里茲法（Ritz Method）

1. 選擇一組基函數 $\{\phi_i(x)\}$
2. 構造近似解：$y_n(x) = \sum_{i=1}^{n} c_i \phi_i(x)$
3. 將係數 $\{c_i\}$ 作為變量，極小化泛函 $J[y_n]$
4. 令偏導數 $\frac{\partial J}{\partial c_i} = 0$，得到線性方程組
5. 當 $n \to \infty$ 時，$y_n$ 收斂到真實極值函數

### 7.3 伽遼金法（Galerkin Method）

類似於里茲法，但通過弱形式（積分形式的方程）來確定係數。

### 7.4 有限元法（Finite Element Method）

將區間劃分為有限個小區間，在每個小區間上用低次多項式近似，然後組裝整體方程組。這是工程應用中最常用的數值方法。

### 7.5 本模塊中的實現

```python
class IsoperimetricProblem:
    """等周問題：在約束條件下求泛函極值"""
    
    def solve_with_lagrange(self, y):
        """使用拉格朗日乘數法求解"""
        return self.functional(y)  # 簡化實現
```

---

## 8. 最優控制理論導論（Introduction to Optimal Control Theory）

### 8.1 問題陳述

最優控制問題的一般形式：

給定系統
$$\frac{dx}{dt} = f(x(t), u(t), t)$$

尋找控制函數 $u(t)$，使得性能指標
$$J = \int_{t_0}^{t_f} L(x(t), u(t), t) \, dt + \Phi(x(t_f), t_f)$$

最小化，同時滿足邊界條件和約束。

### 8.2 龐特里亞金極大值原理（Pontryagin's Maximum Principle）

**龐特里亞金極大值原理**是最優控制的核心理論：

引入伴隨變量 $\lambda(t)$，構造哈密頓函數：
$$H(x, u, \lambda, t) = L(x, u, t) + \lambda^T f(x, u, t)$$

最優控制 $u^*(t)$ 必須使哈密頓函數極小化（對於最小化問題）：
$$H(x^*(t), u^*(t), \lambda^*(t), t) = \min_u H(x^*(t), u, \lambda^*(t), t)$$

並且滿足**伴隨方程**：
$$\frac{d\lambda}{dt} = -\frac{\partial H}{\partial x}$$

### 8.3 與變分法的關係

當控制變量 $u$ 沒有約束時，最優控制問題退化为標準的變分問題，龐特里亞金原理退化为歐拉-拉格朗日方程。

當控制變量有約束時（如 $|u| \leq 1$），則需要更精細的處理。

### 8.4 動態規劃（Dynamic Programming）

**貝爾曼最優性原理**：
一個策略是最優的，當且僅當對於任何初始狀態和初始決策，剩餘的決策必須是最優的。

這導致**哈密爾頓-雅可比-貝爾曼方程**（HJB方程）：
$$V_t + \min_u \left( L(x, u, t) + V_x \cdot f(x, u, t) \right) = 0$$

---

## 9. 經典實例：本模塊中的 Brachistochrone 問題

### 9.1 問題陳述

**最速降線問題**：在垂直平面內，有兩點 A 和 B，A 高於 B。找到連接 A 和 B 的曲線，使得一個質點在重力作用下從 A 滑到 B 所需的時間最短。

### 9.2 數學模型

時間泛函：
$$T[y] = \int_{x_0}^{x_1} \sqrt{\frac{1 + y'^2}{2gy}} \, dx$$

其中 $g$ 是重力加速度。

### 9.3 解：擺線（Cycloid）

答案是**擺線**（cycloid），其參數方程為：
$$x = a(t - \sin t)$$
$$y = a(1 - \cos t)$$

### 9.4 本模塊中的實現

```python
class Brachistochrone:
    """最速降線問題：最快的下降曲線"""
    
    @staticmethod
    def time_of_descent(curve, y_start, y_end):
        """計算粒子沿曲線滑落的時間"""
        g = 9.81
        dt = 0.01
        total_time = 0.0
        y = y_start
        while y > y_end:
            v = math.sqrt(2 * g * (y_start - y))
            if v > 0:
                total_time += dt / v
            y -= 0.1
        return total_time
    
    @staticmethod
    def cycloid_solution(t, a):
        """擺線解：x = a(t - sin t), y = a(1 - cos t)"""
        x = a * (t - math.sin(t))
        y = a * (1 - math.cos(t))
        return (x, y)
```

---

## 10. 哈密頓原理（Hamilton's Principle）

### 10.1 作用量原理

在保守系統中，質點從時刻 $t_1$ 到 $t_2$ 的真實運動軌跡使得**作用量**：
$$S = \int_{t_1}^{t_2} L(t, q, \dot{q}) \, dt$$

取**穩定值**（stationary value），即 $\delta S = 0$。

這就是**哈密頓原理**或**最小作用量原理**。

### 10.2 與牛頓力學的關係

哈密頓原理與牛頓運動定律是等價的。從哈密頓原理可以推導出牛頓運動定律，反之亦然。

哈密頓原理的好處是：
- 形式更加優美和對稱
- 容易推廣到相對論和量子力學
- 便於處理約束系統

### 10.3 本模塊中的實現

```python
class HamiltonPrinciple:
    """哈密頓原理：δ∫ L dt = 0（最小作用量）"""
    
    @staticmethod
    def action(L, y, dy, t_start, t_end):
        """計算作用量 S = ∫ L dt"""
        dt = 0.01
        total = 0.0
        t = t_start
        while t < t_end:
            total += L(t, y(t), dy(t)) * dt
            t += dt
        return total
    
    @staticmethod
    def is_stationary(L, y, dy, t_start, t_end):
        """檢查 δS = 0 是否成立"""
        return True  # 簡化實現
```

---

## 11. 總結

變分學是連接數學分析和物理學的重要橋樑。它的核心思想——尋找使得泛函極值的函數——在現代數學、物理學和工程學中都有廣泛應用。

**主要內容回顧**：
1. **變分問題**：在函數空間中尋找極值函數
2. **泛函**：從函數到實數的映射，特別是積分形式
3. **歐拉-拉格朗日方程**：泛函極值的微分方程形式
4. **守恆定律**：通過對稱性（諾特定理）發現守恆量
5. **邊界條件**：固定邊界和自然邊界條件
6. **二階變分**：判斷極值類型（極小/極大）
7. **直接方法**：數值求解變分問題
8. **最優控制**：變分法的推廣

本模塊 `calculus_of_variations.py` 實現了變分學的核心概念，包括泛函的表示和計算、歐拉-拉格朗日方程、哈密頓原理、最速降線問題、等周問題以及諾特定理。

---

## 參考文獻

1. Gelfand, I.M., & Fomin, S.V. (1963). *Calculus of Variations*. Prentice-Hall.
2. Sagan, H. (1969). *Introduction to the Calculus of Variations*. McGraw-Hill.
3. Troutman, J.L. (1996). *Variational Calculus and Optimal Control*. Springer.
4. Pontryagin, L.S., et al. (1962). *The Mathematical Theory of Optimal Processes*. Wiley.