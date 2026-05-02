# 圖神經網絡 (Graph Neural Networks) 數學原理文檔

本模塊實現了圖神經網絡的核心組件，用於圖結構數據的表示學習。

---

## 1. 圖神經網絡概述

圖神經網絡 (GNN) 是一類專門處理圖結構數據的神經網絡架構。傳統的神經網絡（如 CNN、RNN）主要處理規則的網格數據或序列數據，而 GNN 能夠有效處理節點間關係不規則的圖數據。

**核心思想**：每個節點的表示（embedding）通過聚合其鄰居節點的信息來更新。

數學表達式：
$$h_v^{(l+1)} = UPDATE^{(l)}(h_v^{(l)}, AGGREGATE(\{h_u^{(l)} : u \in \mathcal{N}(v)\}))$$

其中：
- $h_v^{(l)}$ 是節點 $v$ 在第 $l$ 層的隱藏狀態
- $\mathcal{N}(v)$ 是節點 $v$ 的鄰居集合
- $UPDATE$ 和 $AGGREGATE$ 分別是更新函數和聚合函數

---

## 2. 消息傳遞框架 (Message Passing Framework)

`MessagePassing` 類是所有消息傳遞神經網絡的基類。

### 2.1 聚合操作 (Aggregation)

將鄰居節點的消息進行聚合：

$$\text{aggregated} = \frac{1}{|\mathcal{N}(v)|} \sum_{u \in \mathcal{N}(v)} m_u$$

其中 $m_u$ 是鄰居節點 $u$ 傳遞的消息。

代碼實現（見 `gnn.py:14-18`）：
```python
def aggregate(self, messages: List[float], neighbors: List[int]) -> float:
    if not messages:
        return 0.0
    return sum(messages) / len(messages)
```

### 2.2 更新操作 (Update)

結合節點自身特徵與聚合後的鄰居信息：

$$h_v^{(l+1)} = h_v^{(l)} + \text{aggregated}$$

代碼實現（見 `gnn.py:20-22`）：
```python
def update(self, node_embedding: float, aggregated: float) -> float:
    return node_embedding + aggregated
```

---

## 3. 圖卷積網絡 (Graph Convolutional Network, GCN)

### 3.1 數學原理

GCN 由 Kipf 和 Welling 在 2017 年提出，核心思想是使用譜圖卷積的簡化形式。

**層級傳播規則**：
$$H^{(l+1)} = \sigma(\tilde{D}^{-\frac{1}{2}} \tilde{A} \tilde{D}^{-\frac{1}{2}} H^{(l)} W^{(l)})$$

其中：
- $\tilde{A} = A + I$ 是鄰接矩陣加上自連接（self-loop）
- $\tilde{D}$ 是 $\tilde{A}$ 的度矩陣
- $H^{(l)}$ 是第 $l$ 層的節點特徵矩陣
- $W^{(l)}$ 是可學習的權重矩陣
- $\sigma$ 是激活函數（如 ReLU）

### 3.2 實現細節

代碼實現（見 `gnn.py:25-89`）：

1. **構建鄰接矩陣**（`gnn.py:57-64`）：
```python
adj = [[0.0] * n_nodes for _ in range(n_nodes)]
for i, j in edges:
    adj[i][j] = 1.0
    adj[j][i] = 1.0
# 添加自連接
for i in range(n_nodes):
    adj[i][i] = 1.0
```

2. **對稱歸一化**（`gnn.py:70-74`）：
```python
normalized[i][j] = adj[i][j] / (math.sqrt(degree[i]) * math.sqrt(degree[j]))
```

3. **線性變換與傳播**（`gnn.py:76-84`）：
```python
HW = H @ W  # 節點特徵線性變換
output = normalized @ HW  # 圖卷積傳播
```

### 3.3 物理意義

對稱歸一化拉普拉斯矩陣 $\tilde{D}^{-\frac{1}{2}} \tilde{A} \tilde{D}^{-\frac{1}{2}}$ 的作用：
- 節點特徵的加權平均
- 折疊度歸一化：度大的節點影響較小，度小的節點影響較大
- 保持圖的無向性質

---

## 4. 圖注意力機制 (Graph Attention Network, GAT)

### 4.1 注意力機制的引入

GAT 使用注意力係數來權衡不同鄰居節點的貢獻，允許模型自動學習每個鄰居的重要性。

**注意力係數計算**：
$$e_{ij} = \text{LeakyReLU}(a^T [W h_i \| W h_j])$$

其中：
- $W$ 是線性變換矩陣
- $[ \cdot \| \cdot ]$ 是拼接操作
- $a$ 是注意力向量

