# 流形學習 (Manifold Learning)

## 1. 流形假設 (Manifold Hypothesis)

### 1.1 核心概念

流形假設認為，高維數據實際上分佈在一個低維流形上。也就是說，觀察到的 $D$ 維數據 $\mathbf{x}_1, \mathbf{x}_2, \ldots, \mathbf{x}_n$ 是由某個潛在的 $d$ 維流形 $\mathcal{M} \subset \mathbb{R}^D$（其中 $d \ll D$）上的點經過映射 $f: \mathcal{M} \to \mathbb{R}^D$ 生成的。

形式化地說，若 $\mathbf{y}_i \in \mathbb{R}^d$ 是低維潛在坐標，則觀測數據為：
$$\mathbf{x}_i = f(\mathbf{y}_i) + \epsilon_i$$

其中 $\epsilon_i$ 是噪聲，$f$ 是未知的非线性映射。

### 1.2 為什麼重要

- **維度災難的緩解**：在高維空間中，數據點往往稀疏分佈，但低維流形上的數據密度可以更高
- **幾何結構的保持**：流形學習方法嘗試保持數據的内在幾何結構
- **可視化**：將高維數據嵌入到 2D 或 3D 空間進行可視化

---

## 2. Isomap (等距映射)

### 2.1 算法思想

Isomap 的核心思想是通過圖距離來近似流形上的測地線距離，然後使用經典 MDS 進行維度約簡。

### 2.2 測地線距離

在流形上，兩點之間的最短路徑沿著流形表面，稱為**測地線距離** $d_G(i, j)$。Isomap 通過以下步驟近似：

1. 構建 $k$-近鄰圖 $G$
2. 使用 Floyd-Warshall 或 Dijkstra 算法計算圖距離 $d_G(i, j)$
3. 當 $k$ 足够大且數據密集時，$d_G(i, j) \approx$ 實際測地線距離

### 2.3 雙重中心化 (Double Centering)

给定距離矩陣 $D = [d_{ij}]$，Isomap 使用經典 MDS：

1. 計算 $D^2$（距離平方矩陣）
2. 雙重中心化：$B = -\frac{1}{2} J D^2 J$，其中 $J = I - \frac{1}{n}\mathbf{1}\mathbf{1}^T$
3. 矩陣 $B$ 可以寫成：
   $$B_{ij} = -\frac{1}{2}\left(D_{ij}^2 - \bar{D}_{i\cdot}^2 - \bar{D}_{\cdot j}^2 + \bar{D}_{\cdot\cdot}^2\right)$$

### 2.4 嵌入結果

對 $B$ 進行特征值分解 $B = V \Lambda V^T$，取前 $d$ 個最大特征值對應的特征向量：
$$\mathbf{z}_i = \left(\sqrt{\lambda_1} v_{1i}, \sqrt{\lambda_2} v_{2i}, \ldots, \sqrt{\lambda_d} v_{di}\right)$$

### 2.5 代碼實現要點

```python
# 計算 k-NN 圖
graph = _compute_knn_graph(data, k)

# 計算測地線距離
geodesic = _floyd_warshall(graph, n)

# 雙重中心化
D2 = [[d * d for d in row] for row in geodesic]
row_means = [sum(D2[i]) / n for i in range(n)]
col_means = [sum(D2[i][j] for i in range(n)) / n for j in range(n)]
total_mean = sum(sum(D2[i]) for i in range(n)) / (n * n)

B = [[-0.5 * (D2[i][j] - row_means[i] - col_means[j] + total_mean)
      for j in range(n)] for i in range(n)]
```

---

## 3. LLE (局部線性嵌入)

### 3.1 算法思想

LLE 假設數據局部是線性的，每個數據點都可以由其近鄰點的線性組合重構。

### 3.2 重構權重

對於每個點 $\mathbf{x}_i$，找到 $k$ 個近鄰 $\mathbf{x}_{j \in N(i)}$，求解最小化重構誤差：

$$\min_{w_{ij}} \left\| \mathbf{x}_i - \sum_{j \in N(i)} w_{ij} \mathbf{x}_j \right\|^2$$

約束條件：$\sum_{j \in N(i)} w_{ij} = 1$

這個問題有閉式解。設 $Z$ 為鄰居與 $\mathbf{x}_i$ 的差值矩陣，局部協方差矩陣 $C = ZZ^T$，則：

