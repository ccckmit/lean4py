# 統計學模組 (statistics.py)

本模組提供描述統計、推論統計與迴歸分析的完整實現，涵蓋機率論基礎到假說檢定。

---

## 1. 描述性統計量

### 1.1 算術平均數 (Mean)

$$\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$$

平均數是数据中心趋势的度量，对所有数据点求和后除以数据个数。实现时需注意空数据返回 0.0，避免除以零错误。

### 1.2 中位數 (Median)

中位數是將數據排序後位於中間位置的值：
- 奇數個數據：中間那個值
- 偶數個數據：中間兩個值的平均

中位數比平均數更穩健，不受極端值影響。

### 1.3 眾數 (Mode)

眾數是出現次數最多的值。數據集可能有多個眾數（雙峰、多峰分佈），因此返回列表。空數據返回空列表。

### 1.4 變異數 (Variance)

$$\sigma^2 = \frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n}$$

**樣本變異數**（分母 n-1）使用貝塞爾校正，提供母體變異數的無偏估計。**母體變異數**（分母 n）適用於已知整個母體的情況。

---

## 2. 標準差 (Standard Deviation)

$$\sigma = \sqrt{\frac{\sum_{i=1}^{n}(x_i - \bar{x})^2}{n}}$$

標準差是變異數的平方根，與原始數據具有相同單位，更直觀理解數據離散程度。

---

## 3. quartiles 與 IQR

本模組雖未直接實現四分位數，但可通過以下方式計算：
- Q1 = 第 25 百分位數
- Q2 = 中位數
- Q3 = 第 75 百分位數

**四分位距 (IQR)**：
$$IQR = Q3 - Q1$$

IQR 用於異常值檢測：低於 Q1 - 1.5×IQR 或高於 Q3 + 1.5×IQR 的點為異常值。

---

## 4. 偏度與峰度

### 4.1 偏度 (Skewness)

$$g_1 = \frac{n}{(n-1)(n-2)}\sum_{i=1}^{n}\left(\frac{x_i - \bar{x}}{s}\right)^3$$

- g₁ > 0：右偏（正偏），分佈右側有長尾
- g₁ < 0：左偏（負偏），分佈左側有長尾
- g₁ ≈ 0：對稱分佈

### 4.2 峰度 (Kurtosis)

$$g_2 = \frac{n(n+1)}{(n-1)(n-2)(n-3)}\sum_{i=1}^{n}\left(\frac{x_i - \bar{x}}{s}\right)^4 - \frac{3(n-1)^2}{(n-2)(n-3)}$$

- g₂ > 0：尖峰分佈（leptokurtic），尾部更厚
- g₂ < 0：平坦分佈（platykurtic），尾部更薄
- g₂ ≈ 0：近似常態分佈（使用 excess kurtosis）

---

## 5. 共變異數與相關係數

### 5.1 共變異數 (Covariance)

$$cov(X,Y) = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})$$

共變異數衡量兩個變數的聯合變異程度。正值表示同向變動，負值表示反向變動。

### 5.2 皮爾森相關係數 (Pearson Correlation)

$$r = \frac{cov(X,Y)}{s_X \cdot s_Y}$$

或展開為：
$$r = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n}(x_i - \bar{x})^2 \cdot \sum_{i=1}^{n}(y_i - \bar{y})^2}}$$

- r = 1：完全正相關
- r = -1：完全負相關
- r = 0：無線性相關
- |r| < 0.3：弱相關
- 0.3 ≤ |r| < 0.7：中等相關
- |r| ≥ 0.7：強相關

---

## 6. 簡單線性迴歸

### 6.1 迴歸模型

$$y_i = \beta_0 + \beta_1 x_i + \varepsilon_i$$

其中：
- β₀：截距（intercept）
- β₁：斜率（slope）
- εᵢ：誤差項，服從 N(0, σ²)

### 6.2 最小平方法 (OLS)

目標：最小化殘差平方和

$$SS_{res} = \sum_{i=1}^{n}(y_i - \hat{y}_i)^2 = \sum_{i=1}^{n}(y_i - \beta_0 - \beta_1 x_i)^2$$

求偏導並設為零，得到正規方程組：

$$\beta_1 = \frac{n\sum x_i y_i - \sum x_i \sum y_i}{n\sum x_i^2 - (\sum x_i)^2} = \frac{S_{xy}}{S_{xx}}$$

$$\beta_0 = \bar{y} - \beta_1 \bar{x}$$

實現中注意分母可能為零的情況。

---

## 7. 決定係數 R²

$$R^2 = 1 - \frac{SS_{res}}{SS_{tot}} = 1 - \frac{\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}{\sum_{i=1}^{n}(y_i - \bar{y})^2}$$

- R² = 1：完美擬合
- R² = 0：模型無解釋力
- R² < 0：模型比簡單均值更差

Adjusted R² 考慮了自變數數量的懲罰：
$$R^2_{adj} = 1 - \frac{(1-R^2)(n-1)}{n-p-1}$$

其中 p 為自變數個數。

---

## 8. 常態分佈與 Z 分數

### 8.1 Z 分數 (標準化)

$$z = \frac{x - \mu}{\sigma}$$

Z 分數表示某數值距離平均數多少個標準差。用於標準化不同尺度的數據。

