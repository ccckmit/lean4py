# L-函數模組 (l_functions)

本模組實現了黎曼ζ函數與狄利克雷 L-函數，模仿 mathlib4 的 `Mathlib.NumberTheory.LFunctions` 設計。

---

## 1. 黎曼ζ函數 (Riemann Zeta Function)

### 定義

黎曼ζ函數定義為：

$$\zeta(s) = \sum_{n=1}^{\infty} n^{-s} = 1 + \frac{1}{2^s} + \frac{1}{3^s} + \frac{1}{4^s} + \cdots$$

其中 $s$ 為複數變數。當 $\text{Re}(s) > 1$ 時，此級數絕對收斂。

### 平凡零點 (Trivial Zeros)

ζ函數的平凡零點位於負偶數處：

$$s = -2, -4, -6, -8, \ldots$$

這些零點稱為「平凡」，因為它們的存在可以通過伽瑪函數的性質簡單解釋。

---

## 2. 歐拉積 (Euler Product)

### 素數無窮積表示

對於 $\text{Re}(s) > 1$，ζ函數可以表示為素數的無窮積：

$$\zeta(s) = \prod_{p \text{ prime}} \frac{1}{1 - p^{-s}} = \prod_{p \text{ prime}} (1 - p^{-s})^{-1}$$

這是歐拉乘積公式，表明ζ函數與素數分佈有深刻聯繫。展開後即恢復原始級數定義。

### 收斂性

歐拉積在 $\text{Re}(s) > 1$ 時絕對收斂。當 $s = 1$ 時，積分發散，這與調和級數 $\sum \frac{1}{n}$ 發散的事實一致。

---

## 3. 函數方程 (Functional Equation)

### ζ函數的函數方程

黎曼ζ函數滿足對稱性方程：

$$\zeta(s) = 2^s \pi^{s-1} \sin\left(\frac{\pi s}{2}\right) \Gamma(1-s) \zeta(1-s)$$

### 另類形式 (Λ函數)

定義輔助函數：

$$\Lambda(s) = \pi^{-s/2} \Gamma\left(\frac{s}{2}\right) \zeta(s)$$

則函數方程簡化為優美形式：

$$\Lambda(s) = \Lambda(1-s)$$

這種對稱性是理解ζ函數零點分佈的核心。

---

## 4. 狄利克雷 L-函數 (Dirichlet L-functions)

### 定義

對於狄利克雷特徵 $\chi$，L-函數定義為：

$$L(s, \chi) = \sum_{n=1}^{\infty} \frac{\chi(n)}{n^s} = \sum_{n=1}^{\infty} \chi(n) n^{-s}$$

當 $\text{Re}(s) > 1$ 時收斂。

### 主要性質

- **L(1, χ) = 0**：當 $\chi$ 為非主特徵時，此結果導出狄利克雷素數定理
- **函數方程**：$L(s, \chi) = \varepsilon(\chi) L(1-s, \bar{\chi})$，其中 $\varepsilon(\chi)$ 為複數因子

---

## 5. 解析延拓 (Analytic Continuation)

### ζ函數的延拓

黎曼ζ函數可以解析延拓至整個複平面，除 $s = 1$ 外的所有點：

$$\zeta(s) = \frac{1}{\Gamma(s)} \int_0^\infty \frac{x^{s-1}}{e^x - 1} dx$$

此積分表示在 $\text{Re}(s) > 1$ 時有效，但可通過解析延拓擴展定義域。$s = 1$ 為唯一極點，留數為 1。

### L-函數的延拓

對於原始特徵 $\chi$，L-函數 $L(s, \chi)$ 是整函數（無奇點），可延拓至整個複平面。

---

## 6. 臨界帶 (Critical Strip)

### 定義

臨界帶是複平面中滿足以下條件的區域：

$$0 < \text{Re}(s) < 1$$

### 黎曼猜想

黎曼猜想斷言：ζ函數的所有非平凡零點（即非平凡零點，非 $s = -2n$）都位於臨界線上：

$$\text{Re}(s) = \frac{1}{2}$$

即所有非平凡零點都在直線 $\frac{1}{2} + it$ 上，其中 $t \in \mathbb{R}$。

### 零點分佈

- **平凡零點**：$s = -2, -4, -6, \ldots$（負偶數）
- **非平凡零點**：位於臨界帶內，目前已知數十億個，且皆在 $\text{Re}(s) = \frac{1}{2}$ 上

---

## 7. 素數歐拉因子 (Euler Factors at Primes)

### 局部因子

對於每個素數 $p$，ζ函數的歐拉因子為：

$$\frac{1}{1 - p^{-s}}$$

對於 L-函數，相應因子為：

$$\frac{1}{1 - \chi(p) p^{-s}}$$

### 有限素積

對於有限素數集合 $S$，定義部分積：

$$\zeta_S(s) = \prod_{p \in S} \frac{1}{1 - p^{-s}}$$

這些有限積可用於逼近完整ζ函數。

---

## 8. Rankin-Selberg L-函數

### 起源

Rankin-Selberg L-函數起源於數論中的譜理論，與自守形式密切相关。

### 定義

對於兩個黎曼ζ函數的線性組合或更一般的自守表示，Rankin-Selberg L-函數定義為：

$$L(s, f \times g) = \prod_{p} \prod_{i=1}^{m} \prod_{j=1}^{n} \frac{1}{1 - \alpha_{p,i} \beta_{p,j} p^{-s}}$$

其中 $f$ 和 $g$ 為自守形式，$\alpha_{p,i}$、$\beta_{p,j}$ 為其局部Satake參數。

### 函數方程

Rankin-Selberg L-函數同樣滿足函數方程，形式為：

$$\Lambda(s, f \times g) = \varepsilon(s, f \times g) \Lambda(1-s, f \times g)$$

### 應用

- 證明黎曼猜想與自守形式的聯繫
- 研究素數分佈的下界估計
- 數論中許多重要結果的證明工具

---

## 模組類別對照表

| 類別 | 對應數學對象 |
|------|-------------|
| `RiemannZeta` | 黎曼ζ函數 ζ(s) |
| `DirichletLFunction` | 狄利克雷 L-函數 L(s, χ) |
| `FunctionalEquation` | 函數方程 |
| `AnalyticContinuation` | 解析延拓 |
| `EulerProduct` | 歐拉積表示 |

---

## 參考文獻

- Riemann, B. (1859). Über die Anzahl der Primzahlen unter einer gegebenen Größe.
- Dirichlet, P.G.L. (1837). Beweis des Satzes, dass jede unendliche arithmetische Progression, deren erstes Glied und Differenz ganze Zahlen sind und in welcher nicht alle Zahlen durch eine endliche Zahl theilbar sind, unendlich viele Primzahlen enthält.
- Rankin, R.A. (1939). Contributions to the theory of Ramanujan's function τ(n) and similar arithmetical functions.
- Selberg, A. (1942). On the zeros of Riemann's zeta-function.