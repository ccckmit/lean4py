# 高等交換代數（Commutative Algebra Advanced）

本模組實現了交換代數中的高等概念，對應 mathlib4 的 `Mathlib.RingTheory.Commutative` 模組。主要涵蓋局部化、主理想分解、諾特環等核心理論。

---

## 1. 諾特環與希爾伯特基定理（Noetherian Rings & Hilbert Basis Theorem）

### 1.1 諾特環的定義

**諾特環**是滿足**升鏈條件**（Ascending Chain Condition, ACC）的交換環。對於任意理想升鏈：

```
I₁ ⊆ I₂ ⊆ I₃ ⊆ ···
```

存在整數 $n$ 使得 $I_n = I_{n+1} = I_{n+2} = ···$，即鏈必定穩定。

### 1.2 諾特環的等價條件

設 $R$ 為環，以下條件相互等價：

1. $R$ 滿足升鏈條件（ACC）
2. $R$ 滿足**極大條件**：每一組非空理想集合必有極大元
3. $R$ 的每個理想都是**有限生成**的
4. $R$ 滿足**準素分解**：每個理想可以分解為準素理想的交

### 1.3 希爾伯特基定理

**定理**：若 $R$ 為諾特環，則多項式環 $R[x]$ 也是諾特環。

**證明思路**：
- 設 $I \subseteq R[x]$ 為任意理想
- 將係數的最高次數收集為 $R$ 中的理想 $a_0, a_1, a_2, ...$
- 由於 $R$ 諾特，每個 $a_i$ 有限生成
- 利用這些生成元構造 $I$ 的有限生成集

**推論**：$R[x_1, x_2, ..., x_n]$ 為諾特環。

---

## 2. 主理想分解（Primary Decomposition）

### 2.1 準素理想

設 $Q$ 為環 $R$ 的理想。若：

$$xy \in Q \Rightarrow x \in Q \text{ 或 } y^n \in Q \text{（對某個 } n \text{）}$$

則稱 $Q$ 為**準素理想**（Primary Ideal）。

**例子**：
- 素理想一定是準素理想
- $(p^n)$ 是準素理想，其根為 $(p)$
- $(4) \subseteq \mathbb{Z}$ 是準素理想，$\sqrt{(4)} = (2)$

### 2.2 主理想分解定理

**定理**（Lasker-Noether）：設 $R$ 為諾特環，$I \subseteq R$ 為任意理想。則 $I$ 可以寫成有限個準素理想的交：

$$I = Q_1 \cap Q_2 \cap ··· \cap Q_n$$

其中每個 $Q_i$ 的根 $p_i = \sqrt{Q_i}$ 兩兩不同。

### 2.3 極小與孤立準素分量

- **孤立分量**：對應極小素理想（不包含其他素理想）
- **嵌入分量**：對應嵌入素理想（被其他素理想包含）

孤立分量是唯一確定的，而嵌入分量在某种程度上唯一。

---

## 3. 局部化（Localization: S⁻¹R）

### 3.1 局部化的定義

設 $R$ 為交換環，$S \subseteq R$ 為**乘法子集**（即 $1 \in S$，封閉於乘法）。

定義 **局部化** $S^{-1}R$ 為：

$$S^{-1}R = \{ \frac{r}{s} \mid r \in R, s \in S \} / \sim$$

其中 $\frac{r}{s} \sim \frac{r'}{s'}$ 當且僅當存在 $t \in S$ 使得 $t(rs' - r's) = 0$。

### 3.2 局部化的泛性質

局部化 $S^{-1}R$ 滿足以下泛性質：
- 存在自然同態 $\iota: R \rightarrow S^{-1}R$，$\iota(s)$ 在 $S^{-1}R$ 中可逆
- 對任意環 $T$ 及同態 $\phi: R \rightarrow T$，若 $\phi(S)$ 中的元素都可逆，則存在唯一同態 $\psi: S^{-1}R \rightarrow T$ 使得 $\psi \circ \iota = \phi$

### 3.3 素理想的對應

存在一一對應：

