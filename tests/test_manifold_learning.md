# 流形學習測試文檔

本文檔說明 `test_manifold_learning.py` 中測試用例的數學原理。

## 1. 測試驗證的內容概述

本測試文件驗證流形學習（Manifold Learning）模組的三個核心功能：

| 類別 | 測試函數 | 驗證目標 |
|------|----------|----------|
| Isomap | 3 個測試 | 等度量映射算法 |
| LLE | 3 個測試 | 局部線性嵌入算法 |
| Geodesic Distances | 2 個測試 | 測地線距離計算 |

流形學習是一種**非線性降維**技術，旨在保留數據的內在幾何結構。與線性方法（如 PCA）不同，流形學習能夠發現彎曲的、低維流形結構。

---

## 2. Isomap 測試

### 2.1 數學原理

**Isomap（Isometric Mapping）** 的核心思想：

1. **k 近鄰圖構建**：對每個數據點找到 k 個最近鄰，建立鄰接圖
2. **測地線距離估計**：使用 Floyd-Warshall 算法計算所有點對之間的最短路徑作為測地線距離
3. **經典 MDS 應用**：對距離矩陣 D 進行雙重心變換得到內積矩陣 B，然後特徵分解

```
B = -0.5 × J × D² × J
其中 J = I - (1/n) × 1 × 1ᵀ
```

### 2.2 測試用例解析

**test_isomap_basic**
```python
data = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
embedded = isomap(data, n_components=2, k=3)
```

- **驗證點**：簡單 2D 正方形點集的嵌入
- **數學含義**：四個頂點形成封閉正方形，k=3 確保每個點至少有 2 個鄰居可達
- **預期結果**：輸出維度為 n_components=2，保持點之間的測地線距離結構

**test_isomap_single_point**
```python
data = [[1.0, 2.0]]
embedded = isomap(data, n_components=1, k=1)
```

- **驗證點**：邊界條件處理
- **數學含義**：單點數據的測地線距離矩陣為 1×1 零矩陣
- **預期結果**：正確返回單點嵌入

**test_isomap_dimension_reduction**
```python
data = [[i*0.1, i*0.2, i*0.3] for i in range(10)]
embedded = isomap(data, n_components=2, k=5)
```

- **驗證點**：3D → 2D 降維
- **數學含義**：數據點位於 3D 空間中的直線上（退化流形），理想情況下可降至 1D
- **預期結果**：n_components=2 的輸出維度約束生效

---

## 3. LLE 測試

### 3.1 數學原理

**LLE（Locally Linear Embedding）** 假設數據在局部是線性的：

1. **局部重建權重**：對每個點，用 k 個最近鄰的線性組合重建該點
2. **代價函數最小化**：
   ```
   min Σᵢ ||xᵢ - Σⱼ Wᵢⱼ xⱼ||²
   ```
   約束條件：Σⱼ Wᵢⱼ = 1（權重和為 1）

3. **降維嵌入**：保持局部重建權重不變，在低維空間中找嵌入

LLE 的核心矩陣運算：
```
M = (I - W)ᵀ × (I - W)
```
嵌入即 M 的最小 n_components 個特徵值對應的特徵向量（跳過首個全 1 向量）。

### 3.2 測試用例解析

**test_lle_basic**
```python
data = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]
embedded = LLE(data, n_components=2, k=2)
```

- **驗證點**：簡單數據的局部線性結構
- **數學含義**：k=2 確保每個點有足夠鄰居進行重建，但不超過點數
- **預期結果**：保持原始數據的局部鄰域結構

**test_lle_empty_data**
```python
embedded = LLE([], n_components=2, k=2)
```

- **驗證點**：空數據的異常處理
- **預期結果**：返回空列表 `[]`

**test_lle_dimension_reduction**
```python
data = [[float(i+j) for j in range(5)] for i in range(10)]
embedded = LLE(data, n_components=2, k=4)
```

- **驗證點**：5D → 2D 降維
- **數學含義**：數據實際位於低維子空間，k=4 < n_features=5 滿足 LLE 約束
- **預期結果**：輸出為 10 個 2 維向量

---

## 4. 測地線距離測試

### 4.1 數學原理

測地線距離是流形上沿曲面傳播的距離。通過 k-NN 圖近似：

```
d_geo(i, j) ≈ 圖上最短路徑長度
```

使用 **Floyd-Warshall** 算法計算全對最短路徑：
```
for k in range(n):
    for i in range(n):
        for j in range(n):
            dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
```

### 4.2 測試用例解析

**test_geodesic_distances**
```python
data = [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0], [3.0, 0.0]]
distances = compute_geodesic_distances(data, k=2)
```

- **驗證點**：線性排列數據的測地線距離
- **數學含義**：k=2 時每個內部點有左右兩個鄰居，形成鏈狀圖
- **預期結果**：4×4 距離矩陣，直線距離等於路徑累加

**test_geodesic_self_distance**
```python
data = [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0]]
distances = compute_geodesic_distances(data, k=2)
```

- **驗證點**：自距離恆為零
- **數學含義**：dist[i][i] = 0（初始化時設定）
- **預期結果**：`abs(distances[i][i]) < 1e-6`

---

## 5. 關於 t-SNE

**注意**：當前測試文件中**不包含 t-SNE 測試用例**。

t-SNE（t-distributed Stochastic Neighbor Embedding）是另一種流行的流形學習算法，其數學原理：

- **概率分佈轉換**：將高維數據的點對相似度轉換為概率分佈
- **KL 散度最小化**：在低維嵌入中保持相似的概率分佈
- **t 分佈應用**：低維空間使用 Student t 分佈（重尾）避免擁擠問題

如需添加 t-SNE 測試，需先在 `manifold_learning.py` 中實現 `tsne` 函數。

---

## 6. 測試覆蓋範圍總結

| 功能 | 邊界條件 | 正常情況 | 降維 |
|------|----------|----------|------|
| Isomap | 單點 | 基本數據 | 3D→2D |
| LLE | 空數據 | 基本數據 | 5D→2D |
| Geodesic | 自距離 | 鏈狀數據 | - |

本測試套件主要驗證：
1. **輸出維度正確性**：`len(embedded) == n_samples` 且 `len(point) == n_components`
2. **異常處理**：空數據、單點等邊界情況
3. **算法正確性**：測地線距離的自距離為零