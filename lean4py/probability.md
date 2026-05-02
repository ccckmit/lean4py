# 概率論模組 (probability.py) 數學原理文檔

本文件詳細說明 `lean4py/probability.py` 模組背後的數學原理。

---

## 1. 概率空間 (Ω, F, P)

概率空間是概率論的基礎概念，由三元組 (Ω, F, P) 定義：

- **Ω (Sample Space)**: 樣本空間，包含所有可能的實驗結果
- **F (Event Space)**: 事件空間，是 Ω 的子集組成的σ-代數
- **P (Probability Function)**: 概率函數，將每個事件映射到 [0,1] 區間

### 代碼對應

```python
class ProbabilitySpace:
    def __init__(self, sample_space: Set[Any], event_space: Optional[Set['Event']] = None, 
                 prob_func: Optional[Callable[[Any], float]] = None):
        self.sample_space = sample_space      # Ω
        self.event_space = event_space or set()  # F
        self.prob_func = prob_func            # P
```

### 均勻概率空間

當每個基本事件概率相等時，稱為**均勻概率空間**：

$$P(\omega) = \frac{1}{|\Omega|}, \quad \forall \omega \in \Omega$$

---

## 2. 事件類別與運算

事件是樣本空間的子集。Event 類別支援以下運算：

### 2.1 交集 (Intersection)

$$A \cap B = \{x : x \in A \text{ 且 } x \in B\}$$

```python
def __and__(self, other):
    return Event(self.elements & other.elements)
```

### 2.2 聯集 (Union)

$$A \cup B = \{x : x \in A \text{ 或 } x \in B\}$$

```python
def __or__(self, other):
    return Event(self.elements | other.elements)
```

### 2.3 補集 (Complement)

$$A^c = \Omega \setminus A$$

```python
def complement(self, sample_space: Set) -> 'Event':
    return Event(sample_space - self.elements)
```

---

## 3. 條件概率

條件概率表示在事件 B 已發生的條件下，事件 A 發生的概率：

$$P(A|B) = \frac{P(A \cap B)}{P(B)}, \quad P(B) > 0$$

### 代碼實現

```python
def conditional_probability(self, event: Any, given: Any) -> float:
    p_given = self.probability(given)
    if p_given == 0:
        return 0.0
    p_both = self.probability(self.intersection(event, given))
    return p_both / p_given
```

---

## 4. 隨機變量

隨機變量是從樣本空間到實數的函數：

$$X: \Omega \rightarrow \mathbb{R}$$

在代碼中，隨機變量由其可能取值和對應概率定義：

```python
class RandomVariable:
    def __init__(self, name: str, values: Dict[Any, float]):
        self.name = name
        self.values = values  # 值域 -> 概率 的映射
```

### 支撐集 (Support)

隨機變量取值概率大於零的集合：

$$\text{Support}(X) = \{x : P(X = x) > 0\}$$

```python
def support(self) -> List[Any]:
    return [k for k, v in self.values.items() if v > 0]
```

---

## 5. 期望值 (Expected Value)

離散隨機變量的期望值定義為：

$$E[X] = \sum_{x} x \cdot P(X = x)$$

### 代碼實現

```python
def expected_value(self) -> float:
    if self._expected is not None:
        return self._expected
    self._expected = sum(k * v for k, v in self.values.items())
    return self._expected
```

期望值具有線性性：

$$E[aX + bY] = aE[X] + bE[Y]$$

---

## 6. 方差 (Variance)

方差衡量隨機變量偏離其均值的程度：

$$\text{Var}(X) = E[(X - \mu)^2] = E[X^2] - (E[X])^2$$

### 代碼實現

```python
def variance(self) -> float:
    if self._variance is not None:
        return self._variance
    mu = self.expected_value()
    self._variance = sum(((k - mu) ** 2) * v for k, v in self.values.items())
    return self._variance
```

---

## 7. 標準差 (Standard Deviation)

標準差是方差的平方根，與原隨機變量具有相同單位：

$$\sigma = \sqrt{\text{Var}(X)}$$

```python
def std_dev(self) -> float:
    return math.sqrt(self.variance())
```

---

## 8. 協方差與相關係數

### 8.1 協方差 (Covariance)

協方差衡量兩個隨機變量的聯合變異程度：

