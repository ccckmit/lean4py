# Sheaf 測試文件文檔

本文檔說明 `test_sheaf.py` 中測試案例的數學原理。

---

## 1. 測試驗證的內容概述

本測試文件驗證了層（Sheaf）理論的核心概念實現，包括：
- 拓撲空間的構建
- 預層（Presheaf）的結構與限制映射
- 層（Sheaf）的全域截面與粘合條件
- 層上同調的基本計算
- 仿射概形與其結構層

---

## 2. 預層（Presheaf）測試

### 2.1 數學背景

**預層**是定義在拓撲空間上的函子：
- 對每個開集 $U$ 關聯一個對象 $F(U)$
- 對每個開集之間的包含關係 $V \subseteq U$ 關聯一個限制映射 $\rho_{UV}: F(U) \to F(V)$

預層滿足：
- $F(\emptyset) = \emptyset$（或單位對象）
- $\rho_{UU} = \text{id}_{F(U)}$
- 若 $W \subseteq V \subseteq U$，則 $\rho_{VW} \circ \rho_{UV} = \rho_{UW}$

### 2.2 測試案例解析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | 預層對象可正確創建 | $F: \text{Open}(X) \to \text{Set}$ 對象部分 |
| `test_add_section` | 可向開集添加截面 | 添加元素 $s \in F(U)$ |
| `test_get_section_missing` | 查詢不存在區域返回 None | 基於局部性的函子性 |
| `test_restrict` | 限制映射的實現 | 驗證 $\rho_{UV}: F(U) \to F(V)$ |

---

## 3. 層（Sheaf）公理測試

### 3.1 數學背景

**層**是滿足額外條件的預層：

**局部性公理**：若 $\{U_i\}$ 是開集 $U$ 的開覆蓋，且
$$s, t \in F(U), \quad \rho_Ui(s) = \rho_Ui(t) \quad \forall i$$
則 $s = t$。

**粘合公理**：若 $\{U_i\}$ 是開集 $U$ 的開覆蓋，且對每個 $i$ 有 $s_i \in F(U_i)$ 使得
$$\rho_{U_i \cap U_j}(s_i) = \rho_{U_j \cap U_i}(s_j) \quad \forall i, j$$
則存在唯一 $s \in F(U)$ 使得 $\rho_Ui(s) = s_i$。

層的典型例子包括：
- 連續函數層 $U \mapsto C(U)$
- 光滑函數層 $U \mapsto C^\infty(U)$
- 局部常值函數層

### 3.2 測試案例解析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | Sheaf 繼承自 Presheaf | 層是特殊的預層 |
| `test_global_section` | 全域截面的獲取 | $F(X)$ 中的整體截面 |

---

## 4. 莖（Germ）/ 纖維（Stalk）測試

### 4.1 數學背景

**莖**是層理論的核心概念：

對於層 $F$ 和點 $x \in X$，**莖** $F_x$ 定義為：
$$F_x = \oload{\lim}{\longrightarrow} F(U)$$
即所有包含 $x$ 的開集的截面在等价关系下的正向極限。

兩個截面 $s \in F(U)$ 和 $t \in F(V)$ 在莖中相等，當且僅當存在一個包含 $x$ 的小開集 $W \subseteq U \cap V$ 使得：
$$\rho_Uw(s) = \rho_Vw(t)$$

** germs** 是莖中的元素，代表截面在點附近的局部行為。

### 4.2 測試驗證內容

測試文件間接通過以下方式驗證莖的性質：
- `SheafCohomology.compute_H0()` 計算第零層上同調，其結果與全域截面相關
- 全域截面的存在性與唯一性蕴涵粘合公理

---

## 5. 層上同調（Sheaf Cohomology）測試

### 5.1 數學背景

層上同調是用於測量層「非精確程度」的工具：

對於層 $\mathcal{F}$ 和開覆蓋 $\mathcal{U} = \{U_i\}$：
- $H^0(\mathcal{U}, \mathcal{F}) = \text{ker}(\delta^0) / \text{im}(\delta^{-1})$
  - 其中 $\delta^0$ 是 Cech 上同調中的第一位差分
  - 當覆蓋足够好時，$H^0 \cong \Gamma(X, \mathcal{F})$（全域截面）

Serre 定理告訴我們在仿射概形上：
$$H^i(\text{Spec}(R), \widetilde{M}) = 0 \quad \forall i > 0$$

### 5.2 測試案例解析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | 上同調對象的初始化 | $H^i(\mathcal{U}, \mathcal{F})$ 數據結構 |
| `test_compute_H0` | 第零上同調群的計算 | $H^0 \cong \Gamma(X, \mathcal{F})$ |

---

## 6. 仿射概形（Affine Scheme）測試

### 6.1 數學背景

仿射概形 $\text{Spec}(R)$ 由拓撲空間和結構層組成：
- 底層拓撲空間：$R$ 的所有素理想的集合
- 結構層：$\mathcal{O}_X(U) = S^{-1}R$，其中 $S = R \setminus \bigcup_{\mathfrak{p} \in U} \mathfrak{p}$

### 6.2 測試案例解析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | 仿射概形的創建 | $\text{Spec}(R)$ 對象 |
| `test_is_affine` | 判定仿射性 | 檢驗是否為 $\text{Spec}(R)$ 形式 |
| `test_structure_sheaf` | 結構層的獲取 | $\mathcal{O}_{\text{Spec}(R)}$ |

---

## 7. 子概形（Subscheme）測試

### 7.1 數學背景

**閉子概形**由概形 $X$ 和理想層 $\mathcal{I}$ 定義：
$$Z = \text{Spec}(R/I) \hookrightarrow X = \text{Spec}(R)$$

**開子概形**是開浸入的像：
$$U \hookrightarrow X, \quad U \cong \text{Spec}(R_f)$$

### 7.2 測試案例解析

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_closed_subscheme` | 閉子概形的結構 | $Z \hookrightarrow X$ 浸入 |
| `test_open_subscheme` | 開子概形的結構 | $U \hookrightarrow X$ 開浸入 |

---

## 8. 測試關係圖

```
TopologicalSpace
      │
      ▼
  Presheaf ──── Sheaf 公理（局部性 + 粘合）
      │                  │
      │                  ▼
      │           global_section()
      │
      ▼
SheafCohomology
      │
      ├─── compute_H0() ─── H⁰ ≅ Γ(X, ℱ)
      │
      ▼
AffineScheme ── Spec(R)
      │
      ├─── structure_sheaf() → Sheaf
      │
      ▼
ClosedSubscheme / OpenSubscheme
```