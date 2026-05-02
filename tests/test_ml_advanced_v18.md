# test_ml_advanced_v18.py 測試文檔

## 概述

本文檔說明 `test_ml_advanced_v18.py` 測試模組的數學原理。該模組測試高級機器學習算法，包括**線性支持向量機 (SVM)** 和**決策樹**分類器。

> **注意**：原始測試文件 `test_ml_advanced_v18.py` 不存在，本文檔基於 `test_ml_advanced.py` 編寫。

---

## 1. 測試驗證內容

### 1.1 TestSVMLinear - 線性支持向量機測試

#### 數學原理

線性 SVM 的目標是找到一個最大間隔分類超平面：

```
w · x + b = 0
```

對於線性可分數據，SVM 求解以下優化問題：

```
minimize: (1/2) ||w||²
subject to: yᵢ(w · xᵢ + b) ≥ 1, ∀i
```

#### 本測試驗證的內容

| 測試方法 | 驗證目標 |
|---------|---------|
| `test_separable_data` | 驗證 SVM 對線性可分數據的處理能力 |
| `test_predict_separable` | 驗證預測函數 `sign(w·x + b)` 的正確性 |
| `test_empty_data` | 邊界情況：空數據輸入 |
| `test_regularization` | 正則化參數 λ 的正確傳遞 |

### 1.2 TestDecisionTree - 決策樹測試

#### 數學原理

決策樹採用 **CART (Classification and Regression Tree)** 算法，使用**基尼不純度 (Gini Impurity)** 作為分裂準則：

```
Gini(S) = 1 - Σ[pᵢ]²
```

其中 `pᵢ` 是類別 i 在集合 S 中的比例。

最佳分裂選擇使加權平均基尼不純度最小化：

```
Gini_split = (n_left/n) × Gini(left) + (n_right/n) × Gini(right)
```

#### 本測試驗證的內容

| 測試方法 | 驗證目標 |
|---------|---------|
| `test_simple_classification` | 驗證樹的結構完整性（葉節點/內部節點） |
| `test_predict_tree` | 驗證 `predict_tree` 返回有效標籤 |
| `test_single_class` | 單類別情況：應直接返回葉節點 |
| `test_max_depth` | 驗證 `max_depth` 參數限制生效 |

---

## 2. 高級算法測試詳解

### 2.1 SVM 的 Hinge Loss 損失函數

SVM 使用 **Hinge Loss** 加上 L2 正則化：

```
L(w) = Σ max(0, 1 - yᵢ(w · xᵢ + b)) + (λ/2) ||w||²
```

在 `ml_basics.py:118` 的實現中：
```python
if y[i] * pred < 1:
    grad[j] -= y[i] * X[i][j]
```

當 `yᵢ · pred < 1` 時（即樣本在間隔內或錯誤分類），損失函數的子梯度為 `-yᵢxᵢ`。

### 2.2 決策樹的遞歸構建

決策樹采用**深度優先遞歸**方式構建：

```
build_tree(x, y, depth):
    停止條件：
        - 所有樣本屬於同一類別
        - 達到最大深度 max_depth
        - 樣本集為空

    對每個特徵和每個可能的閾值：
        - 計算分裂後的加權基尼不純度
        - 選擇最優分裂

    遞歸構建左右子樹
```

### 2.3 測試數據設計

#### SVM 測試數據
```python
# test_separable_data: 完美線性可分
x = [[0.0, 0.0], [1.0, 1.0]]  # 兩類樣本
y = [-1, 1]

# test_predict_separable: 一維情況
x = [[0.0], [1.0], [2.0]]
y = [-1, 1, 1]
```

#### 決策樹測試數據
```python
# XOR 問題
x = [[0.0, 0.0], [1.0, 1.0], [0.0, 1.0], [1.0, 0.0]]
y = [0, 1, 0, 1]  # 需要深度至少為 2 的樹才能正確分類
```

---

## 3. v18 版本差異說明

> 由於 `test_ml_advanced_v18.py` 不存在，以下說明基於標准版本的假設差異：

v18 版本可能包含：

1. **更嚴格的數值精度測試**：驗證浮點數計算的收斂性
2. **更大規模數據測試**：測試算法在數百樣本上的性能
3. **額外的邊界情況**：如所有特徵相同、少於兩個類別等

---

## 4. 關鍵實現細節

### 4.1 SVM 返回格式

```python
# 返回：[bias, weight_1, weight_2, ...]
w = svm_linear(x, y)
# 預測：sign(w[0] + w[1]*x₁ + w[2]*x₂ + ...)
```

### 4.2 決策樹的 Dict 結構

```python
# 葉節點
{'leaf': True, 'label': class_label}

# 內部節點
{
    'leaf': False,
    'feature': feature_index,
    'threshold': threshold_value,
    'left': left_subtree,
    'right': right_subtree
}
```

### 4.3 預測邏輯

```python
def predict_tree(tree, x):
    if tree['leaf']:
        return tree['label']
    if x[tree['feature']] <= tree['threshold']:
        return predict_tree(tree['left'], x)
    return predict_tree(tree['right'], x)
```

---

## 5. 測試覆蓋範圍

- [x] SVM 基本功能（分離能力）
- [x] SVM 預測邏輯
- [x] SVM 正則化參數
- [x] SVM 空數據處理
- [x] 決策樹結構驗證
- [x] 決策樹預測
- [x] 決策樹單類別情況
- [x] 決策樹深度限制

---

## 6. 數學附錄

### 基尼不純度公式

```
Gini(S) = 1 - Σᵢ cₖ²

其中 cₖ = |{x ∈ S : label(x) = k}| / |S|
```

### 歐氏距離（K-means 等算法用）

```
d(a, b) = √[Σᵢ (aᵢ - bᵢ)²]
```

---

*文檔基於 `lean4py/ml_basics.py` v1.34.0 版本*