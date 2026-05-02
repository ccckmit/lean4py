# 表示論測試文檔 (test_representation_theory_v127)

## 1. 概述

本測試模組基於 `lean4py.representation_theory_v127` 模組，用於驗證表示論的核心概念與定理。表示論是代數學中將抽象群結構轉化為線性變換进行研究的重要分支。

## 2. Representation 類別測試

### 2.1 創建與基本屬性

```python
rep = Representation("S3", 2)
```

**數學原理：** 表示論研究群 G 在向量空間 V 上的線性作用。一個表示 ρ 是一個群同態：

$$\rho: G \to GL(V)$$

其中 GL(V) 是 V 上的可逆線性變換群。`Representation` 類別封裝了：
- `group`: 群 G 的名稱（如對稱群 S₃）
- `dim`: 表示的維度（向量空間 V 的維數）
- `matrices`: 群元素對應的矩陣表示

### 2.2 字符計算

```python
result = rep.character("identity")
```

**數學原理：** 字符（Character）是表示的關鍵不變量。對於群元素 g，字符定義為：

$$\chi(g) = Tr(\rho(g))$$

即表示矩陣的跡。單位元素的字符恆等於表示的維度：
$$\chi(e) = Tr(\rho(e)) = Tr(I_n) = n$$

這是因為單位元素對應單位矩陣。

## 3. Character 類別測試

### 3.1 字符計算

```python
result = Character.compute(rep)
```

**數學原理：** `Character.compute` 計算表示在所有群元素上的字符值。對於有限群 G 的表示，字符函數：

$$\chi: G \to \mathbb{C}, \quad \chi(g) = Tr(\rho(g))$$

滿足以下性質：
- 共軛不變性：$\chi(hgh^{-1}) = \chi(g)$
- 單位元素字符等於維度：$\chi(e) = dim(V)$

### 3.2 字符正交性與不可約判斷

```python
Character.is_irreducible(char, 6)
```

**數學原理：** 字符的內積用於判斷不可約性。對於兩個字符 $\chi_1, \chi_2$：

$$\langle \chi_1, \chi_2 \rangle = \frac{1}{|G|} \sum_{g \in G} \chi_1(g) \overline{\chi_2(g)}$$

不可約表示的字符滿足：
$$\langle \chi, \chi \rangle = 1$$

這是表示論的基本定理之一，適用於特徵不整除群階的有限群。

### 3.3 字符內積

```python
Character.inner_product(char1, char2, 6)
```

**數學原理：** 字符內積是表示論中的核心工具。對稱群的不可約字符構成正交基，這使得任何表示都可以分解為不可約表示的直和。

## 4. IrreducibleRepresentation 類別測試

### 4.1 直和分解

```python
result = IrreducibleRepresentation.decompose(rep)
```

**數學原理：** 任意有限維表示可以唯一地（忽略同構）分解為不可約表示的直和：

$$V \cong \bigoplus_{i} m_i \cdot V_i$$

其中 $V_i$ 是不可約表示，$m_i$ 是重數。對於 S₃ 群：
- 平凡表示（維度 1）
- 符號表示（維度 1）
- 二維標準表示

## 5. Maschke 定理測試

### 5.1 半單性判斷

```python
MaschkeTheorem.is_semisimple(6)
```

**數學原理：** Maschke 定理表明：若群 G 的特徵不整除 |G|，則 G 的每個表示都是完全可約的（即半單的）。

對於特征為 p 的域：
- 若 p ∤ |G|：群代數 $\mathbb{C}[G]$ 是半單的（Maschke 定理）
- 若 p | |G|：存在非半單表示（如 S₃ 在特徵 3 下）

## 6. Schur 引理測試

### 6.1 標量變換判斷

```python
SchurLemma.is_scalar(endo, rep)
```

**數學原理：** Schur 引理是表示論的基本工具：

**Schur 引理：** 若 V, W 是不可約 G-表示，則任何 G-線性映射 $f: V \to W$ 或為同構，或為零映射。

推論：對於複數域上的不可約表示，其 G-自同態環為：
$$End_G(V) \cong \mathbb{C}$$

即任何 G-不變的線性變換都是標量倍數。

## 7. Decomposition 類別測試

### 7.1 直和構造

```python
Decomposition.direct_sum([rep1, rep2])
```

**數學原理：** 兩個表示的直和定義為：
$$(V \oplus W, \rho_{V \oplus W})，其中 \rho_{V \oplus W}(g) = \rho_V(g) \oplus \rho_W(g)$$

矩陣形式為分塊對角矩陣：
$$\rho_{V \oplus W}(g) = \begin{pmatrix} \rho_V(g) & 0 \\ 0 & \rho_W(g) \end{pmatrix}$$

直和的維度為各表示維度之和：
$$dim(V \oplus W) = dim(V) + dim(W)$$

## 8. 測試與數學原理對照表

| 測試類別 | 測試方法 | 驗證的數學概念 |
|---------|---------|---------------|
| TestRepresentation | test_creation | 群的表示定義 |
| TestRepresentation | test_character | 字符 $\chi(g) = Tr(\rho(g))$ |
| TestRepresentation | test_is_irreducible | 不可約性 |
| TestCharacter | test_compute | 字符函數計算 |
| TestCharacter | test_is_irreducible | $\langle \chi, \chi \rangle = 1$ 判斷法 |
| TestCharacter | test_inner_product | 字符內積正交性 |
| TestIrreducibleRepresentation | test_decompose | 直和分解定理 |
| TestMaschkeTheorem | test_is_semisimple | Maschke 定理條件 |
| TestSchurLemma | test_is_scalar | Schur 引理 |
| TestDecomposition | test_direct_sum | 直和維度疊加 |

## 9. 參考文獻

- Serre, J.-P. *Linear Representations of Finite Groups*
- Fulton, W., & Harris, J. *Representation Theory: A First Course*
- mathlib4: Mathlib.RepresentationTheory