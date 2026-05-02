# Topos 測試文檔

## 概述

本測試文件 (`test_topos.py`) 驗證 lean4py 庫中與 Topos 理論相關的實現。Topos 理論是範疇論的重要分支，作為集合論的推廣，同時容納了幾何與邏輯的視角。

---

## 1. 測試驗證的 Topos 理論內容

### 1.1 基本 Topos 結構

測試類 `TestTopos` 驗證了 elementary topos 的核心性質：

| 測試方法 | 驗證內容 | 數學意義 |
|---------|---------|---------|
| `test_creation` | 空的 sheaves 列表 | Topos 的基本構造 |
| `test_subobject_classifier` | 子對象分類器含 `True` | 判斷命題真假的基础 |
| `test_has_exponentials` | 指數對象存在性 | 笛卡爾封閉性的關鍵 |
| `test_is_cartesian_closed` | 笛卡爾封閉性 | 有限極限存在且指數對象存在 |
| `test_power_object` | 冪對象 | 集合的冪集在 Topos 中的推廣 |

### 1.2 Topos 的定義

一個 **elementary topos** 是滿足以下條件的範疇：
1. 有有限極限（特別是終對象和纖維積）
2. 有餘積（對偶有限餘極限）
3. 是笛卡爾封閉的（有指數對象）
4. 有子對象分類器

---

## 2. Elementary Topos 測試

### 2.1 子對象分類器 (Subobject Classifier)

子對象分類器 $\Omega$ 是 Topos 中最核心的結構之一。

**數學定義**：子對象分類器是一個對象 $\Omega$，伴隨一個態射 $t: 1 \to \Omega$（真值選擇），使得對任何單態射 $S \hookrightarrow X$，存在唯一的特徵態射 $\chi_S: X \to \Omega$ 使得以下交換圖成立：

```
S ----→ 1
|        |
|        V
X ----→ Ω
```

**測試代碼分析**：
```python
def test_subobject_classifier(self):
    t = Topos()
    assert True in t.subobject_classifier
```
此測試驗證子對象分類器包含真值 `True`，這是布爾值在 Topos 中的推廣。

### 2.2 指數對象 (Exponential Object)

指數對象 $B^A$ 表示從 $A$ 到 $B$ 的所有態射的「集合」。

**測試驗證**：
```python
def test_has_exponentials(self):
    t = Topos()
    assert t.has_exponentials() is True

def test_is_cartesian_closed(self):
    t = Topos()
    assert t.is_cartesian_closed() is True
```

當 Topos 中所有指數對象都存在時，稱其為**笛卡爾封閉範疇**。這賦予了 Topos 类似集合範疇的函數空間概念。

### 2.3 冪對象 (Power Object)

冪對象 $P(X)$ 是指數對象的特殊情形 $P(X) = \Omega^X$，表示 $X$ 的所有子對象的「集合」。

```python
def test_power_object(self):
    t = Topos()
    result = t.power_object("X")
    assert result == "X"
```

---

## 3. 子對象分類器深入測試

### 3.1 單態射與滿態射

測試類 `TestMonomorphism` 和 `TestEpimorphism` 驗證了 Topos 中的基本態射：

```python
class TestMonomorphism:
    def test_creation(self):
        m = Monomorphism("A", "B", lambda x: x)
        assert m.source == "A"
        assert m.target == "B"

    def test_is_mono(self):
        m = Monomorphism("A", "B", lambda x: x)
        assert m.is_mono() is True
```

**數學背景**：
- **單態射 (Monomorphism)**：類似集合範疇中的單射，滿足 $f \circ g = f \circ h \Rightarrow g = h$
- **滿態射 (Epimorphism)**：類似集合範疇中的滿射

### 3.2 子對象

```python
def test_subobject(self):
    t = Topos()
    result = t.subobject("X")
    assert isinstance(result, list)
```

子對象是某個對象的單態射同構類，代表了對象的「子結構」。

---

## 4. Sheaf 在 Topos 中的測試

### 4.1 SheafTopos

Grothendieck Topos 是位址 (site) 上的層範疇。

```python
class TestSheafTopos:
    def test_creation(self):
        st = SheafTopos()
        assert st.space is None

    def test_creation_with_space(self):
        st = SheafTopos("space")
        assert st.space == "space"

    def test_is_grothendieck_topos(self):
        st = SheafTopos()
        assert st.is_grothendieck_topos() is True
```

**數學意義**：
- SheafTopos 是 Grothendieck topos 的實現
- 每個 Grothendieck topos 等價於某個拓撲空間上的層範疇
- `is_grothendieck_topos()` 返回 `True` 表示該 Topos 具有足夠的投射對象

### 4.2 Boolean Topos

布爾 Topos 是子對象分類器同構於 $1 + 1$ 的 Topos。

```python
class TestBooleanTopos:
    def test_is_boolean(self):
        bt = BooleanTopos()
        assert bt.is_boolean() is True

    def test_law_of_excluded_middle(self):
        bt = BooleanTopos()
        assert bt.law_of_excluded_middle() is True
```

**重要性質**：在布爾 Topos 中，排中律成立，即每個子對象要么為真要么為假。

---

## 5. Abel 範疇測試

### 5.1 基本結構

```python
class TestAbelianCategory:
    def test_zero_object(self):
        ac = AbelianCategory(["A"])
        assert ac.zero_object() == "A"

    def test_kernel(self):
        ac = AbelianCategory()
        k = ac.kernel(lambda x: x)
        assert isinstance(k, Monomorphism)

    def test_cokernel(self):
        ac = AbelianCategory()
        ck = ac.cokernel(lambda x: x)
        assert isinstance(ck, Epimorphism)
```

