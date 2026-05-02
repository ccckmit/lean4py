# 變分推斷 (Variational Inference)

## 概述

變分推斷（Variational Inference，簡稱 VI）是一種用於近似計算貝葉斯推斷中後驗分佈的自動化方法。當我們有觀測數據 $x$ 和潛在變量 $z$ 時，後驗分佈 $p(z|x) = \frac{p(x,z)}{p(x)}$ 通常難以計算，因為邊緣似然 $p(x)$ 需要對所有潛在變量進行積分：

$$p(x) = \int p(x|z)p(z) dz$$

當 $z$ 的維度很高或分佈結構複雜時，這個積分是無法解析求解的。變分推斷的核心思想是：**用一個簡單的引數化分佈 $q(z)$ 來近似真實的後驗分佈 $p(z|x)$**。

---

## 1. 變分推斷的基本框架

我們引入一個候選分佈族 $\mathcal{Q}$，通常稱為**變分分佈族（variational family）**。我們的目標是找到這個族中與真實後驗最接近的分佈 $q^*(z)$。

### KL 散度目標

衡量兩個分佈之間的接近程度，我們使用 KL 散度（Kullback-Leibler divergence）：

$$\text{KL}(q \| p) = \int q(z) \log \frac{q(z)}{p(z|x)} dz$$

由於 $p(z|x) = \frac{p(x,z)}{p(x)}$，我們有：

$$\text{KL}(q \| p) = \int q(z) \log \frac{q(z)p(x)}{p(x,z)} dz = \log p(x) - \mathcal{L}(q)$$

其中 $\mathcal{L}(q)$ 是**證據下界（ELBO）**，定義為：

$$\mathcal{L}(q) = \mathbb{E}_q[\log p(x,z)] - \mathbb{E}_q[\log q(z)]$$

由於 $\log p(x)$ 是一個與 $q$ 無關的常數，最小化 $\text{KL}(q \| p)$ 等價於**最大化 ELBO**。

---

## 2. 證據下界（ELBO）

ELBO（Evidence Lower Bound）是變分推斷的核心目標函數：

$$\mathcal{L}(q) = \mathbb{E}_q[\log p(x|z)] + \mathbb{E}_q[\log p(z)] - \mathbb{E}_q[\log q(z)]$$

### ELBO 的兩種分解形式

**形式一：似然減去 KL 散度**
$$\mathcal{L}(q) = \mathbb{E}_q[\log p(x|z)] - \text{KL}(q(z) \| p(z))$$

這表明 ELBO 由兩部分組成：
- **重構誤差（Reconstruction error）**：$\mathbb{E}_q[\log p(x|z)]$，衡量模型對觀測數據的重構能力
- **先驗正規化項**：$-\text{KL}(q(z) \| p(z))$，確保變分分佈不會偏離先驗太遠

**形式二：標準形式**
$$\mathcal{L}(q) = \mathbb{E}_q[\log p(x,z)] - \mathbb{E}_q[\log q(z)]$$

### 代碼實現

在 `variational_inference.py` 中，ELBO 的計算如下：

```python
def ELBO(
    log_likelihood: Callable[[List[float]], float],
    log_prior: Callable[[List[float]], float],
    q: MeanFieldVI,
    n_samples: int = 100
) -> float:
    samples = q.sample(n_samples)
    
    # E_q[log p(x|z)]
    exp_likelihood = sum(log_likelihood(s) for s in samples) / len(samples)
    
    # E_q[log p(z)] - E_q[log q(z)]
    exp_prior = sum(log_prior(s) for s in samples) / len(samples)
    
    # KL term (approximation for mean-field Gaussian)
    kl = 0.0
    for p in q.variational_params:
        kl += -0.5 * (1 + p.get('log_var', 0) - p['mean']**2 - math.exp(p.get('log_var', 0)))
    
    return exp_likelihood - kl
```

對於均場高斯變分分佈，KL 項可以解析計算為：

$$\text{KL}(q \| p) = -\frac{1}{2}\sum_{j=1}^{d} \left(1 + \log\sigma_j^2 - \mu_j^2 - \sigma_j^2\right)$$

---

## 3. 均場近似（Mean Field Approximation）

