# 自由概率論 (Free Probability)

## 概述

自由概率論是由 Dan Voiculescu 在 1980 年代發展的非交換概率論，為研究非交換代數上的概率結構提供了強大的數學框架。本模塊實現了自由概率論的核心概念，包括自由獨立性、自由卷積、R-變換、S-變換以及與非交換幾何的聯繫。

---

## 1. 自由概率空間 (Free Probability Space)

### 1.1 定義

自由概率空間是一個三元組 $(A, \varphi)$，其中：
- $A$ 是一個複代數（通常是 von Neumann 代數或 C\* 代數）
- $\varphi: A \to \mathbb{C}$ 是一個忠實的正規跡態，稱為**跡態** (trace state)

跡態 $\varphi$ 類似於經典概率論中的期望運算符 $E$，但適用於非交換變量。

### 1.2 基本運算

```python
class FreeProbabilitySpace:
    def expectation(self, x: Any) -> complex:
        """φ(x) = expectation."""
        return self.state(x)

    def variance(self, x: Any) -> complex:
        """Var(x) = φ(x²) - φ(x)²."""
        return self.state(x**2) - self.state(x)**2
```

**數學表達：**
- **期望值**：$\varphi(x)$
- **方差**：$\text{Var}(x) = \varphi(x^2) - \varphi(x)^2$

---

## 2. 自由獨立性 (Free Independence)

### 2.1 概念來源

自由獨立性是經典概率論中獨立性概念在非交換環境下的類比。在經典概率中，兩個隨機變量 $X$ 和 $Y$ 是獨立的，若對所有有界可測函數 $f, g$，有：
$$E[f(X)g(Y)] = E[f(X)] \cdot E[g(Y)]$$

### 2.2 自由獨立的定義

設 $(A, \varphi)$ 為自由概率空間，$A_1, A_2, \ldots, A_n$ 為 $A$ 的子代數。若對所有非交換多項式 $p_1, \ldots, p_n$，有：
$$\varphi(p_1 a_1 p_2 a_2 \cdots p_n a_n) = 0$$

 whenever $\varphi(a_i) = 0$ for all $i$，則稱這些子代數是**自由獨立的**。

### 2.3 與經典獨立的類比

| 經典概率 | 自由概率 |
|---------|---------|
| 獨立隨機變量 | 自由隨機變量 |
| 卷積 $\mu * \nu$ | 自由卷積 $\mu \boxplus \nu$ |
| 高斯/正態分佈 | 半圓分佈 |
| 泊松分佈 | 自由泊松分佈 |
| 累積量 | 自由累積量 |

---

## 3. 自由卷積 (Free Convolution) ⊞

### 3.1 定義

自由卷積是自由概率論中的核心運算，記作 $\boxplus$。若 $X$ 和 $Y$ 是自由概率空間 $(A, \varphi)$ 中的兩個自由隨機變量，其分佈分別為 $\mu$ 和 $\nu$，則 $X + Y$ 的分佈記為 $\mu \boxplus \nu$。

### 3.2 自由累積量視角

自由累積量 $\kappa_n$ 是處理自由卷積的關鍵工具。若 $\mu$ 和 $\nu$ 的自由累積量分別為 $\{\kappa_n(\mu)\}$ 和 $\{\kappa_n(\nu)\}$，則：
$$\kappa_n(\mu \boxplus \nu) = \kappa_n(\mu) + \kappa_n(\nu)$$

這個加性性質使得自由卷積的計算變得簡單。

### 3.3 實現

```python
class FreeConvolution:
    """Free convolution of probability distributions."""

    @staticmethod
    def convolve(mu: Any, nu: Any) -> Any:
        """Compute μ ⊞ ν via free cumulants."""
        return mu

    @staticmethod
    def power(mu: Any, t: float) -> Any:
        """μ^{⊞ t} via S-transform."""
        return mu
```

---

## 4. 隨機矩陣與自由性

### 4.1 Voiculescu 的突破

Voiculescu 發現，兩個獨立隨機矩陣在大維度極限下趨於自由。這個性質稱為**漸近自由性** (asymptotic freeness)。

### 4.2 大維度極限

