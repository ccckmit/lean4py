# Arithmetic Geometry Module Documentation

## 概述

本模組實現了算術幾何的基本概念，對應 mathlib4 中的 `Mathlib.ArithmeticGeometry`。算術幾何是研究代數簇的算術性質與數論之間聯繫的數學分支，核心研究對象包括算術格式（Arithmetic Schemes）、Néron 模型（Néron Models）、阿羅開洛夫幾何（Arakelov Geometry）以及莫德爾-韋伊定理（Mordell-Weil Theorem）。

---

## 1. Number Fields and Rings of Integers（數域與整環）

### 1.1 數域的定義

**數域**（Number Field）是有理數域 $\mathbb{Q}$ 的有限擴張。若 $[K : \mathbb{Q}] = n$，則稱 $K$ 為一個 $n$ 次數域。數域是代數數論研究的核心對象，因為它們提供了有理數域的自然推廣，同時保留了許多良好的性質。

任何數域 $K$ 都可以寫成 $K = \mathbb{Q}(\alpha)$ 的形式，其中 $\alpha$ 是某個代數整數，生成元 $\alpha$ 的最小多項式為首一整係數不可約多項式。這個多項式的係數決定了數域的結構，而判別式（Discriminant）則刻畫了 $K$ 中整數環 $\mathcal{O}_K$ 的幾何性質。

數域的嵌入（Embeddings）是將 $K$ 嵌入到 $\mathbb{C}$ 的域同態。由於 $[K : \mathbb{Q}] = n$，恰好存在 $n$ 個不同的嵌入，其中 $r_1$ 個是實嵌入，$r_2$ 個是共軛複嵌入，滿足 $r_1 + 2r_2 = n$。這些嵌入在研究單位群（Unit Group）和類數公式（Class Number Formula）時起關鍵作用。

### 1.2 整環與代數整數

**代數整數環**（Ring of Integers）$\mathcal{O}_K$ 是數域 $K$ 中所有代數整數的集合。具體來說，如果 $K$ 是數域，則

$$\mathcal{O}_K = \{ \alpha \in K \mid \alpha \text{ 是某個首一整係數多項式的根} \}$$

當 $K = \mathbb{Q}$ 時，$\mathcal{O}_K = \mathbb{Z}$。對於虛二次域 $K = \mathbb{Q}(\sqrt{d})$（其中 $d$ 是無平方因子整數），整環具有已知的結構：當 $d \equiv 1 \pmod{4}$ 時，$\mathcal{O}_K = \mathbb{Z}[\frac{1 + \sqrt{d}}{2}]$；否則 $\mathcal{O}_K = \mathbb{Z}[\sqrt{d}]$。

整環 $\mathcal{O}_K$ 在加法下構成阿貝爾群，其結構由數域的**判別式**和**基架」（Basis）決定。一組整基（Integral Basis）是 $\mathcal{O}_K$ 作為 $\mathbb{Z}$-模的生成元集合，通常表示為 $\{ \omega_1, \omega_2, \ldots, \omega_n \}$，使得每個代數整數可以唯一表示為這些基底的整係數線性組合。

---

## 2. Algebraic Number Theory Fundamentals（代數數論基礎）

### 2.1 代數數論的核心問題

代數數論將數論問題置于更廣闊的代數結構中研究。經典數論研究 $\mathbb{Z}$ 中的質因數分解，而代數數論則研究數域整環 $\mathcal{O}_K$ 中的理想分解。這個推廣源於對費馬大定理的研究——人們發現在某些數域中，$\mathbb{Z}$ 的類似結構會喪失唯一分解性質，這是推动理想理論發展的根本原因。

在代數數論中，我們將「質數」的概念推廣為**素理想**（Prime Ideal）。在 $\mathbb{Z}$ 中，每個非零素理想都是由某個質數 $p$ 生成的主理想 $(p)$。在一般的 Dedekind 環中，每個非零素理想都是最大理想，且每個非零理想都可以唯一分解為素理想的乘積。

### 2.2 理想的基本性質

**理想**（Ideal）是環論中的核心概念。對於環 $R$，其子集 $\mathfrak{a}$ 若滿足對加法封閉且對乘法封閉（即對所有 $r \in R$ 和 $a \in \mathfrak{a}$ 有 $ra \in \mathfrak{a}$），則稱 $\mathfrak{a}$ 為 $R$ 的理想。

