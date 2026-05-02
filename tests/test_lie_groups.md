# Lie 群测试文档

本文档说明 `test_lie_groups.py` 中测试用例的数学原理。

## 1. 测试概述

本测试文件验证 Lie 群模块的核心功能，涵盖李群的基本结构、指数映射、李代数、同态表示以及经典李群的具体实现。测试采用面向对象的方式，对各个类进行独立的单元测试。

## 2. 群结构测试

### 2.1 LieGroup 基本性质

`TestLieGroup` 类测试 Lie 群的基本属性：

- **维数（dimension）**：Lie 群作为流形，其维数定义为在单位元处切空间的维数。测试 `lg.dimension == 3` 验证维度属性的正确性。

- **单位元（identity）**：每个李群都有唯一的单位元 $e$，满足 $ge = eg = g$ 对所有群元 $g$ 成立。测试 `lg.identity() == 1` 验证单位元方法返回正确的值。

- **群公理验证**：
  - `is_group()` 验证闭合性、结合性、单位元存在性和逆元存在性
  - `is_manifold()` 验证 Lie 群作为光滑流形的结构

### 2.2 子群结构

`TestClosedSubgroup` 和 `TestLieSubgroup` 测试子群性质：

- **闭子群（Closed Subgroup）**：Carathéodory 定理表明，Lie 群的子群若为闭集，则是 Lie 子群。`is_closed()` 验证这一性质。

- **父子关系**：子群保留对父群的引用 `sub.parent`，确保子群结构信息的完整性。

## 3. 表示论测试

### 3.1 酉表示

`TestUnitaryRepresentation` 测试有限维 Hilbert 空间上的酉表示：

- **酉性**：表示 $\rho: G \to GL(V)$ 若满足 $\langle \rho(g)v, \rho(g)w \rangle = \langle v, w \rangle$ 对所有 $v, w \in V$ 成立，则是酉表示。

- **不可约性**：表示若没有真子空间在表示作用下保持不变，则是不可约的。`is_irreducible()` 验证这一点。

### 3.2 伴随表示

`TestAdjointRepresentation` 测试伴随表示：

伴随表示定义为 $Ad_g(X) = gXg^{-1}$（矩阵群情形），是 Lie 群在其自身 Lie 代数上的重要表示。`compute()` 方法计算特定群元和切向量的伴随作用结果。

## 4. 指数映射测试

### 4.1 ExponentialMap

`TestExponentialMap` 验证指数映射：

- **定义**：指数映射 $\exp: \mathfrak{g} \to G$ 将 Lie 代数 $\mathfrak{g}$ 的元素映射到对应李群元。对于矩阵 Lie 群，有闭式公式 $\exp(X) = \sum_{n=0}^{\infty} \frac{X^n}{n!}$。

- **基本性质**：
  - $\exp(0) = e$（单位元）：`test_exp_zero` 验证 $\exp([0,0]) = 1$
  - $\exp$ 在零点附近是局部双射

- **对数映射**：`log()` 是 `exp()` 的局部逆映射，`test_log` 验证 $\log(e) = 0$。

### 4.2 Baker-Campbell-Hausdorff 公式

`TestBakerCampbellHausdorff` 测试 BCH 公式：

BCH 公式描述指数映射的对易结构：

$$Z = \log(e^X e^Y) = X + Y + \frac{1}{2}[X,Y] + \frac{1}{12}[X,[X,Y]] - \frac{1}{12}[Y,[X,Y]] - \frac{1}{24}[Y,[X,[X,Y]]] + \cdots$$

- `compute(X, Y, n)` 计算至 $n$ 阶的 BCH 展开
- `series(t, terms)` 计算给定项的加权级数

## 5. Lie 代数与对应定理

### 5.1 Lie 代数对应

`TestLieGroupCorrespondence` 测试 Lie 群与 Lie 代数之间的对应关系：

每一个连通 Lie 群对应唯一的 Lie 代数，反之每一个有限维 Lie 代数对应唯一的单连通 Lie 群。这种对应保持了如闭合子群↔Lie 子代数的对应关系。

### 5.2 单参数子群

`TestOneParameterSubgroup` 测试单参数子群：

单参数子群是形如 $\gamma(t) = \exp(tX)$ 的光滑群同态，其中 $X \in \mathfrak{g}$ 为生成元。它对应 Lie 代数中的一维子空间。

## 6. 同态测试

### 6.1 Lie 群同态

`TestLieGroupHomomorphism` 测试群同态：

Lie 群同态 $\phi: G \to H$ 是光滑的群同态，满足：
- $\phi(e_G) = e_H$
- $\phi(ab) = \phi(a)\phi(b)$

`is_homomorphism()` 验证映射是否保持群结构。测试使用恒等映射作为简单例子验证基本性质。

## 7. 经典群测试

`TestClassicalGroups` 测试经典矩阵 Lie 群的维数：

| 群 | 定义 | 维数公式 |
|---|---|---|
| **GL(n, ℝ)** | 可逆 $n \times n$ 实矩阵 | $n^2$ |
| **SL(n, ℝ)** | 行列式为 1 的 $n \times n$ 实矩阵 | $n^2 - 1$ |
| **SO(n)** | 正交矩阵且行列式为 1 | $\frac{n(n-1)}{2}$ |
| **SU(n)** | 酉矩阵且行列式为 1 | $n^2 - 1$ |
| **Sp(n)** | 辛群 | $n(2n+1)$ |

测试验证：
- $GL(3)$：$3^2 = 9$ 维
- $SL(2)$：$2^2 - 1 = 3$ 维
- $SO(3)$：$\frac{3 \times 2}{2} = 3$ 维
- $SU(2)$：$2^2 - 1 = 3$ 维
- $Sp(1)$：$1 \times 3 = 3$ 维

## 8. 模块导入测试

`test_import_from_package` 验证从顶层包导入核心类的功能，确保 `from lean4py import LieGroup` 等导入语句正常工作。