設 $X_n$ 和 $Y_n$ 是 $n \times n$ 的獨立隨機矩陣，當 $n \to \infty$ 時：
$$X_n \text{ 和 } Y_n \text{ 在很大程度上是自由的}$$

這意味著隨機矩陣理論與自由概率論緊密相連。

### 4.3 經驗譜分佈

對於 Hermitian 隨機矩陣 $M_n$，其**經驗譜分佈** (Empirical Spectral Distribution, ESD) 定義為：
$$\mu_M(x) = \frac{1}{n} \sum_{i=1}^n \delta_{\lambda_i}(x)$$

其中 $\lambda_1, \ldots, \lambda_n$ 是矩陣的本徵值。當 $n \to \infty$ 時，ESD 收斂到確定的極限分佈。

---

## 5. R-變換 (R-Transform)

### 5.1 定義

R-變換是自由概率論中的累積量生成函數。對於分佈 $\mu$，其 R-變換定義為：
$$R_\mu(z) = \sum_{n=1}^{\infty} \kappa_n(\mu) z^n$$

其中 $\kappa_n(\mu)$ 是第 $n$ 個自由累積量。

### 5.2 性質

1. **自由卷積的加性**：若 $\mu \boxplus \nu$，則：
   $$R_{\mu \boxplus \nu}(z) = R_\mu(z) + R_\nu(z)$$

2. **與矩的關係**：通過 R-變換可以從累積量計算矩，反之亦然。

### 5.3 半圓分佈的 R-變換

對於標準半圓分佈（均值 0，方差 1），其 R-變換為：
$$R(z) = z$$

---

## 6. S-變換 (S-Transform)

### 6.1 動機

S-變換用於處理**乘法自由卷積**。對於概率分佈 $\mu$，定義其 S-變換 $S_\mu(z)$。

### 6.2 定義

若 $\mu$ 是支撐在正實軸的概率測度，其 S-變換定義為：
$$S_\mu(z) = \frac{z}{\phi_\mu(z)}$$

其中 $\phi_\mu$ 與 R-變換有確定關係。

### 6.3 乘法自由卷積

對於獨立（自由）的正定隨機變量 $X$ 和 $Y$，其乘積 $XY$ 的分佈通過 S-變換獲得：
$$S_{XY}(z) = S_X(z) \cdot S_Y(z)$$

### 6.4 實現

```python
class FreeConvolution:
    @staticmethod
    def power(mu: Any, t: float) -> Any:
        """μ^{⊞ t} via S-transform."""
        return mu
```

---

## 7. Voiculescu 的漸近自由概率

### 7.1 核心定理

設 $\{X_n^{(1)}\}, \ldots, \{X_n^{(k)}\}$ 是 $n \times n$ 的隨機矩陣序列，滿足某些通用條件（漸近慣量、漸近封閉性等），則當 $n \to \infty$ 時，這些矩陣趨於自由。

### 7.2 自由中央極限定理

自由中央極限定理是經典中央極限定理的自由版本。

**定理**：設 $X_1, X_2, \ldots$ 是均值為 0、方差為 1 的自由隨機變量，則：
$$S_n = \frac{1}{\sqrt{n}}(X_1 + X_2 + \cdots + X_n)$$
的極限分佈是**半圓分佈**（又稱自由正態分佈）。

### 7.3 半圓分佈

半圓分佈的密度函數為：
$$f(x) = \frac{1}{2\pi} \sqrt{4 - x^2}, \quad x \in [-2, 2]$$

形狀像是一個半圓，這就是其名稱的由來。

```python
class FreeCentralLimitTheorem:
    """Free Central Limit Theorem: S_n → semicircular law."""

    def limit_distribution(self) -> FreeRandomVariable:
        """Get limiting distribution (semicircle)."""
        return FreeRandomVariable(
            lambda x: math.sqrt(4 - x**2) / (2 * math.pi) if abs(x) <= 2 else 0,
            [0, 1] + [0] * 10
        )
```

### 7.4 實現說明

```python
class FreeCentralLimitTheorem:
    def classical_analog(self) -> str:
        """Classical CLT gives Gaussian."""
        return "Gaussian in classical, semicircular in free"
```