$$w = \frac{C^{-1} \mathbf{1}}{\mathbf{1}^T C^{-1} \mathbf{1}}$$

### 3.3 嵌入階段

保持重構權重不變，在低維空間中尋找保持該關系的坐標 $\mathbf{y}_i$：

$$\min_{y_i} \sum_i \left\| \mathbf{y}_i - \sum_{j \in N(i)} w_{ij} \mathbf{y}_j \right\|^2$$

定義矩陣 $M = (I - W)^T(I - W)$，最小化問題的解為 $M$ 的最小特征值對應的特征向量（忽略最小的特徵向量，因為它對應常數解）。

### 3.4 代碼實現要點

```python
# 計算重構權重 W
Z = [[data[j][d] - data[i][d] for j in neighbor_indices]
     for d in range(len(data[0]))]
C = [[sum(Z[a][i] * Z[a][j] for a in range(k_n))
      for j in range(k_n)] for i in range(k_n)]

# 正則化
trace = sum(C[i][i] for i in range(k_n))
for i in range(k_n):
    C[i][i] += 1e-6 * trace

# 求解 CW = 1
w = _solve_linear_system(C, [1.0] * k_n)

# 計算 M = (I - W)^T * (I - W)
I_minus_W = [[I[i][j] - W[i][j] for j in range(n)] for i in range(n)]
M = _mat_mat_mul(_transpose(I_minus_W), I_minus_W)
```

---

## 4. t-SNE (t-分佈隨機鄰域嵌入)

### 4.1 算法思想

t-SNE 通過保持高維空間中的相似性概率分佈來進行嵌入，使用 Student-t 分佈在低維空間中計算相似性。

### 4.2 概率分佈

**高維空間**（原始數據 $\mathbf{x}_i$）：

$$p_{j|i} = \frac{\exp(-\|\mathbf{x}_i - \mathbf{x}_j\|^2 / 2\sigma_i^2)}{\sum_{k \neq i} \exp(-\|\mathbf{x}_i - \mathbf{x}_k\|^2 / 2\sigma_i^2)}$$

$$p_{ij} = \frac{p_{j|i} + p_{i|j}}{2n}$$

**低維空間**（嵌入 $\mathbf{y}_i$）：

$$q_{ij} = \frac{(1 + \|\mathbf{y}_i - \mathbf{y}_j\|^2)^{-1}}{\sum_{k \neq l} (1 + \|\mathbf{y}_k - \mathbf{y}_l\|^2)^{-1}}$$

### 4.3 目標函數

使用 KL 散度度量兩個分佈的差异：

$$C = \sum_i \sum_j p_{ij} \log \frac{p_{ij}}{q_{ij}}$$

### 4.4 Student-t 分佈的優勢

1. **長尾效應**：當 $\|\mathbf{y}_i - \mathbf{y}_j\|$ 較大時，$q_{ij}$ 衰減更慢
2. **防止擁擠問題**：避免低維嵌入中不同簇距離太近
3. **梯度性質**：梯度計算穩定

### 4.5 訓練過程

使用梯度下降法最小化 $C$：

$$\frac{\partial C}{\partial \mathbf{y}_i} = 4 \sum_j (p_{ij} - q_{ij})(\mathbf{y}_i - \mathbf{y}_j)(1 + \|\mathbf{y}_i - \mathbf{y}_j\|^2)^{-1}$$

---

## 5. MDS (多維標度法)

### 5.1 經典 MDS

給定距離矩陣 $D = [d_{ij}]$，經典 MDS 尋找點 $\mathbf{z}_1, \ldots, \mathbf{z}_n \in \mathbb{R}^d$ 使得：

$$\|\mathbf{z}_i - \mathbf{z}_j\| \approx d_{ij}$$

通過雙重中心化矩陣 $B = -\frac{1}{2}JDDJ$ 並取前 $d$ 個特征向量。

### 5.2 度量 MDS vs 非度量 MDS

- **度量 MDS**：保持距離的比例關系
- **非度量 MDS**：只保持距離的順序（秩）

### 5.3 壓力函數 (Stress)

衡量嵌入質量：

$$\text{stress}(\mathbf{z}_1, \ldots, \mathbf{z}_n) = \sqrt{\frac{\sum_{i < j} (d_{ij} - \|\mathbf{z}_i - \mathbf{z}_j\|)^2}{\sum_{i < j} d_{ij}^2}}$$

