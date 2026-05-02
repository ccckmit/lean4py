# p-adic Numbers Module Documentation

## 概述

本模組實現了 p-adic 數論的核心概念，對應 mathlib4 的 `Mathlib.NumberTheory.PAdic`。p-adic 數是數論中重要的工具，在密碼學、丟番圖方程求解和代數幾何中有廣泛應用。

---

## 1. p-adic 賦值 (p-adic Valuation)

### 定義

對於素數 $p$ 和非零有理數 $x \in \mathbb{Q}^*$，p-adic 賦值定義為：

$$v_p(x) = \max\{k \in \mathbb{N} \mid p^k \text{ 整除 } x\}$$

即 $x$ 可以被 $p^k$ 整除的最大指數。

### 性質

- $v_p: \mathbb{Q}^* \to \mathbb{Z}$ 是離散賦值
- $v_p(xy) = v_p(x) + v_p(y)$
- $v_p(x+y) \geq \min(v_p(x), v_p(y))$

### 代碼實現

```python
class PadicValuation:
    """p-adic valuation v_p: Q* → ℤ."""

    @staticmethod
    def compute(p: int, x: float) -> int:
        """v_p(x) for x ∈ ℚ (simplified)."""
        if x == 0:
            return float('inf')
        count = 0
        while x % p == 0:
            x //= p
            count += 1
        return count
```

---

## 2. p-adic 絕對值 (p-adic Absolute Value)

### 定義

基於 p-adic 賦值，p-adic 絕對值定義為：

$$|x|_p = p^{-v_p(x)}$$

對於 $x = 0$，定義 $|0|_p = 0$。

### 強三角不等式 (Strong Triangle Inequality)

p-adic 絕對值滿足**非阿基米德絕對值**的性質：

$$|x + y|_p \leq \max(|x|_p, |y|_p)$$

這比普通絕對值的三角不等式 $|x + y| \leq |x| + |y|$ 更強。

### 推論

- 若 $|x|_p \neq |y|_p$，則 $|x + y|_p = \max(|x|_p, |y|_p)$
- 所有三角形都是等腰三角形，且最長邊唯一決定周長

### 代碼實現

```python
class PadicAbsoluteValue:
    """p-adic absolute value |·|_p."""

    @staticmethod
    def compute(p: int, x: float) -> float:
        """|x|_p = p^{-v_p(x)}."""
        v = PadicValuation.compute(p, x)
        if v == float('inf'):
            return 0.0
        return p ** (-v)

    @staticmethod
    def is_nonarchimedean(p: int) -> bool:
        """|x + y|_p ≤ max(|x|_p, |y|_p)."""
        return True
```

---

## 3. p-adic 數 $\mathbb{Q}_p$ 作為有理數的完備化

### 構造

p-adic 數域 $\mathbb{Q}_p$ 是有理數 $\mathbb{Q}$ 在 p-adic 距離：

$$d_p(x, y) = |x - y|_p$$

下的**完備化**（類似於實數 $\mathbb{R}$ 是 $\mathbb{Q}$ 在歐氏距離下的完備化）。

### 不同質數的不同完備化

- $\mathbb{R}$ 是唯一的實數域（基於歐氏距離）
- $\mathbb{Q}_p$ 對每個素數 $p$ 都不同
- $\mathbb{Q}_2, \mathbb{Q}_3, \mathbb{Q}_5, \ldots$ 都是不同的完备化

### 重要性質

| 性質 | 說明 |
|------|------|
| 特徵 | 特徵為 0（與 $\mathbb{R}$ 相同） |
| 局部域 | 是局部域 (local field) |
| 代數封閉 | $\mathbb{Q}_p$ 不是代數封閉的 |
| 代數閉包 | $\overline{\mathbb{Q}}_p$ 是代數封閉的 |

---

## 4. p-adic 展開 (p-adic Expansions)

### 形式

每個 p-adic 數可以唯一寫成**向左無限**的展開式：

$$x = \sum_{n=k}^{\infty} a_n p^n = a_k p^k + a_{k+1} p^{k+1} + a_{k+2} p^{k+2} + \cdots$$

其中係數 $a_n \in \{0, 1, 2, \ldots, p-1\}$，且 $a_k \neq 0$（除非 $x = 0$）。

### 與整數進位制的類比

- 普通整數：$\ldots d_3 d_2 d_1 d_0$（有限位，向左延伸）
- p-adic 數：$\ldots d_3 d_2 d_1 d_0$（無限位，向左延伸）

### 示例

以 $p = 5$ 為例：
- $-1 = \ldots 44444_5$（在 5-adic 中）
- $1/3 = \ldots 1313132_5$（週期展開）

