# Real Analysis Module Documentation

## 模塊概述

`real_analysis.py` 模塊提供了實分析（Real Analysis）領域的核心數學概念之數值實現。該模塊包含實數表示、極限、連續性、導數、積分、級數、常微分方程數值解法等關鍵功能。

---

## 1. 實數表示與浮點數（Real Number Representation with Floating Point）

### 數學原理

計算機無法精確表示所有實數，採用 IEEE 754 雙精度浮點數（64-bit）進行近似：
- 精度：約 15-17 有效十進制位
- 最小正數：≈ 2.2 × 10⁻³⁰⁸
- 最大正數：≈ 1.8 × 10³⁰⁸

### 代碼實現

```python
class Real:
    def __init__(self, value: float):
        self.value = float(value)
```

`Real` 類封裝浮點數值，提供基本算術運算（加、減、乘、除）和比較運算。相等判斷使用容差機制：

```python
def __eq__(self, other):
    if isinstance(other, Real):
        return abs(self.value - other.value) < 1e-10
    return False
```

---

## 2. 函數極限（Limit of a Function）

### 數學定義

函數 f(x) 在 x → x₀ 时的極限 L 定义为：
$$\lim_{x \to x_0} f(x) = L$$

即對于任意 ε > 0，存在 δ > 0，使得當 0 < |x - x₀| < δ 時，|f(x) - L| < ε。

### 數值逼近

本模塊使用雙側逼近法：

```python
def limit(f: Callable[[float], float], x0: float, h: float = 1e-8) -> Real:
    left_limit = f(x0 - h)
    right_limit = f(x0 + h)
    if abs(left_limit - right_limit) < 1e-6:
        return Real((left_limit + right_limit) / 2)
    return Real((left_limit + right_limit) / 2)
```

取左右極限的平均值作為逼近值：
$$\lim_{x \to x_0} f(x) \approx \frac{f(x_0 - h) + f(x_0 + h)}{2}$$

---

## 3. 左極限與右極限（Left and Right Limits）

### 數學定義

- **左極限**：$$\lim_{x \to x_0^-} f(x) = L_1$$
- **右極限**：$$\lim_{x \to x_0^+} f(x) = L_2$$

當 L₁ = L₂ 時，雙側極限存在。

### 代碼實現

```python
def limit_left(f: Callable[[float], float], x0: float, h: float = 1e-8) -> Real:
    return Real(f(x0 - h))

def limit_right(f: Callable[[float], float], x0: float, h: float = 1e-8) -> Real:
    return Real(f(x0 + h))
```

---

## 4. 連續性（Continuity）

### ε-δ 定義（數值近似）

函數 f 在點 x₀ 連續當且僅當：
$$\forall \varepsilon > 0, \exists \delta > 0, \text{ 使得 } |x - x_0| < \delta \Rightarrow |f(x) - f(x_0)| < \varepsilon$$

### 數值實現

```python
def is_continuous(f: Callable[[float], float], x0: float, delta: float = 1e-6) -> bool:
    limit_val = limit(f, x0, delta)
    f_val = f(x0)
    return abs(limit_val.value - f_val) < 1e-6
```

通過比較極限值與函數值之差是否小於容差來判斷連續性。

---

## 5. 導數（Derivative）

### 數學定義

$$f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

### 中央差分法（Central Difference）

本模塊使用二階中央差分公式：
$$f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$$

```python
def derivative(f: Callable[[float], float], x: float, h: float = 1e-8) -> Real:
    left_deriv = (f(x) - f(x - h)) / h
    right_deriv = (f(x + h) - f(x)) / h
    if abs(left_deriv - right_deriv) > 1e-6:
        return Real(float('nan'))
    df = (f(x + h) - f(x - h)) / (2 * h)
    return Real(df)
```

中央差分法的誤差為 O(h²)，優於前向差分 O(h) 和後向差分 O(h)。

---

## 6. 偏導數（Partial Derivatives）

### 數學定義

對於多元函數 f(x₁, x₂, ..., xₙ)，關於第 i 個變量的偏導數：
$$\frac{\partial f}{\partial x_i} = \lim_{h \to 0} \frac{f(x_1, ..., x_i + h, ..., x_n) - f(x_1, ..., x_i, ..., x_n)}{h}$$

### 代碼實現

