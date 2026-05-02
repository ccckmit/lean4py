# 測量理論測試文檔

本文檔說明 `test_measure_theory.py` 中測試案例背後的數學原理。

## 1. 測試驗證的內容概述

測量理論（Measure Theory）是實變函數論的核心基礎，本測試模組驗證以下關鍵組件：

- σ-代數的構建與性質
- 可測空間的定義
- 測度的基本性質
- 勒貝格測度與積分
- Lp 空間相關功能

---

## 2. σ-代數測試（Sigma-Algebra Tests）

### 測試類別：`TestSigmaAlgebra`

### 數學原理

σ-代數是滿足以下三個條件的集合族 $\mathcal{F}$：

1. **封閉性**：$\Omega \in \mathcal{F}$（全集在 σ-代數中）
2. **補集封閉**：若 $A \in \mathcal{F}$，則 $A^c = \Omega \setminus A \in \mathcal{F}$
3. **可數並封閉**：若 $A_1, A_2, \ldots \in \mathcal{F}$，則 $\bigcup_{n=1}^{\infty} A_n \in \mathcal{F}$

由以上三條可得：σ-代數對可數交集也是封閉的，因為：
$$A \cap B = (A^c \cup B^c)^c$$

### 測試案例分析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | σ-代數可成功創建 | 確認 sigma_algebra 對象的基本構造 |
| `test_is_in` | 空集和全集屬於 σ-代數 | 驗證性質 1：$\emptyset, \Omega \in \mathcal{F}$ |
| `test_complement` | 補集運算正確 | 驗證性質 2：對補集封閉 |
| `test_is_sigma_algebra` | 確認是有效的 σ-代數 | 綜合驗證三條公理 |
| `test_union` | 可數並封閉 | 驗證性質 3 |
| `test_intersection` | 可數交封閉 | 由性質 2、3 導出 |

### 代碼對應
- `SigmaAlgebra.is_in()` - 檢查集合是否在 σ-代數中
- `SigmaAlgebra.complement()` - 計算補集
- `SigmaAlgebra.is_sigma_algebra()` - 驗證三條公理

---

## 3. 可測空間測試（Measurable Space Tests）

### 測試類別：`TestMeasurableSpace`

### 數學原理

可測空間是二元組 $(\Omega, \mathcal{F})$，其中：
- $\Omega$ 是全集（樣本空間）
- $\mathcal{F}$ 是定義在 $\Omega$ 上的 σ-代數

可測空間是構建測度的基礎，只有在可測空間上才能定義測度。

### 測試案例分析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | 可測空間包含σ-代數 | 確認 $(X, \mathcal{F})$ 結構正確 |
| `test_is_measurable` | 空集是可測的 | $\emptyset \in \mathcal{F}$ 是基本要求 |

---

## 4. 測度測試（Measure Tests）

### 測試類別：`TestMeasure`

### 數學原理

測度 $\mu$ 是定義在可測空間 $(\Omega, \mathcal{F})$ 上的函數，滿足：

1. **非負性**：$\mu(A) \geq 0$ 對所有 $A \in \mathcal{F}$
2. **空集測度為零**：$\mu(\emptyset) = 0$
3. **可數可加性**：若 $A_1, A_2, \ldots$ 兩兩不交，則：
$$\mu\left(\bigcup_{n=1}^{\infty} A_n\right) = \sum_{n=1}^{\infty} \mu(A_n)$$

從可數可加性可導出有限可加性：當 $A \cap B = \emptyset$ 時，$\mu(A \cup B) = \mu(A) + \mu(B)$

### 測試案例分析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | 測度值非負 | 驗證非負性 |
| `test_empty_set` | $\mu(\emptyset) = 0$ | 測度的基本要求 |
| `test_is_measure` | 確認是有效的測度 | 驗證三條公理 |
| `test_is_finite` | 測度有限 | 確保 $\mu(\Omega) < \infty$ |

### 重要性質

測度的連續性：
- **從下連續**：若 $A_n \uparrow A$，則 $\mu(A_n) \uparrow \mu(A)$
- **從上連續**：若 $A_n \downarrow A$ 且 $\mu(A_1) < \infty$，則 $\mu(A_n) \downarrow \mu(A)$

---

## 5. 勒貝格測度測試（Lebesgue Measure Tests）

### 測試類別：`TestLebesgueMeasure`

### 數學原理

勒貝格測度 $m$ 是 $\mathbb{R}^n$ 上最自然的測度，具備以下特性：

1. **平移不變性**：$m(A + x) = m(A)$ 對所有 $x \in \mathbb{R}^n$
2. **正則性**：開集的測度是內部逼近，封閉集的測度是外部逼近
3. 在區間 $[a,b]$ 上，$m([a,b]) = b - a$

勒貝格測度是勒貝格積分的基礎，區別於黎曼積分，它能處理更多奇異函數。

### 測試案例分析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | 勒貝格測度對象可創建 | 確認 LebesgueMeasure 類初始化 |
| `test_interval_length` | 區間長度非負 | 驗證 $m([0,1]) = 1 > 0$ |
| `test_empty_set` | 空集測度為零 | 與一般測度一致 |

### 勒貝格測度 vs 黎曼積分

勒貝格測度的優勢：
- 可以處理不可數個不連續點的函數
- 極限運算與積分可交換的條件更寬鬆
- 完整的收斂定理（ dominated convergence 等）

