# 序理論測試文檔

本文件說明 `test_order_theory.py` 中測試用例背後的數學原理。

## 1. 概述

本測試模組驗證序理論（Order Theory）的核心概念，包括偏序、全序、格、完整格、Galois 連接、Heyting 代數和 Boolean 代數。這些結構是數學和計算機科學中表示層次關係和約束的基礎工具。

## 2. 偏序測試 (Partial Order Tests)

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建偏序集合 |
| `test_leq` | 驗證 `<=` 關係（自反、反對稱、傳遞） |
| `test_is_partial_order` | 確認偏序性質 |
| `test_is_comparable` | 判斷兩元素是否可比較 |
| `test_min_elements` | 找出極小元素 |
| `test_max_elements` | 找出極大元素 |

### 數學原理

**偏序定義**：集合 $P$ 上的二元關係 $\leq$ 若滿足以下三條件，則為偏序：
- **自反性**：$\forall a \in P, a \leq a$
- **反對稱性**：$\forall a, b \in P, a \leq b \land b \leq a \Rightarrow a = b$
- **傳遞性**：$\forall a, b, c \in P, a \leq b \land b \leq c \Rightarrow a \leq c$

**可比較性**：若 $a \leq b$ 或 $b \leq a$ 任一成立，則 $a$ 與 $b$ 可比較。

**極小/極大元素**：
- $m$ 為極小元素：不存在 $x \in P$ 使得 $x < m$
- $M$ 為極大元素：不存在 $x \in P$ 使得 $M < x$

測試使用整數集合 `{1, 2, 3}` 和標準 `<=` 關係作為示例。

## 3. 全序測試 (Total Order Tests)

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建全序集合 |
| `test_is_total_order` | 確認全序性質 |

### 數學原理

**全序定義**：偏序 $\leq$ 若額外滿足**完全性**（comparability），則為全序：
$$\forall a, b \in P, a \leq b \lor b \leq a$$

全序也稱為線性序，意味著任意兩元素均可比較。整數、有理數、實數的標準順序都是全序。

## 4. 格測試 (Lattice Tests)

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建格結構 |
| `test_join` | 驗證上確界（join）運算 |
| `test_meet` | 驗證下確界（meet）運算 |
| `test_is_lattice` | 確認格性質 |

### 數學原理

**格定義**：偏序集合 $(L, \leq)$ 若任意兩元素 $a, b$ 的上確界（join）和下確界（meet）都存在，則稱為格。

- **Join（$\sqcup$ 或 $\vee$）**：$a \vee b$ 為 $a$ 和 $b$ 的最小上界（least upper bound）
- **Meet（$\sqcap$ 或 $\wedge$）**：$a \wedge b$ 為 $a$ 和 $b$ 的最大下界（greatest lower bound）

**格的基本性質**：
$$a \leq b \iff a \wedge b = a \iff a \vee b = b$$

測試中 `join(1, 2) = max(1, 2) = 2`，`meet(1, 2) = min(1, 2) = 1$。

## 5. 完整格測試 (Complete Lattice Tests)

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建完整格（驗證 `_complete` 標誌） |
| `test_is_complete` | 確認完整格性質 |

### 數學原理

**完整格定義**：偏序集合 $(L, \leq)$ 若任意子集（不僅限於二元）的上確界和下確界都存在，則稱為完整格。

**與格的關係**：完整格必為格，但格不一定是完整格。

**完整格的例子**：
- 任意有限格的 powerset 都是完整格
- 實數區間 $[0, 1]$ 是完整格
- 自然數集合 with bottom element 是完整格

測試驗證 `is_complete()` 方法返回 `True`。

## 6. Galois 連接測試 (Galois Connection Tests)

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建 Galois 連接 |
| `test_is_galois_connection` | 確認 Galois 連接性質 |

### 數學原理

**Galois 連接定義**：設 $(P, \leq_P)$ 和 $(Q, \leq_Q)$ 為偏序集合。若函數 $f: P \to Q$ 和 $g: Q \to P$ 滿足以下條件，則 $(f, g)$ 構成 Galois 連接：
$$\forall a \in P, \forall b \in Q, f(a) \leq_Q b \iff a \leq_P g(b)$$

**等價條件**：
1. $f$ 和 $g$ 為單調函數
2. $a \leq g(f(a))$ 且 $f(g(b)) \leq b$
3. $g \circ f$ 為閉包算子，$f \circ g$ 為核算子

**測試示例**：
- $f(x) = x \times 10$（從 $\{1, 2\}$ 到 $\{10, 20\}$）
- $g(y) = y \div 10$（從 $\{10, 20\}$ 到 $\{1, 2\}$）
- 驗證：$f(1) = 10 \leq 20 \iff 1 \leq 2 = g(20)$ ✓

## 7. Heyting 代數測試 (Heyting Algebra Tests)

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建 Heyting 代數 |
| `test_implies` | 驗證蘊含運算 |
| `test_is_heyting` | 確認 Heyting 代數性質 |

### 數學原理

**Heyting 代數定義**：有界格 $H$ 若任意元素 $a, b$ 的相對偽補（relative pseudocomplement）$a \to b$ 存在，則稱為 Heyting 代數。

**蘊含運算的性質**：
$$c \leq (a \to b) \iff (c \wedge a) \leq b$$

**偽補性質**：
- $a \to a = \top$（top 為單位元）
- $a \wedge (a \to b) \leq b$
- $a \to b = \top$ 當且僅當 $a \leq b$

測試使用二元集合 $\{0, 1\}$，蘊含定義為：$x \to y = 1$ 若 $x \leq y$，否則為 $0$。

## 8. Boolean 代數測試 (Boolean Algebra Tests)

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 創建 Boolean 代數 |
| `test_complement` | 驗證補運算 |
| `test_is_boolean` | 確認 Boolean 代數性質 |

### 數學原理

**Boolean 代數定義**：格 $(B, \vee, \wedge)$ 若滿足：
1. 為有界分配格
2. 每元素都有補元

**補元的性質**：
$$\forall a \in B, a \vee \neg a = \top, \quad a \wedge \neg a = \bot$$

**與 Heyting 代數的關係**：Boolean 代數是 Heyting 代數的特例，其中每元素都有補元。

**De Morgan 定律**：
$$\neg(a \vee b) = \neg a \wedge \neg b$$
$$\neg(a \wedge b) = \neg a \vee \neg b$$

測試使用二元 Boolean 代數，補運算為 $\neg x = 1 - x$。

## 9. 測試架構

```
TestPartialOrder      → 基礎偏序結構
    ↓
TestTotalOrder        → 全序（額外完全性）
    ↓
TestLattice           → 格（join/meet 封閉）
    ↓
TestCompleteLattice   → 完整格（任意子集封閉）
```

附加結構：
- `TestHeytingAlgebra` - 在格的基礎上增加蘊含運算
- `TestBooleanAlgebra` - 在 Heyting 代數基礎上增加補運算
- `TestGaloisConnection` - 獨立的序對偶之間的映射關係

## 10. 數據類型對照表

| 數學結構 | 代碼類 | 關鍵方法 |
|---------|--------|---------|
| 偏序 | `PartialOrder` | `leq()`, `is_partial_order()` |
| 全序 | `TotalOrder` | `is_total_order()` |
| 格 | `Lattice` | `join()`, `meet()` |
| 完整格 | `CompleteLattice` | `is_complete()` |
| Galois 連接 | `GaloisConnection` | `is_galois_connection()` |
| Heyting 代數 | `HeytingAlgebra` | `implies()` |
| Boolean 代數 | `BooleanAlgebra` | `complement()` |