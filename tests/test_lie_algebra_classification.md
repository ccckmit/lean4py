# Lie 代數分類測試文檔

本文檔說明 `test_lie_algebra_classification.py` 中測試用例所驗證的數學原理。

## 1. 概述

測試模組基於經典的 **半單李代數分類定理**：每一個有限維半單李代數都對應於一個不可約根系，而不可約根系由其 Dynkin 圖唯一確定。分類過程的核心是：

1. 構造根系（Root System）
2. 計算 Dynkin 圖
3. 從 Cartan 矩陣進行分類

---

## 2. 根系測試（Root System）

### 2.1 數學原理

根系 $\Phi$ 是由有限個非零向量（稱為**根**）組成的集合，滿足：
- 封閉性：若 $\alpha, \beta \in \Phi$，則反射 $s_\alpha(\beta) \in \Phi$
- 封閉性：$\Phi$ 中不含 $0$

根系的核心性質：
- **正根與單根**：每個根系可劃分為正根 $\Phi^+$ 和負根 $\Phi^-$，簡單根是無法表示為兩個正根之和的正根
- **Weyl 群**：由所有根反射生成的有限群，描述根系的對稱性

### 2.2 測試用例

| 測試 | 驗證內容 |
|------|----------|
| `test_creation` | 檢驗根系對象可正確初始化，確認 rank 為 2 |
| `test_creation_with_roots` | 檢驗可通過指定根向量集合創建根系 |
| `test_compute_positive_roots` | 驗證計算正根集合的功能 |
| `test_compute_simple_roots` | 驗證計算單根集合的功能 |
| `test_weyl_group_generators` | 驗證 Weyl 群的生成元計算 |

### 2.3 代數結構關係

```
RootSystem (根系)
    ├── rank: 秩（根系維度）
    ├── roots: 根向量集合
    ├── positive_roots(): 正根
    └── simple_roots(): 單根
```

---

## 3. Dynkin 圖測試

### 3.1 數學原理

Dynkin 圖是根系分類的圖形表示：
- 每個節點代表一個單根
- 節點間的連線表示對應單根的角度關係
- 連線上可標記數字表示重數

**連線規則**：
- 無連線：單根正交（夾角 $90^\circ$）
- 單線：夾角 $120^\circ$（典型情況）
- 雙線或三線：對應於 $BC_n$ 或 $G_2$ 等例外情況

**分類邏輯**：
- 若圖為空（無節點）：為平凡李代數
- 若無連線且有多個節點：為 $A_1^n$（互不相關的 $A_1$ 直和）
- 若為單線連接的鏈：可能為 $A_n, B_n, C_n, D_n$ 型
- 若包含雙邊或三邊：對應例外型 $G_2, F_4$

### 3.2 測試用例

| 測試 | 驗證內容 |
|------|----------|
| `test_classify_A1` | 單節點無連線 → 分類為 $A_1$ |
| `test_classify_A2` | 兩節點單線連接 → 分類為 $A_2$ |
| `test_classify_G2` | 兩節點三線連接 → 分類為 $G_2$ |
| `test_classify_F4` | 兩節點四線連接 → 分類為 $F_4$ |
| `test_has_double_edge` | 區分單線與雙線 |
| `test_is_simple_chain` | 驗證鏈狀結構判定 |
| `test_rank` | 節點數等於根系秩 |

### 3.3 典型 Dynkin 圖對應

| 類型 | 圖結構 |
|------|--------|
| $A_n$ | 線性鏈（$n$ 個節點） |
| $D_n$ | 分叉於倒數第二節點 |
| $E_6, E_7, E_8$ | 含分叉的例外型 |
| $G_2$ | 兩節點，三線連接 |
| $F_4$ | 含雙線的鏈 |

---

## 4. Cartan 矩陣測試

### 4.1 數學原理

Cartan 矩陣 $A = (a_{ij})$ 定義為：

$$a_{ij} = \frac{2(\alpha_i, \alpha_j)}{(\alpha_j, \alpha_j)}$$

其中 $\alpha_i, \alpha_j$ 為單根，$(\cdot, \cdot)$ 為 Killing 型誘導的內積。

**Cartan 矩陣的性質**：
1. 對角元素恆為 2
2. 非對角元素為 $0, -1, -2, -3$ 之一
3. 可逆且逆矩陣元素均為整數
4. 正定性（對半單根系）

**從 Cartan 矩陣分類**：
- 計算行列式
- 檢測是否符合經典型或例外型的標準形式
- 確定具體類型（如 $A_n, B_n, C_n, D_n, E_6, E_7, E_8, F_4, G_2$）

### 4.2 測試用例

| 測試 | 驗證內容 |
|------|----------|
| `test_classify_from_cartAN_single` | $A = [2]$ → $A_1$ |
| `test_classify_from_cartAN_A2` | $A = \begin{pmatrix} 2 & -1 \\ -1 & 2 \end{pmatrix}$ → $A_2$ |
| `test_is_cartan_matrix_valid` | 標準 $A_2$ 矩陣應為有效 Cartan 矩陣 |
| `test_is_cartan_matrix_invalid` | 正對角元素（如 $[2, 1; 1, 2]$）不是有效 Cartan 矩陣 |
| `test_is_cartan_matrix_wrong_diag` | 對角線不為 2 的矩陣無效 |

### 4.3 Cartan 矩陣示例

```
A_1: [2]
A_2: [[2, -1], [-1, 2]]
G_2: [[2, -1], [-1, 2]]  (需配合根系結構識別)
```

