# 代數結構模組 (algebra.py) 數學原理文檔

## 1. 概述

本模組實現了代數結構的層次體系，從基本的二元運算封閉性到場的完整定義。這一體系遵循抽象代數的標準層級結構，每一層級都在前一層級的基礎上增加新的代數性質。

## 2. 代數結構層級體系

```
Magma → Semigroup → Monoid → Group → AbelianGroup
                                       ↓
                                      Ring
                                       ↓
                                     Field
```

### 2.1 層級之間的關係

| 結構 | 額外性質 | 符號表示 |
|------|----------|----------|
| Magma | 封閉性 | (S, ·) |
| Semigroup | 結合律 | (S, ·) |
| Monoid | 單位元 | (S, ·, e) |
| Group | 逆元 | (S, ·, e, ⁻¹) |
| AbelianGroup | 交換律 | (S, +, 0, −) |
| Ring | 額外乘法半群 + 分配律 | (R, +, 0, −, ×, 1) |
| Field | 非零元乘法群 | (F, +, 0, −, ×, 1, ⁻¹) |

## 3. 結構性質詳解

### 3.1 封閉性 (Closure)

**定義**：對於集合 S 上的二元運算 ·，若對所有 a, b ∈ S 都有 a · b ∈ S，則運算在 S 上封閉。

**驗證方法** (`is_closed`)：
```python
def is_closed(self) -> bool:
    for a in self.carrier:
        for b in self.carrier:
            if self.op(a, b) not in self.carrier:
                return False
    return True
```

**意義**：封閉性是所有其他代數結構的基礎，確保二元運算的結果仍在定義域內。

### 3.2 結合律 (Associativity)

**定義**：運算 · 滿足結合律當且僅當對所有 a, b, c ∈ S：
(a · b) · c = a · (b · c)

**驗證方法** (`is_associative`)：
```python
def is_associative(self) -> bool:
    for a in self.carrier:
        for b in self.carrier:
            for c in self.carrier:
                if self.op(self.op(a, b), c) != self.op(a, self.op(b, c)):
                    return False
    return True
```

**意義**：結合律允許我們忽略表達式的括號順序，例如 (a + b) + c = a + (b + c)。

### 3.3 單位元 (Identity Element)

**定義**：元素 e ∈ S 是運算 · 的單位元當且僅當對所有 a ∈ S：
e · a = a · e = a

**驗證方法** (`has_identity`)：
```python
def has_identity(self) -> bool:
    if self.identity is None:
        return False
    for a in self.carrier:
        if self.op(self.identity, a) != a or self.op(a, self.identity) != a:
            return False
    return True
```

**意義**：單位元是代數結構中的「中性元素」，如加法中的 0，乘法中的 1。

### 3.4 逆元 (Inverse Element)

**定義**：對於群 (G, ·, e, ⁻¹)，每個元素 a ∈ G 都有逆元 a⁻¹ ∈ G，使得：
a · a⁻¹ = a⁻¹ · a = e

**驗證方法** (`has_inverses`)：
```python
def has_inverses(self) -> bool:
    if self.inv is None or self.identity is None:
        return False
    for a in self.carrier:
        if self.op(a, self.inv(a)) != self.identity:
            return False
    return True
```

**意義**：逆元允許「撤銷」操作的概念，是群論的核心特性。

### 3.5 交換律 (Commutativity / Abelian)

**定義**：運算 · 滿足交換律當且僅當對所有 a, b ∈ S：
a · b = b · a

**驗證方法** (`is_abelian`)：
```python
def is_abelian(self) -> bool:
    for a in self.carrier:
        for b in self.carrier:
            if self.op(a, b) != self.op(b, a):
                return False
    return True
```

**意義**：交換律表明元素的順序不影響運算結果，如普通加法和乘法。

## 4. 代數結構類型

### 4.1 Magma（胚群）

**定義**：集合 S 配上封閉的二元運算 ·，記作 (S, ·)。

**要求**：
- 封閉性：∀a, b ∈ S, a · b ∈ S

**程式碼實現**：
```python
class Magma(AlgebraicStructure):
    def __init__(self, name: str, carrier: set, op: Callable):
        super().__init__(name, carrier, op)
```

