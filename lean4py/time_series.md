# 時間序列分析 (Time Series Analysis)

本模組提供時間序列分析的基礎功能，包括移動平均、自身相關函數（ACF）及偏自身相關函數（PACF）的計算。

---

## 1. 時間序列基礎 (Time Series Fundamentals)

**時間序列**是指一個隨機變量序列 $\{X_t\}$，其中 $t$ 表示時間索引，通常為整數或離散的時間點。

$$X = \{X_t : t \in \mathbb{T}\}$$

常見的時間序列包括：
- 股價數據 $\{P_t\}$
- 溫度觀測 $\{T_t\}$
- 季度銷售額 $\{S_t\}$

---

## 2. 穩定性 (Stationarity)

### 嚴格穩態 (Strict Stationarity)

若對於所有時間點 $t_1, t_2, \ldots, t_n$ 和任意時間平移 $k$，滿足：

$$(X_{t_1}, X_{t_2}, \ldots, X_{t_n}) \overset{d}{=} (X_{t_1+k}, X_{t_2+k}, \ldots, X_{t_n+k})$$

則稱該時間序列為**嚴格平穩**（strictly stationary）。

### 弱穩態 (Weak Stationarity / Covariance Stationarity)

若時間序列滿足以下條件，則稱為**弱平穩**或**協方差平穩**：

1. **均值常數**：$E[X_t] = \mu$，對所有 $t$ 成立
2. **方差有限**：$Var(X_t) = E[(X_t - \mu)^2] < \infty$
3. **協方差僅依賴於落後階數**：$Cov(X_t, X_{t+k}) = \gamma(k)$，與 $t$ 無關

弱平穩性較為實用，因為大多數時間序列分析方法都基於此假設。

---

## 3. 自身相關函數 (Autocorrelation Function, ACF)

**自身相關函數**衡量時間序列在不同落後階數下的自身相關程度。

### 樣本自協方差

$$\hat{\gamma}(k) = \frac{1}{n-k} \sum_{t=1}^{n-k} (x_t - \bar{x})(x_{t+k} - \bar{x})$$

### 樣本自身相關係數

$$\hat{\rho}(k) = \frac{\hat{\gamma}(k)}{\hat{\gamma}(0)} = \frac{\hat{\gamma}(k)}{\hat{\sigma}^2}$$

其中：
- $k$ 為落後階數（lag）
- $\hat{\gamma}(0)$ 為方差
- $\hat{\rho}(0) = 1$

### Python 實現

```python
def autocovariance(x: List[float], lag: int = 1) -> float:
    """樣本自協方差計算。"""
    n = len(x)
    if n <= lag:
        return 0.0
    mean_x = sum(x) / n
    total = sum((x[i] - mean_x) * (x[i-lag] - mean_x) for i in range(lag, n))
    return total / (n - lag)

def acf(x: List[float], max_lag: int = 10) -> List[float]:
    """自身相關函數計算。"""
    n = len(x)
    if n < 2:
        return []
    acov = [autocovariance(x, lag) for lag in range(max_lag + 1)]
    var = acov[0]
    if var == 0:
        return [1.0] * (max_lag + 1)  # 常數序列
    return [acov[lag] / var for lag in range(max_lag + 1)]
```

---

## 4. 滑動平均過程 (Moving Average Process, MA)

**MA(q) 過程**定義為：

$$X_t = \varepsilon_t + \theta_1 \varepsilon_{t-1} + \theta_2 \varepsilon_{t-2} + \cdots + \theta_q \varepsilon_{t-q}$$

其中：
- $\{\varepsilon_t\}$ 為白噪音過程，$E[\varepsilon_t] = 0$，$Var(\varepsilon_t) = \sigma^2$
- $\theta_1, \theta_2, \ldots, \theta_q$ 為 MA 參數

### MA(1) 過程

$$X_t = \varepsilon_t + \theta \varepsilon_{t-1}$$

**均值**：$E[X_t] = 0$

**方差**：$Var(X_t) = (1 + \theta^2)\sigma^2$

**自身相關**：
$$\gamma(k) = \begin{cases} (1 + \theta^2)\sigma^2 & k = 0 \\ \theta\sigma^2 & k = 1 \\ 0 & k > 1 \end{cases}$$

### 簡單移動平均

實際應用中的**簡單移動平均**（Simple Moving Average）：

$$\bar{X}_t = \frac{1}{k} \sum_{i=0}^{k-1} X_{t-i}$$

```python
def moving_average(x: List[float], window: int = 3) -> List[float]:
    """簡單移動平均。"""
    if len(x) < window:
        return []
    return [sum(x[i:i+window]) / window for i in range(len(x) - window + 1)]
```

---

## 5. 自回歸過程 (Autoregressive Process, AR)

**AR(p) 過程**定義為：

$$X_t = \phi_1 X_{t-1} + \phi_2 X_{t-2} + \cdots + \phi_p X_{t-p} + \varepsilon_t$$

其中 $\varepsilon_t$ 為白噪音。

### AR(1) 過程

$$X_t = \phi X_{t-1} + \varepsilon_t$$

**均值**：當 $|\phi| < 1$ 時，$E[X_t] = 0$

**方差**：$Var(X_t) = \frac{\sigma^2}{1-\phi^2}$

**自身相關**：
$$\gamma(k) = \frac{\phi^k \sigma^2}{1-\phi^2}, \quad k \geq 0$$

