# Bayesian 統計測試文檔

本文檔說明 `test_bayesian.py` 中測試用例所驗證的貝葉斯推斷數學原理。

---

## 1. 測試驗證的內容概述

本測試模組驗證以下核心貝葉斯統計功能：

- **先驗分佈** (Prior)：GaussianPrior、BetaPrior
- **後驗更新** (Posterior Update)：共軛先驗更新
- **MCMC 採樣**：Metropolis-Hastings 演算法
- **貝葉斯線性迴歸**：帶先驗的線性迴歸
- **貝葉斯因子** (Bayes Factor)：模型比較

---

## 2. 先驗分佈測試 (Prior Tests)

### 2.1 GaussianPrior（高斯先驗）

測試類別：`TestGaussianPrior`

#### 數學原理

高斯先驗適用於連續型參數的貝葉斯推斷。其對數似然函數為：

$$\log p(x | \mu, \sigma^2) = -\frac{1}{2} \left( \frac{(x - \mu)^2}{\sigma^2} + \log(2\pi\sigma^2) \right)$$

其中：
- $\mu$ 為均值（mean）
- $\sigma^2$ 為方差（variance）
- $\sigma$ 為標準差（std = $\sqrt{variance}$）

#### 測試用例說明

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_initialization` | 初始化時 mean、variance、std 正確計算 |
| `test_log_likelihood` | 對數似然在均值處最大，且為負值 |
| `test_likelihood_at_mean` | 確認似然函數的峰值在先驗均值處 |

### 2.2 BetaPrior（Beta 先驗）

測試類別：`TestBetaPrior`

#### 數學原理

Beta 分佈是 [0,1] 区間上概率參數的共軛先驗：

$$\text{Beta}(\theta | \alpha, \beta) = \frac{\theta^{\alpha-1} (1-\theta)^{\beta-1}}{B(\alpha, \beta)}$$

其中 $B(\alpha, \beta) = \frac{\Gamma(\alpha)\Gamma(\beta)}{\Gamma(\alpha+\beta)}$

Beta 先驗的特性：
- **均值**：$E[\theta] = \frac{\alpha}{\alpha + \beta}$
- **方差**：$\text{Var}[\theta] = \frac{\alpha\beta}{(\alpha+\beta)^2(\alpha+\beta+1)}$

#### 測試用例說明

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_initialization` | alpha、beta 參數正確初始化 |
| `test_mean_variance` | 均值為 0.5，方差大於 0 |
| `test_log_likelihood_valid` | 有效概率的對數似然為有限值；邊界值趨近無窮 |
| `test_invalid_probability` | 無效概率（<0 或 >1）返回 $-\infty$ |

---

## 3. 後驗更新測試 (Posterior Tests)

### 3.1 Normal-Normal 共軛更新

測試類別：`TestPosteriorUpdateNormal`

#### 數學原理

當似然函數為高斯分佈且先驗也是高斯分佈時，後驗分佈也是高斯分佈。這稱為**共軛先驗**關係。

**似然函數**（數據 $D = \{x_1, ..., x_n\}$）：
$$p(D | \mu, \sigma^2) = \prod_{i=1}^{n} \mathcal{N}(x_i | \mu, \sigma_l^2)$$

**先驗**：
$$\mu \sim \mathcal{N}(\mu_0, \sigma_0^2)$$

**後驗均值**（閉式解）：
$$\mu_n = \frac{\frac{\mu_0}{\sigma_0^2} + \frac{n\bar{x}}{\sigma_l^2}}{\frac{1}{\sigma_0^2} + \frac{n}{\sigma_l^2}}$$

**後驗方差**：
$$\sigma_n^2 = \left( \frac{1}{\sigma_0^2} + \frac{n}{\sigma_l^2} \right)^{-1}$$

這相當於**精度（precision）的加法**：
$$\text{Precision}_{\text{posterior}} = \text{Precision}_{\text{prior}} + n \cdot \text{Precision}_{\text{likelihood}}$$

#### 測試用例說明

| 測試方法 | 數學驗證 |
|---------|---------|
| `test_perfect_prior` | 當數據完全符合先驗時，後驗均值接近數據均值；後驗方差減小 |
| `test_empty_data` | 無數據時，後驗等於先驗（無更新） |
| `test_uncertain_prior` | 大方差先驗（不確定）時，後驗更接近數據 |

### 3.2 Beta-Binomial 共軛更新

測試類別：`TestPosteriorUpdateBetaBinomial`

#### 數學原理

二項似然與 Beta 先驗構成共軛對：

**似然函數**（成功率 $\theta$，試驗 $n$ 次，成功 $k$ 次）：
$$p(k | n, \theta) = \binom{n}{k} \theta^k (1-\theta)^{n-k}$$

**先驗**：
$$\theta \sim \text{Beta}(\alpha, \beta)$$

**後驗**：
$$\theta | k \sim \text{Beta}(\alpha + k, \beta + n - k)$$

這意味著：
- $\alpha$ 增加 $k$（成功次數）
- $\beta$ 增加 $n - k$（失敗次數）

#### 測試用例說明

| 測試方法 | 數學驗證 |
|---------|---------|
| `test_uniform_prior` | 均勻先驗 Beta(1,1) 更新後：$\alpha' = 1 + k$，$\beta' = 1 + (n-k)$ |
| `test_strong_prior` | 強先驗 Beta(50,50) 將後驗拉向 0.5，但數據 p=0.9 的證據會使後驗介於 0.5 和 0.9 之間 |

---

