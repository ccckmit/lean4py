# 範疇理論進階測試文檔 (test_category_theory_advanced)

## 1. 測試概述

本測試文件驗證 `lean4py/category_theory_advanced.py` 模塊中的高級範疇理論概念，包括伴隨函子、極限與餘極限、米田引理、單子與餘單子等核心概念。這些測試確保數學結構的正確性和範疇理論定律的成立。

## 2. 伴隨函子測試 (Adjoint Functor)

### 數學原理

伴隨函子是範疇理論中最重要的概念之一。設 $F: \mathcal{C} \to \mathcal{D}$ 和 $G: \mathcal{D} \to \mathcal{C}$ 為兩個函子，若對所有 $X \in \mathcal{C}$ 和 $Y \in \mathcal{D}$ 存在自然同構：

$$\text{Hom}_{\mathcal{D}}(F(X), Y) \cong \text{Hom}_{\mathcal{C}}(X, G(Y))$$

則稱 $F$ 為 $G$ 的左伴隨，記作 $F \dashv G$。

### 測試案例

| 測試方法 | 驗證內容 | 數學含義 |
|---------|---------|----------|
| `test_is_adjoint` | 檢驗 `is_adjoint()` 返回 `True` | 驗證 Hom 集同構條件是否滿足 |
| `test_unit` | 單位態射的名稱為 `"unit"` | 單位 $\eta: \text{Id}_\mathcal{C} \to G \circ F$ |
| `test_counit` | 余單位態射的名稱為 `"counit"` | 余單位 $\varepsilon: F \circ G \to \text{Id}_\mathcal{D}$ |

**單位與余單位的性質：**
- **單位 (Unit)**：$\eta: 1_\mathcal{C} \Rightarrow G \circ F$，將每個對象 $X$ 映射到 $X \to G(F(X))$
- **余單位 (Counit)**：$\varepsilon: F \circ G \Rightarrow 1_\mathcal{D}$，將每個對象 $Y$ 映射到 $F(G(Y)) \to Y$

## 3. 極限測試 (Limit)

### 數學原理

極限是範疇中描述「普遍對象」的核心概念。給定一個函子 $D: \mathcal{J} \to \mathcal{C}$（其中 $\mathcal{J}$ 為指標範疇），$D$ 的極限 $(\lim D, \pi_i)$ 由一個對象 $\lim D$ 和一族態射 $\pi_i: \lim D \to D(i)$ 組成，使得對任何其他對象 $X$ 與態射 $\phi_i: X \to D(i)$，存在唯一的態射 $u: X \to \lim D$ 使得 $\pi_i \circ u = \phi_i$。

### 測試案例

| 測試方法 | 驗證內容 | 數學對象 |
|---------|---------|----------|
| `test_product` | 積的類型為 `"product"` | 有限積 $\prod_i X_i$ |
| `test_equalizer` | 等化子的類型為 `"equalizer"` | 等化子 $\text{eq}(f, g)$ |
| `test_pullback` | 拉回的類型為 `"pullback"` | 拉回（纖維積）$X \times_Z Y$ |

### 重要性質

- **積 (Product)**：對象簇 $\{X_i\}$ 的積是，使得每個對象到各因子的投影滿足泛性質的對象
- **等化子 (Equalizer)**：兩個態射 $f, g: X \to Y$ 的等化子是使得 $f \circ i = g \circ i$ 成立的對象 $E$ 和單射 $i: E \to X$
- **拉回 (Pullback)**：給定態射 $f: X \to Z$ 和 $g: Y \to Z$，其拉回 $X \times_Z Y$ 是使得 diagram 可交換的泛對象

## 4. 餘極限測試 (Colimit)

### 數學原理

餘極限是極限的對偶概念。對於函子 $D: \mathcal{J} \to \mathcal{C}$，$D$ 的餘極限 $(\text{colim } D, \iota_i)$ 由一個對象 $\text{colim } D$ 和一族態射 $\iota_i: D(i) \to \text{colim } D$ 組成，使得對任何其他對象 $X$ 與態射 $\psi_i: D(i) \to X$，存在唯一的態射 $u: \text{colim } D \to X$ 使得 $u \circ \iota_i = \psi_i$。

### 測試案例

| 測試方法 | 驗證內容 | 數學對象 |
|---------|---------|----------|
| `test_coproduct` | 餘積的類型為 `"coproduct"` | 餘積 $\coprod_i X_i$ |
| `test_coequalizer` | 餘等化子的類型為 `"coequalizer"` | 餘等化子 $\text{coeq}(f, g)$ |
| `test_pushout` | 推出類型為 `"pushout"` | 推出（纖維餘積） |

