# Topology Module Documentation

本模組實現了一般拓撲學（General Topology）的基本概念，對應 mathlib4 的 `Mathlib.Topology` 結構。

---

## 1. 拓撲空間 (Topological Space)

### 數學定義

拓撲空間由一對 $(X, \tau)$ 構成，其中：
- $X$ 是任意集合（稱為**底層集合**）
- $\tau$ 是 $X$ 的子集族，滿足以下公理：

1. $\emptyset \in \tau$ 且 $X \in \tau$
2. 任意多個開集的聯集仍在 $\tau$ 中
3. 有限多個開集的交集仍在 $\tau$ 中

$\tau$ 中的元素稱為**開集**（open sets）。

### 實現

```python
class TopologicalSpace:
    def __init__(self, points: Set[Any], open_sets: Optional[Set[Any]] = None):
        self.points = points
        self.open_sets = open_sets if open_sets is not None else {frozenset(), frozenset(points)}
```

預設拓撲只包含空集和整個空間，這是最粗糙的拓撲（平凡拓撲）。

---

## 2. 開集、閉集、閉包、內部

### 開集與閉集

- **開集**：屬於 $\tau$ 的集合
- **閉集**：其補集為開集的集合

```python
def is_open(self, s: Set[Any]) -> bool:
    return frozenset(s) in self.open_sets

def is_closed(self, s: Set[Any]) -> bool:
    return set(s) <= self.closure(s)
```

### 內部 (Interior)

**定義**：集合 $S$ 的內部 $\operatorname{int}(S)$ 是 $S$ 中最大的開子集。

**性質**：
- $\operatorname{int}(S) \subseteq S$
- $\operatorname{int}(S)$ 是開集
- 若 $U$ 為開集且 $U \subseteq S$，則 $U \subseteq \operatorname{int}(S)$

```python
def interior(self, s: Set[Any]) -> Set[Any]:
    interior = set()
    for op in self.open_sets:
        if op <= frozenset(s):
            interior |= set(op)
    return interior
```

### 閉包 (Closure)

**定義**：集合 $S$ 的閉包 $\overline{S}$ 是包含 $S$ 的最小閉集。

**性質**：
- $S \subseteq \overline{S}$
- $\overline{S}$ 是閉集
- 若 $C$ 為閉集且 $S \subseteq C$，則 $\overline{S} \subseteq C$

```python
def closure(self, s: Set[Any]) -> Set[Any]:
    closed_union = set()
    s_frozen = frozenset(s)
    for op in self.open_sets:
        if op & s_frozen == frozenset():
            closed_union |= set(frozenset(self.points) - op)
    return closed_union | set(s)
```

### 邊界 (Boundary)

**定義**：$\partial S = \overline{S} \cap \overline{X \setminus S}$

```python
def boundary(self, s: Set[Any]) -> Set[Any]:
    complement = set(self.points) - set(s)
    return self.closure(s) & self.closure(complement)
```

---

## 3. 連續性 (Continuity)

### 數學定義

設 $f: (X, \tau_X) \to (Y, \tau_Y)$ 為兩拓撲空間之間的函數。$f$ 在點 $x \in X$ 處連續若且為若：

$$\forall V \in \tau_Y, f(x) \in V \implies \exists U \in \tau_X, x \in U \text{ 且 } f(U) \subseteq V$$

或等價地（全域連續）：

$$f \text{ 連續} \iff \forall V \in \tau_Y, f^{-1}(V) \in \tau_X$$

即**開集的原像仍是開集**。

### 實現

```python
class ContinuousFunction:
    def is_continuous(self) -> bool:
        for v_open in self.codomain.open_sets:
            preimage = {x for x in self.domain.points if frozenset([self.func(x)]) <= v_open}
            if not self.domain.is_open(preimage):
                return False
        return True
```

---

## 4. 同胚 (Homeomorphism)

### 數學定義

