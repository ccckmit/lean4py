# Adeles 模組文檔

## 概述

本模組 imitates mathlib4 的 `Mathlib.NumberTheory.Adele`，實現了adelic 結構的核心類別，包括：

- `AdeleRing`: 整體域 K 的 adelering A_K
- `FiniteAdeles`: 有限位置 adeles A_K^f
- `InfiniteAdeles`: 無限位置 adeles A_K^∞
- `RestrictedProduct`: 限制積結構

---

## 1. Adeles：局部域的受限積與受限積拓撲

### 1.1 局部域的回顧

對於整體域 K（如有理數域 Q 或代數數域），每個素除子（素點）v 對應一個局部域 K_v：
- **非Archimedes局部域**：對於有限生成的素除子，K_v 是 p-進域（如 Q_p）
- **Archimedes局部域**：對於實數嵌入或複數嵌入，K_v ≅ ℝ 或 ℂ

每個局部域 K_v 都是局部緊緻的拓撲空間，配备自然的白手拓撲。

### 1.2 受限積的定義

對於一組局部域 {K_i}，其受限積（restricted product）定義為：

$$\prod'_i K_i = \left\{ (x_i) \in \prod_i K_i \mid x_i \in \mathcal{O}_i \text{ 對幾乎所有有限位置成立} \right\}$$

其中 $\mathcal{O}_i$ 是 K_i 的整環（valutation ring）。

### 1.3 受限積拓撲

受限積配备**受限積拓撲**（restricted product topology）：

- 基開集由形如 $\prod_i U_i$ 的集合組成，其中每個 U_i 是 K_i 中的開集
- 對於幾乎所有有限位置，U_i = \mathcal{O}_i
- 這個拓撲使受限積成為局部緊緻的拓撲環

---

## 2. 整體域 K 的 adelering A_K

### 2.1 定義

對於整體域 K，其 **adelering** A_K 是有限位置 adeles 和無限位置 adeles 的直積：

$$\mathbb{A}_K = \mathbb{A}_K^f \times \mathbb{A}_K^\infty$$

其中：
- $\mathbb{A}_K^f = \prod'_{v \nmid \infty} K_v$：有限位置 adeles（受限制積）
- $\mathbb{A}_K^\infty = \prod_{v \mid \infty} K_v$：無限位置 adeles（普通積）

對於 Q：
- $\mathbb{A}_\mathbb{Q} = \mathbb{A}_\mathbb{Q}^f \times \mathbb{R}$
- $\mathbb{A}_\mathbb{Q}^f = \prod'_p \mathbb{Q}_p$

### 2.2 AdeleRing 類別

```python
class AdeleRing:
    """Adele ring A_K of number field K."""

    def __init__(self, field: str = "Q"):
        self.field = field
        self.finite_adeles: List[Any] = []
        self.infinite_adeles: List[Any] = []
```

### 2.3 拓撲性質

- **局部緊緻**：A_K 是局部緊緻的拓撲環
- **非離散**：A_K 不是離散空間
- **對角嵌入**：K 可以自然地對角嵌入到 A_K 中：
  $$\Delta: K \hookrightarrow \mathbb{A}_K, \quad x \mapsto (x, x, x, \ldots)$$

### 2.4 整環結構

有限 adeles $\mathbb{A}_K^f$ 是交換環，配備受限積拓撲。整體 adeles A_K 也是交換環。

---

## 3. Ideles：Adeles 的可逆元

### 3.1 定義

**Ideles** 是 adeles 的可逆元群，記為 $\mathbb{A}_K^\times$：

$$\mathbb{A}_K^\times = \{ (x_v) \in \prod_v K_v^\times \mid x_v \in \mathcal{O}_v^\times \text{ 對幾乎所有有限位置成立} \}$$

### 3.2 Idele 範數

Ideles 装备**範數映射**：

$$|\cdot|_{\mathbb{A}}: \mathbb{A}_K^\times \to \mathbb{R}_{>0}$$

對於 idele x = (x_v)，其adelic 範數定義為：

$$|x|_{\mathbb{A}} = \prod_v |x_v|_v$$

其中 |·|_v 是局部域 K_v 的標準化絕對值。

### 3.3 與Adeles環的關係

Ideles 可以視為 adeles 環的單位群，但装備不同的拓撲：
- Ideles 的拓撲是 A_K^\times 作為拓撲群的子空間拓撲的精細化
- 這個精細化拓撲使 ideles 成為局部緊緻的拓撲群

---

## 4. 類群關係：C_K = K^\times \ A_K^\times / K^\times

### 4.1 理想類群的 adelic 描述

整體域 K 的 **理想類群**（ideal class group）可以完全用 adelic 語言描述：

$$\text{Cl}_K = K^\times \backslash \mathbb{A}_K^\times / \mathbb{A}_K^\infty$$

更精確地：

$$C_K = \mathbb{A}_K^\times / (K^\times \cdot \mathbb{A}_K^\infty)$$

其中 $\mathbb{A}_K^\infty = \prod_{v|\infty} K_v^\times$ 是無限位置的 ideles。

### 4.2 類群關係的拓撲意義

這個分解反映：
- **K^\times**：全域主 ideles（來自 K 的元素）
- **A_K^\times / K^\times**：Adelic 類群
- **A_K^∞**：逼近定理保證某些結構

### 4.3 有限性

對於代數數域 K，類群 Cl_K 是有限群。Adelic 描述可用於：
- 類群計算演算法
- Chebotarev 密度定理的證明
- 類域論的表述

### 4.4 說明

類群關係 $C_K = K^* \backslash \mathbb{A}_K^* / \mathbb{A}_K^*$ 是計算類群的基礎。這個關係式表達了全域域的類群可以透過其adelic 可逆元群在主理想和有限分支上的商來描述，反映了局部與全域性質的深刻統一。

