# 遍歷理論測試文檔 (test_ergodic_theory.py)

本文檔說明 `test_ergodic_theory.py` 中測試用例所驗證的數學原理。

---

## 1. 測試概覽

測試文件位於 `/Users/Shared/ccc/project/lean4py/tests/test_ergodic_theory.py`，包含 9 個測試類，共 30 個測試方法。測試對象涵蓋：

- `ErgodicTransformation` (遍歷變換)
- `MeasurePreservingMap` (保測度映射)
- `ErgodicTheorem` (遍歷定理)
- `MixingTransformation` (混合變換)
- `KolmogorovSinaiEntropy` (Kolmogorov-Sinai 熵)
- `BernoulliShift` (伯努利移位)
- `PoincareRecurrence` (龐加萊回歸)
- `InvariantMeasure` (不變測度)
- `ErgodicDecomposition` (遍歷分解)

---

## 2. 遍歷理論基礎

遍歷理論是動力系統和測度論的分支，研究在長時間下系統的平均行為。

### 核心概念

- **動力系統**：定義為 $(X, \mathcal{B}, \mu, T)$，其中 $T: X \to X$ 為變換
- **測度空間**：$(X, \mathcal{B}, \mu)$ 為概率空間
- **不變測度**：若 $\mu(T^{-1}(A)) = \mu(A)$ 對所有可測集 $A$ 成立，則 $\mu$ 為 $T$ 不變測度

---

## 3. 保測度變換測試 (TestErgodicTransformation)

### 3.1 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 遍歷變換對象的正確創建 |
| `test_is_measure_preserving` | 變換是否保持測度 |
| `test_is_ergodic` | 系統是否遍歷 |
| `test_iterate` | 迭代運算 $T^n(x)$ |
| `test_time_average` | 時間平均 $\frac{1}{n}\sum_{i=0}^{n-1} f(T^i(x))$ |
| `test_space_average` | 空間平均 $\int f \, d\mu$ |
| `test_Birkhoff_ergodic_theorem` | Birkhoff 遍歷定理 |

### 3.2 數學原理

**保測度變換**：變換 $T: X \to X$ 若滿足 $\mu(T^{-1}(A)) = \mu(A)$ 對所有可測集 $A$ 成立，則稱 $T$ 為保測度變換。

**遍歷性**：若不變測度 $\mu$ 下，僅有 $\varnothing$ 和 $X$ 本身是 $T$ 不變集，則稱 $T$ 是遍歷的。數學表達為：若 $T^{-1}(A) = A$，則 $\mu(A) = 0$ 或 $\mu(A) = 1$。

**Birkhoff 遍歷定理**：設 $T$ 為保測度變換，$f \in L^1(X, \mu)$，則
$$\lim_{n \to \infty} \frac{1}{n} \sum_{i=0}^{n-1} f(T^i(x)) = \frac{1}{\mu(X)} \int_X f \, d\mu$$
幾乎處處收斂，且時間平均等於空間平均。

---

## 4. 保測度映射測試 (TestMeasurePreservingMap)

### 4.1 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 保測度映射對象的創建 |
| `test_push_forward` | 前推測度 $\mu \circ T^{-1}$ |
| `test_is_measure_preserving` | 映射是否保測度 |

### 4.2 數學原理

**保測度映射**：映射 $T: X \to Y$ 若滿足 $\mu(T^{-1}(B)) = \nu(B)$ 對所有可測集 $B \subseteq Y$ 成立，則 $T$ 將測度空間 $(X, \mu)$ 映射到 $(Y, \nu)$，且是保測度的。

**前推測度**：若 $T: X \to Y$ 為可測映射，則前推測度定義為 $(T_* \mu)(B) = \mu(T^{-1}(B))$。

---

## 5. 遍歷定理測試 (TestErgodicTheorem)

### 5.1 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_Birkhoff` | Birkhoff 遍歷定理 |
| `test_Kingman_subadditive` | Kingman 子加性遍歷定理 |
| `test_maximal_inequality` | 極大不等式 |

### 5.2 數學原理

**Birkhoff 遍歷定理**：見 3.2 節。

**Kingman 子加性遍歷定理**：若 $\{a_{m+n}\} \leq a_m + a_n$（子加性），則
$$\lim_{n \to \infty} \frac{a_n}{n} = \inf_n \frac{a_n}{n}$$
此定理應用於非負次可加序列，收斂到其下確界。

