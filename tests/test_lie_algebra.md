# Lie 代數測試文檔

本文檔說明 `test_lie_algebra.py` 中測試用例背後的數學原理。

## 1. 測試概述

本測試文件驗證 `lean4py.lie_algebra` 模組的核心功能，涵蓋李代數的基本結構、子代數、伴隨表示、通用包絡代數、根系統和經典李代數。

## 2. Lie 括號測試 (TestLieAlgebra)

### 數學原理

Lie 括號是李代數的核心運算，滿足：
- **反對稱性**: `[x, y] = -[y, x]`
- **Jacobi 恆等式**: `[x, [y, z]] + [y, [z, x]] + [z, [x, y]] = 0`
- **雙線性性**: `[ax + by, z] = a[x, z] + b[y, z]`

### 測試案例

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 李代數的基本創建，確認 name 和 dimension 屬性正確 |
| `test_default_basis` | 預設基底的維度與宣告一致 |
| `test_bracket_of_basis` | 基底元素的 Lie 括號計算返回三維向量 |
| `test_is_abelian` | Abel 李代數的判定：所有 Lie 括號均為零 |
| `test_is_lie_algebra` | 驗證所定義運算構成合法的李代數 |

**零括號示例**（構成 Abel 李代數）：
```python
def zero_bracket(x, y):
    return [0.0, 0.0, 0.0]
```

## 3. Jacobi 恆等式測試

### 數學原理

Jacobi 恆等式是李代數的定義公理之一，確保了伴隨表示的導數性質：

```
[x, [y, z]] + [y, [z, x]] + [z, [x, y]] = 0
```

這反映了三代數運算的結合性質，是李群和牛頓-萊布尼茨公式的基礎。

### 與伴隨表示的關係

測試中的 `AdjointRepresentation` 類計算：
- `ad_x(y) = [x, y]`
- 這是李代數的導數，滿足導數的 Leibniz 規則

## 4. 子代數與理想測試 (TestLieSubalgebra)

### 數學原理

**子代數 (Subalgebra)**：封閉於 Lie 括號的向量空間子空間
- 若 I, J ∈ subalgebra，則 [I, J] ∈ subalgebra

**理想 (Ideal)**：更強的條件，封閉於左作用
- 若 I ∈ ideal，則對所有 x ∈ L，有 [x, I] ∈ I
- 理想是同態核的預像，是正規子群的李代數類比

### 測試案例

```python
# 零括號構成任意子空間都是理想
def zero_bracket(x, y):
    return [0.0] * 3
la = LieAlgebra("test", 3, zero_bracket)
sub = LieSubalgebra(la, {0, 1})  # 二維子空間
assert sub.is_ideal() is True
```

## 5. 伴隨表示與 Killing 形式測試 (TestAdjointRepresentation)

### 數學原理

**伴隨表示 (Adjoint Representation)**：
- 對每個 x ∈ L，定義線性變換 ad_x: L → L
- `ad_x(y) = [x, y]`
- 這是 L 到 gl(L) 的 Lie 代數同態

**Killing 形式**：
- `K(x, y) = Tr(ad_x ∘ ad_y)`
- 是對稱雙線性形式
- 用於判斷半單李代數的結構
- Cartan 準則：一個李代數是半單的當且僅當其 Killing 形式非退化

### 測試案例

```python
def bracket(x, y):
    return [0.0, y[0] - x[0], 0.0]
la = LieAlgebra("test", 3, bracket)
ad = AdjointRepresentation(la)
result = ad.killing_form([1, 0, 0], [0, 1, 0])  # 返回標量
```

## 6. 可解性與冪零性測試

### 數學原理

**導來列 (Derived Series)**：
- L^(0) = L
- L^(1) = [L, L]
- L^(n+1) = [L^(n), L^(n)]

**下中心的列 (Lower Central Series)**：
- L^1 = L
- L^2 = [L, L^1]
- L^(n+1) = [L, L^n]

