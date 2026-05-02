# Kahler 几何测试文档

## 概述

本文档解释 `test_kahler_geometry.py` 中测试用例的数学原理。本模块测试 Kähler 几何的核心概念，包括复流形、Hermite 度量、Kähler 形式以及 Hodge 分解理论。

---

## 1. 测试验证的内容

本测试文件验证 Kähler 几何模块的核心功能：

- **复流形结构**：验证 `ComplexManifold` 和 `AlmostComplexStructure` 的基本属性
- **Hermite 度量**：验证 `HermitianMetric` 类的度量组件设置和性质
- **Kähler 流形**：验证 `KahlerManifold` 的 Kähler 条件和曲率
- **陈类理论**：验证 `ChernConnection` 和 `FirstChernClass` 的联络与陈类计算
- **Hodge 分解**：验证 `CohomologyRing` 的 Betti 数和 Hodge 数分解

---

## 2. Hermite 度量测试

### 数学背景

Hermite 度量是复流形上的 Riemann 度量，满足以下条件：

$$
g(JX, JY) = g(X, Y)
$$

其中 $J$ 是复结构算子。对于复坐标 $z^k, \bar{z}^{\bar{k}}$，度量形式为：

$$
g_{k\bar{l}} = g\left(\frac{\partial}{\partial z^k}, \frac{\partial}{\partial \bar{z}^{\bar{l}}}\right)
$$

### 测试内容

```python
class TestHermitianMetric:
    def test_set_metric_component(self):
        hm = HermitianMetric()
        hm.set_metric_component(1, 2, lambda: 1.0)
        assert hm.get_metric_component(1, 2) == 1.0
```

此测试验证：
- `set_metric_component(i, j, value)` 设置度量分量 $g_{ij}$
- `get_metric_component(i, j)` 获取对应的度量分量值
- 默认情况下，未设置的分量返回 0.0

### Hermite 性验证

```python
def test_is_hermitian(self):
    hm = HermitianMetric()
    assert hm.is_hermitian() is True
```

验证度量张量满足 Hermite 对称性：$g_{ij} = \overline{g_{ji}}$

---

## 3. Kähler 形式测试

### 数学背景

Kähler 流形是同时具有以下三种等价结构的复流形：

1. **复结构** $J$ 与 Riemann 度量 $g$ 相容
2. **Kähler 形式** $\omega(X, Y) = g(JX, Y)$ 是闭的 ($d\omega = 0$)
3. **局部上**，存在 Kähler 势函数 $\phi$ 使得 $\omega = i\partial\bar{\partial}\phi$

在线坐标中：
$$
\omega = i g_{k\bar{l}} dz^k \wedge d\bar{z}^{\bar{l}}
$$

### Kähler 条件测试

```python
def test_kahler_condition(self):
    km = KahlerManifold(2)
    assert km.kahler_condition() is True
```

验证流形满足 Kähler 条件：Kähler 形式是闭的。

### Kähler 度量测试

```python
def test_metric_from_potential(self):
    km = KahlerMetric()
    result = km.metric_from_potential()
    assert isinstance(result, dict)

def test_is_kahler(self):
    km = KahlerMetric()
    assert km.is_kahler() is True
```

验证：
- Kähler 度量可从 Kähler 势函数导出
- 度量满足 Kähler 条件

---

## 4. Hodge 分解测试

### 数学背景

在 Kähler 流形上，de Rham 上同调具有特殊的 Hoddge 分解：

$$
H^k(M, \mathbb{C}) = \bigoplus_{p+q=k} H^{p,q}(M, \mathbb{C})
$$

其中 $H^{p,q}$ 由型 $(p,q)$ 的全纯形式构成。Hodge 数 $h^{p,q} = \dim H^{p,q}$ 满足：
$$
b_k = \sum_{p+q=k} h^{p,q}
$$

### Betti 数测试

```python
def test_betti_number(self):
    cm = ComplexManifold(3)
    cr = CohomologyRing(cm)
    result = cr.betti_number(0)
    assert isinstance(result, int)
```

验证 Betti 数 $b_k = \dim H^k(M, \mathbb{C})$ 的计算。

### Hodge 数测试

```python
def test_hodge_numbers(self):
    cm = ComplexManifold(3)
    cr = CohomologyRing(cm)
    result = cr.hodge_numbers()
    assert isinstance(result, dict)
```

验证 Hodge 数 $h^{p,q}$ 的计算，返回字典类型存储所有 Hodge 数。

---

## 5. 其他重要测试

### 陈类联络

```python
class TestChernConnection:
    def test_curvature_form(self):
        cc = ChernConnection()
        result = cc.curvature_form()
        assert result is None

    def test_chern_curvature(self):
        cc = ChernConnection()
        result = cc.chern_curvature()
        assert isinstance(result, dict)
```

陈类联络是复流形上 Hermite 向量丛的联络，其曲率形式决定了陈类。

### Calabi-Yau 流形

```python
def test_yau_solution(self):
    cy = CalabiYauManifold(3)
    initial = KahlerMetric()
    result = cy.yau_solution(initial)
    assert isinstance(result, KahlerMetric)
```

Yau 的解的存在性定理证明：对于第一陈类为零的紧 Kähler 流形，存在唯一的 Ricci 平坦度量。

### Fubini-Study 度量

```python
def test_fubini_study_metric(self):
    cpp = ComplexProjectiveSpace(2)
    metric = cpp.fubini_study_metric()
    assert isinstance(metric, KahlerMetric)
```

复射影空间 $\mathbb{CP}^n$ 上的标准 Kähler 度量。

---

## 测试类列表

| 测试类 | 验证内容 |
|--------|----------|
| `TestComplexManifold` | 复流形基本结构 |
| `TestAlmostComplexStructure` | 几乎复结构 |
| `TestHermitianMetric` | Hermite 度量 |
| `TestKahlerManifold` | Kähler 流形性质 |
| `TestKahlerMetric` | Kähler 度量 |
| `TestChernConnection` | 陈类联络 |
| `TestFirstChernClass` | 第一陈类 |
| `TestHolomorphicSection` | 全纯截面 |
| `TestComplexProjectiveSpace` | 复射影空间 |
| `TestHermitianEinsteinMetric` | Hermite-Einstein 度量 |
| `TestCalabiYauManifold` | Calabi-Yau 流形 |
| `TestComplexSubmanifold` | 复子流形 |
| `TestCohomologyRing` | 上同调环 |
| `TestHolomorphicVectorBundle` | 全纯向量丛 |