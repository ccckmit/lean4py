# 稀疏编码模块文档

## 目录

1. [稀疏编码概述](#1-稀疏编码概述)
2. [字典学习](#2-字典学习)
3. [L0 范数与 L1 范数正则化](#3-l0-范数与-l1-范数正则化)
4. [匹配追踪算法](#4-匹配追踪算法)
5. [正交匹配追踪 (OMP)](#5-正交匹配追踪-omp)
6. [K-SVD 算法](#6-k-svd-算法)
7. [压缩感知与受限等距性质](#7-压缩感知与受限等距性质)

---

## 1. 稀疏编码概述

### 1.1 核心思想

稀疏编码（Sparse Coding）的核心思想是：将输入数据表示为**稀疏线性组合**的形式，即在一组**过完备字典（Overcomplete Dictionary）**的原子上的稀疏表示。

给定一个信号 $\mathbf{x} \in \mathbb{R}^n$，我们希望找到稀疏系数 $\boldsymbol{\alpha} \in \mathbb{R}^k$ 使得：

$$\mathbf{x} \approx \mathbf{D}\boldsymbol{\alpha}$$

其中：
- $\mathbf{D} \in \mathbb{R}^{n \times k}$ 是过完备字典（$k > n$）
- $\boldsymbol{\alpha}$ 是稀疏向量，其大部分元素为零或接近零
- 稀疏度（Sparsity）：$\|\boldsymbol{\alpha}\|_0 = m$ 表示非零元素的个数

### 1.2 数学形式

稀疏编码的优化问题可以表述为：

$$\min_{\boldsymbol{\alpha}} \|\boldsymbol{\alpha}\|_0 \quad \text{s.t.} \quad \|\mathbf{x} - \mathbf{D}\boldsymbol{\alpha}\|_2^2 \leq \epsilon$$

或等价的拉格朗日形式：

$$\min_{\boldsymbol{\alpha}} \|\mathbf{x} - \mathbf{D}\boldsymbol{\alpha}\|_2^2 + \lambda \|\boldsymbol{\alpha}\|_0$$

其中 $\lambda$ 是控制稀疏度的正则化参数。

### 1.3 应用场景

- 图像去噪与增强
- 特征提取与模式识别
- 信号压缩
- 脑电信号分析与神经编码
- 语音处理

---

## 2. 字典学习

### 2.1 字典的定义

字典 $\mathbf{D}$ 是一个包含 $k$ 个原子（atoms）的矩阵，每个原子 $\mathbf{d}_i \in \mathbb{R}^n$ 是字典的一列。当 $k > n$ 时，称其为**过完备字典**。

过完备字典的优势：
- 提供更多的表示自由度
- 能够更灵活地适配各种数据结构
- 允许多种等效的稀疏表示

### 2.2 字典学习问题

给定训练数据 $\mathbf{X} = [\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_N]$，字典学习的目标是同时学习：
1. 字典 $\mathbf{D}$
2. 对应的稀疏系数矩阵 $\mathbf{A}$

$$\min_{\mathbf{D}, \mathbf{A}} \sum_{i=1}^N \|\mathbf{x}_i - \mathbf{D}\boldsymbol{\alpha}_i\|_2^2 + \lambda \|\boldsymbol{\alpha}_i\|_0$$

### 2.3 交替优化策略

字典学习通常采用**交替优化**（Alternating Optimization）策略：

1. **稀疏编码步**：固定字典 $\mathbf{D}$，求解每个样本的稀疏系数
2. **字典更新步**：固定稀疏系数，更新字典原子

$$\mathbf{D} = \arg\min_{\mathbf{D}} \|\mathbf{X} - \mathbf{D}\mathbf{A}\|_F^2$$

---

## 3. L0 范数与 L1 范数正则化

### 3.1 L0 范数

L0 范数定义为向量中**非零元素的个数**：

$$\|\boldsymbol{\alpha}\|_0 = \sum_{i=1}^k \mathbb{1}(\alpha_i \neq 0)$$

L0 正则化直接约束稀疏度，但带来 **NP 难问题**——需要在所有可能的稀疏模式中搜索最优解。

### 3.2 L1 范数

L1 范数是向量元素的绝对值之和：

$$\|\boldsymbol{\alpha}\|_1 = \sum_{i=1}^k |\alpha_i|$$

L1 正则化是 L0 的**凸松弛**（Convex Relaxation），具有更好的计算性质。在一定条件下（如受限等距性质），L1 正则化可以获得与 L0 相同的解。

### 3.3 几何解释

对于二维情况：
- L0 范数约束：稀疏模式 $\{[a,0], [0,b]\}$ 上的搜索
- L1 范数约束：菱形区域 $\{|a| + |b| \leq \lambda\}$

L1 范数的约束区域是凸集，使得优化问题变为凸优化问题。

### 3.4 稀疏性保证

当满足**受限等距性质（RIP）**时，L1 范数最小化与 L0 范数最小化等价。这意味着在足够的稀疏度条件下，可以精确恢复原始信号。

---

## 4. 匹配追踪算法

### 4.1 基本思想

匹配追踪（Matching Pursuit，MP）是一种**贪心算法**，用于在过完备字典中寻找信号的稀疏表示。其核心思想是：

1. 在每一步，选择与当前残差最相关的字典原子
2. 从信号中减去该原子的投影
3. 迭代直到达到稀疏度要求

### 4.2 算法步骤

**输入**：信号 $\mathbf{x}$，字典 $\mathbf{D}$，稀疏度 $m$

**输出**：稀疏系数 $\boldsymbol{\alpha}$

1. 初始化残差 $\mathbf{r} \leftarrow \mathbf{x}$，索引集 $\Lambda \leftarrow \emptyset$
2. **for** $t = 1$ **to** $m$ **do**:
   - 计算相关性：$c_i = \langle \mathbf{r}, \mathbf{d}_i \rangle$（对所有 $i \notin \Lambda$）
   - 选择原子：$i^* = \arg\max_i |c_i|$
   - 更新索引集：$\Lambda \leftarrow \Lambda \cup \{i^*\}$
   - 更新系数：$\alpha_{i^*} \leftarrow \alpha_{i^*} + \langle \mathbf{r}, \mathbf{d}_{i^*} \rangle$
   - 更新残差：$\mathbf{r} \leftarrow \mathbf{r} - \langle \mathbf{r}, \mathbf{d}_{i^*} \rangle \mathbf{d}_{i^*}$
3. **return** $\boldsymbol{\alpha}$

### 4.3 收敛性

MP 算法每次迭代都会减少残差范数，且残差会正交于所有已选原子。收敛速度取决于字典的原子的相关性——**高度相关的原子会导致收敛缓慢**。

---

## 5. 正交匹配追踪 (OMP)

### 5.1 MP 的局限性

MP 算法的主要问题是**原子重选择问题**：由于残差与已选原子正交，但与未选原子不正交，同一原子可能被重复选择。

### 5.2 OMP 的改进

OMP 通过**最小二乘正交化**解决此问题：在选择新原子后，对所有已选原子进行**Gram-Schmidt 正交化**。

### 5.3 算法步骤

**输入**：信号 $\mathbf{x}$，字典 $\mathbf{D}$，稀疏度 $m$

**输出**：稀疏系数 $\boldsymbol{\alpha}$

1. 初始化残差 $\mathbf{r} \leftarrow \mathbf{x}$，索引集 $\Lambda \leftarrow \emptyset$
2. **for** $t = 1$ **to** $m$ **do**:
   - 计算相关性：$c_i = \langle \mathbf{r}, \mathbf{d}_i \rangle$
   - 选择原子：$i^* = \arg\max_i |c_i|$
   - 更新索引集：$\Lambda \leftarrow \Lambda \cup \{i^*\}$
   - **求解最小二乘问题**：
     $$\boldsymbol{\alpha}_\Lambda = \arg\min_{\mathbf{a}} \|\mathbf{x} - \mathbf{D}_\Lambda \mathbf{a}\|_2$$
   - 更新残差：$\mathbf{r} \leftarrow \mathbf{x} - \mathbf{D}_\Lambda \boldsymbol{\alpha}_\Lambda$
3. **return** $\boldsymbol{\alpha}$

### 5.4 本模块实现

本模块的 `OMP` 函数实现要点：

1. **相关性计算**：计算每个原子与当前残差的点积绝对值
2. **原子选择**：选择相关性最高的原子（已选原子相关性置零）
3. **最小二乘求解**：通过正规方程 $\mathbf{D}_\Lambda^T \mathbf{D}_\Lambda \boldsymbol{\alpha} = \mathbf{D}_\Lambda^T \mathbf{x}$ 求解
4. **残差更新**：使用更新后的系数计算新的残差

```python
def OMP(x, dictionary, n_nonzero=5):
    # 初始化残差和系数
    residual = x[:]
    selected = []
    coefficients = [0.0] * n_atoms

    for _ in range(n_nonzero):
        # 计算相关性
        correlations = [abs(sum(dictionary[i][j] * residual[j]
                               for j in range(n_features)))
                       for i in range(n_atoms)]

        # 选择最大相关原子
        atom_idx = correlations.index(max(correlations))
        selected.append(atom_idx)

        # 最小二乘求解
        coeffs = _solve_least_squares(DtD, Dtx, len(selected))

        # 更新系数和残差
        ...
```

### 5.5 收敛性保证

OMP 保证每次迭代后残差范数严格减小，且在字典原子规范正交时，最多 $m$ 步即可精确恢复稀疏信号。

---

## 6. K-SVD 算法

### 6.1 算法概述

K-SVD（K-Singular Value Decomposition）是由 Aharon 等人提出的著名字典学习算法。其名称源于对字典原子的 SVD 分解更新。

### 6.2 目标函数

$$\min_{\mathbf{D}, \mathbf{A}} \|\mathbf{X} - \mathbf{D}\mathbf{A}\|_F^2 \quad \text{s.t.} \quad \forall i, \|\boldsymbol{\alpha}_i\|_0 \leq T_0$$

### 6.3 算法步骤

1. **稀疏编码**：使用 OMP 或其他追踪算法更新系数矩阵 $\mathbf{A}$
2. **字典更新**：对每个原子 $\mathbf{d}_j$ 单独更新
   - 找出使用原子 $j$ 的样本索引：$\Omega_j = \{i | \alpha_j(i) \neq 0\}$
   - 计算残差矩阵：$\mathbf{E}_j = \mathbf{X} - \sum_{i \neq j} \mathbf{d}_i \boldsymbol{\alpha}_i$
   - 对 $\mathbf{E}_j$ 在 $\Omega_j$ 限制的列上进行 SVD 分解
   - 更新原子 $\mathbf{d}_j$ 为第一左奇异向量，系数相应更新

### 6.4 本模块简化实现

本模块的 `sparse_coding` 函数实现了简化版 K-SVD：

```python
def sparse_coding(data, n_atoms=20, max_iter=100, tol=1e-4):
    # 初始化字典（随机选取样本）
    indices = random.sample(range(n_samples), min(n_atoms, n_samples))
    dictionary = [[data[i][j] for i in indices] for j in range(n_features)]

    for iteration in range(max_iter):
        # 稀疏编码步：使用 OMP 求解系数
        codes = []
        for sample in data:
            code = OMP(sample, dictionary, n_nonzero=5)
            codes.append(code)

        # 字典更新步
        for j in range(n_atoms):
            # 找出使用原子 j 的样本
            indices_using = [i for i in range(n_samples)
                           if abs(codes[i][j]) > 1e-6]
            if not indices_using:
                continue

            # 计算残差和
            residual_sum = [0.0] * n_features
            for i in indices_using:
                approx = _mat_vec_mul(dictionary, codes[i])
                residual = _subtract_vectors(data[i], approx)
                residual_sum = _add_vectors(residual_sum, residual)

            # 更新原子为残差和的归一化
            norm_res = math.sqrt(sum(r**2 for r in residual_sum))
            if norm_res > 1e-10:
                for f in range(n_features):
                    dictionary[f][j] = residual_sum[f] / norm_res
```

### 6.5 收敛性

K-SVD 在每次迭代中都会减少目标函数值，算法收敛到局部最优解。

---

## 7. 压缩感知与受限等距性质

### 7.1 压缩感知基础

压缩感知（Compressed Sensing，CS）理论指出：**如果信号在某个变换域是稀疏的，则可以通过远低于奈奎斯特采样率的测量来精确恢复信号**。

核心问题：
- 测量矩阵 $\boldsymbol{\Phi} \in \mathbb{R}^{m \times n}$（$m \ll n$）
- 观测：$\mathbf{y} = \boldsymbol{\Phi}\mathbf{x}$
- 恢复：$\min \|\boldsymbol{\alpha}\|_0 \quad \text{s.t.} \quad \mathbf{y} = \boldsymbol{\Phi}\mathbf{D}\boldsymbol{\alpha}$

### 7.2 受限等距性质 (RIP)

**定义**：对于常数 $\delta_k \in (0,1)$，如果对所有稀疏度至多为 $k$ 的向量 $\mathbf{z}$ 都有：

$$(1 - \delta_k) \|\mathbf{z}\|_2^2 \leq \|\mathbf{A}\mathbf{z}\|_2^2 \leq (1 + \delta_k) \|\mathbf{z}\|_2^2$$

其中 $\mathbf{A} = \boldsymbol{\Phi}\mathbf{D}$，则称矩阵 $\mathbf{A}$ 满足 $k$ 阶受限等距性质。

### 7.3 RIP 的意义

- **精确恢复保证**：当 $\mathbf{A}$ 满足 RIP 且稀疏度 $k$ 足够小时，L1 优化与 L0 优化等价
- **测量数量下界**：恢复 $k$-稀疏信号需要 $m = O(k \log(n/k))$ 次测量
- **RIP 条件**：随机矩阵（如高斯、伯努利、部分傅里叶矩阵）以高概率满足 RIP

### 7.4 稀疏恢复条件

| 条件 | 描述 |
|------|------|
| **Spark** | 矩阵列的最小线性相关数；$\text{spark}(\mathbf{A}) > 2k$ 时可精确恢复 |
| **Mutual Coherence** | $\mu(\mathbf{A}) = \max_{i \neq j} \frac{|\langle \mathbf{a}_i, \mathbf{a}_j \rangle|}{\|\mathbf{a}_i\|_2 \|\mathbf{a}_j\|_2}$；恢复条件：$k < \frac{1}{2}(1 + 1/\mu)$ |
| **RIP** | 最严格的恢复保证条件 |

### 7.5 与稀疏编码的关系

压缩感知为稀疏编码提供了理论基础：

1. **恢复保证**：在满足 RIP 条件下，可以从少量测量中高精度恢复稀疏表示
2. **算法设计**：OMP、BP（基追踪）等算法可用于压缩感知中的稀疏恢复
3. **字典设计**：好的字典应具有低相关性，以提高稀疏表示的唯一性和可恢复性

---

## 参考资料

1. Olshausen, B. A., & Field, D. J. (1996). Emergence of simple-cell receptive field properties by learning a sparse code for natural images. *Nature*, 381(6583), 607-609.
2. Lee, H., Battle, A., Raina, R., & Ng, A. Y. (2006). Efficient sparse coding algorithms. *Advances in Neural Information Processing Systems*, 19, 801.
3. Aharon, M., Elad, M., & Bruckstein, A. (2006). K-SVD: An algorithm for designing overcomplete dictionaries for sparse representation. *IEEE Transactions on Signal Processing*, 54(11), 4311-4322.
4. Pati, Y. C., Rezaiifar, R., & Krishnaprasad, P. S. (1993). Orthogonal matching pursuit: Recursive function approximation with applications to wavelet decomposition. *Conference Record of The Twenty-Seventh Asilomar Conference on Signals, Systems and Computers*, 40-44.
5. Candes, E. J., & Tao, T. (2005). Decoding by linear programming. *IEEE Transactions on Information Theory*, 51(12), 4203-4215.
6. Donoho, D. L. (2006). Compressed sensing. *IEEE Transactions on Information Theory*, 52(4), 1289-1306.