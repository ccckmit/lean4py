# 卡爾曼濾波器 (Kalman Filter)

## 概述

卡爾曼濾波器是一種用於**線性動態系統**的最優狀態估計器，適用於噪聲環境下的線性系統。它基於貝葉斯估計理論，通過預測-更新两步迭代的遞推方式，實現對系統狀態的最優估計。

卡爾曼濾波器的核心思想是：結合系統的先驗模型知識和實際觀測數據，最小化狀態估計的均方誤差。

---

## 數學模型

### 狀態轉移模型 (State Transition Model)

$$x_k = F \cdot x_{k-1} + w_{k-1}$$

其中：
- $x_k$：時刻 $k$ 的狀態向量
- $F$：狀態轉移矩陣 (State Transition Matrix)
- $w_{k-1} \sim \mathcal{N}(0, Q)$：過程噪聲，服從均值為0、協方差為 $Q$ 的高斯分佈

### 觀測模型 (Observation Model)

$$z_k = H \cdot x_k + v_k$$

其中：
- $z_k$：時刻 $k$ 的觀測向量
- $H$：觀測矩陣 (Observation Matrix)
- $v_k \sim \mathcal{N}(0, R)$：觀測噪聲，服從均值為0、協方差為 $R$ 的高斯分佈

---

## 預測步驟 (Prediction Step)

根據系統模型預先估計下一時刻的狀態：

### 先驗狀態估計

$$\hat{x}_{k|k-1} = F \cdot \hat{x}_{k-1|k-1}$$

### 先驗協方差估計

$$P_{k|k-1} = F \cdot P_{k-1|k-1} \cdot F^T + Q$$

其中：
- $P$：狀態估計的協方差矩陣
- $Q$：過程噪聲協方差矩陣

---

## 更新步驟 (Update Step)

當獲得新的觀測數據 $z_k$ 後，更新狀態估計：

### 創新量 (Innovation)

$$y_k = z_k - H \cdot \hat{x}_{k|k-1}$$

創新量是觀測值與預測觀測值之間的差異。

### 創新協方差 (Innovation Covariance)

$$S_k = H \cdot P_{k|k-1} \cdot H^T + R$$

### 卡爾曼增益 (Kalman Gain)

$$K_k = P_{k|k-1} \cdot H^T \cdot S_k^{-1}$$

卡爾曼增益決定了預測估計和觀測數據之間的權衡：
- 增益越大，越依賴觀測數據
- 增益越小，越依賴模型預測

### 後驗狀態估計

$$\hat{x}_{k|k} = \hat{x}_{k|k-1} + K_k \cdot y_k$$

### 後驗協方差估計

$$P_{k|k} = (I - K_k \cdot H) \cdot P_{k|k-1}$$

---

## 算法流程

```
初始化: x_0, P_0

for k = 1, 2, 3, ... do
    # 預測步驟
    x_pred = F * x_est
    P_pred = F * P_est * F^T + Q

    # 更新步驟
    y = z_k - H * x_pred                    # 創新量
    S = H * P_pred * H^T + R                 # 創新協方差
    K = P_pred * H^T * S^{-1}                # 卡爾曼增益
    x_est = x_pred + K * y                    # 後驗估計
    P_est = (I - K * H) * P_pred             # 後驗協方差
end for
```

---

## 擴展卡爾曼濾波器 (Extended Kalman Filter, EKF)

### 問題背景

現實世界中，許多系統是非線性的。標準卡爾曼濾波器僅適用於線性系統。

### 解決方案

EKF 通過**線性化**將非線性系統近似為線性系統：

$$x_k = f(x_{k-1}) + w_{k-1}$$
$$z_k = h(x_k) + v_k$$

其中 $f(\cdot)$ 和 $h(\cdot)$ 是非線性函數。

### 線性化方法

使用**雅可比矩陣**進行一階泰勒展開：

$$F_k = \frac{\partial f}{\partial x}\bigg|_{x_{k-1}}$$
$$H_k = \frac{\partial h}{\partial x}\bigg|_{x_{k|k-1}}$$

### EKF 流程

```
for k = 1, 2, 3, ... do
    # 預測步驟 (使用非線性模型)
    x_pred = f(x_est)
    P_pred = F_k * P_est * F_k^T + Q

    # 更新步驟 (使用線性化觀測矩陣)
    y = z_k - h(x_pred)
    S = H_k * P_pred * H_k^T + R
    K = P_pred * H_k^T * S^{-1}
    x_est = x_pred + K * y
    P_est = (I - K * H_k) * P_pred
end for
```

