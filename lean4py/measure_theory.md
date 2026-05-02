# Measure Theory (測度論)

本文件說明 lean4py 的 `measure_theory.py` 模組所實現的測度論基本概念與數學原理。

---

## 1. σ-代數 (σ-Algebra)

### 定義

σ-代數（又稱 σ-域）是集合 X 上的一個子集族 Ω，滿足以下三條公理：

1. **全域性**：X ∈ Ω（整個空間是可測的）
2. **封閉於補運算**：若 A ∈ Ω，則 X \ A ∈ Ω
3. **封閉於可數聯集**：若 A₁, A₂, A₃, ... ∈ Ω，則 ∪_{n=1}^∞ Aₙ ∈ Ω

由這些公理可推導出：σ-代數也封閉於可數交集
$$A_1, A_2, \ldots \in \Omega \implies \bigcap_{n=1}^{\infty} A_n \in \Omega$$

### 代數實現 (`SigmaAlgebra` 類)

```python
class SigmaAlgebra:
    def __init__(self, universe: Set[Any], sets: Optional[Set[Any]] = None):
        self.universe = frozenset(universe)
        self.sets = frozenset(frozenset(s) for s in sets)
```

核心方法：
- `is_in(s)`: 檢查集合 s 是否屬於該 σ-代數
- `complement(s)`: 返回 s 在全集下的補集
- `union(a, b)`, `intersection(a, b)`: 可測集之間的交聯運算
- `is_sigma_algebra()`: 驗證三條公理是否滿足

---

## 2. 可測空間 (Measurable Space)

### 定義

可測空間記為 (X, Σ)，其中：
- X 是底層集合（樣本空間）
- Σ 是 X 上的一個 σ-代數

可測空間本身不赋予「大小」的概念，僅定義哪些子集是「可測的」。

### 代數實現 (`MeasurableSpace` 類)

```python
class MeasurableSpace:
    def __init__(self, universe: Set[Any], sigma_algebra: SigmaAlgebra):
        self.universe = universe
        self.sigma_algebra = sigma_algebra

    def is_measurable(self, s: Set[Any]) -> bool:
        return self.sigma_algebra.is_in(s)
```

---

## 3. 測度 (Measure)

### 定義

測度 μ 是在可測空間 (X, Σ) 上定義的集函數：
$$\mu: \Sigma \to [0, \infty]$$

滿足以下公理：

1. **非負性**：對所有 A ∈ Σ，μ(A) ≥ 0
2. **空集測度為零**：μ(∅) = 0
3. **可數可加性**：若 {Aₙ} 是兩兩不相交的可測集族，則
$$\mu\left(\bigcup_{n=1}^{\infty} A_n\right) = \sum_{n=1}^{\infty} \mu(A_n)$$

### 代數實現 (`Measure` 類)

```python
class Measure:
    def __init__(self, space: MeasurableSpace,
                 mu: Optional[Callable[[Set[Any]], float]] = None):
        self.space = space
        self._mu = mu if mu is not None else (lambda s: 0.0)

    def __call__(self, s: Set[Any]) -> float:
        if not self.space.is_measurable(s):
            raise ValueError("Set is not measurable")
        return self._mu(s)

    def is_probability(self) -> bool:
        return self(self.space.universe) == 1.0
```

### 測度的特殊類型

- **有限測度**：μ(X) < ∞
- **概率測度**：μ(X) = 1（記作 P）
- **σ-有限測度**：X 可表示為可數個有限測度集的聯集

---

## 4. 勒貝格測度 (Lebesgue Measure)

### 定義

勒貝格測度是 ℝ 上的標準測度，滿足：
- 區間 [a, b] 的測度為 b - a
- 平移不變性：μ(A + x) = μ(A)
- 是 ℝ 上唯一的平移不變概率測度

### 代數實現 (`LebesgueMeasure` 類)

```python
class LebesgueMeasure(Measure):
    def __init__(self):
        real_line = frozenset(range(-1000, 1001))
        sigma = SigmaAlgebra(set(real_line))
        space = MeasurableSpace(set(real_line), sigma)
        super().__init__(space, self._lebesgue)

    def _lebesgue(self, s: Set[Any]) -> float:
        if len(s) == 0:
            return 0.0
        numeric_vals = [x for x in s if isinstance(x, (int, float))]
        if not numeric_vals:
            return 0.0
        return float(max(numeric_vals) - min(numeric_vals))
```

