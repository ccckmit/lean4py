# 2-范帱测试文档 (test_two_category.py)

## 概述

本测试文件验证 `lean4py.two_category` 模块中关于 2-范帱（2-category）及相关数学结构的实现。2-范帱是范畴论中高阶范畴的基本概念，除了对象和态射外，还包含 2-态射作为态射之间的态射。

---

## 1. 测试所验证的 2-范帱性质

### 1.1 基本结构 (TestTwoCategory)

`TwoCategory` 类实现了 2-范帱的基本结构，包含三层结构：

- **对象 (objects)**：2-范帱中的 0-细胞
- **1-态射 (one_morphisms)**：对象之间的态射
- **2-态射 (two_morphisms)**：1-态射之间的态射

测试验证了：
- `test_add_object`：对象的添加
- `test_add_one_morphism`：1-态射的添加及其所在 hom-集合
- `test_hom_two`：获取两个 1-态射之间的 2-态射集合
- `test_interchange_law`：交换律成立

### 1.2 交换律 (Interchange Law)

2-范帱中垂直合成与水平合成满足**交换律**：

```
(α · β) ⋆ (γ · δ) = (α ⋆ γ) · (β ⋆ δ)
```

这确保了两种合成方式的相容性，是 2-范帱的核心公理之一。

---

## 2. 2-范帱结构测试

### 2.1 Cat（范畴的范畴）

`Cat` 类表示范畴的范畴，是 2-范帱的重要例子：

- **对象**：小范畴
- **1-态射**：函子 (Functor)
- **2-态射**：自然变换 (Natural Transformation)

测试 `test_functor_category` 验证了**函子范畴** (Functor Category) 的构造：
- 给定源范畴 C 和目标范畴 D
- `FunctorCategory("C", "D")` 表示从 C 到 D 的所有函子构成的范畴

### 2.2 DoubleCategory（双范帱）

`DoubleCategory` 是一种特殊的 2-维结构，其中：

- 对象同时具有水平和垂直两个方向的态射
- **胞腔 (cells)**：具有四个边界（源对象、目标对象、源态射、目标态射）

测试验证了 `source_and_target("cell")` 返回长度为 4 的元组，对应四个边界。

---

## 3. 2-态射测试 (TestTwoMorphism)

### 3.1 TwoMorphism 的结构

2-态射是连接两个平行 1-态射的态射：

```
f ⇒ g  (source: f, target: g)
```

测试验证了：
- `test_creation`：2-态射由源态射、目标态射和数据构成
- `test_source_morphism` / `test_target_morphism`：获取源/目标 1-态射
- `test_is_invertible`：判断 2-态射是否可逆

### 3.2 可逆性

在 2-范帱中，2-态射可以是可逆的（等价），这定义了同伦等价等重要概念。

---

## 4. 合成测试

### 4.1 垂直合成与水平合成

`TestTwoCategory` 中的合成测试：

- `test_vertical_composition`：垂直合成 α · β
- `test_horizontal_composition`：水平合成 f ⋆ g

**垂直合成**：沿 2-态射的方向合成
```
α: f ⇒ g
β: g ⇒ h
─────────
β · α: f ⇒ h
```

**水平合成**：沿 1-态射的方向合成
```
f: A → B
g: B → C
─────────
g ○ f: A → C
```

### 4.2 Bicategory 中的合成

`Bicategory`（弱 2-范帱）测试了更复杂的合成结构：

- `test_associator`：结合子 α_{f,g,h}： (f ○ g) ○ h ⇒ f ○ (g ○ h)
- `test_left_unitor` / `test_right_unitor`：左/右单位子

#### 五边形恒等式 (Pentagon Identity)

验证结合子的兼容性：

```
((f ○ g) ○ h) ○ k  --α-->  (f ○ g) ○ (h ○ k)
   |                        |
   α                    α
   v                        v
f ○ (g ○ h) ○ k  --α-->  f ○ (h ○ (h ○ k))
```

#### 三角形恒等式 (Triangle Identity)

验证单位子与结合子的兼容性：

```
(id ○ f) ○ g  --α-->  id ○ (f ○ g)
    |                  |
  λ                  ρ
    v                  v
      f  ==============  f
```

---

## 5. 伴随与 Kan 扩张

### 5.1 伴随 (AdjunctionIn2Category)

伴随是 2-范帱中的重要结构：

```
L ⊣ R  (L 是左伴随，R 是右伴随)
```

伴随由单位 η: Id ⇒ R ○ L 和余单位 ε: L ○ R ⇒ Id 给出。

测试验证了：
- `test_triangle_identities`：三角形恒等式
  - R(ε) ○ ηR = id_R
  - εL ○ L(η) = id_L
- `test_mate`：伴随的伴随（mate）对应

### 5.2 Kan 扩张 (KanExtension2Category)

Kan 扩张是函子在范畴间的一种"最佳近似"：

- **左 Kan 扩张** Lan_K(F)：沿 K 将 F 左推出
- **右 Kan 扩张** Ran_K(F)：沿 K 将 F 右推出

测试验证了：
- `test_left_kan_extension`：返回包含 "Lan" 的结果
- `test_right_kan_extension`：返回包含 "Ran" 的结果
- `test_universal_property`：万有性质成立

---

## 6. 函子与严格 2-范帱

### 6.1 Lax Functor（宽松函子）

`LaxFunctor` 表示弱 2-函子，保持单位但仅要求合成不等式而非等式：

- F(id_X) ⇒ id_{F(X)}（可能不相等）
- F(g) ○ F(f) ⇒ F(g ○ f)（可能不相等）

测试验证了：
- `test_on_objects` / `test_on_morphisms` / `test_on_2morphisms`：对象、态射、2-态射的映射
- `test_preserves_composition`：合成保持性质

### 6.2 Strict 2Category（严格 2-范帱）

`Strict2Category` 严格满足所有 2-范帱公理：

- **严格结合性**：所有合成都是严格等式
- **严格单性**：单位态射严格满足单位律

测试验证了：
- `test_strict_associativity`：严格结合律
- `test_strict_unitality`：严格单性

---

## 7. 测试类列表

| 测试类 | 测试内容 |
|--------|----------|
| `TestTwoCategory` | 基本 2-范帱结构、垂直/水平合成、交换律 |
| `TestCat` | 范畴的范畴、函子范畴 |
| `TestFunctorCategory` | 函子范畴的维数 |
| `TestDoubleCategory` | 双范帱、胞腔的边界 |
| `TestBicategory` | 弱 2-范帱、结合子、单位子、恒等式 |
| `TestTwoMorphism` | 2-态射的结构与可逆性 |
| `TestAdjunctionIn2Category` | 伴随、三角恒等式、mate |
| `TestKanExtension2Category` | Kan 扩张、万有性质 |
| `TestLaxFunctor` | 宽松函子、合成保持 |
| `TestStrict2Category` | 严格 2-范帱 |

---

## 8. 数学意义

这些测试覆盖了 2-范帱理论的核心概念：

1. **层次结构**：对象 → 1-态射 → 2-态射的三层结构
2. **合成兼容性**：垂直/水平合成的交换律
3. **弱与严格**：Bicategory（弱）vs Strict2Category（严格）
4. **伴随理论**：伴随的三角形恒等式和 mate
5. **极限与余极限**：Kan 扩张作为函子的最佳近似
6. **函子范畴**：范畴本身构成范畴（Cat）