$$\{\text{素理想 } \mathfrak{p} \subseteq R \mid \mathfrak{p} \cap S = \emptyset\} \longleftrightarrow \{\text{素理想 } \mathfrak{q} \subseteq S^{-1}R\}$$

給定 $\mathfrak{p}$，對應的素理想為 $S^{-1}\mathfrak{p}$。

---

## 4. 整擴張（Integral Extensions）

### 4.1 整元素的定義

設 $R \subseteq S$ 為環擴張，$s \in S$。若存在首一多項式：

$$s^n + a_{n-1}s^{n-1} + ··· + a_0 = 0 \quad (a_i \in R)$$

則稱 $s$ 為 **$R$ 上的整元素**。

### 4.2 整閉包

設 $R \subseteq S$ 為環擴張。$S$ 中所有 $R$ 的整元素構成的集合稱為 $R$ 在 $S$ 中的**整閉包**。

若 $R$ 在其分式域中的整閉包等於 $R$，則稱 $R$ 為**整閉**（Integrally Closed）。

### 4.3 整擴張的性質

- 若 $R \subseteq S$ 為整擴張，則 $\dim R = \dim S$
- 若 $R \subseteq S$ 為整擴張，$S$ 為域 $K$ 的有限生成代數，則 $S$ 為域
- **上升定理**：設 $R \subseteq S$ 為整擴張，$p_1 \subseteq p_2$ 為 $R$ 的素理想，則存在 $S$ 的素理想 $q_1 \subseteq q_2$ 使得 $q_i \cap R = p_i$

---

## 5. 賦值環（Valuation Rings）

### 5.1 賦值環的定義

設 $K$ 為域，$R \subseteq K$ 為子環。若對任意非零 $x \in K$，要么 $x \in R$ 要么 $x^{-1} \in R$（或兩者皆成立），則稱 $R$ 為 $K$ 的**賦值環**（Valuation Ring）。

### 5.2 賦值環的性質

- 賦值環是局部環
- 賦值環是整閉環
- 若 $R$ 為 $K$ 的賦值環，則 $R$ 是 **局部環**且其極大理想中的每個非零因子都在某個意義下是「小的」

### 5.3 離散賦值環

**離散賦值環**（Discrete Valuation Ring, DVR）是主理想環，其極大理想為主理想且存在元素 $\pi$（**統一元素**）使得每個非零理想都可以寫成 $(\pi^n)$。

DVR 等價於：
- 諾特局部主理想域
- 一維正則局部環
- 分式域的離散賦值定義的環

---

## 6. 戴德金域與理想分解（Dedekind Domains & Ideal Factorization）

### 6.1 戴德金域的定義

設 $R$ 為整環。若滿足以下三個條件：
1. $R$ 是**整閉**的
2. $R$ 是**諾特環**
3. $\dim R = 1$（每個非零素理想都是極大理想）

則稱 $R$ 為 **戴德金域**（Dedekind Domain）。

### 6.2 分式域的代數整閉包

**定理**：若 $R$ 為戴德金域，則其分式域 $K$ 的代數整閉包的任意局部化是戴德金域。

### 6.3 理想唯一分解

**定理**：設 $R$ 為戴德金域，$I \subseteq R$ 為非零理想。則：

$$I = \mathfrak{p}_1^{n_1} \mathfrak{p}_2^{n_2} ··· \mathfrak{p}_k^{n_k}$$

其中 $\mathfrak{p}_i$ 為（唯一的）素理想，$n_i > 0$。

這稱為**理想到素理想的唯一分解**。

### 6.4 分式理想

戴德金域的分式理想在乘法下構成一個阿貝爾群，其商群為理想類群（Ideal Class Group）。

---

## 7. 維度理論：克魯爾維度（Dimension Theory: Krull Dimension）

### 7.1 克魯爾維度的定義

設 $R$ 為環。$R$ 的**克魯爾維度**（Krull Dimension）定義為：

