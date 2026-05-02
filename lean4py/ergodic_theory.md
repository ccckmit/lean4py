# 遍歷理論 (Ergodic Theory) 模塊文檔

## 概述

遍歷理論是動力系統與測度論的交叉學科，研究在保測度變換下空間的漸近行為。本模塊實現了遍歷理論的核心概念，包括遍歷變換、混合性、熵、以及相關定理。

---

## 1. 保測度變換 (Measure-Preserving Transformations)

### 數學定義

設 $(X, \mathcal{B}, \mu)$ 為測度空間，變換 $T: X \to X$ 稱為**保測度變換**，若對所有可測集合 $A \in \mathcal{B}$：

$$\mu(T^{-1}(A)) = \mu(A)$$

### 類層次

```
MeasurePreservingMap          # 通用保測度映射
    └── ErgodicTransformation  # 遍歷變換（保測度 + 遍歷性）
```

### 核心方法

| 方法 | 說明 |
|------|------|
| `is_measure_preserving()` | 檢驗 $\mu(T^{-1}(A)) = \mu(A)$ |
| `push_forward()` | 前推測度 $\mu_*(A) = \mu(T^{-1}(A))$ |

---

## 2. 遍歷定理 (Ergodic Theorem)

### Birkhoff 遍歷定理

**定理（Birkhoff, 1931）**：設 $T: X \to X$ 為保測度變換，$f \in L^1(X, \mu)$，則：

$$\lim_{n \to \infty} \frac{1}{n} \sum_{i=0}^{n-1} f(T^i(x)) = \bar{f}(x) \quad \text{幾乎處處成立}$$

其中 $\bar{f}$ 為不變函數，且若 $T$ 為遍歷的，則 $\bar{f}$ 為常數。

**核心含義**：時間平均 = 空間平均

$$\frac{1}{n} \sum_{i=0}^{n-1} f(T^i(x)) \xrightarrow{n \to \infty} \int_X f \, d\mu$$

### 實現說明

```python
Birkhoff_ergodic_theorem(f, x, n) -> Tuple[float, float]
```

- `time_average`: 時間平均 $\frac{1}{n} \sum_{i=0}^{n-1} f(T^i(x))$
- `space_average`: 空間平均（Monte Carlo 積分估計）

### Kingman 次加法遍歷定理

對於非負次加法序列 $\{a_n\}$：

$$\frac{a_n}{n} \to \inf_{k \geq 1} \frac{a_k}{k}$$

---

## 3. 遍歷性 (Ergodicity)

### 數學定義

保測度變換 $T: X \to X$ 稱為**遍歷的**，若任意不變集合都是平凡的：

$$T^{-1}(A) = A \implies \mu(A) \in \{0, 1\}$$

或等價地：

$$\mu(A \Delta T^{-1}(A)) = 0 \implies \mu(A) \in \{0, 1\}$$

### 不變測度

測度 $\mu$ 稱為 **$T$-不變測度**，若：

$$\mu(T^{-1}(A)) = \mu(A) \quad \forall A \in \mathcal{B}$$

### 類：`InvariantMeasure`

```python
InvariantMeasure(space, measure_func)
    ├── apply_to_set()        # 計算 μ(A)
    ├── is_T_invariant()      # 檢驗不變性
    └── ergodic_decomposition() # 分解為遍歷分量
```

---

## 4. 混合性 (Mixing)

### 強混合 (Strong Mixing)

$T$ 稱為**強混合**，若對所有可測集合 $A, B$：

$$\lim_{n \to \infty} \mu(T^{-n}(A) \cap B) = \mu(A) \cdot \mu(B)$$

物理意義：過去狀態與未來狀態漸進獨立。

### 弱混合 (Weak Mixing)

$T$ 稱為**弱混合**，若在 $L^2$ 中不存在非平凡特徵函數：

$$f \circ T = e^{i\theta} f \implies f = \text{常數}$$

或等價於：

$$\frac{1}{n} \sum_{k=0}^{n-1} |\mu(T^{-k}(A) \cap B) - \mu(A)\mu(B)| \to 0$$

### 層次關係

```
遍歷 (Ergodic)
    └── 弱混合 (Weakly Mixing)
            └── 強混合 (Strongly Mixing)
                    └── Bernoulli 變換
```

