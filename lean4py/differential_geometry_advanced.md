# 微分几何进阶 / Advanced Differential Geometry

## 概述

本模块实现了一系列高级微分几何概念，对应 mathlib4 中的 `Mathlib.Geometry.Differential` 模块。主要包括**联络**、**曲率**、**holonomy**（和乐群）以及**示性类**等核心概念。这些工具是现代几何与拓扑研究的基石，在理论物理中也具有重要应用。

---

## 1. 主 G-丛 (Principal G-Bundles)

### 1.1 定义

设 $G$ 为一个李群，$P \to M$ 是一个光滑流形间的光纤丛。若 $G$ 在 $P$ 上自由且恰当可迁地作用（右手作用），则称 $P$ 为**主 $G$-丛**，记作 $P(M, G)$。

- **底空间** $M$：光滑流形
- **结构群** $G$：李群
- **光纤** 同构于 $G$（作为齐性空间 $G/G = \{e\}$）

### 1.2 转移函数

对于局部平凡化 $\{(U_i, \varphi_i)\}$，转移函数为：

$$g_{ij}: U_i \cap U_j \to G, \quad p \mapsto g_{ij}(p)$$

满足上链条件：

$$g_{ij} \cdot g_{jk} = g_{ik} \quad \text{on } U_i \cap U_j \cap U_k$$

### 1.3 例子

| 丛 | 结构群 | 描述 |
|----|--------|------|
| $O(n)$-丛 | $O(n)$ | 正交标架丛 |
| $U(n)$-丛 | $U(n)$ | 酉标架丛 |
| $G$-主丛 | 一般李群 $G$ | 规范理论中的纤维丛 |

---

## 2. 联络与平行移动 (Connections on Principal Bundles)

### 2.1 Ehresmann 联络

设 $\pi: P \to M$ 为主 $G$-丛。在 $P$ 的每点 $p$ 处，**水平子空间** $H_p P \subset T_p P$ 满足：

$$T_p P = H_p P \oplus V_p P$$

其中 $V_p P = \ker(d\pi_p)$ 为**竖直子空间**（与纤维相切）。

### 2.2 协变导数

对于截面 $s: M \to P$ 和向量场 $X \in \mathfrak{X}(M)$，联络的协变导数定义为：

$$\nabla_X s := (ds)_p(X) - \tilde{X}_p$$

其中 $\tilde{X}$ 是 $X$ 的**水平提升**。

### 2.3 规范势 (Connection 1-form)

光滑 $ \mathfrak{g}$-值 1-形式 $\omega \in \Omega^1(P, \mathfrak{g})$ 称为**规范势**或**联络形式**，满足：

1. **$G$-等变性**：$r_g^* \omega = \mathrm{Ad}(g^{-1}) \circ \omega$
2. **竖直限制**：对基本向量场 $A^\#$，有 $\omega(A^\#) = A$

其中 $A \in \mathfrak{g}$，$A^\#$ 是对应的**基本向量场**。

### 2.4 Levi-Civita 联络

在黎曼流形 $(M, g)$ 上，存在唯一的无挠率且 $g$-兼容的联络——**Levi-Civita 联络** $\nabla$：

$$T(X, Y) = \nabla_X Y - \nabla_Y X - [X, Y] = 0$$

$$\nabla g = 0$$

克里斯托费尔符号：

$$\Gamma^k_{ij} = \frac{1}{2} g^{kl}(\partial_i g_{jl} + \partial_j g_{il} - \partial_l g_{ij})$$

---

## 3. 曲率与示性形式 (Curvature and Characteristic Forms)

### 3.1 曲率张量

**黎曼曲率张量**定义为：

$$R(X, Y)Z = \nabla_X \nabla_Y Z - \nabla_Y \nabla_X Z - \nabla_{[X,Y]} Z$$

在局部坐标系中：

$$R^k_{ijl} = \partial_i \Gamma^k_{jl} - \partial_j \Gamma^k_{il} + \Gamma^k_{im} \Gamma^m_{jl} - \Gamma^k_{jm} \Gamma^m_{il}$$

### 3.2 曲率的代数性质

| 性质 | 表达式 |
|------|--------|
| **对称性** | $R(X,Y)Z = -R(Y,X)Z$ |
| **比安基恒等式** | $R(X,Y)Z + R(Y,Z)X + R(Z,X)Y = 0$ |
| **里奇对称** | $\mathrm{Ric}(X,Y) = \mathrm{tr}(Z \mapsto R(X,Z)Y)$ |

