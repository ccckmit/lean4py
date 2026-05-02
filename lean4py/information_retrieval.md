# 信息检索模块 (Information Retrieval)

本文档介绍 `lean4py/information_retrieval.py` 模块的数学原理。该模块实现了信息检索中的核心算法，包括向量空间模型、TF-IDF权重、BM25排序和余弦相似度。

---

## 1. 向量空间模型 (Vector Space Model)

向量空间模型是信息检索的基础框架，将文档和查询表示为高维空间中的向量。

### 核心思想

给定词汇表 $V = \{t_1, t_2, ..., t_m\}$，每篇文档 $d_j$ 可以表示为 $m$ 维向量：

$$\vec{d}_j = (w_{1,j}, w_{2,j}, ..., w_{m,j})$$

其中 $w_{i,j}$ 是第 $i$ 个词项在文档 $d_j$ 中的权重。

### 相似度度量

查询 $q$ 与文档 $d$ 的相关性通过计算其在向量空间中的距离或夹角来衡量。本模块使用**余弦相似度**作为主要度量方式。

---

## 2. TF-IDF 权重 (Term Frequency-Inverse Document Frequency)

TF-IDF 是最常用的词项权重计算方法，由 Salton 和 Buckley 提出。

### 词频 (Term Frequency)

词频 $tf(t, d)$ 表示词项 $t$ 在文档 $d$ 中出现的次数。本模块采用**归一化词频**：

$$tf(t, d) = \frac{\text{count}(t, d)}{|d|}$$

其中 $|d|$ 是文档 $d$ 的总词数。

### 逆文档频率 (Inverse Document Frequency)

IDF 用于降低常见词的影响，提升稀有词的重要性：

$$\text{idf}(t) = \log\left(\frac{N + 1}{df(t) + 1}\right) + 1$$

其中：
- $N$ 是文档总数
- $df(t)$ 是包含词项 $t$ 的文档数量
- 加 1 操作避免零除错误

### TF-IDF 权重计算

$$w(t, d) = tf(t, d) \times idf(t)$$

**代码实现** (`information_retrieval.py:61-66`)：
```python
tf_value = count / max(len(tokens), 1)
vector[idx] = tf_value * self.idf[idx]
```

### IDF 的性质

| 词项类型 | df 值 | IDF 值 | 权重影响 |
|---------|-------|--------|---------|
| 常见词（the, is） | 高 | 低 | 降低 |
| 中频词 | 中 | 中 | 正常 |
| 稀有词 | 低 | 高 | 提升 |

---

## 3. 余弦相似度 (Cosine Similarity)

余弦相似度衡量两个向量方向的接近程度，忽略向量长度的影响。

### 数学定义

给定两个向量 $\vec{a} = (a_1, ..., a_n)$ 和 $\vec{b} = (b_1, ..., b_n)$：

$$\text{cosine}(\vec{a}, \vec{b}) = \frac{\vec{a} \cdot \vec{b}}{\|\vec{a}\| \|\vec{b}\|} = \frac{\sum_{i=1}^{n} a_i b_i}{\sqrt{\sum_{i=1}^{n} a_i^2} \cdot \sqrt{\sum_{i=1}^{n} b_i^2}}$$

### 取值范围

- **1.0**：向量方向完全相同（完全相关）
- **0.0**：向量正交（无相关性）
- **-1.0**：向量方向完全相反（完全反相关）

### 代码实现 (`information_retrieval.py:143-162`)

```python
def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot_prod = sum(a[i] * b[i] for i in range(len(a)))
    norm_a = math.sqrt(sum(a[i]**2 for i in range(len(a))))
    norm_b = math.sqrt(sum(b[i]**2 for i in range(len(b))))
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_prod / (norm_a * norm_b)
```

### 在检索中的应用

1. 将查询 $q$ 转换为向量 $\vec{q}$
2. 将所有文档 $d_j$ 转换为向量 $\vec{d}_j$
3. 计算 $\text{score}(q, d_j) = \text{cosine}(\vec{q}, \vec{d}_j)$
4. 返回得分最高的 $k$ 篇文档

---

## 4. 潜在语义索引 (Latent Semantic Indexing, LSI)

LSI 由 Deerwester 等人于 1990 年提出，通过**奇异值分解 (SVD)** 发现文档间的潜在语义结构。

### 核心思想

原始文档-词项矩阵 $X$ 可以分解为：

$$X = U \Sigma V^T$$

其中：
- $U$：文档-概念矩阵
- $\Sigma$：奇异值对角矩阵
- $V^T$：概念-词项矩阵

### 降维过程

保留前 $k$ 个最大的奇异值：

$$X_k = U_k \Sigma_k V_k^T$$

这实现了：
1. **同义词合并**：具有相似含义的词在概念空间中接近
2. **噪声消除**：移除不重要的高频/低频信号
3. **语义关联**：发现隐含的主题关系

### 本模块状态

当前模块**未实现 LSI**，但 TF-IDF 向量可作为 LSI 的输入。如需扩展，可使用 NumPy 的 `linalg.svd` 实现：

