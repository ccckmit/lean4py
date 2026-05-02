# K-理论测试文档

本文档说明 `test_k_theory.py` 中测试用例的数学原理。

## 概述

K-理论是拓扑学与代数中研究向量丛和环上模的代数不变量重要工具。本测试文件验证了lean4py库中K-理论模块的核心功能，涵盖拓扑K-理论、代数K-理论以及相关的高级构造。

---

## 1. K₀群测试 (TestK0Group)

### 数学原理

K₀群是最基本的K-理论群。给定一个环R，K₀(R)由R上有限生成投射模的同构类组成，模加法对应直和，类比于向量丛的惠特尼和。

### 测试验证内容

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | K₀群对象的创建，确认环结构正确存储 |
| `test_add_class` | 添加向量丛类，验证类标记与阶数的记录 |
| `test_class_of_missing` | 缺失丛的类返回0（平凡丛） |
| `test_is_idempotent` | 幂等性检验：对于K₀中任意元素[x]，有[x]⊕[x] = [x⊕x] |
| `test_grothendieck_group` | 从么半群构造Grothendieck群的泛性质 |
| `test_addition` | 加法运算的正确性 |
| `test_inverse` | 逆元素的存在（Grothendieck群中每个元素均有逆） |
| `test_resolution_chebotarev` | 切博塔廖夫密度定理相关的分解（当前返回None） |

---

## 2. K₁群测试 (TestK1Group)

### 数学原理

K₁群是General Linear群的连通分同伦等价类的商群。对于环R，K₁(R) = GL(R)/GL₀(R)，其中GL(R)是一般线性群的并，GL₀(R)是其连通分量。

### 测试验证内容

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | K₁群对象的创建，确认代数结构 |
| `test_GL_n` | n阶一般线性群的构造，验证GLₙ记号 |
| `test_stabilization_map` | 稳定化映射：GLₙ(R) → GLₙ₊₁(R)，添加单位行/列 |
| `test_compute_k1` | K₁群的计算，返回集合类型 |
| `test_is_stable` | 稳定性：n足够大时GLₙ(R)不再变化 |
| `test_determinant_map` | 行列式映射：det: K₁(R) → units(R)/{±1} |
| `test_whithead_lemma` | 怀特黑德引理：K₁中某些元素的自同构平凡性 |

---

## 3. K₂群测试 (TestK2Group)

### 数学原理

K₂群由Steinberg群St(R)的中心扩张定义。Steinberg群由基本初等矩阵生成，满足 Steinberg关系。

### 测试验证内容

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | K₂群对象的创建 |
| `test_add_steinberg_generator` | 添加Steinberg生成元x_{ij}(a)，验证存储 |
| `test_compute_k2` | K₂群的计算 |
| `test_milnor_k2` | Milnor K₂群的构造（记号"Milnor"） |
| `test_tame_symbol` | 驯符号：K₂到域上局部不变量的映射 |
| `test_is_stable` | 稳定性检验 |

---

## 4. K-环测试 (TestKRing)

### 数学原理

K-环是装备λ-运算的交换环。λ-运算满足λ⁰(x)=1, λ¹(x)=x, λᵐ(x+y) = Σλⁱ(x)λⱼ(y)。Adams运算ψⁿ是基于λ-运算定义的重要不变量。

### 测试验证内容

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | K-环对象的创建 |
| `test_lambda_ring` | λ-环结构的验证 |
| `test_lambda_operation` | λ₂运算的性质：λ₂(5) = 5（二次幂等） |
| `test_adams_operation` | Adams运算ψ³(5) = 5³ = 125（对于分裂情形） |
| `test_lambda_square` | λ²运算的额外性质 |
| `test_grothendieck_riemann_roch` | Grothendieck-Riemann-Roch定理的应用 |

---

## 5. 向量丛测试 (TestTopologicalKTheory)

### 数学原理

拓扑K-理论研究拓扑空间上向量丛的代数拓扑性质。K⁰(X)是X上所有向量丛的Grothendieck群；K¹(X)通过丛的附加类构造。Bott周期性和 suspension 同构是核心性质。

### 测试验证内容

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | 拓扑K-理论对象创建 |
| `test_add_vector_bundle` | 添加向量丛到类集合，确认classes_0 |
| `test_K0` | K⁰(X)的计算，丛"E"的类存在于K₀中 |
| `test_K1` | K¹(X)的计算，空丛返回空集 |
| `test_bott_periodicity` | **Bott周期性**：K⁰(X) ≅ K⁰(Σ²X)，周期为2 |
| `test_suspension_isomorphism` | 悬挂同构：K⁰(X) ≅ K⁰(ΣX) |
| `test_chern_character` | 陈类构建的Chern特征映射 |
| `test_atiyah_hirzebruch_spectral` | Atiyah-Hirzebruch谱序列 |
| `test_complexification` | 复化运算：实丛到复丛 |

