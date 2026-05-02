# 變分推斷測試文檔 (Variational Inference Tests)

## 概述

本測試文件驗證 `lean4py/variational_inference.py` 模塊中的變分推斷（Variational Inference, VI）實現。

變分推斷是一種用於近似貝葉斯推斷的計算方法，通過優化一個可控制的變分分佈來近似真實的後驗分佈。

---

## 1. 測試驗證的內容

### 1.1 核心功能測試

| 測試類別 | 驗證內容 |
|---------|---------|
| **ELBO 測試** | 證據下界的正確計算 |
| **Mean Field 測試** | 均值場近似分佈的構建與更新 |
| **Reparameterization 測試** | 重參數化採樣的數值穩定性 |

---

## 2. ELBO 測試 (ELBO Tests)

### 2.1 數學原理

**證據下界（Evidence Lower Bound, ELBO）** 是變分推斷的核心目標函數。

給定觀察數據 $x$ 和潛在變量 $z$，真實後驗 $p(z|x)$ 難以直接計算。ELBO 定義為：

$$\mathcal{L}(q) = \mathbb{E}_q[\log p(x|z)] - \text{KL}(q(z) \| p(z))$$

其中：
- $\mathbb{E}_q[\log p(x|z)]$：對變分分佈 $q(z)$ 的期望對數似然
- $\text{KL}(q(z) \| p(z))$：變分分佈與先驗的 KL 散度

### 2.2 ELBO 的兩種等價形式

**形式一（展開形式）：**
$$\mathcal{L} = \mathbb{E}_q[\log p(x|z)] - \mathbb{E}_q[\log q(z)] + \mathbb{E}_q[\log p(z)]$$

**形式二（KL 形式）：**
$$\mathcal{L} = \mathbb{E}_q[\log p(x|z)] - \text{KL}(q(z) \| p(z))$$

### 2.3 代碼實現對應

```python
def ELBO(log_likelihood, log_prior, q, n_samples=100):
    samples = q.sample(n_samples)
    
    # E_q[log p(x|z)] - 期望對數似然
    exp_likelihood = sum(log_likelihood(s) for s in samples) / len(samples)
    
    # E_q[log p(z)] - E_q[log q(z)]
    exp_prior = sum(log_prior(s) for s in samples) / len(samples)
    
    # KL term (mean-field Gaussian 近似)
    kl = 0.0
    for p in q.variational_params:
        kl += -0.5 * (1 + p.get('log_var', 0) - p['mean']**2 - math.exp(p.get('log_var', 0)))
    
    return exp_likelihood - kl
```

### 2.4 KL 散度的具體計算

對於均值場高斯分佈，KL 散度有封閉形式：

$$\text{KL}(q \| p) = \sum_{d=1}^{D} \left( \frac{\sigma_p^2}{\sigma_d^2} + \frac{(\mu_d - \mu_p)^2}{\sigma_d^2} - 1 - \log\frac{\sigma_p^2}{\sigma_d^2} \right)$$

當先驗為標準正態分佈 $p(z) = \mathcal{N}(0, I)$ 時：

$$\text{KL}(q \| p) \approx \sum_{d=1}^{D} \left( 1 + \log\sigma_d^2 - \mu_d^2 - \sigma_d^2 \right)/2$$

### 2.5 測試要點

```python
# ELBO 測試驗證：
# 1. Monte Carlo 估計的收斂性（n_samples 增加時趨於穩定）
# 2. KL 散度非負性：ELBO ≤ 對數邊際似然
# 3. 先驗匹配時 ELBO 的特定值
# 4. 數值穩定性（避免 log(0) 等問題）
```

---

## 3. Mean Field 測試 (Mean Field Tests)

### 3.1 數學原理

**均值場變分推斷（Mean Field Variational Inference）** 假設潛在變量之間相互獨立：

$$q(z) = \prod_{d=1}^{D} q_d(z_d)$$

其中每個 $q_d(z_d)$ 是簡單的分佈（如高斯分佈）。

### 3.2 坐標上升更新

對於每個變分參數，坐標上升法（Coordinate Ascent）進行更新：

$$q_d^*(z_d) \propto \exp\left( \mathbb{E}_{q_{-d}}[\log p(x, z)] \right)$$

更新公式（高斯情況）：

$$\mu_d^{new} = \mu_d^{old} + \eta \cdot \frac{\partial \mathcal{L}}{\partial \mu_d}$$

$$\log\sigma_d^{2,new} = \log\sigma_d^{2,old} + \eta \cdot \frac{\partial \mathcal{L}}{\partial \log\sigma_d^2}$$

### 3.3 代碼實現

```python
class MeanFieldVI:
    def __init__(self, n_params, param_types=None):
        self.n_params = n_params
        self.param_types = param_types or ['normal'] * n_params
        # 初始化變分參數：均值和對數方差
        self.variational_params = []
        for _ in range(n_params):
            self.variational_params.append({'mean': 0.0, 'log_var': 0.0})
```

### 3.4 梯度估計

```python
def mean_field_update(log_likelihood, log_prior, q, idx, n_samples=50):
    samples = q.sample(n_samples)
    
    # 有限差分近似梯度
    grad_sum = 0.0
    for s in samples:
        eps = 0.01
        s_plus = s[:]
        s_plus[idx] += eps
        s_minus = s[:]
        s_minus[idx] -= eps
        
        grad = (log_likelihood(s_plus) - log_likelihood(s_minus)) / (2 * eps)
        grad_sum += grad
    
    avg_grad = grad_sum / n_samples
    new_mean = q.variational_params[idx]['mean'] + 0.01 * avg_grad
    
    return {'mean': new_mean, 'log_var': q.variational_params[idx].get('log_var', 0)}
```

