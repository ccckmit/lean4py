# Gaussian Process 高斯過程

## 1. 高斯過程定義

高斯過程（Gaussian Process，簡稱 GP）是一種强大的非參數概率模型，用於回歸和分類任務。

**定義**：高斯過程是隨機變量的集合，其中任意有限個變量服從聯合多元正態分佈。

```math
f(x) \sim \mathcal{GP}(m(x), k(x, x'))
```

形式上，一個高斯過程由均值函數和協方差函數（核函數）完全指定。

### 為何使用高斯過程？

- **非參數靈活性**：不像引數化模型，高斯過程的複雜度隨數據增長
- **概率預測**：不僅預測均值，還預測不确定性（方差）
- **理論優美**：建立在堅實的概率論基礎上

---

## 2. 均值函數與協方差函數

### 均值函數 m(x)

均值函數表示在輸入 x 處的先驗期望值：

```math
m(x) = \mathbb{E}[f(x)]
```

通常我們設均值函數為零（centered GP），因為數據可以預先中心化。

### 協方差函數 k(x, x')

協方差函數（核函數）衡量兩個輸入點函數值的相關性：

```math
k(x, x') = \text{Cov}(f(x), f(x')) = \mathbb{E}[(f(x) - m(x))(f(x') - m(x'))]
```

協方差函數必須是**正定**的，保證生成的協方差矩陣始終有效。

---

## 3. 核函數（Kernel Functions）

核函數決定了高斯過程的性質，是 GP 的核心組件。

### 3.1 RBF / 高斯核 / 指數二次核

代碼實現（`gaussian_process.py:7-23`）：
```python
def rbf_kernel(x1, x2, length_scale=1.0):
    squared_dist = sum((x1[i] - x2[i]) ** 2 for i in range(len(x1)))
    return math.exp(-squared_dist / (2 * length_scale ** 2))
```

數學表達式：
```math
k_{\text{RBF}}(x, x') = \exp\left(-\frac{\|x - x'\|^2}{2\ell^2}\right)
```

**特性**：
- 無限光滑（任意階導數連續）
- `length_scale ℓ` 控制函數變化的特徵長度
- ℓ 越大，函數越平滑；ℓ 越小，函數變化越劇烈

### 3.2 Matern 核

Matern 核提供了更大的靈活性：

```math
k_{\text{Matern}}(r) = \frac{1}{\Gamma(\nu) 2^{\nu-1}} \left(\frac{\sqrt{2\nu} \cdot r}{\ell}\right)^\nu K_\nu\left(\frac{\sqrt{2\nu} \cdot r}{\ell}\right)
```

其中 r = ||x - x'||，K_ν 為修正 Bessel 函數。

常見特例：
- **ν = 3/2**：一次導數均方可微
- **ν = 5/2**：二次導數均方可微

### 3.3 周期的綠核（Periodic Kernel）

用於建模具有固有週期性的函數：

```math
k_{\text{Periodic}}(x, x') = \exp\left(-\frac{2\sin^2(\pi |x - x'| / p)}{\ell^2}\right)
```

其中 p 為週期長度。

---

## 4. 後驗預測

### 4.1 預測分佈推導

假設觀測數據：
```math
y = f(X) + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma_n^2 I)
```

其中 f(X) 服從 GP 先驗。

預測新輸入 x* 的輸出 f*：

```math
f^* \mid X, y, x^* \sim \mathcal{N}(\mu^*, \Sigma^*)
```

### 4.2 後驗均值

代碼實現（`gaussian_process.py:78-84`）：
```python
# Mean: k*^T @ K_inv @ y
mean = sum(k_star[i][j] * sum(self.K_inv[j][k] * self.y_train[k] 
                              for k in range(n_train))
          for j in range(n_train))
```

數學表達式：
```math
\mu^* = k_*^T (K + \sigma_n^2 I)^{-1} y
```

### 4.3 後驗方差

代碼實現（`gaussian_process.py:86-97`）：
```python
# Variance: k(x,x) - k*^T @ K_inv @ k*
k_xx = self.kernel(X_test[i], X_test[i])
temp = [sum(self.K_inv[j][k] * k_star[i][k] for k in range(n_train))
        for j in range(n_train)]
k_Kinv_k = sum(k_star[i][j] * temp[j] for j in range(n_train))
variances.append(max(k_xx - k_Kinv_k, 1e-10))
```

數學表達式：
```math
\Sigma^* = k(x^*, x^*) - k_*^T (K + \sigma_n^2 I)^{-1} k_*
```

**關鍵洞察**：
- 預測方差自動考慮數據點之間的相關性
- 在訓練數據點附近，方差減小（不確定性降低）
- 遠離訓練數據，方差趨近於先驗方差

---

## 5. 高斯過程回歸

### 5.1 回歸流程

本模組實現的高斯過程回歸流程（`GaussianProcessRegressor` 類）：

1. **初始化**：選擇核函數和噪聲水準
2. **訓練**：計算核矩陣 K 並求逆
3. **預測**：計算後驗均值和方差

代碼實現（`gaussian_process.py:26-99`）：

