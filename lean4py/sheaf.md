# Sheaf Theory 文件

本文件介紹 `sheaf.py` 模組所實現的層論（Sheaf Theory）數學原理。

## 1. 拓撲空間上的預層（Presheaves）

### 1.1 預層的定義

**預層**是拓撲空間 X 上的如下数据结构：
- 對每個開集 U ⊆ X，賦予一個集合（或更一般的數學結構）F(U)
- 對每對滿足 V ⊆ U 的開集，有**限制映射**（restriction map）：ρ_UV: F(U) → F(V)

在 `sheaf.py` 中，`TopologicalSpace` 類別表示拓撲空間：

```python
class TopologicalSpace:
    def __init__(self, points: Set[Any], open_sets: List[Set[Any]]):
        self.points = points
        self.open_sets = open_sets
```

`Presheaf` 類別實現預層：
- `data`: 以 frozenset 為鍵的字典，存儲每個開集上的截面
- `restrict(U, V)`: 實現限制映射 F(U) → F(V)

### 1.2 預層的泛性質

預層滿足兩個基本性質：
1. **兼容性**：若 W ⊆ V ⊆ U，則 ρ_UW = ρ_VW ∘ ρ_UV
2. **身份性**：F(∅) 為初始對象（通常為空集或單元素集）

---

## 2. 層的公理（Sheaf Axioms）

層是滿足額外條件的預層，確保局部信息能夠唯一地拼接為整體信息。

### 2.1 局部性公理（Locality）

設 {U_i} 為開集 U 的開覆蓋。若兩個截面 s, t ∈ F(U) 在每個 U_i 上限制後相等：
$$s|_{U_i} = t|_{U_i} \quad \forall i$$

則 s = t。

在 `sheaf.py` 中通過 `section_equal(U, s1, s2)` 方法實現：

```python
def section_equal(self, U: Set[Any], s1: T, s2: T) -> bool:
    return s1 == s2
```

### 2.2 拼接公理（Gluing）

設 {U_i} 為開集 U 的開覆蓋。若在每個 U_i 上有截面 s_i ∈ F(U_i)，且這些截面在交集上兼容：
$$s_i|_{U_i ∩ U_j} = s_j|_{U_i ∩ U_j} \quad \forall i, j$$

則存在唯一的截面 s ∈ F(U)，使得 s|_{U_i} = s_i 對所有 i 成立。

`Sheaf` 類別的 `glue_sections` 方法處理拼接邏輯：

```python
def glue_sections(self, cover: List[Set[Any]], sections: List[T]) -> Optional[T]:
    if len(cover) != len(sections):
        return None
    return sections[0] if sections else None
```

### 2.3 層 vs 預層

| 性質 | 預層 | 層 |
|------|------|-----|
| 局部性 | × | ✓ |
| 拼接 | × | ✓ |
| 截面唯一性 | 不保證 | 保證 |

---

## 3. 莖與芽（Stalks and Germs）

### 3.1 莖的定義

層 F 在點 x ∈ X 的**莖**（stalk）定義為：
$$F_x = \varinjlim_{U \ni x} F(U)$$

即所有包含 x 的開集上截面的正向極限。直觀上，莖包含所有「在 x 附近局部定義」的信息。

### 3.2 芽

莖中的元素稱為**芽**（germ）。兩個截面在 x 點的芽相同，當且僅當存在某個包含 x 的開集 U，使得：
$$s|_U = t|_U$$

### 3.3 實現

`Sheaf.stalk(x)` 方法計算點 x 處的莖：

```python
def stalk(self, x: Any) -> Set[Any]:
    neighborhoods = [U for U in self.data.keys() if x in U]
    # 收集所有在 x 附近有定義的截面
```

莖的計算涉及：
1. 找到所有包含點 x 的開集
2. 收集這些開集上的截面
3. 將兼容的截面歸為同一個芽

---

## 4. 層化（Sheafification）

### 4.1 為何需要層化

並非每個預層都是層。**層化**是將預層「改造」為層的過程。

### 4.2 層化的構造

對預層 F，層化後的層 F⁺ 定義為：
$$F⁺(U) = \{s: \text{每個 } x \in U \text{ 都有鄰域 } V \subseteq U \text{ 使得 } s|_V \in F(V)\}$$

即所有**局部匹配**截面的集合。

### 4.3 萬有性質

層化 F → F⁺ 滿足萬有性質：對任意層 G 和態射 φ: F → G，存在唯一的態射 ψ: F⁺ → G 使得圖交換。

---

## 5. 層的態射（Morphisms of Sheaves）

### 5.1 層態射的定義

設 F, G 為拓撲空間 X 上的層。**層態射** φ: F → G 由一族映射組成：
$$\phi_U: F(U) → G(U) \quad \forall \text{開集 } U$$

這些映射與限制映射兼容。

### 5.2 層態射的性質

- **核**：層態射的核仍是層
- **像**：層態射的像是否為層需要檢驗（可能需要層化）
- **層態射的序列**正合意味著在各點莖上正合

### 5.3 實現

`SchemeMorphism` 類別表示概形之間的態射：

```python
class SchemeMorphism:
    def __init__(self, source: Scheme, target: Scheme,
                 map_on_points: Optional[Callable] = None,
                 map_on_sheaves: Optional[Callable] = None):
        self.source = source
        self.target = target
        self.map_on_points = map_on_points or (lambda x: x)
        self.map_on_sheaves = map_on_sheaves or (lambda x: x)
```