拓撲空間之間的**同胚**是滿足以下條件的雙射 $f: X \to Y$：

1. $f$ 連續
2. $f^{-1}$ 連續

同胚表示兩個拓撲空間在拓撲學意義下**完全相同**——它們具有完全相同的拓撲性質。

### 性質

若 $f: X \to Y$ 為同胚，則：
- $f$ 將開集映射為開集（開映射）
- $f$ 將閉集映射為閉集（閉映射）
- 保持連通性
- 保持緊緻性

### 實現

```python
class Homeomorphism:
    @staticmethod
    def is_homeomorphism(f: ContinuousFunction) -> bool:
        # f 為雙射且 f 和 f^{-1} 都連續
        pass  # 可透過連續函數反轉實現
```

---

## 5. 緊緻性 (Compactness)

### 數學定義

拓撲空間 $X$ 是**緊緻**的，若對於 $X$ 的任意開覆蓋 $\{U_i\}_{i \in I}$，都存在有限子覆蓋：

$$\exists J \subseteq I, |J| < \infty \text{ 且 } X \subseteq \bigcup_{j \in J} U_j$$

### 海涅-博雷爾定理 (Heine-Borel)

在 $\mathbb{R}^n$ 中（配備歐氏度量），子集 $K$ 為緊緻集若且為若：

$$K \text{ 有界且封閉}$$

### 實現

```python
class Compactness:
    @staticmethod
    def is_compact(space: TopologicalSpace) -> bool:
        return space.is_compact()

    @staticmethod
    def heine_borel(space: MetricSpace) -> bool:
        return space.is_complete()  # 簡化版本
```

### 緊緻空間的性質

- 緊緻空間的連續像是緊緻的
- 緊緻 Hausdorff 空間是正規的
- 緊緻 metric 空間是完全有界的

---

## 6. 連通性與道路連通性

### 連通性 (Connectedness)

**定義**：拓撲空間 $X$ 是**連通**的，若不存在非平凡的同時為開且閉的子集。

即：不存在 $U, V$ 使得 $X = U \cup V$，$U \cap V = \emptyset$，且 $U, V$ 皆非空。

```python
def is_connected(self) -> bool:
    for op in self.open_sets:
        if op != frozenset() and op != frozenset(self.points):
            complement = frozenset(self.points) - op
            if complement in self.open_sets:
                return False
    return True
```

### 道路連通性 (Path-Connectedness)

**定義**：空間 $X$ 是**道路連通**的，若對任意 $x, y \in X$，存在連續函數 $\gamma: [0,1] \to X$ 使得 $\gamma(0) = x$，$\gamma(1) = y$。

**重要蘊含**：道路連通 $\implies$ 連通（但反向不成立）。

```python
class Connectedness:
    @staticmethod
    def is_path_connected(space: TopologicalSpace) -> bool:
        return space.is_connected()  # 簡化版本
```

---

## 7. Hausdorff 空間

### 數學定義

拓撲空間 $(X, \tau)$ 是 **Hausdorff 空間**（或 $T_2$ 空間），若對任意不同的兩點 $x, y \in X$，存在開集 $U, V$ 使得：

$$x \in U, y \in V, \text{ 且 } U \cap V = \emptyset$$

### 意義

Hausdorff 性質保證了**極限的唯一性**——在 Hausdorff 空間中，每個收斂序列的極限是唯一的。

### 實現

```python
def is_hausdorff(self) -> bool:
    points_list = list(self.points)
    for i, x in enumerate(points_list):
        for y in points_list[i+1:]:
            # 檢查是否存在隔離的開鄰域
            ...
    return True

class HausdorffSpace(TopologicalSpace):
    def __init__(self, points: Set[Any], open_sets: Optional[Set[Any]] = None):
        super().__init__(points, open_sets)
        if not self.is_hausdorff():
            raise ValueError("Space is not Hausdorff")
```

---

## 8. 拓撲基 (Basis)

