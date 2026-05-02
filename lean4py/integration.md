# 積分理論模組 (integration.py)

## 模組概述

本模組提供積分理論的核心功能，連接測度論模組 (`measure_theory.py`)，模擬 mathlib4 的 `Mathlib.MeasureTheory.Integral` 設計。包含黎曼積分、勒貝格積分、重積分、變數變換及各類積分不等式。

---

## 1. 黎曼積分 (Riemann Integration)

### 1.1 基本概念

**分割 (Partition)**: 區間 $[a,b]$ 的分割是指一組點 $P = \{x_0, x_1, \ldots, x_n\}$，其中
$$a = x_0 < x_1 < x_2 < \cdots < x_n = b$$

### 1.2 黎曼和 (Riemann Sum)

對於有界函數 $f: [a,b] \to \mathbb{R}$，給定分割 $P$ 和取樣點 $\xi_i \in [x_{i-1}, x_i]$，黎曼和定義為：
$$R(f, P, \xi) = \sum_{i=1}^{n} f(\xi_i) \Delta x_i$$
其中 $\Delta x_i = x_i - x_{i-1}$。

### 1.3 可積條件

函數 $f$ 在 $[a,b]$ 上黎曼可積當且僅當：
- $f$ 有界
- $f$ 的不連續點集合測度為零（迪尼性質）

---

## 2. 勒貝格積分理論 (Lebesgue Integration)

### 2.1 博赫納積分 (Bochner Integral)

**定義**: 設 $f: X \to B$（$B$ 為巴拿赫空間），若存在一列簡單函數 $s_n$ 使得：
$$\|f(x) - s_n(x)\|_B \to 0 \quad \text{當 } n \to \infty \text{ 對幾乎處處 } x$$

則博赫納積分定義為：
$$\int_X f \, d\mu = \lim_{n \to \infty} \int_X s_n \, d\mu$$

### 2.2 線性性質驗證

模組中 `BochnerIntegral.is_linear()` 驗證：
$$\int (af + bg) = a\int f + b\int g$$

---

## 3. 瑕積分 (Improper Integrals)

### 3.1 定義

當積分區間無界或被積函數有無界點時，稱為瑕積分。

**第一類瑕積分**（無界區間）：
$$\int_a^\infty f(x) \, dx = \lim_{b \to \infty} \int_a^b f(x) \, dx$$

**第二類瑕積分**（無界函數）：
$$\int_a^b f(x) \, dx = \lim_{\varepsilon \to 0^+} \int_a^{b-\varepsilon} f(x) \, dx$$

### 3.2 收斂判別法

- **比較判別法**: 若 $0 \leq f(x) \leq g(x)$ 且 $\int g$ 收斂，則 $\int f$ 收斂
- **絕對收斂**: $\int |f|$ 收斂則 $\int f$ 收斂

---

## 4. 重積分與富比尼定理 (Multiple Integrals & Fubini's Theorem)

### 4.1 富比尼定理 (Fubini's Theorem)

設 $f: X \times Y \to \mathbb{R}$ 為可測函數，若：
$$\int_{X \times Y} |f(x,y)| \, d(x,y) < \infty$$

則：
$$\int_{X \times Y} f(x,y) \, d(x,y) = \int_X \left( \int_Y f(x,y) \, dy \right) dx = \int_Y \left( \int_X f(x,y) \, dx \right) dy$$

### 4.2 迭代積分

模組中 `FubiniTheorem.iterated_integral()` 計算：
$$\iint f(x,y) \, dx \, dy = \sum_{x \in X} \sum_{y \in Y} f(x,y)$$

---

## 5. 變數變換公式 (Change of Variables)

### 5.1 換元公式

設 $\varphi: [a,b] \to \mathbb{R}$ 為光滑雙射，則：
$$\int_a^b f(\varphi(t)) |\varphi'(t)| \, dt = \int_{\varphi(a)}^{\varphi(b)} f(x) \, dx$$

### 5.2 雅可比行列式

在多變數情況下，變換 $x = \varphi(u)$ 的雅可比行列式 $J_\varphi(u)$ 滿足：
$$\int_{\varphi(\Omega)} f(x) \, dx = \int_\Omega f(\varphi(u)) |J_\varphi(u)| \, du$$