### 3.3 里奇曲率与数量曲率

- **里奇曲率**：$\mathrm{Ric}(X,Y) = g^{ij} R(e_i, X, Y, e_j)$
- **数量曲率**（标量曲率）：$R = g^{ij} \mathrm{Ric}(e_i, e_j) = g^{ik} g^{jl} R_{ijkl}$

### 3.4 曲率形式

对于主 $G$-丛上的联络，其**曲率形式** $\Omega \in \Omega^2(P, \mathfrak{g})$ 定义为：

$$\Omega(X, Y) = d\omega(X_h, Y_h)$$

或更著名的是**结构方程**（Cartan 结构方程）：

$$\Omega = d\omega + \frac{1}{2}[\omega, \omega]$$

在局部平凡化下：$\Omega = g^{-1} dg + g^{-1} \omega g$（取决于规范）

---

## 4. 陈省身-韦尔理论 (Chern-Weil Theory)

### 4.1 背景

给定主 $G$-丛 $P \to M$ 及其联络，**Chern-Weil 理论**通过曲率形式构造**示性类**——流形的整体拓扑不变量。

### 4.2 不变多项式

设 $\mathfrak{g}$ 为李群 $G$ 的李代数，$P: \mathfrak{g} \times \cdots \times \mathfrak{g} \to \mathbb{R}$ 为**$G$-不变对称多重线性泛函**。

例如对于 $U(n)$（$\mathfrak{u}(n)$ 为反-Hermitian 矩阵）：

$$P(A_1, \ldots, A_k) = \frac{1}{k!}\sum_{\sigma \in S_k} \mathrm{tr}(A_{\sigma(1)} \cdots A_{\sigma(k)})$$

### 4.3 示性形式

给定不变多项式 $P$，定义**示性形式**：

$$\alpha_P = P(\Omega, \ldots, \Omega) \in \Omega^{2k}(M)$$

由于比安基恒等式，$\alpha_P$ 是**闭形式**。

### 4.4 示性类

**闭形式在 de Rham 上同调中的类**即为示性类，与丛的拓扑相关。

---

## 5. 陈类、庞特里亚金类与欧拉类 (Chern, Pontryagin, Euler Classes)

### 5.1 陈类 (Chern Classes)

对于复向量丛 $E \to M$（结构群 $U(n)$），陈类 $c_k(E) \in H^{2k}(M; \mathbb{Z})$ 递归定义为：

$$\det(I + \frac{t\Omega}{2\pi i}) = \sum_{k=0}^n c_k(E) t^k$$

**性质**：

- $c_0(E) = 1$
- $c_k(E)$ 仅依赖于 $E$ 的陈示性式
- $c(E) = \prod_{i=1}^n (1 + x_i)$，其中 $x_i$ 为 Bott 形式的根

### 5.2 庞特里亚金类 (Pontryagin Classes)

对于实向量丛 $E \to M$（结构群 $SO(n)$），庞特里亚金类定义为：

$$p_k(E) = (-1)^k c_{2k}(E \otimes \mathbb{C}) \in H^{4k}(M; \mathbb{Z})$$

总庞特里亚金类：

$$p(E) = \prod_{i=1}^{[n/2]} (1 + x_i^2)$$

### 5.3 欧拉类 (Euler Class)

仅在偶数维定向实向量丛上定义：

$$e(E) \in H^n(M; \mathbb{Z})$$

对于黎曼流形的切丛：$\chi(M) = \langle e(TM), [M] \rangle$（高斯-博内定理）。

### 5.4 例子一览

| 示性类 | 次数 | 定义空间 |
|--------|------|----------|
| $c_1$ | 2 | $H^2(M; \mathbb{Z})$ |
| $c_2$ | 4 | $H^4(M; \mathbb{Z})$ |
| $p_1$ | 4 | $H^4(M; \mathbb{Z})$ |
| $e$ | $n$ | $H^n(M; \mathbb{Z})$ |

---

## 6. 自旋结构与旋量 (Spin Structures and Spinors)

### 6.1 自旋结构

设 $M$ 为定向黎曼流形，$P_{SO}(M)$ 为其正交标架丛。**自旋结构**是如下提升：

