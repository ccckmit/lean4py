# stacks 测试文档

## 概述

本测试文件验证 `lean4py.stacks` 模块中与栈（Stack）相关的数学结构，包括群胚（Groupoid）、预层（Presheaf）、栈（Stack）、DM栈、Artin栈、模空间、GIT商以及下降数据（Descent Data）和纤维范畴（Fibered Category）。

## 1. 群胚测试 (Groupoid)

### TestGroupoid 类

群胚是一个范畴，其中所有态射都是同构。数学上，群胚满足以下性质：

- **对象集合**：测试验证群胚可以接受对象集合 `{1, 2, 3}`
- **态射计算**：`morphisms_between` 方法计算两个对象之间的态射集合
- **传递性**：群胚中任意两个对象之间存在态射，则称其为传递的
- **连通性**：群胚中任意对象可通过态射到达其他任意对象时，称其为连通的
- **自同构群**：`aut(1)` 计算对象 1 的自同构群

群胚测试确保基本数据结构正确创建并满足群胚公理。

## 2. 预层群胚测试 (PresheafOfGroupoids)

### TestPresheafOfGroupoids 类

预层是定义在拓扑空间（或更一般的范畴）上的函子，将每个开集映射到一个群胚。

- **创建测试**：验证 PresheafOfGroupoids 可以在给定空间上创建
- **空间属性**：测试确认预层关联的空间非空

数学上，预层 $F: C^{op} \to \mathbf{Groupoid}$ 满足层化条件（对于重叠开集的唯一延拓）。

## 3. 栈测试 (Stack)

### TestStack 类

栈是满足下降条件的预层。在范畴论中，栈是层的推广，允许局部定义对象的粘合。

- **创建测试**：验证 Stack 对象可以正确创建
- **栈性质**：`is_stack()` 方法确认对象满足栈公理

栈的核心性质：对于任意覆盖，可以将局部对象粘合为整体对象。

## 4. DM 栈测试 (DMStack)

### TestDMStack 类

DM 栈（Deligne-Mumford 栈）是一种特殊的 Artin 栈，其惯性堆有被良好定义的固定点。

#### 4.1 有限稳定子群

```python
dm.has_finite_stabilizers()
```

DM 栈要求所有点的stabilizer群为有限群。这区别于 Artin 栈，后者允许无穷stabilizer。

#### 4.2 惯性栈

```python
dm.inertia_stack()
```

惯性栈 $I_X$ 是 DM 栈 $X$ 的重要不变量：
$$I_X = X \times_{\Delta} X$$
其中 $\Delta: X \to X \times X$ 是对角态射。

惯性栈在计算 DM 栈的示性类和研究轨迹公式时至关重要。

## 5. Artin 栈测试

### TestArtinStack 类

Artin 栈是具有良好模空间理论的栈，允许用光滑映射局部逼近。

- **Artin性质**：`is_artin()` 确认栈满足 Artin 条件
- **可表示性**：Artin 栈的遗忘函子可表示

Artin 栈是 DM 栈的推广，允许无穷 stabilizer 群。

## 6. 模空间测试 (ModuliSpace)

### TestModuliSpace 类

模空间参数化某种几何对象的等价类。

#### 6.1 创建与属性

```python
m = ModuliSpace("M_g", 3)
m.moduli_type  # "M_g"
m.dimension    # 3
```

- `M_g`：亏格 $g$ 的曲线模空间
- 维度：对于亏格 $g$ 的稳定曲线，维度为 $3g - 3$

#### 6.2 模空间类型

```python
m.get_moduli_type()
```

常见的模空间类型：
- $M_g$：亏格 $g$ 曲线
- $M_{g,n}$：带 $n$ 个标记点的亏格 $g$ 曲线
- $\mathcal{M}_{g,n}$：DM 堆版本

## 7. GIT 商测试 (GITQuotient)

### TestGITQuotient 类

几何不变量理论（Geometric Invariant Theory）商是构造模空间的标准方法。

#### 7.1 基本结构

```python
g = GITQuotient("X", "G")
g.space   # "X" - 作用的空间
g.group   # "G" - 线性代数群
```

#### 7.2 商构造

```python
g.quotient()
```

GIT 商的数学背景：
- 线性化的作用：$G \times L^{\otimes n} \to L^{\otimes n}$
- 稳定点：$\exists n, \mu^n(x) > 0$
- 商：$[X^{ss} / G] = \text{Proj}(\bigoplus_{n \geq 0} H^0(X, L^{\otimes n})^G)$

## 8. 下降数据测试 (Descent Data)

### TestDescentData 类

下降理论是栈理论的核心，描述如何从局部数据重建整体对象。

#### 8.1 创建与结构

```python
d = DescentData([{1}, {2}], ["data1", "data2"])
d.cover        # 覆盖 [{1}, {2}]
d.local_data   # 局部数据 ["data1", "data2"]
```

#### 8.2 下降条件

```python
d.check_descent()
```

下降数据必须满足：
- **重叠条件**：在交集上，局部数据一致
- **上环条件**：三重交集上的兼容性

#### 8.3 粘合数据

```python
d.gluing_data()
```

粘合数据方法将局部数据合并为整体数据。

#### 8.4 上圈条件

```python
d.cocycle_condition()
```

上圈条件确保：
$$\alpha_{ij} \cdot \alpha_{jk} = \alpha_{ik}$$
在覆盖的重叠区域上成立。

## 9. 纤维范畴测试 (FiberedCategory)

### TestFiberedCategory 类

纤维范畴是范畴论中的重要结构，其中每个对象有"基"对象。

#### 9.1 基本性质

```python
f = FiberedCategory("base")
f.base_category  # "base"
```

#### 9.2 纤维性

```python
f.is_fibered()
```

纤维范畴 $F: C \to D$ 满足：
- 每个态射 $f: x \to y$ 可提升唯一（如果拉回存在）
- 纤维 $F(x)$ 是范畴

**Cartesian 纤维**：对于基范畴 $C$ 的态射 $f: x \to y$，$F$ 中存在 Cartesian 提升。

## 10. 包级别导入测试

```python
from lean4py import Groupoid, Stack, DMStack, ModuliSpace, GITQuotient
```

确认主要类可以从包顶层正确导入。

## 数学背景总结

| 概念 | 数学定义 |
|------|----------|
| 群胚 | 所有态射均为同构的范畴 |
| 预层 | 从范畴 $C^{op}$ 到群胚的函子 |
| 栈 | 满足下降条件的预层 |
| DM 栈 | stabilizer 有限的 Artin 栈 |
| Artin 栈 | 光滑可表示的栈 |
| 纤维范畴 | 具有纤维结构的函子范畴 |

## 参考

- Laumon, G., & Moret-Bailly, L. (2000). *Champs algébriques*. Springer
- Olsson, M. (2016). *Algebraic Spaces and Stacks*. American Mathematical Society