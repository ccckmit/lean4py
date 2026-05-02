# Galois Representations 測試文檔

本文檔說明 `test_galois_representations.py` 中測試案例的數學原理。

## 1. 測試驗證內容概述

### GaloisRepresentation 類測試

| 測試方法 | 驗證內容 |
|---------|----------|
| `test_creation` | 表示的 Galois 群與維數設定正確 |
| `test_is_continuous` | 表示的連續性條件 |
| `test_character` | 跡字符 `χ(σ) = Tr(ρ(σ))` 的計算 |

---

## 2. L-adic 表示測試

### 數學背景

L-adic 表示是數論中的核心概念：

$$\rho: G_K \rightarrow GL_n(\overline{\mathbb{Q}}_l)$$

其中：
- $G_K = \text{Gal}(\overline{K}/K)$ 為數體 $K$ 的絕對 Galois 群
- $l$ 為素數
- $n$ 為表示的維數

### 測試案例

```python
def test_is_l_adic(l: int, K: str) -> bool
def test_weight(l: int) -> int
```

**權重（Weight）**：L-adic 表示的權重決定了其幾何來源。根據 Deligne 的猜想，純表示具有確定的權重 $w \in \mathbb{Z}$，影響其 L-函數的函數方程。

---

## 3. Weil-Deligne 表示測試

### 數學背景

Weil-Deligne 表示是局部域的表示形式，由三部分組成：

$$\pi = (\pi, N, \rho)$$

- $\pi$：光滑表示
- $N$：冪零算子（Nilpotent operator）
- $\rho$：Galoiste 的連續表示

這種表示適用於局部剛好叢（local systems）的分類，在 p-adic Hodge 理論中至關重要。

### 測試案例

```python
def test_creation(pi: str)
def test_is_representation(pi: str) -> bool
```

---

## 4. Fontaine 理論與 Character 測試

### Fontaine's p-adic Hodge 理論

Fontaine 理論建立了 p-adic 表示與幾何對象之間的橋樑：

| 性質 | 數學定義 |
|-----|----------|
| De Rham | 表示的 Hodge-Tate 權重集合 $\{0, 1, ..., n-1\}$ |
| Crystalline | 更強的條件，與晶體上同調相關 |

### Character 測試

跡字符（Trace character）定義為：

$$\chi_\rho(\sigma) = \text{Tr}(\rho(\sigma))$$

這是表示的關鍵不變量，決定了表示的許多重要性質。

### 測試案例

```python
def test_is_de_Rham(rho: GaloisRepresentation) -> bool
def test_is_crystalline(rho: GaloisRepresentation) -> bool
```

---

## 5. 測試架構

```
TestGaloisRepresentation       # 基礎 Galois 表示測試
├── test_creation             # 創建與屬性驗證
├── test_is_continuous         # 連續性檢查
└── test_character             # 跡字符計算

TestLAdicRepresentation        # L-adic 表示測試
├── test_is_l_adic             # L-adic 條件驗證
└── test_weight                # 權重計算

TestWeilDeligneRepresentation  # Weil-Deligne 表示測試
├── test_creation              # 創建與表示結構
└── test_is_representation     # 表示有效性

TestFontaineTheory            # Fontaine 理論測試
├── test_is_de_Rham            # De Rham 性檢驗
└── test_is_crystalline        # Crystalline 性檢驗
```

---

## 6. 數學意義

這些測試確保了 Galois 表示模組的正確性，涵蓋了：

1. **全局表示**：通過 `Gal(Q̄/Q)` 研究的整數論對象
2. **局部表示**：Weil-Deligne 表示用於局部域分析
3. **p-adic Hodge 理論**：Fontaine 理論連接了 p-adic 表示與幾何

這些結構是現代數論，特別是 Langlands 綱領的基礎構件。