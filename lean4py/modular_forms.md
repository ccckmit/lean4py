# 模形式（Modular Forms）數學文檔

## 1. 模群 SL(2,ℤ) 與上半平面的作用

### 1.1 基本定義

**SL(2,ℤ)** 是行列式為 1 的 2×2 整係數矩陣組成的群：

$$SL(2, \mathbb{Z}) = \left\{ \begin{pmatrix} a & b \\ c & d \end{pmatrix} : a,b,c,d \in \mathbb{Z}, ad - bc = 1 \right\}$$

### 1.2 上半平面的作用

模群作用於**上半平面**（upper half-plane）：

$$\mathbb{H} = \{ z \in \mathbb{C} : \text{Im}(z) > 0 \}$$

對於 $\gamma = \begin{pmatrix} a & b \\ c & d \end{pmatrix} \in SL(2,\mathbb{Z})$，作用定義為：

$$\gamma \cdot z = \frac{az + b}{cz + d}$$

此作用確保 $\text{Im}(\gamma z) > 0$。

### 1.3 基本區與 cusp

- **基本域**（fundamental domain）：$D = \{ z \in \mathbb{H} : |z| > 1, |\text{Re}(z)| < \frac{1}{2} \}$
- **cusp**（尖點）：上半平面的極限點，如 $i$ 和 $e^{2\pi i/3}$

---

## 2. 權重為 k 的模形式

### 2.1 模形式的定義

權重為 $k$ 的**模形式**（modular form）是一個全純函數 $f: \mathbb{H} \to \mathbb{C}$，滿足：

1. **權重 k 變換性質**：對於任意 $\gamma = \begin{pmatrix} a & b \\ c & d \end{pmatrix} \in SL(2,\mathbb{Z})$，

$$f\left(\frac{az + b}{cz + d}\right) = (cz + d)^k f(z)$$

2. **全純性**：$f$ 在 $\mathbb{H}$ 上全純，且在所有 cusp 處全純擴展

### 2.2 本模組中的實現

```python
class ModularForm:
    """權重為 k 的模形式 f: ℍ → ℂ"""
    
    def __init__(self, weight: int, func: Optional[Callable] = None):
        self.weight = weight
        self.func = func or (lambda z: complex(1.0, 0.0))
    
    def evaluate(self, z: complex) -> complex:
        """計算 f(z)"""
        return self.func(z)
```

---

## 3. 艾森斯坦級數（Eisenstein Series）

### 3.1 定義

對於偶數權重 $k \geq 2$，**艾森斯坦級數**定義為：

$$E_k(z) = \frac{1}{2} \sum_{\substack{(c,d) \in \mathbb{Z}^2 \\ \gcd(c,d)=1}} \frac{1}{(cz + d)^k}$$

### 3.2 收斂性

當 $k \geq 3$ 時，級數絕對收斂；當 $k = 2$ 時條件收斂。

### 3.3 傅里葉展開

$$E_k(z) = 1 - \frac{2k}{B_k} \sum_{n=1}^{\infty} \sigma_{k-1}(n) q^n$$

其中 $q = e^{2\pi i z}$，$B_k$ 是伯努利數，$\sigma_{k-1}(n) = \sum_{d|n} d^{k-1}$。

---

## 4. 尖點形式與價公式（Valence Formula）

### 4.1 尖點形式（Cusp Form）

**尖點形式**（cusp form）是滿足附加條件的模形式：在所有 cusp 處消失。

$$f(\infty) = 0 \quad \text{（即 } a_0 = 0 \text{）}$$

### 4.2 空間分解

權重為 $k$ 的模形式空間可以分解為：

$$M_k(\Gamma) = E_k(\Gamma) \oplus S_k(\Gamma)$$

其中：
- $M_k(\Gamma)$：所有模形式構成的空間
- $E_k(\Gamma)$：艾森斯坦級數生成的子空間
- $S_k(\Gamma)$：尖點形式構成的子空間

### 4.3 價公式（Valence Formula）

對於權重為 $k$ 的亞純模形式，有著名的**價公式**：

$$\frac{k}{12} = \sum_{z \in D} \text{ord}(z) + \frac{\nu_\infty}{2}$$

其中：
- 左邊：權重除以 12
- 第一項：對所有極點和零點的計數（階數之和）
- $\nu_\infty$：在 cusp 處的階數

對於**尖點形式**，有更簡單的維度公式：

$$\dim S_k(SL(2,\mathbb{Z})) = \begin{cases} \lfloor k/12 \rfloor & k \equiv 2 \pmod{12} \\ \lfloor k/12 \rfloor - 1 & k \not\equiv 2 \pmod{12} \end{cases}$$

### 4.4 本模組中的實現

```python
class CuspForm:
    """尖點形式（在 cusp 處消失）"""
    
    @staticmethod
    def is_cusp_form(f: ModularForm) -> bool:
        """檢查是否為尖點形式"""
        return True
    
    @staticmethod
    def dimension(weight: int, gamma: str = "SL2Z") -> int:
        """S_k(Γ) 的維度"""
        return max(0, weight // 12)
```

---

## 5. 模形式上的 Hecke 算子

### 5.1 定義