```python
import numpy as np
from numpy.linalg import svd

def lsi_transform(tfidf_matrix, k=100):
    """截断 SVD 降维"""
    U, S, Vt = svd(tfidf_matrix, full_matrices=False)
    return U[:, :k] @ np.diag(S[:k])
```

---

## 5. BM25 排序函数 (BM25 Ranking)

BM25 (Best Matching 25) 是基于概率模型的排名算法，由 Robertson 和 Jones 提出，是 Lucene、Elasticsearch 等搜索引擎的核心算法。

### 历史背景

BM25 是 Okapi 系统的第 25 个版本，取代了早期的 TF-IDF 模型。

### 核心公式

对于查询 $q$ 和文档 $d$：

$$Score(q, d) = \sum_{i=1}^{n} \text{IDF}(t_i) \cdot \frac{tf(t_i, d) \cdot (k_1 + 1)}{tf(t_i, d) + k_1 \cdot (1 - b + b \cdot \frac{|d|}{avgdl})}$$

其中：
- $tf(t_i, d)$：词项 $t_i$ 在文档 $d$ 中的词频
- $|d|$：文档长度（词数）
- $avgdl$：平均文档长度
- $k_1$：词频饱和参数（典型值：1.2-2.0）
- $b$：文档长度归一化参数（典型值：0.75）

### IDF 公式（BM25 变体）

$$\text{IDF}(t_i) = \log\left(\frac{N - df(t_i) + 0.5}{df(t_i) + 0.5} + 1\right)$$

### 参数分析

| 参数 | 作用 | 典型值 |
|------|------|--------|
| $k_1$ | 控制词频饱和 | 1.2-2.0 |
| $b$ | 控制长度归一化 | 0.5-0.75 |

- $k_1 = 0$：忽略词频，仅用 IDF
- $b = 0$：禁用长度归一化
- $b = 1$：完全归一化

### 词频饱和性

BM25 通过分母中的 $k_1$ 因子实现**词频饱和**：高频词的贡献增长速度会减缓，避免某些词过度主导结果。

```
TF贡献
  ^
  |      /  BM25 (饱和)
  |     /
  |    /  ______  TF-IDF (线性增长)
  |   /  /
  |  /  /
  | /  /
  |/__/________________> TF
```

### 代码实现 (`information_retrieval.py:110-134`)

```python
def score(self, query: str, doc_idx: int) -> float:
    tokens = query.lower().split()
    doc_df = self.doc_freqs[doc_idx]
    doc_len = self.doc_lengths[doc_idx]
    n_docs = len(self.doc_freqs)
    
    score = 0.0
    for token in tokens:
        if token not in self.vocabulary:
            continue
        
        df = doc_df.get(token, 0)
        if df == 0:
            continue
        
        idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1)
        
        tf = df
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
        
        score += idf * numerator / denominator
    
    return score
```

---

## 6. 查询扩展 (Query Expansion)

查询扩展通过增加相关词项来改善检索效果，主要方法包括：

### 6.1 基于相关反馈

**Rocchio 算法**：
$$\vec{q}_{new} = \alpha \vec{q}_{original} + \beta \frac{1}{|D_r|} \sum_{d \in D_r} \vec{d} - \gamma \frac{1}{|D_{nr}|} \sum_{d \in D_{nr}} \vec{d}$$

其中 $D_r$ 是相关文档集，$D_{nr}$ 是不相关文档集。

### 6.2 同义词扩展

使用词林、知网等资源扩展查询词。

### 6.3 伪相关反馈 (Pseudo Relevance Feedback)

假设检索结果前 $k$ 篇都是相关的，从中提取扩展词。

### 本模块支持

当前模块提供 `build_inverted_index` 函数作为扩展基础：

```python
def build_inverted_index(documents: List[str]) -> Dict[str, List[int]]:
    """构建倒排索引"""
    index: Dict[str, List[int]] = {}
    for doc_id, doc in enumerate(documents):
        tokens = set(doc.lower().split())
        for token in tokens:
            if token not in index:
                index[token] = []
            index[token].append(doc_id)
    return index
```

---

## 模块 API 概览

| 类/函数 | 功能 |
|--------|------|
| `TFIDF` | 文档向量化，支持 `fit`、`transform`、`fit_transform` |
| `BM25` | BM25 排序，支持 `fit`、`score`、`rank` |
| `cosine_similarity` | 计算两个向量的余弦相似度 |
| `retrieve` | 基于余弦相似度的文档检索 |
| `build_inverted_index` | 构建倒排索引 |

---

## 参考文献

1. Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. *Information Processing & Management*, 24(5), 513-523.
2. Robertson, S., & Zaragoza, H. (2009). The probabilistic relevance framework: BM25 and beyond. *Foundations and Trends in Information Retrieval*, 3(4), 333-389.
3. Deerwester, S., et al. (1990). Indexing by latent semantic analysis. *Journal of the American Society for Information Science*, 41(6), 391-407.
4. Manning, C. D., Raghavan, P., & Schütze, H. (2008). *Introduction to Information Retrieval*. Cambridge University Press.