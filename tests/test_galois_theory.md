# Galois 理論測試文檔

本文檔說明 `test_galois_theory.py` 中測試用例的數學原理。

## 1. 測試驗證的內容

該測試套件驗證伽羅瓦理論（Galois Theory）的核心概念，這是法國數學家埃瓦里斯特·伽羅瓦（Évariste Galois）創立的抽象代數分支。測試涵蓋：

- 域擴張的基本性質
- 伽羅瓦群的計算
- 擴張的可分性與正規性
- 伽羅瓦擴張的判定
- 基本定理的中間域對應
- 根式可解性

---

## 2. 域擴張測試（FieldExtension）

### 數學原理

**定義**：設 $K$ 為一個域，$L$ 為包含 $K$ 的更大域，則稱 $L/K$ 為一個**域擴張**，記作 $L \supseteq K$。$K$ 稱為**基域**（base field），$L$ 稱為**擴張域**。

**擴張次數**：$[L:K]$ 表示擴張的次數，等於 $L$ 作為 $K$-向量空間的維數。對於 $L = K(\alpha)$ 這樣的單代數擴張，$[L:K]$ 等於最小多項式的次數。

### 測試用例

| 測試 | 驗證內容 |
|------|----------|
| `test_creation` | 確認 `FieldExtension` 對象正確存儲基域、擴張域和次數 |
| `test_is_algebraic` | 驗證擴張是代數的（即每個元素都滿足某個非零多項式方程） |
| `test_is_finite` | 驗證擴張是有限的（$[L:K] < \infty$） |

**測試示例**：
```python
ext = FieldExtension("Q", "Q(√2)", degree=2)
```

這表示有理數域 $\mathbb{Q}$ 的二次擴張 $\mathbb{Q}(\sqrt{2})$，其中 $\sqrt{2}$ 的最小多項式為 $x^2 - 2$，所以 $[L:K] = 2$。

---

## 3. 伽羅瓦群測試（GaloisGroup）

### 數學原理

**定義**：給定域擴張 $L/K$，$L$ 在 $K$ 上的**伽羅瓦群**定義為：
$$\text{Gal}(L/K) = \{\sigma: L \to L \mid \sigma \text{ 為域自同構，且 } \sigma|_K = \text{id}_K\}$$

**伽羅瓦群的性質**：
- $|\text{Gal}(L/K)| = [L:K]$（當擴張為伽羅瓦擴張時）
- 伽羅瓦群描述了擴張的對稱性

### 測試用例

| 測試 | 驗證內容 |
|------|----------|
| `test_compute` | 計算並返回伽羅瓦群的結構 |
| `test_is_abelian` | 判斷伽羅瓦群是否為阿貝爾群（交換群） |

**測試示例**：
```python
ext = FieldExtension("Q", "Q(√2)", degree=2)
result = GaloisGroup.compute(ext)
```

對於 $\mathbb{Q}(\sqrt{2})/\mathbb{Q}$，伽羅瓦群包含兩個自同構：
- 恆等映射：$\sigma_1(\sqrt{2}) = \sqrt{2}$
- 共軛映射：$\sigma_2(\sqrt{2}) = -\sqrt{2}$

但當前實現返回 `trivial` 群，這是簡化版本。

---

## 4. 可分性測試（SeparableExtension）

### 數學原理

**定義**：域擴張 $L/K$ 稱為**可分的**，若每個元素 $\alpha \in L$ 的最小多項式在分裂域中沒有重根。

**判別準則**：
- 特徵零域（如 $\mathbb{Q}$）上的擴張總是可分的
- 有限域上的擴張總是可分的
- $L/K$ 可分 $\Leftrightarrow$ $[\text{Sep}:K] = [L:K]$，其中 Sep 為 $K$ 在 $L$ 中的可分閉包

### 測試用例

| 測試 | 驗證內容 |
|------|----------|
| `test_is_separable` | 判斷擴張是否可分 |

**測試示例**：
```python
ext = FieldExtension("Q", "Q(√2)", degree=2)
SeparableExtension.is_separable(ext)  # 返回 True
```

$\mathbb{Q}(\sqrt{2})/\mathbb{Q}$ 是可分的，因為 $x^2 - 2$ 的導數為 $2x$，在 $\mathbb{Q}(\sqrt{2})$ 中有非零值。

---

## 5. 正规性测试（NormalExtension）

### 数学原理

**定义**：域扩张 $L/K$ 称为**正规的**，若 $L$ 是 $K$ 上某个多项式的分裂域。

**判别准则**：
- $L/K$ 正规 $\Leftrightarrow$ 对于每个不可约多项式 $f(x) \in K[x]$，若 $f$ 在 $L$ 中有一个根，则 $f$ 在 $L$ 中完全分裂

### 测试用例

| 测试 | 验证内容 |
|------|----------|
| `test_is_normal` | 判断扩张是否正规 |

**测试示例**：
```python
ext = FieldExtension("Q", "Q(√2)", degree=2)
NormalExtension.is_normal(ext)  # 返回 True
```

$\mathbb{Q}(\sqrt{2})/\mathbb{Q}$ 是正规的，因为 $x^2 - 2$ 在 $\mathbb{Q}(\sqrt{2})$ 中完全分裂：根为 $\pm\sqrt{2}$。

---

## 6. 伽罗瓦扩张测试（GaloisExtension）

### 数学原理