```python
class GaussianProcessRegressor:
    def __init__(self, kernel=None, noise=1e-8):
        self.kernel = kernel if kernel else rbf_kernel
        self.noise = noise
        self.K_inv = None

    def fit(self, X, y):
        # 計算核矩陣
        K = [[self.kernel(X[i], X[j]) for j in range(n)] for i in range(n)]
        # 加入噪聲
        for i in range(n):
            K[i][i] += self.noise
        # 求逆
        self.K_inv = self._invert_matrix(K)

    def predict(self, X_test):
        # 後驗均值和方差計算
        ...
```

### 5.2 方便函數

代碼實現（`gaussian_process.py:141-164`）：
```python
def predict_gp(X_train, y_train, X_test, kernel=None, noise=1e-8):
    """GP 回歸的便捷函數"""
    gp = GaussianProcessRegressor(kernel=kernel, noise=noise)
    gp.fit(X_train, y_train)
    means, variances = gp.predict(X_test)
    stds = [math.sqrt(v) for v in variances]
    return means, stds
```

### 5.3 使用範例

```python
from lean4py import predict_gp, rbf_kernel

X_train = [[0.0], [1.0], [2.0], [3.0]]
y_train = [0.0, 1.0, 1.5, 2.0]
X_test = [[0.5], [1.5], [2.5]]

means, stds = predict_gp(X_train, y_train, X_test)
# means: 後驗均值
# stds: 後驗標準差
```

---

## 6. 超參數優化（邊際似然）

### 6.1 邊際似然

高斯過程的邊際似然（marginal likelihood）是在所有可能的底層函數上的積分：

```math
p(y \mid X, \theta) = \int p(y \mid f, X) p(f \mid X, \theta) \, df
```

封閉形式為：
```math
\log p(y \mid X, \theta) = -\frac{1}{2} y^T (K_\theta + \sigma_n^2 I)^{-1} y - \frac{1}{2} \log |K_\theta + \sigma_n^2 I| - \frac{n}{2} \log 2\pi
```

### 6.2 優化目標

最大化邊際似然等价於最小化：
```math
\mathcal{L}(\theta) = y^T K^{-1} y + \log |K| + n \log 2\pi
```

### 6.3 解釋

邊際似然包含兩項權衡：
- **數據擬合項**：y^T K^{-1} y — 偏好模型擬合數據
- **複雜度懲罰項**：log |K| — 偏好簡單（平滑）的函數

這使得 GP 具有天然的 **奧卡姆剃刀** 特性，自動防止過擬合。

### 6.4 數值方法

實際中常用：
- 梯度下降（需要計算邊際似然對參數的梯度）
- L-BFGS-B
- 暴力網格搜索（適用於少量參數）

---

## 7. 與貝葉斯線性回歸的關係

### 7.1 貝葉斯線性回歸

設線性模型：
```math
f(x) = x^T w, \quad w \sim \mathcal{N}(0, \Sigma_p)
```

預測分佈：
```math
f^* \mid x^*, X, y \sim \mathcal{N}(\phi(x^*)^T \Sigma_p \Phi (K + \sigma_n^2 I)^{-1} y, \phi(x^*)^T \Sigma_p \phi(x^*) - \phi(x^*)^T \Sigma_p \Phi (K + \sigma_n^2 I)^{-1} \Phi^T \Sigma_p \phi(x^*))
```

### 7.2 作為無限維拓展

**核心洞察**：高斯過程可以視為**無限維**的貝葉斯線性回歸。

取特徵映射 φ(x)，使得：
```math
k(x, x') = \phi(x)^T \phi(x')
```

則 GP 回歸與貝葉斯線性回歸**數學上等價**。

### 7.3 區別

| 特點 | 貝葉斯線性回歸 | 高斯過程 |
|------|--------------|---------|
| 特徵維度 | 有限維 φ(x) | 無限維（核函數） |
| 計算複雜度 | O(nd²) | O(n³) |
| 靈活性 | 受限於特徵選擇 | 自適應 |

### 7.4 直觀理解

貝葉斯線性回歸的權重空間視角：
```math
\text{GP}(m, k) \approx \lim_{d \to \infty} \text{BayesianLinearRegression}(x \mapsto \phi_d(x))
```

這解釋了為何 GP 能夠擬合任意複雜函數——當特徵維度趨於無窮時，模型的表示能力趨於無窮。

---

## 8. 總結

高斯過程是現代機器學習的重要工具，其核心思想：

1. **先驗指定**：通過核函數 k(x, x') 指定函數空間的平滑性假設
2. **後驗推斷**：利用條件正態分佈的解析性質，獲得封閉形式的后驗
3. **預測不確定性**：自然輸出預測方差，量化認知不確定性
4. **理論基礎**：連接貝葉斯非參數統計與函數空間分析

本模組實現了完整的高斯過程回歸功能，包括 RBF 核、噪聲處理和矩陣求逆。實際應用中，可根據問題特性選擇或設計核函數，並通過邊際似然優化超參數。

---

## 參考文獻

1. Rasmussen, C. E., & Williams, C. K. I. (2006). *Gaussian Processes for Machine Learning*. MIT Press.
2. Bishop, C. M. (2006). *Pattern Recognition and Machine Learning*. Springer.
3. Schölkopf, B., & Smola, A. J. (2002). *Learning with Kernels*. MIT Press.