---

## 5. 權與最高權向量測試

### 5.1 權（Weight）

**數學原理**：
權是表示空間中的向量，滿足：
- 對於每個根 $\alpha$，權 $\lambda$ 滿足對稱性條件
- 支配權（dominant weight）：所有基本權的非負整數線性組合
- 正則權（regular weight）：不在任何根超平面上的權

**權的內積**：
$$(\lambda, \mu) = \sum_i \lambda_i \mu_i$$

這用於計算權的長度和角度關係。

### 5.2 測試用例

| 測試 | 驗證內容 |
|------|----------|
| `test_inner_product` | $[1,2] \cdot [3,4] = 1\times3 + 2\times4 = 11$ |
| `test_is_dominant` | $[1,2]$ 為支配權（所有分量非負） |
| `test_is_regular` | $[1,2]$ 為正則權 |
| `test_is_integral` | 分量為實數即為整格權 |

### 5.3 最高權向量

**數學原理**：
最高權向量是满足：
$$H_\alpha \cdot v = 0, \quad E_\alpha \cdot v \neq 0 \text{（對所有正根 $\alpha$）}$$

其中 $H_\alpha$ 為對應於根 $\alpha$ 的餘根，$E_\alpha$ 為對應的冪零元。

---

## 6. Weyl 群測試

### 6.1 數學原理

Weyl 群由根系中每個根 $\alpha$ 確定的反射生成：

$$s_\alpha(v) = v - \frac{2(v, \alpha)}{(\alpha, \alpha)} \alpha$$

**關鍵性質**：
- 有限群（根的有限性保證）
- 由單根反射生成的簡單反射
- 最長元（longest element）：Weyl 群中唯一的極大長度元素
- 軌道（orbit）：向量在 Weyl 群作用下的全體像是理解根系對稱性的關鍵

### 6.2 測試用例

| 測試 | 驗證內容 |
|------|----------|
| `test_reflect` | 對 $[1,0]$ 關於 $[1,0]$ 反射得 $[-1,0]$ |
| `test_reflect_zero_vector` | 零向量反射後不變 |
| `test_orbit` | 計算向量在 Weyl 群下的軌道 |
| `test_length` | 單位元長度為 0 |
| `test_longest_element` | 最長元是 Weyl 群中的特殊元素 |

---

## 7. Verma 模測試

### 7.1 數學原理

Verma 模 $M(\lambda)$ 是權 $\lambda$ 的**最高權模**，它是具有該最高權的最小的一般域模。

**結構性質**：
- 字符（character）：$M(\lambda)$ 的字符形如 $e^\lambda \prod_{\alpha \in \Phi^+} (1 - e^{-\alpha})^{-1}$
- 簡單性：Verma 模通常不是簡單模
- 根基（radical）與餘根基（socle）：決定模的合成列

### 7.2 測試用例

| 測試 | 驗證內容 |
|------|----------|
| `test_character` | 字符包含 "M"（標記最高權） |
| `test_is_simple` | Verma 模一般不是簡單模 |
| `test_socle` | 餘根基為權的集合 |
| `test_radical` | 根基為某個子模 |

---

## 8. Kostant 形式測試

### 8.1 數學原理

Kostant 形式是泛包絡代數 $U(\mathfrak{g})$ 的一個子代數，具有：
- PBW 基底（Poincaré-Birkhoff-Witt）：單項式的有序基
- 典範基（canonical basis）：由 Kazhdan-Lusztig 理論導出的基

### 8.2 測試用例

| 測試 | 驗證內容 |
|------|----------|
| `test_PBW_basis` | 返回 "monomials"（單項式基） |
| `test_canonical_basis` | 返回 "canonical"（典範基） |

---

## 9. 簡單李代數分類測試

### 9.1 分類定理

有限維半單李代數的分類由 Dynkin 圖完全決定：

| 類型 | 描述 |
|------|------|
| $A_n$ | $\mathfrak{sl}_{n+1}$，秩 $n$ |
| $B_n$ | $\mathfrak{so}_{2n+1}$，奇數維正交 |
| $C_n$ | $\mathfrak{sp}_{2n}$，辛代數 |
| $D_n$ | $\mathfrak{so}_{2n}$，偶數維正交 |
| $E_6, E_7, E_8$ | 五個例外李代數中最大的三個 |
| $F_4$ | 十六維例外李代數 |
| $G_2$ | 十四維例外李代數 |

### 9.2 測試用例

| 測試 | 驗證內容 |
|------|----------|
| `test_types` | $A_n$ 和 $G_2$ 在 SimpleLieAlgebra.TYPES 中 |
| `test_from_dynkin_diagram_A1` | 從 Dynkin 圖恢復 $A_1$ |
| `test_rank_A1` | $A_1$ 的秩為 1 |
| `test_rank_A5` | $A_5$ 的秩為 5 |
| `test_rank_G2` | $G_2$ 的秩為 2 |
| `test_rank_E6` | $E_6$ 的秩為 6 |

---

## 10. 總結

本測試模組驗證了李代數分類理論的核心組件：

1. **根系結構**：提供分類的幾何基礎
2. **Dynkin 圖**：將根系轉化為離散不變量
3. **Cartan 矩陣**：根系的代數表示
4. **表示理論組件**：權、Weyl 群、Verma 模等

這些組件共同構成從抽象李代數到具體類型（如 $A_n, B_n, E_8$ 等）的完整分類流程。