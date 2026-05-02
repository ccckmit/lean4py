# 導出範疇測試文檔 (test_derived_categories.py)

## 概述

本測試模組驗證 `lean4py.derived_categories` 模組中的導出範疇理論實現，涵蓋鏈複形、同倫範疇、三角範疇、穩定範疇及導出函子等核心概念。

---

## 1. 導出範疇 (Derived Category) 測試

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 基本對象創建，確認 `abelian_category` 為 `None`，對象列表為空 |
| `test_add_object` | 向導出範疇添加對象 |
| `test_hom_set` | 計算兩個對象之間的 hom 集合 |
| `test_is_localizing` | 驗證是否為局部化範疇 |
| `test_shift` | 測試对象的平移（shift）操作 |

### 數學原理

導出範疇 $D(\mathcal{A})$ 是由一個阿貝爾範疇 $\mathcal{A}$ 構造而來，其對象為鏈複形的同倫等價類，態射為局部化後的同倫類。導出範疇保留了原始範疇的同調代數結構，使得可計算 Ext 群和 Tor 群。

---

## 2. 同倫範疇 (Homotopy Category / Hot) 測試

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 確認同倫範疇的基本結構 |
| `test_homotopy_equivalence` | 驗證同倫等價關係（身份映射的複合） |
| `test_quasi_isomorphism` | 驗證擬同構（同調同構）的判定 |

### 數學原理

同倫範疇 $K(\mathcal{A})$ 將鏈複形的同倫等價類組織成範疇。若兩個鏈複形之間的態射在所有維度上誘導出同調群的同構，則稱其為**擬同構 (quasi-isomorphism)**。這是構造導出範疇的關鍵步驟。

---

## 3. 三角範疇 (Triangulated Category) 測試

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 驗證三角範疇的對象列表初始化 |
| `test_shift` | 測試平移函子 $\Sigma$ |
| `test_distinguished_triangle` | 驗證杰出三角的結構（5 個元素） |
| `test_octahedral_axiom` | 驗證八面體公理 |

### 數學原理

三角範疇是配備了平移函子 $\Sigma$ 和一族杰出三角的範疇，滿足：
- TR1: 映射錐存在
- TR2: 三角闭合於同構
- TR3: 複合映射的標準三角
- TR4: 八面體公理 — 確保了映射錐的兼容性

---

## 4. 穩定範疇 (Stable Category) 測試

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 驗證穩定範疇初始化 |
| `test_sphere` | 測試球面對象 $S^n$ 的構造 |
| `test_suspension` | 測試懸垂操作 $\Sigma X$ |

### 數學原理

穩定範疇來源於加法範疇，其平移函子具有逆函子。對於安定化範疇 $\underline{\mathcal{A}}$，對象的懸垂 $\Sigma X$ 對應於同倫論中空間的懸垂操作，滿足 $\Omega \Sigma X \cong X$（當穩定時）。

---

## 5. 導出函子 (Derived Functor) 測試

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 驗證源範疇與目標範疇 |
| `test_apply` | 測試函子作用於複形 |
| `test_is_left_derived` | 驗證是否為左導出函子 |
| `test_is_right_derived` | 驗證是否為右導出函子 |
| `test_is_exact` | 驗證導出函子的正合性 |

### 數學原理

導出函子 $LF$（左導出）或 $RF$（右導出）是將阿貝爾範疇的函子提升到導出範疇的標準方法：

- **左導出函子** $LF$: 使用左內射分解，適用於右正合函子
- **右導出函子** $RF$: 使用右投射分解，適用於左正合函子

---

## 6. RHom 與 Ext 群測試

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 驗證基礎環結構 |
| `test_compute` | 測試 $RHom(X, Y)$ 的計算 |
| `test_Ext_group` | 計算 $\text{Ext}^n(M, N)$ 群 |

### 數學原理

$RHom(X, Y)$ 是 Hom 的右導出函子，定義為：

$$RHom_{\mathcal{A}}(X, Y) = \text{Hom}_{D(\mathcal{A})}(X, Y)$$

Ext 群滿足 $\text{Ext}^n(M, N) \cong H^n(RHom(M, N))$，且當 $n > 0$ 時為阿貝爾群的offshoot。

---

## 7. 左/右導出函子 (Lf / Rf) 測試

### 測試內容

| 測試 | 函子 | 驗證 |
|-----|------|------|
| `test_apply` (Lf) | 左導出 | 作用於複形 |
| `test_apply` (Rf) | 右導出 | 作用於複形 |

### 數學原理

- **Lf (左導出)**: $Lf = L \circ F \circ \Gamma$，先取內射分解，再作用函子 $F$，最後取同調
- **Rf (右導出)**: $Rf = R \circ F \circ \Gamma$，先取投射分解，再作用函子 $F$，最後取同調

---

## 8. 撓積 (Torsion Product) 測試

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 驗證基礎環結構 |
| `test_compute` | 計算 $\text{Tor}_n^R(M, N)$ |

### 數學原理

$$\text{Tor}_n^R(M, N) = H_n(M \otimes_R^L N)$$

撓積是張量積的左導出函子，用於測量模的撓性質。當 $M$ 為平坦模時，$\text{Tor}_n^R(M, N) = 0$（對所有 $n > 0$）。

---

## 9. 同調複形 (HomologicalComplex) 測試

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 驗證模列表與微分映射 |
| `test_homology_at` | 計算指定維度的同調群 |

### 數學原理

同調複形 $(C_\bullet, d_\bullet)$ 滿足 $d_{n-1} \circ d_n = 0$。同調群定義為：

$$H_n(C) = \ker(d_n) / \text{im}(d_{n+1})$$

同調群測量了複形的「非精確程度」。

---

## 10. Connes 精確三角 (Connes Exact Triangle) 測試

### 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 驗證複形類型（如 Hochschild 上同調） |
| `test_periodicity_operator` | 計算週期性算子 |
| `test_is_exact_triangle` | 驗證是否為精確三角 |

### 數學原理

在循環同調理論中，Connes 精確三角來自於週期性雙複形。週期性算子 $S$ 將 Ext 群週期化：

$$\text{Ext}_{\Lambda}^n(A, B) \cong \text{Ext}_{\Lambda}^{n+2}(A, B)$$

---

## 測試覆蓋矩陣

| 類別 | 創建 | 計算 | 性質 | 公理 |
|------|:----:|:----:|:----:|:----:|
| DerivedCategory | ✓ | ✓ | ✓ | — |
| Hot | ✓ | — | ✓ | — |
| TriangulatedCategory | ✓ | ✓ | — | ✓ |
| StableCategory | ✓ | — | — | — |
| DerivedFunctor | ✓ | ✓ | ✓ | — |
| RHom | ✓ | ✓ | — | — |
| Lf/Rf | ✓ | ✓ | — | — |
| TorsionProduct | ✓ | ✓ | — | — |
| HomologicalComplex | ✓ | ✓ | — | — |
| ConnesExactTriangle | ✓ | ✓ | — | — |