**極大不等式**：定義 $f^* = \sup_{n \geq 0} \frac{1}{n} \sum_{i=0}^{n-1} f(T^i(x))$，則
$$\mu(f^* > \alpha) \leq \frac{1}{\alpha} \int f^+ \, d\mu$$

---

## 6. 混合變換測試 (TestMixingTransformation)

### 6.1 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 混合變換對象創建 |
| `test_is_weakly_mixing` | 弱混合性 |
| `test_is_strongly_mixing` | 強混合性 |
| `test_is_bernoulli` | Bernoulli 性 |
| `test_correlation_function` | 相關函數 |
| `test_spectral_radius` | 譜半徑 |

### 6.2 數學原理

**弱混合**：變換 $T$ 若滿足
$$\lim_{n \to \infty} \frac{1}{n} \sum_{k=0}^{n-1} |\mu(T^{-k}(A) \cap B) - \mu(A)\mu(B)| = 0$$
對所有可測集 $A, B$ 成立，則 $T$ 是弱混合的。

**強混合**：若
$$\lim_{n \to \infty} \mu(T^{-n}(A) \cap B) = \mu(A)\mu(B)$$
則 $T$ 是強混合的。

**相關函數**：定義為
$$C_{f,g}(n) = \int f \cdot g \circ T^n \, d\mu - \int f \, d\mu \int g \, d\mu$$

**譜半徑**：變換的譜半徑為 1（對於概率空間上的保測度變換）。

**Bernoulli 性**：為最強的混合性質，表示系統可以分解為獨立的隨機試驗。

---

## 7. 熵測試 (TestKolmogorovSinaiEntropy)

### 7.1 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | KS 熵對象創建 |
| `test_partition_entropy` | 分割熵 $H(\mathcal{P})$ |
| `test_conditional_entropy` | 條件熵 $H(\mathcal{P} \mid \mathcal{Q})$ |
| `test_compute_ks_entropy` | Kolmogorov-Sinai 熵 |
| `test_Pesin_entropy_formula` | Pesin 熵公式 |
| `test_isomorphism_invariant` | 同構不變性 |

### 7.2 數學原理

**分割熵**：對於有限分割 $\mathcal{P} = \{A_1, \ldots, A_k\}$，熵定義為
$$H(\mathcal{P}) = -\sum_{i=1}^k \mu(A_i) \log \mu(A_i)$$

**條件熵**：
$$H(\mathcal{P} \mid \mathcal{Q}) = -\sum_{j=1}^m \mu(B_j) \sum_{i=1}^k \mu(A_i \mid B_j) \log \mu(A_i \mid B_j)$$

**Kolmogorov-Sinai 熵**：定義為
$$h_{KS}(T) = \sup_{\mathcal{P}} \lim_{n \to \infty} \frac{1}{n} H\left(\bigvee_{i=0}^{n-1} T^{-i}\mathcal{P}\right)$$
其中 $\bigvee$ 表示分割的細分。

**Pesin 熵公式**：對於光滑動力系統，有
$$h_{KS}(T) = \sum_{i: \lambda_i > 0} \lambda_i$$
其中 $\lambda_i$ 為 Lyapounov 指數。

**同構不變性**：KS 熵是動力系統的同構不變量，意味著同構的系統具有相同的 KS 熵。

---

## 8. Bernoulli 移位測試 (TestBernoulliShift)

### 8.1 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | Bernoulli 移位創建 |
| `test_shift_map` | 移位映射 |
| `test_is_bernoulli` | Bernoulli 性 |
| `test_kolmogorov_entropy` | Kolmogorov 熵（公平硬幣） |
| `test_kolmogorov_entropy_unfair` | Kolmogorov 熵（不公平硬幣） |

### 8.2 數學原理

**Bernoulli 移位**：定義於 $\{0, 1, \ldots, b-1\}^{\mathbb{Z}}$ 上，移位映射為
$$(\ldots, x_{-1}, x_0, x_1, \ldots) \mapsto (\ldots, x_0, x_1, x_2, \ldots)$$

**移位映射**：對於序列 $x = (x_0, x_1, x_2, \ldots)$，移位後為 $(x_1, x_2, x_3, \ldots)$。

