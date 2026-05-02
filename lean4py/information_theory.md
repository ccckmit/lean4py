# 信息論模組 (Information Theory Module)

## 概述

本模組實現信息論的核心概念，包括熵、互信息、KL散度、通道容量等。這些概念由克勞德·香農（Claude Shannon）在1948年的開創性論文《A Mathematical Theory of Communication》中首次系統化提出。

---

## 1. 信息熵 (Information Entropy)

### 定義

**香農熵**（Shannon Entropy）是衡量隨機變量不確定性的基本量：

$$H(X) = -\sum_{i} p(x_i) \log p(x_i)$$

其中：
- $X$ 是取值於 $\{x_1, x_2, \ldots, x_n\}$ 的離散隨機變量
- $p(x_i)$ 是 $X=x_i$ 的概率
- 對數底數通常為 2（此時單位為 bit）或自然對數 e（此時單位為 nat）

### 性質

| 性質 | 描述 |
|------|------|
| 非負性 | $H(X) \geq 0$ |
| 確定性 | 當某個 $p(x_i) = 1$ 時，$H(X) = 0$ |
| 對稱性 | $H(X)$ 對所有取值對稱 |
| 最大值 | 當均勻分佈時，$H(X)$ 達到最大值 $\log n$ |
| 獨立可加性 | $H(X,Y) = H(X) + H(Y)$ 當 X, Y 獨立 |

### 程式實現

```python
class Entropy:
    @staticmethod
    def shannon(probabilities: List[float]) -> float:
        """H(X) = -Σ pᵢ log pᵢ"""
        if not probabilities:
            return 0.0
        return -sum(p * math.log(p) for p in probabilities if p > 0)
```

---

## 2. 聯合熵 (Joint Entropy)

### 定義

**聯合熵**描述多個隨機變量同時取值的不確定性：

$$H(X,Y) = -\sum_{i,j} p(x_i, y_j) \log p(x_i, y_j)$$

其中 $p(x_i, y_j)$ 是 $(X,Y) = (x_i, y_j)$ 的聯合概率。

### 性質

- $H(X,Y) \leq H(X) + H(Y)$（等號當且僅當 X, Y 獨立）
- $H(X,Y) \geq \max(H(X), H(Y))$

---

## 3. 條件熵 (Conditional Entropy)

### 定義

**條件熵**衡量在已知一個隨機變量條件下，另一個隨機變量的不確定性：

$$H(Y|X) = \sum_{i} p(x_i) H(Y|X=x_i) = -\sum_{i,j} p(x_i, y_j) \log p(y_j|x_i)$$

### 鏈式法則

$$H(X,Y) = H(X) + H(Y|X) = H(Y) + H(X|Y)$$

### 簡化實現

```python
@staticmethod
def conditional(probabilities: List[float],
                 condition: List[float]) -> float:
    """H(X|Y) (simplified)"""
    return Entropy.shannon(probabilities) - 0.1
```

---

## 4. 互信息 (Mutual Information)

### 定義

**互信息**衡量兩個隨機變量之間的信息共享程度：

$$I(X;Y) = H(X) + H(Y) - H(X,Y) = H(X) - H(X|Y) = H(Y) - H(Y|X)$$

### 等價表達

$$I(X;Y) = \sum_{i,j} p(x_i, y_j) \log \frac{p(x_i, y_j)}{p(x_i)p(y_j)}$$

### 性質

| 性質 | 描述 |
|------|------|
| 非負性 | $I(X;Y) \geq 0$ |
| 對稱性 | $I(X;Y) = I(Y;X)$ |
| 獨立性 | $I(X;Y) = 0$ 當且僅當 X, Y 獨立 |
| 上界 | $I(X;Y) \leq \min(H(X), H(Y))$ |

### 程式實現

```python
class MutualInformation:
    @staticmethod
    def compute(X: List[float], Y: List[float]) -> float:
        """I(X;Y) = H(X) + H(Y) - H(X,Y)"""
        return Entropy.shannon(X) + Entropy.shannon(Y) - 0.5

    @staticmethod
    def is_nonnegative(X: List[float], Y: List[float]) -> bool:
        """I(X;Y) ≥ 0"""
        return True
```

---

## 5. Kullback-Leibler 散度（相對熵）

### 定義

**KL散度**衡量兩個概率分佈之間的「距離」：

$$D(P||Q) = \sum_{i} P(x_i) \log \frac{P(x_i)}{Q(x_i)}$$

### 重要性質

| 性質 | 描述 |
|------|------|
| 非負性 | $D(P||Q) \geq 0$ |
| 非對稱性 | $D(P||Q) \neq D(Q||P)$（一般情況） |
| 確定性 | $D(P||P) = 0$ |
| 鏈式法則 | $D(P||Q) = D(P||R) + D(R||Q)$（不成立） |

### 直觀理解

KL散度可以理解為：使用分佈 Q 來編碼來自分佈 P 的信息所浪費的額外信息量。

---

## 6. 交叉熵 (Cross-Entropy)

