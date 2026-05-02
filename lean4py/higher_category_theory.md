# Higher Category Theory (高階範疇論)

## 概述

高階範疇論是範疇論的推廣，考慮範疇之間的態射、態射之間的態射（2-態射）、以及更高階的結構。本模組實現了 ∞-範疇、Kan 複形、Segal 空間等高階範疇論核心概念。

## 主要類別

### InfinityCategory (∞-範疇)

`InfinityCategory` 是具有同倫等价性的範疇模型。

**數學原理：**

∞-範疇是一個範疇，其中任意兩個物件之間的態射空間是一個 ∞-群胚（Kan 複形）。與傳統範疇不同，∞-範疇允許態射之間存在高階態射，且所有複合運算滿足同倫結合律。

**模型類型：**

- **Kan 複形**：所有 horn 都有填充子的单纯形集
- **Segal 空間**：滿足 Segal 條件的字典序空間序列
- **完全 Segal 空間**：Segal 空間加上完备性條件
- **Quasi-categories**：Joyal 模型結構中的弱 Kan 複形

```python
C = InfinityCategory("C")
C.add_object("X")
C.add_object("Y")
hom_space = C.hom_space("X", "Y")  # Map(X,Y) 作為 Kan 複形
```

### KanComplex (Kan 複形)

`KanComplex` 是单纯形集，其中所有 horn 都有唯一的填充子。

**數學原理：**

Kan 複形是滿足 Kan 條件的单纯形集。對於任意 n-維 horn Λ^n_i（去掉第 i 個面的 n-單形），存在一個填充單形 σ ∈ X_n 使得 σ 的第 i 個面等於給定的 horn。

Kan 複形模型 ∞-群胚（即同倫類型的空間）。一個 Kan 複形 K 的基本群 π₁(K) 是其 1-骨架的古典基本群，高階同倫群 π_n(K) 定義為相應同倫群的 Kan 複合。

```python
K = KanComplex()
K.add_simplex(0, "x0")
K.add_simplex(1, ("x0", "x1"))
print(K.filler_exists(horn, 2))  # 檢查 horn 是否有填充子
print(K.is_kan())  # 驗證 Kan 條件
```

### NCategory (n-範疇)

`NCategory` 是 enrich over (n-1)-範疇的範疇。

**數學原理：**

n-範疇的層次結構：
- **0-範疇**：集合（離散範疇）
- **1-範疇**：傳統範疇，態射组成集合
- **2-範疇**：態射之間有 2-態射的範疇
- **n-範疇**：Hom-物件是 (n-1)-範疇的範疇

n-範疇分為：
- **嚴格 n-範疇**：所有複合運算嚴格滿足結合律
- **弱 n-範疇**：複合在同倫意義下滿足結合律（更高階的 coherence）

```python
C2 = NCategory(n=2, name="2Cat")
C2.add_object("A")
C2.add_object("B")
print(C2.is_strict())  # 檢查是否嚴格
print(C2.is_weak())    # 或是否為弱範疇
```

## 2-範疇與雙範疇

### Bicategory (雙範疇)

雙範疇是具有 functorial 複合態射的範疇。一個雙範疇 B 包含：
- **0-胞**：物件（0-cells）
- **1-胞**：態射（1-cells）f: A → B
- **2-胞**：態射之間的態射（2-cells）α: f ⇒ g

雙範疇的複合運算：
- 物件之間的水平複合：g ∘ f
- 態射之間的垂直複合：β ∘ α
- 混合複合（Interchange law）：(g' ∘ f') ∘ (g ∘ f) = (g' ∘ g) ∘ (f' ∘ f)

### 嚴格 2-群 (Strict 2-Group)

嚴格 2-群是一個嚴格 2-範疇，其中所有物件是點，所有 1-態射構成群，所有 2-態射是單位態射。嚴格 2-群對應於群範疇 Cat(G)（G 為群的離散範疇）。

## ∞-範疇 (Infinity Categories)

### 無限範疇的定義

∞-範疇是具有同倫維度的範疇理論結構。形式上，一個 ∞-範疇 C 包含：
- 一組物件
- 對於每對物件 X, Y，一個 Kan 複形 Map_C(X, Y)
- 複合運算：Map_C(Y, Z) × Map_C(X, Y) → Map_C(X, Z)，在同倫意義下結合

### Joyal 模型結構

Joyal 於 2000 年代建立了单纯形集範疇上的模型結構，專門用於研究 ∞-範疇：

- **弱性**：所有內部 horn 的填充子存在（這區分於 Kan 複形的完全填充）
- **纖維化**：內纖維 = 對所有 i ∈ {0,...,n} 的 horn Λ^n_i 都有填充子
- **柔性弱化**：Joyal 弱化 = 對 i ≠ 0,n 的 horn 有填充子

Quasi-category 是此模型結構中的纖維化物件。

```python
C = InfinityCategory()
print(C.joyal_model_structure())  # "Joyal"
print(C.is_fibrant())             # 檢查是否為纖維化物件
```

## Segal 空間

### Segal 條件

Segal 空間是一個函子 X: Δ^op → Spaces，滿足 Segal 條件：

X_n ≃ X_1 ×_{X_0} X_1 ×_{X_0} ... ×_{X_0} X_1  （n 個 X_1 的纖維積）

這個條件確保 X_n 描述了從 n 個物件到一個物件的 n 個態射的複合。

```python
Seg = SegalCategory("Seg")
Seg.add_space(0, "discrete")
Seg.add_space(1, "loop_space")
print(Seg.is_segal())  # 驗證 Segal 條件
```

