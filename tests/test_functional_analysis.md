# 泛函分析测试文档 (test_functional_analysis.py)

本文档解释 `test_functional_analysis.py` 测试文件背后的数学原理。

## 1. 测试验证的内容概述

本测试文件验证泛函分析核心概念的实现，包括：
- 赋范空间 (Normed Space)
- 内积空间 (Inner Product Space)
- 巴拿赫空间 (Banach Space)
- 希尔伯特空间 (Hilbert Space)
- 有界线性算子 (Bounded Linear Operator)
- 对偶空间 (Dual Space)

---

## 2. 赋范空间测试 (Normed Space)

### 数学原理

赋范空间是带有范数概念的向量空间。范数 $\|\cdot\|: V \to \mathbb{R}$ 满足：

1. **正定性**: $\|x\| \geq 0$，且 $\|x\| = 0 \iff x = 0$
2. **齐次性**: $\|\alpha x\| = |\alpha| \cdot \|x\|$
3. **三角不等式**: $\|x + y\| \leq \|x\| + \|y\|$

### 测试用例

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | 空间维度正确创建 (dim = 3) |
| `test_norm` | 验证 $\\|(3,4)\\| = \sqrt{3^2 + 4^2} = 5$ |
| `test_is_normed` | 验证正交向量 $(1,0)$ 和 $(0,1)$ 满足范数公理 |
| `test_is_complete` | 确认空间是完备的 |
| `test_to_topological_space` | 范数诱导拓扑空间的转换 |

---

## 3. 内积空间测试 (Inner Product Space)

### 数学原理

内积空间是带有内积 $\langle \cdot, \cdot \rangle: V \times V \to \mathbb{R}$ 的向量空间，满足：

1. **共轭对称性**: $\langle x, y \rangle = \overline{\langle y, x \rangle}$
2. **线性性**: $\langle ax + by, z \rangle = a\langle x, z \rangle + b\langle y, z \rangle$
3. **正定性**: $\langle x, x \rangle \geq 0$，且 $\langle x, x \rangle = 0 \iff x = 0$

内积诱导范数：$\|x\| = \sqrt{\langle x, x \rangle}$

两向量夹角：$\cos \theta = \frac{\langle x, y \rangle}{\|x\| \|y\|}$

### 测试用例

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | 空间维度正确创建 (dim = 3) |
| `test_inner` | 验证 $\langle (1,2), (3,4) \rangle = 1 \times 3 + 2 \times 4 = 11$ |
| `test_norm_from_inner` | 验证诱导范数 $\\|(3,4)\\| = \sqrt{9+16} = 5$ |
| `test_is_inner_product` | 验证内积公理（线性性、正定性等） |
| `test_angle` | 验证标准基向量夹角为 $\pi/2$（正交） |

---

## 4. 巴拿赫空间测试 (Banach Space)

### 数学原理

巴拿赫空间是完备的赋范空间。**完备性**指所有柯西序列都收敛到空间中的某个元素。

形式化：若 $\\{x_n\\}$ 满足 $\\|x_n - x_m\\| \to 0$（当 $n,m \to \infty$），则存在 $x$ 使 $\\|x_n - x\\| \to 0$。

有限维赋范空间（如 $\mathbb{R}^n$）天然是巴拿赫空间。

### 测试用例

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | 空间维度正确创建 (dim = 3) |
| `test_is_banach` | 验证空间的完备性（所有柯西序列收敛） |

---

## 5. 希尔伯特空间测试 (Hilbert Space)

### 数学原理

希尔伯特空间是完备的内积空间。结合了内积结构和完备性，是量子力学和函数分析的核心概念。

**正交投影**：对于闭子空间 $M \subset H$，任意 $x \in H$ 可唯一分解为 $x = P_M x + (x - P_M x)$，其中 $P_M x \in M$ 且 $(x - P_M x) \perp M$。

**格拉姆-施密特正交化**：将线性无关向量组 $\\{v_1, ..., v_n\\}$ 转化为正交单位向量组 $\\{u_1, ..., u_n\\}$：

$$u_1 = v_1$$
$$u_2 = v_2 - \frac{\langle v_2, u_1 \rangle}{\langle u_1, u_1 \rangle} u_1$$
$$u_3 = v_3 - \frac{\langle v_3, u_1 \rangle}{\langle u_1, u_1 \rangle} u_1 - \frac{\langle v_3, u_2 \rangle}{\langle u_2, u_2 \rangle} u_2$$
以此类推。

### 测试用例

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | 空间维度正确创建 (dim = 3) |
| `test_is_hilbert` | 验证空间既是完备的又是内积空间 |
| `test_projection` | 验证向子空间的正交投影计算 |
| `test_gram_schmidt` | 验证正交化过程产生正确数量的向量 |

---

## 6. 有界线性算子测试 (Bounded Operator)

### 数学原理

有界线性算子 $T: V \to W$ 满足：
1. **线性性**: $T(ax + by) = aT(x) + bT(y)$
2. **有界性**: 存在 $M \geq 0$ 使 $\|T(x)\|_W \leq M \|x\|_V$ 对所有 $x$ 成立

算子范数定义为：
$$\|T\| = \sup \\{\|T(x)\|_W : \|x\|_V = 1\\}$$

有限维空间上的线性算子自动有界。

### 测试用例

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | 验证定义域和陪域正确关联 |
| `test_apply` | 验证算子作用于向量产生正确维度的结果 |
| `test_operator_norm` | 验证算子范数非负 |
| `test_is_bounded` | 验证算子的有界性 |

---

## 7. 对偶空间与里斯表示定理

### 数学原理

**对偶空间** $V^*$ 是从赋范空间 $V$ 到 $\mathbb{R}$ 的所有有界线性泛函的集合。

**里斯表示定理**：在希尔伯特空间 $H$ 中，每个有界线性泛函 $f \in H^*$ 都可以唯一表示为 $f(x) = \langle x, y \rangle$ 对某个 $y \in H$。

### 测试用例

| 测试方法 | 验证内容 |
|---------|---------|
| `test_riesz_representation` | 验证线性泛函的里斯表示返回正确维度的向量 |

---

## 8. 算子范数测试

### 数学原理

算子范数是定义在有界线性算子空间上的范数，满足：
1. $\|T\| \geq 0$，且 $\|T\| = 0 \iff T = 0$
2. $\|\alpha T\| = |\alpha| \|T\|$
3. $\|T + S\| \leq \|T\| + \|S\|$

### 测试用例

| 测试方法 | 验证内容 |
|---------|---------|
| `test_is_norm` | 验证算子范数满足范数公理 |

---

## 总结

这些测试覆盖了泛函分析的核心结构，从基础的赋范空间和内积空间，到更高级的巴拿赫空间和希尔伯特空间，以及有界算子和对偶空间的理论。这些概念构成了现代分析学和数学物理的基石。