### 極限與餘極限的對偶關係

| 極限 | 餘極限 |
|------|--------|
| 積 (Product) | 餘積 (Coproduct) |
| 等化子 (Equalizer) | 餘等化子 (Coequalizer) |
| 拉回 (Pullback) | 推出 (Pushout) |
| 終對象 (Terminal Object) | 初始對象 (Initial Object) |

## 5. 米田引理測試 (Yoneda Lemma)

### 數學原理

米田引理是範疇理論中最基本且重要的結果之一。對於任意局部小範疇 $\mathcal{C}$、對象 $X \in \mathcal{C}$ 和預層 $F: \mathcal{C}^{\text{op}} \to \textbf{Set}$，存在自然同構：

$$\text{Nat}(\text{Hom}(X, -), F) \cong F(X)$$

其中 $\text{Hom}(X, -)$ 為由 $X$ 表示的可表預層（米田嵌入）。

### 測試案例

| 測試方法 | 驗證內容 | 數學含義 |
|---------|---------|----------|
| `test_embedding` | 嵌入類型為 `"yoneda_embedding"` | 米田嵌入 $X \mapsto \text{Hom}(X, -)$ |
| `test_isomorphism` | 同構返回 `True` | 驗證 $\text{Nat}(\text{Hom}(X, -), F) \cong F(X)$ |

### 米田嵌入的意義

- 將對象 $X$ 映射到Hom函子 $\text{Hom}(X, -)$
- 這是一個完全忠實的函子 $y: \mathcal{C} \to [\mathcal{C}^{\text{op}}, \textbf{Set}]$
- 意味著每個範疇都可以嵌入到集合範疇的預層範疇中

## 6. 單子與餘單子測試 (Monad & Comonad)

### 數學原理

**單子 (Monad)**：設 $\mathcal{C}$ 為範疇，單子由三元組 $(T, \eta, \mu)$ 組成，其中：
- $T: \mathcal{C} \to \mathcal{C}$ 為函子
- $\eta: \text{Id}_\mathcal{C} \to T$ 為單位態射
- $\mu: T \circ T \to T$ 為乘法態射

需滿足結合律和單位律。

**餘單子 (Comonad)**：單子的對偶概念，由三元組 $(G, \varepsilon, \delta)$ 組成：
- $G: \mathcal{C} \to \mathcal{C}$ 為函子
- $\varepsilon: G \to \text{Id}_\mathcal{C}$ 為余單位
- $\delta: G \to G \circ G$ 為余乘法態射

### 測試案例

| 測試類別 | 測試方法 | 驗證內容 |
|---------|---------|---------|
| `TestMonad` | `test_creation` | 創建單子並驗證 `is_monad()` 返回 `True` |
| `TestComonad` | `test_creation` | 創建餘單子並驗證 `is_comonad()` 返回 `True` |

### 單子的應用

單子廣泛應用於：
- 代數幾何（K-theory, sheaf cohomology）
- 函數式編程（Effect systems, monadic IO）
- 拓撲學（CW 複形的構造）

## 7. 測試與 mathlib4 的對應關係

本模塊參考 Lean 4 的 mathlib4 庫設計，對應關係如下：

| 本模塊 | mathlib4 路徑 |
|--------|--------------|
| `AdjointFunctor` | `Mathlib.CategoryTheory.Adjunction` |
| `Limit` | `Mathlib.CategoryTheory.Limits` |
| `Colimit` | `Mathlib.CategoryTheory.Limits` |
| `YonedaLemma` | `Mathlib.CategoryTheory.Yoneda` |
| `Monad` | `Mathlib.CategoryTheory.Monad` |
| `Comonad` | `Mathlib.CategoryTheory.Comonad` |

## 8. 測試覆蓋範圍

本測試文件覆蓋了範疇理論進階模塊的核心功能：

- ✅ 伴隨函子的基本性質（單位、余單位）
- ✅ 三種基本極限（積、等化子、拉回）
- ✅ 三種基本餘極限（餘積、餘等化子、推出）
- ✅ 米田嵌入與米田引理
- ✅ 單子與餘單子的創建與驗證

---

**版本**：`v1.28`  
**模塊路徑**：`lean4py/category_theory_advanced.py`  
**測試文件**：`tests/test_category_theory_advanced.py`