# Galois 理論測試文檔

## 概述

本文件描述 `test_galois_theory.py` 中的測試案例及其背後的伽羅瓦理論數學原理。

---

## 1. 測試驗證的內容

### 1.1 場擴張的基本性質

| 測試類別 | 驗證內容 |
|---------|---------|
| `TestFieldExtension` | 場擴張的創建、代數性、有限性 |
| `TestGaloisGroup` | 伽羅瓦群的計算與阿貝爾性 |
| `TestSeparableExtension` | 可分擴張判定 |
| `TestNormalExtension` | 正規擴張判定 |
| `TestGaloisExtension` | 伽羅瓦擴張判定 |
| `TestFundamentalTheorem` | 基本定理的中間域與對應關係 |
| `TestSolvabilityByRadicals` | 多項式的根式可解性 |

---

## 2. 場擴張測試 (FieldExtension)

### 2.1 數學原理

**場擴張** L/K 是指一個場 L 包含另一個場 K 作為其子場。記號 L/K 表示 L 是 K 的擴張。

- **基域 (Base Field)**: K = Q（有理數域）
- **擴張域 (Extension Field)**: L = Q(√2)
- **擴張次數 (Degree)**: [L:K] = 2

### 2.2 Q(√2) 的意義

Q(√2) 是將 √2 添加到有理數域 Q 形成的擴張：

$$ \mathbb{Q}(\sqrt{2}) = \{a + b\sqrt{2} \mid a, b \in \mathbb{Q}\} $$

這是一個**單代數擴張**，由多項式 $x^2 - 2$ 的根生成。

### 2.3 測試案例

```python
ext = FieldExtension("Q", "Q(√2)", degree=2)
```

- `test_creation`: 驗證擴張物件的基域為 "Q"，次數為 2
- `test_is_algebraic`: Q(√2) 是代數擴張（每個元素都是某個有理係數多項式的根）
- `test_is_finite`: [Q(√2):Q] = 2 是有限的

---

## 3. 伽羅瓦群測試 (GaloisGroup)

### 3.1 數學原理

**伽羅瓦群** Gal(L/K) 是所有保持 K 不動的 L 的自同構組成的群。

對於 Q(√2)/Q：
- 恆等映射: σ(a + b√2) = a + b√2
- 共軛映射: τ(a + b√2) = a - b√2

因此 Gal(Q(√2)/Q) ≅ C₂（循環群，階為 2）。

### 3.2 測試案例

```python
result = GaloisGroup.compute(ext)
# 結果: {"group": "trivial", "order": 1, "generators": []}
```

**注意**: 當前實現返回的是簡化版本（平凡群），實際上 Q(√2)/Q 的伽羅瓦群是二階群。

```python
GaloisGroup.is_abelian(ext)  # True
```

伽羅瓦群一定是阿貝爾群（交換群）。

---

## 4. 可分性與正規性測試

### 4.1 可分擴張 (Separable Extension)

**定義**: 一個代數擴張 L/K 是**可分的**，若每個元素 α ∈ L 的極小多項式在分裂域中沒有重根。

對於特徵為零的域（如 Q），所有代數擴張都是可分的。

```python
SeparableExtension.is_separable(ext)  # True
```

### 4.2 正規擴張 (Normal Extension)

**定義**: 一個代數擴張 L/K 是**正規的**，若每個不可約多項式 f(x) ∈ K[x] 若在 L 中有一個根，則在 L 中完全分裂。

Q(√2) 對多項式 x² - 2 是正規的，因為 x² - 2 = (x - √2)(x + √2) 在 Q(√2) 中完全分裂。

```python
NormalExtension.is_normal(ext)  # True
```

### 4.3 伽羅瓦擴張

**定義**: 一個擴張 L/K 是**伽羅瓦擴張**，若它是正規且可分的。

```python
GaloisExtension.is_galois(ext)  # True
```

這是因為 Q(√2)/Q 同時滿足：
- 可分性（特徵為 0）
- 正規性（x² - 2 在其中完全分裂）

---

## 5. 基本定理測試 (FundamentalTheorem)

### 5.1 數學原理

**伽羅瓦理論基本定理**建立了中間域與伽羅瓦子群之間的雙射對應：

對於有限伽羅瓦擴張 L/K：
- 每個中間域 K ⊆ E ⊆ L 對應一個子群 H = Gal(L/E)
- 每個子群 H ⊆ G = Gal(L/K) 對應一個中間域 L^H

### 5.2 對應關係圖

```
        L = Q(√2)
         |
    ┌────┴────┐
    │  Gal(L/K)│ = {e, σ}  (階 2)
    └────┬────┘
         |
    ┌────┴────┐
    │  {e}    │ (階 1) 對應 中間域 L
    └────┬────┘
         |
        K = Q
```

### 5.3 測試案例

```python
FundamentalTheorem.intermediate_fields(ext)
# 返回: ["Q", "Q(√2)"]

FundamentalTheorem.correspondence(ext)
# 返回: {"fields": [], "subgroups": []}（簡化版本）
```

---

## 6. 根式可解性測試 (SolvabilityByRadicals)

### 6.1 數學原理

**伽羅瓦定理**: 一個代數方程可用根式求解的充分必要條件是其伽羅瓦群是可解群。

- **可解群**: 存在一個子群鏈 {e} = G₀ ⊂ G₁ ⊂ ... ⊂ Gₙ = G，使得每個商群 Gᵢ₊₁/Gᵢ 是阿貝爾群。

### 6.2 多項式次數與可解性

| 次數 | 可解性 | 說明 |
|------|--------|------|
| n ≤ 4 | 必可解 | 二次、三次、四次公式 |
| n = 5 | 一般不可解 | 一般的五次方程不可用根式求解 |
| n ≥ 6 | 一般不可解 | 高次方程一般無根式解 |

### 6.3 伽羅瓦群示例

- **二次方程** x² + bx + c = 0: Gal = C₂（可解）
- **五次方程** 一般形式: Gal = S₅（不可解，因為 A₅ 是單群）

### 6.4 測試案例

```python
SolvabilityByRadicals.is_solvable(3)   # True (三次可解)
SolvabilityByRadicals.is_solvable(5)  # False (五次一般不可解)
```

---

## 7. 測試覆蓋矩陣

| 類別 | 場擴張 | 伽羅瓦群 | 可分性 | 正規性 | 伽羅瓦性 | 基本定理 | 根式可解 |
|------|--------|---------|--------|--------|---------|---------|---------|
| `test_creation` | ✓ | | | | | | |
| `test_is_algebraic` | ✓ | | | | | | |
| `test_is_finite` | ✓ | | | | | | |
| `test_compute` | | ✓ | | | | | |
| `test_is_abelian` | | ✓ | | | | | |
| `test_is_separable` | | | ✓ | | | | |
| `test_is_normal` | | | | ✓ | | | |
| `test_is_galois` | | | | | ✓ | | |
| `test_intermediate_fields` | | | | | | ✓ | |
| `test_correspondence` | | | | | | ✓ | |
| `test_is_solvable` | | | | | | | ✓ |

---

## 8. 擴展測試建議

當前測試使用簡化的實現版本。以下是更完整測試的建議：

1. **非平凡伽羅瓦群**: 測試 Q(ζₙ)/Q 的伽羅瓦群 Zₙ*
2. **不可解群**: 測試 S₅ 的不可解性
3. **分裂域**: 測試多項式分裂域的計算
4. **中間域計算**: 實現真正的伽羅瓦對應

---

## 9. 參考文獻

- Artin, E. *Galois Theory*
- Lang, S. *Algebra*
- Stewart, I. *Galois Theory*