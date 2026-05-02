# 集合論 (Set Theory) 數學原理文檔

## 概述

本文檔說明 `lean4py/sets.py` 模組背後的集合論數學原理。該模組實現了有限集合的基本操作，支援集合的創建、交集、聯集、差集、補集、子集判斷、笛卡爾積、冪集、對稱差集等運算。

---

## 1. 集合論基礎

### 1.1 集合與元素

**數學定義**：集合是由確定、互異的對象組成的整體。這些對象稱為集合的**元素**（element）。

- 若元素 $a$ 屬於集合 $A$，記為 $a \in A$
- 若元素 $a$ 不屬於集合 $A$，記為 $a \notin A$

**實現**：`Set` 類使用 Python 的 `set` 來存儲元素，確保元素的唯一性和確定性。

```python
# 集合 A = {1, 2, 3}
A = Set([1, 2, 3])

# 檢查元素是否屬於集合
in_(2, A)  # True
```

### 1.2 集合的表示

- **枚舉法**：列出所有元素，如 $A = \{1, 2, 3\}$
- **描述法**：用性質描述，如 $B = \{x \mid x \text{ 是偶數}\}$

**實現**：`__repr__` 方法將集合顯示為 `{元素1, 元素2, ...}` 的形式。

```python
A = Set([1, 2, 3])
print(A)  # {1, 2, 3}

empty_set()  # 顯示為 ∅
```

---

## 2. 基本集合運算

### 2.1 聯集 (Union)

**數學定義**：$A \cup B = \{x \mid x \in A \text{ 或 } x \in B\}$

兩個集合的聯集包含所有屬於至少一個集合的元素。

**實現**：

```python
def union(s1: Set, s2: Set) -> Set:
    return Set(s1._elems | s2._elems)
```

**運算符**：使用 `+` 或 `__add__` 方法

```python
A = Set([1, 2, 3])
B = Set([3, 4, 5])
A + B  # {1, 2, 3, 4, 5}
```

### 2.2 交集 (Intersection)

**數學定義**：$A \cap B = \{x \mid x \in A \text{ 且 } x \in B\}$

兩個集合的交集包含所有同時屬於兩個集合的元素。

**實現**：

```python
def intersection(s1: Set, s2: Set) -> Set:
    return Set(s1._elems & s2._elems)
```

**運算符**：使用 `*` 或 `__mul__` 方法

```python
A = Set([1, 2, 3])
B = Set([3, 4, 5])
A * B  # {3}
```

### 2.3 差集 (Difference)

**數學定義**：$A - B = \{x \mid x \in A \text{ 且 } x \notin B\}$

從集合 A 中移除所有屬於集合 B 的元素。

**實現**：

```python
def difference(s1: Set, s2: Set) -> Set:
    return Set(s1._elems - s2._elems)
```

**運算符**：使用 `-` 或 `__sub__` 方法

```python
A = Set([1, 2, 3])
B = Set([2, 3, 4])
A - B  # {1}
```

### 2.4 補集 (Complement)

**數學定義**：$\overline{A} = U - A$，其中 $U$ 是全集（論域）

補集是相對於全集而言的。`sets.py` 要求明確指定全集。

**實現**：

```python
def complement(s: Set, universe: Set) -> Set:
    return Set(universe._elems - s._elems)
```

```python
U = Set([1, 2, 3, 4, 5])  # 全集
A = Set([2, 4])
complement(A, U)  # {1, 3, 5}
```

> **注意**：`__invert__` 方法（`~` 運算符）已被棄用，因為補集需要明確的論域。

---

## 3. 集合關係

### 3.1 子集 (Subset)

**數學定義**：$A \subseteq B$ 當且僅當 $\forall x (x \in A \rightarrow x \in B)$

集合 A 是集合 B 的子集，表示 A 的每個元素都是 B 的元素。

**實現**：

```python
def subset(s1: Set, s2: Set) -> bool:
    return s1._elems <= s2._elems
```

**運算符**：使用 `<=` 或 `__le__` 方法

```python
A = Set([1, 2])
B = Set([1, 2, 3])
A <= B  # True
```

### 3.2 真子集 (Proper Subset)

**數學定義**：$A \subset B$ 當且僅當 $A \subseteq B$ 且 $A \neq B$

真子集是嚴格小於的子集關係。

**實現**：

```python
def __lt__(self, other):
    return subset(self, other) and self != other
```

**運算符**：使用 `<`

```python
A = Set([1, 2])
B = Set([1, 2, 3])
A < B   # True
B < B  # False（相等集合不是真子集）
```

---

## 4. 笛卡爾積 (Cartesian Product)

### 4.1 定義

**數學定義**：$A \times B = \{(a, b) \mid a \in A \text{ 且 } b \in B\}$

兩個集合的笛卡爾積是所有有序對的集合。

**實現**：

```python
def cartesian(s1: Set, s2: Set) -> Set:
    return Set((a, b) for a in s1._elems for b in s2._elems)
```

```python
A = Set([1, 2])
B = Set(['a', 'b'])
cartesian(A, B)  # {(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')}
```

---

## 5. 冪集 (Power Set)

### 5.1 定義

**數學定義**：$\mathcal{P}(S) = \{X \mid X \subseteq S\}$

冪集是给定集合 S 的所有子集組成的集合。若 $|S| = n$，則 $|\mathcal{P}(S)| = 2^n$。

### 5.2 實現原理

使用二進制掩碼法：對於 n 個元素的集合，每個從 0 到 $2^n - 1$ 的二進制數都代表一個子集。