### 局限性

- 只適用于**弱非線性**系統
- 高階項被忽略，誤差不確定
- 可能導致濾波器發散

---

## 無跡卡爾曼濾波器 (Unscented Kalman Filter, UKF)

### 問題解決思路

為避免 EKF 線性化帶來的誤差，UKF 採用**無跡變換 (Unscented Transform)**：

- 選擇一組確定的採樣點（稱為 sigma 點）
- 這些採樣點完全捕捉輸入分佈的均值和協方差
- 通過非線性函數變換採樣點
- 由變換後的採樣點計算輸出分佈的均值和協方差

### Sigma 點選擇

對於 $n$ 維狀態，選擇 $2n+1$ 個 sigma 點：

$$\chi_0 = \hat{x}$$
$$\chi_i = \hat{x} + (\sqrt{(n+\lambda)P})_i, \quad i = 1, \ldots, n$$
$$\chi_{i+n} = \hat{x} - (\sqrt{(n+\lambda)P})_i, \quad i = 1, \ldots, n$$

其中 $\lambda = \alpha^2(n + \kappa) - n$ 是縮放參數。

### UKF 流程

```
# 初始化
chi = [x_est, x_est +/- sqrt((n+lambda)*P)]

for k = 1, 2, 3, ... do
    # 預測步驟
    for each sigma point chi_i do
        chi_pred_i = f(chi_i)               # 狀態傳播
    end for
    x_pred = sum(weights_i * chi_pred_i)
    P_pred = sum(weights_i * (chi_pred_i - x_pred)(chi_pred_i - x_pred)^T) + Q

    # 更新步驟
    for each sigma point chi_pred_i do
        zeta_pred_i = h(chi_pred_i)          # 觀測預測
    end for
    z_pred = sum(weights_i * zeta_pred_i)
    S = sum(weights_i * (zeta_pred_i - z_pred)(zeta_pred_i - z_pred)^T) + R
    cross_cov = sum(weights_i * (chi_pred_i - x_pred)(zeta_pred_i - z_pred)^T)

    K = cross_cov * S^{-1}
    x_est = x_pred + K * (z_k - z_pred)
    P_est = P_pred - K * S * K^T
end for
```

### UKF 的優勢

| 特性 | EKF | UKF |
|------|-----|-----|
| 線性化誤差 | 高階項被忽略 | 採樣點精確傳播 |
| 計算複雜度 | $O(n^2)$ | $O((2n+1)n^2)$ |
| 雅可比矩陣 | 需要計算 | 無需計算 |
| 非線性強度 | 僅適用于弱非線性 | 可處理強非線性 |

---

## Rauch-Tung-Striebel 平滑器

本模塊還提供了**RTS 平滑器**，用於**後向平滑**處理：

RTS 平滑器利用整個時間序列的觀測數據（包括未來數據），給出每個時刻的最優估計。

$$\hat{x}_{k|N} = \hat{x}_{k|k} + G_k \cdot (\hat{x}_{k+1|N} - \hat{x}_{k+1|k})$$
$$P_{k|N} = P_{k|k} + G_k \cdot (P_{k+1|N} - P_{k+1|k}) \cdot G_k^T$$

其中 $G_k$ 為平滑增益：

$$G_k = P_{k|k} \cdot F^T \cdot P_{k+1|k}^{-1}$$

---

## 使用範例

```python
from lean4py.kalman_filter import KalmanFilter

# 初始化卡爾曼濾波器
kf = KalmanFilter(
    state_dim=2,      # 狀態維度
    obs_dim=2,         # 觀測維度
    F=[[1, 1], [0, 1]],  # 狀態轉移矩陣
    H=[[1, 0], [0, 1]],  # 觀測矩陣
    Q=[[0.1, 0], [0, 0.1]],  # 過程噪聲協方差
    R=[[1, 0], [0, 1]]      # 觀測噪聲協方差
)

# 預測
kf.predict()

# 更新（使用觀測數據）
z = [1.0, 2.0]
kf.update(z)
```

---

## 總結

| 濾波器類型 | 適用系統 | 線性化方式 | 計算效率 |
|-----------|---------|-----------|---------|
| KF | 線性 | 無需線性化 | 高 |
| EKF | 弱非線性 | 一階泰勒展開 | 高 |
| UKF | 強非線性 | 無跡變換 | 中等 |