**Bernoulli 移位的 KS 熵**：對於底數為 $b$、概率分佈為 $\{p_0, p_1, \ldots, p_{b-1}\}$ 的 Bernoulli 移位，
$$h = -\sum_{i=0}^{b-1} p_i \log p_i$$
即為分割的熵。

---

## 9. 龐加萊回歸測試 (TestPoincareRecurrence)

### 9.1 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 回歸對象創建 |
| `test_recurrence_time` | 回歸時間 |
| `test_almost_all_recurrent` | 幾乎所有點都回歸 |
| `test_recurrence_theorem` | 龐加萊回歸定理 |

### 9.2 數學原理

**龐加萊回歸定理**：設 $(X, \mathcal{B}, \mu, T)$ 為有限測度空間，$A \subseteq X$ 為可測集，則幾乎所有 $x \in A$ 都會無限次回歸到 $A$，即
$$\mu\left(\{x \in A : \exists n_k \to \infty, T^{n_k}(x) \in A\}\right) = \mu(A)$$

**回歸時間**：點 $x$ 回歸到集合 $A$ 的時間為
$$\tau_A(x) = \min\{n > 0 : T^n(x) \in A\}$$

---

## 10. 不變測度測試 (TestInvariantMeasure)

### 10.1 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 不變測度對象創建 |
| `test_apply_to_set` | 測度應用於集合 |
| `test_is_T_invariant` | $T$ 不變性 |
| `test_ergodic_decomposition` | 遍歷分解 |

### 10.2 數學原理

**$T$ 不變測度**：測度 $\mu$ 若滿足 $\mu(T^{-1}(A)) = \mu(A)$ 對所有可測集 $A$ 成立，則 $\mu$ 為 $T$ 不變測度。

**遍歷分解**：任何不變測度都可以分解為遍歷測度的凸組合：
$$\mu = \int \mu_x \, d\nu(x)$$
其中 $\mu_x$ 為遍歷測度，$\nu$ 為位於分解上的概率測度。

---

## 11. 遍歷分解測試 (TestErgodicDecomposition)

### 11.1 測試內容

| 測試方法 | 驗證內容 |
|---------|---------|
| `test_creation` | 遍歷分解對象創建 |
| `test_decomposition_exists` | 分解存在性 |
| `test_uniqueness` | 分解唯一性 |
| `test_support_of_component` | 分量的支撐集 |

### 11.2 數學原理

**遍歷分解定理**：每個不變測度都可以唯一地分解為遍歷測度的積分。具體地，對於不變測度 $\mu$，存在一個遍歷測度的 Borel 概率分佈 $\nu$ 使得
$$\mu = \int \mu_z \, d\nu(z)$$

**分量支撐集**：遍歷分解中每個分量 $\mu_x$ 的支撐集是 $T$ 不變的，且這些支撐集幾乎處處不相交。

---

## 12. 測試失敗診斷

### 12.1 常見問題

1. **時間平均不等於空間平均**：檢查變換是否真正遍歷
2. **KS 熵計算錯誤**：檢查分割是否正確，細分運算是否正確
3. **混合性質測試失敗**：檢查相關函數的收斂性條件
4. **回歸時間不正確**：檢查移位映射的定義是否正確

### 12.2 調試建議

- 使用 `pytest -v tests/test_ergodic_theory.py` 查看詳細輸出
- 檢查測度函數是否為概率測度（總測度為 1）
- 確認不變集的定義是否與變換一致

---

## 13. 數學術語對照表

| 英文術語 | 中文術語 |
|---------|---------|
| Ergodic Transformation | 遍歷變換 |
| Measure-Preserving | 保測度 |
| Birkhoff Ergodic Theorem | Birkhoff 遍歷定理 |
| Weakly Mixing | 弱混合 |
| Strongly Mixing | 強混合 |
| Kolmogorov-Sinai Entropy | Kolmogorov-Sinai 熵 |
| Bernoulli Shift | Bernoulli 移位 |
| Poincare Recurrence | 龐加萊回歸 |
| Invariant Measure | 不變測度 |
| Ergodic Decomposition | 遍歷分解 |
| Pesin Entropy Formula | Pesin 熵公式 |
| Lyapunov Exponent | Lyapounov 指數 |

---

*本文檔基於 lean4py v1.34.0 版本的 ergodic_theory 模組測試編寫。*