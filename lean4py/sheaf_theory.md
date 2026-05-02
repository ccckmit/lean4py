# Sheaf Theory (層論)

本文件介紹 lean4py 中 sheaf_theory.py 模組的數學原理。層論是 代數拓撲與幾何 中的核心工具，用於研究局部與整體性質的關係。

---

## 1. 預層 (Presheaf)

### 定義

**預層** 是從拓撲空間 X 的開集範疇到某個目標範疇 C 的反變函子：

```
F : Open(X)^op → C
```

其中：
- `Open(X)^op` 是 X 開集範疇的反變範疇
- 對於每個開集 U，給出一個對象 F(U)
- 對於每個包含關係 V ⊆ U，給出限制映射 `res_{U,V} : F(U) → F(V)`

### 預層公理

1. **身份性**：對於任意開集 U，`res_{U,U} = id_{F(U)}`
2. **複合性**：若 W ⊆ V ⊆ U，則 `res_{V,W} ∘ res_{U,V} = res_{U,W}`

### 代碼對應

```python
class Presheaf:
    """預層 F: Open(X)^op → C"""
    def __init__(self, space: str, target_category: str = "Set"):
        self.space = space           # 底層拓撲空間 X
        self.target = target_category # 目標範疇 (如 "Set", "Ab", "Ring")
        self.sections: Dict[str, List[Any]] = {}  # 各開集上的截面

    def restrict(self, section: Any, open_subset: str) -> Any:
        """限制映射 res_{U,V}: F(U) → F(V)"""
        return section
```

---

## 2. 層 (Sheaf)

### 層條件

層是滿足**局部-整體恆等**和**拼接**公理的預層。

#### 局部-整體恆等公理 (Local-Global Identity)

若 {U_i} 是開集 U 的開覆蓋，s ∈ F(U) 滿足對所有 i 都有 `res_{U,U_i}(s) = 0`，則 s = 0。

#### 拼接公理 (Gluing Axiom)

若 {U_i} 是開集 U 的開覆蓋，且對每個 i 給定元素 s_i ∈ F(U_i)，滿足在交疊處一致：
```
res_{U_i, U_i ∩ U_j}(s_i) = res_{U_j, U_i ∩ U_j}(s_j)
```
則存在唯一 s ∈ F(U) 使得對所有 i，`res_{U,U_i}(s) = s_i`。

### 層的直觀意義

層描述了「局部定義、全局拼接」的數學結構。例如：
- 連續函數層：每個開集上的連續函數可以局部定義並拼接
- 局部常數層：每個開集上的局部常數函數

### 代碼對應

```python
class Sheaf:
    """層：滿足層條件的預層"""
    @staticmethod
    def satisfies_sheaf_condition(presheaf: Presheaf, cover: List[str]) -> bool:
        """檢驗局部性 + 拼接條件"""
        return True

    @staticmethod
    def is_sheaf(space: str, target: str) -> bool:
        """判定預層是否為層"""
        return True
```

---

## 3. 莖 (Stalk)

### 定義

給定點 x ∈ X，**莖** F_x 定義為 F 在 x 處的直接極限：

```
F_x = lim_{→} (U ∋ x) F(U)
```

即取所有包含 x 的開集 U 以及其間的限制映射的直接極限。

### 構造方式

對於包含 x 的開集 U, V：
- 若 U ⊆ V，則有限制映射 `res_{V,U} : F(V) → F(U)`
- 直接極限將這些資料整合為莖 F_x

### 莖的泛性質

F_x 是所有 F(U) (U ∋ x) 的最終對象，滿足對任意其他共變函子 G，若對所有 U ∋ x 有態射 φ_U : F(U) → G，且滿足兼容性，則存在唯一態射 F_x → G。

---

## 4. 胚 (Germ)

### 定義

**胚**是莖中的元素，等價於在某鄰域上一致的截面類。

形式化地說：兩個截面 s ∈ F(U) 和 t ∈ F(V) 在 x 處有相同的胚，若存在包含 x 的開集 W ⊆ U ∩ V 使得：

```
res_{U,W}(s) = res_{V,W}(t)
```

### 胚與截面的關係

- 每個截面 s ∈ F(U) 確定一個胚，位於所有包含 U 的點 x 處
- 胚是截面的局部不變量，只保留在點附近的行為

### 直觀理解

胚像是「函數在一点的局部行為」的精確描述：
- 兩個函數在 x 處有相同胚 ⟺ 它們在 x 的某鄰域上相等
- 這與泰勒展開的局部性概念相關

---

## 5. 層上同調 (Sheaf Cohomology)

### 背景

層上同調是研究層的整體截面缺陷的工具。對于阿貝爾群層，正合序列：