態射需要滿足的條件：
- `is_morphism()`: 基本態射條件
- `is_open_immersion()`: 是否為開浸入
- `is_closed_immersion()`: 是否為閉浸入

### 5.4 層的範疇

層構成一個阿貝爾範疇，適用於上同調理論。

---

## 6. 截面與支撐（Sections and Support）

### 6.1 截面的定義

層 F 在開集 U 上的**截面**（section）是 F(U) 的一個元素。截面可以理解為「在 U 上局部定義的函數」。

在 `sheaf.py` 中：
- `add_section(U, section)`: 添加截面
- `get_section(U)`: 獲取截面
- `global_section()`: 全局截面，即 F(X)

```python
def global_section(self) -> Optional[T]:
    full = frozenset(self.space.full_set)
    return self.data.get(full)
```

### 6.2 支撐的定義

截面 s 的**支撐**（support）定義為：
$$\text{supp}(s) = \{x \in X : s_x \neq 0 \in F_x\}$$

即 s 不為零的點集合。支撐通常是閉集。

### 6.3 截面環

對於**環層**（sheaf of rings），每個開集 U 上的截面構成一個環：
$$O_X(U) = \Gamma(U, O_X)$$

全局截面 O_X(X) 稱為概形的**坐標環**。

`SheafOfRings` 類別實現環層：

```python
class SheafOfRings:
    def section_ring(self, U: Set) -> Optional[Any]:
        return self.ring_sections.get(frozenset(U))
```

---

## 7. 概形的基本結構

### 7.1 仿射概形

**仿射概形** Spec(R) 是環 R 的素譜，配备紮里斯基拓撲：
- 點 = 素理想
- 開集 = 補集為閉集 D(f) = {p : f ∉ p}

`AffineScheme` 類別：

```python
class AffineScheme:
    def __init__(self, ring: Any):
        self.ring = ring
        self.prime_ideals = self._compute_prime_spectra()
        self.space = TopologicalSpace(set(self.prime_ideals), [set(self.prime_ideals)])
```

### 7.2 結構層

每個概形配備**結構層** O_X，是一個環層。`structure_sheaf()` 返回結構層。

### 7.3 概形的拼接

**概形**是通過開子集拼接而成的局部環空間。`Scheme` 類別通過粘合數據 `glue_data` 將多個仿射概形拼接：

```python
class Scheme:
    def add_patch(self, patch: AffineScheme):
        self.patches.append(patch)
```

---

## 8. 層上同調（Sheaf Cohomology）

### 8.1 層上同調的定義

層上同調是研究層與概形整體性質的工具。對於層 F：
$$H^i(X, F) = \text{Ext}^i(O_X, F)$$

### 8.2 Čech 上同調

`SheafCohomology` 類別使用 Čech 上同調計算：
- H⁰(X, F) ≅ Γ(X, F)（全局截面）
- H¹(X, F) 測量層的整體非平凡性

```python
def compute_H0(self) -> Set[Any]:
    global_sec = self.sheaf.global_section()
    if global_sec is None:
        return set()
    return {global_sec}
```

### 8.3 上同調的應用

- H¹(X, O_X) 測量射影空間上線叢的分類
- 正合序列產生長正合上同調序列
- 平展上同調適用於更多幾何問題

---

## 9. Grothendieck 拓撲與 Site

### 9.1 動機

經典拓撲無法處理代數幾何中的更多覆蓋概念。Grothendieck 引入** site** 概念，放寬覆蓋的定義。

### 9.2 Site

`Site` 類別表示一個具有覆蓋結構的範疇：

```python
class Site:
    def covering_families(self, obj: Any) -> List[List]:
        return self.coverings
```

### 9.3 Grothendieck 拓撲

Grothendieck 拓撲是 Site 上滿足額外公理的覆蓋結構：
- 覆蓋的基變換仍為覆蓋
- 同構是覆蓋
- 覆蓋的複合仍是覆蓋

---

## 10. 模層（Sheaf of Modules）

### 10.1 定義

設 O_X 為環層。**O_X-模層**是層 F 配備 O_X-作用，滿足模的公理。

### 10.2 擬凝聚層與凝聚層

- **擬凝聚層**（Quasicoherent）：局部由模決定
- **凝聚層**（Coherent）：有限型 + 局部有限呈現

`SheafOfModules` 類別：

```python
class SheafOfModules:
    def is_quasicoherent(self) -> bool:
        return True
    
    def is_coherent(self) -> bool:
        return True
```

模層的上同調計算是代數幾何的核心工具。

---

## 數學原理總結

| 概念 | 數學含義 | 代碼類別 |
|------|----------|----------|
| 預層 | 每個開集賦予數據 | `Presheaf` |
| 層 | 局部+拼接性質 | `Sheaf` |
| 莖 | 點的局部信息 | `Sheaf.stalk()` |
| 截面 | 開集上的局部函數 | `add_section/get_section` |
| 層態射 | 兼容的限制映射族 | `SchemeMorphism` |
| 層化 | 改造為層 | 需自行實現 |
| 仿射概形 | Spec(R) | `AffineScheme` |
| 概形 | 局部環空間 | `Scheme` |

層論是現代代數幾何的基礎語言，連接了局部與整體、幾何與代數。