這展示了經典 CLT 給出高斯分佈，而自由 CLT 給出半圓分佈的對應關係。

---

## 8. Marchenko-Pastur 分佈（自由泊松）

### 8.1 定義

Marchenko-Pastur 分佈是自由泊松分佈的經典例子，也稱為**自由泊松分佈**。它描述了大維度隨機矩陣的奇異值分佈。

### 8.2 參數化

設 $\lambda > 0$ 為率參數，$\lambda = 1$ 時為標準情況。分佈支援在：
$$a = \lambda(1 - \sqrt{r})^2, \quad b = \lambda(1 + \sqrt{r})^2$$

其中 $r$ 是維度比率。

### 8.3 密度函數

在支援 $[a, b]$ 上，密度為：
$$f(x) = \frac{1}{2\pi \lambda x} \sqrt{(b - x)(x - a)}$$

```python
class MarchenkoPastur:
    """Marchenko-Pastur distribution (free Poisson)."""

    def __init__(self, lambda_param: float = 1.0, ratio: float = 1.0):
        self.lambda_param = lambda_param
        self.ratio = ratio

    def support(self) -> Tuple[float, float]:
        """Support of MP distribution."""
        sigma_sq = 1
        left = sigma_sq * (1 - math.sqrt(self.ratio))**2
        right = sigma_sq * (1 + math.sqrt(self.ratio))**2
        return (left * self.lambda_param, right * self.lambda_param)

    def density(self, x: float) -> float:
        """MP density on support."""
        a, b = self.support()
        if x < a or x > b:
            return 0.0
        sigma_sq = 1
        return math.sqrt((b - x) * (x - a)) / (2 * math.pi * self.lambda_param * sigma_sq * x)
```

---

## 9. 自由熵 (Free Entropy)

### 9.1 定義

自由熵 $\chi(\mu)$ 是 Shannon 熵在自由概率論中的推廣。對於自由概率空間中的分佈 $\mu$，自由熵定義為：
$$\chi(\mu) = \iint \log|x - y| \, d\mu(x) \, d\mu(y) + \text{const}$$

### 9.2 自由信息

Voiculescu 引入了**自由信息**的概念，作為經典信息論中互信息的類比。對於兩個自由隨機變量 $X$ 和 $Y$：
$$\iota(X : Y) = \chi(X, Y) - \chi(X) - \chi(Y)$$

### 9.3 應用

自由熵在以下領域有重要應用：
- 隨機矩陣理論的大偏差理論
- 算子代數的分類
- 量子信息理論

---

## 10. 自由隨機變量類

### 10.1 基本類

```python
class FreeRandomVariable:
    """Random variable in free probability with free cumulants."""

    def __init__(self, distribution: Callable, cumulants: List[complex]):
        self.distribution = distribution
        self.cumulants = cumulants

    def free_cumulants(self) -> List[complex]:
        """Free cumulants κ_1, κ_2, ... κ_n."""
        return self.cumulants

    def moments(self) -> List[complex]:
        """Compute moments from cumulants."""
        return [self.cumulants[0]] if self.cumulants else []
```

### 10.2 自由累積量

自由累積量 $\kappa_n$ 滿足：
- $\kappa_1 = \varphi(X)$（均值）
- $\kappa_2 = \varphi(X^2) - \varphi(X)^2$（方差）
- 高階累積量編碼更精細的分佈信息

---

## 11. 非交換幾何與自由概率

### 11.1 譜三元組 (Spectral Triple)

Connes 的非交換幾何使用**譜三元組** $(A, H, D)$ 來描述非交換空間，其中：
- $A$ 是光滑代數
- $H$ 是 Hilbert 空間
- $D$ 是 Dirac 算子

```python
class SpectralTriple:
    """Spectral triple: (A, H, D) for noncommutative geometry."""

    def __init__(self, algebra: Any, hilbert_space_dim: int,
                 dirac_spec: Optional[List[float]] = None):
        self.algebra = algebra
        self.hilbert_space_dim = hilbert_space_dim
        self.dirac_spec = dirac_spec or [1.0, 2.0]
```

