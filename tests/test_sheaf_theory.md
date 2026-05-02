# Sheaf Theory 測試文件說明

本文件基於 `tests/test_sheaf_theory.py` 測試案例，說明層論（Sheaf Theory）的數學原理。

## 1. 測試驗證概述

測試文件驗證了層論模組的核心功能，包含：
- 前層（Presheaf）的創建與基本性質
- 層（Sheaf）的條件滿足
- 層化（Sheafification）過程
- Grothendieck 拓撲
- 層上同調（Sheaf Cohomology）

## 2. 前層（Presheaf）測試

### 測試案例
- `test_creation`: 驗證前層對象的創建
- `test_restrict`: 驗證限制映射（restriction map）
- `test_is_presheaf`: 驗證前層性質

### 數學原理

**前層**是从开集范畴的相反范畴到某个目标范畴的函子：

```
F: Open(X)ᵒᵖ → C
```

對於拓撲空間 X 的每個開集 U，前層 F 分配一個對象 F(U)。
對於包含關係 V ⊆ U，存在限制映射：

```
res_{U,V}: F(U) → F(V)
```

限制映射滿足：
- `res_{U,U} = id_{F(U)}`
- 若 W ⊆ V ⊆ U，則 `res_{V,W} ∘ res_{U,V} = res_{U,W}`

## 3. 層（Sheaf）條件測試

### 測試案例
- `test_satisfies_sheaf_condition`: 驗證層條件
- `test_is_sheaf`: 驗證對象是否為層

### 數學原理

層是滿足**層公理**的前層，包含兩個條件：

#### 局部性（Locality）
若 `{Uᵢ}` 是開集 U 的覆蓋，且
- s, t ∈ F(U)
- 對所有 i，`res_{U,Uᵢ}(s) = res_{U,Uᵢ}(t)`

則 s = t。

#### 粘合（Gluing）
若 `{Uᵢ}` 是開集 U 的覆蓋，
且對每個 i 給定 sᵢ ∈ F(Uᵢ)，
滿足對所有 i, j：`res_{Uᵢ,Uᵢ∩Uⱼ}(sᵢ) = res_{Uⱼ,Uᵢ∩Uⱼ}(sⱼ)`，

則存在唯一的 s ∈ F(U)，使得對所有 i：
`res_{U,Uᵢ}(s) = sᵢ`。

## 4. 莖（Stalk）測試

**注意**：當前測試文件中沒有明確的莖測試案例。以下說明若存在此類測試時應驗證的內容。

### 若存在莖測試，應驗證

莖是層在某一點的「局部化」：

```
F_x = colim_{x ∈ U} F(U)
```

即所有包含 x 的開集的截面正向極限。

### 數學原理

對於前層 F，點 x 處的莖 Fₓ 由以下元素組成：
- 對 (U, s)，其中 x ∈ U 且 s ∈ F(U)
- 等價關係：(U, s) ~ (V, t) 當且僅當存在 x ∈ W ⊆ U ∩ V 使得 `res_{U,W}(s) = res_{V,W}(t)`

**層的關鍵性質**：
- 層的截面由其莖完全決定
- 若所有莖都為平凡，則層為平凡

## 5. 層化（Sheafification）測試

### 測試案例
- `test_sheafify`: 驗證前層到層的轉換
- `test_unit`: 驗證單位映射 η: P → sheafify(P)

### 數學原理

層化是將前層轉為層的函子：

```
sheafify: PSh(X) → Sh(X)
```

存在自然變換（單位）η: 1_{PSh} ⇒ sheafify，使得：
- 對每個前層 P，sheafify(P) 是層
- 對每個層 F，sheafify(F) ≅ F

**構造方式**（Igor 構造）：
對每個開集 U，定義：

```
sheafify(P)(U) = { (s_x)_{x∈U} | 對每個 x ∈ U，存在開鄰域 V ⊆ U 使得 s ∈ P(V)，且對所有 y ∈ V 有 s_y = res_{V,y}(s) }
```

## 6. Grothendieck 拓撲測試

### 測試案例
- `test_creation`: 驗證 Grothendieck 拓撲的創建
- `test_is_covering`: 驗證覆蓋判定
- `test_is_topology`: 驗證拓撲公理

### 數學原理

Grothendieck 拓撲 J 在範疇 C 上分配每個對象 X 一組覆蓋族 J(X)，滿足：

1. **退化性**：{X} ∈ J(X)
2. **反射性**：若 {Uᵢ} ∈ J(X)，V ⊆ X，則 {Uᵢ ∩ V} ∈ J(V)
3. **兼容性**：若 {Uᵢ} ∈ J(X)，每個 Uᵢ 有覆蓋 {Vᵢⱼ}，則 {Vᵢⱼ} ∈ J(X)
4. **同構穩定性**：若 {Uᵢ} ∈ J(X)，f: Y → X 為同構，則 {f^{-1}(Uᵢ)} ∈ J(Y)

## 7. 層上同調測試

### 測試案例
- `test_compute`: 驗證上同調群的計算
- `test_vanishing`: 驗證維數消失定理

### 數學原理

層上同調 Hⁱ(X, F) 定義為：

```
Hⁱ(X, F) = Extⁱ(ℤ_X, F)
```

或等價地，使用內注射分解：
```
0 → F → I⁰ → I¹ → I² → ...
```
其中 Iᵏ 為內射層，取全局截面後取上同調。

**基本性質**：
- H⁰(X, F) ≅ Γ(X, F)（整體截面）
- 若 F 為鬆弛層，H¹(X, F) 分類 F-值的 Čech 上同調

**維數消失**：若 dim X < ∞，則對所有 i > dim X，Hⁱ(X, F) = 0。

## 測試覆蓋矩陣

| 類別 | 測試方法 | 驗證內容 |
|------|---------|---------|
| TestPresheaf | test_creation, test_restrict, test_is_presheaf | 前層基本結構 |
| TestSheaf | test_satisfies_sheaf_condition, test_is_sheaf | 層公理 |
| TestSheafification | test_sheafify, test_unit | 層化函子 |
| TestGrothendieckTopology | test_creation, test_is_covering, test_is_topology | Grothendieck 拓撲 |
| TestSheafCohomology | test_compute, test_vanishing | 層上同調 |
| TestStalk | （未實現） | 莖的構造與性質 |

## 與 mathlib4 的對齊

本模組參考 `Mathlib.Topology.Sheaves` 設計，當前為簡化版本。
完整實現應包含：
- 莖的精確構造
- 截面層的豐富結構
- Čech 上同調與 derived functor 的關聯
- 譜序列應用