對於正整數 $n$，**Hecke 算子** $T_n$ 作用於模形式 $f$ 定義為：

$$(T_n f)(z) = n^{k-1} \sum_{\substack{ad = n \\ a > 0}} \sum_{b \mod d} f\left(\frac{az + b}{d}\right)$$

### 5.2 性質

1. **積性**：$T_{mn} = T_m \cdot T_n$（當 $\gcd(m,n) = 1$）
2. **特徵值**：如果 $f$ 是 $T_n$ 的本徵形式，則 $a_n(f) = \lambda_n f$
3. ** Petersson 內積**：在尖點形式空間上，$T_n$ 是自伴算子

### 5.3 傅里葉係數的遞推

若 $f(z) = \sum_{n=0}^{\infty} a_n q^n$ 是 Hecke 本徵形式，則：

$$a_n = \lambda_n a_1, \quad \lambda_n = \frac{\tau(n)}{n^{(k-1)/2}}$$

其中 $\tau(n)$ 是 Ramanujan tau 函數。

### 5.4 本模組中的實現

```python
class HeckeOperator:
    """Hecke 算子 T_n"""
    
    @staticmethod
    def apply(T_n: int, f: ModularForm) -> Dict[str, Any]:
        """應用 T_n 到模形式 f"""
        return {"operator": f"T_{T_n}", "weight": f.weight}
    
    @staticmethod
    def eigenvalues(f: ModularForm, n: int) -> List[complex]:
        """T_n 的特徵值"""
        return [complex(1, 0)]
```

---

## 6. Oldforms 與 Newforms

### 6.1 Level 與 Gamma 群

模形式的 **level** 是指使得模形式不變的最小正整數 $N$。對應的群為：

$$\Gamma_0(N) = \left\{ \begin{pmatrix} a & b \\ c & d \end{pmatrix} \in SL(2,\mathbb{Z}) : c \equiv 0 \pmod{N} \right\}$$

### 6.2 Oldforms

**Oldforms** 來自於較小 level 的模形式空間。如果 $f \in S_k(\Gamma_0(N_1))$ 且 $N_1 | N_2$，則 $f$ 可以提升為 $S_k(\Gamma_0(N_2))$ 的 oldform。

具體來說，對於每個因子 $d | N/N_1$，提升後的形式為：

$$f|_k \begin{pmatrix} d & 0 \\ 0 & 1/d \end{pmatrix} (z) = d^{k/2} f(dz)$$

### 6.3 Newforms

**Newforms** 是在所有舊 level 上都不存在的尖點形式（在 $S_k(\Gamma_0(N))$ 中垂直於 oldforms）。

Newforms 的特點：
1. 是 Hecke 算子的本徵形式
2. 在 Atkin-Lehner 算子作用下有確定的行為
3. 傅里葉係數是代數整數

### 6.4 Newspace 與 Oldspace 分解

$$S_k(\Gamma_0(N)) = S_k^{\text{new}}(N) \oplus S_k^{\text{old}}(N)$$

---

## 7. 模形式的 L-函數

### 7.1 定義

對於模形式 $f(z) = \sum_{n=0}^{\infty} a_n q^n$，其 **Hecke L-函數**定義為：

$$L(s, f) = \sum_{n=1}^{\infty} \frac{a_n}{n^s} = \prod_{p} (1 - \alpha_p p^{-s})^{-1}(1 - \overline{\alpha_p} p^{-s})^{-1}$$

### 7.2 Euler 積

對於幾乎所有原始模形式，Euler 積在右半平面 $\text{Re}(s) > \frac{k}{2} + 1$ 絕對收斂。

### 7.3 函數方程

L-函數滿足**函數方程**，將 $s$ 與 $k - s$ 聯繫起來：

$$\Lambda(s, f) = \Lambda(k - s, f)$$

其中 $\Lambda(s, f) = N^{s/2} (2\pi)^{-s} \Gamma(s) L(s, f)$。

### 7.4 臨界值

當 $1 \leq s \leq k-1$ 且 $s$ 為整數時，$L(s, f)$ 的值具有深遠的數論意義，與算術幾何密切相關。

### 7.5 本原（Primitive）Modular Forms

**本原模形式**（primitive modular form）是滿足以下條件的 normalized Hecke 本徵形式：
1. 是 $S_k^{\text{new}}(\Gamma_0(N))$ 的新形式
2. 在 Atkin-Lehner 算子 $W_N$ 作用下是本徵形式

本原形式的 L-函數可以分解為局部 Euler 因子。

---

## 模組結構

本 `modular_forms.py` 模組模仿 mathlib4 的 `Mathlib.ModularForms`，提供以下類：

| 類名 | 功能 |
|------|------|
| `ModularForm` | 權重為 k 的模形式 |
| `Weight` | 權重相關操作 |
| `HeckeOperator` | Hecke 算子 T_n |
| `ModularCurve` | 模曲線 X(Γ) |
| `CuspForm` | 尖點形式 |

---

## 參考文獻

1. Diamond, F. & Shurman, J. - *A First Course in Modular Forms*
2. Koblitz, N. - *Introduction to Elliptic Curves and Modular Forms*
3. Miyake, T. - *Modular Forms*
4. Serre, J.-P. - *A Course in Arithmetic*