---

## 5. Tamagawa 數

### 5.1 定義

對於連通簡約代數群 G over 全域域 K，**Tamagawa 數** τ(G) 定義為：

$$\tau(G) = \text{Vol}(G(\mathbb{A}_K) / G(K))$$

其中體積是透過 Haar 測度正規化使得 self-dual 測度滿足特定條件。

### 5.2 Tamagawa 數的意義

- **有限性**：對於大多數代數群，G(K)\G(A_K) 是緊緻的或有有限不變測度
- **Weil猜想**：對於simply connected代數群，Tamagawa 數猜想為 1
- **應用**：與局部不變量、整數點分布密切相關

### 5.3 重要結果

- **Tamagawa 數猜想**（已被證明）：對於 simply connected 簡約群，G 的 Tamagawa 數等於 1
- 這個結果在數論中具有基礎性的意義

---

## 6. Adele 積分

### 6.1 局部與全域的關係

Adele 積分的核心思想是：**全域積分等於局部積分的積**

對於适当函數 f: A_K → ℂ：

$$\int_{\mathbb{A}_K} f(x) \, dx = \prod_v \int_{K_v} f_v(x_v) \, dx_v$$

其中：
- dx 是 A_K 上的 Haar 測度
- dx_v 是每個局部域 K_v 上的局部 Haar 測度
- 測度需要適當正規化

### 6.2 Fourier 變換

在 adeles 上定義 Fourier 變換：

$$\hat{f}(\xi) = \int_{\mathbb{A}_K} f(x) \psi(x \xi) \, dx$$

其中 ψ 是 A_K 的標準加法特徵（standard additive character）。

### 6.3 積分的收斂性

- **局部積分**：每個局部積分需要在相應局部域中收斂
- **全域積分**：全域積分的收斂性由 product formula 保證
- **正規化**：測度的選擇影響積分的具體數值

---

## 7. Tate's Thesis 與 Adeles 上的 Fourier 分析

### 7.1 Tate's Thesis 概述

John Tate 的博士論文（1950）建立了 adeles 上 Fourier 分析的理論框架，是數論中最優美的統一理論之一。

### 7.2 核心內容

#### 7.2.1 局部與全域 Fourier 變換

Tate 構造瞭如何從局部 Fourier 變換推到全域：
- 對於每個局部域 K_v，定義局部 Fourier 變換
- 利用 product formula 組合局部結果得到全域定理

#### 7.2.2 Riemann-Roch 定理

在 adeles 上，Tate 證明了 Riemann-Roch 型定理：
$$\sum_{x \in K} f(x) = \sum_{x \in K} \hat{f}(x)$$

#### 7.2.3 Θ 函數與 L-函數

Tate 的方法可用於：
- Θ 函數的函數方程
- Dirichlet L-函數的推廣（Artin L-函數、Hecke L-函數）
- L-函數的函數方程

### 7.3 函數方程

對於 cusp form 或 parabolical form f，關於L-函數的函數方程可表述為：
$$\Lambda(s, f) = \varepsilon(s, f) \Lambda(1-s, \tilde{f})$$

其中 Λ 是正規化的 L-函數，ε 是 ε-因子，兩者都可以用 adelic 方法自然地定義。

### 7.4 局部密度

Tate 的方法涉及：
- **局部 Riemann-Roch 定理**
- **局部 density 計算**
- **全局逼近**

---

## 8. Global Langlands 群

### 8.1 Langlands 對偶群

對於代數群 G，其 Langlands 對偶群 ^L G 定義為：
$${}^L G = \hat{G} \rtimes \text{Gal}(K/k)$$

其中 Gal(K/k) 是適當的 Galois 群。

### 8.2 全域 Langlands 群

**全域 Langlands 群**是一個假設的拓撲群，它應該滿足：
- 包含 K 的絕對 Galois 群 Gal(K/K)
- 為每個局部域 K_v 對應一個局部Langlands群
- 作為 Galois 群和 Langlands 對偶群的推廣

### 8.3 Langlands 對應

全域 Langlands 對應預測：
- n 維 Galois 表示 ↔ n 維 automorphic 表示
- 這個對應應該通過全域 Langlands 群作為媒介

### 8.4 與 Adeles 的關係

Adeles 在 Langlands 對應中起關鍵作用：
- **Automorphic forms** 定义在 adeles 群上
- **Automorophic 表示** 是 adeles 群的表示
- **局部 Langlands 對應** 在每個局部域上成立
- **全域性** 需要通過 adeles 协调局部結果

### 8.5 Taniyama-Shimura 猜想

作爲 Langlands 對應的特殊情况，Wiles 等人關於 Taniyama-Shimura 猜想的證明使用了：
- Modular forms 的 adelic 表述
- Elliptic curves 的 Galois 表示
- 局部與全域相容性

---

## 模組結構

| 類別 | 描述 |
|------|------|
| `AdeleRing` | 整體域 K 的 Adelering A_K |
| `FiniteAdeles` | 有限位置 adeles A_K^f = Π'_v∤∞ K_v |
| `InfiniteAdeles` | 無限位置 adeles A_K^∞ = Π_{v\|∞} K_v |
| `RestrictedProduct` | 限制積 Π'_i M_i 的實現 |

---

## 數學背景

Adeles 和 Ideles 的理論是現代數論的基礎工具，連接了：
- 局部域理論與全域域理論
- 代數數論與調和分析
- 類域論與Langlands program

本模組參考了 mathlib4 的 `Mathlib.NumberTheory.Adele` 實現，為 lean4py 提供了基礎的 adelic 結構支持。