### 4.2 歸一化注意力權重

使用 softmax 函數進行歸一化：
$$\alpha_{ij} = \frac{\exp(e_{ij})}{\sum_{k \in \mathcal{N}(i)} \exp(e_{ik})}$$

### 4.3 GAT 層輸出

$$h_i' = \sigma\left(\sum_{j \in \mathcal{N}(i)} \alpha_{ij} W h_j\right)$$

### 4.4 代碼實現

代碼實現（見 `gnn.py:92-155`）：

**注意力分數計算**（`gnn.py:108-112`）：
```python
def attention_score(self, h_i: List[float], h_j: List[float]) -> float:
    concat = h_i + h_j
    score = sum(self.a[k] * concat[k] for k in range(len(concat)))
    return math.exp(max(score, 0))  # LeakyReLU + softmax
```

**注意力權重歸一化**（`gnn.py:135-140`）：
```python
for i in range(n_nodes):
    row_sum = sum(adj_attention[i])
    if row_sum > 0:
        for j in range(n_nodes):
            adj_attention[i][j] /= row_sum
```

### 4.5 多頭注意力 (Multi-head Attention)

GAT 可以使用多頭注意力機制，將 $k$ 個獨立的注意力頭的結果拼接：
$$h_i' = \|_{|k=1}^K \sigma\left(\sum_{j \in \mathcal{N}(i)} \alpha_{ij}^k W^k h_j\right)$$

本實現通過 `n_heads` 參數支持多頭注意力（`gnn.py:98`）。

---

## 5. GraphSAGE：採樣與聚合

### 5.1 核心思想

GraphSAGE（SAmple and AGgrEgatE）提出了採樣鄰居並聚合的框架，解決了大規模圖的計算效率問題。

**三個基本聚合函數**：

1. **Mean 聚合**：
$$h_v^{(l+1)} = \sigma(W \cdot \text{mean}(\{h_v^{(l)}\} \cup \{h_u^{(l)} : u \in \mathcal{N}(v)\}))$$

2. **LSTM 聚合**（序列敏感性）：
$$h_v^{(l+1)} = \sigma(W \cdot \text{LSTM}([h_v^{(l)}] \oplus \text{RANDOM-SHUFFLE}(\{h_u^{(l)} : u \in \mathcal{N}(v)\})))$$

3. **Pooling 聚合**：
$$h_v^{(l+1)} = \sigma(W \cdot \max(\{\sigma(W_{pool} h_u^{(l)}) : u \in \mathcal{N}(v)\}))$$

### 5.2 鄰居採樣

為控制計算成本，GraphSAGE 採用均勻採樣：
- 1-hop：最多採樣 $S_1$ 個鄰居
- 2-hop：每個 1-hop 鄰居採樣 $S_2$ 個

典型設置：$S_1 = 25, S_2 = 10$

---

## 6. GIN（Graph Isomorphism Network）

### 6.1 設計目標

GIN 由 Xu 等人在 2019 年提出，旨在成為理論上最強大的 GNN 架構，能夠區分任何非同構的圖。

### 6.2 數學表達式

$$h_v^{(l+1)} = \text{MLP}^{(l)}\left((1 + \epsilon^{(l)}) \cdot h_v^{(l)} + \sum_{u \in \mathcal{N}(v)} h_u^{(l)}\right)$$

關鍵特點：
- 使用 **多重集合上的注入函數**（injective function）
- $\epsilon^{(l)}$ 是可學習的標量或向量
- 當 $\epsilon = 0$ 時，等價於 Sum 聚合

### 6.3 理論保證

GIN 能夠區分的所有圖對：
$$G_1 \not\cong G_2 \implies \text{GIN}(G_1) \neq \text{GIN}(G_2)$$

這得益於 Sum 聚合對於多重集合是注入的（而 Mean 和 Max 不是）。

---

## 7. 圖池化操作 (Graph Pooling)

### 7.1 節點到圖的聚合

將節點級嵌入聚合為圖級嵌入：

$$\text{graph\_embedding} = \text{POOL}(\{h_v^{(L)} : v \in V\})$$

### 7.2 三種基本池化方法

代碼實現（見 `gnn.py:158-186`）：

| 方法 | 公式 | 特點 |
|------|------|------|
| **Mean Pooling** | $\frac{1}{|V|}\sum_{v \in V} h_v$ | 對所有節點等權重 |
| **Max Pooling** | $\max_{v \in V} h_v$ | 保留最顯著特徵 |
| **Sum Pooling** | $\sum_{v \in V} h_v$ | 累積所有信息 |

