# 符號計算測試文檔 (test_symbolic.py)

## 概述

本測試文件驗證 `lean4py/symbolic.py` 模塊中的符號計算功能，依賴 SymPy 庫進行代數運算。

## 測試結構

| 測試類別 | 測試數量 | 核心功能 |
|----------|----------|----------|
| `TestSymbolicDerivative` | 4 | 符號微分 |
| `TestSymbolicIntegral` | 3 | 符號積分 |
| `TestSymbolicSimplify` | 2 | 符號簡化 |

---

## 1. 表達式創建測試

本模塊通過字符串形式接收數學表達式，內部使用 `sympy.sympify()` 將字符串轉換為 SymPy 符號對象。

```python
expr = sp.sympify(expr_str)  # "x**2" → x²
```

---

## 2. 簡化測試 (TestSymbolicSimplify)

### 測試用例

| 測試方法 | 輸入表達式 | 預期結果 |
|----------|------------|----------|
| `test_combine_like_terms` | `x**2 + 2*x**2 + 3*x` | 合併同類項後包含 `3*x` |
| `test_cancel_terms` | `x + x**2 - x` | 消除後結果包含 `x**2` |

### 數學原理

**同類項合併**：代數運算中，指數相同的項可以合併系數。
- $x^2 + 2x^2 = 3x^2$

**項消除**：加減運算中，互為相反數的項可以相互抵消。
- $x + x^2 - x = x^2$

SymPy 的 `simplify()` 函數會自動應用這些代數規則。

---

## 3. 微分測試 (TestSymbolicDerivative)

### 測試用例

| 測試方法 | 輸入 | 預期結果 | 數學原理 |
|----------|------|----------|----------|
| `test_power_rule` | `x**2` | `2*x` | 冪函數求導法則：$\frac{d}{dx}x^n = nx^{n-1}$ |
| `test_linear` | `3*x + 5` | 系數 `3` | 常數乘法與加法法則 |
| `test_constant` | `42` | `0` | 常數導數為零 |
| `test_sin` | `sin(x)` | 包含 `cos` | 三角函數導數：$\frac{d}{dx}\sin x = \cos x$ |

### 核心微分法則

| 法則 | 表達式 | 導數 |
|------|--------|------|
| 冪法則 | $x^n$ | $nx^{n-1}$ |
| 常數乘法 | $cf(x)$ | $cf'(x)$ |
| 加法法則 | $f(x) + g(x)$ | $f'(x) + g'(x)$ |
| 常數 | $c$ | $0$ |

---

## 4. 積分測試 (TestSymbolicIntegral)

### 測試用例

| 測試方法 | 輸入 | 預期結果 | 數學原理 |
|----------|------|----------|----------|
| `test_power_rule` | `x**2` | `x**3/3` 或 `x**3/3 + C` | 冪函數積分：$\int x^n dx = \frac{x^{n+1}}{n+1} + C$ |
| `test_linear` | `3*x` | `3*x**2/2` 或 `1.5*x**2` | 積分乘法法則 |
| `test_constant` | `5` | `5*x` | 常數積分：$\int c dx = cx + C$ |

### 核心積分法則

| 法則 | 表達式 | 積分結果 |
|------|--------|----------|
| 冪法則 | $x^n$ (n≠-1) | $\frac{x^{n+1}}{n+1} + C$ |
| 常數乘法 | $cf(x)$ | $c\int f(x)dx$ |
| 加法法則 | $f(x) + g(x)$ | $\int f(x)dx + \int g(x)dx$ |
| 常數積分 | $c$ | $cx + C$ |

---

## 5. 方程求解測試

**注意**：當前測試文件中未包含方程求解測試。若需此功能，可擴展以下方法：

```python
# 潛在的方程求解接口
def symbolic_solve(expr_str: str, var: str = 'x') -> str:
    """求解代數方程 expr = 0"""
    x = sp.symbols(var)
    expr = sp.sympify(expr_str)
    solutions = sp.solve(expr, x)
    return str(solutions)
```

### 典型方程求解測試示例

| 方程 | 求解結果 |
|------|----------|
| $x^2 - 4 = 0$ | $x = \pm 2$ |
| $2x + 3 = 0$ | $x = -\frac{3}{2}$ |

---

## 依賴說明

所有符號計算功能依賴 `sympy` 庫。若未安裝，測試會自動跳過（使用 `pytest.skip`）。

```bash
pip install sympy
```

---

## 測試運行

```bash
pytest tests/test_symbolic.py -v
```