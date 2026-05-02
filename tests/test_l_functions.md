# L-函數測試文檔

本文檔說明 `test_l_functions.py` 中測試用例的數學原理。

## 1. 測試驗證內容概述

L-函數是數論中一類重要的特殊函數，本測試套件驗證以下核心功能：

- **黎曼 zeta 函數**的計算與性質
- **狄利克雷 L-函數**的構造與性質
- **函數方程**的對稱性
- **解析延拓**的正確性
- **歐拉積**表示

---

## 2. 黎曼 zeta 函數測試 (Riemann Zeta)

### 測試用例

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_evaluate` | `RiemannZeta.evaluate(complex(2.0, 0.0))` |
| `test_trivial_zeros` | `RiemannZeta.trivial_zeros()` |
| `test_critical_line` | `RiemannZeta.critical_line()` |

### 數學原理

**定義（黎曼 zeta 函數）**

對於 Re(s) > 1，zeta 函數定義為：

$$\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s} = \prod_{p \text{ prime}} \frac{1}{1 - p^{-s}}$$

**平凡零點**

當 s = -2, -4, -6, ...（負偶數）時，zeta 函數的值為零，這些稱為**平凡零點**。

**臨界線**

黎曼猜想斷言：zeta 函數的所有非平凡零點都位於複平面上的直線 Re(s) = 1/2，稱為**臨界線**。

---

## 3. 狄利克雷 L-函數測試 (Dirichlet L-function)

### 測試用例

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 使用特徵 `chi = {1: 1.0, 3: -1.0}` 和模 4 創建 L-函數 |
| `test_evaluate` | 在 s = i（虛數單位）處求值 |
| `test_is_entire` | 判斷 L-函數是否為整函數 |

### 數學原理

**狄利克雷特徵**

狄利克雷特徵 $\chi$ 是定義在整數上的函數，滿足：
- $\chi(mn) = \chi(m)\chi(n)$
- 若 $\gcd(m, n) = 1$，則 $\chi(mn) = \chi(m)\chi(n)$
- 存在模 q，使得 $\chi(n + q) = \chi(n)$

**L-函數定義**

對於 Re(s) > 1：

$$L(s, \chi) = \sum_{n=1}^{\infty} \frac{\chi(n)}{n^s} = \prod_{p \text{ prime}} \frac{1}{1 - \chi(p)p^{-s}}$$

**示例中的特徵**

$\chi = \{1: 1.0, 3: -1.0\}$ 是模 4 的非主特徵：
- $\chi(1) = 1$
- $\chi(2) = 0$（未在字典中，通常意味著 0）
- $\chi(3) = -1$
- $\chi(4) = 0$

---

## 4. 函數方程測試 (Functional Equation)

### 測試用例

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_for_zeta` | `FunctionalEquation.for_zeta()` |
| `test_for_dirichlet` | `FunctionalEquation.for_dirichlet()` |

### 數學原理

**黎曼 zeta 函數的函數方程**

$$\zeta(s) = 2^s \pi^{s-1} \sin\left(\frac{\pi s}{2}\right) \Gamma(1-s) \zeta(1-s)$$

或等價形式：

$$\Xi(s) = \xi(1-s) \quad \text{其中} \quad \xi(s) = \frac{1}{2}s(s-1)\pi^{-s/2}\Gamma\left(\frac{s}{2}\right)\zeta(s)$$

**狄利克雷 L-函數的函數方程**

對於模 q 的原特徵 $\chi$：

$$L(s, \chi) = \epsilon(\chi) \cdot q^{1-s} \cdot \frac{\tau(\chi)}{i^q} \cdot L(1-s, \bar{\chi})$$

其中 $\tau(\chi)$ 是高斯和，$\epsilon(\chi)$ 是 eps 常數。

---

## 5. 解析延拓測試 (Analytic Continuation)

### 測試用例

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_continue_zeta` | `AnalyticContinuation.continue_zeta(i)` |
| `test_continue_dirichlet` | `AnalyticContinuation.continue_dirichlet(i, chi)` |

### 數學原理

解析延拓是將函數的定義域擴展到更大區域的過程。

**為何需要解析延拓**

- zeta 函數的級數定義 $\sum 1/n^s$ 只在 Re(s) > 1 收斂
- 通過解析延拓，可以將 zeta 函數擴展到整個複平面（除 s=1 外）
- s = 1 是唯一的一階極點（與素數倒數發散相關）

**反射公式**

利用函數方程和 Γ 函數的性質，可以將 zeta 延拓到 Re(s) ≤ 1 的區域。

---

## 6. 歐拉積測試 (Euler Product)

### 測試用例

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_for_zeta` | `EulerProduct.for_zeta(i)` |
| `test_for_dirichlet` | `EulerProduct.for_dirichlet(i, chi)` |

### 數學原理

**歐拉積表示**

對於 Re(s) > 1：

$$\zeta(s) = \prod_{p \text{ prime}} \frac{1}{1 - p^{-s}}$$

這個積公式展示了素數在解析數論中的核心地位。

**狄利克雷 L-函數的歐拉積**

$$L(s, \chi) = \prod_{p \text{ prime}} \frac{1}{1 - \chi(p)p^{-s}}$$

**收斂性**

- 在 Re(s) > 1 區域，歐拉積絕對收斂
- 對於 s = i（純虛數），歐拉積不收斂，但通過解析延拓可以得到有意義的值
- 這解釋了為何測試用例選擇 s = i 來驗證實現的穩健性

---

## 7. 測試設計原則

1. **類型安全**：所有測試首先驗證返回值的類型是 `complex`
2. **邊界條件**：測試涵蓋收斂邊界（Re(s) = 1）和臨界線（Re(s) = 1/2）
3. **穩健性**：使用虛數單位 i 作為輸入，確保實現能處理非實數輸入

---

## 8. 數學意義

L-函數研究是現代數論的核心：

- **黎曼猜想**：關於 zeta 函數零點分布的著名未解問題
- **狄利克雷定理**：算術級數中的素數分布
- **朗蘭茲綱領**：連接數論與表示理論的深層框架

這些測試確保 lean4py 庫中的 L-函數實現符合數學規範。