```python
def partial_derivative(f: Callable[[List[float]], float], x: List[float], var_idx: int, h: float = 1e-8) -> Real:
    def single_var(t):
        vals = x[:]
        vals[var_idx] = t
        return f(vals)
    return derivative(single_var, x[var_idx], h)
```

通過固定其他變量，將多元函數轉化為單變量函數，然後調用 `derivative` 計算。

---

## 7. 積分——黎曼和與梯形法則（Integral as Limit of Riemann Sums）

### 數學定義

定積分定義為黎曼和的極限：
$$\int_a^b f(x)\,dx = \lim_{n \to \infty} \sum_{i=1}^{n} f(x_i^*) \Delta x$$

其中 Δx = (b - a)/n。

### 梯形法則（Trapezoidal Rule）

本模塊使用梯形法則逼近：
$$\int_a^b f(x)\,dx \approx \frac{\Delta x}{2} \left[ f(x_0) + 2\sum_{i=1}^{n-1} f(x_i) + f(x_n) \right]$$

```python
def integral(f: Callable[[float], float], a: float, b: float, n: int = 1000) -> Real:
    if a >= b:
        return Real(0)
    dx = (b - a) / n
    result = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        result += f(a + i * dx)
    return Real(result * dx)
```

誤差為 O(1/n²)。

---

## 8. 泰勒級數（Taylor Series）

### 數學定義

函數 f 在點 x₀ 处的泰勒展開：
$$f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(x_0)}{n!} \cdot (x - x_0)^n$$

### 代碼實現

```python
def nth_derivative(f: Callable[[float], float], x0: float, n: int, h: float = 0.001) -> float:
    if n == 0:
        return f(x0)
    result = 0.0
    for k in range(n + 1):
        result += (-1) ** (n - k) * math.comb(n, k) * f(x0 + k * h)
    return result / (h ** n)

def taylor_series(f: Callable[[float], float], x0: float, n: int, h: float = 0.001) -> Callable[[float], float]:
    coeffs = []
    for i in range(n + 1):
        coeffs.append(nth_derivative(f, x0, i, h))
    def taylor(x):
        result = 0.0
        for i, c in enumerate(coeffs):
            result += c * ((x - x0) ** i) / math.factorial(i)
        return result
    return taylor
```

n 階泰勒多項式 Tₙ(x) 逼近原函數，誤差余項：
$$R_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!} \cdot (x - x_0)^{n+1}$$

---

## 9. 麥克勞林級數（Maclaurin Series）

### 數學定義

泰勒級數在 x₀ = 0 处的特例：
$$f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(0)}{n!} \cdot x^n$$

### 代碼實現

```python
def mclaurin_series(f: Callable[[float], float], n: int, h: float = 1e-8) -> Callable[[float], float]:
    return taylor_series(f, 0.0, n, h)
```

---

## 10. 洛必達法則（L'Hôpital's Rule）

### 數學定義

對於不定式 0/0 或 ∞/∞：
$$\lim_{x \to x_0} \frac{f(x)}{g(x)} = \lim_{x \to x_0} \frac{f'(x)}{g'(x)}$$

若仍是不定式，可重複應用。

### 數值實現

```python
def lhopital_limit(f: Callable[[float], float], g: Callable[[float], float], x0: float, n: int = 10) -> Optional[Real]:
    for _ in range(n):
        f0, g0 = f(x0), g(x0)
        if abs(g0) > 1e-10:
            break
        f = derivative(f, x0)
        g = derivative(g, x0)
    try:
        return limit(lambda x: f(x) / g(x), x0)
    except:
        return None
```

迭代計算分子分母的導數，直到不再是 0/0 型。

---

## 11. 數列極限與收斂（Sequence Limit and Convergence）

### 數學定義

數列 {aₙ} 收斂於 L：
$$\lim_{n \to \infty} a_n = L$$

### 单调有界收斂定理

**定理**：单调递增且有上界的数列必收斂；单调递减且有下界的数列必收斂。