此實現將離散集合的「測度」定義為最大值與最小值之差（區間長度）。

---

## 5. 零測集與全測集 (Null Sets and Full Measure Sets)

### 定義

- **零測集**：測度為零的集合
  $$\mu(N) = 0$$

- **全測集**：補集為零測集的集合
  $$A \text{ 全測} \iff \mu(X \setminus A) = 0$$

### 性質

- 零測集的子集仍是零測集（未必，見下）
- 若 A ⊆ B，則 μ(A) ≤ μ(B)（單調性）
- 可數個零測集的聯集仍是零測集

### 幾乎處處 (Almost Everywhere)

若命題在 X \ N 上成立，其中 N 是零測集，則稱命題**幾乎處處**（a.e.）成立。

---

## 6. 可測函數 (Measurable Function)

### 定義

設 (X, Σ) 和 (Y, Τ) 為可測空間。函數 f: X → Y 稱為**可測的**，若：
$$\forall B \in \Τ: f^{-1}(B) \in \Sigma$$

即：每個可測集的逆像仍是可測的。

### 可測函數的性質

若 f, g 可測，則：
- f + g, f · g 可測（加法和乘法封閉）
- sup(f, g), inf(f, g), |f| 可測
- 若 fₙ → f，逐點收斂，則 f 可測

### 代數實現 (`MeasurableFunction` 類)

```python
class MeasurableFunction:
    def __init__(self, domain: MeasurableSpace, codomain: MeasurableSpace,
                 func: Callable[[Any], Any]):
        self.domain = domain
        self.codomain = codomain
        self.func = func

    def is_measurable(self) -> bool:
        for b in self.codomain.sigma_algebra.sets:
            preimage = {x for x in self.domain.universe
                       if frozenset([self.func(x)]) <= b}
            if not self.domain.is_measurable(preimage):
                return False
        return True
```

---

## 7. 簡單函數與逼近 (Simple Functions and Approximation)

### 定義

**簡單函數**是有限個指示函數的線性組合：
$$s(x) = \sum_{i=1}^{n} a_i \cdot \mathbf{1}_{A_i}(x)$$

其中 aᵢ ∈ ℝ，Aᵢ 是兩兩不相交的可測集。

### 標準化簡單函數

任意非負可測函數 f 可被一列**遞增的簡單函數**逼近：
$$0 \leq s_1 \leq s_2 \leq \cdots \leq f, \quad s_n \uparrow f$$

### 代數實現 (`SimpleFunction` 類)

```python
class SimpleFunction:
    def __init__(self, pairs: List[Tuple[float, Set[Any]]],
                 space: MeasurableSpace):
        self.pairs = pairs  # (係數, 可測集) 對列表
        self.space = space

    def evaluate(self, x: Any) -> float:
        for coeff, s in self.pairs:
            if x in s:
                return coeff
        return 0.0

    def is_measurable(self) -> bool:
        return all(self.space.sigma_algebra.is_in(s) for _, s in self.pairs)
```

---

## 8. 勒貝格積分 (Lebesgue Integration)

### 定義

對非負簡單函數 s = Σ aᵢ · 1_{Aᵢ}：
$$\int_X s \, d\mu = \sum_{i=1}^{n} a_i \mu(A_i)$$

對非負可測函數 f：
$$\int_X f \, d\mu = \sup\left\{\int_X s \, d\mu : 0 \leq s \leq f, s \text{ 為簡單函數}\right\}$$

也可定義為：
$$\int_X f \, d\mu = \lim_{n \to \infty} \int_X s_n \, d\mu$$

其中 {sₙ} 是逼近 f 的簡單函數序列。

### 代數實現 (`LebesgueIntegral` 類)

```python
class LebesgueIntegral:
    @staticmethod
    def of_simple(f: SimpleFunction) -> float:
        total = 0.0
        measure = LebesgueMeasure()
        for coeff, s in f.pairs:
            total += coeff * measure(s)
        return total

    @staticmethod
    def of_positive(f: Callable[[Any], float],
                    space: MeasurableSpace,
                    partition: List[Set[Any]]) -> float:
        total = 0.0
        measure = LebesgueMeasure()
        for s in partition:
            if space.is_measurable(s):
                sample = next(iter(s), None)
                if sample is not None:
                    total += f(sample) * measure(s)
        return total
```

---

## 9. 單調收斂定理 (Monotone Convergence Theorem, MCT)

