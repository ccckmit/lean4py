# Scheme Theory 測試文檔

## 概述

本測試文件驗證 `lean4py.scheme_theory` 模組的核心功能，該模組模仿 mathlib4 的 `Mathlib.AlgebraicGeometry.Scheme`。測試涵蓋仿射格式、射影格式、格式態射、纖維積與 proper 態射。

---

## 1. 測試驗證的內容

這些測試確保 scheme theory 實現滿足以下數學性質：

| 類別 | 驗證內容 |
|------|----------|
| `AffineScheme` | 仿射格式的創建、Spec 建構、環的關聯 |
| `ProjectiveScheme` | 射影格式的維度、射影空間 ℙⁿ_R 的性質 |
| `SchemeMorphism` | 態射的連續性與合法性 |
| `FiberProduct` | 纖維積 X ×_Z Y 的計算 |
| `ProperMorphism` | proper 態射的判定與 valuation criterion |

---

## 2. 仿射格式測試 (TestAffineScheme)

### 數學原理

**仿射格式** (Affine Scheme) `Spec(R)` 是代數幾何中最基本的物件。對於交換環 `R`，`Spec(R)` 是 `R` 的所有素理想的集合，配備札托普斯基拓撲。

```python
class TestAffineScheme(unittest.TestCase):
    def test_creation(self):
        a = AffineScheme("Z")
        self.assertEqual(a.ring, "Z")
```

### 測試說明

| 測試 | 含義 |
|------|------|
| `test_creation` | 驗證 `AffineScheme("Z")` 正確存儲環 `Z`（整數環） |
| `test_spectrum` | 驗證 `Spec(Q)` 返回正確的字典結構，包含 `type: "affine_scheme"` |
| `test_is_affine` | 驗證 `is_affine()` 返回 `True`（仿射格式的基本性質） |

**核心概念**：
- `AffineScheme("Z")` 表示 `Spec(ℤ)`
- `spectrum()` 靜態方法構建 `Spec(R)`
- `is_affine()` 確認格式的仿射性

---

## 3. 射影格式測試 (TestProjectiveScheme)

### 數學原理

**射影格式** (Projective Scheme) ℙⁿ_R 是射影空間的格式化版本。射影空間 ℙⁿ 是 n 維射影幾何的基本空間，具有豐富的幾何性質（如 proper 性）。

```python
class TestProjectiveScheme(unittest.TestCase):
    def test_creation(self):
        p = ProjectiveScheme("Z", 2)
        self.assertEqual(p.dim, 2)
```

### 測試說明

| 測試 | 含義 |
|------|------|
| `test_creation` | 驗證 `ProjectiveScheme("Z", 2)` 正確存儲基環和維度 |
| `test_projective_space` | 驗證 `projective_space(3, "Z")` 返回射影空間結構 |
| `test_is_proper` | 驗證 `is_proper()` 返回 `True`（射影格式的核心性質） |

**核心概念**：
- 射影格式 ℙⁿ_R 的維度為 n
- `ProjectiveScheme("Z", 2)` 表示 ℙ²_ℤ（二維射影平面）
- 射影格式是 proper 的，這是其最重要性質之一

---

## 4. 格式態射測試 (TestSchemeMorphism)

### 數學原理

**格式態射** (Scheme Morphism) `f: X → Y` 是格式之間的結構保持映射。對於態射 `f`，需要滿足：
- 底層拓撲映射連續
- 結構層之間的環同態兼容

```python
class TestSchemeMorphism(unittest.TestCase):
    def test_creation(self):
        f = SchemeMorphism("X", "Y")
        self.assertEqual(f.source, "X")
```

### 測試說明

| 測試 | 含義 |
|------|------|
| `test_creation` | 驗證態射的源 (source) 和目標 (target) 正確存儲 |
| `test_is_continuous` | 驗證 `is_continuous()` 返回 `True`（拓撲連續性） |
| `test_is_morphism` | 驗證 `is_morphism()` 返回 `True`（格式態射合法性） |