```python
def sequence_limit(a_n: Callable[[int], float], n0: int = 1, tolerance: float = 1e-6, max_iter: int = 100000) -> Tuple[Real, bool]:
    prev = a_n(n0)
    for n in range(n0 + 1, n0 + max_iter):
        curr = a_n(n)
        if abs(curr - prev) < tolerance:
            return (Real(curr), True)
        prev = curr
    return (Real(prev), False)

def is_monotonic(a_n: Callable[[int], float], n_start: int = 1, n_end: int = 100) -> str:
    increasing = decreasing = True
    for n in range(n_start, n_end):
        diff = a_n(n + 1) - a_n(n)
        if diff <= 0:
            increasing = False
        if diff >= 0:
            decreasing = False
    if increasing:
        return "increasing"
    elif decreasing:
        return "decreasing"
    else:
        return "non-monotonic"

def is_bounded(a_n: Callable[[int], float], n_start: int = 1, n_end: int = 1000) -> Tuple[bool, bool]:
    values = [a_n(n) for n in range(n_start, n_end)]
    lower_bound = min(values)
    upper_bound = max(values)
    return (lower_bound > -float('inf'), upper_bound < float('inf'))
```

---

## 12. 無窮級數與收斂判斷（Infinite Series and Convergence Tests）

### 數學定義

無窮級數 $\sum_{n=1}^{\infty} a_n$ 收斂當且僅當部分和 Sₙ = Σaᵢ 收斂。

### 比值判別法（Ratio Test）

$$\lim_{n \to \infty} \left| \frac{a_{n+1}}{a_n} \right| = L$$

- 若 L < 1：級數絕對收斂
- 若 L > 1：級數發散
- 若 L = 1：判別法失效

```python
def ratio_test(a_n: List[float]) -> str:
    if len(a_n) < 2:
        return "inconclusive"
    ratios = [abs(a_n[i+1] / a_n[i]) for i in range(len(a_n)-1) if a_n[i] != 0]
    if not ratios:
        return "inconclusive"
    last_ratios = ratios[-min(5, len(ratios)):]
    avg_ratio = sum(last_ratios) / len(last_ratios)
    if avg_ratio < 1:
        return "converges"
    elif avg_ratio > 1:
        return "diverges"
    return "inconclusive"
```

### 根值判別法（Root Test）

$$\lim_{n \to \infty} \sqrt[n]{|a_n|} = L$$

- 若 L < 1：級數收斂
- 若 L > 1：級數發散
- 若 L = 1：判別法失效

```python
def root_test(a_n: List[float]) -> str:
    if not a_n:
        return "inconclusive"
    roots = [abs(x) ** (1/(i+1)) for i, x in enumerate(a_n) if x != 0]
    if not roots:
        return "inconclusive"
    lim_sup = max(roots)
    if lim_sup < 1:
        return "converges"
    elif lim_sup > 1:
        return "diverges"
    return "inconclusive"
```

---

## 13. 常微分方程數值方法（ODE Numerical Methods）

### 13.1 歐拉法（Euler Method）

#### 數學原理

一階常微分方程初值問題：
$$\frac{dy}{dt} = f(t, y), \quad y(t_0) = y_0$$

歐拉法離散化：
$$y_{n+1} = y_n + h \cdot f(t_n, y_n)$$

其中 h 為時間步長。歐拉法精度為 O(h)，為一階方法。

```python
def euler_method(
    f: Callable[[float, List[float]], List[float]],
    y0: List[float],
    t_span: Tuple[float, float],
    dt: float = 0.01
) -> Tuple[List[float], List[List[float]]]:
    t0, tf = t_span
    n_steps = int((tf - t0) / dt)
    t_vals = [t0 + i * dt for i in range(n_steps + 1)]
    y_vals = [y0[:]]
    
    y = y0[:]
    for i in range(n_steps):
        dydt = f(t_vals[i], y)
        y = [y[j] + dt * dydt[j] for j in range(len(y))]
        y_vals.append(y[:])
    
    return t_vals, y_vals
```

### 13.2 四階龍格-庫塔法（Runge-Kutta 4）

#### 數學原理

四階龍格-庫塔法使用四個斜率估計值的加權平均：
$$k_1 = f(t_n, y_n)$$
$$k_2 = f\left(t_n + \frac{h}{2}, y_n + \frac{h}{2}k_1\right)$$
$$k_3 = f\left(t_n + \frac{h}{2}, y_n + \frac{h}{2}k_2\right)$$
$$k_4 = f(t_n + h, y_n + h \cdot k_3)$$

$$y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)$$

精度為 O(h⁴)，為四階方法。

