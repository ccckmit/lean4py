# Kähler 几何模块

本模块实现了 Kähler 几何的基本概念，包括复流形、Hermitian 度量、Kähler 流形以及相关的上同调理论。

## 1. 复流形 (Complex Manifold)

复流形是带有复坐标卡片的光滑流形。局部同构于 $\mathbb{C}^n$ 的开集，使得坐标变换是全纯的。

**形式定义**：拓扑流形 $M$ 若存在一族坐标卡 $(U_\alpha, \phi_\alpha)$，使得 $\phi_\alpha: U_\alpha \to \mathbb{C}^n$ 为同胚，且转移映射 $\phi_\beta \circ \phi_\alpha^{-1}$ 在交集上全纯，则称 $M$ 为 $n$ 维复流形。

**相关类**：`ComplexManifold`、`AlmostComplexStructure`

## 2. Hermitian 流形

### 2.1 复结构

复结构 $J$ 是切丛上的线性映射，满足 $J^2 = -I$。这使得实切丛分解为两个 $n$ 维权子空间：

$$T_{\mathbb{C}}M = T^{1,0}M \oplus T^{0,1}M$$

### 2.2 Hermitian 度量

Hermitian 度量 $g$ 是 $TM$ 上的 Riemannian 度量，满足：

$$g(JX, JY) = g(X, Y)$$

即 $J$ 关于 $g$ 是正交的。在局部坐标中，Hermitian 度量表示为：

$$h_{i\bar{j}} = g\left(\frac{\partial}{\partial z_i}, \frac{\partial}{\partial \bar{z}_j}\right)$$

满足 $h_{j\bar{i}} = \overline{h_{i\bar{j}}}$。

**相关类**：`HermitianMetric`

## 3. Kähler 流形

### 3.1 Kähler 条件

Kähler 流形是满足以下等价条件之一的 Hermitian 流形：

1. **局部 Kähler 势**：存在局部函数 $K$（Kähler 势），使得
   $$g_{i\bar{j}} = \frac{\partial^2 K}{\partial z_i \partial \bar{z}_j}$$

2. **平行复结构**：$\nabla J = 0$，其中 $\nabla$ 是 Levi-Civita 联络

3. **Kähler 形式闭性**：$d\omega = 0$，其中
   $$\omega(X, Y) = g(JX, Y)$$

称为 Kähler 形式

### 3.2 Kähler 形式

Kähler 形式 $\omega$ 是一个 $(1,1)$-形式，在复坐标下为：

$$\omega = \frac{i}{2} \sum_{i,j} h_{i\bar{j}} dz_i \wedge d\bar{z}_j$$

**关键性质**：
- $d\omega = 0$（Kähler 条件）
- $\omega^n/n!$ 是体积形式

**相关类**：`KahlerManifold`、`KahlerMetric`

## 4. 流形层次关系

复几何中存在严格的层次结构：

```
Kähler 流形 ⊂ Hermitian 流形 ⊂ 复流形
```

- **复流形**：只有复结构 $J$
- **Hermitian 流形**：复结构 $J$ 与 Riemannian 度量 $g$ 兼容
- **Kähler 流形**：Hermitian 流形满足 $d\omega = 0$（或 $\nabla J = 0$）

典型例子：
- $\mathbb{CP}^n$（配备 Fubini-Study 度量）是 Kähler 流形
- 紧致 Hermitian 流形未必是 Kähler 流形（第一 Betti 数 $b_1$ 可为奇数）

**相关类**：`ComplexProjectiveSpace`（$\mathbb{CP}^n$ 的 Fubini-Study 度量）

## 5. Hodge 分解

对于紧致 Kähler 流形 $M$，de Rham 上同调满足**Hodge 分解**：

$$H^k(M, \mathbb{C}) = \bigoplus_{p+q=k} H^{p,q}(M, \mathbb{C})$$

其中 $H^{p,q}(M)$ 是 $(p,q)$-型上同调群。

**性质**：
- $H^{q,p} = \overline{H^{p,q}}$
- $H^{p,q} \cong H^q(M, \Omega^p)$

**相关类**：`CohomologyRing`

## 6. Hodge 数

**Hodge 数** $h^{p,q} = \dim H^{p,q}(M, \mathbb{C})$ 满足：

1. **Hodge 菱形**：
   $$h^{p,q} = h^{q,p} = h^{n-p,n-q}$$