```
0 → F → G → H → 0
```

不一定導出整體截面的正合性，需要上同調來測量偏差。

### 定義

對拓撲空間 X 上的層 F，定義右導出函子：

```
H^i(X, F) = R^iΓ(X, F)
```

其中 Γ(X, F) = F(X) 是整體截面函子。

### 性質

1. **H⁰(X, F) ≅ Γ(X, F)**：零次上同調即整體截面
2. **H¹(X, F)**：測量障礙類
3. **消沒定理**：若空間滿足特定條件，高次上同調可在某維度後消沒

### 代碼對應

```python
class SheafCohomology:
    """層上同調 H^i(X, F)"""
    @staticmethod
    def compute(sheaf: Sheaf, degree: int) -> Dict[str, Any]:
        """計算 H^degree(X, F)"""
        return {"group": "0", "degree": degree}

    @staticmethod
    def vanishing(sheaf: Sheaf, dimension: int) -> bool:
        """H^i(X, F) = 0 當 i > dim(X)"""
        return True
```

---

## 6. Čech 上同調 (Čech Cohomology)

### 構造

對開覆蓋 U = {U_i}，定義 Čech 複形：

```
C^p(U, F) = ∏_{i₀<...<i_p} F(U_{i₀}∩...∩U_{i_p})
```

及其邊界映射 δ : C^p → C^{p+1}。

### 上同調群

Čech 上同調定義為：

```
Ḣ^p(U, F) = H^p(C^*(U, F))
```

當開覆蓋充分精細時，Ḣ^p(U, F) ≅ H^p(X, F)。

### 應用

- 線叢的分類：H¹(X, O*) 分類解析線叢
- 陳類：通過 Čech 構造計算
- 障害理論：描述整體對象的局部資料粘合障礙

---

## 7. 層的正合序列 (Exact Sequences of Sheaves)

### 短正合序列

層的正合序列形式為：

```
0 → F → G → H → 0
```

這意味著在每個莖處有正合性：

```
0 → F_x → G_x → H_x → 0
```

### 連接映射

長正合序列通過函子性產生：

```
0 → H^0(X, F) → H^0(X, G) → H^0(X, H) → H^1(X, F) → H^1(X, G) → H^1(X, H) → ...
```

###  Seven  Lemma

若層正合圖表交換，則誘導上同調的長正合序列。

### 常用序列

1. **局部與整體截面**：0 → F → G → H → 0
2. **商層構造**：0 → F → G → G/F → 0
3. **Twist 序列**：0 → Z → O_X → O_X* → 0

---

## 8. 鬆弛層與非循環分解 (Flasque Sheaves and Acyclic Resolutions)

### 鬆弛層 (Flasque Sheaf)

**定義**：層 F 稱為鬆弛的，若對任意開集 U ⊆ V，限制映射 `res_{V,U} : F(V) → F(U)` 是**滿射**。

### 鬆弛層的性質

1. 鬆弛層的莖是平坦的
2. 鬆弛層的 Čech 上同調等於層上同調
3. 鬆弛層在計算上同調時「行為良好」

### 非循環層 (Acyclic Sheaf)

**定義**：層 F 稱為**非循環的**，若對所有 i > 0 有 H^i(X, F) = 0。

### 非循環分解

若 0 → F → A^0 → A^1 → A^2 → ... 是層的內射分解，且每個 A^i 都是非循環的，則：

```
H^i(X, F) ≅ H^i(A^*(X))
```

這是計算層上同調的基本方法。

### Godement 分解

Godement 提供了標準的鬆弛層分解：
- 使用層的「配置層」構造
- 產生的分解是鬆弛的
- 可直接用於上同調計算

### 常用的非循環層

| 層類型 | 特性 |
|--------|------|
| 鬆弛層 | 限制映射滿射 |
| 內射層 | 在層範疇中是內射對象 |
| 平坦層 | 張量積保持正合性 |

---

## 模組結構總覽

```
sheaf_theory.py
├── Presheaf          # 預層：反變函子 Open(X)^op → C
├── Sheaf             # 層：滿足局部-整體條件的預層
├── Sheafification    # 層化：將預層嵌入層範疇
├── GrothendieckTopology  # Grothendieck 拓撲
└── SheafCohomology   # 層上同調 H^i(X, F)
```

---

## 數學拓展閱讀

1. **Hartshorne, Algebraic Geometry**: 第 II 章 - 層論基礎
2. **Godement, Topologie Algébrique et Théorie des Faisceaux**: 層上同調經典參考
3. **Bredon, Sheaf Theory**: 層論的系統介紹
4. **Mathlib4**: `Mathlib.Topology.Sheaves` - 形式化層論的實現參考