**例子**：整數減法 (ℤ, −) 形成一個 Magma，但不是 Semigroup（不滿足結合律）。

### 4.2 Semigroup（半群）

**定義**：滿足結合律的 Magma，記作 (S, ·)。

**要求**：
- 封閉性：✓
- 結合律：∀a, b, c ∈ S, (a · b) · c = a · (b · c)

**驗證方法** (`is_semigroup`)：
```python
def is_semigroup(self) -> bool:
    return self.is_closed() and self.is_associative()
```

**例子**：
- 字元串連接 (Σ*, concat)
- 矩陣乘法 Mₙ(ℝ)
- 自然數加法 (ℕ, +)

### 4.3 Monoid（含幺半群）

**定義**：帶有單位元的 Semigroup，記作 (S, ·, e)。

**要求**：
- 是 Semigroup：✓
- 單位元存在：∃e ∈ S, ∀a ∈ S, e · a = a · e = a

**驗證方法** (`is_monoid`)：
```python
def is_monoid(self) -> bool:
    return self.is_semigroup() and self.has_identity()
```

**例子**：
- (ℕ, +, 0) - 自然數加法幺半群
- (Σ*, concat, ε) - 字元串連接幺半群
- (Mₙ(ℝ), ×, I) - n 階實矩陣乘法幺半群

### 4.4 Group（群）

**定義**：每個元素都有逆元的 Monoid，記作 (G, ·, e, ⁻¹)。

**要求**：
- 是 Monoid：✓
- 逆元存在：∀a ∈ G, ∃a⁻¹ ∈ G, a · a⁻¹ = a⁻¹ · a = e

**驗證方法** (`is_group`)：
```python
def is_group(self) -> bool:
    return self.is_monoid() and self.has_inverses()
```

**例子**：
- (ℤ, +, 0, −) - 整數加法群
- (ℝ\{0}, ×, 1, 1/x) - 非零實數乘法群
- Sₙ - n 階對稱群（置換群）

### 4.5 AbelianGroup（阿貝爾群/交換群）

**定義**：運算可交換的群，記作 (G, +, 0, −)。

**要求**：
- 是 Group：✓
- 交換律：∀a, b ∈ G, a + b = b + a

**驗證方法** (`is_abelian_group`)：
```python
def is_abelian_group(self) -> bool:
    return self.is_group() and self.is_abelian()
```

**例子**：
- (ℤ, +, 0, −) - 整數加法群（阿貝爾）
- (ℝⁿ, +, 0, −) - n 維實向量空間

### 4.6 Ring（環）

**定義**：具有兩種運算（加法和乘法）的代數結構，記作 (R, +, 0, −, ×, 1)。

**要求**：
- (R, +, 0, −) 是阿貝爾群
- (R, ×) 是半群
- 乘法對加法滿足分配律：
  - 左分配律：a × (b + c) = a × b + a × c
  - 右分配律：(a + b) × c = a × c + b × c

**驗證方法** (`is_ring`)：
```python
def is_ring(self) -> bool:
    if not self.is_abelian_group():
        return False
    if not self.is_closed_under(self.mul):
        return False
    if not self.is_associative_under(self.mul):
        return False
    return self.is_left_distributive() and self.is_right_distributive()
```

**分配律驗證**：
```python
def is_left_distributive(self) -> bool:
    for a in self.carrier:
        for b in self.carrier:
            for c in self.carrier:
                if self.mul(a, self.op(b, c)) != self.op(self.mul(a, b), self.mul(a, c)):
                    return False
    return True

def is_right_distributive(self) -> bool:
    for a in self.carrier:
        for b in self.carrier:
            for c in self.carrier:
                if self.mul(self.op(a, b), c) != self.op(self.mul(a, c), self.mul(b, c)):
                    return False
    return True
```

**例子**：
- (ℤ, +, 0, −, ×, 1) - 整數環
- (ℝ[x], +, 0, −, ×, 1) - 多項式環
- Mₙ(ℝ) - 矩陣環

### 4.7 Field（域）

