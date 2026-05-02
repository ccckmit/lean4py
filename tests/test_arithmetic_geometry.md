# 算術幾何測試文檔

## 測試概述

本測試文件 (`test_arithmetic_geometry.py`) 針對 `lean4py.arithmetic_geometry` 模組進行驗證，該模組參考 mathlib4 的 `Mathlib.ArithmeticGeometry` 實現。

### 測試覆蓋範圍

| 類別 | 測試方法 | 驗證內容 |
|------|----------|----------|
| `ArithmeticScheme` | `test_creation`, `test_fiber`, `test_is_proper` | 算術 scheme 的基本結構 |
| `NeronModel` | `test_compute`, `test_is_unirational` | Néron 模型的計算與性質 |
| `ArakelovGeometry` | `test_hermitian_metric`, `test_arithmetic_degree` | Arakelov 幾何的度量性質 |
| `MordellWeil` | `test_holds`, `test_rank` | Mordell-Weil 定理的驗證 |

---

## 1. 算術幾何測試驗證內容

### 1.1 ArithmeticScheme 類測試

```python
X = ArithmeticScheme("Z")
```

**數學原理：**

- 算術cheme 是指在 `Spec(ℤ)` 上的有限型 scheme
- 這對應於代數數論中研究代數簇的基礎框架
- `base = "Z"` 表示底空間為整數的譜

**`fiber(p)` 測試驗證：**

$$X_p = X \times_{\text{Spec}(\mathbb{Z})} \text{Spec}(\mathbb{F}_p)$$

這是將算術cheme約化到有限域上，得到的纖維是有限域上的代數簇。

**`is_proper()` 測試驗證：**

proper 性是代數幾何中的重要概念，表示映射具有良好拓撲性質（如分離性、緊性推廣）。

### 1.2 Néron Model 類測試

**數學原理：**

Néron 模型是阿貝爾簇的Canonical smooth model。對於域 $K$ 上的阿貝爾簇 $A$，其 Néron 模型 $N(A)$ 是 $\mathcal{O}_K$ 上的光滑群 scheme，具有泛性質。

```python
NeronModel.compute("A")  # 返回 {"model": "...", "is_smooth": True}
```

**`is_unirational` 測試驗證：**

Néron 模型的可理性（unirational）性質是研究有理點存在性的關鍵。

### 1.3 ArakelovGeometry 類測試

**數學原理：**

Arakelov 幾何將復幾何方法推廣到算術情形。對於算術cheme上的厄米特線叢 $\overline{L}$，定義算術度：

$$\widehat{\deg}(L) = \sum_{p} \log p \cdot \text{length}(\Gamma(X, L \otimes \mathbb{F}_p)) + \frac{1}{2} \int_{X(\mathbb{C})} c_1(L) \cdot \omega$$

### 1.4 MordellWeil 類測試

**Mordell-Weil 定理：**

對於數域 $K$ 上的阿貝爾簇 $A$，其 $K$-有理點群 $A(K)$ 是有限生成的阿貝爾群。

$$\text{rank}(A/K) = \text{rank of } A(K)_{\text{torsion}}$$

---

## 2. 數域測試（Number Field Tests）

算術幾何中，數域 $K$ 是 $\mathbb{Q}$ 的有限擴張。研究對象包括：

- **代數簇在 $K$ 上的有理點**
- **局部整環的性質**
- **函子性質**

本模組中，`MordellWeil.holds("A", "Q")` 測試阿貝爾簇在 $\mathbb{Q}$ 上的有理點群是否有限生成，這正是 Mordell-Weil 定理的核心內容。

---

## 3. 理想測試（Ideal Tests）

理想論在算術幾何中扮演核心角色：

### 3.1 環與理想的基礎

- $\mathcal{O}_K$：數域 $K$ 的代數整數環
- 分式理想：$\mathcal{O}_K$ 的非零分式理想構成自由阿貝爾群

### 3.2 分解群與慣性群

對於素理想 $\mathfrak{p} \subset \mathcal{O}_K$：

$$e(\mathfrak{p}/\mathfrak{p} \cap \mathbb{Z}) = \text{分歧指數}$$
$$f(\mathfrak{p}/\mathfrak{p} \cap \mathbb{Z}) = \text{剩餘類域次數}$$

### 3.3 理想類群

$$\text{Cl}(K) = I_K / P_K$$

其中 $I_K$ 是分式理想群，$P_K$ 是主分式理想群。

**注意：** 當前測試文件未包含專門的理想測試，這屬於 `number_theory` 模組的範疇。

---

## 4. 類群測試（Class Group Tests）

### 4.1 類群的定義

類群測量了數域中理想的非主性：

$$\text{Cl}(K) \cong \text{Gal}(K^{\text{ab}})/K$$

### 4.2 類群與算術幾何的關係

- 類群為有限群（類數有限定理）
- 類數公式連接類群與黎曼ζ函數
- Hilbert 類域的刻畫

### 4.3 當前實現

本測試文件未包含類群的直接測試。類群相關功能位於 `lean4py.number_theory` 模組，包括：
- 類數計算
- 類群結構分析
- 理想類的運算

---

## 測試數學意義總結

| 測試類別 | 數學意義 |
|----------|----------|
| `ArithmeticScheme` | 算術cheme理論的基礎結構 |
| `NeronModel` | 阿貝爾簇的模型論 |
| `ArakelovGeometry` | 厄米特度量與算術度 |
| `MordellWeil` | 有理點的有限生成性 |

這些測試確保了算術幾何模組的基本功能正確性，為更高層次的數論研究提供堅實基礎。