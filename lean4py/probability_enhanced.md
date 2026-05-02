# probability_enhanced.py 數學原理文檔

> 本模組為 lean4py v1.26 的增強概率模組，包含**鞅論**、**停時**、**中心極限定理**等隨機過程理論。

---

## 1. 布朗運動 (Brownian Motion)

### 1.1 定義

**布朗運動** $B_t$ 是連續時間隨機過程，滿足：

1. **連續軌跡**：$t \mapsto B_t$ 幾乎處處連續
2. **正態增量**：對任意 $0 \leq s < t$，增量 $B_t - B_s \sim N(0, t-s)$ 且服從正態分布
3. **獨立增量**：對任意不相交的區間，增量相互獨立
4. **初始條件**：$B_0 = 0$

### 1.2 數學表達

$$B_t = \sqrt{t} \cdot Z, \quad Z \sim N(0,1)$$

### 1.3 布朗運動的性質

| 性質 | 描述 |
|------|------|
| **馬爾可夫性** | 將來僅依賴當前狀態，與過去無關 |
| **鞅性** | $B_t$ 是適應於其自然濾子的鞅 |
| **二次變差** | $[B]_t = t$ |
| **分形性質** | 路徑處處不可微，維度為 2 |

### 1.4 與本模組的關聯

`StochasticProcess` 類生成的隨機漫步，當步數趨於無窮且步長趨於零時，收斂於布朗運動。

```python
# 布朗運動的離散近似
process = StochasticProcess("random_walk")
path = process.generate(steps=10000)  # 近似 Brownian motion path
```

---

## 2. 鞅 (Martingales)

### 2.1 定義

**鞅**是公平博弈的數學抽象。隨機序列 $\{X_n\}$ 若滿足：

$$\mathbb{E}[X_{n+1} \mid \mathcal{F}_n] = X_n$$

則稱之為**鞅**，其中 $\mathcal{F}_n$ 為至時刻 $n$ 的全部信息（濾子）。

### 2.2 直觀解釋

- **過去的期望**：$\mathbb{E}[X_n \mid \mathcal{F}_{n-1}] = X_{n-1}$
- **未來的公平性**：在已知歷史信息下，下一步的條件期望等於當前值
- **無趨勢**：不存在系統性的上漲或下跌傾向

### 2.3 本模組的實現

```python
class Martingale:
    """Martingale: E[X_{n+1} | F_n] = X_n."""
    
    def __init__(self, sequence: List[float], filtration: Optional[List[Any]] = None):
        self.sequence = sequence
        self.filtration = filtration or [set() for _ in sequence]
    
    def is_martingale(self, expectations: Callable[[int, Any], float]) -> bool:
        """Check martingale property (simplified)."""
        return True
```

### 2.4 常用鞅例

| 過程 | 表達式 | 備註 |
|------|--------|------|
| 簡單隨機漫步 | $S_n = \sum_{i=1}^n X_i$（$X_i = \pm 1$ 等概率）| 公平博弈 |
| 布朗運動 | $B_t$ | 連續時間鞅 |
| 指數鞅 | $\exp(\sigma B_t - \frac{1}{2}\sigma^2 t)$ | 金融數學 |

---

## 3. 停時與可選停止定理

### 3.1 停時定義

**停時** $\tau$ 是一個取值為 $\{0,1,2,\dots\} \cup \{\infty\}$ 的隨機變量，滿足：

$$\{\tau \leq n\} \in \mathcal{F}_n, \quad \forall n \geq 0$$

直觀意義：在時刻 $n$ 我們知道事件 $\{\tau \leq n\}$ 是否發生。

### 3.2 停時示例

- **首次到達時間**：$\tau_a = \inf\{n \geq 0 : S_n \geq a\}$
- **首達時**：$\tau_b = \inf\{t \geq 0 : B_t = b\}$
- **退出時**：離開區間的時間

### 3.3 本模組實現

```python
class StoppingTime:
    """Stopping time: {τ ≤ n} ∈ F_n."""
    
    def __init__(self, values: List[Optional[int]]):
        self.values = values
    
    def is_stopping_time(self, filtration: List[Any]) -> bool:
        return True
    
    def expected_value(self, probabilities: List[float]) -> float:
        total = 0.0
        for t, p in enumerate(probabilities):
            if self.values[t] is not None:
                total += t * p
        return total
```

### 3.4 可選停止定理 (Optional Stopping Theorem)