**均場近似**是變分推斷中最常用的假設。它假設潛在變量之間相互獨立，即：

$$q(z) = \prod_{i=1}^{d} q_i(z_i)$$

其中每個 $q_i(z_i)$ 是一個簡單的引數化分佈（如高斯分佈、伯努利分佈等）。

### 優點
- 大大簡化了計算
- 每個變量可以獨立更新

### 缺點
- 忽略了變量之間的相關性
- 可能導致過度自信的近似

### 代碼實現

`MeanFieldVI` 類實現了均場變分推斷：

```python
class MeanFieldVI:
    def __init__(self, n_params: int, param_types: Optional[List[str]] = None):
        self.n_params = n_params
        if param_types is None:
            param_types = ['normal'] * n_params
        self.param_types = param_types
        
        # 對於高斯分佈：存儲均值和對數方差
        self.variational_params = []
        for _ in range(n_params):
            self.variational_params.append({'mean': 0.0, 'log_var': 0.0})
```

每個潛在變量 $z_i$ 的變分分佈為：
$$q_i(z_i) = \mathcal{N}(\mu_i, \sigma_i^2)$$

其中 $\mu_i$ 是均值，$\sigma_i^2 = e^{\log\sigma_i^2}$ 是方差。

---

## 4. 坐標上升變分推斷（CAVI）

**坐標上升變分推斷（Coordinate Ascent Variational Inference）** 是一種迭代優化算法，每次只更新一個變分參數，同時固定其他參數。

### 更新公式

對於均場近似，每個變分參數 $q_j(z_j)$ 的最優更新為：

$$\log q_j^*(z_j) \propto \mathbb{E}_{-q_j}[\log p(x, z)]$$

即：
$$q_j^*(z_j) \propto \exp\left(\mathbb{E}_{-q_j}[\log p(x, z)]\right)$$

### 算法流程

```
初始化：設置所有變分參數的初始值
重複直到收斂：
    對於每個 j = 1, ..., d：
        更新 q_j(z_j) 根據 ∝ exp(E[-q_j][log p(x,z)])
    計算 ELBO
    檢查收斂準則
```

### 代碼實現

```python
def mean_field_update(
    log_likelihood: Callable[[List[float]], float],
    log_prior: Callable[[List[float]], float],
    q: MeanFieldVI,
    idx: int,
    n_samples: int = 50
) -> dict:
    samples = q.sample(n_samples)
    
    # 使用有限差分近似梯度
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

---

## 5. 隨機變分推斷（SVI）

**隨機變分推斷（Stochastic Variational Inference）** 是對 CAVI 的隨機擴展，允許使用隨機梯度上升來優化 ELBO。這對於大規模數據集和難以計算完整數據似然的模型特別有用。

### 隨機梯度估計

SVI 的核心是用**隨機估計器**替換完整數據梯度：

$$\nabla_\theta \mathcal{L} \approx \frac{1}{S} \sum_{s=1}^{S} \nabla_\theta \log q(z^{(s)}; \theta) \cdot \left[\log p(x, z^{(s)}) - \log q(z^{(s)}; \theta)\right]$$

其中 $z^{(s)} \sim q(z; \theta)$ 是從變分分佈中採樣的。

### 小批量擴展

對於大型數據集，我們可以使用小批量（mini-batch）來估計梯度：

$$\nabla_\theta \mathcal{L} \approx \frac{N}{B} \sum_{i \in \mathcal{B}} \nabla_\theta \mathcal{L}_i$$

其中 $N$ 是總樣本數，$B$ 是小批量大小，$\mathcal{B}$ 是小批量索引集合。

---

## 6. 重參數化技巧（Reparameterization Trick）

重參數化技巧是實現**可導變分推斷**的關鍵技術。對於高斯變分分佈 $q_\phi(z) = \mathcal{N}(\mu_\phi, \sigma_\phi^2)$，我們將採樣過程重參數化為：

$$z = \mu + \sigma \cdot \epsilon, \quad \epsilon \sim \mathcal{N}(0, I)$$

### 為什麼需要重參數化？

直接從變分分佈採樣的結果 $\nabla_\phi z \sim \nabla_\phi q_\phi(z)$ 是一個隨機量，不能直接用於梯度下降。通過重參數化：

$$z = g(\phi, \epsilon)$$

梯度可以通過以下方式計算：

$$\nabla_\phi \mathbb{E}_q[ f(z) ] = \mathbb{E}_\epsilon \left[ \nabla_\phi f(g(\phi, \epsilon)) \right]$$

### 代碼實現

模組中的採樣方法已經隱式使用了重參數化：

```python
def sample(self, n_samples: int = 1) -> List[List[float]]:
    samples = []
    for _ in range(n_samples):
        sample = []
        for p in self.variational_params:
            std = math.sqrt(math.exp(p.get('log_var', 0)))
            z = random.gauss(p['mean'], std)  # z = μ + σ·ε
            sample.append(z)
        samples.append(sample)
    return samples
