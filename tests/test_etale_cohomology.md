# Étale 上同调测试文档

本文件说明 `test_etale_cohomology.py` 中测试用例的数学原理。

## 1. 测试验证内容概述

这些测试验证了 étale 上同调模块的核心功能，包括：
- Étale 拓扑与覆盖空间
- Étale 上同调群的计算
- 基变换定理
- Weil 猜想（Deligne 定理）

---

## 2. Étale 态射测试 (TestEtaleSite)

### 数学原理

**Étale 态射** 是代数几何中类似于拓扑空间中局部同构的态射。形式上，态射 `f: Y → X` 称为 étale 的是指：
- `f` 是平坦的
- `f` 是无分歧的（unramified）

### 测试用例说明

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | 创建 Étale 站点对象，验证概型关联 |
| `test_is_etale_covering` | 验证给定的覆盖族是否为 étale 覆盖 |
| `test_topology` | 验证返回的拓扑类型为 `"etale_topology"` |

**数学背景**：Étale 覆盖在代数几何中的地位类似于拓扑空间中的局部同构覆盖，它们是研究概型局部性质的基本工具。

---

## 3. 基本群测试 (EtaleCohomologyGroup)

### 数学原理

**Étale 上同调群** `H^i_et(X, F)` 是经典拓扑上同调的代数几何类比。其中：
- `X` 是概型
- `F` 是étale 层（sheaf）
- `i` 是上同调次数

### 测试用例说明

| 测试方法 | 验证内容 |
|---------|---------|
| `test_compute` | 计算上同调群，验证返回结构 |
| `test_is_finite` | 对于 proper 概型，验证上同调群是有限的 |

**数学背景**：对于 proper 概型上的有限生成层，étale 上同调群 `H^i_et(X, F)` 是有限的。这是 étale 上同调的基本 finiteness 定理。

---

## 4. 基变换测试 (TestBaseChange)

### 数学原理

**基变换定理** 是 étale 上同调中最重要的定理之一。设 `f: X → Y` 是某种态射，`g: Y' → Y` 是平坦基变换，则有基变换同构：

```
g*Rf* ≅ Rf'*g'*
```

其中 `X' = X ×_Y Y'`。

### 测试用例说明

| 测试方法 | 验证内容 |
|---------|---------|
| `test_flat_base_change` | 验证平坦基变换定理 |
| `test_is_cdh_descendable` | 验证 cdh 下降性质 |

**数学背景**：
- 平坦基变换定理确保上同操作与平坦基变换交换
- cdh（经典分歧满射，classical proper dh）下降用于交换局部上同调信息

---

## 5. Weil 猜想测试 (TestWeilConjectures)

### 数学原理

**Weil 猜想** 是 1940 年代 André Weil 提出的关于代数簇上 zeta 函数的三条猜想。Deligne 于 1974 年证明了这些猜想。

设 `X` 是定义在有限域 `𝔽_q` 上的非奇异射影簇，`Z(X, t)` 是 zeta 函数：

```
Z(X, t) = exp(Σ_{n≥1} #X(𝔽_{q^n}) · t^n/n)
```

### 猜想内容

| 猜想 | 内容 |
|-----|------|
| 有理性 | `Z(X, t)` 是 `t` 的有理函数 |
| 函数方程 | `Z(X, t)` 满足函数方程 |
| Riemann 假设 | 零点 `α` 满足 `|α| = q^(i/2)`，其中 `i` 是权重 |

### 测试用例说明

| 测试方法 | 验证内容 |
|---------|---------|
| `test_rationality` | 验证 zeta 函数的有理性 |
| `test_functional_equation` | 验证函数方程 |
| `test_riemann_hypothesis` | 验证 Riemann 假设（绝对值条件）|

**数学背景**：Weil 猜想建立了代数几何与数论的深刻联系，在密码学、编码理论等领域有重要应用。

---

## 6. 测试与 mathlib4 对齐

本模块对应 mathlib4 中的：
- `Mathlib.AlgebraicGeometry.EtaleCohomology`
- `Mathlib.AlgebraicTopology.EtaleSite`
- `Mathlib.NumberTheory.WeilConjectures`

---

## 7. 参考文献

- Grothendieck, A., et al. *Théorie des Topos et Cohomologie Étale des Schémas* (SGA 4)
- Deligne, P. *La conjecture de Weil I, II*
- Hartshorne, R. *Algebraic Geometry*, Chapter III