在數域的整環中，每個非零理想都可以唯一分解為素理想的乘積（將在第三節詳細討論）。這個性質使得我們能夠將數論問題轉化為代數問題。例如，研究質數在數域中的分解問題就轉化為研究主理想 $(p)$ 如何分解為素理想的乘積。

理想在加法下構成一個阿貝爾群。對於有限生成理想 $\mathfrak{a} = (a_1, a_2, \ldots, a_n)$，其范數定义为 $N(\mathfrak{a}) = |R/\mathfrak{a}|$，即商環的元素個數。當 $\mathfrak{a}$ 為主理想 $(\alpha)$ 時，有 $N((\alpha)) = |N_{K/\mathbb{Q}}(\alpha)|$，其中 $N_{K/\mathbb{Q}}$ 表示域擴張的 norm 映射。

---

## 3. Dedekind Domains and Unique Factorization of Ideals（戴德金域與理想的唯一分解）

### 3.1 Dedekind 域的定義與性質

**Dedekind 域**（Dedekind Domain）是一類滿足以下三個條件的整態（Integral Domain）$R$：

1. $R$ 是 Noether 環（即每個理想都是有限生成的）；
2. $R$ 是整閉的（即若 $K$ 為 $R$ 的分式域，則 $R$ 在 $K$ 中是整閉的）；
3. 每個非零素理想都是最大理想（即 $R$ 是一維的）。

數域的整環 $\mathcal{O}_K$ 是 Dedekind 域的典型例子。這個事實的證明依賴於以下幾個關鍵觀察：$\mathcal{O}_K$ 是有限生成 $\mathbb{Z}$-模，因此是 Noether 環；$\mathcal{O}_K$ 是整閉的（這需要驗證）；最後，$\mathcal{O}_K$ 是一維的，因為每個非零素理想都對應於某個非零素數理想的擴張或限制。

Dedekind 域的關鍵特性是其每個非零真理想都可以唯一（順序不計）分解為素理想的乘積。這是唯一分解環（UFD）在更一般設置下的推廣。即使某些 Dedekind 域（如 $\mathbb{Z}[\sqrt{-5}]$）不是 UFD，其理想仍具有唯一分解性質。

### 3.2 理想分解的結構

設 $R$ 為 Dedekind 域，$\mathfrak{a}$ 為非零理想。根據 Dedekind 域的性質，$\mathfrak{a}$ 可以唯一寫成

$$\mathfrak{a} = \prod_{\mathfrak{p}} \mathfrak{p}^{e_{\mathfrak{p}}}$$

其中 $\mathfrak{p}$ 遍歷非零素理想，$e_{\mathfrak{p}} \geq 0$ 為整數，且只有有限多個 $\mathfrak{p}$ 使得 $e_{\mathfrak{p}} \neq 0$。指數 $e_{\mathfrak{p}}$ 稱為 $\mathfrak{p}$ 在 $\mathfrak{a}$ 中的**重數**（Multiplicity）。

若 $\mathfrak{a} \subseteq \mathfrak{b}$ 為兩個非零理想，則存在唯一的理想 $\mathfrak{c}$ 使得 $\mathfrak{a} = \mathfrak{b}\mathfrak{c}$，這時我們寫 $\mathfrak{b} \mid \mathfrak{a}$ 並稱 $\mathfrak{b}$ 整除 $\mathfrak{a}$。這個整除關係與素理想分解緊密相關：素理想 $\mathfrak{p}$ 整除 $\mathfrak{a}$ 當且僅當 $\mathfrak{p}$ 出現在 $\mathfrak{a}$ 的素理想分解中。

對於分式理想（Fractional Ideal），即非零環 $R$ 的分式域中的 $R$-子模，我們同樣有唯一分解性質。實際上，Dedekind 域的全部分式理想構成一個阿貝爾群，稱為**理想類群**（Ideal Class Group），這將在第四節詳細討論。

### 3.3 局部化與完備化

在研究 Dedekind 域時，局部化（Localization）是重要的技術工具。對於素理想 $\mathfrak{p}$，局部化 $R_{\mathfrak{p}}$ 是一個 DVR（Discrete Valuation Ring），其唯一最大理想由某個元素生成。這個局部化過程使我們能夠逐個研究每個素理想附近的性質。

對於 $p$-進數域 $\mathbb{Q}_p$ 的整環 $\mathbb{Z}_p$，其局部化與 $\mathbb{Z}_p$ 本身的結構密切相關。在數論中，局部化與全域（Global）性質的關係由 Hasse-Minkowski 原理描述——某些性質在全域成立的充要條件是其局部化對所有素理想（包含無窮素位）都成立。

