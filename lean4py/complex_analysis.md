# 複變分析 (Complex Analysis)

本模組實現了複變分析的核心概念，對應 mathlib4 的 `Mathlib.Analysis.Complex` 模組。

---

## 1. 複數 (Complex Numbers)

### 定義

複數的形式為：

$$z = x + iy$$

其中：
- $x, y \in \mathbb{R}$ 為實數
- $i$ 為虛數單位，滿足 $i^2 = -1$
- $x$ 稱為實部 (Real Part)：$\text{Re}(z) = x$
- $y$ 稱為虛部 (Imaginary Part)：$\text{Im}(z) = y$

### 基本運算

設 $z_1 = x_1 + iy_1$，$z_2 = x_2 + iy_2$：

| 運算 | 公式 |
|------|------|
| 加法 | $z_1 + z_2 = (x_1 + x_2) + i(y_1 + y_2)$ |
| 減法 | $z_1 - z_2 = (x_1 - x_2) + i(y_1 - y_2)$ |
| 乘法 | $z_1 \cdot z_2 = (x_1x_2 - y_1y_2) + i(x_1y_2 + y_1x_2)$ |
| 除法 | $\dfrac{z_1}{z_2} = \dfrac{x_1x_2 + y_1y_2}{x_2^2 + y_2^2} + i\dfrac{y_1x_2 - x_1y_2}{x_2^2 + y_2^2}$ |

### 模與共軛

- **模 (Modulus)**：$|z| = \sqrt{x^2 + y^2}$
- **共軛複數 (Conjugate)**：$\overline{z} = x - iy$

---

## 2. 複平面與 Argand 圖

複數 $z = x + iy$ 可以視為平面上的點 $(x, y)$，這個平面稱為**複平面** (Complex Plane) 或 **Argand 平面**。

### Argand 圖

```
        Im(z)
          │
          │        z = x + iy
          │        ↑
          │       ╱
          │      ╱
          │     ╱
          │    ● (x, y)
          │   ╱
          │  ╱
          │ ╱
          │╱
 ─────────┼──────────→ Re(z)
         ╱│
        ╱ │
       ╱  │
```

### 極座標表示

任意複數可表示為：

$$z = r(\cos\theta + i\sin\theta)$$

其中：
- $r = |z|$ 為模
- $\theta = \arg(z)$ 為輻角 (argument)

---

## 3. Euler 公式 (Euler's Formula)

### 公式

$$e^{i\theta} = \cos\theta + i\sin\theta$$

### 推論

1. **複數的極座標形式**：
   $$z = re^{i\theta} = r(\cos\theta + i\sin\theta)$$

2. **De Moivre 公式**：
   $$(\cos\theta + i\sin\theta)^n = \cos(n\theta) + i\sin(n\theta)$$

3. **歐拉恆等式** (當 $\theta = \pi$)：
   $$e^{i\pi} + 1 = 0$$

### 幾何意義

Euler 公式將指數函數與三角函數連繫起來，在複平面上，$e^{i\theta}$ 對應單位圓上角度為 $\theta$ 的點。

---

## 4. 複變微分與全純函數 (Holomorphic Functions)

### 定義

設 $f: \mathbb{C} \to \mathbb{C}$ 為複變函數，若極限

$$f'(z) = \lim_{h \to 0} \frac{f(z+h) - f(z)}{h}$$

存在，則稱 $f$ 在 $z$ 處**可微** (Differentiable)。若 $f$ 在區域 $D$ 內處處可微，則稱 $f$ 為**全純函數** (Holomorphic Function)。

### Cauchy-Riemann 方程組

設 $f(z) = u(x, y) + iv(x, y)$，其中 $u, v: \mathbb{R}^2 \to \mathbb{R}$。

$f$ 在 $z = x + iy$ 處全純的充要條件是 $u$ 和 $v$ 滿足 **Cauchy-Riemann 方程組**：

$$\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y} \quad \text{且} \quad \frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}$$

### 模組實作

```python
class CauchyRiemann:
    """Cauchy-Riemann equations: ∂u/∂x = ∂v/∂y, ∂u/∂y = -∂v/∂x."""
```

---

## 5. 複變積分與路徑積分 (Contour Integrals)

### 定義

設 $\gamma$ 為複平面上一條分段光滑曲線，$f$ 為連續函數，則

$$\int_\gamma f(z)\,dz = \int_a^b f(\gamma(t))\gamma'(t)\,dt$$

### 基本性質

1. **線性性**：
   $$\int_\gamma (af + bg)\,dz = a\int_\gamma f\,dz + b\int_\gamma g\,dz$$

2. **反向路徑**：
   $$\int_{-\gamma} f(z)\,dz = -\int_\gamma f(z)\,dz$$

3. **路徑可加性**：
   $$\int_{\gamma_1 + \gamma_2} f(z)\,dz = \int_{\gamma_1} f(z)\,dz + \int_{\gamma_2} f(z)\,dz$$

### 數值計算

模組使用數值近似：

```python
# 沿圓形路徑積分
for k in range(n_points):
    theta = 2πk / n_points
    z = center + radius * exp(i*theta)
    dz = radius * exp(i*theta) * 2π / n_points
    integral += f(z) * dz
```

---

## 6. Cauchy 積分定理與公式

### Cauchy 定理 (Cauchy's Integral Theorem)

若 $f$ 在單連通區域 $D$ 內全純，則對於 $D$ 內任意封閉曲線 $\gamma$：

$$\oint_\gamma f(z)\,dz = 0$$

### Cauchy 積分公式 (Cauchy's Integral Formula)

若 $f$ 在封閉路徑 $\gamma$ 內部全純，則對於內部任意點 $z_0$：

