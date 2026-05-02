# test_topology.py 测试文档

## 概述

本文档说明 `tests/test_topology.py` 中测试用例所验证的拓扑学数学原理。

---

## 1. 测试验证的拓扑学内容

本测试套件覆盖了拓扑学的核心概念：
- 拓扑空间的构造与性质
- 度量空间的特性
- 连续函数的基本性质
- 紧致性
- 连通性
- Hausdorff 空间
- 开映射与闭映射

---

## 2. 开集测试 (Open Set Tests)

### `TestTopologicalSpace` - `test_is_open`

**数学原理：**

设 $X$ 为集合，$\tau$ 为 $X$ 上的拓扑，当且仅当：
1. $\emptyset \in \tau$ 且 $X \in \tau$
2. 任意多个 $\tau$ 中集合的并仍在 $\tau$ 中
3. 有限多个 $\tau$ 中集合的交仍在 $\tau$ 中

则称 $(X, \tau)$ 为拓扑空间，$\tau$ 中的集合称为开集。

**测试代码：**
```python
points = {1, 2, 3}
open_sets = {frozenset(), frozenset({1}), frozenset(points)}
space = TopologicalSpace(points, open_sets)
assert space.is_open({1}) is True
assert space.is_open({2}) is False
```

验证 `{1}` 是开集（存在于 `open_sets` 中），而 `{2}` 不是开集。

### `test_interior` - 内部运算

**数学原理：**

集合 $A$ 的内部 $\operatorname{int}(A)$ 是 $A$ 中最大的开集，定义为：
$$\operatorname{int}(A) = \bigcup\{U \subseteq A \mid U \text{ 是开集}\}$$

对于拓扑空间 $(\{1,2,3\}, \tau)$，其中 $\tau = \{\emptyset, \{1\}, \{1,2,3\}\}$：
- $\operatorname{int}(\{1,2\}) = \{1\}$（因为只有 `{1}` 是包含在 `{1,2}` 中的开集）

---

## 3. 连续性测试 (Continuity Tests)

### `TestTopologicalSpace` - `test_closure`

**数学原理：**

集合 $A$ 的闭包 $\overline{A}$ 是包含 $A$ 的最小闭集，等价于：
$$\overline{A} = X \setminus \operatorname{int}(X \setminus A)$$

测试验证 `{2}` 的闭包包含 `2` 本身。

### `TestTopologicalSpace` - `test_boundary`

**数学原理：**

集合 $A$ 的边界 $\partial A$ 定义为：
$$\partial A = \overline{A} \setminus \operatorname{int}(A)$$

边界点既不属于内部也不属于外部，是拓扑学中的重要概念。

### `TestContinuousFunction` - `test_preimage`

**数学原理：**

连续函数的 $\varepsilon$-$\delta$ 定义：$f: X \to Y$ 在点 $x_0$ 连续，当 $\forall \varepsilon > 0, \exists \delta > 0$ 使得：
$$d_X(x, x_0) < \delta \implies d_Y(f(x), f(x_0)) < \varepsilon$$

开集的的原像也是开集：$f$ 连续 $\iff$ $\forall$ 开集 $V \subseteq Y$，$f^{-1}(V)$ 在 $X$ 中开。

测试验证：
```python
preimage = func.preimage({20, 30})  # 20, 30 对应原空间中的 2, 3
assert 2 in preimage and 3 in preimage
```

---

## 4. 紧致性测试 (Compactness Tests)

### `TestCompactness` - `test_is_compact`

**数学原理：**

拓扑空间 $X$ 是紧致的，当每个开覆盖都有有限子覆盖。即：若 $\bigcup_{\alpha \in I} U_\alpha \supseteq X$，其中 $U_\alpha$ 为开集，则存在有限指标集 $I_0 \subseteq I$ 使得 $\bigcup_{\alpha \in I_0} U_\alpha \supseteq X$。

有限集合是紧致的（测试使用三点集合）。

### `TestCompactness` - `test_heine_borel`

**数学原理：**

Heine-Borel 定理：在 $\mathbb{R}^n$ 中，紧致 $\iff$ 有界且闭。

但对于一般度量空间，`Compactness.heine_borel()` 方法测试紧致性。

---

## 5. 连通性测试 (Connectedness Tests)

### `TestConnectedness` - `test_is_connected`

**数学原理：**

拓扑空间 $X$ 是连通的，当且仅当不存在非平凡既开又闭的子集。即：不存在 $A \subset X$ 使得 $A \neq \emptyset$ 且 $A \neq X$，同时 $A$ 既开又闭。

测试代码：
```python
points = {1, 2, 3}
open_sets = {frozenset(), frozenset(points)}  # 只有平凡开集
space = TopologicalSpace(points, open_sets)
assert space.is_connected() is True
```

此拓扑空间是连通的，因为没有非平凡的开闭子集。

---

## 6. 其他重要测试

### Hausdorff 空间测试

**数学原理：**

Hausdorff 空间（T2 空间）满足：任意两个不同点都有不相交的开邻域。即 $\forall x \neq y \in X, \exists U \ni x, V \ni y$ 使得 $U \cap V = \emptyset$。

```python
def test_not_hausdorff_raises(self):
    points = {1, 2}
    open_sets = {frozenset(), frozenset(points)}  # 离散拓扑
    with pytest.raises(ValueError):
        HausdorffSpace(points, open_sets)
```

注意：此处 `{1,2}` 作为整体是开集，但 `{1}` 和 `{2}` 不是单独的开集，因此不满足 Hausdorff 条件。

### 度量空间测试

**数学原理：**

度量空间 $(X, d)$ 满足：
1. $d(x, y) \geq 0$，且 $d(x, y) = 0 \iff x = y$
2. $d(x, y) = d(y, x)$（对称性）
3. $d(x, z) \leq d(x, y) + d(y, z)$（三角不等式）

```python
def test_ball(self):
    ball = space.ball((0,), 1.5)  # 开球 B((0,), 1.5)
    assert (0,) in ball
    assert (1,) in ball
    assert (2,) not in ball
```

开球定义：$B(x_0, r) = \{x \in X \mid d(x, x_0) < r\}$

---

## 总结

| 测试类 | 验证内容 |
|--------|----------|
| `TestTopologicalSpace` | 拓扑空间基本性质（开集、内部、闭包、边界） |
| `TestMetricSpace` | 度量空间的距离、球、直径 |
| `TestContinuousFunction` | 连续函数的像与原像 |
| `TestCompactness` | 紧致空间的性质 |
| `TestConnectedness` | 连通空间的判别 |
| `TestHausdorffSpace` | T2 空间的验证 |
| `TestOpenMap` / `TestClosedMap` | 开映射与闭映射 |