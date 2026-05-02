# 優化測試文檔

本文檔說明 `tests/test_optimization.py` 中測試用例的數學原理。

## 1. 測試概述

本模組測試 `lean4py.optimization` 中的優化演算法，包括：

- **梯度下降法** (Gradient Descent)：一階優化方法
- **線性規劃** (Linear Programming)：使用 scipy 求解器

## 2. 梯度下降法測試

### 2.1 數學原理

梯度下降法是求解無約束優化問題的基本方法。對於目標函數 $f(x)$，演算法沿著梯度的負方向迭代：

$$x_{k+1} = x_k - \alpha \nabla f(x_k)$$

其中 $\alpha$ 為學習率（learning rate），控制步長大小。

本模組使用數值微分計算梯度：
$$\nabla f(x) \approx \frac{f(x+h) - f(x-h)}{2h}$$

### 2.2 測試用例分析

#### `test_minimize_x_squared`

測試函數：$f(x) = x^2$

- **理論最優解**：$x^* = 0$，$f(x^*) = 0$
- **初始點**：$x_0 = 5.0$
- **學習率**：$\alpha = 0.1$
- **收斂條件**：$|x_{opt}| < 0.1$ 且 $f(x_{opt}) < 0.01$

這是最簡單的凸優化問題，二次函數圖像為拋物線，梯度為 $\nabla f(x) = 2x$。

#### `test_minimize_quadratic`

測試函數：$f(x) = (x-3)^2 + 2$

- **理論最優解**：$x^* = 3$，$f(x^*) = 2$
- **初始點**：$x_0 = 0.0$
- **驗證**：$|x_{opt} - 3.0| < 0.1$ 且 $|f(x_{opt}) - 2.0| < 0.1$

此測試檢驗演算法能否正確找到偏離原點的最優解。

#### `test_convergence_tol`

測試收斂容忍度機制：

- **函數**：$f(x) = x^2$
- **初始點**：$x_0 = 10.0$
- **容忍度**：$tol = 10^{-3}$
- **驗證**：當 $|x_{new} - x| < tol$ 時停止迭代

## 3. 牛頓法測試說明

當前 `test_optimization.py` 中**未包含牛頓法測試**。

牛頓法的數學原理如下：

$$x_{k+1} = x_k - \frac{f'(x_k)}{f''(x_k)}$$

牛頓法使用二階資訊（赫斯矩陣），收斂速度比梯度下降法快，但需要計算二階導數。相關實作可見 `optimization.py` 中的 `newton_method` 函數。

## 4. 凸優化測試

### 4.1 凸優化基本概念

凸優化問題具有以下特性：
- 目標函數為凸函數
- 可行域為凸集合
- 任何局部最優解即為全域最優解

上述測試中使用的二次函數 $f(x) = x^2$ 和 $f(x) = (x-3)^2 + 2$ 均為嚴格凸函數。

### 4.2 線性規劃測試

#### `test_simple_lp`

**數學形式**：
$$\min_{x,y} \quad x + y$$
$$\text{s.t.} \quad x + y \geq 1$$
$$\quad x \geq 0, \quad y \geq 0$$

轉換為標準形 $Ax \leq b$：
- $c = [1, 1]$
- $A = [[-1, -1]]$，$b = [-1]$
- 即 $-x - y \leq -1$

**理論最優解**：$x = y = 0.5$，目標值 $= 1.0$

#### `test_lp_infeasible`

測試不可行情況：
$$\text{s.t.} \quad x \geq 2 \quad \Rightarrow \quad x \leq 1$$
$$x \leq 1 \quad \Rightarrow \quad -x \leq -2$$

約束條件相互矛盾，應返回 `None`。

## 5. 測試函數對應關係

| 測試函數 | 測試目標 | 優化方法 |
|---------|---------|---------|
| `test_minimize_x_squared` | 基本二次函數最小化 | 梯度下降 |
| `test_minimize_quadratic` | 偏移二次函數最小化 | 梯度下降 |
| `test_convergence_tol` | 收斂容忍度機制 | 梯度下降 |
| `test_simple_lp` | 簡單線性規劃 | 單形法/內點法 |
| `test_lp_infeasible` | 不可行問題檢測 | 單形法 |

## 6. 相關參考

- 梯度下降法：`lean4py.optimization.gradient_descent`
- 牛頓法：`lean4py.optimization.newton_method`
- 線性規劃：`lean4py.optimization.linear_programming`
- 其他優化方法：共軛梯度法、BFGS、L-BFGS、蘭格朗日乘數法等