$$\text{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - E[X]E[Y]$$

```python
def Covariance(X: RandomVariable, Y: RandomVariable) -> float:
    EX = X.expected_value()
    EY = Y.expected_value()
    return X.e(lambda k: Y.values.get(k, 0) * (k - EX) * (Y.values.get(k, 0) - EY))
```

### 8.2 相關係數 (Correlation)

相關係數是標準化後的協方差，取值範圍為 [-1, 1]：

$$\rho_{XY} = \frac{\text{Cov}(X, Y)}{\sigma_X \cdot \sigma_Y}$$

```python
def Correlation(X: RandomVariable, Y: RandomVariable) -> float:
    cov = Covariance(X, Y)
    std_x = X.std_dev()
    std_y = Y.std_dev()
    if std_x == 0 or std_y == 0:
        return 0.0
    return cov / (std_x * std_y)
```

---

## 9. 概率分佈

所有分佈都繼承自抽象基類 Distribution：

```python
class Distribution:
    def pdf(self, x: float) -> float:
        raise NotImplementedError
    def cdf(self, x: float) -> float:
        raise NotImplementedError
    def mean(self) -> float:
        raise NotImplementedError
    def variance(self) -> float:
        raise NotImplementedError
```

---

### 9.1 正態分佈 (Normal Distribution)

**符號**: $X \sim N(\mu, \sigma^2)$

**概率密度函數 (PDF)**:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

**累積分布函數 (CDF)**:

$$F(x) = \frac{1}{2}\left(1 + \text{erf}\left(\frac{x-\mu}{\sigma\sqrt{2}}\right)\right)$$

**矩**:
- 均值: $E[X] = \mu$
- 方差: $\text{Var}(X) = \sigma^2$

```python
class NormalDistribution(Distribution):
    def __init__(self, mu: float = 0, sigma2: float = 1):
        self.mu = mu
        self.sigma2 = sigma2
        self.sigma = math.sqrt(sigma2)
        self._normalizing_constant = 1.0 / (self.sigma * math.sqrt(2 * math.pi))

    def pdf(self, x: float) -> float:
        z = (x - self.mu) / self.sigma
        return self._normalizing_constant * math.exp(-0.5 * z * z)

    def cdf(self, x: float) -> float:
        return 0.5 * (1 + math.erf((x - self.mu) / (self.sigma * math.sqrt(2))))
```

---

### 9.2 二項分佈 (Binomial Distribution)

**符號**: $X \sim \text{Binomial}(n, p)$

**概率質量函數 (PMF)**:

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}, \quad k = 0, 1, 2, \ldots, n$$

**矩**:
- 均值: $E[X] = np$
- 方差: $\text{Var}(X) = np(1-p)$

```python
class BinomialDistribution(Distribution):
    def __init__(self, n: int, p: float):
        self.n = n
        self.p = p
        self.q = 1 - p

    def pdf(self, k: int) -> float:
        if k < 0 or k > self.n:
            return 0.0
        return math.comb(self.n, k) * (self.p ** k) * (self.q ** (self.n - k))
```

---

### 9.3 帕松分佈 (Poisson Distribution)

**符號**: $X \sim \text{Poisson}(\lambda)$

**概率質量函數 (PMF)**:

$$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}, \quad k = 0, 1, 2, \ldots$$

**矩**:
- 均值: $E[X] = \lambda$
- 方差: $\text{Var}(X) = \lambda$

```python
class PoissonDistribution(Distribution):
    def __init__(self, lam: float):
        self.lam = lam

    def pdf(self, k: int) -> float:
        if k < 0:
            return 0.0
        return math.exp(-self.lam) * (self.lam ** k) / math.factorial(k)
```

---

### 9.4 均勻分佈 (Uniform Distribution)

**符號**: $X \sim U(a, b)$

**概率密度函數 (PDF)**:

$$f(x) = \begin{cases} \frac{1}{b-a} & a \leq x \leq b \\ 0 & \text{otherwise} \end{cases}$$

**累積分布函數 (CDF)**:

$$F(x) = \begin{cases} 0 & x < a \\ \frac{x-a}{b-a} & a \leq x \leq b \\ 1 & x > b \end{cases}$$

**矩**:
- 均值: $E[X] = \frac{a+b}{2}$
- 方差: $\text{Var}(X) = \frac{(b-a)^2}{12}$

```python
class UniformDistribution(Distribution):
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b
        self.length = b - a

    def pdf(self, x: float) -> float:
        if self.a <= x <= self.b:
            return 1.0 / self.length
        return 0.0

    def cdf(self, x: float) -> float:
        if x < self.a:
            return 0.0
        elif x >= self.b:
            return 1.0
        return (x - self.a) / self.length
```

---

### 9.5 指數分佈 (Exponential Distribution)

**符號**: $X \sim \text{Exp}(\lambda)$

**概率密度函數 (PDF)**:

$$f(x) = \begin{cases} \lambda e^{-\lambda x} & x \geq 0 \\ 0 & x < 0 \end{cases}$$

**累積分布函數 (CDF)**:

$$F(x) = \begin{cases} 1 - e^{-\lambda x} & x \geq 0 \\ 0 & x < 0 \end{cases}$$

**矩**:
- 均值: $E[X] = \frac{1}{\lambda}$
- 方差: $\text{Var}(X) = \frac{1}{\lambda^2}$

```python
class ExponentialDistribution(Distribution):
    def __init__(self, lam: float):
        self.lam = lam

    def pdf(self, x: float) -> float:
        if x < 0:
            return 0.0
        return self.lam * math.exp(-self.lam * x)

    def cdf(self, x: float) -> float:
        if x < 0:
            return 0.0
        return 1 - math.exp(-self.lam * x)
```

---

## 10. 貝葉斯定理 (Bayes' Theorem)

貝葉斯定理是概率論中最重要的公式之一：

$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

