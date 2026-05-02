# 譜序列（Spectral Sequence）

## 1. 概述

譜序列是一种强大的代数拓扑工具，用于通过**逐次逼近**（successive approximation）来计算同调群。其核心思想是将一个复杂的代数对象分解为一系列越来越简单的层次，每个层次都提供关于最终目标的更多信息。

谱序列在同调代数、代数拓扑学中具有广泛应用，是计算高维同调群的标准工具。

## 2. 基本結構

### 2.1 E² 頁面（Second Page）

谱序列从一个 **E² 頁面**开始，这是一个双次数（bidegree）的对象：

```
E²_{p,q}
```

其中：
- `p`：filtration 指标（表示在某个滤子中的位置）
- `q`：内部次数（internal degree）

在齐性上同调/同调代数中，E²_{p,q} 通常解释为某个 Selker 理论的一部分。

### 2.2 微分（ Differentials）

谱序列在每一页 `E_r` 上定义了一个**微分**：

```
d_r : E_r^{p,q} → E_r^{p+r, q-r+1}
```

其中 `r ≥ 2`，且满足 ** Leibniz 规则**：

```
d_r(xy) = d_r(x)y + (-1)^{|x|} x d_r(y)
```

微分的次数由 `(r, -r+1)` 给出。

### 2.3 頁面的演化

给定第 `r` 页和微分 `d_r`，第 `r+1` 页定义为：

```
E_{r+1}^{p,q} = ker(d_r : E_r^{p,q} → E_r^{p+r, q-r+1}) / im(d_r : E_r^{p-r, q+r-1} → E_r^{p,q})
```

直观上，这是将已经「收敛」的元素（核）除以已经「消失」的元素（像）。

## 3. 收斂（Convergence）

谱序列的**收斂性**是其最关键的理论性质之一。

### 3.1 基本收斂

我们说谱序列 **收斂**到目标对象 `H_*`，记作：

```
E²_{p,q} ⇒ H_{p+q}
```

这意味着存在一个**降滤链**（descending filtration）：

```
... ⊂ F_{p-1}H_n ⊂ F_p H_n ⊂ F_{p+1} H_n ⊂ ...
```

使得：

```
E²_{p,q} ≅ H(F_p H_{p+q} / F_{p-1} H_{p+q})
```

即 E² 页面同构于与该滤子相关的**相关分级（associated graded）**对象。

### 3.2 E∞ 頁面

当所有微分都稳定化（即后续页面的微分都为零）时，得到 **E∞ 页面**：

```
E_{r+1} = E_r  当且仅当 d_r = 0
```

E∞ 页面直接给出了目标对象的滤过同调：

```
E∞_{p,q} ≅ F_p H_{p+q} / F_{p-1} H_{p+q}
```

### 3.3 收斂標準

一个谱序列在以下情况下**收斂**：

1. **有限性条件**：每个次数 `n` 的同调群只有有限多个非零的 E² 项
2. **有界性条件**：存在一个函数 `f(q)` 使得当 `p < f(q)` 或 `p > g(q)` 时，E²_{p,q} = 0
3. **离开每个次数的项有限**：对于固定的 total degree `n = p + q`，只有有限多个非零项

## 4. 濾過複形（Filtered Complex）

### 4.1 濾過複形的定義

一个**濾過複形** `(C_*, F)` 由以下组成：

- 一个链复形 `C_* = {... → C_n → C_{n-1} → ...}`
- 一个降滤子 `F`，满足 `F^p C_* ⊂ F^{p+1} C_*`
- 微分保持滤子：`d(F^p C_n) ⊂ F^p C_{n-1}`

### 4.2 濾過複形的譜序列

从滤过复形可以构造一个谱序列，其 **E² 页面**为：

```
E²_{p,q} = H_{p+q}(F^p C_* / F^{p+1} C_*)
```

即第 `(p,q)` 项是相应滤过层的同调群。

这个谱序列**收斂**到 `H_*(C_*)`。

### 4.3 边界條件

如果滤过是**有界的**（即存在 `a, b` 使得 `F^a = 0` 且 `F^b = C_*`），则谱序列一定收斂。

## 5. 正合偶（Exact Couples）

### 5.1 定義

一个 **正合偶** `(E, A, d, i, j, k)` 由两个对象 `E` 和 `A` 及其间的映射组成：

```
d : E → E
i : A → A
j : A → E
k : E → A
```

满足以下正合序列：

```
A --j--> E --d--> E --k--> A --i--> A
```

### 5.2 正合偶與譜序列

从任何一个正合偶都可以**生成**一个谱序列：

1. 设 `E_1 = E`
2. 定义 `d_1 = d`
3. 计算 `A_2 = im(j)`
4. 定义 `E_2 = ker(d) / im(d)`
5. 递归重复，得到完整的谱序列

### 5.3 派生正合偶

从正合偶可以**派生**出新的正合偶：

- `i' = i|_A`
- `j' : A → im(i)`
- `k' : im(i) → A`

派生正合偶产生的谱序列与原偶相同，但可能更易计算。

## 6. Leray-Serre 譜序列（Leray-Serre Spectral Sequence）

### 6.1 纖維化

给定纤维化（fibration）：

```
F → E → B
```

其中 `F` 是纤维，`E` 是全空间，`B` 是基空间。

假设 `B` 是路径连通的，且所有空间都是良好行为（如 CW 复形）。

### 6.2 Serre 譜序列

Serre 谱序列的 **E² 页面**为：

```
E²_{p,q} = H_p(B; H_q(F))
```

即以纤维同调群为系数的基空间同调。

该谱序列**收斂**到整体同调：

```
E²_{p,q} ⇒ H_{p+q}(E)
```

### 6.2 邊界映射

