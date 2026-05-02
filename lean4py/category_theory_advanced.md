# Category Theory Advanced - 范畴论进阶

> 本文档解释 lean4py.category_theory_advanced 模块背后的数学原理。

## 1. 范畴 (Category)

**范畴** 由以下组成：
- **对象 (Objects)**: 记作 `Ob(C)`，可以是任何数学对象（集合、群、拓扑空间等）
- **态射 (Morphisms)**: 记作 `Hom_C(X, Y)`，表示从对象 X 到对象 Y 的箭头
- **复合运算**: 若 `f: X → Y` 和 `g: Y → Z`，则 `g ∘ f: X → Z`
- **单位态射**: 每个对象 X 都有身份态射 `id_X: X → X`

**范畴公理**：
1. **结合律**: `(h ∘ g) ∘ f = h ∘ (g ∘ f)`
2. **单位律**: `f ∘ id_X = f = id_Y ∘ f`

```python
# 示例：Set 范畴
# 对象：所有集合
# 态射：集合间的函数
# 复合：函数的复合
# 单位：恒等函数
```

---

## 2. 函子 (Functor)

**函子** 是范畴之间的结构保持映射 `F: C → D`。

**函子的两个映射**：
1. **对象映射**: `F: Ob(C) → Ob(D)`
2. **态射映射**: `F: Hom_C(X, Y) → Hom_D(FX, FY)`

**结构保持**：
- `F(id_X) = id_{FX}`
- `F(g ∘ f) = F(g) ∘ F(f)`

**协变函子 vs 反变函子**：
- **协变 (Covariant)**: 方向保持 `f: X → Y ⇒ F(f): F(X) → F(Y)`
- **反变 (Contravariant)**: 方向反转 `f: X → Y ⇒ F(f): F(Y) → F(X)`

---

## 3. 自然变换 (Natural Transformation)

**自然变换** 是函子之间的"映射" `η: F ⇒ G`。

对于每个对象 `X`，有**自然成分** `η_X: F(X) → G(X)`，使得对于任意态射 `f: X → Y`，下图可交换：

```
F(X) ---η_X---> G(X)
|               |
| F(f)         | G(f)
v               v
F(Y) ---η_Y---> G(Y)
```

---

## 4. 万有性质与万有元素 (Universal Properties & Elements)

### 万有性质

**万有性质** 描述对象通过泛映射性(unique mapping)来定义：

> 对象 U 是"关于性质 P 的万有对象"，当且仅当对于每个对象 X，存在唯一的态射 `X → U` 满足某性质。

### 万有元素

**万有元素** 是从终结对象到函子的唯一态射对应的元素：

若 `U` 是余极限且 `1` 是终对象，则万有元素是唯一态射 `1 → U` 选择的元素。

---

## 5. 极限与余极限 (Limits & Colimits)

### 极限 (Limit)

**极限** 是函子的特定余极限（余极限的对偶概念）。

**典范构造**：

| 构造 | 定义 | 泛性质 |
|------|------|--------|
| **积 (Product)** | `∏ X_i` | 存在唯一的 `π_i: ∏X_i → X_i`，使得对任意 `Y` 和 `f_i: Y → X_i`，存在唯一的 `u: Y → ∏X_i` |
| **等化子 (Equalizer)** | `eq(f, g)` | 使得 `f ∘ e = g ∘ e` 的对象 |
| **拉回 (Pullback)** | `X ×_Z Y` | 使得下图可交换的 `P` |

```
    X
   / \
  /   \
 f     \ (唯一)
  \   /
   \ /
    Z
```

### 余极限 (Colimit)

**余极限** 是极限的对偶（箭头反向）。

| 构造 | 定义 | 泛性质 |
|------|------|--------|
| **余积 (Coproduct)** | `∐ X_i` | 存在唯一的 `ι_i: X_i → ∐X_i`，使得对任意 `Y` 和 `f_i: X_i → Y`，存在唯一的 `u: ∐X_i → Y` |
| **余等化子 (Coequalizer)** | `coeq(f, g)` | 使得 `e ∘ f = e ∘ g` 的对象 |
| **推出 (Pushout)** | `X +_Z Y` | 拉回的对偶 |

---

## 6. 伴随 (Adjunction)

**伴随** 是范畴论中最重要的概念之一。

**定义**：函子 `L: C → D` 和 `R: D → C` 构成伴随 `L ⊣ R`，当且仅当存在自然同构：