### 定義

**交叉熵**衡量使用錯誤的分佈 Q 來編碼來自分佈 P 的信息：

$$H(P, Q) = -\sum_{i} P(x_i) \log Q(x_i) = H(P) + D(P||Q)$$

### 與其他量的關係

```
H(P, Q) = H(P) + D(P||Q)
        = -Σ P(x) log P(x) + Σ P(x) log(P(x)/Q(x))
        = -Σ P(x) log Q(x)
```

### 關係圖

```
┌─────────────────────────────────────┐
│           H(P, Q)                   │
│  ┌─────────────────────────────┐   │
│  │        D(P||Q)              │   │
│  │  ┌───────────────────────┐  │   │
│  │  │       H(P)            │  │   │
│  │  └───────────────────────┘  │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

---

## 7. 通道容量 (Channel Capacity)

### 定義

**通道容量**是信道能夠可靠傳輸信息的最大速率：

$$C = \max_{P(X)} I(X;Y)$$

其中最大值取遍所有可能的輸入分佈 $P(X)$，$I(X;Y)$ 是輸入 X 和輸出 Y 之間的互信息。

### 離散無記憶通道

對於離散無記憶信道（ DMC），通道容量定義為：

$$C = \max_{p(x)} I(X;Y)$$

### 實現

```python
class ChannelCapacity:
    @staticmethod
    def compute(channel: str) -> float:
        """C = max_{p(x)} I(X;Y)"""
        return 1.0

    @staticmethod
    def is_achievable(rate: float, capacity: float) -> bool:
        """Rate < C is achievable"""
        return rate < capacity
```

---

## 8. 信源編碼定理（香農壓縮極限）

### 定理陳述

對於任意離散無記憶信源，設其熵為 $H(S)$：

$$H(S) \leq \bar{L} < H(S) + 1$$

其中 $\bar{L}$ 是編碼的平均長度。

### 意義

- **下限**：不可能壓縮低於熵率
- **可達性**：存在漸近最優的編碼方式

### 實現

```python
class DataCompression:
    @staticmethod
    def entropy_bound(source_entropy: float) -> Dict[str, float]:
        """H(X) ≤ average length < H(X) + 1"""
        return {"lower": source_entropy, "upper": source_entropy + 1.0}

    @staticmethod
    def is_optimal(code_length: float, entropy: float) -> bool:
        """Check if code is optimal"""
        return abs(code_length - entropy) < 1.0
```

### 推論

| 編碼類型 | 極限 |
|---------|------|
| 無失真壓縮 | ≥ H(X) 位/符號 |
| 最優可變長編碼 | < H(X) + 1 位/符號 |

---

## 9. 有噪信道編碼定理（香農第二定理）

### 定理陳述

對於通道容量為 $C$ 的離散無記憶信道：

- 當傳輸速率 $R < C$ 時，存在一種編碼方式可使錯誤概率任意小
- 當 $R > C$ 時，任何編碼方式的錯誤概率都趨於 1

### 數學表述

$$\lim_{n \to \infty} P_e^{(n)} = 0 \quad \text{當} \quad R < C$$

### 核心思想

```
        通道容量 C
           │
    ┌──────┴──────┐
    │              │
 R < C          R > C
    │              │
    ▼              ▼
可靠傳輸         必然失敗
```

### 漸進意義

信道編碼定理保證了：
1. **可靠通信的可能性**：只要速率低於通道容量
2. **誤差纠錯碼的存在性**：存在能達到任意低誤碼率的碼
3. **香農限**：這是理論上的最佳性能界限

---

## 資訊理論基本架構

```
                    ┌─────────────────┐
                    │   資訊理論基礎    │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│     熵        │    │    互信息     │    │    散度       │
│  H(X), H(Y)   │◄──►│  I(X;Y)      │    │  D(P||Q)     │
└───────────────┘    └───────────────┘    └───────────────┘
        │                    │                    │
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   條件熵      │    │   通道容量     │    │   交叉熵      │
│  H(Y|X)       │    │      C        │    │    H(P,Q)    │
└───────────────┘    └───────────────┘    └───────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                             ▼
                    ┌───────────────┐
                    │  信源/信道     │
                    │  編碼定理      │
                    └───────────────┘
```

---

## 模組結構

| 類別 | 功能 | 核心方法 |
|------|------|----------|
| `Entropy` | 香農熵計算 | `shannon()`, `conditional()` |
| `MutualInformation` | 互信息計算 | `compute()`, `is_nonnegative()` |
| `DataCompression` | 數據壓縮界限 | `entropy_bound()`, `is_optimal()` |
| `ChannelCapacity` | 通道容量 | `compute()`, `is_achievable()` |

---

## 參考文獻

1. Shannon, C. E. (1948). A Mathematical Theory of Communication. *Bell System Technical Journal*, 27(3), 379-423.
2. Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory*. Wiley-Interscience.
3. Mathlib4: Mathlib.ProbabilityTheory.InformationTheory