```python
def runge_kutta_4(
    f: Callable[[float, List[float]], List[float]],
    y0: List[float],
    t_span: Tuple[float, float],
    dt: float = 0.01
) -> Tuple[List[float], List[List[float]]]:
    t0, tf = t_span
    n_steps = int((tf - t0) / dt)
    t_vals = [t0 + i * dt for i in range(n_steps + 1)]
    y_vals = [y0[:]]
    
    y = y0[:]
    for i in range(n_steps):
        t = t_vals[i]
        k1 = f(t, y)
        k2 = f(t + dt/2, [y[j] + dt/2 * k1[j] for j in range(len(y))])
        k3 = f(t + dt/2, [y[j] + dt/2 * k2[j] for j in range(len(y))])
        k4 = f(t + dt, [y[j] + dt * k3[j] for j in range(len(y))])
        y = [y[j] + dt/6 * (k1[j] + 2*k2[j] + 2*k3[j] + k4[j]) for j in range(len(y))]
        y_vals.append(y[:])
    
    return t_vals, y_vals
```

---

## 14. 自適應辛普森法則（Adaptive Simpson's Rule）

### 數學原理

辛普森法則（Simpson's Rule）使用二次多項式逼近：
$$\int_a^b f(x)\,dx \approx \frac{h}{6}\left[f(a) + 4f\left(\frac{a+b}{2}\right) + f(b)\right]$$

其中 h = (b - a)/2。

### 自適應演算法

自適應方法根據局部誤差估計動態調整子區間：

```python
def adaptive_simpson(f: Callable[[float], float], a: float, b: float, 
                     tol: float = 1e-6, max_depth: int = 20) -> float:
    def _simpson(f, a, b):
        c = (a + b) / 2
        h = (b - a) / 6
        return h * (f(a) + 4*f(c) + f(b))
    
    def _recursive(f, a, b, S, tol, depth):
        c = (a + b) / 2
        S_left = _simpson(f, a, c)
        S_right = _simpson(f, c, b)
        if depth <= 0 or abs(S_left + S_right - S) < 15 * tol:
            return S_left + S_right + (S_left + S_right - S) / 15
        return (_recursive(f, a, c, S_left, tol/2, depth-1) +
                _recursive(f, c, b, S_right, tol/2, depth-1))
    
    S0 = _simpson(f, a, b)
    return _recursive(f, a, b, S0, tol, max_depth)
```

**誤差控制**：當 |S - (S_left + S_right)| < 15·tol 时，认为子区间精度足够，停止细分。

---

## 附錄：類層次結構

### Function 類

```python
class Function:
    def __init__(self, f: Callable[[float], float], domain: Optional[Tuple[float, float]] = None):
        self.f = f
        self.domain = domain or (float('-inf'), float('inf'))
    
    def __call__(self, x: float) -> float:
        if self.domain[0] <= x <= self.domain[1]:
            return self.f(x)
        raise ValueError(f"x = {x} is outside domain {self.domain}")
```

提供函數封裝，支持定義域檢查，並內建 limit、derivative、integral 等方法。

### Sequence 類

```python
class Sequence:
    def __init__(self, a_n: Callable[[int], float]):
        self.a_n = a_n
    
    def limit(self, n0: int = 1, tolerance: float = 1e-8) -> Tuple[Real, bool]:
        return sequence_limit(self.a_n, n0, tolerance)
    
    def is_monotonic(self, n_start: int = 1, n_end: int = 100) -> str:
        return is_monotonic(self.a_n, n_start, n_end)
    
    def is_bounded(self, n_start: int = 1, n_end: int = 1000) -> Tuple[bool, bool]:
        return is_bounded(self.a_n, n_start, n_end)
    
    def converges(self, n_start: int = 1) -> bool:
        limit_val, converged = self.limit(n_start)
        if not converged:
            return False
        m = is_monotonic(self.a_n, n_start, n_start + 100)
        lower, upper = is_bounded(self.a_n, n_start, n_start + 100)
        return (m != "non-monotonic") and lower and upper
```

---

## 參考文獻

1. Apostol, T. M. (1967). *Calculus*, Vol. 1. Wiley.
2. Burden, R. L., & Faires, J. D. (2011). *Numerical Analysis*. Cengage Learning.
3. Rudin, W. (1976). *Principles of Mathematical Analysis*. McGraw-Hill.