$$f(z_0) = \frac{1}{2\pi i}\oint_\gamma \frac{f(z)}{z - z_0}\,dz$$

### 高階導數公式

$$f^{(n)}(z_0) = \frac{n!}{2\pi i}\oint_\gamma \frac{f(z)}{(z - z_0)^{n+1}}\,dz$$

### 模組實作

```python
class CauchyIntegralFormula:
    """Cauchy integral formula."""
    
    @staticmethod
    def cauchy_integral(f, z0, radius=1.0, n_points=1000):
        """f(z0) = (1/2πi) ∮_γ f(z)/(z-z0) dz."""
    
    @staticmethod
    def nth_derivative(f, z0, n=1, radius=1.0):
        """f^(n)(z0) = n!/(2πi) ∮ f(z)/(z-z0)^(n+1) dz."""
```

---

## 7. Laurent 級數 (Laurent Series)

### 定義

在全純環域 $r < |z - z_0| < R$ 內，任意全純函數可展開為：

$$f(z) = \sum_{n=-\infty}^{\infty} a_n (z - z_0)^n$$

其中係數：

$$a_n = \frac{1}{2\pi i}\oint_\gamma \frac{f(z)}{(z - z_0)^{n+1}}\,dz$$

### Laurent 級數的結構

- **解析部分** (Analytic Part)：$\sum_{n=0}^{\infty} a_n (z - z_0)^n$
- **主要部分** (Principal Part)：$\sum_{n=1}^{\infty} a_{-n} (z - z_0)^{-n}$

### 與 Taylor 級數的關係

當函數在 $z_0$ 處全純時，主要部分為零，Laurent 級數退化为 Taylor 級數。

### 模組實作

```python
class LaurentSeries:
    """Laurent series expansion around a point."""
    
    @staticmethod
    def series(f, z0, n_terms=10):
        """Compute Laurent series: Σ a_n (z-z0)^n."""
```

---

## 8. 留數定理 (Residue Theorem)

### 孤立奇點

若 $z_0$ 為 $f$ 的孤立奇點，則 $f$ 在 $z_0$ 處的**留數** (Residue) 定義為：

$$\text{Res}(f, z_0) = \frac{1}{2\pi i}\oint_\gamma f(z)\,dz$$

其中 $\gamma$ 為環繞 $z_0$ 的小圓。

### 留數計算

對於簡單極點 $z_0$：

$$\text{Res}(f, z_0) = \lim_{z \to z_0} (z - z_0)f(z)$$

### 留數定理

設 $f$ 在封閉路徑 $\gamma$ 內除了有限個孤立奇點 $z_1, z_2, \ldots, z_n$ 外皆全純，則：

$$\oint_\gamma f(z)\,dz = 2\pi i \sum_{k=1}^{n} \text{Res}(f, z_k)$$

### 模組實作

```python
class ResidueTheorem:
    """Residue theorem: ∮ f(z) dz = 2πi Σ Res(f, z_k)."""
    
    @staticmethod
    def residue(f, z0):
        """Compute residue at z0 (simple poles)."""
        h = 1e-6
        return h * f(z0 + h)  # Res = lim (z-z0)f(z)
```

---

## 9. 共形映射 (Conformal Mappings)

### 定義

設 $f$ 為區域 $D$ 內的全純單射，則 $f$ 稱為**共形映射** (Conformal Map)。

### 保角性質

全純函數的導數 $f'(z_0) \neq 0$ 時：
- 無限小圓映射為無限小圓
- 保持兩曲線間的夾角大小與方向

### 常用共形映射

| 映射 | 公式 | 用途 |
|------|------|------|
| 平移 | $w = z + a$ | 平面平移 |
| 旋轉與縮放 | $w = az$ | 原點縮放與旋轉 |
| 反演 | $w = 1/z$ | 單位圓內外部映射 |
| Möbius 變換 | $w = \dfrac{az + b}{cz + d}$ | 圓保持映射 |

### Riemann 映射定理

任意兩個單連通區域（邊界多於一點）之間存在共形映射。

---

## 其他重要定理

### Liouville 定理

若 $f$ 為整函數 (entire function) 且有界，則 $f$ 為常數函數。

```python
class LiouvilleTheorem:
    """Liouville's theorem: bounded entire functions are constant."""
```

### 最大模原理 (Maximum Modulus Principle)

若 $f$ 在區域 $D$ 內全純，則 $|f|$ 不能在 $D$ 內部達到最大值，除非 $f$ 為常數。

```python
class MaximumModulusPrinciple:
    """Maximum modulus principle: |f| attains maximum on boundary."""
```

### 幅角原理 (Argument Principle)

$$\frac{1}{2\pi i}\oint_\gamma \frac{f'(z)}{f(z)}\,dz = N - P$$

其中 $N$ 為零點數，$P$ 為極點數（計數重數）。

```python
class ArgumentPrinciple:
    """Argument principle: (1/2πi) ∮ f'(z)/f(z) dz = N - P."""
```

---

## 模組結構

```
complex_analysis.py
├── ComplexFunction         # 複變函數類
├── CauchyRiemann          # Cauchy-Riemann 方程組
├── CauchyIntegralFormula  # Cauchy 積分公式
├── LiouvilleTheorem       # Liouville 定理
├── MaximumModulusPrinciple # 最大模原理
├── ResidueTheorem         # 留數定理
├── LaurentSeries          # Laurent 級數
└── ArgumentPrinciple      # 幅角原理
```

---

## 參考文獻

1. Ahlfors, L. V. (1979). *Complex Analysis*. McGraw-Hill.
2. Conway, J. B. (1978). *Functions of One Complex Variable*. Springer.
3. Stein, E. M., & Shakarchi, R. (2003). *Complex Analysis*. Princeton University Press.