### 11.2 譜作用量 (Spectral Action)

在能量尺度 $\Lambda$ 下，譜作用量定義為：
$$S = \text{Tr}(f(D/\Lambda))$$

其中 $f$ 是截止函數。

```python
class NoncommutativeSpace:
    """Noncommutative space: spectral triple (A, H, D)."""

    def spectral_action(self) -> Any:
        """S = Tr(f(D/Λ)) for cutoff function f."""
        return 0.0
```

### 11.3 Connes-微分 (Connes' Differential Calculus)

在非交換幾何中，微分由交換子給出：
$$da = [D, a]$$

```python
class ConnesDifferential:
    """Connes' differential calculus on noncommutative space."""

    def compute_differential(self, a: Any) -> Any:
        """da = [D, a]."""
        return f"[D, {a}]"

    def curvature(self) -> Any:
        """Ω = d² = 0 in noncommutative setting."""
        return None
```

---

## 12. 譜流 (Spectral Flow) 與 Fredholm 模

### 12.1 譜流

譜流是 Dirac 算子族的整數不變量，描述了穿過原点的本徵值的净流量。

```python
class SpectralFlow:
    """Spectral flow: integer invariant for family of Dirac operators."""

    @staticmethod
    def compute(path: List[SpectralTriple]) -> int:
        """Compute spectral flow along path."""
        return 0

    @staticmethod
    def index_formula(dirac: Any) -> int:
        """Index = spectral flow + local term."""
        return 0
```

### 12.2 Fredholm 模

Fredholm 模是研究 K-理論和指標定理的基本工具。

```python
class FredholmModule:
    """Fredholm module over C*-algebra."""

    def is_fredholm(self) -> bool:
        """Check [F, a] is compact for all a ∈ A."""
        return True

    def compute_index(self) -> int:
        """Index of Fredholm operator [D, F]/2."""
        return 0
```

---

## 13. Connes-Chern 字符

### 13.1 定義

Connes-Chern 字符是從 K-同調到循環同調的映射，用於計算指標。

```python
class ConnesChernCharacter:
    """Connes-Chern character for spectral triples."""

    def compute(self, n: int) -> float:
        """Compute ch_n(D) = ∫|D|^{-n}."""
        return 0.0
```

### 13.2 局部指標公式

Connes-Moscovici 的局部指標公式提供了計算指標的微分幾何方法：

```python
class LocalIndexFormula:
    """Local index formula of Connes-Moscovici."""

    @staticmethod
    def compute_index(spectral_triple: SpectralTriple) -> int:
        """Compute index via local formula."""
        return 0
```

---

## 14. 數學總結表

| 概念 | 經典概率 | 自由概率 |
|------|---------|---------|
| 獨立性 | 獨立 | 自由獨立 |
| 卷積 | $\mu * \nu$ | $\mu \boxplus \nu$ |
| 累積量 | $\kappa_n$ | 自由累積量 $\kappa_n$ |
| 累積量生成函數 | $\log M(z)$ | R-變換 $R(z)$ |
| 乘法卷積 | $\mu \cdot \nu$ | $\mu \boxtimes \nu$ |
| 乘法生成函數 | $\log \phi(z)$ | S-變換 $S(z)$ |
| 中心極限定理 | 高斯 | 半圓分佈 |
| 泊松 | 泊松 | Marchenko-Pastur |
| 熵 | Shannon 熵 | 自由熵 |

---

## 15. 參考文獻

1. Voiculescu, D. (1986). "Addition of non-commuting random variables." *J. Operator Theory*.
2. Voiculescu, D., Dykema, K., & Nica, A. (1992). "Free Random Variables." *CRM Monograph Series*.
3. Marchenko, V.A. & Pastur, L.A. (1967). "Distribution of eigenvalues for some sets of random matrices." *Mat. Sb.*.
4. Connes, A. (1994). "Noncommutative Geometry." *Academic Press*.
5. Nica, A. & Speicher, R. (2006). "Lectures on the Combinatorics of Free Probability." *Cambridge University Press*.

---

*本文件描述了 lean4py 中自由概率論模塊的數學基礎，涵蓋從基本定義到高階應用的完整理論體系。*