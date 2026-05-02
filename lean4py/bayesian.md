# Bayesian Statistics Module

## 概述

`bayesian.py` 模組實現了貝葉斯統計的核心概念，包括共軛先驗、分佈更新、馬爾可夫鏈蒙特卡羅（MCMC）採樣以及貝葉斯線性回歸。本模組支援Beta-Binomial和Normal-Normal共軛先驗更新，並提供了Metropolis-Hastings MCMC演算法用於後驗分佈採樣。

---

## 1. 貝葉斯定理 (Bayes' Theorem)

### 核心公式

$$P(\theta|D) = \frac{P(D|\theta) \cdot P(\theta)}{P(D)}$$

其中：
- $P(\theta|D)$：後驗分佈（posterior）
- $P(D|\theta)$：似然函數（likelihood）
- $P(\theta)$：先驗分佈（prior）
- $P(D)$：邊際似然（marginal likelihood），也稱為證據（evidence）

### 另一種表達形式

$$P(\theta|D) \propto P(D|\theta) \cdot P(\theta)$$

後驗與似然和先驗的乘積成比例，這是貝葉斯推斷的核心原理。

---

## 2. 先驗分佈 P(θ)

先驗分佈表達在觀察數據之前，我們對參數θ的已有知識或信念。

### 本模組中的先驗類

#### GaussianPrior（高斯先驗）

```python
class GaussianPrior:
    def __init__(self, mean: float, variance: float):
        self.mean = mean
        self.variance = variance
```

高斯先驗適用於連續型參數，其log似然為：

$$\log P(x) = -\frac{1}{2} \log(2\pi\sigma^2) - \frac{(x-\mu)^2}{2\sigma^2}$$

#### BetaPrior（Beta先驗）

```python
class BetaPrior:
    def __init__(self, alpha: float, beta: float):
        self.alpha = alpha
        self.beta = beta
```

Beta先驗適用於機率參數，其log似然為：

$$\log P(p) = (\alpha-1)\log p + (\beta-1)\log(1-p)$$

Beta分佈的均值和方差：
- 均值：$E[p] = \frac{\alpha}{\alpha + \beta}$
- 方差：$\text{Var}(p) = \frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$

---

## 3. 似然函數 P(D|θ)

似然函數給定參數值時，觀察到數據D的概率。

### 高斯似然

對於獨立同分佈的高斯數據：
$$P(D|\theta) = \prod_{i=1}^{n} \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x_i-\theta)^2}{2\sigma^2}\right)$$

### 二項似然

對於n次試驗中k次成功：
$$P(D|p) = \binom{n}{k} p^k (1-p)^{n-k}$$

---

## 4. 後驗分佈 P(θ|D)

後驗分佈是貝葉斯推斷的核心結果，它結合了先驗知識和觀察數據。

### 後驗分佈的計算

在共軛先驗的情況下，後驗分佈與先驗分佈屬於同一家族，這簡化了計算。

### Normal-Normal 共軛更新

模組函數 `posterior_update_normal` 實現：

```python
def posterior_update_normal(
    prior_mean: float,
    prior_variance: float,
    data: List[float],
    likelihood_variance: float
) -> Tuple[float, float]:
```

**更新公式：**

後驗方差：
$$\sigma_n^2 = \frac{1}{\frac{1}{\sigma_0^2} + \frac{n}{\sigma^2}}$$

後驗均值：
$$\mu_n = \sigma_n^2 \left(\frac{\mu_0}{\sigma_0^2} + \frac{n\bar{x}}{\sigma^2}\right)$$

---

## 5. 後驗預測分佈 (Posterior Predictive Distribution)

後驗預測分佈用於預測未來觀察值：

$$P(x_{new}|D) = \int P(x_{new}|\theta) \cdot P(\theta|D) d\theta$$

這是對未來數據的預測，分佈於參數的後驗加權。

---

## 6. 共軛先驗 (Conjugate Priors)

共軛先驗的優點是後驗分佈與先驗分佈屬於同一機率分佈家族，使得更新計算簡單高效。

### 6.1 Beta-Binomial 共軛

**適用場景：** 二項試驗中成功機率的推斷

**先驗：** $p \sim \text{Beta}(\alpha, \beta)$

**後驗更新：**

```python
def posterior_update_beta_binomial(
    prior_alpha: float,
    prior_beta: float,
    successes: int,
    trials: int
) -> Tuple[float, float]:
```

**更新公式：**
$$\alpha_{post} = \alpha_{prior} + k$$
$$\beta_{post} = \beta_{prior} + (n - k)$$

其中k為成功次數，n為總試驗次數。

### 6.2 Dirichlet-Multinomial 共軛

**適用場景：** 多項試驗中各類別機率的推斷

**先驗：** $\mathbf{p} \sim \text{Dirichlet}(\boldsymbol{\alpha})$

**後驗：** $\mathbf{p}|D \sim \text{Dirichlet}(\boldsymbol{\alpha} + \mathbf{k})$

其中 $\mathbf{k}$ 為觀察到的各類別計數。

### 6.3 Normal-Normal 共軛

**適用場景：** 高斯數據的均值參數推斷

**先驗：** $\mu \sim N(\mu_0, \sigma_0^2)$

**似然：** $X_i|\mu \sim N(\mu, \sigma^2)$

**後驗：** $\mu|D \sim N(\mu_n, \sigma_n^2)$

更新公式見第4節。