### 8.2 常態分佈

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$$

標準常態分佈 N(0,1) 的累計分佈函數：
$$\Phi(z) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{z} e^{-t^2/2} dt$$

本模組使用誤差函數 erf 計算：
$$p = 2\left(1 - \frac{1}{2}(1 + erf\left(\frac{z}{\sqrt{2}}\right))\right)$$

---

## 9. 中央極限定理 (CLT)

**定理**：從任意分佈的母體中抽取獨立同分佈樣本，當樣本數 n 足夠大時，樣本均值的抽樣分佈趨近於常態分佈 N(μ, σ²/n)。

$$\bar{X} \sim N\left(\mu, \frac{\sigma^2}{n}\right) \quad \text{當 } n \to \infty$$

實務上通常 n ≥ 30 時近似效果良好。

這個定理是推論統計的基石，使得小樣本情況下也能進行假說檢定。

---

## 10. 信賴區間 (Confidence Interval)

### 10.1 母體平均數的信賴區間

當母體標準差已知時：
$$\bar{x} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}$$

當母體標準差未知時（使用樣本標準差）：
$$\bar{x} \pm t_{\alpha/2, n-1} \cdot \frac{s}{\sqrt{n}}$$

本模組使用 Z 分數近似（當 n 足夠大時 t 分數趨近於 z 分數）：
```python
def confidence_interval_mean(data, confidence=0.95):
    z = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}[confidence]
    m = z * s / sqrt(n)
    return (x_bar - m, x_bar + m)
```

### 10.2 解釋

「95% 信賴區間」表示：如果重複抽樣 100 次，約 95 次的信賴區間會包含真實的母體參數。

---

## 11. 點估計與最大概似估計 (MLE)

### 11.1 點估計

點估計使用樣本統計量估計未知的母體參數。良好的估計量應具備：
- **不偏性**：E(θ̂) = θ
- **有效性**：Var(θ̂) 最小
- **一致性**：n → ∞ 時 θ̂ → θ
- **有效性**：漸進常態

### 11.2 最大概似估計 (MLE)

給定觀測數據 X，最大化似然函數 L(θ|X) 以獲得參數估計：

$$\hat{\theta}_{MLE} = \arg\max_\theta L(\theta | X) = \arg\max_\theta \prod_{i=1}^{n} f(x_i | \theta)$$

為方便計算，通常使用對數似然：
$$\ell(\theta) = \log L(\theta | X) = \sum_{i=1}^{n} \log f(x_i | \theta)$$

**範例**：常態分佈 N(μ, σ²) 的 MLE
- μ̂ = x̄（樣本均值）
- σ̂² = Σ(xi - x̄)²/n（並非不偏估計）

本模組中的 `linear_regression` 實現在誤差項服從常態分佈假設下，OLS 即為 MLE。

---

## 12. 假說檢定

### 12.1 單樣本 t 檢定

檢定 H₀: μ = μ₀

$$t = \frac{\bar{x} - \mu_0}{s / \sqrt{n}}$$

自由度 df = n - 1。p 值由 t 分佈計算。

### 12.2 變異數分析 (ANOVA)

檢定多組均值是否相等。

$$F = \frac{MS_{between}}{MS_{within}}$$

其中：
- MS_between = SS_between / (k-1)
- MS_within = SS_within / (N-k)

### 12.3 卡方檢定 (Chi-Square Test)

$$χ^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i}$$

自由度 df = k - 1（擬合優度檢定）。

### 12.4 無母數檢定

本模組提供多種無母數檢定：

**Mann-Whitney U 檢定**：比較兩組位置
- 結合兩樣本並賦予等級
- 計算 U 統計量
- 使用常態近似計算 p 值

**Kruskal-Wallis H 檢定**：ANOVA 的無母數版本
- 對所有觀測值排序並賦予等級
- 計算各組等級和

**Wilcoxon 符號等級檢定**：單樣本或配對樣本
- 計算與中位數的差值
- 對絕對差值排序

**Mann-Kendall 趨勢檢定**：時間序列趨勢
- 計算 concordant 和 discordant 配對數
- S 統計量標準化後檢定趨勢顯著性

---

## 13. 迴歸診斷

`linear_regression_diagnostics` 函數提供：

```python
{
    'slope': β₁,
    'intercept': β₀,
    'r_squared': R²,
    'residuals': [e₁, e₂, ..., eₙ],
    'fitted_values': [ŷ₁, ŷ₂, ..., ŷₙ]
}
```

殘差分析用於診斷：
- **常態性**：殘差應接近常態分佈
- **同方差性**：殘差變異數應恆定
- **獨立性**：殘差間應無自相關

---

## 數學符號對照表

| 符號 | 意義 |
|------|------|
| x̄ | 樣本均值 |
| s² | 樣本變異數 |
| s | 樣本標準差 |
| σ² | 母體變異數 |
| σ | 母體標準差 |
| n | 樣本大小 |
| N | 母體大小 |
| r | 皮爾森相關係數 |
| R² | 決定係數 |
| β₀ | 迴歸截距 |
| β₁ | 迴歸斜率 |
| ε | 誤差項 |
| ŷ | 預測值 |
| IQR | 四分位距 |

---

*本文件基於 lean4py v1.34.0 統計模組編寫*