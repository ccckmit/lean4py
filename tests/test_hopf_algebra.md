# Hopf 代數測試文檔

本文檔說明 `test_hopf_algebra.py` 中測試案例所驗證的數學原理。

---

## 1. 測試驗證的內容概述

Hopf 代數是同時具有代數結構和餘代數結構的雙代數對象。本測試文件驗證以下核心內容：

- **餘代數結構**：餘乘法、餘單位
- **代數結構**：乘法、單位
- **雙代數兼容性**：代數與餘代數結構的和諧性
- **反極子（Antipode）**：Hopf 代數的特徵映射
- **量子群**：q-變形 Lie 代數
- **模與表示**：Hopf 模代數、表示論

---

## 2. 餘代數（Coalgebgra）測試

### TestCoalgebra

餘代數是具有餘乘法（comultiplication）和餘單位（counit）的代數結構。

```python
c = Coalgebra({"a", "b"}, lambda x: (x, x), lambda x: 1)
```

### 測試項目

| 測試 | 驗證內容 |
|------|----------|
| `test_creation` | 餘代數的承載集合（carrier set）正確創建 |
| `test_is_coassociative` | **餘結合性**：$(\Delta \otimes \text{id}) \circ \Delta = (\text{id} \otimes \Delta) \circ \Delta$ |
| `test_is_cocommutative` | **餘交換性**：$\Delta = \tau \circ \Delta$（其中 $\tau$ 為張量交換） |
| `test_sweedler_notation` | **Sweedler 記號**：餘乘法結果以 $\Delta(x) = x_{(1)} \otimes x_{(2)}$ 表示 |

### 數學原理

**餘結合性**確保了餘乘法的三種複合方式一致：
$$(\Delta \otimes \text{id})\Delta(x) = (\text{id} \otimes \Delta)\Delta(x)$$

**Sweedler 記號**是處理餘代數的标准符號：
$$\Delta(x) = \sum x_{(1)} \otimes x_{(2)}$$

---

## 3. 雙代數（Bialgebra）測試

### TestBialgebra

雙代數是同時具備代數結構和餘代數結構的對象，兩者必須兼容。

```python
b = Bialgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1)
```

### 兼容性條件

雙代數需滿足以下兼容性公理：

1. **餘乘法保持乘法**：
   $$\Delta(xy) = \Delta(x)\Delta(y)$$

2. **餘單位保持單位**：
   $$\Delta(1) = 1 \otimes 1$$

3. **乘法保持餘乘法**：
   $$m \circ (S \otimes S) = S \circ m$$

### 測試項目

| 測試 | 驗證內容 |
|------|----------|
| `test_creation` | 雙代數結構正確創建 |
| `test_is_bialgebra` | 所有雙代數公理滿足 |
| `test_is_commutative` | 代數乘法可交換：$xy = yx$ |
| `test_is_cocommutative` | 餘乘法可交換 |

---

## 4. 反極子（Antipode）測試

### TestHopfAlgebra

Hopf 代數是具有反極子映射 $S$ 的雙代數。

```python
h = HopfAlgebra(
    {"a"}, lambda x: x, "1",
    lambda x: (x, x), lambda x: 1, lambda x: x  # 最後參數為反極子
)
```

### 核心反極子性質

反極子 $S: H \to H$ 滿足：
$$m \circ (S \otimes \text{id}) \circ \Delta = \eta \circ \epsilon$$
$$m \circ (\text{id} \otimes S) \circ \Delta = \eta \circ \epsilon$$

即：
$$S(x_{(1)})x_{(2)} = \epsilon(x)1 = x_{(1)}S(x_{(2)})$$

### 測試項目

| 測試 | 驗證內容 |
|------|----------|
| `test_creation` | Hopf 代數正確創建 |
| `test_is_hopf` | 反極子存在且滿足 Hopf 代數定義 |
| `test_antipode_property` | 驗證 $S(x_{(1)})x_{(2)} = \epsilon(x)$ |

### GroupAlgebra 範例

群代數 $k[G]$ 是典型的交換 Hopf 代數：

```python
ga = GroupAlgebra("G")
ga.comultiplication("g")  # 返回 ("g", "g")
ga.counit("g")           # 返回 1
ga.antipode("g")         # 返回 "g"（群元素逆元）
```

---

## 5. 量子群（Quantum Group）測試

### TestQuantumGroup

量子群是經典 Lie 代數的 q-變形（quantized deformation）。

```python
qg = QuantumGroup("A_1", 0.5)
```

### 數學原理

量子群 $U_q(\mathfrak{g})$ 的定義：

- 參數 $q$ 為變形參數
- 當 $q \to 1$ 時，量子群收斂到經典 enveloping algebra
- 量子群是非交換、非餘交換的 Hopf 代數

### 測試項目