---

## 6. 可測函數測試（Measurable Function Tests）

### 測試類別：`TestMeasurableFunction`

### 數學原理

可測函數 $f: (\Omega_1, \mathcal{F}_1) \to (\Omega_2, \mathcal{F}_2)$ 滿足：

$$\forall B \in \mathcal{F}_2: f^{-1}(B) \in \mathcal{F}_1$$

即原像為可測集。簡單函數是可測函數的特殊情況，可表示為：
$$f = \sum_{i=1}^n a_i \cdot \mathbf{1}_{A_i}$$
其中 $A_i$ 是兩兩不交的可測集。

### 測試案例分析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | 可測函數構造正確 | $f(x) = 10x$ 在定義域上可測 |
| `test_is_measurable` | 確認是可測函數 | 驗證原像條件 |

### 簡單函數測試（TestSimpleFunction）

簡單函數測試驗證：
- **標準表示**：$f(x) = 1$ 當 $x \in \{1\}$，$f(x) = 2$ 當 $x \in \{2,3\}$
- **可測性**：每個取值對應的集合都是可測的
- **求值**：正確計算 $f(x)$ 的值

---

## 7. 勒貝格積分測試（Lebesgue Integral Tests）

### 測試類別：`TestLebesgueIntegral`

### 數學原理

勒貝格積分通過簡單函數逼近定義：

**對簡單函數**：
$$\int f \,d\mu = \sum_{i=1}^n a_i \mu(A_i)$$

**對非負函數**：
$$\int f \,d\mu = \sup \left\{ \int s \,d\mu : 0 \leq s \leq f, s \text{ 為簡單函數} \right\}$$

**對一般可積函數**：
$$f = f^+ - f^-$$
$$\int f \,d\mu = \int f^+ \,d\mu - \int f^- \,d\mu$$
要求 $\int f^+ \,d\mu < \infty$ 或 $\int f^- \,d\mu < \infty$

### 與黎曼積分的區別

| 黎曼積分 | 勒貝格積分 |
|---------|-----------|
| 分定義域 | 分值域 |
| 依賴區間逼近 | 依賴測度逼近 |
| 極限交換條件嚴格 | 極限交換條件寬鬆 |

### 測試案例分析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_of_simple` | 簡單函數積分 | 直接計算 $\int f \,d\mu = \sum a_i \mu(A_i)$ |
| `test_of_positive` | 非負函數積分 | 使用逼近定義驗證非負性 |

---

## 8. 概率測度測試（Probability Measure Tests）

### 測試類別：`TestProbabilityMeasure`

### 數學原理

概率測度 $\mathbb{P}$ 是滿足 $\mathbb{P}(\Omega) = 1$ 的測度，稱為概率測度空間 $(\Omega, \mathcal{F}, \mathbb{P})$。

概率測度的特殊性質：
1. $\mathbb{P}(\Omega) = 1$（歸一化條件）
2. $\mathbb{P}(A^c) = 1 - \mathbb{P}(A)$
3. $\mathbb{P}(A \cup B) = \mathbb{P}(A) + \mathbb{P}(B) - \mathbb{P}(A \cap B)$

### 測試案例分析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | $\mathbb{P}(\Omega) = 1$ | 驗證概率測度的歸一化 |

---

## 9. 波萊爾 σ-代數測試（Borel Sigma-Algebra Tests）

### 測試類別：`TestBorelSigmaAlgebra`

### 數學原理

波萊爾 σ-代數 $\mathcal{B}(\Omega)$ 是由拓撲空間 $\Omega$ 的開集生成的 σ-代數：
$$\mathcal{B}(\Omega) = \sigma(\mathcal{T})$$
其中 $\mathcal{T}$ 是 $\Omega$ 上的拓撲。

波萊爾 σ-代數包含所有開集、閉集，以及它們的可數並、交、補運算所得的集合。

### 測試案例分析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_from_topology` | 從拓撲生成波萊爾σ-代數 | $\mathcal{B} = \sigma(\mathcal{T})$ |

---

## 10. Lp 空間相關說明

雖然本測試文件未直接包含 Lp 空間測試，但測量理論是 Lp 空間理論的基礎：

### 數學原理

對 $1 \leq p < \infty$，Lp 空間定義為：
$$L^p(\Omega, \mathcal{F}, \mu) = \left\{ f \text{ 可測} : \int |f|^p \,d\mu < \infty \right\}$$

配備範數：
$$\|f\|_p = \left( \int |f|^p \,d\mu \right)^{1/p}$$

重要性質：
- **完備性**：$L^p$ 是巴拿赫空間
- ** Hölder 不等式**：$\|fg\|_1 \leq \|f\|_p \|g\|_q$ 其中 $\frac{1}{p} + \frac{1}{q} = 1$
- **閔可夫斯基不等式**：$\|f + g\|_p \leq \|f\|_p + \|g\|_p$

---

## 總結

本測試模組全面覆蓋了測量理論的核心概念：
- σ-代數作為可測集合的結構
- 測度作為集合的「大小」度量
- 可測函數作為可積分的函數類
- 勒貝格積分作為黎曼積分的推廣
- 概率測度作為歸一化測度的特殊情況

這些構成實變函數論和現代概率論的數學基礎。