模組中 `ChangeOfVariables.change_of_variables()` 實現此公式的中點近似。

---

## 6. 曲線積分 (Line Integrals)

### 6.1 第一類曲線積分（數量場）

沿曲線 $C$ 的積分：
$$\int_C f(x,y,z) \, ds = \int_a^b f(x(t), y(t), z(t)) \sqrt{(x')^2 + (y')^2 + (z')^2} \, dt$$

### 6.2 第二類曲線積分（向量場）

沿有向曲線 $C$ 的功：
$$\int_C \mathbf{F} \cdot d\mathbf{r} = \int_a^b \mathbf{F}(\mathbf{r}(t)) \cdot \mathbf{r}'(t) \, dt$$

---

## 7. 曲面積分 (Surface Integrals)

### 7.1 第一類曲面積分

設曲面 $S$ 由參數 $\mathbf{r}(u,v)$ 給定：
$$\iint_S f(x,y,z) \, dS = \iint_D f(\mathbf{r}(u,v)) \|\mathbf{r}_u \times \mathbf{r}_v\| \, du \, dv$$

### 7.2 第二類曲面積分（通量）

$$\iint_S \mathbf{F} \cdot \mathbf{n} \, dS = \iint_D \mathbf{F} \cdot (\mathbf{r}_u \times \mathbf{r}_v) \, du \, dv$$

---

## 8. 積分不等式 (Integral Inequalities)

### 8.1 柯西-施瓦茨不等式 (Cauchy-Schwarz Inequality)

對於 $f, g \in L^2$：
$$\left| \int f(x) g(x) \, dx \right| \leq \left( \int |f|^2 \, dx \right)^{1/2} \left( \int |g|^2 \, dx \right)^{1/2}$$

等號成立當且僅當 $f$ 與 $g$ 線性相關。

### 8.2 赫爾德不等式 (Hölder Inequality)

設 $1 < p, q < \infty$ 且 $\frac{1}{p} + \frac{1}{q} = 1$，則：
$$\|fg\|_1 \leq \|f\|_p \|g\|_q$$

模組中 `HolderInequality.holder_holds()` 驗證此不等式。

### 8.3 明可夫斯基不等式 (Minkowski Inequality)

對於 $1 \leq p \leq \infty$：
$$\|f + g\|_p \leq \|f\|_p + \|g\|_p$$

此不等式保證 $L^p$ 空間的三角不等式，模組中 `MinkowskiInequality.minkowski_holds()` 實現驗證。

---

## 9. L^p 空間

### 9.1 定義

$L^p$ 空間由滿足下式的可測函數組成：
$$\|f\|_p = \left( \int |f|^p \, d\mu \right)^{1/p} < \infty$$

模組中 `LpSpace.norm()` 計算此範數。

### 9.2 巴拿赫空間性質

當 $1 \leq p \leq \infty$ 時，$L^p$ 為巴拿赫空間。`LpSpace.is_banach()` 驗證此性質。

---

## 10. 卷積 (Convolution)

### 10.1 定義

$$(f * g)(x) = \int_{\mathbb{R}^n} f(t) g(x-t) \, dt$$

模組中 `Convolution.convolve()` 使用數值近似計算卷積。

### 10.2 交換性

卷積運算滿足交換律：$f * g = g * f$。`Convolution.is_commutative()` 驗證此性質。

---

## 類別對照表

| 類別 | 功能 | 數學理論 |
|------|------|----------|
| `BochnerIntegral` | 向量值函數積分 | 博赫納積分 |
| `FubiniTheorem` | 重積分計算 | 富比尼定理 |
| `ChangeOfVariables` | 換元法 | 變數變換 |
| `Convolution` | 卷積運算 | 卷積理論 |
| `LpSpace` | $L^p$ 範數空間 | 泛函分析 |
| `HolderInequality` | Hölder 不等式 | 積分不等式 |
| `MinkowskiInequality` | Minkowski 不等式 | 積分不等式 |

---

## 參考文獻

1. Rudin, W. *Real and Complex Analysis*
2. Folland, G. B. *Real Analysis: Modern Techniques and Applications*
3. Stein, E. M. *Real Analysis: Measure Theory, Integration, & Hilbert Spaces*
4. mathlib4 Measure Theory Module