```

這裡 `random.gauss(p['mean'], std)` 採樣自 $\mathcal{N}(\mu, \sigma^2)$，相當於從標準正態分佈採樣 $\epsilon \sim \mathcal{N}(0,1)$，然後計算 $z = \mu + \sigma \cdot \epsilon$。

---

## 7. 貝葉斯神經網絡的變分推斷

**貝葉斯神經網絡（Bayesian Neural Networks）** 將網絡權重視為隨機變量，而非確定性參數。這使得模型能夠自然地量化預測不確定性。

### 數學框架

對於權重 $w$ 和偏差 $b$，我們有：
- **先驗**：$p(w), p(b)$（通常選擇高斯先驗）
- **似然**：$p(y|x, w, b)$（如分類的 softmax 或回歸的高斯）
- **後驗**：$p(w, b|x, y)$（我們希望近似的目標）

### 變分推斷應用

使用均場近似，假設權重相互獨立：

$$q(w, b) = \prod_i q(w_i) \prod_j q(b_j)$$

其中每個 $q(w_i) = \mathcal{N}(\mu_i, \sigma_i^2)$。

### 代碼實現

`variational_linear_regression` 展示了變分推斷在貝葉斯線性回歸中的應用：

```python
def variational_linear_regression(
    X: List[List[float]],
    y: List[float],
    n_samples: int = 100
) -> Tuple[List[float], List[float]]:
    n = len(X)
    m = len(X[0])
    
    # 對數似然：log p(y|X,w)
    def log_likelihood(w):
        pred = [sum(w[j] * X[i][j] for j in range(m)) for i in range(n)]
        return -0.5 * sum((y[i] - pred[i])**2 for i in range(n))
    
    # 對數先驗：標準正態 prior
    def log_prior(w):
        return -0.5 * sum(wi**2 for wi in w)
    
    # 運行 VI
    q = coordinate_ascent_vi(log_likelihood, log_prior, m)
    
    # 獲取後驗統計量
    posterior_means = q.get_means()
    posterior_stds = [0.1] * m
    
    return posterior_means, posterior_stds
```

### 預測分佈

給定新輸入 $x^*$，貝葉斯預測通過邊緣化權重得到：

$$p(y^*|x^*) = \int p(y^*|x^*, w) \, q(w) \, dw$$

這可以通過蒙特卡洛採樣估計：

```python
def predict(x_new, q, n_samples=100):
    samples = q.sample(n_samples)
    predictions = []
    for w in samples:
        y_pred = sum(w[j] * x_new[j] for j in range(len(x_new)))
        predictions.append(y_pred)
    return predictions  # 返回預測分佈的採樣
```

---

## 模組函數一覽

| 函數 | 說明 |
|------|------|
| `MeanFieldVI` | 均場變分推斷類，用於存儲和操作變分參數 |
| `ELBO` | 計算證據下界 |
| `mean_field_update` | 單個變分參數的坐標上升更新 |
| `coordinate_ascent_vi` | 完整 CAVI 算法實現 |
| `variational_linear_regression` | 基於 VI 的貝葉斯線性回歸 |

---

## 參考文獻

1. Blei, D. M., Kucukelbir, A., & McAuliffe, J. D. (2017). Variational inference: A review for statisticians. *Journal of the American Statistical Association*.
2. Kingma, D. P., & Welling, M. (2014). Auto-encoding variational Bayes. *International Conference on Machine Learning*.
3. Murphy, K. P. (2012). *Machine Learning: A Probabilistic Perspective*. MIT Press.