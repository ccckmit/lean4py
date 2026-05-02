# test_commutative_algebra_advanced.py 測試文件說明

本文件測試 `lean4py.commutative_algebra_advanced` 模組，該模組模擬 mathlib4 的 `Mathlib.RingTheory.Commutative` 結構。

## 1. 測試涵蓋的交換代數領域

本測試文件驗證以下核心概念的實現：

| 類別 | 功能 |
|------|------|
| `Localization` | 環的局部化 |
| `PrimaryDecomposition` | 理想的準素分解 |
| `NoetherianRing` | 諾特環與希爾伯特基定理 |
| `IntegralClosure` | 整閉包 |
| `DedekindDomain` | 戴德金整環 |

---

## 2. Noetherian Ring 測試

### 測試內容

- `test_is_noetherian`: 驗證環 `Z` 滿足升鏈條件（Ascending Chain Condition, ACC）
- `test_hilbert_basis_theorem`: 驗證希爾伯特基定理

### 數學原理

**諾特環定義**：一個環 R 稱為諾特環，若 R 的每個理想上昇鏈都會穩定，即：

$$I_1 \subseteq I_2 \subseteq I_3 \subseteq \cdots \subseteq I_n \subseteq \cdots$$

存在整數 N 使得對所有 $n \geq N$ 有 $I_n = I_{n+1}$。

**希爾伯特基定理**：若 R 是諾特環，則多項式環 R[x] 也是諾特環。這保證了代數幾何中仿射空間的閉集可以由有限多個多項式定義。

```python
NoetherianRing.is_noetherian("Z")  # True - Z 是諾特環
NoetherianRing.hilbert_basis_theorem("Z")  # True - Z[x] 也是諾特環
```

---

## 3. Localization 測試

### 測試內容

- `test_compute`: 驗證局部化結構的計算
- `test_is_local_ring`: 驗證局部環的判定

### 數學原理

**局部化定義**：給定環 R 及其乘法封閉子集 S（不含零因子），局部化 $S^{-1}R$ 構造了一個新環，其中 S 中的每個元素都可逆。

對於素理想 $\mathfrak{p}$，局部化 $R_{\mathfrak{p}}$ 是個局部環，其唯一极大理想為 $\mathfrak{p}R_{\mathfrak{p}}$。

**局部環性質**：
- 只有一個极大理想
- 非可逆元構成极大理想

```python
Localization.compute("Z")  # 返回 {"ring": "S⁻¹Z", "is_local": True}
Localization.is_local_ring("Z", "pZ")  # True - Z 在素理想 pZ 處的局部化是局部環
```

---

## 4. Primary Decomposition 測試

### 測試內容

- `test_decompose`: 驗證理想的準素分解
- `test_is_primary`: 驗證準素理想的判定

### 數學原理

**準素理想**：理想 Q 稱為準素理想，若 $xy \in Q$ 蘊含 $x \in Q$ 或 $y^n \in Q$（某個冪）。

**準素分解**：每個理想 I 都可以表示為有限個準素理想的交：

$$I = \bigcap_{i=1}^n Q_i$$

其中每個 $Q_i$ 的根理想是素理想。

---

## 5. Integral Closure 測試

### 測試內容

- `test_compute`: 驗證整閉包的計算
- `test_is_integrally_closed`: 驗證整閉性

### 數學原理

**整元定義**：設 R 是域 K 的子環，元素 $\alpha \in K$ 在 R 上整，若且僅若存在首一多項式：

$$f(x) = x^n + a_{n-1}x^{n-1} + \cdots + a_0 \in R[x]$$

使得 $f(\alpha) = 0$。

**整閉包**：R 在 K 中的整閉包是所有在 K 中整的元素組成的環。

**整閉環**：若一個整環等於其分式域中的整閉包，則稱為整閉環（正規環）。

```python
IntegralClosure.compute("Z")  # 返回整閉包結構
IntegralClosure.is_integrally_closed("Z")  # True - Z 是整閉環
```

---

## 6. Dedekind Domain 測試

### 測試內容

- `test_is_dedekind`: 驗證戴德金整環的判定
- `test_unique_factorization`: 驗證理想唯一分解

### 數學原理

**戴德金整環定義**：一個整環 D 稱為戴德金整環，若滿足：
1. D 是整閉的
2. D 是諾特環
3. D 的每個非零素理想都是极大理想（維數為 1）

**理想唯一分解**：在戴德金整環中，每個非零理想都可以唯一分解為素理想的乘積（不计顺序）。這推廣了整數中質因數分解的唯一性。

```python
DedekindDomain.is_dedekind("Z")  # True - Z 是戴德金整環
DedekindDomain.unique_factorization("I")  # 返回素理想分解
```

---

## 7. 測試覆蓋矩陣

| 類別 | 方法 | 測試驗證 |
|------|------|----------|
| Localization | `compute`, `is_local_ring` | 局部化結構、局部環判定 |
| PrimaryDecomposition | `decompose`, `is_primary` | 準素分解、準素理想判定 |
| NoetherianRing | `is_noetherian`, `hilbert_basis_theorem` | ACC條件、希爾伯特基定理 |
| IntegralClosure | `compute`, `is_integrally_closed` | 整閉包計算、整閉性判定 |
| DedekindDomain | `is_dedekind`, `unique_factorization` | 戴德金條件、理想分解 |

---

## 8. 與 mathlib4 的對應關係

本模組模仿 Lean 4 mathlib4 庫中的以下結構：
- `Mathlib.RingTheory.Localization`
- `Mathlib.RingTheory.PrimaryDecomposition`
- `Mathlib.RingTheory.Noetherian`
- `Mathlib.RingTheory.IntegralClosure`
- `Mathlib.RingTheory.DedekindDomain`