$$\dim R = \sup \{ n \mid \exists \text{素理想鏈 } \mathfrak{p}_0 \subsetneq \mathfrak{p}_1 \subsetneq ··· \subsetneq \mathfrak{p}_n \}$$

即最長素理想嚴格升鏈的長度。

### 7.2 維度的性質

- $\dim \mathbb{Z} = 1$
- $\dim K[x_1, ..., x_n] = n$（$K$ 為域）
- 若 $R \subseteq S$ 為整擴張，則 $\dim R = \dim S$（**維度相等定理**）
- 局部環 $(R, \mathfrak{m})$ 的維度等於 $\mathfrak{m}$ 的高度（height）

### 7.3 超越維度

對於代數簇 $X$：
- $\dim X = \dim K[X]$（仿射簇情形）
- $\dim \mathbb{A}^n = n$
- $\dim \mathbb{P}^n = n$

---

## 8. 正則局部環（Regular Local Rings）

### 8.1 正則局部環的定義

設 $(R, \mathfrak{m})$ 為 $d$ 維諾特局部環。若：

$$\dim_k (\mathfrak{m} / \mathfrak{m}^2) = d$$

其中 $k = R / \mathfrak{m}$ 為剩餘域，則稱 $R$ 為**正則局部環**（Regular Local Ring）。

### 8.2 正則性的幾何意義

- 正則局部環對應**光滑點**
- 非正則局部環對應**奇點**
- 若 $\mathfrak{m}$ 可以由 $d$ 個元素生成，則 $R$ 為正則局部環

### 8.3 正則局部環的性質

- 正則局部環是唯一分解環（UFD）
- 正則局部環是正規環（整閉）
- 若 $R$ 為正則局部環，則 $\text{projdim}_R(k) = \dim R$（剩餘域的射影維度等於維度）

---

## 9. 完備化與形式概型（Completion and Formal Spectra）

### 9.1 拓扑與完備化

設 $(R, \mathfrak{m})$ 為局部環。定義 $\mathfrak{m}$-adic 拓扑：

$$U_n = 1 + \mathfrak{m}^n$$

$R$ 的 **$\mathfrak{m}$-adic 完備化** 為：

$$\hat{R} = \varprojlim R / \mathfrak{m}^n$$

### 9.2 亨澤爾引理

設 $R$ 為完備局部環，$f: R \rightarrow \bar{R}$ 為局部同態。若 $\bar{R}$ 為有限生成 $\bar{R}$-模，則存在提升（ Hensel's Lemma ）。

### 9.3 形式概型

**形式概型**（Formal Scheme）是局部同於某個仿射形式概型的空間：

$$\text{Spf}(R) = \varinjlim \text{Spec}(R / \mathfrak{m}^n)$$

形式概型用於研究局部性質，特別是在奇點理論中。

### 9.4 形式性格部化

設 $R$ 為諾特環，$\hat{R}$ 為其 $\mathfrak{m}$-adic 完備化。則：

- 若 $R$ 為貓（貓 = equidimensional 且 unmixed），則 $\hat{R}$ 的理想與 $R$ 的理想有對應
- **MITTAG-LEFFLER 條件**在層上同調中的作用

---

## 模組結構

本模組包含以下類：

| 類別 | 功能 |
|------|------|
| `NoetherianRing` | 諾特環判斷與希爾伯特基定理 |
| `PrimaryDecomposition` | 主理想分解 |
| `Localization` | 局部化 $S^{-1}R$ 與局部環判斷 |
| `IntegralClosure` | 整閉包計算 |
| `DedekindDomain` | 戴德金域判斷與理想唯一分解 |

---

## 參考文獻

1. Atiyah, M. F., & Macdonald, I. G. (1969). *Introduction to Commutative Algebra*. Addison-Wesley.
2. Matsumura, H. (1989). *Commutative Ring Theory*. Cambridge University Press.
3. Eisenbud, D. (1995). *Commutative Algebra with a View Toward Algebraic Geometry*. Springer-Verlag.
4. Zariski, O., & Samuel, P. (1958). *Commutative Algebra, Vol. I & II*. Van Nostrand.