| 測試 | 驗證內容 |
|------|----------|
| `test_creation` | 根系類型（A_1, B_2, G_2 等）和 q 值正確設置 |
| `test_is_quantized` | 當 $q \neq 1$ 時為量子化 |
| `test_special_case` | 返回特殊情形標記 |
| `test_R_matrix` | R-矩陣：用於辫化（braiding）和量子Yang-Baxter方程 |
| `test_quantum_BPBW_basis` | 量子 PBW 基：一種優先序基 |

### R-矩陣與辫化

R-矩陣 $R$ 滿足**量子 Yang-Baxter方程**：
$$R_{12}R_{13}R_{23} = R_{23}R_{13}R_{12}$$

這保證了辫化范畴的結合性約束。

---

## 6. sl₂ 量子化測試

### TestSl2Hopf 與 TestSl2Quantized

$\mathfrak{sl}_2$ 的量子化是量子群的核心範例。

```python
h = sl2_hopf()           # 經典 sl2 Hopf 代數
h = sl2_quantized(0.5)   # q=0.5 的量子化版本
```

### 生成元關係

$U_q(\mathfrak{sl}_2)$ 的生成元 $e, f, k$ 滿足：
$$ke = q^2ek,\quad kf = q^{-2}fk,\quad ef - fe = \frac{k - k^{-1}}{q - q^{-1}}$$

---

## 7. Hopf 模代數與不變理論

### TestModuleAlgebra

模代數是同時具有左 $H$-模結構和代數結構的對象。

```python
ma = ModuleAlgebra("A", "H", lambda x: x)
```

需滿足：
$$h \cdot (ab) = (h_{(1)} \cdot a)(h_{(2)} \cdot b)$$

### TestInvariantTheory

不變子環：
$$A^G = \{a \in A \mid g \cdot a = a, \forall g \in G\}$$

---

## 8. Hopf 代數表示論

### TestRepresentationOfHopfAlgebra

表示是Hopf代數作用於向量空間。

```python
h = HopfAlgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1, lambda x: x)
rh = RepresentationOfHopfAlgebra(h, "V", lambda x: x)
```

| 測試 | 驗證內容 |
|------|----------|
| `test_is_representation` | 表示公理滿足 |
| `test_is_simple` | 表示是否單模（無非平凡子表示） |
| `test_is_completely_reducible` | 是否完全可約（任意表示可分解為單表示之和） |

---

## 9. 對偶 Hopf 代數

### TestDualHopfAlgebra

若 $H$ 為有限維 Hopf 代數，則其對偶空間 $H^*$ 仍是 Hopf 代數。

```python
h = HopfAlgebra({"a"}, lambda x: x, "1", lambda x: (x, x), lambda x: 1, lambda x: x)
dh = DualHopfAlgebra(h)
```

---

## 10. 辫化范畴

### TestBraidedCategory

辫化范畴中的對象可通過 R-矩陣辫化。

```python
bc = braided_category()
bc.add_object(h)
br = bc.braiding(h, h)  # 返回辫化映射
```

辫化需滿足 Hexagon 公理。

---

## 測試覆蓋矩陣

| 類別 | 創建 | 結構驗證 | 性質檢查 | 特殊操作 |
|------|------|----------|----------|----------|
| Coalgebra | ✅ | coassociative, cocommutative | Sweedler | - |
| Bialgebra | ✅ | is_bialgebra | commutative, cocommutative | - |
| HopfAlgebra | ✅ | is_hopf | antipode_property | - |
| GroupAlgebra | ✅ | is_hopf | comultiplication, counit, antipode | - |
| QuantumGroup | ✅ | is_quantized | - | R_matrix, PBW basis |
| ModuleAlgebra | ✅ | is_module_algebra | - | invariants |
| InvariantTheory | ✅ | - | invariants, Hilbert series | primary/secondary invariants |
| Representation | ✅ | is_representation | simple, completely_reducible | - |
| sl2/sl2_q | ✅ | is_hopf | - | - |
| DualHopfAlgebra | ✅ | is_hopf | dual_multiplication | - |
| BraidedCategory | ✅ | - | - | braiding |

---

## 數學背景資料

### 交換圖：Hopf 代數基本性質

```
Δ ━━━━━━━━━━━━━━━━━━━━━━━━▶ H ⊗ H
▲                         ▲
│                         │
│ (m⊗id)○(S⊗id⊗id)○(Δ⊗id)   │ id⊗Δ
│                         │
│ (id⊗m)○(id⊗S⊗id)○(id⊗Δ)   │
│                         │
▼                         │
H ⊗ H ◀━━━━━━━━━━━━━━━━━━━ H ⊗ H
              Δ
```

### 核心定理

1. **反極子唯一性**：Hopf 代數的反極子若存在則唯一
2. ** convolution 代數**：$Hom(H, H)$ 在 convolution 下構成代數
3. **Maschke 定理**：特徵標籤域上有限維半單 Hopf 代數是完全可約的

---

*文檔版本：v1.18*
*相關模組：`lean4py.hopf_algebra`*