**實現**：

```python
def power_set(s: Set) -> Set:
    if not s._elems:
        return Set([Set()])
    elems = list(s._elems)
    n = len(elems)
    result = set()
    for mask in range(1 << n):  # 遍歷 0 到 2^n - 1
        subset_elems = {elems[i] for i in range(n) if mask & (1 << i)}
        result.add(Set(subset_elems))
    return Set(result)
```

```python
A = Set([1, 2, 3])
power_set(A)  # {∅, {1}, {2}, {3}, {1, 2}, {1, 3}, {2, 3}, {1, 2, 3}}
```

---

## 6. 對稱差集 (Symmetric Difference)

### 6.1 定義

**數學定義**：$A \ominus B = (A - B) \cup (B - A) = (A \cup B) - (A \cap B)$

對稱差集包含所有屬於恰好一個集合的元素（不兩者皆有）。

### 6.2 實現

```python
def symmetric_difference(s1: Set, s2: Set) -> Set:
    return union(difference(s1, s2), difference(s2, s1))
```

```python
A = Set([1, 2, 3])
B = Set([3, 4, 5])
symmetric_difference(A, B)  # {1, 2, 4, 5}
```

---

## 7. 不相交與相交集合

### 7.1 不相交集合 (Disjoint Sets)

**數學定義**：兩個集合不相交當且僅當 $A \cap B = \emptyset$

即它們沒有公共元素。

**實現**：

```python
def is_disjoint(s1: Set, s2: Set) -> bool:
    return len(intersection(s1, s2)._elems) == 0
```

```python
A = Set([1, 2])
B = Set([3, 4])
is_disjoint(A, B)  # True
```

### 7.2 相交集合 (Overlapping Sets)

**數學定義**：兩個集合相交當且僅當 $A \cap B \neq \emptyset$

即它們至少有一個公共元素。

**實現**：

```python
def is_overlapping(s1: Set, s2: Set) -> bool:
    return len(intersection(s1, s2)._elems) > 0
```

```python
A = Set([1, 2, 3])
B = Set([3, 4, 5])
is_overlapping(A, B)  # True
```

---

## 8. 數學符號與實現對照表

| 數學符號 | 含義 | 實現函數/運算符 |
|---------|------|-----------------|
| $\in$ | 元素屬於 | `in_(elem, set)` |
| $\subseteq$ | 子集 | `set1 <= set2` |
| $\subset$ | 真子集 | `set1 < set2` |
| $\cup$ | 聯集 | `set1 + set2` |
| $\cap$ | 交集 | `set1 * set2` |
| $-$ 或 $\setminus$ | 差集 | `set1 - set2` |
| $\overline{A}$ | 補集 | `complement(set, universe)` |
| $\times$ | 笛卡爾積 | `cartesian(set1, set2)` |
| $\mathcal{P}(S)$ | 冪集 | `power_set(set)` |
| $\ominus$ | 對稱差集 | `symmetric_difference(set1, set2)` |
| $\emptyset$ | 空集 | `empty_set()` |

---

## 9. 集合運算定律

以下定律在 `sets.py` 中通過集合運算自然滿足：

### 9.1 交換律
- $A \cup B = B \cup A$
- $A \cap B = B \cap A$

### 9.2 結合律
- $(A \cup B) \cup C = A \cup (B \cup C)$
- $(A \cap B) \cap C = A \cap (B \cap C)$

### 9.3 分配律
- $A \cap (B \cup C) = (A \cap B) \cup (A \cap C)$
- $A \cup (B \cap C) = (A \cup B) \cap (A \cup C)$

### 9.4 吸收律
- $A \cup (A \cap B) = A$
- $A \cap (A \cup B) = A$

### 9.5 德·摩根定律
- $\overline{A \cup B} = \overline{A} \cap \overline{B}$
- $\overline{A \cap B} = \overline{A} \cup \overline{B}$

---

## 10. 使用範例

```python
from lean4py.sets import Set, union, intersection, complement, power_set

# 創建集合
A = Set([1, 2, 3, 4])
B = Set([3, 4, 5, 6])
U = Set([1, 2, 3, 4, 5, 6, 7, 8])  # 全集

# 基本運算
print(A + B)           # 聯集: {1, 2, 3, 4, 5, 6}
print(A * B)           # 交集: {3, 4}
print(A - B)           # 差集: {1, 2}
print(complement(A, U)) # 補集: {5, 6, 7, 8}

# 子集關係
print(A <= U)          # True (A 是 U 的子集)

# 笛卡爾積
C = Set([1, 2])
D = Set(['a', 'b'])
print(cartesian(C, D)) # {(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')}

# 冪集
P = Set([1, 2, 3])
print(power_set(P))    # {∅, {1}, {2}, {3}, {1,2}, {1,3}, {2,3}, {1,2,3}}

# 對稱差集
print(symmetric_difference(A, B))  # {1, 2, 5, 6}
```

---

## 11. 實現注意事項

1. **有限集合**：該模組僅支援有限集合，不支援無限集合（如自然數集）。

2. **元素要求**：集合元素可以是任何可哈希的 Python 對象。

3. **集合相等性**：使用 `==` 判斷集合相等（基於元素），而非 `is`（對象標識）。

4. **空集**：空集使用 `empty_set()` 創建，顯示為 `∅` 符號。

5. **冪集大小**：若集合有 n 個元素，冪集將有 $2^n$ 個元素，可能導致組合爆炸。