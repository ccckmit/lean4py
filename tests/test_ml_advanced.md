# 高级机器学习算法测试文档

本文档说明 `test_ml_advanced.py` 中测试用例的数学原理。

## 1. 测试概述

本测试文件验证以下机器学习算法的核心功能：

- **线性 SVM（支持向量机）**：使用铰链损失函数和次梯度下降法
- **决策树**：基于 CART 算法的分类树

## 2. SVM 测试 (TestSVMLinear)

### 2.1 数学原理

线性 SVM 的目标是找到一个最优超平面 `w·x + b = 0` 来分隔两类数据。

**目标函数**：
$$\min_{w,b} \frac{1}{2}\|w\|^2 + C \sum_{i=1}^{n} \max(0, 1 - y_i(w·x_i + b))$$

其中：
- 第一项 $\frac{1}{2}\|w\|^2$ 是正则化项，控制模型复杂度
- 第二项是铰链损失 (hinge loss)，当样本正确分类且间隔大于 1 时损失为 0
- $C$（代码中为 `lambda_reg`）控制两项的权衡

**次梯度下降**：
代码实现中使用次梯度下降法更新权重。当 $y_i(w·x_i + b) < 1$ 时：
$$\nabla_w L = -y_i \cdot x_i + \lambda \cdot w$$

### 2.2 测试用例说明

| 测试名称 | 验证内容 | 数学意义 |
|---------|---------|---------|
| `test_separable_data` | 可分数据上的权重返回 | 验证算法收敛，返回 m+1 维权向量（含偏置）|
| `test_predict_separable` | 预测功能正确性 | 验证 $\text{sign}(w·x + b)$ 决策边界正确 |
| `test_empty_data` | 空数据处理 | 边界条件：n=0 时返回空列表 |
| `test_regularization` | 正则化参数接受 | 验证不同 $\lambda$ 值不影响输出维度 |

## 3. 决策树测试 (TestDecisionTree)

### 3.1 数学原理

决策树采用 CART (Classification and Regression Tree) 算法，通过递归二分特征空间来构建。

**基尼不纯度 (Gini Impurity)**：
$$Gini(S) = 1 - \sum_{k=1}^{K} p_k^2$$

其中 $p_k$ 是类别 $k$ 在集合 $S$ 中的比例。基尼不纯度衡量数据集的纯度，值越小表示数据越纯净。

**最优分裂选择**：
对于每个特征和阈值，计算加权平均基尼不纯度：
$$Gini_{split} = \frac{|S_L|}{|S|}Gini(S_L) + \frac{|S_R|}{|S|}Gini(S_R)$$

选择使 $Gini_{split}$ 最小的特征和阈值进行分裂。

**停止条件**：
- 深度达到 `max_depth`
- 所有样本属于同一类别
- 无法进一步分裂（可选阈值无有效划分）

### 3.2 测试用例说明

| 测试名称 | 验证内容 | 数学意义 |
|---------|---------|---------|
| `test_simple_classification` | 树结构正确性 | 验证返回 `leaf`, `feature`, `threshold`, `left`, `right` 字段 |
| `test_predict_tree` | 预测功能 | 验证 $\text{predict}_tree$ 返回有效类别标签 |
| `test_single_class` | 单类情况 | 深度优先时返回叶节点，标签为多数类 |
| `test_max_depth` | 深度限制 | `max_depth=1` 时树应为一层结构 |

## 4. 树结构表示

决策树以嵌套字典形式存储：

```python
# 叶节点
{'leaf': True, 'label': 0}

# 内部节点
{
    'leaf': False,
    'feature': 0,        # 分裂特征索引
    'threshold': 0.5,   # 分裂阈值
    'left': {...},       # 左子树 (x[feature] <= threshold)
    'right': {...}      # 右子树 (x[feature] > threshold)
}
```

## 5. 预测机制

**SVM 预测**：
$$f(x) = \text{sign}(w_0 + \sum_{i=1}^{m} w_i x_i)$$

**决策树预测**：
从根节点开始，根据特征值与阈值比较，递归向左或向右，直到到达叶节点返回类别标签。

---

*本文档基于 `lean4py/ml_basics.py` 中的实现。*