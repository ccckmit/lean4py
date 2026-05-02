# 數值方法測試文檔 (test_numerical_methods.py)

## 1. 測試驗證概述

本測試文件針對 `lean4py.numerical_methods` 模組進行驗證，涵蓋：
- 方程求根方法（牛頓法、割線法、二分法、不動點迭代）
- 多項式插值（拉格朗日插值、牛頓插值）
- 數值積分（高斯積分、辛普森積分、龍格庫塔積分）

## 2. 方程求根測試

### 2.1 牛頓-拉弗森法 (Newton-Raphson)

**數學原理：**
牛頓法的迭代公式為：
$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

該方法在初始猜測值靠近真實根且導數非零時，收斂速度為二次收斂。

**測試內容：**
- `test_find_root`: 驗證 $f(x) = x^2 - 2$ 在 $x_0 = 1$ 處收斂到 $\sqrt{2} \approx 1.41421356$，精度要求 $10^{-6}$
- `test_find_root_no_convergence`: 驗證 $f(x) = x^3 - x + 2$ 在有限迭代次數內不收斂時返回 `conv = False`
- `test_find_all_roots_simple`: 驗證區間搜索功能可找到多個根

### 2.2 割線法 (Secant Method)

**數學原理：**
割線法使用兩個初始點，通過割線斜率逼近導數：
$$x_{n+1} = x_n - f(x_n) \cdot \frac{x_n - x_{n-1}}{f(x_n) - f(x_{n-1})}$$

相比牛頓法，無需計算導數，但收斂速度較慢（約黃金比例）。

**測試內容：**
- `test_find_root`: 驗證 $f(x) = x^2 - 2$ 在區間 $[1, 2]$ 內求根，精度要求 $10^{-4}$

### 2.3 二分法 (Bisection Method)

**數學原理：**
若 $f(a) \cdot f(b) < 0$，則區間 $[a,b]$ 內必有根。每次取中點 $c = \frac{a+b}{2}$，根據符號將區間縮小一半。

**收斂性：**
二分法保證收斂，收斂速度為線性：
$$\text{誤差} \leq \frac{b-a}{2^n}$$

**測試內容：**
- `test_find_root`: 驗證 $f(x) = x^2 - 2$ 在區間 $[0, 2]$ 內求根，精度要求 $10^{-8}$

### 2.4 不動點迭代 (Fixed Point Iteration)

**數學原理：**
將方程 $f(x) = 0$ 改寫為 $x = g(x)$，迭代公式為：
$$x_{n+1} = g(x_n)$$

**收斂條件（巴拿赫不動點定理）：**
若 $|g'(x)| < 1$ 在區間內成立，則迭代收斂。

**測試內容：**
- `test_find_fixed_point`: 驗證 $g(x) = x/2 + 1$ 的不動點為 $x = 2$
- `test_has_convergence_guarantee`: 驗證收斂性判斷方法

## 3. 數值積分測試

### 3.1 高斯-勒讓德積分 (Gaussian Quadrature)

**數學原理：**
高斯積分使用勒讓德多項式的根作為節點，在這些節點上對函數值加權求和：

$$\int_{-1}^{1} f(x) dx \approx \sum_{i=1}^{n} w_i f(x_i)$$

其中 $x_i$ 為 $n$ 階勒讓德多項式的根，$w_i$ 為對應權重。對於 $n$ 個節點，高斯積分可精確積分最高 $2n-1$ 次多項式。

**勒讓德多項式遞推關係：**
$$P_0(x) = 1, \quad P_1(x) = x$$
$$(n+1)P_{n+1}(x) = (2n+1)xP_n(x) - nP_{n-1}(x)$$

**測試內容：**
- `test_legendre_polynomial_n0/n1/n2`: 驗證勒讓德多項式計算（$P_0(0.5)=1$, $P_1(0.5)=0.5$, $P_2(0.5)=-0.125$）
- `test_gauss_legendre_nodes_weights`: 驗證 $n=3$ 時節點和權重的數量
- `test_integrate`: 驗證 $\int_0^1 x^2 dx = \frac{1}{3}$，精度要求 $10^{-4}$

