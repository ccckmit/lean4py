# 高階範疇論測試文檔

本文檔說明 `test_higher_category_theory.py` 中測試用例的數學原理。

---

## 1. 測試驗證的內容概述

本測試模組驗證高階範疇論（Higher Category Theory）的核心概念實現，包括：

- **∞-範疇（∞-Categories）**：具有無限維度同倫結構的範疇
- **Kan 複形（Kan Complexes）**：滿足 Kan 條件的 simplicial set
- **n-範疇（n-Categories）**：維度受限的高階範疇
- **弱等價（Weak Equivalences）**：同倫論中的弱化等價關係
- **同倫推出/拉回（Homotopy Pushout/Pullback）**：同倫論中的極限結構
- **Segal 範疇（Segal Categories）**：用於建模∞-範疇的經典方法
- **完整 Segal 空間（Complete Segal Spaces）**：另一種∞-範疇模型
- **Anima**：同倫論中的基本對象
- **∞-Topos**：廣義的拓撲斯理論

---

## 2. 雙範疇測試（Bicategory Tests）

### 2.1 測試類別：`TestNCategory`

 bicategory 是二維範疇的經典形式。

```python
nc = NCategory(3)  # 建立一個 3-範疇
nc.add_object("X")  # 添加對象
hom = nc.hom_category("X", "Y")  # 獲取 hom-範疇
```

### 2.2 數學原理

**n-範疇的結構：**
- **對象（Objects）**：範疇中的元素
- **態射（Morphisms）**：對象之間的箭頭
- **高階態射（Higher Morphisms）**：態射之間的變形

對於 **bicategory**（2-範疇）：
- 對象之間存在 hom-category（而非 hom-set）
- 態射之間有 1-態射和 2-態射
- 合成律在弱意義下成立（associativity up to homotopy）

**測試驗證點：**
- `test_hom_category_n1`：當 n=1 時，hom_category 返回 None，因為 1-範疇的 hom 仍是 set
- `test_is_strict` / `test_is_weak`：區分嚴格範疇與弱範疇
- `test_coherence_theorem`： coherence 定理確保弱範疇可提升為嚴格範疇

---

## 3. Kan 複形測試（Kan Complex Tests）

### 3.1 測試類別：`TestKanComplex`

Kan 複形是 simplicial set 中的重要概念，是 ∞-範疇的基礎模型。

```python
kc = KanComplex()
kc.add_simplex(2, "simplex_2d")  # 添加 2-維單形
fm = kc.face_map(simplex, 0)     # 面映射
dm = kc.degeneracy_map(simplex, 0)  # 退化映射
```

### 3.2 數學原理

**Kan 條件（Kan Condition）：**
對於任何  horn Λ^n[k]，存在一個 n-單形擴展。這確保了「所有內部填充」的存在性。

**基本結構：**
- **單形（Simplices）**：幾何胞腔
- **面映射（Face Maps）**：d_i : X_n → X_{n-1}
- **退化映射（Degeneracy Maps）**：s_i : X_n → X_{n+1}
- **Horn**：部分單形，如 Λ^2[1] = {0,2}（缺少面 1）

**測試驗證點：**
- `test_horn_lambda`：檢查特定 horn 的填充因子
- `test_filler_exists`：驗證 Kan 填充條件
- `test_is_kan`：確認是合法的 Kan 複形
- `test_homotopy_groups`：計算同倫群 π_n(K)
- `test_fundamental_groupoid`：提取基本群胚

---

## 4. ∞-範疇測試（∞-Category Tests）

### 4.1 測試類別：`TestInfinityCategory`

∞-範疇是具有無限維度同倫結構的範疇，是高階範疇論的核心研究對象。

```python
ic = InfinityCategory("C")
ic.add_object("X")
ic.add_object("Y")
hs = ic.hom_space("X", "Y")  # 返回 KanComplex
```

### 4.2 數學原理

