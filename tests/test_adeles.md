# Adele 環測試文檔

## 概述

本測試文件驗證 `lean4py/adeles.py` 模塊中關於阿代數（Adeles）的核心功能。Adeles 是局部緊域的粿限乘積，是數論中研究整體域性質的重要工具。

---

## 1. 測試驗證的內容

### 1.1 Adele Ring 測試 (`TestAdeleRing`)

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | AdeleRing 對象正確創建，field 屬性為 "Q" |
| `test_is_ring` | Adele環是環結構（滿足加法和乘法封閉性） |
| `test_diagonal_embedding` | 對角嵌入 Δ: K → A_K 正確返回 adele 類型元素 |

### 1.2 有限Adele測試 (`TestFiniteAdeles`)

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_restricted_product` | 有限Adele A_K^f = Π'_v∤∞ K_v 的受限乘積計算 |
| `test_is_locally_compact` | 有限Adele空間是局部緊的 |

### 1.3 無限Adele測試 (`TestInfiniteAdeles`)

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_product` | 無限Adele A_K^∞ = Π_{v\|∞} K_v 的笛卡爾積計算 |
| `test_is_euclidean_space` | 無限Adele同構於 ℝ^{r₁} × ℂ^{r₂}（歐幾里得空間） |

### 1.4 受限乘積測試 (`TestRestrictedProduct`)

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_compute` | 受限乘積 Π'_i M_i 的計算，含多個分量（如 Q_2, Q_3） |
| `test_is_topological_ring` | 受限乘積是拓撲環 |

---

## 2. Adele環的數學原理

### 2.1 定義

Adele環 A_K 是域 K 的所有局部域的受限粿限乘積：

$$A_K = \prod'_v K_v = \left\{(x_v) \in \prod_v K_v \mid x_v \in \mathcal{O}_{K_v} \text{ 對幾乎所有有限位}\right\}$$

其中：
- K_v 是域 K 在位 v 的局部域
- 對幾乎所有有限位，x_v 屬於其整環 O_{K_v}

### 2.2 對角嵌入

對角嵌入 Δ: K → A_K 將域 K 的元素映射到其 Adele 環中：

$$\Delta(x) = (x, x, x, \ldots)$$

這使得 K 可以看作是 A_K 的子環。

### 2.3 有限Adele與無限Adele

Adele環可分解為：
- **有限Adele**: A_K^f = Π'_v∤∞ K_v（僅含有限位）
- **無限Adele**: A_K^∞ = Π_{v|∞} K_v（僅含無限位）
- **完全Adele**: A_K = A_K^f × A_K^∞

---

## 3. Idele的數學原理

### 3.1 定義

Idele群是 Adele 環的可逆元群：

$$\mathbb{I}_K = A_K^\times = \{x \in A_K \mid x_v \neq 0 \text{ 對所有位 } v\}$$

### 3.2 主Idele

主Idele由域 K 的非零元素生成：

$$\Delta: K^\times \hookrightarrow \mathbb{I}_K$$

### 3.3 Tamagawa數

Tamagawa數 τ(K) 是Idele伴隨測度的體積：

$$\tau(K) = \text{Vol}(\mathbb{I}_K / K^\times)$$

對於代數數域，Tamagawa數猜想為 1（此猜想已被證明）。

---

## 4. 受限乘積結構

### 4.1 定義

受限乘積 Π'_i M_i 由滿足「幾乎所有分量屬於指定子集」的元素組成：

$$\prod'_i M_i = \left\{(x_i) \mid x_i \in S_i \text{ 對幾乎所有 } i\right\}$$

### 4.2 拓撲結構

受限乘積配備了自然的拓撲結構，使其成為拓撲環。

---

## 5. 測試數學意義總結

| 測試類別 | 數學意義 |
|---------|---------|
| AdeleRing | 驗證 Adele 環的基本結構和對角嵌入 |
| FiniteAdeles | 驗證有限位的局部緊性和受限乘積 |
| InfiniteAdeles | 驗證無限位同構於歐幾里得空間 |
| RestrictedProduct | 驗證受限乘積的拓撲環性質 |

---

## 6.相關數學庫

本模組仿照 mathlib4 的 `Mathlib.NumberTheory.Adele` 實現，用於代數數論研究。