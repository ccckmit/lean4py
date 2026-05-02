# test_optimization_v18.py 測試文件說明

## 概述

本測試文件驗證 `lean4py.optimization` 模組中**牛頓-拉弗森法 (Newton-Raphson Method)** 和**萊文伯格-馬夸特法 (Levenberg-Marquardt Method)** 的正確性。

## 數學原理

### 牛頓-拉弗森法 (Newton-Raphson Method)

牛頓-拉弗森法是一種用於求解非線性方程 f(x) = 0 的迭代方法，也可用於無約束優化（求導數為零的點）。

**迭代公式：**
```
x_{n+1} = x_n - f(x_n) / f'(x_n)
```

對於優化問題（求極值），使用：
```
x_{n+1} = x_n - f'(x_n) / f''(x_n)
```

**收斂性：**
- 在單根附近具有二階收斂速度
- 對初始猜測值敏感
- 需要計算一階和二階導數

### 萊文伯格-馬夸特法 (Levenberg-Marquardt Method)

萊文伯格-馬夸特法是一種用於解決非線性最小二乘問題的迭代方法，結合了梯度下降法和高斯-牛頓法。

**問題形式：**
```
minimize Σ r_i(x)²
```

**迭代公式：**
```
x_{n+1} = x_n - (JᵀJ + λI)^{-1}Jᵀr
```

其中：
- J 是殘差函數的雅可比矩陣
- λ 是阻尼參數（λ → 0 趨近高斯-牛頓法，λ → ∞ 趨近梯度下降法）

**優點：**
- 自動調整步長，保證穩定性
- 適合病態條件數的問題

## 測試案例分析

### TestNewtonRaphson

#### 1. `test_1d_minimum`

**目標函數：** f(x) = (x - 2)²

這是一個簡單的二次函數，在 x = 2 處取得最小值 0。
牛頓法從初始點 x₀ = 0 迭代，應收斂到 x ≈ 2。

#### 2. `test_1d_convergence`

**目標函數：** f(x) = (x - 3)²

驗證牛頓法的收斂性：最終函數值應小於初始函數值。

### TestLevenbergMarquardt

#### 1. `test_simple_regression`

**殘差函數：** r(params) = params[0] × 1.0 - 1.0

這等價於線性擬合問題 y = ax，目標是找到 a 使得 a × 1 ≈ 1，即 a ≈ 1。

#### 2. `test_residual_reduction`

同樣的殘差函數，驗證 LM 法能夠降低殘差平方和。

## 測試環境

- 模組：`lean4py.optimization`
- 函數：`newton_raphson`, `levenberg_marquardt`
- 測試框架：pytest