2. **Betti 数**：
   $$b_k = \sum_{p+q=k} h^{p,q}$$

3. **Euler 特征**：
   $$\chi(M) = \sum_{p,q} (-1)^{p+q} h^{p,q}$$

**相关类**：`CohomologyRing.hodge_numbers()`

## 7. Lefschetz 超平面定理

设 $X \subset \mathbb{CP}^N$ 是光滑射影簇，$Y \subset X$ 是超平面截面，则：

1. **同构**（$k < n-1$）：
   $$H^k(X, \mathbb{Z}) \cong H^k(Y, \mathbb{Z})$$

2. **满射**（$k = n-1$）：
   $$H^k(X, \mathbb{Z}) \to H^k(Y, \mathbb{Z})$$

这导致 Hodge 数的约束，例如 $h^{p,0}$ 在超平面截面中继承。

**相关类**：`ComplexSubmanifold`

## 8. Hodge 猜想（简要提及）

**Hodge 猜想**（未解决）：在射影代数簇上，Hodge 类（即 $H^{p,p}$ 中代表代数闭链的类）由代数闭链生成。

形式表述：设 $X$ 为非奇异复射影簇，则
$$\operatorname{Hdg}^{p,p}(X) = H^{2p}(X, \mathbb{Q}) \cap H^{p,p}(X, \mathbb{C})$$
中的每个类都可以表示为代数闭链的同调类。

**与本模块的关系**：
- `FirstChernClass` 用于陈类计算
- `HolomorphicVectorBundle` 的欧拉示性数与陈类相关

## 9. 特殊 Kähler 流形

### 9.1 Calabi-Yau 流形

Calabi-Yau 流形是 $c_1(TM) = 0$ 的 Kähler 流形，等价于存在整体全纯体积形式 $\Omega$。

**性质**：
- 平凡规范线丛：$K_M = \mathcal{O}$
- Yau 定理：每个 Kähler 类中存在唯一 Ricci-平坦度量

**相关类**：`CalabiYauManifold`

### 9.2 Hermitian-Einstein 度量

Hermitian-Einstein 度量（也称 Yang-Mills 度量）满足：

$$\Lambda_\omega F_\nabla = \lambda \cdot \operatorname{id}$$

Donaldson-Uhlenbeck-Yau 定理：稳定向量丛上存在 Hermitian-Einstein 度量。

**相关类**：`HermitianEinsteinMetric`

## 10. 陈类理论

### 10.1 第一陈类

第一陈类 $c_1(M) \in H^2(M, \mathbb{Z})$ 与 Ricci 曲率相关：

$$c_1(M) = -\frac{1}{2\pi} \operatorname{Ric}$$

在 Kähler 度量下，Ricci 形式是闭的，且 $[Ric] = 2\pi c_1(M)$。

**相关类**：`FirstChernClass`

### 10.2 陈联络

Chern 联络是全纯向量丛上保持 Hermitian 度量的唯一联络，其曲率形式为：

$$\Omega = \partial\bar{\partial}(\log \det h)$$

**相关类**：`ChernConnection`

## 模块类结构

| 类 | 描述 |
|---|---|
| `ComplexManifold` | 复流形 |
| `AlmostComplexStructure` | 几乎复结构 $J$ |
| `HermitianMetric` | Hermitian 度量 $h_{i\bar{j}}$ |
| `KahlerManifold` | Kähler 流形 |
| `KahlerMetric` | Kähler 度量（从势函数构造） |
| `ChernConnection` | 陈联络 |
| `FirstChernClass` | 第一陈类 $c_1$ |
| `HolomorphicSection` | 全纯截面 |
| `ComplexProjectiveSpace` | 复射影空间 $\mathbb{CP}^n$ |
| `HermitianEinsteinMetric` | Hermitian-Einstein 度量 |
| `CalabiYauManifold` | Calabi-Yau 流形 |
| `ComplexSubmanifold` | 复子流形 |
| `CohomologyRing` | 上同调环 |
| `HolomorphicVectorBundle` | 全纯向量丛 |

## 数学背景

Kähler 几何是复几何、Riemannian 几何与代数几何的交叉点。典型应用包括：

- **弦论**：Calabi-Yau 流形作为紧化空间
- **代数几何**：射影簇的度量性质
- **复几何**：Kähler-Einstein 度量的存在性