# 橢圓曲線（Elliptic Curves）

## 1. 概述

橢圓曲線是代數幾何中最重要的研究對象之一，在數論和密碼學中有著廣泛的應用。一條橢圓曲線由以下魏爾斯特拉斯標準方程定義：

$$E: y^2 = x^3 + ax + b$$

其中判別式 $\Delta = -16(4a^3 + 27b^2) \neq 0$，確保曲線是光滑的（沒有奇點）。

在 `lean4py` 中，`EllipticCurve` 類封裝了這一結構：

```python
class EllipticCurve:
    def __init__(self, A: float, B: float):
        self.A = A
        self.B = B
        self.discriminant = -16 * (4 * A**3 + 27 * B**2)
```

## 2. 群結構

橢圓曲線最驚人的性質之一是它的點集合可以構成一個阿貝爾群。

### 2.1 無窮遠點作為單位元

群的單位元（恆等元素）是「無窮遠點」$O$（在射影幾何中引進）。這對應於 `GroupLaw.identity()` 所返回的 `"O"`。

### 2.2 點加法運算

對於兩個點 $P$ 和 $Q$，連接它們的直線（若 $P \neq Q$ 為割線，若 $P = Q$ 為切線）與曲線的第三個交點關於 $x$ 軸的對稱點即為 $P + Q$。這稱為「弦切法」。

公式如下（當 $P \neq Q$ 時）：

$$m = \frac{y_Q - y_P}{x_Q - x_P}$$

$$x_R = m^2 - x_P - x_Q$$

$$y_R = m(x_P - x_R) - y_P$$

對應實現：

```python
@staticmethod
def add(P: Tuple[float, float], Q: Tuple[float, float],
        curve: EllipticCurve) -> Tuple[float, float]:
    if P == Q:
        return GroupLaw.double(P, curve)
    m = (Q[1] - P[1]) / (Q[0] - P[0])
    x_r = m**2 - P[0] - Q[0]
    y_r = m * (P[0] - x_r) - P[1]
    return (x_r, y_r)
```

### 2.3 倍點運算

當 $P = Q$ 時，使用切線斜率：

$$m = \frac{3x_P^2 + a}{2y_P}$$

$$x_{2P} = m^2 - 2x_P$$

$$y_{2P} = m(x_P - x_{2P}) - y_P$$

```python
@staticmethod
def double(P: Tuple[float, float],
            curve: EllipticCurve) -> Tuple[float, float]:
    m = (3 * P[0]**2 + curve.A) / (2 * P[1])
    x_r = m**2 - 2 * P[0]
    y_r = m * (P[0] - x_r) - P[1]
    return (x_r, y_r)
```

## 3. 撓點與 Mordell-Weil 群

### 3.1 撓點（Torsion Points）

撓點是滿足 $nP = O$（單位元）的有限階點。若存在正整數 $n$ 使得 $nP = O$，則 $P$ 的撓率為 $n$。

根據 Mazur 定理，橢圓曲線在 $\mathbb{Q}$ 上的撓子群只能是以下 15 種之一：
- $\mathbb{Z}/n\mathbb{Z}$，其中 $n = 1, 2, \ldots, 10$ 或 $12$
- $\mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/2n\mathbb{Z}$，其中 $n = 1, \ldots, 4$

### 3.2 Mordell-Weil 群

Mordell-Weil 定理表明，橢圓曲線在有理數域上的點群 $E(\mathbb{Q})$ 是有限生成的：

$$E(\mathbb{Q}) \cong E(\mathbb{Q})_{\text{tors}} \times \mathbb{Z}^r$$

其中 $r$ 稱為**秩**（rank），表示獨立無窮階點的數目。

```python
class Rank:
    @staticmethod
    def compute(curve: EllipticCurve) -> int:
        return 0  # 簡化實現

    @staticmethod
    def is_finite_generated(curve: EllipticCurve) -> bool:
        return True
```

## 4. 自同態

### 4.1 弗羅比尼烏斯自同態

對於定義在有限域 $\mathbb{F}_p$（$p$ 為素數）上的橢圓曲線，弗羅比尼烏斯自同態為：

$$\varphi: (x, y) \mapsto (x^p, y^p)$$

它滿足特徵多項式：

$$\varphi^2 - t\varphi + p = 0$$

其中 $t = p + 1 - |E(\mathbb{F}_p)|$ 為曲線的跡。

### 4.2 倍數映射

對於任意整數 $n$，倍數映射 $[n]: P \mapsto nP$ 是一個從群到自身的同態。

## 5. 韋伊配對（Weil Pairing）

韋伊配對是撓點之間的一個重要的非退化雙線性型：

$$e_n: E[n] \times E[n] \to \mu_n$$

其中 $E[n] = \{P \in \bar{E} : nP = O\}$ 為 $n$ 撓點群，$\mu_n$ 為 $n$ 次單位根群。

韋伊配對在構造基於配對的密碼學中起關鍵作用。

## 6. Birch 與 Swinnerton-Dyer 猜想

Birch 與 Swinnerton-Dyer 猜想是千禧年七大數學難題之一，斷言：

**橢圓曲線 $E$ 在 $\mathbb{Q}$ 上的秩 $r$ 等於$L$函數 $L(E, s)$ 在 $s=1$ 處的零點階數。**

即：

$$\text{ord}_{s=1} L(E, s) = \text{rank}(E(\mathbb{Q}))$$

## 7. 密碼學應用

### 7.1 ECDSA（橢圓曲線數字簽名算法）

ECDSA 是 DSA（數字簽名算法）的橢圓曲線版本。簽名過程：

1. 選擇私鑰 $d \in [1, n-1]$
2. 公鑰 $Q = dG$（$G$ 為生成元）
3. 簽名：$(r, s)$ 其中 $r$ 來自 $kG$ 的 $x$ 座標，$s \equiv k^{-1}(H(m) + dr) \pmod{n}$

### 7.2 ECDH（橢圓曲線 Diffie-Hellman 密鑰交換）

ECDH 允許雙方在不安全通道上建立共享密鑰：

1. Alice 選擇私鑰 $a$，發送公鑰 $A = aG$
2. Bob 選擇私鑰 $b$，發送公鑰 $B = bG$
3. 共享密鑰：$S = aB = bA = abG$

### 7.3 安全性基礎

橢圓曲線密碼學的安全性基於**橢圓曲線離散對數問題**（ECDLP）：給定點 $G$ 和 $Q = nG$，求 $n$ 是計算上不可行的。

對於一般曲線，最佳攻擊需要 $O(\sqrt{n})$ 時間，比 RSA 的亞指數攻擊更有效，因此可以使用更短的密鑰達到同等安全級別。

## 8. 模塊結構

本模塊 (`elliptic_curves.py`) 提供以下類：

| 類別 | 功能 |
|------|------|
| `EllipticCurve` | 橢圓曲線的基本定義與性質 |
| `GroupLaw` | 點加法與倍點的群運算 |
| `TorsionPoint` | 撓點的搜尋與階計算 |
| `Rank` | Mordell-Weil 秩的計算 |
| `Isogeny` | 曲線間的同源映射 |

## 9. 參考文獻

- Silverman, J. H. (2009). *The Arithmetic of Elliptic Curves* (2nd ed.). Springer.
- Washington, L. C. (2008). *Elliptic Curves: Number Theory and Cryptography* (2nd ed.). Chapman and Hall/CRC.
- Cremona, J. E. (1997). *Algorithms for Modular Elliptic Curves* (2nd ed.). Cambridge University Press.