---

## 4. Class Group and Picard Group（類群與皮卡群）

### 4.1 類群的定義

**類群**（Class Group）是刻畫 Dedekind 域偏離主理想域（PID）的程度的代數不變量。對於 Dedekind 域 $R$，考慮其所有非零分式理想构成的阿貝爾群 $I(R)$（稱為理想群），以及主分式理想构成的子群 $P(R)$。則商群

$$Cl(R) = I(R) / P(R)$$

稱為 $R$ 的**類群**。類群是有限阿貝爾群，其階稱為**類數**（Class Number）。

當 $Cl(R)$ 為平凡群（即類數為 1）時，每個非零分式理想都是主理想，這意味著 $R$ 是 PID。在這種情況下，理想理論與古典因子理論完全一致。然而，對於一般的數域整環，類數通常大於 1，表明唯一分解性質不成立。

類群的計算是代數數論中的重要問題。對於虛二次域 $K = \mathbb{Q}(\sqrt{d})$，類數公式給出了類數的精確表達式，涉及判別式、單位根數、歐拉積分以及黎曼 ξ 函數的值。這個公式是研究類數問題的基礎工具。

### 4.2 Picard 群

**Picard 群** $\text{Pic}(X)$ 是代數幾何中研究直叢（Line Bundle）的同構類构成的群。對於一維諾特整態 $R$（即代數曲線的函數域的整環），Picard 群與類群自然同構。這個對應關係是代數數論與代數幾何之間深刻聯繫的體現。

具體來說，若 $X$ 為一條代數曲線，$k(X)$ 為其函數域，則 $X$ 的 Picard 群恰好與 $k(X)$ 的整環 $\mathcal{O}_k(X)$ 的類群同構。在這個意義上，類群可以視為曲線的 Picard 群，體現了算術幾何的統一觀點。

對於更高維的算術格式（如 $\text{Spec}(\mathbb{Z})$ 上的格式），Picard 群的定義更为复杂，涉及除子的類似的概念。這時我們考慮 Cartier 除子或等價地考慮可逆層（Invertible Sheaves）的同構類，其群結構給出了 Picard 群的定義。

### 4.3 類群的計算與性質

類群的計算方法包括代數方法（如使用格蘭-舒恩曼算法）和解析方法（如使用類數公式）。對於虛二次域，已知類數公式為

$$h(d) = \frac{w_K \sqrt{|d|}}{2\pi} L(1, \chi_d)$$

其中 $w_K$ 為單位根個數，$d$ 為判別式，$\chi_d$ 為相應的狄利克雷特徵，$L(s, \chi_d)$ 為 Dirichlet $L$-函數。這個公式連接了類數與 $L$-函數的解析性質，是解析數論與代數數論交叉的核心結果。

類群還與**廣義類數公式**（Stark-Barthelmasz 公式）密切相關，這個公式在算術幾何的各種上下文中都有應用。

---

## 5. Unit Group and Dirichlet's Unit Theorem（單位群與狄利克萊單位定理）

### 5.1 單位群的結構

在數域 $K$ 的整環 $\mathcal{O}_K$ 中，**單位**（Unit）是指在乘法下有逆元的非零元素。全體單位构成的群記為 $\mathcal{O}_K^{\times}$，稱為**單位群**（Unit Group）。

在有理數域 $\mathbb{Q}$ 中，單位群為 $\{\pm 1\}$，僅包含兩個元素。然而，對於一般的數域，單位群的結構要豐富得多。單位群與數域的嵌入結構密切相關，因為每個嵌入 $\sigma_i : K \to \mathbb{C}$ 都會將單位映射到複數的乘法群中。

對於實嵌入 $\sigma_i$ 和共軛複嵌入 $\sigma_{r_1+i} = \overline{\sigma_i}$（$i = 1, \ldots, r_2$），考慮對數映射

$$\ell: \mathcal{O}_K^{\times} \to \mathbb{R}^{r_1 + r_2}, \quad \ell(u) = (\log|\sigma_1(u)|, \ldots, \log|\sigma_{r_1+r_2}(u)|)$$

這個映射的像是 $\mathbb{R}^{r_1 + r_2}$ 中的一個格（lattice），其維數為 $r_1 + r_2 - 1$。

### 5.2 Dirichlet's Unit Theorem

**Dirichlet 單位定理**（Dirichlet's Unit Theorem）是代數數論中最優美的結果之一，定理斷言：