---

## 6. Laplacian Eigenmaps (拉普拉斯科涅斯映射)

### 6.1 圖拉普拉斯矩陣

定義權重矩陣 $W$，常見選擇：
- **鄰接矩陣**：$W_{ij} = 1$ 若 $j \in N(i)$，否則 $0$
- **熱核**：$W_{ij} = \exp(-\|\mathbf{x}_i - \mathbf{x}_j\|^2 / 2\sigma^2)$

度矩陣 $D$：$D_{ii} = \sum_j W_{ji}$

圖拉普拉斯矩陣：$L = D - W$

### 6.2 目標函數

最小化：

$$\min_{\mathbf{y}} \sum_{i,j} W_{ij} \|\mathbf{y}_i - \mathbf{y}_j\|^2 = 2 \mathbf{y}^T L \mathbf{y}$$

約束 $Y^T D Y = I$（防止退化）和 $\mathbf{y}^T D \mathbf{1} = 0$（可選）。

### 6.3 幾何意義

- 若兩點相鄰 ($W_{ij}$ 大)，則它們的低維表示 $\mathbf{y}_i, \mathbf{y}_j$ 也應相近
- $L$ 的特征值趨近於 0 的方向是數據變異性最大的方向

---

## 7. Diffusion Maps (擴散映射)

### 7.1 隨機遊走與轉移矩陣

定義轉移概率矩陣 $P$：

$$P_{ij} = \frac{W_{ij}}{\sum_k W_{ik}}$$

$P$ 描述了在數據點上的隨機遊走。

### 7.2 擴散距離

$t$ 步之後的轉移概率為 $P^t$，定義擴散距離：

$$D_t^2(i, j) = \frac{1}{\pi_i} \|P^t_{i,:} - P^t_{j,:}\|^2$$

其中 $\pi$ 是穩態分佈。

### 7.3 譜表示

$P$ 是半正定的，對稱（若 $W$ 對稱）。设特征值 $\lambda_0 \geq \lambda_1 \geq \ldots \geq \lambda_{n-1}$，對應特征向量 $\psi_0, \psi_1, \ldots, \psi_{n-1}$。

擴散映射嵌入：

$$\mathbf{z}_i = (\lambda_1^t \psi_1(i), \lambda_2^t \psi_2(i), \ldots, \lambda_d^t \psi_d(i))$$

### 7.4 尺度性質

- 小尺度 $t$：捕捉局部結構
- 大尺度 $t$：捕捉全局幾何

---

## 8. API 參考

### 8.1 isomap

```python
def isomap(
    data: List[List[float]],
    n_components: int = 2,
    k: int = 5
) -> List[List[float]]:
    """Isomap 算法用於非线性維度約簡。
    
    參數:
        data: 輸入數據 (n_samples x n_features)
        n_components: 目標維度
        k: 近鄰數量
        
    返回:
        嵌入後的數據 (n_samples x n_components)
    """
```

### 8.2 LLE

```python
def LLE(
    data: List[List[float]],
    n_components: int = 2,
    k: int = 5
) -> List[List[float]]:
    """局部線性嵌入算法。
    
    參數:
        data: 輸入數據 (n_samples x n_features)
        n_components: 目標維度
        k: 近鄰數量
        
    返回:
        嵌入後的數據 (n_samples x n_components)
    """
```

### 8.3 compute_geodesic_distances

```python
def compute_geodesic_distances(
    data: List[List[float]],
    k: int = 5
) -> List[List[float]]:
    """計算流形上的近似測地線距離。
    
    參數:
        data: 輸入數據
        k: 近鄰數量
        
    返回:
        距離矩陣
    """
```

---

## 9. 總結

| 方法 | 核心思想 | 保持的結構 |
|------|----------|------------|
| Isomap | 測地線距離近似 | 全局幾何 |
| LLE | 局部線性重構 | 局部線性結構 |
| t-SNE | 概率分佈匹配 | 局部相似性 |
| MDS | 距離矩陣嵌入 | 距離 |
| Laplacian Eigenmaps | 圖拉普拉斯譜 | 局部鄰域 |
| Diffusion Maps | 隨機遊走譜 | 多尺度結構 |