---

## 7. 可信區間 (Credible Intervals)

可信區間是貝葉斯版本的置信區間，表示參數落在該區間的概率。

### 定義

對於後驗分佈 $P(\theta|D)$，100(1-α)% 可信區間為：

$$P(L \leq \theta \leq U|D) = 1 - \alpha$$

### 常見類型

1. **等尾區間：** 左右尾概率各為 α/2
2. **最高後驗密度區間（HDI）：** 區間內所有點的後驗密度都不低於區間外的點

### 對稱可信區間（高斯近似）

當後驗分佈接近高斯分佈時：
$$\theta \pm z_{\alpha/2} \cdot \sqrt{\text{Var}(\theta|D)}$$

---

## 8. 貝葉斯因子 (Bayes Factor)

貝葉斯因子用於比較兩個假設或模型：

$$B_{10} = \frac{P(D|H_1)}{P(D|H_0)} = \frac{\int P(D|\theta) P(\theta|H_1) d\theta}{\int P(D|\theta) P(\theta|H_0) d\theta}$$

### 模組實現

```python
def compute_bayes_factor(
    log_likelihood_1: List[float],
    log_likelihood_2: List[float]
) -> float:
```

使用log-sum-exp技巧確保數值穩定性：

$$\log B = \log \sum_i P(D_i|\theta_i) - \log \sum_j P(D_j|\theta_j)$$

### 貝葉斯因子解釋

| $|B_{10}|$ | 解釋 |
|------------|------|
| 1-3 | 輕微證據 |
| 3-10 | 中等證據 |
| 10-30 | 強證據 |
| 30-100 | 非常強證據 |
| >100 | 決定性證據 |

---

## 9. 參數的貝葉斯推斷

### 點估計

#### 後驗均值

$$E[\theta|D] = \int \theta \cdot P(\theta|D) d\theta$$

#### 後驗中位數

滿足 $P(\theta \leq \tilde{\theta}|D) = 0.5$ 的 $\tilde{\theta}$

#### MAP 估計（最大後驗估計）

見第10節。

### 區間估計

使用可信區間（如第7節所述）。

---

## 10. MAP 估計 (Maximum A Posteriori Estimation)

MAP估計是後驗分佈的最大值點：

$$\theta_{MAP} = \arg\max_\theta P(\theta|D) = \arg\max_\theta P(D|\theta) \cdot P(\theta)$$

### 與MLE的關係

當先驗均勻分佈時，MAP估計退化为最大似然估計（MLE）。

### 數值計算

可通過梯度上升或Metropolis-Hastings採樣後取最高後驗密度點來估計。

---

## 11. 後驗分佈的漸近正態性 (Asymptotic Normality)

### 理論保證

當樣本量趨於無窮大時，後驗分佈趨近於高斯分佈：

$$\theta|D \xrightarrow{d} N(\theta_{MLE}, I(\theta)^{-1})$$

其中 $I(\theta)$ 是費雪信息矩陣。

### 拉普拉斯逼近

對於有限樣本，可用拉普拉斯逼近近似後驗分佈：

$$P(\theta|D) \approx N(\theta_{MAP}, -\nabla^2 \log P(\theta|D)|_{\theta_{MAP}})$$

這意味著在大樣本下，後驗均值趋於MLE，後驗方差趋於Cramer-Rao下界。

---

## 模組函數總覽

| 函數 | 說明 |
|------|------|
| `GaussianPrior` | 高斯先驗類 |
| `BetaPrior` | Beta先驗類 |
| `posterior_update_normal` | Normal-Normal共軛更新 |
| `posterior_update_beta_binomial` | Beta-Binomial共軛更新 |
| `metropolis_hastings` | Metropolis-Hastings MCMC採樣 |
| `bayesian_linear_regression` | 貝葉斯線性回歸 |
| `compute_bayes_factor` | 貝葉斯因子計算 |

---

## 使用範例

### Beta-Binomial 共軛更新

```python
from lean4py.bayesian import posterior_update_beta_binomial, BetaPrior

# 先驗：Beta(2, 2) - 均勻先驗
prior_alpha, prior_beta = 2, 2

# 觀察數據：10次試驗中7次成功
posterior_alpha, posterior_beta = posterior_update_beta_binomial(
    prior_alpha, prior_beta, successes=7, trials=10
)

# 後驗：Beta(9, 5)
print(f"後驗參數: alpha={posterior_alpha}, beta={posterior_beta}")
```

### Metropolis-Hastings 採樣

```python
from lean4py.bayesian import metropolis_hastings
import math

# 目標分佈：標準高斯
log_target = lambda x: -0.5 * x**2

samples = metropolis_hastings(
    log_target=log_target,
    initial=0.0,
    n_samples=5000,
    proposal_std=1.0
)
```

### 貝葉斯線性回歸

```python
from lean4py.bayesian import bayesian_linear_regression

X = [[1, 1], [1, 2], [1, 3], [1, 4]]
y = [2.1, 4.2, 5.9, 8.2]

posterior_mean, posterior_cov = bayesian_linear_regression(X, y)
```

---

## 參考文獻

1. Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian Data Analysis* (3rd ed.). Chapman and Hall/CRC.
2. Bernardo, J. M., & Smith, A. F. M. (1994). *Bayesian Theory*. John Wiley & Sons.
3. Murphy, K. P. (2012). *Machine Learning: A Probabilistic Perspective*. MIT Press.