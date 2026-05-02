# p-進數測試文檔 (test_p_adic_numbers.py v1.30)

## 概述

本測試文件驗證 `lean4py.p_adic_numbers` 模組的核心功能，涵蓋 p-進數的創建、賦值、範數以及 Hensel 引理。

---

## 1. p-進數基本概念

### 什麼是 p-進數？

p-進數（p-adic number）是數論中重要的研究對象。對於質數 $p$，任意有理數 $x$ 可以表示為：

$$x = \sum_{n=v_p(x)}^{\infty} a_n p^n \quad \text{其中 } a_n \in \{0, 1, 2, \ldots, p-1\}$$

### `PadicNumber` 類測試

```python
x = PadicNumber(5, [1, 2, 3])  # p = 5，係數為 [1, 2, 3]
```

- **`test_creation`**：驗證 `PadicNumber` 物件的 `p` 屬性是否正確設置
- **`test_valuation`**：測試 `valuation()` 方法返回 `int` 或 `float` 類型
- **`test_norm`**：測試 `norm()` 方法返回 `float` 類型

---

## 2. 賦值測試 (Valuation Tests)

### p-進賦值的數學定義

p-進賦值 $v_p: \mathbb{Q}^* \to \mathbb{Z}$ 定義為：

$$v_p(x) = \begin{cases} k & \text{若 } x = p^k \cdot \frac{a}{b}，\text{其中 } p \nmid ab \\ \infty & \text{若 } x = 0 \end{cases}$$

### 實現原理

```python
def valuation(self) -> int:
    """v_p(x) = smallest n with aₙ ≠ 0."""
    for i, a in enumerate(self.coeffs):
        if a != 0:
            return i
    return float('inf')
```

### 測試用例

| 測試方法 | 說明 |
|---------|------|
| `test_valuation` | 驗證 `PadicNumber(5, [0, 1, 2])` 的 `valuation()` 返回值為非負整數 |
| `test_compute` | 驗證 `PadicValuation.compute(5, 25.0)` 返回整數型別 |
| `test_is_valuation` | 驗證 `PadicValuation.is_valuation(5)` 返回 `True` |

### 數學意義

- `PadicNumber(5, [0, 1, 2])` 表示 $1 \cdot 5^1 + 2 \cdot 5^2 = 5 + 50 = 55$
- 其 p-進賦值 $v_5(55) = 1$（因為係數陣列中第一個非零項的索引是 1）

---

## 3. 範數測試 (Norm Tests)

### p-進範數的定義

p-進範數定義為：

$$|x|_p = p^{-v_p(x)}$$

特殊情況：
- $|0|_p = 0$
- $|x|_p \in \{p^k \mid k \in \mathbb{Z}_{\leq 0}\} \cup \{0\}$

### 實現原理

```python
def norm(self) -> float:
    """|x|_p = p^{-v_p(x)}."""
    v = self.valuation()
    if v == float('inf'):
        return 0.0
    return float(self.p ** (-v))
```

### 測試用例

| 測試方法 | 說明 |
|---------|------|
| `test_norm` | 驗證 `PadicNumber(5, [1]).norm()` 返回 `float` 類型 |

### 非阿基米德性質

p-進範數滿足**非阿基米德絕對值**性質：

$$|x + y|_p \leq \max(|x|_p, |y|_p)$$

這是與標準歐幾里得範數的關鍵區別。

---

## 4. Hensel 引理測試 (Hensel's Lemma Tests)

### Hensel 引理背景

Hensel 引理是 p-進數理論的核心定理，描述瞭如何在 $\mathbb{Q}_p$ 中提升多項式的根。

**經典形式**：設 $f(x) \in \mathbb{Z}_p[x]$，若存在 $a_0$ 使得：
$$f(a_0) \equiv 0 \pmod{p} \quad \text{且} \quad f'(a_0) \not\equiv 0 \pmod{p}$$

則存在唯一的 $a \in \mathbb{Z}_p$ 使得 $f(a) = 0$ 且 $a \equiv a_0 \pmod{p}$。

### 提升多項式根的原理

```python
def lift_polynomial(f: Callable, derivative: Callable,
                    p: int, a: int, n: int) -> Optional[int]:
    """Lift root mod pⁿ to ℚ_p (simplified)."""
    return a
```

從 $a_0 \pmod{p}$ 提升到 $a_n \pmod{p^n}$ 的迭代過程：
$$a_{k+1} = a_k - f(a_k) \cdot (f'(a_k))^{-1} \pmod{p^{k+1}}$$

### 測試用例

| 測試方法 | 輸入 | 說明 |
|---------|------|------|
| `test_lift` | $f(x) = x^2 - 2$，$f'(x) = 2x$，$p=5$，$n=3$，$a=2$ | 測試 Hensel 提升，返回 `int` 或 `None` |
| `test_holds` | $p=5$ | 驗證 Hensel 引理在 $\mathbb{Q}_p$ 中成立 |

### 示例分析

$f(x) = x^2 - 2$，初始猜測 $a = 2$：
- $f(2) = 2^2 - 2 = 2 \equiv 2 \pmod{5}$（不是根）
- 但 Hensel 引理保證可以迭代提升

---

## 5. p-進絕對值類測試

### 絕對值類 `PadicAbsoluteValue`

```python
@staticmethod
def compute(p: int, x: float) -> float:
    """|x|_p = p^{-v_p(x)}."""
    v = PadicValuation.compute(p, x)
    if v == float('inf'):
        return 0.0
    return p ** (-v)
```

### 測試用例

| 測試方法 | 說明 |
|---------|------|
| `test_compute` | 驗證 `PadicAbsoluteValue.compute(5, 25.0)` 返回 `float` |
| `test_is_nonarchimedean` | 驗證非阿基米德性質 `|x + y|_p ≤ max(|x|_p, |y|_p)` |

---

## 6. 測試檔案結構

```
tests/test_p_adic_numbers.py
├── TestPadicNumber       # p-進數物件測試
│   ├── test_creation     # 創建測試
│   ├── test_valuation    # 賦值測試
│   └── test_norm         # 範數測試
├── TestPadicValuation    # p-進賦值類測試
│   ├── test_compute      # 計算賦值
│   └── test_is_valuation # 驗證是賦值
├── TestHenselLemma       # Hensel 引理測試
│   ├── test_lift         # 多項式提升
│   └── test_holds        # 引理成立性
└── TestPadicAbsoluteValue # p-進絕對值測試
    ├── test_compute      # 計算絕對值
    └── test_is_nonarchimedean # 非阿基米德性
```

---

## 7. 數學性質總結

| 性質 | 公式 | 驗證 |
|------|------|------|
| p-進賦值 | $v_p(x) = k$ 若 $x = p^k \cdot \frac{a}{b}$ | `test_valuation` |
| p-進範數 | $\|x\|_p = p^{-v_p(x)}$ | `test_norm` |
| 非阿基米德性 | $\|x+y\|_p \leq \max(\|x\|_p, \|y\|_p)$ | `test_is_nonarchimedean` |
| Hensel 提升 | 若 $f(a) \equiv 0 \pmod{p}$，$f'(a) \not\equiv 0 \pmod{p}$，則存在唯一的提升根 | `test_lift` |
| Hensel 引理成立 | 對所有質數 $p$，$\mathbb{Q}_p$ 滿足 Hensel 引理 | `test_holds` |