**Abel 範疇的定義**：一個預加法範疇滿足：
1. 有零對象
2. 有有限雙積
3. 所有核與餘核存在
4. 每個單態射都是核，所有滿態射都是餘核
5. 每個態射的像與餘像相等

### 5.2 核與餘核

- **核 (Kernel)**：態射 $f: A \to B$ 的核是滿足 $f \circ k = 0$ 的普遍對象
- **餘核 (Cokernel)**：餘核是核的對偶概念

```python
def test_universal_property(self):
    k = Kernel(lambda x: x, "ker")
    assert k.universal_property() is True
```

---

## 6. 函子測試

### 6.1 正合函子

```python
class TestExactFunctor:
    def test_is_exact(self):
        ef = ExactFunctor()
        assert ef.is_exact() is True

    def test_is_left_exact(self):
        ef = ExactFunctor()
        assert ef.is_left_exact() is True
```

**正合性層級**：

| 類型 | 保持的極限 |
|-----|----------|
| 左正合函子 | 有限極限（特別是核） |
| 右正合函子 | 有限餘極限（特別是餘核） |
| 正合函子 | 兩者都保持 |

### 6.2 左正合與右正合函子區分

```python
class TestLeftExactFunctor:
    def test_is_left_exact(self):
        lef = LeftExactFunctor()
        assert lef.is_left_exact() is True

    def test_is_right_exact(self):
        lef = LeftExactFunctor()
        assert lef.is_right_exact() is False

class TestRightExactFunctor:
    def test_is_left_exact(self):
        ref = RightExactFunctor()
        assert ref.is_left_exact() is False

    def test_is_right_exact(self):
        ref = RightExactFunctor()
        assert ref.is_right_exact() is True
```

---

## 7. 內射對象與投射對象

### 7.1 投射對象

```python
class TestProjectiveObject:
    def test_creation(self):
        p = ProjectiveObject("P")
        assert p.obj == "P"

    def test_is_projective(self):
        p = ProjectiveObject("P")
        assert p.is_projective() is True

    def test_project_cover(self):
        p = ProjectiveObject("P")
        result = p.projective_cover()
        assert isinstance(result, ProjectiveObject)
```

**投射對象定義**：對任何滿態射 $E \twoheadrightarrow B$ 和任何態射 $P \to B$，存在提升態射 $P \to E$ 使得圖交換。

### 7.2 內射對象

```python
class TestInjectiveObject:
    def test_creation(self):
        i = InjectiveObject("I")
        assert i.obj == "I"

    def test_is_injective(self):
        i = InjectiveObject("I")
        assert i.is_injective() is True

    def test_injective_envelope(self):
        i = InjectiveObject("I")
        result = i.injective_envelope()
        assert isinstance(result, InjectiveObject)
```

**內射對象定義**：對任何單態射 $A \hookrightarrow B$ 和任何態射 $A \to I$，存在擴展態射 $B \to I$ 使得圖交換。

---

## 8. 生成器與餘生成器

### 8.1 生成器

```python
class TestGenerator:
    def test_creation(self):
        g = Generator("G")
        assert g.obj == "G"

    def test_is_generator(self):
        g = Generator("G")
        assert g.is_generator() is True
```

生成器 $G$ 的條件：對任何兩個不同態射 $f, g: A \to B$，存在態射 $h: G \to A$ 使得 $f \circ h \neq g \circ h$。

### 8.2 餘生成器

```python
class TestCogenerator:
    def test_creation(self):
        c = Cogenerator("C")
        assert c.obj == "C"

    def test_is_cogenerator(self):
        c = Cogenerator("C")
        assert c.is_cogenerator() is True
```

餘生成器的對偶條件使用餘纖維積而非纖維積。

---

## 9. 正合序列

```python
class TestExactSequence:
    def test_creation(self):
        es = ExactSequence(["A", "B", "C"], [lambda x: x, lambda x: x])
        assert len(es.objects) == 3

    def test_is_exact_at_valid(self):
        es = ExactSequence(["A", "B", "C"], [lambda x: x, lambda x: x])
        assert es.is_exact_at(1) is True

    def test_is_exact_at_boundary(self):
        es = ExactSequence(["A", "B", "C"], [lambda x: x, lambda x: x])
        assert es.is_exact_at(0) is False
```

**正合性**：序列在對象 $B$ 處正合當且僅當 $\text{im}(f) = \text{ker}(g)$。

---

## 10. 測試覆蓋範圍總結

| 測試類 | 核心概念 |
|-------|---------|
| `TestTopos` | Elementary topos 基本性質 |
| `TestSheafTopos` | Grothendieck topos |
| `TestBooleanTopos` | 布爾 Topos 與排中律 |
| `TestAbelianCategory` | Abel 範疇結構 |
| `TestMonomorphism` / `TestEpimorphism` | 態射基本性質 |
| `TestProjectiveObject` / `TestInjectiveObject` | 內射/投射對象 |
| `TestGenerator` / `TestCogenerator` | 生成器結構 |
| `TestExactFunctor` | 函子正合性 |
| `TestKernel` / `TestCokernel` | 核與餘核 |
| `TestExactSequence` | 正合序列 |

---

## 附錄：Topos 理論要點

1. **Topos = 集合範疇的推廣**：Topos 提供了處理「集合」概念的不同視角
2. **邏輯解釋**：Topos 中的子對象分類器對應命題的真值
3. **幾何視角**：SheafTopos 連接了拓撲空間與範疇論
4. **集合論的替代**：Topos 可以作為集合論的基礎框架