其中：
- $P(A|B)$: 後驗概率 (posterior probability)
- $P(B|A)$: 似然函數 (likelihood)
- $P(A)$: 先驗概率 (prior probability)
- $P(B)$: 邊際似然 (marginal likelihood)

```python
def bayes_theorem(p_a_given_b: float, p_b_given_a: float, p_a: float, p_b: float) -> float:
    return (p_b_given_a * p_a) / p_b if p_b > 0 else 0.0
```

---

## 11. 全概率公式 (Law of Total Probability)

若 $\{A_i\}$ 是樣本空間的一個劃分，則：

$$P(B) = \sum_{i} P(B|A_i) \cdot P(A_i)$$

```python
def law_ofTotal_probability(p_b_given_a_i: List[float], p_a_i: List[float]) -> float:
    return sum(pb * pa for pb, pa in zip(p_b_given_a_i, p_a_i))
```

---

## 12. 假設檢定 (Hypothesis Testing)

假設檢定是用樣本數據來判斷關於總體的假設是否成立。

### 12.1 Z 檢定 (Z-Test)

適用於已知總體標準差或大樣本 (n ≥ 30)：

$$z = \frac{\bar{x} - \mu_0}{\sigma / \sqrt{n}}$$

```python
if test_type == 'z':
    z_stat = (sample_mean - mu) / (s / math.sqrt(n))
    p_value = 2 * (1 - NormalDistribution(0, 1).cdf(abs(z_stat)))
    return {'z': z_stat, 'p_value': p_value, 'reject': p_value < alpha}
```

### 12.2 T 檢定 (T-Test)

適用於未知總體標準差的小樣本：

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

自由度: $df = n - 1$

```python
elif test_type == 't':
    t_stat = (sample_mean - mu) / (s / math.sqrt(n))
    p_value = 2 * (1 - t_dist.cdf(abs(t_stat), n - 1))
    return {'t': t_stat, 'p_value': p_value, 'reject': p_value < alpha}
```

### 12.3 卡方檢定 (Chi-Square Test)

檢驗觀察頻數與期望頻數的擬合度：

$$\chi^2 = \sum_{i=1}^{n} \frac{(O_i - E_i)^2}{E_i}$$

```python
elif test_type == 'chi-square':
    chi2_stat = sum((obs - exp) ** 2 / exp for obs, exp in zip(sample, expected))
    p_value = 1 - chi2_dist.cdf(chi2_stat, n - 1)
    return {'chi2': chi2_stat, 'p_value': p_value, 'reject': p_value < alpha}
```

---

## 13. 信賴區間 (Confidence Interval)

信賴區間給出參數估計的不確定性範圍。

對於均值的信賴區間：

$$\bar{x} \pm t_{\alpha/2, n-1} \cdot \frac{s}{\sqrt{n}}$$

```python
def confidence_interval(sample: List[float], confidence: float = 0.95) -> Tuple[float, float]:
    n = len(sample)
    mean = sum(sample) / n
    s = math.sqrt(sum((x - mean) ** 2 for x in sample) / (n - 1))
    t_val = t_dist.ppf((1 + confidence) / 2, n - 1)
    margin = t_val * s / math.sqrt(n)
    return (mean - margin, mean + margin)
```

---

## 14. 分佈公式速查表

| 分佈 | 參數 | PDF/PMF | 均值 | 方差 |
|------|------|---------|------|------|
| **正態** $N(\mu, \sigma^2)$ | $\mu, \sigma^2$ | $\frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$ | $\mu$ | $\sigma^2$ |
| **二項** $\text{Bin}(n, p)$ | $n, p$ | $\binom{n}{k} p^k (1-p)^{n-k}$ | $np$ | $np(1-p)$ |
| **帕松** $\text{Poisson}(\lambda)$ | $\lambda$ | $\frac{\lambda^k e^{-\lambda}}{k!}$ | $\lambda$ | $\lambda$ |
| **均勻** $U(a, b)$ | $a, b$ | $\frac{1}{b-a}$ | $\frac{a+b}{2}$ | $\frac{(b-a)^2}{12}$ |
| **指數** $\text{Exp}(\lambda)$ | $\lambda$ | $\lambda e^{-\lambda x}$ | $\frac{1}{\lambda}$ | $\frac{1}{\lambda^2}$ |

---

## 附錄：模組使用範例

```python
from lean4py.probability import *

# 創建概率空間
ps = ProbabilitySpace.uniform({1, 2, 3, 4, 5, 6})

# 創建事件
even_event = Event({2, 4, 6}, "偶數")

# 計算概率
print(ps.probability(even_event))  # 輸出: 0.5

# 使用分布
normal = NormalDistribution(mu=0, sigma2=1)
print(normal.pdf(0))  # 輸出: 0.3989422804
print(normal.cdf(1.96))  # 輸出: ~0.975

# 假設檢定
sample = [2.1, 2.4, 2.3, 2.5, 2.2]
result = hypothesis_test('t', sample, mu=2.0)
print(result)  # {'t': t統計量, 'p_value': p值, 'reject': True/False}
```