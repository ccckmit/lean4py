# Neural Network 测试文档

本文档说明 `test_neural_network.py` 中测试用例的数学原理。

## 1. 测试概述

本测试模块验证神经网络模块的核心功能，包括：
- 激活函数（Sigmoid、ReLU、Tanh）
- 全连接层（DenseLayer）
- 前向传播（Forward Propagation）
- 反向传播（Backpropagation）
- 损失函数（MSE）

---

## 2. 层初始化测试（TestDenseLayer）

### 数学原理

全连接层的权重矩阵形状为 `(output_size, input_size + 1)`，其中最后一列用于偏置（bias）。

### 测试用例分析

```python
layer = DenseLayer(input_size=3, output_size=2, activation='sigmoid')
```

- **权重数量**：`output_size × (input_size + 1)` = `2 × 4`
- **权重初始化**：使用 Xavier 初始化，范围为 `[-√(1/input_size), √(1/input_size)]`

### 验证点

| 测试 | 验证内容 | 预期结果 |
|------|----------|----------|
| `test_initialization` | 权重维度 | `len(weights) == 2`，每行长度 `== 4` |
| `test_forward_pass` | 前向计算 | 输出为 sigmoid 值，范围在 (0, 1) |
| `test_relu_layer` | ReLU 激活 | 正输入原值输出，负输入输出 0 |

---

## 3. 激活函数测试（TestActivationFunctions）

### 3.1 Sigmoid 函数

**数学定义**：
$$\sigma(x) = \frac{1}{1 + e^{-x}}$$

**导数公式**：
$$\sigma'(x) = \sigma(x)(1 - \sigma(x))$$

**特性**：
- 输出范围：(0, 1)
- 极端值处理：当 `x > 500` 返回 1.0，`x < -500` 返回 0.0

### 3.2 ReLU 函数

**数学定义**：
$$\text{ReLU}(x) = \max(0, x)$$

**导数公式**：
$$\text{ReLU}'(x) = \begin{cases} 1 & x > 0 \\ 0 & x \leq 0 \end{cases}$$

**特性**：
- 稀疏激活
- 避免梯度消失问题

### 3.3 Tanh 函数

**数学定义**：
$$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$$

**导数公式**：
$$\tanh'(x) = 1 - \tanh^2(x)$$

**特性**：
- 输出范围：(-1, 1)
- 零中心化输出

### 测试验证点

| 函数 | 测试点 | 数学原理 |
|------|--------|----------|
| Sigmoid | `sigmoid(0) == 0.5` | $\sigma(0) = \frac{1}{1+1} = 0.5$ |
| Sigmoid | `sigmoid(100) > 0.99` | 极限值逼近 1 |
| ReLU | `relu(-1.0) == 0.0` | $\max(0, -1) = 0$ |
| Tanh | `tanh(0) == 0.0` | 奇函数性质 |

---

## 4. 前向传播测试（TestNeuralNetwork）

### 数学原理

前向传播计算：

对于第 $l$ 层：
$$z^{(l)} = W^{(l)} \cdot a^{(l-1)} + b^{(l)}$$
$$a^{(l)} = f(z^{(l)})$$

其中 $W$ 是权重矩阵，$a$ 是激活值，$f$ 是激活函数。

### 测试用例

```python
net.add_layer(DenseLayer(2, 3, 'sigmoid'))
net.add_layer(DenseLayer(3, 1, 'sigmoid'))
output = net.forward([0.5, 0.3])
```

### 验证点

| 测试 | 验证内容 | 预期结果 |
|------|----------|----------|
| `test_add_layer` | 层数量 | `len(net.layers) == 2` |
| `test_forward_pass` | 输出维度 | 输出长度 `== 1` |
| `test_forward_pass` | 输出范围 | 值在 (0, 1) 之间 |
| `test_predict_classification` | 预测类别 | 返回 0 或 1 |

---

## 5. 损失函数测试（TestMSE）

### 数学原理

**均方误差（MSE）**：
$$\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_{\text{pred},i} - y_{\text{true},i})^2$$

**导数公式**：
$$\frac{\partial \text{MSE}}{\partial y_{\text{pred},i}} = \frac{2}{n}(y_{\text{pred},i} - y_{\text{true},i})$$

### 测试用例

```python
y_pred = [1.0, 2.0, 3.0]
y_true = [2.0, 3.0, 4.0]
loss = mse_loss(y_pred, y_true)  # = 1.0
```

计算验证：
$$\text{MSE} = \frac{(1-2)^2 + (2-3)^2 + (3-4)^2}{3} = \frac{1+1+1}{3} = 1.0$$

---

## 6. 反向传播测试（TestTraining）

### 数学原理

反向传播使用链式法则计算梯度：

**输出层梯度**：
$$\delta^{(L)} = \nabla_a J \odot f'(z^{(L)})$$

**隐藏层梯度**：
$$\delta^{(l)} = (W^{(l+1)})^T \delta^{(l+1)} \odot f'(z^{(l)})$$

**权重更新**：
$$W^{(l)} \leftarrow W^{(l)} - \eta \cdot \delta^{(l)} \cdot (a^{(l-1)})^T$$

其中 $\eta$ 是学习率。

### 测试用例

```python
train_neural_network(net, x_train, y_train, epochs=10, learning_rate=0.1)
```

### 验证点

| 测试 | 验证内容 | 预期结果 |
|------|----------|----------|
| `test_simple_training` | 损失记录数量 | `len(losses) == 10`（每个 epoch 记录一次） |
| `test_simple_training` | 损失非负 | `all(l >= 0 for l in losses)` |
| `test_simple_training` | 损失趋势 | `losses[-1] <= losses[0] * 1.5`（允许一定容差） |

---

## 7. 测试覆盖总结

```
test_neural_network.py
├── TestActivationFunctions
│   ├── test_sigmoid      # σ(x) ∈ (0,1), σ(0) = 0.5
│   ├── test_relu         # max(0,x)
│   └── test_tanh         # tanh(x) ∈ (-1,1), tanh(0) = 0
├── TestDenseLayer
│   ├── test_initialization  # 权重维度验证
│   ├── test_forward_pass    # 层前向计算
│   └── test_relu_layer      # ReLU 激活验证
├── TestNeuralNetwork
│   ├── test_add_layer       # 多层堆叠
│   ├── test_forward_pass    # 完整网络前向传播
│   └── test_predict_classification  # 分类预测
├── TestMSE
│   ├── test_mse_loss        # MSE 计算正确性
│   └── test_mse_mismatch_length  # 输入长度不匹配处理
└── TestTraining
    └── test_simple_training # 反向传播训练
```

---

## 8. 关键数学公式汇总

| 功能 | 公式 |
|------|------|
| Sigmoid | $\sigma(x) = \frac{1}{1+e^{-x}}$ |
| Sigmoid 导数 | $\sigma'(x) = \sigma(x)(1-\sigma(x))$ |
| ReLU | $\text{ReLU}(x) = \max(0,x)$ |
| Tanh | $\tanh(x) = \frac{e^x-e^{-x}}{e^x+e^{-x}}$ |
| MSE | $\text{MSE} = \frac{1}{n}\sum(y_{pred}-y_{true})^2$ |
| 权重更新 | $W \leftarrow W - \eta \cdot \delta \cdot a^T$ |