```python
def graph_pooling(node_embeddings: List[List[float]], method: str = 'mean'):
    if method == 'mean':
        return [sum(emb[d] for emb in node_embeddings) / len(node_embeddings)
                for d in range(n_features)]
    elif method == 'max':
        return [max(emb[d] for emb in node_embeddings)
                for d in range(n_features)]
    elif method == 'sum':
        return [sum(emb[d] for emb in node_embeddings)
                for d in range(n_features)]
```

### 7.3 分層池化

用於層級圖表示學習：
- **DiffPool**：使用軟分配矩陣進行分層池化
- **Self-Attention Graph Pooling (SAGPool)**：基於注意力的節點選擇
- **Edge Pooling**：基於邊重要性

---

## 8. 分子圖的應用

### 8.1 分子圖表示

在計算化學中，分子可以被表示為圖結構：
- **節點**：原子（帶有特徵如原子序數、電負性等）
- **邊**：化學鍵（帶有特徵如鍵類型、鍵長等）

### 8.2 分子性質預測

GNN 在分子性質預測中的應用：

1. **藥物發現**：
$$y = \text{GNN}(\text{molecule\_graph}) \rightarrow \text{ affinity}, \text{ toxicity}, \text{solubility}$$

2. **量子化學性質預測**：
- 原子化能
- 分子軌道理論
- 電子密度分佈

### 8.3 分子特徵設計

常見的原子特徵：
| 特徵 | 維度 | 描述 |
|------|------|------|
| 原子序數 | 1 | Z |
| 電負性 | 1 | Pauling 電負性 |
| 價電子數 | 1 | 價層電子數 |
| 原子質量 | 1 | 相對原子質量 |
| 雜化類型 | One-hot | sp, sp², sp³, etc. |
| 芳香性 | 1 | 是否為芳香環 |

### 8.4 化學約束

分子圖 GNN 需要滿足的化學約束：
- **手性保持**：手性中心不應被混淆
- **鍵級別感知的邊特徵**：單鍵、雙鍵、三鍵、芳香鍵
- **環狀結構識別**：環的同構性

### 8.5 本模塊應用示例

使用本模塊進行節點分類（`gnn.py:189-237`）：
```python
def node_classification(node_features, edges, labels, n_classes=2, hidden_dim=16, n_epochs=100):
    gcn1 = GCNLayer(node_dim, hidden_dim)
    gcn2 = GCNLayer(hidden_dim, n_classes)
    
    for _ in range(n_epochs):
        hidden = gcn1.forward(node_features, edges)
        logits = gcn2.forward(hidden, edges)
        # 梯度更新邏輯...
    
    return predictions
```

---

## 9. 進階主題

### 9.1 圖網絡的表達能力

- **WL 測試**：Weisfeiler-Lehman 同構測試是 GNN 表達能力的上界
- **GNN 與 1-WL 等價**：標準 GNN 的表達能力不超過 1-WL 測試
- **超越 1-WL**：使用更高階的結構信息或更複雜的聚合函數

### 9.2 殘差連接與層歸一化

$$h_v^{(l+1)} = h_v^{(l)} + \text{GNN}(h_v^{(l)})$$

### 9.3 圖級任務的讀出函數

常用讀出函數：
- **Set2Set**：基於 LSTM 的順序讀出
- **Self-Attention 讀出**：使用 Transformer 風格的注意力機制

---

## 10. 數學符號總結

| 符號 | 含義 |
|------|------|
| $G = (V, E)$ | 圖，頂點集 $V$，邊集 $E$ |
| $h_v^{(l)}$ | 節點 $v$ 在第 $l$ 層的嵌入 |
| $\mathcal{N}(v)$ | 節點 $v$ 的鄰居集合 |
| $A$ | 鄰接矩陣 |
| $D$ | 度矩陣 |
| $W^{(l)}$ | 第 $l$ 層的權重矩陣 |
| $\sigma$ | 激活函數 |
| $\alpha_{ij}$ | 注意力權重 |

---

## 參考文獻

1. Kipf, T. N., & Welling, M. (2017). Semi-supervised classification with graph convolutional networks. *ICLR*.

2. Veličković, P., et al. (2018). Graph attention networks. *ICLR*.

3. Hamilton, W., Ying, Z., & Leskovec, J. (2017). Inductive representation learning on large graphs. *NeurIPS*.

4. Xu, K., et al. (2019). How powerful are graph neural networks? *ICLR*.

5. Gilmer, J., et al. (2017). Neural message passing for quantum chemistry. *ICML*.