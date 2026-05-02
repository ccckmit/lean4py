# real_analysis 測試文檔

本文檔說明 `lean4py/real_analysis.py` 模塊的測試設計與數學原理。

## 1. 測試驗證概述

本模塊測試涵蓋實分析的核心概念：極限、微積分、級數收斂性以及常微分方程數值解法。

## 2. 極限測試 (Limit Tests)

### 測試函數
- `limit(f, x0)` - 雙側極限
- `limit_left(f, x0)` - 左極限
- `limit_right(f, x0)` - 右極限

### 數學原理

**極限定義**：對於任意 ε > 0，存在 δ > 0 使得當 0 < |x - x0| < δ 時，|f(x) - L| < ε。

**測試案例**：
- `test_limit_simple`: f(x) = x，lim_{x→2} x = 2
- `test_limit_polynomial`: f(x) = x² + 1，lim_{x→1} (x² + 1) = 2
- `test_limit_sin`: f(x) = sin(x)/x，lim_{x→0} sin(x)/x = 1（重要極限）

```python
def test_limit_sin(self):
    f = lambda x: math.sin(x) / x
    result = limit(f, 0)
    assert abs(result.value - 1.0) < 1e-4  # 重要極限：lim sin(x)/x = 1
```

## 3. 導數測試 (Derivative Tests)

### 測試函數
- `derivative(f, x)` - 計算導數 f'(x)
- `is_differentiable(f, x)` - 判斷是否可導

### 數學原理

**導數定義**：f'(x) = lim_{h→0} [f(x+h) - f(x)] / h

**數值導數計算**：通常使用中心差分公式：
f'(x) ≈ [f(x+h) - f(x-h)] / (2h)

**測試案例**：
- `test_derivative_polynomial`: f(x) = x²，f'(3) = 6
- `test_derivative_sin`: f(x) = sin(x)，f'(0) = cos(0) = 1
- `test_derivative_cos`: f(x) = cos(x)，f'(0) = -sin(0) = 0

```python
def test_derivative_polynomial(self):
    f = lambda x: x**2
    result = derivative(f, 3)
    assert abs(result.value - 6.0) < 1e-4  # f'(x) = 2x, f'(3) = 6
```

### 可導性判斷

```python
def test_is_differentiable_abs(self):
    f = lambda x: abs(x)
    assert not is_differentiable(f, 0.0)  # |x| 在 0 處不可導
```

**數學解釋**：|x| 在 x=0 處，左導數為 -1，右導數為 +1，導數不存在。

## 4. 積分測試 (Integral Tests)

### 測試函數
- `integral(f, a, b)` - 定積分
- `riemann_sum(f, a, b, n, method)` - 黎曼和
- `adaptive_simpson(f, a, b, tol)` - 自適應 Simpson 法

### 數學原理

**定積分**：∫[a,b] f(x) dx = F(b) - F(a)，其中 F'(x) = f(x)

**黎曼和**：將區間 [a,b] 分成 n 個小區間，求和：
- 左端點黎曼和：Σ f(a + i·Δx)·Δx，i=0 到 n-1
- 右端點黎曼和：Σ f(a + i·Δx)·Δx，i=1 到 n

```python
def test_integral_x2(self):
    f = lambda x: x**2
    result = integral(f, 0, 1)
    assert abs(result.value - 1.0/3.0) < 1e-4  # ∫₀¹ x² dx = [x³/3]₀¹ = 1/3
```

### 自適應 Simpson 法

基於 Simpson 公式：∫ ≈ (b-a)/6 · [f(a) + 4f((a+b)/2) + f(b)]

通過遞歸細分直到誤差不超過 tolerance。

## 5. 數列極限測試 (Sequence Limit Tests)

### 測試函數
- `sequence_limit(a_n)` - 數列極限
- `is_monotonic(a_n, n1, n2)` - 判斷單調性
- `is_bounded(a_n, n1, n2)` - 判斷有界性

### 數學原理

**單調收斂定理**：單調有界數列必收斂。

```python
def test_sequence_limit(self):
    a_n = lambda n: 1 / n
    result, converged = Sequence(a_n).limit()
    assert converged
    assert result.value < 0.001  # lim 1/n = 0
```

**單調性判斷**：
```python
def test_sequence_monotonic(self):
    a_n = lambda n: n / (n + 1)
    assert is_monotonic(a_n, 1, 100) == "increasing"  # 單調遞增
```

## 6. 收斂性測試 (Convergence Tests)

### 測試函數
- `converges(series)` - 判斷級數收斂
- `infinite_series_sum(a_n)` - 無窮級數求和
- `ratio_test(a_n)` - 比值判別法
- `root_test(a_n)` - 根值判別法

### 數學原理

**比值判別法**：若 L = lim |a_{n+1}/a_n| < 1，則級數收斂；L > 1 則發散。

**根值判別法**：若 L = lim sup |a_n|^{1/n} < 1，則收斂。