### 完全 Segal 空間 (Complete Segal Space)

完全 Segal 空間是滿足以下條件的 Segal 空間：
- **Segal 條件**：X_n ≃ X_1 ×_{X_0} ... ×_{X_0} X_1
- **完备性**：W_0 是離散的（等價於物件的集合）

Dwyer-Kan 等價是比較完全 Segal 空間的正確弱 equivalence 概念。

```python
CSS = CompleteSegalSpace("CSS")
print(CSS.is_complete())    # 檢查完备性
print(CSS.DK_equivalence(CSS))  # Dwyer-Kan 等價
```

## 同倫假說 (Homotopy Hypothesis)

**命題**：n-維 Kan 複形（n-範疇）等價於 n-維同倫類型。

- **∞-群胚** ≡ **Kan 複形** ≡ **CW 複薄的同倫類型**
- **1-群胚** ≡ **Kan 複形**（1-維）≡ **基本群胚**
- **0-群胚** ≡ **集合**

這個假說建立了拓撲學（同倫論）和高階範疇論之間的深刻聯繫。

## Anima (動漫？動形？)

`Anima` 是 ∞-群胚的另一名稱，即作為 Kan 複形的空間。

```python
A = Anima("circle")
print(A.is_kan())          # True：每個 anima 都是 Kan 複形
print(A.is_discrete())     # 檢查是否為離散（等價於集合）
print(A.fundamental_group())  # π₁
```

## 同倫極限與餘極限

### HomotopyPullback (同倫纖維積)

同倫 pullback 是 pullback 的同倫版本。對於交換圖：

```
A → B
↓   ↓
C → D
```

同倫 pullback P 滿足的泛性質：Map(X, P) ≃ Map(X, B) ×_{Map(X, D)} Map(X, C)。

```python
HP = HomotopyPullback([A, B, C, D])
P = HP.compute_pullback()
print(HP.homotopy_fiber(f, base))  # 同倫纖維
```

### HomotopyPushout (同倫纖維餘積)

同倫 pushout 是 pushout 的同倫版本。對於 diagram：

```
B ← A → C
```

同倫 pushout P 滿足的泛性質：Map(P, X) ≃ Map(B, X) ×_{Map(A, X)} Map(C, X)。

```python
HoPo = HomotopyPushout([A, B, C])
P = HoPo.compute_pushout()
print(HoPo.is_homotopy_colimit())  # 驗證同倫餘極限性質
```

## 弱等價 (Weak Equivalence)

`WeakEquivalence` 是 ∞-範疇中的弱等價，誘導所有同倫群的同構。

```python
f = WeakEquivalence(source=X, target=Y, map_func=h)
print(f.is_weak_equivalence())    # π_n(f) 對所有 n 為同構
g = f.homotopy_inverse()          # 同倫逆
print(f.two_out_of_three(g))      # 二中取三性質
```

**二中取三性質**：若 f, g, gf 中任意兩個為弱等價，則第三個也是。

## ∞-拓撲斯 (Infinity Topos)

`InfinityTopos` 是 ∞-範疇的層論推廣。

**數學原理：**

∞-拓撲斯是滿足層公理的 ∞-範疇版本。一個 ∞-拓撲斯 E 包含：
- 對於任意 site (C, J) 上的層，化簡（Sheafification）運算
- 左正合局部化
- 邏輯結構（指數、依賴和等）

n-拓撲斯是 ∞-拓撲斯的 n-截斷，丟棄高於 n 維的同倫資訊。

```python
T = InfinityTopos(underlying_site=site)
sheaf = T.sheafify(presheaf)  # 層化
Tn = T.n_topos(n=1)            # 1-拓撲斯截斷
print(T.is_logical())         # 檢查邏輯結構
```

### 凝聚結構

凝聚 ∞-拓撲斯額外具有形狀函子和餘代數結構，適用於離散幾何的 ∞-化。

```python
print(T.cohesive_structure())  # 檢查凝聚結構
```

## 數學應用

### 1. 同倫論與代數拓撲
- Kan 複形提供 CW 複形的組合模型
- 基本群胚與古典基本群一致
- 高階同倫群编码拓撲資訊

### 2. 數學物理
- n-範疇描述拓撲量子場論的邊界
- 2-範疇中的 trace 對應於路徑積分
- ∞-範疇中的余極限描述宏觀極限

### 3. 代數幾何
- ∞-拓撲斯模型層上同倫論
- 穩定 ∞-範疇用於導出範疇
- 圖像（Schema）的 ∞-版本

### 4. 數學邏輯
- (∞,1)-邏輯是拓撲斯內部的邏輯
- 类型論的 ∞-版本
- 同倫類型論 (HoTT) 的基礎

## 與 mathlib4 的對齊

本模組參照 Jacob Lurie 的《Higher Topos Theory》和《Higher Algebra》中的框架：

- ∞-範疇的模型：Kan 複形、Segal 空間、完全 Segal 空間
- Joyal 模型結構
- ∞-拓撲斯理論
- 穩定 ∞-範疇的基本結構

## 參考文獻

1. Lurie, J. (2009). *Higher Topos Theory*. Annals of Mathematics Studies.
2. Joyal, A. (2008). *The Theory of Quasi-Categories*. Advanced Studies in Mathematics.
3. Lurie's *Higher Algebra*. 稳定 ∞-範疇的理論。
4. Joyal, A., & Tierney, M. (2007). *Notes on Simplicial Homotopy Theory*. CRM.