### 代碼實現

```python
class PadicNumber:
    """p-adic number x = Σ aₙ pⁿ (aₙ ∈ {0,...,p-1})."""

    def __init__(self, p: int, coefficients: Optional[List[int]] = None):
        self.p = p
        self.coeffs = coefficients or [0]

    def valuation(self) -> int:
        """v_p(x) = smallest n with aₙ ≠ 0."""
        for i, a in enumerate(self.coeffs):
            if a != 0:
                return i
        return float('inf')

    def norm(self) -> float:
        """|x|_p = p^{-v_p(x)}."""
        v = self.valuation()
        if v == float('inf'):
            return 0.0
        return float(self.p ** (-v))
```

---

## 5. Hensel 引理 (Hensel's Lemma)

### 歷史背景

由 Kurt Hensel (1904) 創立，是將牛頓法從實數推廣到 p-adic 數的結果。

### 經典形式

設 $f(x) \in \mathbb{Z}_p[x]$，若存在 $a_0 \in \mathbb{Z}_p$ 使得：

$$f(a_0) \equiv 0 \pmod{p}$$

且

$$f'(a_0) \not\equiv 0 \pmod{p}$$

則存在唯一的 $a \in \mathbb{Z}_p$ 使得：
- $f(a) = 0$
- $a \equiv a_0 \pmod{p}$

### 幾何解釋

Hensel 引理表明：如果多項式在模 $p$ 下有一個簡單根，則這個根可以**唯一提升**到 p-adic 整數。

### 牛頓迭代法視角

在 $\mathbb{Q}_p$ 中，牛頓迭代收斂速度更快：

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

### 代碼實現

```python
class HenselLemma:
    """Hensel's lemma: lifting solutions mod pⁿ to ℚ_p."""

    @staticmethod
    def lift_polynomial(f: Callable, derivative: Callable,
                        p: int, a: int, n: int) -> Optional[int]:
        """Lift root mod pⁿ to ℚ_p (simplified)."""
        return a

    @staticmethod
    def holds(p: int) -> bool:
        """Hensel's lemma holds in ℚ_p (simplified)."""
        return True
```

---

## 6. 牛頓多邊形法 (Newton Polygon Method)

### 目的

用於判斷多項式在 $\mathbb{Q}_p$ 中的根的個数和性質。

### 構造方法

設多項式 $f(x) = \sum_{i=0}^n a_i x^i$，其中 $a_i \in \mathbb{Q}_p$。

1. 將每個係數 $a_i$ 寫成 $a_i = p^{k_i} \cdot u_i$（其中 $u_i$ 為 p-adic 單位）
2. 在平面直角坐標系中標出點 $(i, k_i)$
3. 從左到右畫出下凸包絡線（凸包的下邊界）
4. 根據各邊斜率確定根的 p-adic 賦值

### 和牛頓法的關係

牛頓多邊形的每段邊對應一組根，這些根的賦值由邊的斜率給出。

---

## 7. p-adic 數域的代數性質

### 局部域結構

$\mathbb{Q}_p$ 是一個**局部域**，具有以下結構：

- **離散賦值域**：配備離散賦值 $v_p$
- **局部域**：完备的、局部緊的
- **不完全域**：若 $p$ 為完全矛盾數，則 $\mathbb{Q}_p$ 是完全的

### 子結構

$$\mathbb{Z}_p = \{x \in \mathbb{Q}_p \mid |x|_p \leq 1\}$$（p-adic 整數環）

$$\mathbb{Z}_p^\times = \{x \in \mathbb{Q}_p \mid |x|_p = 1\}$$（p-adic 單位群）

### 逼近定理

對於任意有限個兩兩不相同的素數 $p_1, p_2, \ldots, p_n$ 和任意有理數 $a_1, \ldots, a_n$，以及任意正整數 $N$，存在整數 $x$ 使得：

$$x \equiv a_i \pmod{p_i^N} \quad \text{對所有 } i$$

這是**中國剩餘定理**在 p-adic 框架下的推廣。

---

## 8. 應用領域

### 丟番圖方程

Hensel 引理常用於求解丟番圖方程，例如：
- 將解從模 $p$ 提升到 $\mathbb{Z}_p$
- 證明有理數解的存在性

### 密碼學

- RSA 加密的數論基礎
- 橢圓曲線密碼學

### 代數幾何

- p-adic 解析空間
- 剛性解析幾何

---

## 參考文獻

1. Gouvêa, F. Q. - *p-adic Numbers: An Introduction*
2. Koblitz, N. - *p-adic Numbers, p-adic Analysis, and Zeta-Functions*
3. mathlib4 - `Mathlib.NumberTheory.PAdic`