```
Hom_D(LX, Y) ≅ Hom_C(X, RY)
```

**单位与余单位**：
- **单位 (Unit)**: `η: Id_C → R ∘ L`
- **余单位 (Counit)**: `ε: L ∘ R → Id_D`

**伴随的等价条件**：
1. 通用映射性质
2. 单位的每个组件是余极限的万有态射
3. 余单位的每个组件是极限的万有态射

```python
# 在 category_theory_advanced.py 中：
AdjointFunctor.is_adjoint(F, G, category_X, category_Y)
# 检查 Hom(LX, Y) ≅ Hom(X, RY)
```

---

## 7. Yoneda 引理 (Yoneda Lemma)

**Yoneda 引理** 是范畴论的基本结果。

**陈述**：对于任意协变函子 `F: C → Set`，任意对象 `X`：

```
Nat(Hom_C(X, -), F) ≅ F(X)
```

**Yoneda 嵌入**：
- 函子 `y: C^op → Set` 定义为 `y(X) = Hom_C(X, -)`
- `y` 是忠实且满的嵌入

**推论**：
- `Nat(Hom_C(X, -), Hom_C(Y, -)) ≅ Hom_C(Y, X)`
- 对象由其表示的函子唯一决定

```python
# 在 category_theory_advanced.py 中：
YonedaLemma.embedding(category, obj)    # y(X) = Hom(X, -)
YonedaLemma.isomorphism(F, X)          # Nat(Hom(X,-), F) ≅ F(X)
```

---

## 8. 单态、满态、同构 (Monics, Epics, Isomorphisms)

### 单态 (Monic)

态射 `m: X → Y` 是**单态**，当对于任意 `f, g: Z → X`：

```
m ∘ f = m ∘ g  ⇒  f = g
```

在 **Set** 中，单态恰好是**内射函数**。

### 满态 (Epic)

态射 `e: X → Y` 是**满态**，当对于任意 `f, g: Y → Z`：

```
f ∘ e = g ∘ e  ⇒  f = g
```

在 **Set** 中，满态恰好是**满射函数**。

### 同构 (Isomorphism)

态射 `f: X → Y` 是**同构**，当存在逆态射 `g: Y → X` 使得：

```
g ∘ f = id_X  且  f ∘ g = id_Y
```

---

## 9. 初始对象与终止对象 (Initial & Terminal Objects)

### 初始对象 (Initial Object)

对象 `I` 是**初始对象**，当对于每个对象 `X`，存在唯一的态射：

```
I → X
```

在 **Set** 中，空集是初始对象。

### 终止对象 (Terminal Object)

对象 `T` 是**终止对象**，当对于每个对象 `X`，存在唯一的态射：

```
X → T
```

在 **Set** 中，单元集 `{*}` 是终止对象。

### 零对象 (Zero Object)

既是初始又是终止的对象称为**零对象**，记作 `0`。

---

## 补充：幺半群与余幺半群 (Monad & Comonad)

### Monad (单子/三联)

**Monad** 由以下组成：
- 函子 `T: C → C`
- 单位 `η: Id ⇒ T`
- 乘法 `μ: T² ⇒ T`

**Monad 律**：
1. `μ ∘ Tμ = μ ∘ μT` (结合律)
2. `μ ∘ Tη = μ ∘ ηT = id` (单位律)

```python
# 在 category_theory_advanced.py 中：
Monad(functor, unit, multiplication)
```

### Comonad (余单子)

**Comonad** 由以下组成：
- 函子 `G: C → C`
- 余单位 `ε: G ⇒ Id`
- 余乘法 `δ: G ⇒ G²`

```python
# 在 category_theory_advanced.py 中：
Comonad(functor, counit, comultiplication)
```

---

## 模块 API 参考

| 类 | 主要方法 | 描述 |
|-----|---------|------|
| `AdjointFunctor` | `is_adjoint()`, `unit()`, `counit()` | 检查伴随关系，获取单位/余单位 |
| `Limit` | `product()`, `equalizer()`, `pullback()` | 构造各种极限 |
| `Colimit` | `coproduct()`, `coequalizer()`, `pushout()` | 构造各种余极限 |
| `YonedaLemma` | `embedding()`, `isomorphism()` | Yoneda 嵌入与同构 |
| `Monad` | `is_monad()` | 检查 Monad 律 |
| `Comonad` | `is_comonad()` | 检查 Comonad 律 |