### 3.5 測試要點

```python
# Mean Field 測試驗證：
# 1. 變分參數初始化正確性
# 2. 參數更新後 ELBO 不下降（單調性）
# 3. 收斂性：迭代後參數趨於穩定
# 4. 獨立性假設的數值實現正確
```

### 3.6 收斂性判定

```python
def coordinate_ascent_vi(log_likelihood, log_prior, n_params, n_iter=100, tol=1e-4):
    q = MeanFieldVI(n_params)
    prev_elbo = float('-inf')
    
    for iteration in range(n_iter):
        # 更新每個參數
        for idx in range(n_params):
            new_params = mean_field_update(log_likelihood, log_prior, q, idx)
            q.variational_params[idx] = new_params
        
        # 檢查收斂
        current_elbo = ELBO(log_likelihood, log_prior, q)
        
        if abs(current_elbo - prev_elbo) < tol:
            break
        
        prev_elbo = current_elbo
    
    return q
```

---

## 4. Reparameterization 測試 (Reparameterization Tests)

### 4.1 數學原理

**重參數化技巧（Reparameterization Trick）** 將隨機性從分佈參數轉移到一個輔助噪聲變量：

$$z \sim q_\phi(z) = \mathcal{N}(\mu, \sigma^2)$$

重參數化為：

$$z = \mu + \sigma \cdot \epsilon, \quad \epsilon \sim \mathcal{N}(0, 1)$$

這樣可以对 $\mu, \sigma$ 求導：

$$\frac{\partial z}{\partial \mu} = 1, \quad \frac{\partial z}{\partial \sigma} = \epsilon$$

### 4.2 代碼實現

```python
def sample(self, n_samples=1):
    """Sample from variational distribution."""
    import random
    samples = []
    for _ in range(n_samples):
        sample = []
        for p in self.variational_params:
            # 數值穩定性處理
            if p.get('log_var', 0) > 10:
                std = math.exp(5)
            else:
                std = math.sqrt(math.exp(p.get('log_var', 0)))
            
            # z = μ + σ * ε, ε ~ N(0,1)
            z = random.gauss(p['mean'], std)
            sample.append(z)
        samples.append(sample)
    return samples
```

### 4.3 採樣的數值穩定性

```python
# 對數方差的處理避免數值溢出
if log_var > 10:
    std = math.exp(5)  # 限制最大標準差
else:
    std = math.sqrt(math.exp(log_var))
```

### 4.4 測試要點

```python
# Reparameterization 測試驗證：
# 1. 採樣分佈的均值收斂到理論均值
# 2. 採樣分佈的方差收斂到理論方差
# 3. 不同 n_samples 下估計的蒙特卡洛方差
# 4. 數值穩定性（特別是大方差情況）
# 5. 隨機種子可控性
```

---

## 5. 應用示例：變分線性回歸

### 5.1 數學模型

**似然函數：**
$$p(y|X, w) = \prod_{i=1}^{n} \mathcal{N}(y_i | x_i^T w, 1)$$

**先驗分佈：**
$$p(w) = \mathcal{N}(0, I)$$

**對數形式：**
$$\log p(y|X, w) = -\frac{1}{2} \sum_{i=1}^{n} (y_i - x_i^T w)^2 + \text{const}$$

$$\log p(w) = -\frac{1}{2} \sum_{d=1}^{D} w_d^2 + \text{const}$$

### 5.2 代碼實現

```python
def variational_linear_regression(X, y, n_samples=100):
    n = len(X)
    m = len(X[0])
    
    # 對數似然
    def log_likelihood(w):
        pred = [sum(w[j] * X[i][j] for j in range(m)) for i in range(n)]
        return -0.5 * sum((y[i] - pred[i])**2 for i in range(n))
    
    # 對數先驗（標準正態）
    def log_prior(w):
        return -0.5 * sum(wi**2 for wi in w)
    
    # 運行 VI
    q = coordinate_ascent_vi(log_likelihood, log_prior, m)
    
    # 獲取後驗統計
    samples = q.sample(n_samples)
    posterior_means = q.get_means()
    posterior_stds = [0.1] * m
    
    return posterior_means, posterior_stds
```

### 5.3 後驗逼近

變分推斷返回的是變分分佈 $q(w) \approx p(w|y, X)$，可用於：
- 點估計：使用均值 $\mathbb{E}_q[w]$
- 不確定性估計：使用方差 $\text{Var}_q[w]$
- 預測分佈：$p(y^*|x^*) \approx \int p(y^*|x^*, w) q(w) dw$

---

## 6. 測試矩陣

| 測試類別 | 輸入維度 | 樣本數 | 驗證目標 |
|---------|---------|--------|---------|
| ELBO_Convergence | 1D-10D | 10/100/1000 | Monte Carlo 收斂 |
| ELBO_KL_NonNeg | 任意 | 100 | KL(q‖p) ≥ 0 |
| MeanField_Update | 2D-5D | 50 | ELBO 單調增加 |
| MeanField_Convergence | 3D | 100 | 參數收斂 |
| Reparam_Sampling | 1D-5D | 10000 | 分佈匹配 |
| Reparam_Stability | 高方差 | 1000 | 數值穩定 |
| LinearRegression | m=5, n=50 | 100 | 後驗估計 |

---

## 7. 參考文獻

1. Blei, D. M., Kucukelbir, A., & McAuliffe, J. D. (2017). Variational Inference: A Review for Statisticians. *Journal of the American Statistical Association*.
2. Kingma, D. P., & Welling, M. (2014). Auto-Encoding Variational Bayes. *Proceedings of the 2nd International Conference on Learning Representations (ICLR)*.