---

## 6. Grothendieck群测试

### 数学原理

Grothendieck群是从交换么半群构造阿贝尔群的标准方法。对于向量丛的半环，通过Grothendieck构造得到K₀群。

### 相关测试

- `TestK0Group.test_grothendieck_group` - 验证K₀作为丛半环的Grothendieck完备化
- `TestTopologicalKTheory.test_K0` - 验证K⁰(X)的群结构

### 关键性质

1. **泛性**：Grothendieck群是任何从给定么半群到阿贝尔群的同态的泛目标
2. **逆元存在**：每个元素都有加法逆元（形式差[a]-[b]）
3. **正性**：原始元素对应正类

---

## 7. Bott周期性测试

### 数学原理

Bott周期性是拓扑K-理论的核心定理：

- **实K-理论**：πₙ(BU) ⊗ ℚ ≅ ℚ（当n为偶数），周期8
- **复K-理论**：K⁰(X) ≅ K⁰(Σ²X)，周期2

### 测试验证

`test_bott_periodicity` 验证 `bott_periodicity() is True`，确认周期性公理成立。这保证了：
- K-理论是2-周期的（复情形）
- 可通过悬挂运算控制K-群

---

## 8. 代数K-理论测试 (TestAlgebraicKTheory)

### 数学原理

代数K-理论将拓扑K-理论的思想推广到任意环上的模范畴。Quillen的开创性工作建立了高阶K-理论的公理化框架。

### 测试验证内容

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | 代数K-理论对象 |
| `test_K0`, `test_K1`, `test_K2` | 基本K-群的计算 |
| `test_higher_K` | 高阶K群Kₙ(R)的计算 |
| `test_plus_construction` | Plus构造：BGL⁺，消除完美子群 |
| `test_Q_construction` | Q-构造，生成分类空间 |

---

## 9. Quillen K-理论测试 (TestQuillenK)

### 数学原理

Quillen的Q-构造是计算高阶代数K-群的主要方法。通过精确范畴的Q-范畴，构造分类空间并取同伦群。

### 测试验证内容

| 测试方法 | 验证内容 |
|---------|---------|
| `test_Q_category` | Q-范畴的构造 |
| `test_classifying_space` | 分类空间的构建 |
| `test_homology_of_Q` | Q的同调，字典形式返回 |
| `test_plus_minus_comparison` | Plus/minus构造的兼容性 |

---

## 10. Nil K-理论测试 (TestNilKTheory)

### 数学原理

Nil K-理论研究幂零理想的K-理论。对于带有幂零结构环，研究其Nil-基数。

### 测试验证内容

- `test_nil_ideal`: 幂零理想的识别
- `test_excision`: 切除性质，局部化后K-群不变
- `test_periodicity`: 周期性

---

## 11. 高阶K群测试 (TestHigherKGroup)

### 数学原理

高阶K群Kₙ(R)通过Q-构造或plus-构造定义，具有同伦不变性。

### 测试验证内容

| 测试方法 | 验证内容 |
|---------|---------|
| `test_creation` | 创建带阶数n的K群对象 |
| `test_compute` | Kₙ(R)的计算 |
| `test_is_homotopy_invariant` | 同伦不变性 |
| `test_devissage` | Devissage定理：高维K-群可降维计算 |

---

## 12. Atiyah-Hirzebruch谱序列测试 (TestAtiyahHirzebruch)

### 数学原理

Atiyah-Hirzebruch谱序列是将一般 cohomology 理论连接到K-理论的谱序列：

E²_{p,q} = H_p(X; K_q(pt)) ⇒ K_{p+q}(X)

### 测试验证内容

| 测试方法 | 验证内容 |
|---------|---------|
| `test_E2_page_entry` | E²页面项的计算 |
| `test_differentials` | 微分d_r的确定 |
| `test_collapse_at_E2` | E²页面崩溃判据 |
| `test_extension_problem` | 扩张问题求解 |
| `test_bordism_invariant` | 配边不变量的计算 |

---

## 总结

测试文件全面覆盖了K-理论模块的以下方面：

1. **基础K群**：K₀、K₁、K₂的构造与运算
2. **向量丛**：拓扑K-理论中丛的分类与性质
3. **Grothendieck群**：从么半群到阿贝尔群的完备化
4. **Bott周期性**：K-理论的周期性结构
5. **高级构造**：Quillen Q-构造、高阶K-群、Atiyah-Hirzebruch谱序列

这些测试确保了lean4py中K-理论实现的数学正确性和功能完整性。