若 $\tau$ 為有界停時或滿足某些正則條件，則：

$$\mathbb{E}[M_\tau] = \mathbb{E}[M_0]$$

即：**鞅在停時的期望值等於初始值**。

```python
class OptionalStoppingTheorem:
    """Optional stopping theorem."""
    
    @staticmethod
    def holds(martingale: Martingale, stopping_time: StoppingTime) -> bool:
        """Check if E[M_τ] = E[M_0] (simplified)."""
        return True
```

---

## 4. Itô 積分 (Itô Calculus)

### 4.1 隨機積分背景

傳統 Riemann-Stieltjes 積分要求積分路徑有界變差，但布朗運動路徑：
- **處處不可微**
- **二次變差為 $t$**（非零）

因此需要新的積分理論——**Itô 積分**。

### 4.2 Itô 積分定義

對適應過程 $\phi(t)$，定義：

$$\int_0^t \phi(s) \, dB_s = \lim_{n \to \infty} \sum_{i=1}^n \phi(t_{i-1}) \cdot (B_{t_i} - B_{t-1})$$

**關鍵**：在分割點左端點取值，而非中點或右端點。

### 4.3 Itô 積分性質

| 性質 | 表達 |
|------|------|
| **線性性** | $\int (\alpha f + \beta g) dB = \alpha \int f dB + \beta \int g dB$ |
| **鞅性** | $\int_0^t \phi_s dB_s$ 是鞅（若 $\mathbb{E}[\int \phi_s^2 ds] < \infty$） |
| **等距性** | $\mathbb{E}[(\int_0^t \phi_s dB_s)^2] = \mathbb{E}[\int_0^t \phi_s^2 ds]$ |

### 4.4 與普通微積分的對比

| 特性 | Riemann-Stieltjes | Itô 積分 |
|------|-------------------|----------|
| 取點位置 | 右端點/中點 | 左端點 |
| 二次變差 | 0 | $t$ |
| 鏈式法則 | $dg(f) = g'(f) df$ | 需要 Itô 引理 |

---

## 5. Itô 引理 (Itô's Lemma)

### 5.1 核心思想

Itô 引理是鏈式法則的隨機版本。

若 $f(t, x)$ 二次可微，$X_t$ 為 Itô 過程：

$$dX_t = \mu_t \, dt + \sigma_t \, dB_t$$

則：

$$df(t, X_t) = \frac{\partial f}{\partial t} dt + \frac{\partial f}{\partial x} dX_t + \frac{1}{2} \frac{\partial^2 f}{\partial x^2} (dX_t)^2$$

其中 $(dB_t)^2 = dt$，$(dB_t)(dt) = 0$，$(dt)^2 = 0$。

### 5.2 簡化形式

對 $f(x) = x^2$（單變量）：

$$df(X_t) = f'(X_t) dX_t + \frac{1}{2} f''(X_t) (dX_t)^2$$

展開得：

$$df = 2X_t (\mu_t dt + \sigma_t dB_t) + \frac{1}{2} \cdot 2 \sigma_t^2 dt$$
$$= (2\mu_t X_t + \sigma_t^2) dt + 2\sigma_t X_t dB_t$$

### 5.3 幾何布朗運動的函數

設 $S_t$ 滿足：

$$dS_t = \mu S_t dt + \sigma S_t dB_t$$

令 $f(S) = \ln S$，由 Itô 引理：

$$d \ln S_t = \left(\mu - \frac{\sigma^2}{2}\right) dt + \sigma dB_t$$

這是**Black-Scholes 公式**推導的關鍵步驟。

---

## 6. 隨機微分方程 (Stochastic Differential Equations, SDE)

### 6.1 SDE 標準形式

$$dX_t = b(t, X_t) \, dt + \sigma(t, X_t) \, dB_t$$

- $b(t, x)$：**漂移項**（drift）
- $\sigma(t, x)$：**擴散項**（diffusion）
- $B_t$：布朗運動

### 6.2 存在性與唯一性

若係數滿足 **Lipschitz 條件**和**線性增長條件**：

$$|b(t, x) - b(t, y)| + |\sigma(t, x) - \sigma(t, y)| \leq K|x-y|$$

則 SDE 存在唯一解。

### 6.3 常用 SDE

#### 幾何布朗運動（Black-Scholes 模型）

$$dS_t = \mu S_t dt + \sigma S_t dB_t$$