**可解 (Solvable)**：存在 n 使得 L^(n) = 0
**冪零 (Nilpotent)**：存在 n 使得 L^n = 0

每個冪零李代數都是可解的，反之不一定成立。

## 7. Killing 形式測試

### 數學原理

Killing 形式 `K(x, y) = Tr(ad_x ad_y)` 的重要性：

1. **Cartan 判準**：
   - 李代數半單 ⟺ Killing 形式非退化
   - 李代數可解 ⟺ Killing 形式在導來代數上為零

2. **結構分析**：
   - Killing 形式在中心上恆為零
   - 半單李代數的 Killing 形式非退化

3. **根系與 Dynkin 圖**：
   - Killing 形式用於定義根系中根長
   - 決定 Dynkin 圖的結構

## 8. 根系統測試 (TestRootSystem)

### 數學原理

根系統是半單李代數結構的核心：

- **秩 (Rank)**：根系中最大線性無關根的數目
- **單根 (Simple Roots)**：一組基元素，其他根可表示為其整數組合
- **Cartan 矩陣**：描述單根之間的角度關係

### Cartan 矩陣元素

```python
rs = RootSystem(2, [[1, 0], [0, 1]], [[2, -1], [-1, 2]])
rs.cartan_matrix_element(0, 0)  # = 2
rs.cartan_matrix_element(0, 1)  # = -1
```

Cartan 矩陣元素 `A_ij = 2(α_i, α_j) / (α_j, α_j)` 決定了李代數的分類。

## 9. Serre 關係測試

### 數學原理

Serre 定理：每個根系決定一個唯一的半單李代數。

從根系出發，通過 Serre 關係：
- `ad(e_i)^(1 - A_ij)(e_j) = 0`（對 i ≠ j）
- `ad(f_i)^(1 - A_ij)(f_j) = 0`
- `[e_i, f_j] = δ_ij h_i`

這些關係定義了 Kac-Moody 代數的有限維情形。

## 10. 經典李代數測試 (TestStandardLieAlgebras)

### 數學原理

| 李代數 | 矩陣形式 | 維度 | 根系 |
|--------|---------|------|------|
| **sl₂** | traceless 2×2 矩陣 | 3 | A₁ |
| **gl₂** | 全部 2×2 矩陣 | 4 | A₁ |

**sl₂ 的結構**：
- 基底：{e, f, h}
- 關係：[h, e] = 2e, [h, f] = -2f, [e, f] = h
- 这是最簡單的非交換單李代數

**gl₂ 的結構**：
- = sl₂ ⊕ 純量矩陣
- 維度為 4（比 sl₂ 多一維中心）

## 11. 通用包絡代數測試 (TestUniversalEnvelopingAlgebra)

### 數學原理

通用包絡代數 U(L) 是結合代數，包含 L 作为其子空間：
- 泛性質：對任意結合代數 A 和 Lie 代數同態 φ: L → A，存在唯一代數同態 ψ: U(L) → A
- PBW 定理：U(L) 的基底由單項式 e₁^(n₁) e₂^(n₂)... 給出
- 無限維：除非 L 是 Abel 的，否則 U(L) 無限維

```python
def bracket(x, y):
    return [0.0] * 2
la = LieAlgebra("test", 2, bracket)
uea = UniversalEnvelopingAlgebra(la)
uea.dimension()  # 返回 -1（表示無限維）
```

## 12. 總結

這些測試驗證了李代數模組的以下核心能力：

| 類別 | 測試內容 |
|------|---------|
| 基本結構 | 創建、基底、維度 |
| 代數結構 | Abel 性、Lie 代數判定 |
| 子結構 | 子代數、理想 |
| 表示論 | 伴隨表示、Killing 形式 |
| 分類理論 | 根系統、Cartan 矩陣、Serre 關係 |
| 經典例子 | sl₂、gl₂ |
| 包絡代數 | 通用包絡代數構造 |