### 類：`MixingTransformation`

| 方法 | 說明 |
|------|------|
| `is_weakly_mixing()` | 弱混合檢驗 |
| `is_strongly_mixing()` | 強混合檢驗 |
| `is_bernoulli()` | Bernoulli 變換檢驗 |
| `correlation_function()` | 相關函數 $\langle f, g \circ T^n \rangle$ |

---

## 5. 熵 (Entropy)

### 拓撲熵 vs 測度熵

**拓撲熵**：考慮軌道的複雜度，與覆蓋相關。

**Kolmogorov-Sinai 測度熵**：基於分割的信息量。

### Kolmogorov-Sinai 熵

設 $T$ 為保測度變換，$\mathcal{P} = \{P_1, \ldots, P_k\}$ 為分割，則：

$$h(T, \mathcal{P}) = \lim_{n \to \infty} \frac{1}{n} H(\mathcal{P} \vee T^{-1}\mathcal{P} \vee \cdots \vee T^{-(n-1)}\mathcal{P})$$

其中 $H$ 為分割熵：

$$H(\mathcal{P}) = -\sum_{i=1}^k p_i \log_2 p_i, \quad p_i = \mu(P_i)$$

**KS 熵**定義為：

$$h_{KS}(T) = \sup_{\mathcal{P}} h(T, \mathcal{P})$$

### 實現

```python
KolmogorovSinaiEntropy(transformation, partition)
    ├── partition_entropy()      # H(P) = -Σ p_i log p_i
    ├── conditional_entropy()    # H(P|Q)
    ├── compute_ks_entropy()     # h(T)
    └── Pesin_entropy_formula()  # h(T) = Σ max(0, λ_i)
```

### Pesin 熵公式

對於光滑動力系統，正 Lyapunov 指數之和等於 KS 熵：

$$h_{KS}(T) = \sum_{\lambda_i > 0} \lambda_i$$

---

## 6. Shannon-McMillan-Breiman 定理

### 定理陳述

設 $T$ 為遍歷保測度變換，$\mathcal{P}$ 為有限分割，則：

$$-\frac{1}{n} \log_2 \mu(P_n(x)) \to h(T, \mathcal{P}) \quad \text{幾乎處處及 L^1}$$

其中 $P_n(x)$ 為包含 $x$ 的 $n$-階柱集。

### 物理意義

- 軌道的「典型」分割大小呈指數衰減
- 衰減率由 KS 熵決定

### 與 KS 熵的關係

SMB 定理提供了一種**遍歷**意義下計算條件熵的方式：

$$h(T, \mathcal{P}) = \lim_{n \to \infty} \frac{1}{n} H(\mathcal{P} | T^{-1}\mathcal{P} \vee \cdots \vee T^{-n}\mathcal{P})$$

---

## 7. 同構變換 (Isomorphic Transformations)

### 定義

兩個保測度變換 $T: (X, \mu) \to (X, \mu)$ 和 $S: (Y, \nu) \to (Y, \nu)$ 稱為**同構**，若存在雙射 $\phi: X \to Y$（測度幾乎處處雙射）使得：

$$S \circ \phi = \phi \circ T$$

### 同構不變量

| 不變量 | 說明 |
|--------|------|
| KS 熵 $h_{KS}(T)$ | 同構不變量 |
| Lyapunov 指數譜 | 同構不變量（Oseledets 定理）|
| 混合性 | 同構不變量 |
| Bernoulli 性 | 同構不變量 |

### Bernoulli 分割

**Bermoulli 變換**是完全混沌的動力系統，其 KS 熵最大：

$$h(B_p) = -\sum_{i=1}^k p_i \log_2 p_i$$

其中 $B_p$ 為概率向量 $p = (p_1, \ldots, p_k)$ 的 Bernoulli 移位。

---

## 8. Koopman 算子 (Koopman Operator)

### 定義

對於保測度變換 $T: X \to X$，**Koopman 算子** $U_T: L^2(X, \mu) \to L^2(X, \mu)$ 定義為：

$$(U_T f)(x) = f(T^{-1}(x)) = f \circ T^{-1}$$

### 基本性質

1. **等距性**：$U_T$ 為線性等距算子
   $$\|U_T f\|_2 = \|f\|_2$$