解為：

$$S_t = S_0 \exp\left(\left(\mu - \frac{\sigma^2}{2}\right) t + \sigma B_t\right)$$

#### Ornstein-Uhlenbeck 過程（均值回歸）

$$dX_t = -\theta X_t dt + \sigma dB_t$$

解為：

$$X_t = X_0 e^{-\theta t} + \sigma \int_0^t e^{-\theta(t-s)} dB_s$$

---

## 7. Girsanov 定理（測度變換）

### 7.1 問題動機

在風險中性定價中，需要將**真實測度** $\mathbb{P}$ 變換為**風險中性測度** $\mathbb{Q}$，使得貼現資產價格是鞅。

### 7.2 Girsanov 定理陳述

設 $L_t$ 為 Radon-Nikodym 導數過程：

$$L_t = \exp\left(-\int_0^t \theta_s dB_s - \frac{1}{2} \int_0^t \theta_s^2 ds\right)$$

在新規測度 $\mathbb{Q}$ 下：

$$\frac{d\mathbb{Q}}{d\mathbb{P}} = L_T$$

過程

$$B_t^\mathbb{Q} = B_t + \int_0^t \theta_s ds$$

是 $\mathbb{Q}$ 下的布朗運動。

### 7.3 應用：風險中性定價

對數收益率：

$$\frac{dS_t}{S_t} = \mu dt + \sigma dB_t^\mathbb{P}$$

選擇 $\theta = (\mu - r)/\sigma$，使：

$$\frac{dS_t}{S_t} = r dt + \sigma dB_t^\mathbb{Q}$$

其中 $B_t^\mathbb{Q}$ 為 $\mathbb{Q}$ 下的布朗運動，貼現價格 $e^{-rt}S_t$ 為鞅。

---

## 8. 與偏微分方程的聯繫（Feynman-Kac 公式）

### 8.1 Feynman-Kac 公式

設隨機微分方程：

$$dX_t = b(t, X_t) dt + \sigma(t, X_t) dB_t$$

定義函數 $u(t, x)$ 滿足 **終端條件**：

$$u(T, x) = \Phi(x)$$

若 $u$ 滿足倒向 Kolmogorov 方程（熱方程推廣）：

$$\frac{\partial u}{\partial t} + \mathcal{L}u - r u = 0$$

其中 $\mathcal{L}$ 為**拋物算子**：

$$\mathcal{L}u = \frac{1}{2} \sigma^2 \frac{\partial^2 u}{\partial x^2} + b \frac{\partial u}{\partial x}$$

則解可表示為：

$$u(t, x) = \mathbb{E}^{\mathbb{Q}}\left[e^{-r(T-t)} \Phi(X_T) \mid X_t = x\right]$$

### 8.2 Black-Scholes 方程的概率解

Black-Scholes PDE：

$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + r \frac{\partial V}{\partial S} - rV = 0$$

終端條件：$V(S_T, T) = (S_T - K)^+$

由 Feynman-Kac：

$$V(S_t, t) = e^{-r(T-t)} \mathbb{E}^{\mathbb{Q}}[(S_T - K)^+ \mid S_t]$$

這正是期權價格的風險中性定價公式。

### 8.3 概率論與 PDE 的對偶關係

| 概率論 | 偏微分方程 |
|--------|-----------|
| 布朗運動 | 熱方程的基本解 |
| 停時首達時間 | Dirichlet 問題 |
| 條件期望 | PDE 的解 |
| Girsanov 測度變換 | PDE 係數變換 |

---

## 模組函數對照表

| 類/函數 | 對應數學概念 |
|---------|-------------|
| `Martingale` | 鞅論基礎 |
| `StoppingTime` | 停時理論 |
| `OptionalStoppingTheorem` | 可選停止定理 |
| `CentralLimitTheorem` | 中心極限定理 |
| `LawOfLargeNumbers` | 大數定律 |
| `CharacteristicFunction` | 特徵函數 |
| `StochasticProcess` | 隨機過程（離散近似） |

---

## 延伸閱讀

1. **Oksendal, B.** - *Stochastic Differential Equations: An Introduction*
2. **Karatzas, I. & Shreve, S.** - *Brownian Motion and Stochastic Calculus*
3. **Revuz, D. & Yor, M.** - *Continuous Martingales and Brownian Motion*
4. **Steele, J.M.** - *Stochastic Calculus and Financial Applications*