# test_optimization_v14.py 測試文件說明

## 概述

本測試文件驗證 `lean4py.optimization` 模組中**增廣拉格朗日法 (Augmented Lagrange Method)** 的正確性。

## 數學原理

### 增廣拉格朗日法 (Augmented Lagrange Method)

增廣拉格朗日法是一種用於求解帶約束優化問題的迭代方法。對於如下約束優化問題：

```
minimize f(x)
subject to: g(x) = 0 (等式約束)
            h(x) ≤ 0 (不等式約束)
```

增廣拉格朗日函數定義為：

```
L_ρ(x, λ, μ) = f(x) + λᵀg(x) + (ρ/2)‖g(x)‖² + 不等式約束項
```

其中：
- λ 是拉格朗日乘子向量
- ρ > 0 是懲罰參數
- 通過交替更新原始變數 x 和乘子，實現收斂

### 測試案例分析

#### 1. `test_minimize_x2_y2`

**問題：**
```
minimize x² + y²
subject to x + y = 1
```

**解析解：**
由拉格朗日乘數法：
- ∇(x² + y²) = λ∇(x + y - 1)
- 2x = λ, 2y = λ ⇒ x = y
- 代入約束：2x = 1 ⇒ x = y = 0.5
- 最小值：f(0.5, 0.5) = 0.25 + 0.25 = 0.5

測試驗證優化結果滿足約束且目標值接近理論最小值 0.5。

#### 2. `test_minimize_xy`

**問題：**
```
minimize xy
subject to x + y = 10
```

**解析解：**
由約束條件 y = 10 - x，代入目標函數：
- f(x) = x(10 - x) = 10x - x²
- df/dx = 10 - 2x = 0 ⇒ x = 5, y = 5
- 最小值：f(5, 5) = 25

測試驗證 x + y ≈ 10 的約束條件。

## 測試環境

- 模組：`lean4py.optimization`
- 函數：`augmented_lagrange`
- 測試框架：pytest