# 橢圓曲線測試文檔

本文檔說明 `test_elliptic_curves.py` 中測試用例的數學原理。

## 1. 測試驗證內容概述

本測試文件針對橢圓曲線模塊的核心功能進行驗證，包括曲線的基本性質、群運算、撓點分析、秩的計算以及同源映射。

## 2. 點加法測試 (Point Addition)

### 數學原理

設 $E$ 為域 $K$ 上的橢圓曲線，定義為 Weierstrass 方程：
$$E: y^2 = x^3 + Ax + B$$

其中 $A, B \in K$ 且判別式 $\Delta = 4A^3 + 27B^2 \neq 0$（保證曲線光滑）。

對於曲線上兩點 $P = (x_1, y_1)$ 和 $Q = (x_2, y_2)$，其加法規則定義如下：

- 若 $Q$ 為單位元 $O$（無窮遠點），則 $P + O = P$
- 若 $x_1 = x_2$ 但 $y_1 \neq y_2$，則 $P + Q = O$
- 若 $P \neq Q$，則斜率為：
  $$\lambda = \frac{y_2 - y_1}{x_2 - x_1}$$
  和為：
  $$x_3 = \lambda^2 - x_1 - x_2$$
  $$y_3 = \lambda(x_1 - x_3) - y_1$$

### 測試用例 (`TestGroupLaw.test_add`)

```python
E = EllipticCurve(1.0, 1.0)
P = (0.0, 1.0)
Q = (1.0, math.sqrt(3.0))  # Different x-coordinate
result = GroupLaw.add(P, Q, E)
```

測試驗證不同橢圓曲線上兩點相加的結果為一對坐標元組。

## 3. 倍點測試 (Point Doubling)

### 數學原理

點的倍運算是將點與自身相加：$2P = P + P$。

當 $P = (x_1, y_1)$ 且 $y_1 \neq 0$ 時，斜率為：
$$\lambda = \frac{3x_1^2 + A}{2y_1}$$

計算得：
$$x_3 = \lambda^2 - 2x_1$$
$$y_3 = \lambda(x_1 - x_3) - y_1$$

當 $y_1 = 0$ 時，$2P = O$（此時 $P$ 為撓點）。

### 測試用例 (`TestGroupLaw.test_double`)

```python
E = EllipticCurve(1.0, 1.0)
P = (0.0, 1.0)
result = GroupLaw.double(P, E)
```

測試驗證點倍運算返回有效的坐標元組。

## 4. 單位元測試 (Identity Element)

### 數學原理

橢圓曲線加法群的單位元是無窮遠點 $O$，滿足：
$$P + O = O + P = P, \quad \forall P \in E$$

在射影坐標系中，$O = [0:1:0]$。

### 測試用例 (`TestGroupLaw.test_identity`)

```python
result = GroupLaw.identity()
self.assertEqual(result, "O")
```

測試驗證單位元表示為字符串 `"O"`。

## 5. 撓點與階測試 (Torsion Points and Order)

### 數學原理

撓點是指滿足 $nP = O$（單位元）的點 $P$，其中 $n$ 為正整數。滿足此條件的最小正整數 $n$ 稱為點的**階**。

根據 Mazur 定理，撓點的階只能是 1 至 10 或 12 之一，或是 2。

常見的撓點群結構：
- $E[n] \cong \mathbb{Z}/n\mathbb{Z} \times \mathbb{Z}/n\mathbb{Z}$（對有些曲線）
- $E[2] \cong \mathbb{Z}/2\mathbb{Z} \times \mathbb{Z}/2\mathbb{Z}$（所有二撓點）

### 測試用例

**撓點查找 (`TestTorsionPoint.test_find`)**：
```python
E = EllipticCurve(1.0, 1.0)
result = TorsionPoint.find(E, 2)
```
驗證返回撓點列表。

**階計算 (`TestTorsionPoint.test_order`)**：
```python
E = EllipticCurve(1.0, 1.0)
P = (0.0, 1.0)
result = TorsionPoint.order(P, E)
```
驗證返回整數類型的階。

## 6. 群秩測試 (Rank)

### 數學原理

橢圓曲線 $E(\mathbb{Q})$ 的代數獨立生成元個數稱為**秩**，記為 $r$。Mordell-Weil 定理表明：
$$E(\mathbb{Q}) \cong E(\mathbb{Q})_{\text{tors}} \times \mathbb{Z}^r$$

其中 $E(\mathbb{Q})_{\text{tors}}$ 是撓點群（有限），$\mathbb{Z}^r$ 是自由阿貝爾群。

秩是刻畫曲線數論性質的重要不變量：
- $r = 0$：曲線只有撓點（ Mordell 曲線）
- $r = 1$：曲線具有正秩（無限多有理點）
- $r \geq 2$：高度複雜的算術性質

### 測試用例 (`TestRank.test_compute`)

```python
E = EllipticCurve(1.0, 1.0)
result = Rank.compute(E)
```

### 有限生成性 (`TestRank.test_is_finite_generated`)

Mordell-Weil 定理保證 $E(\mathbb{Q})$ 是有限生成的，測試驗證此性質。

## 7. 同源映射測試 (Isogeny)

### 數學原理

同源是橢圓曲線間的態射，保持單位元且滿足群結構。對於曲線 $E_1$ 和 $E_2$，同源 $\phi: E_1 \to E_2$ 滿足：
$$\phi(P + Q) = \phi(P) + \phi(Q)$$

同源的度（degree）定義為其誘導的函子在阿米巴空間上的度。

**Velu 公式**提供了計算同源的具體方法。

### 測試用例

**同源存在性 (`TestIsogeny.test_exists`)**：
```python
E1 = EllipticCurve(1.0, 1.0)
E2 = EllipticCurve(1.0, 1.0)
self.assertTrue(Isogeny.exists(E1, E2))
```

**度計算 (`TestIsogeny.test_degree`)**：
```python
result = Isogeny.degree("phi")
```

## 8. 曲線光滑性測試

### 數學原理

橢圓曲線要求判別式 $\Delta = 4A^3 + 27B^2 \neq 0$，確保曲線沒有奇點（自交或尖點）。

```python
E = EllipticCurve(1.0, 1.0)
self.assertTrue(E.is_smooth())
```

## 9. 測試類層次結構

| 測試類 | 驗證內容 |
|--------|----------|
| `TestEllipticCurve` | 曲線創建、光滑性、函數求值 |
| `TestGroupLaw` | 點加法、倍運算、單位元 |
| `TestTorsionPoint` | 撓點查找、階計算 |
| `TestRank` | 秩計算、有限生成性 |
| `TestIsogeny` | 同源存在性、度計算 |

## 10. 密碼學應用背景

橢圓曲線的這些性質直接支撐以下密碼學應用：

- **ECDSA**：基於離散對數問題
- **橢圓曲線 Diffie-Hellman 密鑰交換 (ECDH)**
- **橢圓曲線配對基密碼學 (Pairing-based cryptography)**
- **橢圓曲線整數分解 (ECRF)**

撓點結構和秩的分析在曲線安全性評估中起關鍵作用。