**∞-範疇的特徵：**
- 對象之間的 hom-space 是 Kan 複形（而非 set）
- 存在∞-維度的態射複合結構
- 滿足同倫版範疇公理

**與普通範疇的關係：**
- 普通範疇可视为 ∞-範疇（所有 hom-space 為離散 Kan 複形）
- π_0 提取給出普通範疇（homotopy category）

**Joyal 模型結構：**
- ∞-範疇在 Joyal 模型結構下是 fibrant 對象
- Cofibrations：mono（單射）
- Weak equivalences：Joy-等價

**測試驗證點：**
- `test_hom_space`：驗證 hom_space 返回 KanComplex
- `test_is_fibrant`：確認是 fibrant 對象
- `test_joyal_model_structure`：檢驗 Joyal 模型結構

---

## 5. 其他重要測試類別

### 5.1 TestWeakEquivalence（弱等價）

```python
we = WeakEquivalence("X", "Y", lambda x: x)
we.two_out_of_three(we2)  # 驗證二三性質
```

**數學原理：**
弱等價是同倫論中的基本概念。二三性質：如果 f,g 是弱等價，則 gf 也是弱等價。

### 5.2 TestHomotopyPushout / TestHomotopyPullback（同倫推出/拉回）

```python
hp = HomotopyPushout(["A", "B", "C"])
hp.universal_property()  # 驗證泛性質
```

**數學原理：**
同倫推出是範疇推出的同倫版本。泛性質：在同倫意義下唯一填充任何交換圖。

### 5.3 TestSegalCategory / TestCompleteSegalSpace（Segal 範疇）

```python
sc = SegalCategory()
sc.is_segal()  # 驗證 Segal 條件
```

**數學原理：**
Segal 條件：Segal 映射 X_n → X_1 ×_{X_0} ... ×_{X_0} X_1 是弱等價。

### 5.4 TestAnima（動形）

```python
a = Anima()
a.is_kan()  # 檢查是否為 Kan 複形
a.is_discrete()  # 是否為離散
```

**數學原理：**
Anima 是同倫論中的基本對象，等價於 topological space 的弱同倫類。

### 5.5 TestInfinityTopos（∞-拓撲斯）

```python
it = InfinityTopos("site")
it.sheafify(presheaf)  # 層化
it.left_exact_localization(S)  # 左正確認同
```

**數學原理：**
∞-Topos 是 Grothendieck topos 的推廣，滿足層公理的 ∞-版本。

---

## 6. 測試結構總覽

| 測試類別 | 測試數量 | 主要驗證對象 |
|---------|---------|------------|
| TestInfinityCategory | 8 | ∞-範疇基本結構 |
| TestKanComplex | 10 | Kan 複形與填充條件 |
| TestNCategory | 8 | n-範疇與 bicategory |
| TestWeakEquivalence | 4 | 弱等價性質 |
| TestHomotopyPushout | 5 | 同倫推出 |
| TestHomotopyPullback | 5 | 同倫拉回 |
| TestSegalCategory | 6 | Segal 範疇 |
| TestCompleteSegalSpace | 5 | 完整 Segal 空間 |
| TestAnima | 5 | 動形對象 |
| TestInfinityTopos | 6 | ∞-拓撲斯 |

---

## 7. 數學背景補充

### 7.1 為何需要高階範疇論？

普通範疇只能描述「對象」和「態射」。高階範疇允許：
- **同倫等價**：態射之間的等價不再是命運
- **弱合成**：結合律在同倫意義下成立
- **豐富結構**：如 topological quantum field theory

### 7.2 模型的多樣性

∞-範疇有多種等價的數學模型：
- **Quasi-categories**（Joyal）：最常用
- **Complete Segal Spaces**（Rezk）：-simplicial spaces
- **Segal Categories**：離散的情形
- **Kan Complexes**：groupoid 情形

---

*本文件由代碼自動生成，基於 lean4py v1.27 版本的 higher_category_theory 模組。*