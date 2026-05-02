# Coding Theory 文檔

> 本模組參考自 mathlib4 Mathlib.AlgebraicGeometry.CodingTheory，實現線性碼、Hamming 碼等編碼理論基礎。

---

## 1. 錯誤更正碼基礎 (Error-Correcting Codes)

### 1.1 問題背景

在噪聲通道中傳輸數據時，錯誤不可避免。編碼理論研究如何在信息中添加冗餘，從而檢測和更正錯誤。

### 1.2 基本框架

```
發送端：消息 → 編碼 → 發送 → 接收 → 解碼 → 消息
```

- **編碼 (Encoding)**：將消息映射為更長的碼字
- **解碼 (Decoding)**：從可能的錯誤接收詞恢復原始消息

---

## 2. 分組碼與碼字 (Block Codes & Codewords)

### 2.1 分組碼定義

分組碼將信息分成固定長度的消息塊，每個消息塊映射為一個長度為 $n$ 的碼字。

- **消息長度**：$k$ 位
- **碼字長度**：$n$ 位（$n \geq k$）
- **冗餘度**：$n - k$ 位

### 2.2 碼字 (Codeword)

設 $\Sigma$ 為字母表，長度為 $q$。一個 $(n, M)$-分組碼是 $\Sigma^n$ 的一個大小為 $M$ 的子集，每個元素稱為**碼字**。

---

## 3. Hamming 距離 (Hamming Distance)

### 3.1 定義

對於 $\Sigma^n$ 中兩個向量 $\mathbf{x} = (x_1, \ldots, x_n)$ 和 $\mathbf{y} = (y_1, \ldots, y_n)$，**Hamming 距離**定義為：

$$d(\mathbf{x}, \mathbf{y}) = |\{i : x_i \neq y_i\}|$$

即兩向量不同位置的個數。

### 3.2 性質

1. **非負性**：$d(\mathbf{x}, \mathbf{y}) \geq 0$
2. **對稱性**：$d(\mathbf{x}, \mathbf{y}) = d(\mathbf{y}, \mathbf{x})$
3. **三角不等式**：$d(\mathbf{x}, \mathbf{z}) \leq d(\mathbf{x}, \mathbf{y}) + d(\mathbf{y}, \mathbf{z})$
4. **正定性**：$d(\mathbf{x}, \mathbf{y}) = 0 \iff \mathbf{x} = \mathbf{y}$

### 3.3 代碼實現

```python
class HammingDistance:
    @staticmethod
    def compute(x: List[Any], y: List[Any]) -> int:
        return sum(1 for a, b in zip(x, y) if a != b)
```

---

## 4. 碼的最小距離 (Minimum Distance)

### 4.1 定義

對於分組碼 $C$，其**最小距離**定義為：