2. **伴隨算子**：$U_T^* = U_{T^{-1}}$

3. **譜半徑**：$\rho(U_T) = 1$

### 與遍歷性的關係

- $T$ 遍歷 $\iff$ $U_T$ 無非平凡不變函數
- $U_T$ 的譜幫助分析 $T$ 的混合性質

### 類：`MixingTransformation` 中的實現

```python
spectral_radius()  # Koopman 算子在 L^2 中的譜半徑
```

---

## 9. Poincaré 返回定理

### 定理

設 $T: X \to X$ 為保測度變換，$A \subseteq X$ 為可測集合，則幾乎所有 $x \in A$ 都會無限次返回到 $A$：

$$|\{n \geq 1 : T^n(x) \in A\}| = \infty \quad \text{幾乎處處}$$

### 實現

```python
PoincareRecurrence(space, transformation)
    ├── recurrence_time()       # 首次返回時間
    ├── almost_all_recurrent()  # 幾乎所有點返回
    └── recurrence_theorem()    # 返回定理
```

---

## 10. 遍歷分解 (Ergodic Decomposition)

### Krylov-Bogoliubov 定理

設 $X$ 為緊緻度量空間，$T: X \to X$ 連續，則存在 $T$-不變概率測度。

### 遍歷分解定理

每個不變概率測度可以唯一分解為遍歷測度的凸組合：

$$\mu = \int_{M_{\text{erg}}(T)} \nu \, d\lambda(\nu)$$

其中 $M_{\text{erg}}(T)$ 為遍歷測度的集合。

### 實現

```python
ErgodicDecomposition(measure)
    ├── decomposition_exists()  # Krylov-Bogoliubov
    ├── uniqueness()            # 唯一遍歷性
    └── support_of_component()  # 分量的支撐集
```

---

## 類層次總結

```
ergodic_theory.py
├── ErgodicTransformation          # 遍歷變換類
│   ├── iterate()                  # T^n(x)
│   ├── time_average()             # 時間平均
│   ├── space_average()            # 空間平均
│   └── Birkhoff_ergodic_theorem() # Birkhoff 定理
├── MeasurePreservingMap            # 保測度映射
│   ├── push_forward()             # 前推測度
│   └── is_measure_preserving()    # 保測度檢驗
├── ErgodicTheorem                 # 遍歷定理集合
│   ├── Birkhoff()                 # Birkhoff 定理
│   ├── Kingman_subadditive()      # Kingman 定理
│   └── maximal_inequality()       # 極大不等式
├── MixingTransformation            # 混合變換
│   ├── is_weakly_mixing()         # 弱混合
│   ├── is_strongly_mixing()       # 強混合
│   ├── is_bernoulli()             # Bernoulli
│   └── correlation_function()     # 相關函數
├── KolmogorovSinaiEntropy         # KS 熵
│   ├── partition_entropy()        # 分割熵
│   ├── conditional_entropy()      # 條件熵
│   ├── compute_ks_entropy()       # KS 熵
│   └── Pesin_entropy_formula()    # Pesin 公式
├── BernoulliShift                 # Bernoulli 移位
│   ├── shift_map()                # 移位映射
│   └── kolmogorov_entropy()       # Bernoulli 熵
├── PoincareRecurrence             # Poincaré 返回
│   ├── recurrence_time()          # 返回時間
│   └── almost_all_recurrent()     # 幾乎處處返回
├── InvariantMeasure               # 不變測度
│   ├── apply_to_set()             # 測度計算
│   ├── is_T_invariant()           # T-不變性
│   └── ergodic_decomposition()     # 遍歷分解
└── ErgodicDecomposition           # 遍歷分解類
    ├── decomposition_exists()     # 存在性
    ├── uniqueness()               # 唯一性
    └── support_of_component()     # 支撐集
```

---

## 數學背景

### 與 mathlib4 的對齊

本模塊實現了遍歷理論的核心概念，對應於 Lean 4 mathlib 中的：
- `MeasureTheory.Measure.MeasureSpaceDef`
- `Dynamics.Ergodic.MeasurePreserving`
- `Entropy.KolmogorovSinai`

### 應用領域

- 統計力學微正則系綜
- 信息論與壓縮算法
- 動力系統混沌理論
- 數論中的遍歷理論方法