> 設 $K$ 為數域，$r_1$ 為實嵌入個數，$r_2$ 為共軛複嵌入對數，則單位群 $\mathcal{O}_K^{\times}$ 是有限群 $\mu_K$（Roots of Unity）與自由阿貝爾群 $\mathbb{Z}^{r_1 + r_2 - 1}$ 的直積：
> $$\mathcal{O}_K^{\times} \cong \mu_K \times \mathbb{Z}^{r_1 + r_2 - 1}$$

定理中的 $\mu_K$ 是 $K$ 中所有單位根构成的有限循環群，其階為 $w_K = |\mu_K|$。對於虛二次域，$r_1 = 0$，$r_2 = 1$，因此單位群結構為 $\mathcal{O}_K^{\times} \cong \mu_K \times \mathbb{Z}$，即存在一個基本單位 $\varepsilon$ 使得每個單位可以唯一寫成 $\pm \varepsilon^n$ 的形式。

定理中的 $r_1 + r_2 - 1$ 稱為單位群的**秩**（Rank）。當 $K = \mathbb{Q}$ 時，$r_1 = 1$，$r_2 = 0$，故秩為 $0$，這與 $\mathbb{Q}$ 的單位群為有限群的事實一致。當 $K$ 為實二次域時，$r_1 = 2$，$r_2 = 0$，故秩為 $1$，單位群形如 $\{\pm \varepsilon^n \mid n \in \mathbb{Z}\}$。

### 5.3 Regulator 與類數公式

**Regulator** 是與單位群相關的重要不變量，定義為對數映射的像构成的格的體積。具體來說，若 $\{ \varepsilon_1, \ldots, \varepsilon_{r_1+r_2-1} \}$ 為單位群的一組基，則 Regulator 為

$$R_K = \left| \det(\log|\sigma_i(u_j)|)_{1 \leq i \leq r_1+r_2-1, 1 \leq j \leq r_1+r_2-1} \right|$$

Regulator 出現在類數公式中。對於代數數域 $K$，完整的類數公式為

$$h_K \cdot R_K = \frac{(2\pi)^{r_2} \cdot w_K \cdot \sqrt{|d_K|}}{n \cdot \Gamma(r_1/2) \cdot \Gamma(r_2/2)} \cdot \prod_{\chi} L(1, \chi)$$

其中 $d_K$ 為判別式，$\Gamma$ 為伽瑪函數，積分遍歷所有非平凡特征 $\chi$。這個公式連接了類數、Regulator、判別式與 $L$-函數，是數論中最深刻的结果之一。

---

## 6. Decomposition of Primes in Extensions（素數在擴張中的分解）

### 6.1 素理想分解定理

設 $L/K$ 為數域的有限擴張，$\mathcal{O}_K$ 和 $\mathcal{O}_L$ 分別為其整環。對於 $K$ 中的非零素理想 $\mathfrak{p}$，考慮其在 $\mathcal{O}_L$ 中的分解。根據代數數論的基本定理，$\mathfrak{p}\mathcal{O}_L$ 可以唯一分解為

$$\mathfrak{p}\mathcal{O}_L = \prod_{i=1}^{g} \mathfrak{P}_i^{e_i}$$

其中 $\mathfrak{P}_i$ 為 $\mathcal{O}_L$ 中的不同素理想，$e_i \geq 1$ 為爆炸指數（Ramification Index），且 $\sum_{i=1}^{g} e_i = [L : K]$。

每個 $\mathfrak{P}_i$ 都是 $\mathfrak{p}$ 上的素理想，且剩餘類域擴張 $\mathcal{O}_L/\mathfrak{P}_i$ 為 $\mathcal{O}_K/\mathfrak{p} = \mathbb{F}_q$ 的有限擴張。若 $f_i = [\mathcal{O}_L/\mathfrak{P}_i : \mathcal{O}_K/\mathfrak{p}]$ 為剩餘類域次數，則有

$$[L : K] = \sum_{i=1}^{g} e_i f_i$$

這是有限擴張中素理想分解的基本公式。當所有 $e_i = 1$ 時，稱 $\mathfrak{p}$ 為**非分歧**（Unramified）的；當 $g = 1$ 且 $e = [L : K]$ 時，稱 $\mathfrak{p}$ 為**全爆炸**（Totally Ramified）的。

### 6.2 分歧與判別式