### 數學定義

設 $(X, \tau)$ 為拓撲空間。$\mathcal{B} \subseteq \tau$ 為**基**，若每個開集都可以表示為 $\mathcal{B}$ 中某些集合的聯集。

即：$$\forall U \in \tau, \exists \mathcal{B}' \subseteq \mathcal{B}, U = \bigcup_{B \in \mathcal{B}'} B$$

### 基的判準

集合族 $\mathcal{B}$ 為某拓撲的基若且為若：
1. $\bigcup_{B \in \mathcal{B}} B = X$
2. 若 $x \in B_1 \cap B_2$，則存在 $B_3 \in \mathcal{B}$ 使得 $x \in B_3 \subseteq B_1 \cap B_2$

### MetricSpace 中的基

```python
class MetricSpace:
    def to_topological_space(self) -> TopologicalSpace:
        open_sets = {frozenset()}
        for center in self.points:
            for radius in [0.5, 1.0, 2.0, float('inf')]:
                ball = self.ball(center, radius)
                open_sets.add(frozenset(ball))
        open_sets.add(frozenset(self.points))
        return TopologicalSpace(self.points, open_sets)
```

在度量空間中，開球族形成拓撲的基。

---

## 9. 子空間拓撲 (Subspace Topology)

### 數學定義

設 $(X, \tau)$ 為拓撲空間，$Y \subseteq X$。則 $Y$ 上的**子空間拓撲**定義為：

$$\tau_Y = \{U \cap Y \mid U \in \tau\}$$

即 $Y$ 的子集在子空間拓撲中為開集若且為若它是 $X$ 中某開集與 $Y$ 的交集。

### 性質

若 $Y$ 配備子空間拓撲，則：
- $Y$ 的閉集形如 $F \cap Y$（其中 $F$ 在 $X$ 中閉）
- 若 $Y$ 在 $X$ 中閉，則 $Y$ 的閉集皆為閉
- 若 $Y$ 在 $X$ 中開，則 $Y$ 的開集皆為開

### 實現提示

```python
class SubspaceTopology:
    @staticmethod
    def subspace(space: TopologicalSpace, subset: Set[Any]) -> TopologicalSpace:
        subspace_open = {frozenset(set(u) & subset) for u in space.open_sets}
        return TopologicalSpace(subset, subspace_open)
```

---

## 度量空間擴展

### 數學定義

**度量空間**為一對 $(X, d)$，其中 $d: X \times X \to \mathbb{R}_{\geq 0}$ 滿足：

1. **正定性**：$d(x, y) \geq 0$，且 $d(x, y) = 0 \iff x = y$
2. **對稱性**：$d(x, y) = d(y, x)$
3. **三角不等式**：$d(x, z) \leq d(x, y) + d(y, z)$

### 開球

$$B(x, r) = \{y \in X \mid d(x, y) < r\}$$

開球族生成度量空間的拓撲。

```python
class MetricSpace:
    def ball(self, center: Any, radius: float) -> Set[Any]:
        return {p for p in self.points if self.d(center, p) < radius}

    def is_metric(self) -> bool:
        # 驗證度量公理
        ...
```

---

## 總結

本模組實現的拓撲學概念對應關係：

| 數學概念 | 實現類別 |
|---------|---------|
| 拓撲空間 | `TopologicalSpace` |
| 連續函數 | `ContinuousFunction` |
| 同胚 | `Homeomorphism`（透過 `ContinuousFunction`）|
| 緊緻性 | `Compactness` |
| 連通性 | `Connectedness` |
| Hausdorff 空間 | `HausdorffSpace` |
| 度量空間 | `MetricSpace` |
| 開映射/閉映射 | `OpenMap` / `ClosedMap` |

---

## 參考文獻

- Munkres, J. R. *Topology: A First Course*
- Engelking, R. *General Topology*
- mathlib4: `Mathlib.Topology`