**ACF**：指數衰減 $\rho(k) = \phi^k$

### AR(1) 的平穩性條件

AR(1) 過程平穩當且僅當 $|\phi| < 1$。

---

## 6. ARMA(p,q) 模型

**ARMA(p,q) 過程**結合了 AR 和 MA 過程：

$$X_t = \phi_1 X_{t-1} + \cdots + \phi_p X_{t-p} + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \cdots + \theta_q \varepsilon_{t-q}$$

或用落後算子 $L$ 表示：

$$\phi(L) X_t = \theta(L) \varepsilon_t$$

其中：
- $\phi(L) = 1 - \phi_1 L - \phi_2 L^2 - \cdots - \phi_p L^p$
- $\theta(L) = 1 + \theta_1 L + \theta_2 L^2 + \cdots + \theta_q L^q$

### ARMA 的平穩性與可逆性

- **平穩性**：AR 多項式 $\phi(z) = 0$ 的根都在單位圓外
- **可逆性**：MA 多項式 $\theta(z) = 0$ 的根都在單位圓外

---

## 7. ARIMA 模型

**ARIMA(p, d, q)**（Autoregressive Integrated Moving Average）是 ARMA 與差分的結合：

$$Y_t = (1-L)^d X_t$$

其中 $d$ 為差分階數，使非平穩序列轉化為平穩序列。

### ARIMA 模型表達式

$$\phi(L) (1-L)^d X_t = \theta(L) \varepsilon_t$$

### 常見特例

| 模型 | 特性 |
|------|------|
| I(0) | 平穩序列 |
| I(1) | 單位根過程，通過一次差分變平穩 |
| ARIMA(p, 1, q) | 趨勢平穩，需差分才能平穩 |

---

## 8. 偏自身相關函數 (Partial Autocorrelation Function, PACF)

**PACF** 衡量在移除中間落後階數影響後，$X_t$ 與 $X_{t-k}$ 之間的直接相關性。

### 定義

$$\phi_{kk} = Corr(X_t, X_{t-k} | X_{t-1}, X_{t-2}, \ldots, X_{t-k+1})$$

### PACF 的性質

- **AR(p) 過程**：PACF 在 $k > p$ 後截斷（為零）
- **MA(q) 過程**：PACF 指數衰減

### Python 實現

```python
def partial_acf(x: List[float], max_lag: int = 10) -> List[float]:
    """偏自身相關函數（簡化版）。"""
    if len(x) < 2:
        return []
    return acf(x, max_lag)  # 簡化版本使用 ACF 近似
```

---

## 9. Yule-Walker 方程式

Yule-Walker 方程式建立了 AR 過程中 ACF 與參數之間的關係。

### AR(p) 過程的 Yule-Walker 方程式

$$\gamma(k) = \phi_1 \gamma(k-1) + \phi_2 \gamma(k-2) + \cdots + \phi_p \gamma(k-p), \quad k \geq 1$$

或用矩陣形式：

$$\boldsymbol{\Gamma}_p \boldsymbol{\phi} = \boldsymbol{\gamma}_p$$

其中：
$$\boldsymbol{\Gamma}_p = \begin{pmatrix} \gamma(0) & \gamma(1) & \cdots & \gamma(p-1) \\ \gamma(1) & \gamma(0) & \cdots & \gamma(p-2) \\ \vdots & \vdots & \ddots & \vdots \\ \gamma(p-1) & \gamma(p-2) & \cdots & \gamma(0) \end{pmatrix}$$

### Yule-Walker 估計

用樣本 ACF 替代總體 ACF：

$$\hat{\phi} = \hat{\boldsymbol{\Gamma}}_p^{-1} \hat{\boldsymbol{\gamma}}_p$$

---

## 10. 預測 (Forecasting)

### 最佳線性預測

给定信息集 $I_{t-1} = \{X_{t-1}, X_{t-2}, \ldots\}$，$X_t$ 的最佳線性預測為：

$$\hat{X}_t = E[X_t | I_{t-1}]$$

### AR(p) 的預測

$$\hat{X}_{t+h} = \phi_1 \hat{X}_{t+h-1} + \cdots + \phi_p \hat{X}_{t+h-p}$$

其中當 $j \leq 0$ 時，$\hat{X}_j = X_j$（使用實際觀測值）。

### 預測誤差

$h$ 步預測的均方誤差（MSE）：

$$MSE(h) = \sigma^2 \sum_{j=0}^{h-1} \psi_j^2$$

其中 $\psi_j$ 為 MA 表示係數。

### ARIMA 預測

1. 若 $d > 0$，先對數據進行 $d$ 階差分
2. 對差分後的平穩序列使用 ARMA 預測
3. 透過累積變換回原尺度

---

## 模組函數速查

| 函數 | 說明 |
|------|------|
| `moving_average(x, window)` | 簡單滑動平均 |
| `autocovariance(x, lag)` | 樣本自協方差 |
| `acf(x, max_lag)` | 自身相關函數 |
| `partial_acf(x, max_lag)` | 偏自身相關函數（簡化版）|

---

## 參考文獻

1. Box, G. E. P., Jenkins, G. M., & Reinsel, G. C. (2015). *Time Series Analysis: Forecasting and Control*. Wiley.
2. Brockwell, P. J., & Davis, R. A. (2016). *Introduction to Time Series and Forecasting*. Springer.
3. Hamilton, J. D. (1994). *Time Series Analysis*. Princeton University Press.