當 $e_i > 1$ 時，相應的素理想 $\mathfrak{P}_i$ 稱為**分歧**（Ramified）的。分歧的發生與判別式密切相關。具體來說，$\mathfrak{p}$ 分歧的充要條件是 $\mathfrak{p}$ 整除數域 $L$ 的判別式 $\Delta_{L/\mathbb{Q}}$。

對於局部分歧，我們定義**分歧群**（Ramification Group）$G_i$ 為穩定化子群包含某個特定條件的子群，其結構反映了在該素理想附近的分歧程度。對於希爾伯特（Hilbert）分歧理論，我們考慮

$$G_i = \{ \sigma \in \text{Gal}(L/K) \mid v_{\mathfrak{P}}(\sigma(x) - x) \geq i+1 \text{ for all } x \in \mathcal{O}_L \}$$

這些分歧群構成了一個過濾系列，決定了分歧的具體結構。

### 6.3 Frobenius 元素與分解群

在伽羅瓦擴張 $L/K$ 中，對於非分歧素理想 $\mathfrak{p}$，存在一個稱為 **Frobenius 自同構**的唯一元素 $\text{Frob}_{\mathfrak{p}} \in \text{Gal}(L/K)$，使得對所有 $x \in \mathcal{O}_L$ 有

$$\text{Frob}_{\mathfrak{p}}(x) \equiv x^{N(\mathfrak{p})} \pmod{\mathfrak{P}}$$

其中 $N(\mathfrak{p}) = |\mathcal{O}_K/\mathfrak{p}|$。Frobenius 元素在類域論和動系統理論中起核心作用。

對於每個素理想 $\mathfrak{P}_i$，其分解群 $D(\mathfrak{P}_i) = \{ \sigma \in \text{Gal}(L/K) \mid \sigma(\mathfrak{P}_i) = \mathfrak{P}_i \}$ 是 Galois 群的子群，滿足 $|D(\mathfrak{P}_i)| = e_i f_i$。當 $\mathfrak{P}_i$ 非分歧時，分解群與循環群同構，其生成元即為 Frobenius 元素。

---

## 7. Ideal Norm and Extension of Ideals（理想范數與理想擴張）

### 7.1 理想范數的定義

對於數域 $K$，非零理想 $\mathfrak{a} \subseteq \mathcal{O}_K$ 的**范數**（Norm）定義為

$$N(\mathfrak{a}) = |\mathcal{O}_K/\mathfrak{a}|$$

這是有限集合 $\mathcal{O}_K/\mathfrak{a}$ 的基數。當 $\mathfrak{a} = (\alpha)$ 為主理想時，有

$$N((\alpha)) = |N_{K/\mathbb{Q}}(\alpha)|$$

即理想的范數等於生成元在基本域擴張中的代數范數的絕對值。這個公式連接了理想論與域論，是計算理想范數的關鍵工具。

對於非主理想，可以通過將理想寫成基矩陣的形式來計算其范數。若 $\{ \alpha_1, \ldots, \alpha_n \}$ 為 $\mathcal{O}_K$ 的一組整基，$\mathfrak{a} = \sum_{i=1}^n a_i \alpha_i \mathbb{Z}$，則 $N(\mathfrak{a}) = |\det(a_i \alpha_i)|$，這個公式在实际计算中非常有用。

### 7.2 范數的乘法性質

理想范數滿足乘法性質：對於任意非零理想 $\mathfrak{a}, \mathfrak{b} \subseteq \mathcal{O}_K$，有

$$N(\mathfrak{a}\mathfrak{b}) = N(\mathfrak{a}) N(\mathfrak{b})$$

這個性質可以直接從定義驗證：因為 $\mathcal{O}_K/(\mathfrak{a}\mathfrak{b}) \cong (\mathcal{O}_K/\mathfrak{a}) \otimes_{\mathcal{O}_K} (\mathcal{O}_K/\mathfrak{b})$，而這個張量積的基數是兩個商環基數的乘積。

對於素理想 $\mathfrak{p}$，其范數為 $N(\mathfrak{p}) = p^f$，其中 $p$ 為 $\mathfrak{p}$ 落下（Residue）的質數，$f$ 為剩餘類域次數。這個事實使得我們可以通過研究質數的分解來理解理想范數的結構。

### 7.3 理想擴張

設 $L/K$ 為數域的有限擴張，$\mathfrak{a} \subseteq \mathcal{O}_K$ 為非零理想。其在 $L$ 中的擴張定義為

$$\mathfrak{a}\mathcal{O}_L = \{ \sum_{i=1}^{n} a_i x_i \mid a_i \in \mathfrak{a}, x_i \in \mathcal{O}_L \}$$

