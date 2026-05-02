# 單胚類別（Monoidal Categories）測試文檔

## 概述

本測試文件驗證單胚類別及其相關結構的數學性質。單胚類別是帶有張量積運算的類別，推廣了集合的乘積和向量空間的張量積等概念。

---

## 1. 測試驗證的內容

### 1.1 單胚類別基本性質

| 測試類別 | 驗證內容 |
|---------|---------|
| `TestMonoidalCategory` | 單胚類別的基本結構：對象管理、單位對象、結合子、左單位子、右單位子 |
| `TestSymmetricMonoidalCategory` | 對稱單胚類別：編織映射、對稱性、六邊形恆等式 |
| `TestClosedMonoidalCategory` | 封閉單胚類別：內部同態對象、評估映射、 curry 化 |
| `TestBraidedMonoidalCategory` | 編織單胚類別：兩個六邊形恆等式 |

### 1.2 核心不變量

- **單位對象 (Unit Object)**：記為 `I`，是張量積的單位元
- **結合子 (Associator)**：α: (A⊗B)⊗C → A⊗(B⊗C)
- **左單位子 (Left Unitor)**：λ: I⊗A → A
- **右單位子 (Right Unitor)**：ρ: A⊗I → A

---

## 2. 張量積測試 (Tensor Product)

### 2.1 數學原理

張量積是單胚類別的核心運算。對於類別 C 中的對象 A 和 B，張量積 A⊗B 仍是該類別的對象。

**基本要求**：
- 存在單位對象 I，使得 I⊗A ≅ A ≅ A⊗I
- 張量積誘導出態射的張量積：若 f: A → A', g: B → B'，則 f⊗g: A⊗B → A'⊗B'

### 2.2 測試案例

```python
# test_tensor_product: 驗證 A ⊗ B = "A⊗B"
mc = MonoidalCategory()
result = mc.tensor_product("A", "B")
assert result == "A⊗B"

# test_tensor_of_morphisms: 驗證態射的張量積
f = lambda x: x + 1
g = lambda x: x * 2
h = mc.tensor_of_morphisms(f, g)
assert h(5) == (6, 10)  # f(5)=6, g(5)=10
```

### 2.3 剛性類別 (Rigid Category) 中的對偶

剛性類別中的每個對象都有對偶對象：

| 映射 | 類型 | 測試 |
|------|------|------|
| 對偶對象 | A ↦ A* | `test_dual_of`, `test_set_dual` |
| 評估映射 | A* ⊗ A → I | `test_evaluation` |
| 餘評估映射 | I → A ⊗ A* | `test_coevaluation` |

---

## 3. 結合性測試 (Associativity)

### 3.1 數學原理

結合子是一個自然同構：

```
α_A,B,C : (A ⊗ B) ⊗ C → A ⊗ (B ⊗ C)
```

**MacLane  coherence 條件**：五個多面體圖必須交換，包括：
- 結合子本身是自然的
- 左右單位子與結合子的相容性
- 結合子的四角化性質

### 3.2 測試案例

```python
# test_associator: 驗證結合子返回恆等態射
mc = MonoidalCategory()
alpha = mc.associator("A", "B", "C")
assert alpha("test") == "test"  # 身份結合子
```

### 3.3 單位子測試

```python
# test_left_unitor: λ_A: I ⊗ A → A
lam = mc.left_unitor("A")
assert lam("x") == "x"

# test_right_unitor: ρ_A: A ⊗ I → A
rho = mc.right_unitor("A")
assert rho("x") == "x"
```

---

## 4. 編織測試 (Braiding)

### 4.1 數學原理

編織是單胚類別中的自然同構：

```
σ_A,B : A ⊗ B → B ⊗ A
```

**對稱單胚類別**額外要求 σ_{B,A} ∘ σ_{A,B} = id，即編織是對合的。

**六邊形恆等式**（對稱/編織單胚類別的基本條件）：

```
六邊形 1:
(I ⊗ σ_{A,B}) ∘ ρ_A ⊗ B = λ_B ∘ σ_{A,I} ⊗ B

六邊形 2:
(σ_{A,C} ⊗ I) ∘ ρ_A ⊗ C = ...
```

### 4.2 測試案例

```python
# test_braiding: 默認編織是恆等態射
smc = SymmetricMonoidalCategory()
sigma = smc.braiding("A", "B")
assert sigma("x") == "x"

# test_set_braiding: 自定義編織映射
smc.set_braiding("A", "B", lambda x: f"braided({x})")
assert smc.braiding("A", "B")("x") == "braided(x)"

# test_hexagon_identity: 驗證六邊形恆等式
assert smc.hexagon_identity() is True

# 編織單胚類別的兩個六邊形
bmc = BraidedMonoidalCategory()
assert bmc.hexagon_1() is True
assert bmc.hexagon_2() is True
```

---

## 5. 封閉性測試 (Closedness)

### 5.1 數學原理

封閉單胚類別具有內部同態對象 [A, B]，使得：

```
Hom(A ⊗ B, C) ≅ Hom(B, [A, C])
```

這推廣了向量空間的對偶性。

### 5.2 測試案例

```python
# test_internal_hom_object: 內部同態對象
cmc = ClosedMonoidalCategory()
ih = cmc.internal_hom_object("A")
assert "A" in ih

# test_currying: curry 化
f = lambda x, y: x + y
curried = cmc.currying(f)
assert curried(2)(3) == 5
```

---

## 6. 函子測試

### 6.1 單胚函子

單胚函子 F: C → D 保持張量積結構：

```
F(A ⊗ B) ≅ F(A) ⊗ F(B)
F(I) ≅ I
```

### 6.2 測試案例

```python
# test_preserves_tensor: 驗證函子保持張量積
mf = MonoidalFunctor(source, target, lambda x: x, lambda f: f)
assert mf.preserves_tensor() is True

# Lax 單胚函子：有自然變換而非相等
lmf = LaxMonoidalFunctor(source, target, lambda x: x)
assert lmf.unit_constraint()("x") == "x"
```

---

## 7. 額外結構

| 結構 | 描述 | 測試類別 |
|------|------|---------|
| **笛卡爾單胚** | 張量積為範疇論積 ×，單位為終對象 1 | `TestCartesianMonoidalCategory` |
| **餘笛卡爾單胚** | 張量積為餘積 ⊕，單位為初始對象 0 | `TestCoCartesianMonoidalCategory` |
| **豐富類別** | Hom-對象是基類別中的對象 | `TestEnrichedCategory` |

---

## 8. 數學術語對照

| 中文 | 英文 | 符號 |
|------|------|------|
| 單胚類別 | Monoidal Category | C |
| 張量積 | Tensor Product | ⊗ |
| 單位對象 | Unit Object | I |
| 結合子 | Associator | α |
| 左單位子 | Left Unitor | λ |
| 右單位子 | Right Unitor | ρ |
| 編織 | Braiding | σ |
| 對偶對象 | Dual Object | A* |
| 內部同態 | Internal Hom | [A, B] |