```python
def test_converges_geometric(self):
    series = lambda n: (1/2) ** n
    assert converges(series)  # 等比級數，公比 1/2 < 1，收斂

def test_converges_harmonic(self):
    series = lambda n: 1 / n
    assert not converges(series)  # 調和級數發散
```

**等比級數求和**：Σ (1/2)^n = 1/(1 - 1/2) = 2，但首項從 n=0 開始故為 1。

## 7. Taylor 級數測試 (Taylor Series Tests)

### 測試函數
- `taylor_series(f, a, n)` - 在點 a 展開 n 階 Taylor 級數
- `mclaurin_series(f, n)` - Maclaurin 級數（a=0）

### 數學原理

**Taylor 展開**：f(x) = Σ_{k=0}^n f^{(k)}(a)/k! · (x-a)^k + R_n

**sin(x) 的 Maclaurin 展開**：
sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...

```python
def test_taylor_sin(self):
    f = lambda x: math.sin(x)
    taylor_fn = taylor_series(f, 0, 5)  # 5 階展開
    approx = taylor_fn(math.pi / 4)
    assert abs(approx - math.sin(math.pi / 4)) < 1e-1
```

## 8. ODE 數值方法測試

### 歐拉法 (Euler Method)

**數學原理**：一階常微分方程 dy/dt = f(t,y)，y(t₀) = y₀

**歐拉公式**：y_{n+1} = y_n + h·f(t_n, y_n)，其中 h 為步長

```python
def test_exp_growth(self):
    """dy/dt = y, y(0)=1, solution: y=e^t."""
    f = lambda t, y: [y[0]]
    t_vals, y_vals = euler_method(f, [1.0], (0.0, 1.0), dt=0.01)
    y_final = y_vals[-1][0]
    assert abs(y_final - math.e) < 0.1  # 近似 e ≈ 2.71828
```

**誤差分析**：歐拉法為一階方法，局部截斷誤差為 O(h²)，全局誤差為 O(h)。

### 四階龍格-庫塔法 (Runge-Kutta 4)

**數學原理**：更高精度的數值方法

**RK4 公式**：
- k₁ = h·f(t_n, y_n)
- k₂ = h·f(t_n + h/2, y_n + k₁/2)
- k₃ = h·f(t_n + h/2, y_n + k₂/2)
- k₄ = h·f(t_n + h, y_n + k₃)
- y_{n+1} = y_n + (k₁ + 2k₂ + 2k₃ + k₄)/6

```python
def test_exp_growth(self):
    f = lambda t, y: [y[0]]
    t_vals, y_vals = runge_kutta_4(f, [1.0], (0.0, 1.0), dt=0.1)
    y_final = y_vals[-1][0]
    assert abs(y_final - math.e) < 0.05  # 比歐拉法更精確
```

### 諧振子測試

```python
def test_harmonic_oscillator(self):
    """d²x/dt² = -x, solution: x=cos(t)."""
    # 轉換為一階系統：dy0/dt = y1, dy1/dt = -y0
    f = lambda t, y: [y[1], -y[0]]
    t_vals, y_vals = runge_kutta_4(f, [1.0, 0.0], (0.0, 3.14159), dt=0.01)
    x_final = y_vals[-1][0]
    assert abs(x_final - (-1.0)) < 0.1  # cos(π) = -1
```

## 9. 連續性測試 (Continuity Tests)

### 測試函數
- `is_continuous(f, x)` - 判斷函數在 x 處是否連續

### 數學原理

**連續定義**：lim_{x→x₀} f(x) = f(x₀)

```python
def test_is_continuous_polynomial(self):
    f = lambda x: x**2
    assert is_continuous(f, 1.0)  # 多項式處處連續
```

## 10. 測試用例總表

| 類別 | 測試方法 | 驗證內容 |
|------|----------|----------|
| Real | test_real_init, test_real_operations | 實數基本運算 |
| Limit | test_limit_* | 多項式、三角函數極限 |
| Derivative | test_derivative_* | 多項式、三角導數 |
| Integral | test_integral_* | 多項式、三角積分 |
| Series | test_geometric_series | 等比級數求和 |
| Continuity | test_is_continuous_* | 連續性判斷 |
| Differentiability | test_is_differentiable_* | 可導性判斷 |
| Sequence | test_sequence_* | 數列極限、單調性、有界性 |
| Taylor | test_taylor_sin | Taylor 展開近似 |
| Riemann | test_riemann_* | 黎曼和逼近 |
| Convergence | test_ratio_test, test_root_test | 級數收斂判別法 |
| ODE | test_euler_method, test_runge_kutta_4 | ODE 數值解 |

## 11. 測試覆蓋範圍

- **精確性測試**：驗證數值結果與解析解的誤差範圍
- **邊界情況**：如導數不存在的點（|x| 在 0 處）
- **收斂性驗證**：如調和級數發散 vs 等比級數收斂
- **數值穩定性**：不同步長對ODE方法的影響