這是 $\mathcal{O}_L$ 的一個非零理想。對於理想范數，有**遞推公式**：

$$N_{L/\mathbb{Q}}(\mathfrak{a}\mathcal{O}_L) = N_{K/\mathbb{Q}}(\mathfrak{a})^{[L:K]}$$

這個公式表明，擴張理想的范數是原理想范數的 $[L:K]$ 次冪。這個結果在研究素數分解時特別有用，因為它建立了局部性質與全域性質之間的聯繫。

### 7.4 共鳴理想與跡

對於非零理想 $\mathfrak{a} \subseteq \mathcal{O}_K$，其**共鳴理想**（Complement Ideal）或**逆步**定義為

$$\mathfrak{a}^{-1} = \{ x \in K \mid x\mathfrak{a} \subseteq \mathcal{O}_K \}$$

這是 $K$ 中的一個分式理想，滿足 $\mathfrak{a}\mathfrak{a}^{-1} = \mathcal{O}_K$。共鳴理想在類群的定義中起關鍵作用，因為類群可以描述為分式理想模主理想的商群。

對於主理想 $(\alpha)$，其逆步為 $(\alpha^{-1})$，只要 $\alpha \neq 0$。對於一般的理想，逆步的結構更為複雜，但總是有 $\mathfrak{a}^{-1} = \text{Hom}_{\mathcal{O}_K}(\mathfrak{a}, \mathcal{O}_K)$。

---

## 模組類別說明

### ArithmeticScheme（算術格式）

`ArithmeticScheme` 類表示算術格式 $X \to \text{Spec}(\mathbb{Z})$，這是算術幾何研究的核心對象。算術格式是介於代數簇與數論對象之間的幾何結構，其纖維 $X_p = X \times_{\text{Spec}(\mathbb{Z})} \text{Spec}(\mathbb{F}_p)$ 編碼了模 $p$ 的算術信息。對於每個質數 $p$，纖維是定義在有限域 $\mathbb{F}_p$ 上的代數簇，其幾何性質反映了原格式的算術性質。

### NeronModel（Néron模型）

`NeronModel` 類實現了阿貝爾簇的 Néron 模型。阿貝爾簇 $A$ 在數域 $K$ 上的 Néron 模型是 $\text{Spec}(\mathcal{O}_K)$ 上的光滑群格式，它滿足 Néron 映射的泛性質（Universal Property）。Néron 模型的存在性是 Serre-Lang 定理的深化，它使得我們能夠將阿貝爾簇的算術性質的研究歸結為其 Néron 模型的幾何性質的研究。

### ArakelovGeometry（阿羅開洛夫幾何）

`ArakelovGeometry` 類實現了阿羅開洛夫幾何的基本概念，這是丘成桐和 Faltings 發展的將微分幾何方法引入算術幾何的理論框架。在阿羅開洛夫幾何中，算術格式上的向量叢配備了赫米特度量（Hermitian Metric），其「算術度」通過在所有質位（包括無窮位）的局部度之和來定義。這個理論在數論中有一系列深刻應用，包括算術 Riemann-Roch 定理和龐加萊叢的算術對偶定理。

### MordellWeil（莫德爾-韋伊定理）

`MordellWeil` 類實現了莫德爾-韋伊定理，這是算術幾何中最基礎的結果之一。定理斷言：若 $A$ 為數域 $K$ 上的阿貝爾簇，則其 $K$-有理點群 $A(K)$ 是有限生成的阿貝爾群。這個結果將阿貝爾簇的有理點結構描述為有限生成的交換群，根據有限生成阿貝爾群的基本定理，這意味著

$$A(K) \cong A(K)_{\text{tor}} \oplus \mathbb{Z}^r$$

其中 $A(K)_{\text{tor}}$ 為撓子群（有限），$r$ 為**莫德爾-韋伊秩**（Mordell-Weil Rank）。這個分解是研究丟番圖方程（Diophantine Equation）的重要工具。

---

## 總結

本模組涵蓋了算術幾何的核心內容，從數域的基本理論出發，經過理想論與類數理論，最終達到阿貝爾簇的莫德爾-韋伊定理。這些內容構成了解決丟番圖方程和數論問題的現代理論基礎，並與數論、幾何、分析等多個數學分支有深刻聯繫。模組中的類提供了一個計算框架，使得這些深刻的數學理論可以在計算機上進行實驗和應用。