## 4. MCMC 測試 (MCMC Tests)

測試類別：`TestMetropolisHastings`

### 數學原理

Metropolis-Hastings 演算法是馬爾科夫鏈蒙特卡羅（MCMC）的核心方法，用於從複雜後驗分佈中採樣。

**演算法步驟**：

1. **提議分佈**：從提議分佈 $q(x' | x_t)$ 採樣候選點 $x'$
2. **接受概率**：
$$a = \min\left(1, \frac{p(x') q(x_t | x')}{p(x_t) q(x' | x_t)}\right)$$
3. **接受/拒絕**：
   - 生成均勻隨機數 $u \sim U(0,1)$
   - 若 $u < a$，則接受 $x_{t+1} = x'$
   - 否則 $x_{t+1} = x_t$

**對稱提議**：若 $q$ 為對稱分佈（如高斯），$q(x_t | x') = q(x' | x_t)$，則接受概率簡化為：
$$a = \min\left(1, \frac{p(x')}{p(x_t)}\right)$$

**對數形式**（避免下溢）：
$$\log a = \min(0, \log p(x') - \log p(x_t))$$

測試中使用的目標分佈：
$$\log p(x) = -\frac{1}{2}x^2 \quad \Rightarrow \quad p(x) = \mathcal{N}(0, 1)$$

#### 測試用例說說明

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_sample_normal_target` | 採樣 5000 次，樣本均值接近 0（目標分佈均值），容許誤差 < 0.2 |
| `test_samples_vary` | 確認樣本具有足夠變異性（max - min > 1.0），而非全部相同 |

---

## 5. 貝葉斯線性迴歸測試 (Bayesian Regression Tests)

測試類別：`TestBayesianLinearRegression`

### 數學原理

貝葉斯線性迴歸結合似然函數與參數先驗，得出参数的後驗分佈。

**模型**：
$$y = X\beta + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2 I)$$

**似然函數**（精度 $\Lambda = \sigma^{-2}I$）：
$$p(y | X, \beta) \propto |\Lambda|^{n/2} \exp\left(-\frac{1}{2}(y - X\beta)^T \Lambda (y - X\beta)\right)$$

**先驗**：共軛高斯先驗 $\beta \sim \mathcal{N}(\mu_0, \Sigma_0)$

**後驗均值**（閉式解）：
$$\mu_n = \Sigma_n \left( \Sigma_0^{-1}\mu_0 + X^T \Lambda y \right)$$

**後驗協方差**：
$$\Sigma_n = \left( \Sigma_0^{-1} + X^T \Lambda X \right)^{-1}$$

這推廣了普通最小二乘法（OLS）：當先驗精度趨於 0（無信息先驗）時，後驗均值趨於 OLS 估計。

#### 測試用例說明

| 測試方法 | 數學驗證 |
|---------|---------|
| `test_simple_case` | 無噪聲數據 $y = 2x + 1$，後驗係數均值應接近 2 |
| `test_empty_data` | 空數據返回空結果 |
| `test_with_prior` | 強先驗均值為 10，數據支持 $y = 2x$，後驗應介於 2 和 10 之間 |

---

## 6. 貝葉斯因子測試 (Bayes Factor Tests)

測試類別：`TestBayesFactor`

### 數學原理

貝葉斯因子用於比較兩個模型：

$$K = \frac{p(D | M_1)}{p(D | M_2)} = \frac{\int p(\theta_1 | M_1) p(D | \theta_1, M_1) d\theta_1}{\int p(\theta_2 | M_2) p(D | \theta_2, M_2) d\theta_2}$$

**對數貝葉斯因子**：
$$\log K = \sum_{i=1}^{n} (\log p(x_i | M_1) - \log p(x_i | M_2))$$

當模型具有**相同的似然函數結構**（如都是高斯）但**不同參數**時，可以通過對數似然差計算。

#### Jeffrey's 準則（對數貝葉斯因子）

| $\log K$ 範圍 | 解釋 |
|-------------|------|
| $> 0$ | 模型 1 較好 |
| $0 \sim 1$ | 證據可忽略 |
| $1 \sim 3$ | 弱證據 |
| $3 \sim 10$ | 中等證據 |
| $> 10$ | 強證據 |

#### 測試用例說明

| 測試方法 | 數學驗證 |
|---------|---------|
| `test_equal_models` | 相同對數似然時，$\log K \approx 0$（$K \approx 1$） |
| `test_model_1_better` | 模型 1 對數似然更高（-3 vs -15），$\log K > 0$ |
| `test_mismatch_length` | 長度不符時返回 0.0 |

---

## 7. 測試覆蓋總結

```
測試類別                    數學概念
─────────────────────────────────────────────────────────
TestGaussianPrior           高斯分佈、對數似然
TestBetaPrior               Beta 分佈、邊界行為
TestPosteriorUpdateNormal   共軛先驗、精度加法
TestPosteriorUpdateBetaBinomial  二項-共軛更新
TestMetropolisHastings      MCMC、接受概率、採樣收斂
TestBayesianLinearRegression   共軛高斯迴歸、閉式解
TestBayesFactor             模型比較、邊緣似然
```

---

## 8. 關鍵數學要點

1. **共軛先驗**：使後驗計算化為簡單的參數更新
2. **精度（Precision）**：方差的倒數，共軛更新時直接相加
3. **對數空間**：避免概率乘法下的數值下溢
4. **MCMC 收斂**：通過樣本均值和變異性診斷
5. **貝葉斯因子**：模型證據的比值，自動考慮奧卡姆剃刀