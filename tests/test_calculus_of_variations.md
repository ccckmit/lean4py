# 變分法測試文檔

本文件說明 `test_calculus_of_variations.py` 中測試用例所驗證的數學原理。

## 概述

變分法（Calculus of Variations）是處理泛函極值問題的數學分支。**泛函**是將函數映射到實數的映射，類似於函數將變量映射到實數。變分法的核心問題是找到使泛函取得極值的函數。

---

## 1. 泛函測試 (TestFunctional)

### 測試內容
- `test_creation`: 驗證 `Functional` 類的創建
- `test_evaluate`: 驗證泛函的計算

### 數學原理

泛函的一般形式為：

$$J[y] = \int_{t_0}^{t_1} L(t, y(t), y'(t)) \, dt$$

其中 $L$ 是**拉格朗日函數**（Lagrangian），依賴於：
- $t$: 獨立變量（通常是時間）
- $y(t)$: 未知函數
- $y'(t) = \frac{dy}{dt}$: 未知函數的導數

測試中使用的拉格朗日函數 $L = y^2 + (y')^2$ 或 $L = (y')^2$。

---

## 2. 歐拉-拉格朗日方程測試 (TestEulerLagrangeEquation)

### 測試內容
- `test_euler_lagrange`: 驗證歐拉-拉格朗日方程的計算
- `test_is_extremal`: 驗證函數是否為極值函數

### 數學原理

**歐拉-拉格朗日方程**是泛函極值的**必要條件**：

$$\frac{d}{dt}\left( \frac{\partial L}{\partial y'} \right) - \frac{\partial L}{\partial y} = 0$$

展開後：

$$\frac{\partial L}{\partial y} - \frac{d}{dt}\left( \frac{\partial L}{\partial y'} \right) = 0$$

對於簡單的拉格朗日函數 $L = (y')^2$：
- $\frac{\partial L}{\partial y} = 0$
- $\frac{\partial L}{\partial y'} = 2y'$
- $\frac{d}{dt}\left( \frac{\partial L}{\partial y'} \right) = 2y''$

因此方程化簡為 $y'' = 0$，其解為線性函數 $y(t) = at + b$。

---

## 3. 哈密頓原理測試 (TestHamiltonPrinciple)

### 測試內容
- `test_action`: 驗證作用量（Action）的計算
- `test_is_stationary`: 驗證作用量是否為平穩值

### 數學原理

**哈密頓原理**（Hamilton's Principle）指出：自然系統的實際運動軌跡使作用量

$$S[y] = \int_{t_0}^{t_1} L(t, y, y') \, dt$$

取得**平穩值**（ stationary value，極值或鞍點）。

當 $L = (y')^2$ 時，對於直線運動 $y(t) = t$：
- $y' = 1$
- $S = \int_0^1 1^2 \, dt = 1$

這與測試中 `assert action >= 0` 一致。

---

## 4. 最速降線問題測試 (TestBrachistochrone)

### 測試內容
- `test_time_of_descent`: 驗證下降時間的計算
- `test_cycloid_solution`: 驗證擺線解

### 數學原理

**最速降線問題**（Brachistochrone Problem）：找到連接兩點 $A$ 和 $B$的曲線，使質點在重力作用下從 $A$ 滑到 $B$ 的時間最短。

擺線（Cycloid）是這個問題的解：

$$x = a(\theta - \sin\theta)$$
$$y = a(1 - \cos\theta)$$

其中 $a$ 是生成圓的半徑參數。

---

## 5. 等周問題測試 (TestIsoperimetricProblem)

### 測試內容
- `test_creation`: 驗證等周問題類的創建
- `test_solve_with_lagrange`: 驗證使用拉格朗日乘數法求解

### 數學原理

**等周問題**：在所有周長固定的閉曲線中，找到面積最大的曲線（答案是圓）。

這是**約束優化問題**，使用**拉格朗日乘數法**求解。構造增廣泛函：

$$\mathcal{L}[y, \lambda] = J[y] + \lambda (G[y] - C)$$

其中：
- $J[y]$ 是待優化的泛函
- $G[y] = C$ 是約束條件
- $\lambda$ 是拉格朗日乘數

---

## 6. 諾特定理測試 (TestNoetherTheorem)

### 測試內容
- `test_has_symmetry`: 驗證拉格朗日函數的對稱性
- `test_conserved_quantity`: 驗證守恒量的計算

### 數學原理

**諾特定理**（Noether's Theorem）：每一個連續對稱性都對應一個守恒定律。

- **時間平移對稱性** → 能量守恒
- **空間平移對稱性** → 動量守恒
- **旋轉對稱性** → 角動量守恒

對於平移對稱性 $y \to y + \epsilon$，守恒量為：

$$Q = \frac{\partial L}{\partial y'} \cdot \frac{dy}{d\epsilon} = \frac{\partial L}{\partial y'}$$

當 $L = (y')^2$ 時，$\frac{\partial L}{\partial y'} = 2y'$，這就是**廣義動量**。

---

## 7. 勒讓德條件測試 (TestLegendreCondition) - 當前測試套件中未包含

### 數學原理

**勒讓德條件**（Legendre Condition）是變分問題的**二階必要條件**，用於判斷極值是極小值還是極大值：

$$\frac{\partial^2 L}{\partial (y')^2} \geq 0 \quad \text{（極小值）}$$

或

$$\frac{\partial^2 L}{\partial (y')^2} \leq 0 \quad \text{（極大值）}$$

對於 $L = (y')^2$：
$$\frac{\partial^2 L}{\partial (y')^2} = 2 > 0$$

這表明直線是**極小值**解。

**強勒讓德條件**要求 $\frac{\partial^2 L}{\partial (y')^2} > 0$（嚴格不等於零）。

### 當前測試狀態

測試套件 `test_calculus_of_variations.py` 目前**未包含**勒讓德條件的專門測試。這是變分法測試的一個擴展方向。

---

## 測試套件結構

| 測試類 | 測試方法 | 驗證內容 |
|--------|----------|----------|
| `TestFunctional` | `test_creation`, `test_evaluate` | 泛函的基本操作 |
| `TestEulerLagrangeEquation` | `test_euler_lagrange`, `test_is_extremal` | 歐拉-拉格朗日方程 |
| `TestHamiltonPrinciple` | `test_action`, `test_is_stationary` | 哈密頓原理 |
| `TestBrachistochrone` | `test_time_of_descent`, `test_cycloid_solution` | 最速降線問題 |
| `TestIsoperimetricProblem` | `test_creation`, `test_solve_with_lagrange` | 等周問題 |
| `TestNoetherTheorem` | `test_has_symmetry`, `test_conserved_quantity` | 諾特定理 |
| `TestLegendreCondition` | （未實現） | 勒讓德條件 |

---

## 核心公式總結

| 名稱 | 公式 |
|------|------|
| 泛函 | $J[y] = \int_{t_0}^{t_1} L(t, y, y') \, dt$ |
| 歐拉-拉格朗日方程 | $\frac{\partial L}{\partial y} - \frac{d}{dt}\left( \frac{\partial L}{\partial y'} \right) = 0$ |
| 哈密頓作用量 | $S = \int_{t_0}^{t_1} L \, dt$ |
| 擺線參數方程 | $x = a(\theta - \sin\theta)$, $y = a(1 - \cos\theta)$ |
| 勒讓德條件 | $\frac{\partial^2 L}{\partial (y')^2} \geq 0$（極小值）|