$$\tilde{P} \to P_{SO}(M)$$

使得结构群从 $SO(n)$ 提升到 $\mathrm{Spin}(n)$，并满足相应兼容性条件。

自旋结构存在的条件与 $w_2(TM) = 0$（第二施蒂费尔-惠特尼类为零）有关。

### 6.2 自旋流形

拥有自旋结构的流形称为**自旋流形**。在自旋流形上，可以构造**旋量束** $\Sigma M$（秩 $2^{[n/2]}$ 的复向量丛）。

### 6.3 旋量

**旋量**是自旋流形上截面 $\psi \in \Gamma(\Sigma M)$。在局部，旋量可以用 **Gamma 矩阵**表示：

$$\gamma: \mathbb{R}^n \to \mathbb{C}(2^{[n/2]})$$

满足**克里弗福德代数**关系：

$$\gamma(u)\gamma(v) + \gamma(v)\gamma(u) = -2g(u,v)I$$

---

## 7. Dirac 算子 (Dirac Operators)

### 7.1 定义

设 $E \to M$ 为自旋流形上的**Clifford 模丛**（带有兼容联络的旋量丛），**Dirac 算子**定义为：

$$\not\partial: \Gamma(E) \to \Gamma(E)$$

$$D\psi = \sum_{i=1}^n \gamma(e_i)(\nabla_{e_i}\psi)$$

其中 $\{e_i\}$ 是局部正交标架，$\nabla$ 是协变导数。

### 7.2 性质

- **椭圆算子**：在紧流形上 Fredholm
- **自伴算子**：$D^* = D$（黎曼度量下）
- **局部表达式**：$D = \sum \gamma(e_i)\nabla_{e_i}$

### 7.3 例子

| 情形 | Dirac 算子 |
|------|-----------|
| 自旋几何 | 手征 Dirac 算子 $\not\partial_A$ |
| Kähler 流形 | $\overline{\partial} + \overline{\partial}^*$ |
| 症状几何 | 手征拉普拉斯算子 |

---

## 8. 阿蒂亚-辛格指标定理 (Atiyah-Singer Index Theorem)

### 8.1 定理陈述

设 $D: \Gamma(E) \to \Gamma(F)$ 为紧流形 $M$ 上的一致椭圆复形，则：

$$\mathrm{ind}(D) = \int_M \mathrm{ch}(E - F) \cdot \mathrm{Td}(TM \otimes \mathbb{C})$$

其中：

- $\mathrm{ind}(D) = \dim \ker D - \dim \ker D^*$（解析指标）
- $\mathrm{ch}$：陈特征
- $\mathrm{Td}$：Todd 类（拓扑指标）

### 8.2 简化形式

对于**自旋流形**上的 Dirac 算子：

$$\mathrm{ind}(\not\partial) = \hat{A}(M)$$

$\hat{A}$ 为**Hirzebruch $\hat{A}$-亏格**。

### 8.3 应用

| 应用领域 | 具体例子 |
|----------|----------|
| 拓扑 | 球面定理 |
| 几何 | 正数量曲率流形的分类 |
| 物理 | APS 索引定理（边缘理论） |
| 代数几何 | 黎曼-罗赫定理的推广 |

---

## 模块类结构总结

本模块实现的类对应关系：

| 类名 | 数学概念 |
|------|----------|
| `Connection` | 协变导数、Levi-Civita 联络 |
| `Curvature` | 曲率张量、里奇曲率、标量曲率 |
| `GeodesicAdvanced` | 测地线、指数映射、雅可比场 |
| `Holonomy` | 和乐群、限制和乐群 |
| `CharacteristicClass` | 陈类、庞特里亚金类、欧拉类 |

---

## 参考文献

1. Kobayashi, S., & Nomizu, K. (1963). *Foundations of Differential Geometry*, Vol. I & II. Wiley-Interscience.
2. Chern, S.-S. (1979). *Complex Manifolds Without Potential Theory*. Springer.
3. Berline, N., Getzler, E., & Vergne, M. (1992). *Heat Kernels and Dirac Operators*. Springer.
4. Lawson, H. B., & Michelsohn, M.-L. (1989). *Spin Geometry*. Princeton University Press.
5. Atiyah, M. F., & Singer, I. M. (1968). The Index of Elliptic Operators I. *Ann. Math.*, 87(3), 484–530.