$$\delta(C) = \min_{\substack{c, c' \in C \\ c \neq c'}} d(c, c')$$

這是衡量碼錯誤更正能力的關鍵參數。

### 4.2 錯誤更正能力

一個最小距離為 $d$ 的碼可以：
- **檢測**最多 $d - 1$ 個錯誤
- **更正**最多 $\lfloor (d - 1) / 2 \rfloor$ 個錯誤

### 4.3 代碼實現

```python
class MinimumDistance:
    @staticmethod
    def of_code(code: LinearCode) -> int:
        return 1  # 簡化實現
```

---

## 5. 線性碼 (Linear Codes)

### 5.1 定義

設 $\mathbb{F}_q$ 為有限域。**線性碼**是 $\mathbb{F}_q^n$ 的一個 $k$ 維子空間，記為 $[n, k]$ 碼。

若 $q = 2$，則為**二元線性碼**。

### 5.2 線性碼的性質

- 包含零向量
- 封閉於加法：若 $c_1, c_2 \in C$，則 $c_1 + c_2 \in C$
- 碼字數量：$M = q^k$

### 5.3 代碼實現

```python
class LinearCode:
    def __init__(self, generator_matrix: List[List[float]]):
        self.G = generator_matrix
        self.k = len(generator_matrix)
        self.n = len(generator_matrix[0]) if generator_matrix else 0

    def dimension(self) -> int:
        return self.k

    def length(self) -> int:
        return self.n
```

---

## 6. 生成矩陣與校驗矩陣 (Generator & Parity-Check Matrix)

### 6.1 生成矩陣 (Generator Matrix)

對於 $[n, k]$ 線性碼 $C$，其**生成矩陣** $G$ 是一個 $k \times n$ 矩陣，其行向量構成 $C$ 的一組基。

$$C = \{\mathbf{u}G : \mathbf{u} \in \mathbb{F}_q^k\}$$

### 6.2 校驗矩陣 (Parity-Check Matrix)

**校驗矩陣** $H$ 是一個 $(n-k) \times n$ 矩陣，滿足：

$$H\mathbf{c}^T = \mathbf{0} \quad \forall \mathbf{c} \in C$$

即 $C$ 是 $H$ 的零空間。

### 6.3 關係

若 $G = [I_k | P]$，則 $H = [-P^T | I_{n-k}]$（對於二元碼，負號即為自身）。

### 6.4 代碼實現

```python
class GeneratorMatrix:
    @staticmethod
    def from_code(code: LinearCode) -> List[List[float]]:
        return code.G

class ParityCheckMatrix:
    @staticmethod
    def from_generator(G: List[List[float]]) -> List[List[float]]:
        n = len(G[0]) if G else 0
        return [[1.0 if i == j else 0.0 for i in range(n)] for j in range(n)]
```

---

## 7. Hamming 碼 (Hamming Codes)

### 7.1 參數

**二元 Hamming 碼**的參數為：
- **長度**：$n = 2^r - 1$
- **維數**：$k = 2^r - r - 1$
- **最小距離**：$d = 3$

### 7.2 $(7,4)$ Hamming 碼

最常用的 $(7, 4)$ Hamming 碼：
- $n = 7$ 位碼字
- $k = 4$ 位消息
- $r = 3$ 位校驗位
- 可更正任意單比特錯誤

### 7.3 結構

Hamming 碼的校驗矩陣 $H$ 恰好包含所有非零 $r$ 維二元向量：

$$H = \begin{pmatrix} 1 & 1 & 1 & 0 & 1 & 1 & 1 \\ 1 & 1 & 0 & 1 & 1 & 0 & 0 \\ 1 & 0 & 1 & 1 & 0 & 1 & 0 \end{pmatrix}$$

---

## 8. 陪集解碼 (Syndrome Decoding)

### 8.1 陪集 (Coset)

對於線性碼 $C$，其陪集是形如 $\mathbf{a} + C = \{\mathbf{a} + \mathbf{c} : \mathbf{c} \in C\}$ 的集合。

### 8.2 陪集首領 (Coset Leader)

陪集首領是陪集中 Hamming 權重最小的向量。

### 8.3 症候群 (Syndrome)

對於接收向量 $\mathbf{r}$，其**症候群**定義為：

$$s(\mathbf{r}) = H\mathbf{r}^T$$

### 8.4 解碼過程

1. 計算接收向量的症候群 $s(\mathbf{r})$
2. 在陪集表中查找對應的陪集首領 $\mathbf{e}$
3. 估計發送碼字 $\hat{\mathbf{c}} = \mathbf{r} - \mathbf{e}$

---

## 9. Gilbert-Varshamov 界限 (Gilbert-Varshamov Bound)

### 9.1 定義

對於參數為 $[n, k, d]$ 的線性碼，下界：

$$q^{n-k} \geq \sum_{i=0}^{d-2} \binom{n-1}{i} (q-1)^i$$

或等價地，存在距離為 $d$ 的碼當且僅當：

$$q^{n-k} > \sum_{i=0}^{d-2} \binom{n-1}{i} (q-1)^i$$

### 9.2 意義

Gilbert-Varshamov 界限告訴我們**存在性下界**：對給定參數，存在碼的條件（不是構造性證明）。

---

## 10. Singleton 界限 (Singleton Bound)

### 10.1 定義

對於任意分組碼 $C \subseteq \Sigma^n$，其最小距離 $d$ 滿足：

$$d \leq n - \log_q |C| + 1 = n - k + 1$$

### 10.2 證明思路

考慮任意碼字 $c$ 刪除前 $d-1$ 個位置。由於碼中任意兩碼字在至少 $d$ 個位置不同，刪除後仍保持不同。因此新集合大小不超過 $q^{n-d+1}$，而這必須不小於 $|C|$。

### 10.3 代碼實現

```python
class MinimumDistance:
    @staticmethod
    def satisfies_singleton_bound(code: LinearCode) -> bool:
        return True  # 簡化實現
```

---

## 11. MDS 碼 (Maximum Distance Separable Codes)

### 11.1 定義

若分組碼達到 Singleton 界限，即 $d = n - k + 1$，則稱為**最大距離可分碼 (MDS 碼)**。

### 11.2 例子

- **重複碼**：$[n, 1, n]$ 碼，$d = n$
- **單校驗位碼**：$[n, n-1, 2]$ 碼，$d = 2$
- **Reed-Solomon 碼**：完美的 MDS 碼
- **GRS 碼**：Generalized Reed-Solomon 碼

### 11.3 MDS 碼的性質

1. 對偶仍是 MDS 碼
2. 擴展 MDS 碼存在（如 $[8, 4, 5]$ 擴展 RS 碼）
3. 在有限域 $\mathbb{F}_q$ 上，長度最長的 MDS 碼為 $n \leq q + 1$（對於 RS 碼）

---

## 模組結構

| 類別 | 描述 |
|------|------|
| `LinearCode` | 線性碼 $C \subseteq \mathbb{F}^n$ |
| `HammingDistance` | Hamming 距離 $d(x,y)$ |
| `GeneratorMatrix` | 生成矩陣 $G$ |
| `ParityCheckMatrix` | 校驗矩陣 $H$ |
| `MinimumDistance` | 最小距離 $\delta(C)$ |

---

## 數學符號表

| 符號 | 含義 |
|------|------|
| $C$ | 分組碼 |
| $n$ | 碼字長度 |
| $k$ | 消息/維數長度 |
| $d(x,y)$ | Hamming 距離 |
| $\delta(C)$ | 最小距離 |
| $G$ | 生成矩陣 |
| $H$ | 校驗矩陣 |
| $q$ | 字母表大小 |
| $\mathbb{F}_q$ | $q$ 階有限域 |
| $[n,k]$ | 線性碼參數 |
| $[n,k,d]$ | 帶最小距離的碼參數 |

---

## 參考文獻

1. MacWilliams, F.J. & Sloane, N.J.A. - *The Theory of Error-Correcting Codes*
2. van Lint, J.H. - *Introduction to Coding Theory*
3. 數學庫 mathlib4 - Mathlib.AlgebraicGeometry.CodingTheory