### 3.2 辛普森積分 (Simpson's Rule)

**數學原理：**
辛普森規則使用拋物線逼近函數。對於等距分割的區間 $[a,b]$（分割為偶數 $n$ 個子區間）：
$$\int_a^b f(x) dx \approx \frac{h}{3} \left[ f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + \cdots + 4f(x_{n-1}) + f(x_n) \right]$$
其中 $h = \frac{b-a}{n}$。

**誤差：**
若 $f^{(4)}$ 連續，誤差與 $h^4$ 成正比。

**測試內容：**
- `test_integrate`: 驗證 $\int_0^1 x^2 dx = \frac{1}{3}$，使用 $n=100$ 個子區間，精度要求 $10^{-4}$

### 3.3 龍格庫塔積分 (Romberg Integration)

**數學原理：**
龍格庫塔積分是二分法的推廣，通過外推技術加速收斂。定義 $R_{k,1}$ 為將區間等分 $2^{k-1}$ 份後的梯形法則結果，則：
$$R_{k,m} = R_{k,m-1} + \frac{R_{k,m-1} - R_{k-1,m-1}}{4^{m-1} - 1}$$

該公式基於誤差展開式的外推，可將低階方法的結果提升到高階精度。

**測試內容：**
- `test_integrate`: 驗證 $\int_0^1 x dx = \frac{1}{2}$，最大迭代次數為 5，精度要求 $10^{-1}$

## 4. 多項式插值測試

### 4.1 拉格朗日插值 (Lagrange Interpolation)

**數學原理：**
對於 $n$ 個數據點 $(x_0, y_0), (x_1, y_1), \ldots, (x_{n-1}, y_{n-1})$，拉格朗日插值多項式為：
$$L(x) = \sum_{i=0}^{n-1} y_i \cdot \ell_i(x)$$
其中基函數為：
$$\ell_i(x) = \prod_{\substack{0 \leq j \leq n-1 \\ j \neq i}} \frac{x - x_j}{x_i - x_j}$$

**測試內容：**
- `test_creation`: 驗證插值對象正確初始化（$n=3$）
- `test_evaluate`: 驗證插值計算返回浮點數
- `test_coefficients`: 驗證返回多項式系數個數正確

### 4.2 牛頓插值 (Newton Interpolation)

**數學原理：**
牛頓插值使用牛頓基函數和有限差分：
$$N(x) = a_0 + a_1(x-x_0) + a_2(x-x_0)(x-x_1) + \cdots + a_{n-1}(x-x_0)\cdots(x-x_{n-2})$$

其中係數 $a_i$ 為**牛頓除差**（有限差商）。

**除差定義：**
$$f[x_i] = y_i$$
$$f[x_i, x_{i+1}] = \frac{f[x_{i+1}] - f[x_i]}{x_{i+1} - x_i}$$
$$f[x_i, x_{i+1}, x_{i+2}] = \frac{f[x_{i+1}, x_{i+2}] - f[x_i, x_{i+1}]}{x_{i+2} - x_i}$$

**測試內容：**
- `test_creation`: 驗證插值對象正確初始化（$n=3$）
- `test_evaluate`: 驗證插值計算返回浮點數
- `test_divided_diffs`: 驗證除差個數等於數據點個數

## 5. 測試覆蓋說明

本測試文件**不包含**以下內容的測試：
- 數值微分（Numerical Differentiation）
- 矩陣分解（Matrix Decomposition，如 LU 分解、QR 分解、奇異值分解）

這些主題可能在其他測試文件中覆蓋，或作為 `numerical_methods` 模組的未來擴展功能。

## 6. 測試驗證策略

| 方法類別 | 測試策略 |
|---------|---------|
| 求根方法 | 驗證收斂性、精度、收斂標誌 |
| 插值方法 | 驗證返回值類型、系數個數、除差個數 |
| 數值積分 | 驗證與解析解的誤差範圍 |
| 特殊多項式 | 驗證已知點上的函數值 |

## 7. 版本信息

- **模組版本**: v1.19
- **測試文件**: `tests/test_numerical_methods.py`