### 定理敘述

設 {fₙ} 是一列非負可測函數，滿足：
$$f_1 \leq f_2 \leq \cdots \leq f_n \uparrow f$$

則：
$$\lim_{n \to \infty} \int_X f_n \, d\mu = \int_X f \, d\mu$$

### 重要性

MCT 允許在積分與極限交換時使用，是測度論中最基本的收斂定理之一。

### 證明思路

1. 由於 fₙ ↑ f，積分序列 {∫fₙ dμ} 是單調遞增的
2. 下界：對每個 n，∫fₙ dμ ≤ ∫f dμ
3. 上界：利用簡單函數逼近的思想構造上界序列
4. 兩邊夾擠得到等式

---

## 10. 受控收斂定理 (Dominated Convergence Theorem, DCT)

### 定理敘述

設 {fₙ} 是一列可測函數，逐點（a.e.）收斂於 f。若存在可積分的控制函數 g ∈ L¹ 使得：
$$|f_n| \leq g \quad \text{對所有 } n$$

則：
$$\lim_{n \to \infty} \int_X |f_n - f| \, d\mu = 0$$

進而：
$$\lim_{n \to \infty} \int_X f_n \, d\mu = \int_X f \, d\mu$$

### 與 MCT 的關係

DCT 的條件更強（需要控制函數），但結論更強（不需要單調性假設）。

---

## 11. Lᵖ 空間

### 定義

對 1 ≤ p < ∞，Lᵖ 空間定義為：
$$\mathcal{L}^p(X, \Sigma, \mu) = \left\{f \text{ 可測} : \int_X |f|^p \, d\mu < \infty\right\}$$

配上準範數：
$$\|f\|_p = \left(\int_X |f|^p \, d\mu\right)^{1/p}$$

當 p = ∞ 時：
$$\|f\|_\infty = \text{ess sup}|f| = \inf\{M : |f| \leq M \text{ a.e.}\}$$

### 空間結構

- **L¹**：可積分函數空間
- **L²**：平方可積分函數（希爾伯特空間）
- **Lᵖ 空間是巴拿赫空間**（p ≥ 1 時）

### 關鍵不等式

1. **赫爾德不等式**（Hölder）：
   $$\|fg\|_1 \leq \|f\|_p \|g\|_q, \quad \frac{1}{p} + \frac{1}{q} = 1$$

2. **閔可夫斯基不等式**（Minkowski）：
   $$\|f + g\|_p \leq \|f\|_p + \|g\|_p$$

---

## 12. 拉東-尼古丁導數 (Radon-Nikodym Derivative)

### 定理敘述

設 ν 和 μ 是 σ-有限的測度。若 ν 對 μ **絕對連續**（ν ≪ μ），則存在唯一的（a.e. 意義下）可測函數 f，使得：
$$d\nu = f \, d\mu \quad \text{即} \quad \nu(A) = \int_A f \, d\mu$$

這個 f 記作：
$$f = \frac{d\nu}{d\mu}$$

稱為 **ν 關於 μ 的拉東-尼古丁導數**或**密度**。

### 物理意義

- 拉東-尼古丁導數像是「相對測度密度」
- 若 μ 是勒貝格測度，則 f 就是普通的概率密度函數（PDF）

### 性質

1. **鏈式法則**：
   $$\frac{d\nu}{d\mu} \cdot \frac{d\mu}{d\lambda} = \frac{d\nu}{d\lambda}$$

2. **唯一性**（a.e. 意義下）：
   若 f 和 g 都滿足 dν = f dμ = g dμ，則 f = g (a.e.)

---

## 模組結構總覽

| 類別 | 對應數學概念 |
|------|-------------|
| `SigmaAlgebra` | σ-代數 |
| `MeasurableSpace` | 可測空間 (X, Σ) |
| `Measure` | 測度 μ |
| `LebesgueMeasure` | 勒貝格測度 |
| `ProbabilityMeasure` | 概率測度 (μ(X) = 1) |
| `MeasurableFunction` | 可測函數 f: X → Y |
| `SimpleFunction` | 簡單函數 |
| `LebesgueIntegral` | 勒貝格積分 |

---

## 參考文獻

- Williams, D. *Probability with Martingales*
- Folland, G. B. *Real Analysis: Modern Techniques and Their Applications*
- Stein, E. M. & Shakarchi, R. *Real Analysis: Measure Theory, Integration, & Hilbert Spaces*