**定义**：域扩张 $L/K$ 称为**伽罗瓦扩张**，当且仅当它是：
1. **正规的**：$L$ 是某个多项式的分裂域
2. **可分的**：每个元素的最小多项式无重根

**重要性质**：
- $|\text{Gal}(L/K)| = [L:K]$
- 伽罗瓦扩张是双反射的：$L/K$ 为伽罗瓦 $\Leftrightarrow$ $K$ 是 $\text{Gal}(L/K)$ 的固定域

### 测试用例

| 测试 | 验证内容 |
|------|----------|
| `test_is_galois` | 综合判断扩张是否为伽罗瓦扩张 |

**测试示例**：
```python
ext = FieldExtension("Q", "Q(√2)", degree=2)
GaloisExtension.is_galois(ext)  # 返回 True (因为既正规又可分)
```

---

## 7. 基本定理测试（FundamentalTheorem）

### 数学原理

**伽罗瓦理论基本定理**：设 $L/K$ 为有限伽罗瓦扩张，$G = \text{Gal}(L/K)$。

则存在**伽罗瓦对应**（Galois correspondence）：
$$\{\text{中间域 } F \mid K \subseteq F \subseteq L\} \leftrightarrow \{\text{子群 } H \leq G\}$$

对应关系：
- $F \mapsto \text{Gal}(L/F)$（$F$ 的伽罗瓦群）
- $H \mapsto L^H$（$H$ 的固定域）

**对应性质**：
- $[L:F] = |H|$，$[F:K] = [G:H]$
- $F/K$ 正规 $\Leftrightarrow$ $\text{Gal}(L/F) \trianglelefteq G$

### 测试用例

| 测试 | 验证内容 |
|------|----------|
| `test_intermediate_fields` | 列出所有中间域 |
| `test_correspondence` | 返回伽罗瓦对应的完整映射 |

**测试示例**：
```python
ext = FieldExtension("Q", "Q(√2)", degree=2)
result = FundamentalTheorem.intermediate_fields(ext)
# 返回 [base, extension] = ["Q", "Q(√2)"]
```

---

## 8. 根式可解性测试（SolvabilityByRadicals）

### 数学原理

**定义**：多项式 $f(x)$ 称为**可根式求解**，若其根可以由系数经过有限次加、减、乘、除、开方运算得到。

**伽罗瓦的里程碑定理**：
$$f(x) \text{ 可根式求解} \Leftrightarrow \text{Gal}(f) \text{ 为可解群}$$

**可解群**：群 $G$ 称为可解的，若存在子群链：
$$1 = G_0 \trianglelefteq G_1 \trianglelefteq \cdots \trianglelefteq G_n = G$$
使得每个商群 $G_{i+1}/G_i$ 都是阿贝尔群。

**五次方程的不可解性**：
- $n \leq 4$ 的多项式总是可解的
- $S_5$（5次对称群）不是可解群
- 因此一般五次方程没有根式解

### 测试用例

| 测试 | 验证内容 |
|------|----------|
| `test_is_solvable` | 根据多项式次数判断是否可根式求解 |

**测试示例**：
```python
SolvabilityByRadicals.is_solvable(3)  # True (三次方程可解)
SolvabilityByRadicals.is_solvable(5)   # False (一般五次方程不可解)
```

当前实现使用简化逻辑：次数 $\leq 4$ 返回 `True`，否则返回 `False`。

---

## 9. constructibility_tests（作图问题）

虽然测试文件中未包含此项，但伽罗瓦理论在古希腊三大作图问题中有重要应用：

### 数学原理

**可作图条件**：点可用尺规作图 $\Leftrightarrow$ 其坐标在某个逐次平方根扩张中。

**三大作图问题**：
| 问题 | 不可作图证明 |
|------|-------------|
| 化圆为方 | $\pi$ 是超越数，不在任何平方根扩张中 |
| 倍立方 | $\sqrt[3]{2}$ 的次数为 3，不是 2 的幂 |
| 三等分角 | $\cos(20^\circ)$ 的最小多项式为 $4x^3 - 3x + 1/2$，次数为 3 |

---

## 10. 测试覆盖总结

| 类 | 测试数 | 核心验证 |
|----|--------|----------|
| `TestFieldExtension` | 3 | 域扩张的基本属性 |
| `TestGaloisGroup` | 2 | 伽罗瓦群的计算与性质 |
| `TestSeparableExtension` | 1 | 可分性判定 |
| `TestNormalExtension` | 1 | 正规性判定 |
| `TestGaloisExtension` | 1 | 伽罗瓦扩张综合判定 |
| `TestFundamentalTheorem` | 2 | 中间域与伽罗瓦对应 |
| `TestSolvabilityByRadicals` | 1 | 根式可解性 |

---

## 11. 与 mathlib4 的对齐

本模块模仿 `mathlib4.Mathlib.FieldTheory.Galois` 的设计：

| lean4py | mathlib4 |
|---------|----------|
| `FieldExtension` | `FieldExtension` |
| `GaloisGroup` | `GaloisGroup` |
| `SeparableExtension` | `SeparableExtension` |
| `NormalExtension` | `NormalExtension` |
| `GaloisExtension` | `IsGalois` |
| `FundamentalTheorem` | `FundamentalTheoremOfGaloisTheory` |
| `SolvabilityByRadicals` | `SolvableByRadicals` |

---

*文档版本：v1.27*