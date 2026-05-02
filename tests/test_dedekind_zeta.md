# Dedekind Zeta 函數測試文檔

## 概述

本文檔說明 `test_dedekind_zeta.py` 中的測試案例所驗證的數學原理。Dedekind zeta 函數是代數數論中的核心研究對象，推廣了黎曼 zeta 函數到任意代數數域。

---

## 1. Dedekind Zeta 函數測試

### 測試內容

| 測試方法 | 驗證目標 |
|----------|----------|
| `test_creation` | 創建 `DedekindZetaFunction("Q")` 實例 |
| `test_evaluate` | 對複變量 `s` 進行求值 |
| `test_euler_product` | 計算 Euler 積展開 |

### 數學原理

Dedekind zeta 函數定義為：

$$\zeta_K(s) = \sum_{I \subset \mathcal{O}_K} N(I)^{-s}$$

其中：
- $K$ 為代數數域
- $I$ 遍歷 $\mathcal{O}_K$ 的所有非零理想
- $N(I) = |\mathcal{O}_K / I|$ 為理想的範數

對於有理數域 $K = \mathbb{Q}$，Dedekind zeta 函數退化為黎曼 zeta 函數：

$$\zeta_{\mathbb{Q}}(s) = \zeta(s) = \sum_{n=1}^{\infty} n^{-s}$$

---

## 2. Zeta 函數測試

### 測試內容

| 測試方法 | 驗證目標 |
|----------|----------|
| `test_for_dedekind` | 計算指定數域的 Euler 積 |
| `test_converges_for` | 判斷複變量是否在收斂域內 |

### 數學原理

Euler 積展開是 Dedekind zeta 函數的核心表示：

$$\zeta_K(s) = \prod_{\mathfrak{P}} \left(1 - N(\mathfrak{P})^{-s}\right)^{-1}$$

其中 $\mathfrak{P}$ 遍歷數域 $K$ 的所有非零素理想。

**收斂性**：Euler 積在 $\text{Re}(s) > 1$ 時絕對收斂，這是因為素理想的分佈遵循有效的漸近估計。

---

## 3. 類數公式測試

### 測試內容

| 測試方法 | 驗證目標 |
|----------|----------|
| `test_formula` | 計算解析類數公式的各分量 |
| `test_holds` | 驗證類數公式是否成立 |

### 數學原理

解析類數公式建立了 zeta 函數在 $s=1$ 處的留數與數域不變量之間的關係：

$$\lim_{s \to 1} (s-1)\zeta_K(s) = \frac{2^{r_1}(2\pi)^{r_2} h_K R_K}{w_K \sqrt{|d_K|}}$$

其中：
| 符號 | 含義 |
|------|------|
| $h_K$ | 類數 |
| $R_K$ |  регулятор |
| $d_K$ | 判別式 |
| $w_K$ | 單位根個數 |
| $r_1$ | 實嵌入個數 |
| $r_2$ | 複嵌入個數 |

對於有理數域 $\mathbb{Q}$：
- $r_1 = 1, r_2 = 0$
- $h_{\mathbb{Q}} = 1$
- $R_{\mathbb{Q}} = 1$
- $w_{\mathbb{Q}} = 2$
- $d_{\mathbb{Q}} = 1$

---

## 4. 函數方程測試

### 測試內容

| 測試方法 | 驗證目標 |
|----------|----------|
| `test_for_dedekind` | 驗證完整 zeta 函數的函數方程 |
| `test_completed_zeta` | 計算完整 zeta 函數的值 |

### 數學原理

Dedekind zeta 函數滿足對稱的函數方程：

$$\Lambda_K(s) = \varepsilon_K \Lambda_K(1-s)$$

其中完整 zeta 函數定義為：

$$\Lambda_K(s) = |d_K|^{s/2} \gamma_K(s) \zeta_K(s)$$

gamma 因子 $\gamma_K(s)$ 取決於數域的嵌入結構：

$$\gamma_K(s) = \pi^{r_2/2} \prod_{i=1}^{r_1} \Gamma\left(\frac{s}{2}\right) \prod_{i=1}^{r_2} \Gamma(s)$$

**有理性因子** $\varepsilon_K$ 是一個代數數，滿足 $|\varepsilon_K| = 1$。

---

## 測試檔案位置

```
tests/test_dedekind_zeta.py
```

## 相關實現

```
lean4py/dedekind_zeta.py
```

---

## 備註

本模組參考 mathlib4 的 `Mathlib.NumberTheory.DedekindZeta` 設計。當前實現為簡化版本，主要用於結構驗證而非數值計算。完整的數值實現需要精確的素理想分解和級數求和算法。