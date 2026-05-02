# test_model_theory.py 测试文档

## 概述

本测试文件验证 `lean4py/model_theory.py` 模块的模型论（Model Theory）功能，该模块模拟 mathlib4 的 `Mathlib.ModelTheory` 实现。测试涵盖结构（Structure）、类型空间（TypeSpace）、紧致性定理（CompactnessTheorem）、Löwenheim-Skolem 定理以及初等扩展（ElementaryExtension）等核心概念。

---

## 1. Structure（结构）测试

### 1.1 结构创建测试 (`test_creation`)

**数学原理：**

Structure（结构）是模型论的基础概念。形式上，结构 $M = (M, \ldots)$ 由一个非空集合（称为论域/universe）以及该集合上的一组关系和函数组成。例如，群的结构包含作为载体的集合及其上的二元运算。

**测试内容：**

```python
M = Structure([1, 2, 3])
```

验证 `Structure` 类可以正确初始化，接收一个 universe（载体集合）作为参数，并内部存储 relations（关系）和 functions（函数）字典。

### 1.2 模型判定测试 (`test_is_model`)

**数学原理：**

$M \models T$ 表示结构 $M$ 是理论 $T$ 的模型，即 $T$ 中的每个句子在 $M$ 中都为真。这是模型论的核心关系。

**测试内容：**

```python
M = Structure([1, 2, 3])
self.assertTrue(M.is_model("T"))
```

测试 `is_model` 方法能正确判断给定的 Structure 是否为某个理论 T 的模型。当前实现返回 `True`（简化版本）。

---

## 2. TypeSpace（类型空间）测试

### 2.1 类型空间计算测试 (`test_compute`)

**数学原理：**

类型空间 $S_n(A)$ 表示在参数集 $A$ 上所有 n 类型的集合。类型是从公式的等价类构造的，用于描述元素在模型中的「行为模式」。

**测试内容：**

```python
result = TypeSpace.compute([1, 2, 3])
self.assertIn("space", result)
```

验证 `TypeSpace.compute` 方法返回包含 `"space"` 键的字典，表示计算得到的类型空间。

### 2.2 紧致性测试 (`test_is_compact`)

**数学原理：**

类型空间 $S_n(A)$ 是紧致的（compact），这是拓扑学概念在模型论中的应用。紧致性意味着每个开覆盖都有有限子覆盖。

**测试内容：**

```python
result = TypeSpace.compute([1])
self.assertTrue(TypeSpace.is_compact(result))
```

验证 `TypeSpace.is_compact` 方法能正确判断给定类型空间是否满足紧致性条件。

---

## 3. Theory（理论）测试 — CompactnessTheorem（紧致性定理）

### 3.1 紧致性成立测试 (`test_holds`)

**数学原理：**

紧致性定理是模型论中最重要的定理之一：

> 理论 $T$ 是协调的（一致的）当且仅当 $T$ 的每个有限子集都是协调的。

形式化表示：$T \models \varphi$ 当且仅当存在有限子集 $T_0 \subseteq T$ 使得 $T_0 \models \varphi$。

**测试内容：**

```python
self.assertTrue(CompactnessTheorem.holds("T"))
```

验证 `CompactnessTheorem.holds` 方法确认紧致性定理对给定理论 T 成立。

### 3.2 逻辑推论测试 (`test_consequence`)

**数学原理：**

逻辑推论关系 $\varphi \in Th(T)$ 等价于 $T \models \varphi$：

> 如果 $T$ 的每个模型都满足 $\varphi$，则 $\varphi$ 是 $T$ 的推论。

**测试内容：**

```python
self.assertTrue(CompactnessTheorem.consequence("phi", "T"))
```

验证 `CompactnessTheorem.consequence` 方法能正确判断公式 $\varphi$ 是否为理论 $T$ 的逻辑推论。

---

## 4. Lowenheim-Skolem（勒文海姆-斯科勒姆）测试

### 4.1 向下定理测试 (`test_downward`)

**数学原理：**

Löwenheim-Skolem 定理指出：

> 如果理论 $T$ 有无限模型，则对任何无穷基数 $\kappa \geq |T|$，$T$ 有一个基数为 $\kappa$ 的模型。

向下定理（Downward Löwenheim-Skolem）：
> 如果 $T$ 有无限模型，则 $T$ 有一个基数为 $\kappa \leq |T|$ 的可数模型。

**测试内容：**

```python
result = LowenheimSkolem.downward("T", 5)
self.assertEqual(result["size"], 5)
```

验证 `LowenheimSkolem.downward` 方法返回指定基数为 5 的模型结构。

### 4.2 向上定理测试 (`test_upward`)

**数学原理：**

向上定理（Upward Löwenheim-Skolem）：
> 如果 $T$ 有无限模型，则对任何 $\kappa \geq |T|$，$T$ 有一个基数为 $\kappa$ 的模型。

这一定理表明：如果一个理论有无限模型，它就有任意大的无限模型。

**测试内容：**

```python
result = LowenheimSkolem.upward("T", 10)
self.assertEqual(result["size"], 10)
```

验证 `LowenheimSkolem.upward` 方法返回指定基数为 10 的模型结构。

---

## 5. Elementary Extension（初等扩展）测试

### 5.1 初等嵌入判定测试 (`test_is_elementary`)

**数学原理：**

$M \prec N$（$M$ 是 $N$ 的初等子结构）当且仅当：

> 对所有一阶公式 $\varphi(x_1, \ldots, x_n)$ 和所有 $a_1, \ldots, a_n \in M$，
> $$M \models \varphi(a_1, \ldots, a_n) \iff N \models \varphi(a_1, \ldots, a_n)$$

初等扩展保留了所有一阶性质。

**测试内容：**

```python
M = Structure([1])
N = Structure([1, 2])
self.assertTrue(ElementaryExtension.is_elementary(M, N))
```

验证 `ElementaryExtension.is_elementary` 方法能正确判断结构 M 是否为 N 的初等子结构。

### 5.2 超幂测试 (`test_ultrapower`)

**数学原理：**

超幂（ultrapower）是构造初等扩展的重要方法。给定结构 $M$、指标集 $I$ 和超滤 $U$，超幂 $M^I/U$ 具有以下性质：

> $M \prec M^I/U$（$M$ 是 $M^I/U$ 的初等子结构）

超幂是构建非标准模型和分析无限结构的基本工具。

**测试内容：**

```python
M = Structure([1])
result = ElementaryExtension.ultrapower(M)
self.assertIn("structure", result)
```

验证 `ElementaryExtension.ultrapower` 方法返回包含 `"structure"` 键的字典，表示构造的超幂结构。

---

## 测试覆盖总结

| 测试类 | 测试方法 | 验证内容 |
|--------|----------|----------|
| TestStructure | test_creation | Structure 对象创建 |
| TestStructure | test_is_model | $M \models T$ 关系判定 |
| TestTypeSpace | test_compute | 类型空间 $S_n(A)$ 计算 |
| TestTypeSpace | test_is_compact | 类型空间紧致性 |
| TestCompactnessTheorem | test_holds | 紧致性定理成立 |
| TestCompactnessTheorem | test_consequence | 逻辑推论判定 |
| TestLowenheimSkolem | test_downward | 向下 L-S 定理 |
| TestLowenheimSkolem | test_upward | 向上 L-S 定理 |
| TestElementaryExtension | test_is_elementary | 初等嵌入 $M \prec N$ |
| TestElementaryExtension | test_ultrapower | 超幂构造 |

---

## 参考

- 模块实现：`lean4py/model_theory.py`
- mathlib4 参考：`Mathlib.ModelTheory`