**核心概念**：
- 態射 `f: X → Y` 的 source 為 X，target 為 Y
- 連續性：`|f|: |X| → |Y|` 在札托普斯基拓撲下連續
- `is_morphism()` 確認態射保持格式結構

---

## 5. 纖維積測試 (TestFiberProduct)

### 數學原理

**纖維積** (Fiber Product) X ×_Z Y 是格式範疇中的pullback。對於態射 f: X → Z 和 g: Y → Z，纖維積 X ×_Z Y 滿足泛性質：任何其他與 X、Y 的兼容性因子唯一分解到此積。

```
        X ×_Z Y
       /    \
      f      g
     /        \
    X    →    Y
      \      /
        Z
```

```python
class TestFiberProduct(unittest.TestCase):
    def test_compute(self):
        result = FiberProduct.compute("X", "Y", "Z", lambda x: x, lambda x: x)
        self.assertEqual(result["type"], "fiber_product")
```

### 測試說明

| 測試 | 含義 |
|------|------|
| `test_compute` | 驗證 `FiberProduct.compute()` 返回正確的纖維積結構 |

**核心概念**：
- 纖維積 X ×_Z Y 是範疇論中的 pullback
- `compute()` 方法接受兩個態射 f 和 g，返回纖維積
- 返回 `{"type": "fiber_product", "factors": [X, Y]}`

---

## 6. Proper 態射測試 (TestProperMorphism)

### 數學原理

**Proper 態射** 是代數幾何中最重要的態射類型之一。態射 `f: X → Y` 是 proper 的當且僅當：
1. 泛閉性 (Universally Closed)：對於任何基變換，f 都閉
2. 分離性 (Separated)：對角態射閉

Valuation criterion 提供了 properness 的純態射論判準。

```python
class TestProperMorphism(unittest.TestCase):
    def test_is_proper(self):
        f = SchemeMorphism("X", "Y")
        self.assertTrue(ProperMorphism.is_proper(f))

    def test_valuation_criterion(self):
        f = SchemeMorphism("X", "Y")
        self.assertTrue(ProperMorphism.valuation_criterion(f))
```

### 測試說明

| 測試 | 含義 |
|------|------|
| `test_is_proper` | 驗證 `is_proper()` 正確判斷態射是否 proper |
| `test_valuation_criterion` | 驗證 `valuation_criterion()` 實現了 properness 的 valuation 判準 |

**核心概念**：
- Proper 態射是緊緻性的推廣
- Valuation criterion：用於檢驗態射的 properness
- 射影格式之間的態射是 proper 的

---

## 7. Sheaf on Scheme 測試

**注意**：當前的 `test_scheme_theory.py` 沒有 sheaf 測試。Sheaf 相關測試位於獨立的測試文件中：

- `test_sheaf.py` - 層論基礎測試
- `test_sheaf_theory.py` - 完整層論測試
- `test_sheaf_extensions.py` - 層的擴展測試

層 (Sheaf) 是格式上的層論結構，用於描述局部-全局相容性。

---

## 測試覆蓋範圍總結

```
scheme_theory.py
├── AffineScheme        → Spec(R), is_affine()
├── ProjectiveScheme    → ℙⁿ_R, dim, is_proper()
├── SchemeMorphism      → f: X→Y, is_continuous(), is_morphism()
├── FiberProduct       → X ×_Z Y
└── ProperMorphism     → is_proper(), valuation_criterion()
```

---

## 數學背景

本模組對應 mathlib4 的 `Mathlib.AlgebraicGeometry.Scheme`，實現了現代代數幾何的基礎設施：

- **仿射格式**：局部可交換環譜
- **射影格式**：射影空間的格式化
- **態射理論**：格式之間的映射
- **纖維積**：範疇論 pullback 在代數幾何中的實現
- **Proper 態射**：緊緻性概念的推廣