谱序列的边界映射 `d_r` 对应于：
- 将纤维同调连接到基空间拓扑的攜貝（transgression）
- 描述了纤维与基空间之间的相互作用

### 6.4 低次数項的應用

从 E² 页面可以读出：

- `E²_{0,0} = Z` → `H_0(E) = Z`
- `E²_{p,0} = H_p(B)` → 给出整体同调的基空间部分
- `E²_{0,q} = H_q(F)` → 给出整体同调的纤维部分

## 7. Atiyah-Hirzebruch 譜序列（Atiyah-Hirzebruch Spectral Sequence）

### 7.1 定義

Atiyah-Hirzebruch 谱序列是 **广义上同调理论** 的谱序列：

```
E²_{p,q} = H_p(X; Ω^q) ⇒ E^{p+q}(X)
```

其中 `E^*` 是任意广义上同调理论（如 K 理论、复超几何上同调等）。

### 7.2 特性

1. **依赖于上同调理论**：不同的广义上同调理论给出不同的谱序列
2. **收敛性**：当 `E^*` 满足一定条件时，谱序列收敛
3. **过滤结构**：给出 `E^n(X)` 的一个滤过，其相关分级由普通上同调决定

### 7.3 K理論實例

对于 K 理论，有：

```
E²_{p,q} = H_p(X; Z) 当 q 为偶数
E²_{p,q} = 0 当 q 为奇数
```

这允许从普通上同调计算 K 群。

## 8. Adams 譜序列（Adams Spectral Sequence）

### 8.1 穩定同倫群

Adams 谱序列用于计算**稳定同伦群**：

```
π^s_*(S^0) = 稳定球面同伦群
```

这是代数拓扑中最基本也最困难的问题之一。

### 8.2 E² 頁面

Adams 谱序列的 **E² 页面**为：

```
E²_{s,t} = Ext^{s,t}_{A_*}(H_*(S^0), Z/2)
```

其中：
- `A_*` 是 **Steenrod 代数**（模 2 的 Steenrod 代数的对偶）
- `Ext` 是在 **comodule** 范畴中计算
- `s`： filtration 次数
- `t`： total degree

### 8.3 收斂

Adams 谱序列在一定条件下**收斂**到稳定同伦群：

```
E²_{s,t} ⇒ π_{t-s}^s(S^0)
```

### 8.4 計算流程

Adams 谱序列的计算通常遵循：

1. 确定 Steenrod 代数的结构
2. 计算 Ext 群（E² 页面）
3. 确定所有微分 `d_r`
4. 识别永久上同调
5. 得到稳定同伦群的估计

## 9. 收斂標準總結

### 9.1 強收斂

谱序列**強收斂**到 `H_*` 如果：

1. 对于每个 `(p,q)`，存在 `r(p,q)` 使得对于所有 `r ≥ r(p,q)`，有 `E_r^{p,q} = E_{∞}^{p,q}`
2. `E∞` 页面的相关分级同构于 `H_*`

### 9.2 有界譜序列

如果谱序列满足**有界性条件**（即每个 total degree 只有有限多个非零项），则必定收斂。

### 9.3 牛頓多邊形

在 Adams 谱序列等具体例子中，收斂性可通过 **牛頓多邊形** 可视化。

### 9.4 有限性與收斂

- **有限性假设**（如 CW 复形的有限性）通常保证收斂
- 无限复杂的对象可能导致谱序列不收斂或需要额外假设

## 10. 模塊 API 說明

### 10.1 SpectralSequence 類

```python
class SpectralSequence(Generic[T]):
    def __init__(self, E2_page=None):
        """初始化谱序列，指定 E² 页面"""

    def compute_differentials(self, page):
        """計算第 page 頁的微分 d_r"""

    def extend_page(self, page_num):
        """從第 page_num 頁計算第 page_num+1 頁"""

    def has_stabilized(self, page_num):
        """檢查是否在第 page_num 頁穩定化"""

    def limit_term(self):
        """計算極限項 E∞"""

    def total_degree(self, p, q):
        """計算總次數 n = p + q"""
```

### 10.2 專門譜序列

| 類 | 用途 |
|---|------|
| `AdamsSpectralSequence` | Adams 谱序列，計算穩定同倫群 |
| `SerreSpectralSequence` | Serre 谱序列，用於纖維化 |
| `CohomologySpectralSequence` | 上同調譜序列 |
| `HomologySpectralSequence` | 同調譜序列 |

### 10.3 輔助類

| 類 | 用途 |
|---|------|
| `ExactCouple` | 正合偶，用於生成譜序列 |
| `FilteredComplex` | 濾過複形，構造譜序列 |
| `Hypercohomology` | 超上同調 |

## 11. 數學背景

### 11.1 歷史

谱序列的概念由 Jean Leray（1946）在研究纤维化时引入。后来 Norman Steenrod、Serge Lang、Jean-Pierre Serre 等人进一步发展。

### 11.2 與其他理論的關係

- **同調代數**：谱序列是計算 Ext 和 Tor 群的核心工具
- **代數拓撲**：Serre 谱序列、Kunneth 公式的证明
- **代數幾何**：層的導出范帱中的譜序列

### 11.3 計算示例

谱序列的最简单应用是**有界复形的同调计算**：

给定一个滤过复形，可以逐次近似计算其同调：
- E² 页面给出第一近似
- 微分修正这些近似
- 重复直到稳定

## 12. 參考文獻

- Hatcher, A. *Algebraic Topology* - 谱序列的入门介绍
- McCleary, J. *A User's Guide to Spectral Sequences* - 详细参考书
- Weibel, C. *An Introduction to Homological Algebra* - 同调代数中的谱序列
- Adams, J.F. *Stable Homotopy and Generalised Homology* - Adams 谱序列

---

*本文档对应 lean4py 版本 1.34.0*