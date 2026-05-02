# Class Field Theory 測試文檔

本文件說明 `test_class_field_theory.py` 中的測試案例及其背後的數學原理。

## 1. 概述：類域論測試驗證的內容

類域論（Class Field Theory）是代數數論的核心分支，研究阿貝爾擴張與局部/全局域的理想類群之間的對應關係。本測試文件驗證以下核心概念：

- **阿貝爾擴張**（Abelian Extension）的結構
- **Artin 映射**（Artin Map）的計算與性質
- **互反律**（Reciprocity Law）的成立
- **伊代爾類群**（Idele Class Group）的性質
- **希爾伯特類域**（Hilbert Class Field）的計算

---

## 2. 局部類域測試（Local Class Field Tests）

### 2.1 IdeleClassGroup 類

```python
def test_compute(self):
    result = IdeleClassGroup.compute("Q")
    self.assertIn("group", result)

def test_is_locally_compact(self):
    self.assertTrue(IdeleClassGroup.is_locally_compact("Q"))
```

### 數學原理

**伊代爾（Idele）** 是局部域的乘法群的對應物。對於全域域 $K$，伊代爾群 $I_K$ 是所有局部伊代爾的直積：

$$I_K = \prod_v K_v^*$$

**伊代爾類群** $C_K$ 定義為：

$$C_K = I_K / K^*$$

這個群裝備了局部緊拓撲，是局部類域論的核心研究對象。

### 2.2 ArtinMap 局部性質

```python
def test_is_surjective(self):
    ext = AbelianExtension("Q", "Q(ζ₅)")
    self.assertTrue(ArtinMap.is_surjective(ext))
```

---

## 3. 全域類域測試（Global Class Field Tests）

### 3.1 AbelianExtension 類

```python
def test_creation(self):
    ext = AbelianExtension("Q", "Q(ζ₅)")
    self.assertEqual(ext.base, "Q")

def test_is_abelian(self):
    ext = AbelianExtension("Q", "Q(ζ₅)")
    self.assertTrue(ext.is_abelian())

def test_conductor(self):
    ext = AbelianExtension("Q", "Q(ζ₅)")
    result = ext.conductor()
    self.assertIsInstance(result, int)
```

### 數學原理

**阿貝爾擴張**是指伽羅瓦群為阿貝爾群的代數擴張 $L/K$。對於分圓域 $\mathbb{Q}(\zeta_n)$：

- 基域：$\mathbb{Q}$
- 擴張：$\mathbb{Q}(\zeta_5)$（5次單位根生成的域）
- 伽羅瓦群：$\text{Gal}(\mathbb{Q}(\zeta_5)/\mathbb{Q}) \cong (\mathbb{Z}/5\mathbb{Z})^\times \cong \mathbb{Z}/4\mathbb{Z}$

這是一個交換群，因此是阿貝爾擴張。

**導子（Conductor）** $f(L/K)$ 是與擴張相關的重要不變量，對於分圓域 $\mathbb{Q}(\zeta_n)$，其導子為 $n$。

### 3.2 HilbertClassField 類

```python
def test_compute(self):
    result = HilbertClassField.compute("Q")
    self.assertIn("field", result)

def test_class_number(self):
    result = HilbertClassField.class_number("Q")
    self.assertIsInstance(result, int)
```

### 數學原理

**希爾伯特類域** $HCF(K)$ 是 $K$ 的最大非分歧（unramified）阿貝爾擴張。根據類域論基本定理：

$$[HCF(K) : K] = h_K = |Cl(K)|$$

其中 $h_K$ 是 $K$ 的**類數**，$Cl(K)$ 是 $K$ 的理想類群。

對於 $\mathbb{Q}$，類數為 1，意味著 $\mathbb{Q}$ 本身就是類域。

---

## 4. Artin 映射測試（Artin Map Tests）

### 4.1 ArtinMap.compute

```python
def test_compute(self):
    ext = AbelianExtension("Q", "Q(ζ₅)")
    result = ArtinMap.compute(ext, "idele")
    self.assertIsInstance(result, str)
```

### 4.2 ArtinMap.is_surjective

```python
def test_is_surjective(self):
    ext = AbelianExtension("Q", "Q(ζ₅)")
    self.assertTrue(ArtinMap.is_surjective(ext))
```

### 數學原理

**Artin 映射**是類域論的核心同構。對於阿貝爾擴張 $L/K$和避開有限素位集合 $S$的伊代爾，定義：

$$\psi_{L/K}: I_K^S \to \text{Gal}(L/K)$$

**Artin 互反律**表明存在標準分解：

$$I_K^S / P_K^S \cong \text{Gal}(L/K)$$

其中 $P_K^S$ 是主伊代爾子群。

對於分圓域 $\mathbb{Q}(\zeta_n)/\mathbb{Q}$，Artin 映射由以下公式給出：

$$\psi(\alpha) = \sigma_a \quad \text{其中} \quad \sigma_a(\zeta_n) = \zeta_n^a$$

---

## 5. 互反律測試（Reciprocity Law Tests）

### 5.1 通用互反律

```python
def test_holds(self):
    ext = AbelianExtension("Q", "Q(ζ₅)")
    self.assertTrue(ReciprocityLaw.holds(ext))
```

### 5.2 二次互反律

```python
def test_quadratic_reciprocity(self):
    self.assertTrue(ReciprocityLaw.quadratic_reciprocity())
```

### 數學原理

**Artin 互反律**是類域論的基本定理。對於阿貝爾擴張 $L/K$：

$$I_K / (K^* \cdot N_{L/K}(I_L) \cong \text{Gal}(L/K)$$

**二次互反律**是 Artin 互反律在二次擴張中的特殊情況。高斯互反律表明：

$$\left(\frac{p}{q}\right) \left(\frac{q}{p}\right) = (-1)^{\frac{p-1}{2} \cdot \frac{q-1}{2}}$$

其中 $\left(\frac{p}{q}\right)$ 是勒讓德符號。

---

## 6. 測試結構總結

| 測試類 | 測試方法 | 驗證內容 |
|--------|----------|----------|
| `TestAbelianExtension` | `test_creation` | 擴張對象的創建與基域識別 |
| `TestAbelianExtension` | `test_is_abelian` | 伽羅瓦群是否阿貝爾 |
| `TestAbelianExtension` | `test_conductor` | 導子計算法 |
| `TestArtinMap` | `test_compute` | Artin 映射計算 |
| `TestArtinMap` | `test_is_surjective` | 映射的滿射性 |
| `TestReciprocityLaw` | `test_holds` | Artin 互反律成立 |
| `TestReciprocityLaw` | `test_quadratic_reciprocity` | 二次互反律 |
| `TestIdeleClassGroup` | `test_compute` | 伊代爾類群計算 |
| `TestIdeleClassGroup` | `test_is_locally_compact` | 局部緊性 |
| `TestHilbertClassField` | `test_compute` | 希爾伯特類域計算 |
| `TestHilbertClassField` | `test_class_number` | 類數計算 |

---

## 7. 數學背景

### 7.1 分圓域 $\mathbb{Q}(\zeta_5)$

- 單位根：$\zeta_5 = e^{2\pi i/5}$
- degree: $[\mathbb{Q}(\zeta_5) : \mathbb{Q}] = \phi(5) = 4$
- 伽羅瓦群同構於 $\mathbb{Z}/4\mathbb{Z}$

### 7.2 類域論基本定理的意義

類域論建立了：
1. **局部域**的乘法群與其阿貝爾擴張的一一對應
2. **全域域**的伊代爾類群與其阿貝爾擴張的一一對應

這使得許多數論問題可以在這些群的結構中得到解決。