**定義**：乘法運算滿足交換律且非零元素構成阿貝爾群的環，記作 (F, +, 0, −, ×, 1, ⁻¹)。

**要求**：
- 是 Ring：✓
- (F\{0}, ×, 1, ⁻¹) 是阿貝爾群（即乘法交換、封閉、結合、有單位元、有逆元）

**驗證方法** (`is_field`)：
```python
def is_field(self) -> bool:
    if not self.is_ring():
        return False
    if self.mul_id is None:
        return False
    for a in self.carrier:
        if a == self.identity:  # 排除加法單位元（零元）
            continue
        if self.mul_inv(a) not in self.carrier:
            return False
    return True
```

**例子**：
- (ℚ, +, 0, −, ×, 1, ⁻¹) - 有理數域
- (ℝ, +, 0, −, ×, 1, ⁻¹) - 實數域
- (ℂ, +, 0, −, ×, 1, ⁻¹) - 複數域

## 5. 驗證方法總覽

| 方法 | 驗證內容 | 適用結構 |
|------|----------|----------|
| `is_closed()` | 二元運算封閉性 | 所有結構 |
| `is_associative()` | 結合律 a·(b·c) = (a·b)·c | Semigroup+ |
| `has_identity()` | 單位元存在性 e·a = a·e = a | Monoid+ |
| `has_inverses()` | 逆元存在性 a·a⁻¹ = e | Group+ |
| `is_abelian()` | 交換律 a·b = b·a | AbelianGroup |
| `is_semigroup()` | Magma + 結合律 | Semigroup |
| `is_monoid()` | Semigroup + 單位元 | Monoid |
| `is_group()` | Monoid + 逆元 | Group |
| `is_abelian_group()` | Group + 交換律 | AbelianGroup |
| `is_ring()` | AbelianGroup + 半群 + 分配律 | Ring |
| `is_field()` | Ring + 非零元乘法群 | Field |

## 6. 類層級設計

```
AlgebraicStructure (基類，含 is_closed, is_associative, has_identity, has_inverses, is_abelian)
    │
    ├── Magma (封閉二元運算)
    │       │
    │       └── Semigroup (結合律)
    │               │
    │               └── Monoid (單位元)
    │                       │
    │                       └── Group (逆元)
    │                               │
    │                               └── AbelianGroup (交換律)
    │                                       │
    │                                       └── Ring (加法群 + 乘法半群 + 分配律)
    │                                               │
    │                                               └── Field (非零元乘法群)
```

## 7. 數學意義

### 7.1 為何需要這樣的層級結構？

代數結構的層級設計反映了數學抽象化的一般原則：

1. **逐步增加性質**：從最基礎的封閉性開始，逐步添加結合律、單位元、逆元、交換律，形成越來越豐富的代數結構。

2. **理論統一性**：不同領域的數學對象（如數、矩陣、多項式）可能共享相同的代數結構，這使得統一理論成為可能。

3. **分類完整性**：每個層級的結構都有其明確的數學意義和應用場景。

### 7.2 重要定理簡述

- **群的基本定理**：每個有限群同構於某個置換群的子群（凱萊定理）。

- **環的結構定理**：每個域都是整環的推廣，每個整環可以嵌入某個域。

- **域的特徵**：域的特徵要么是素數，要么是 0（如 ℚ, ℝ, ℂ）。

## 8. 使用範例

```python
from lean4py.algebra import Group, AbelianGroup, Ring, Field

# 整數加法群
Z_add = Group(
    name="整數加法群",
    carrier=set(range(-10, 11)),
    op=lambda a, b: a + b,
    identity=0,
    inv=lambda a: -a
)
print(Z_add.is_group())  # True

# 有理數域
Q = Field(
    name="有理數域",
    carrier={Fraction(a, b) for a in range(-5, 6) for b in range(1, 6)},
    add=lambda a, b: a + b,
    add_id=Fraction(0),
    add_inv=lambda a: -a,
    mul=lambda a, b: a * b,
    mul_id=Fraction(1),
    mul_inv=lambda a: Fraction(1) / a
)
print(Q.is_field())  # True
```