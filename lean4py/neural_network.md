# 神經網路模組 (Neural Network Module)

本模組實現了基礎的前饋神經網路，包含感知器、激活函數、損失函數、梯度下降和反向傳播等核心組件。

---

## 1. 感知器 (Perceptron)

### 1.1 決策邊界

感知器是最基本的神經網路單元，其輸出為：

$$y = f(\mathbf{w} \cdot \mathbf{x} + b) = f\left(\sum_{i=1}^{n} w_i x_i + b\right)$$

其中：
- $\mathbf{w} = (w_1, w_2, ..., w_n)$ 是權重向量
- $\mathbf{x} = (x_1, x_2, ..., x_n)$ 是輸入向量
- $b$ 是偏置項 (bias)
- $f$ 是激活函數

決策邊界由 $\mathbf{w} \cdot \mathbf{x} + b = 0$ 定義，這是一個超平面，將輸入空間劃分為兩個區域。

### 1.2 感知器學習演算法

權重更新規則：

$$w_i^{(new)} = w_i^{(old)} + \eta(y - \hat{y})x_i$$

其中 $\eta$ 是學習率，$y$ 是真實標籤，$\hat{y}$ 是預測輸出。

---

## 2. 激活函數 (Activation Functions)

激活函數為網路引入非線性，使網路能夠學習複雜的模式。

### 2.1 Sigmoid 函數

$$\sigma(x) = \frac{1}{1 + e^{-x}}$$

**數學性質：**
- 輸出範圍：$(0, 1)$
- 導數：$\sigma'(x) = \sigma(x)(1 - \sigma(x))$

```python
def sigmoid(x: float) -> float:
    """Sigmoid activation function."""
    if x > 500:
        return 1.0
    if x < -500:
        return 0.0
    return 1.0 / (1.0 + math.exp(-x))
```

**程式碼實現：** 在 `neural_network.py:7-13`

### 2.2 ReLU 函數 (Rectified Linear Unit)

$$\text{ReLU}(x) = \max(0, x)$$

**優點：**
- 計算高效
- 緩解梯度消失問題
- 稀疏激活

**導數：**
$$\text{ReLU}'(x) = \begin{cases} 1 & \text{if } x > 0 \\ 0 & \text{if } x \leq 0 \end{cases}$$

```python
def relu(x: float) -> float:
    """ReLU activation function."""
    return max(0.0, x)
```

**程式碼實現：** 在 `neural_network.py:22-24`

### 2.3 Tanh 函數 (雙曲正切)

$$\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$$

**數學性質：**
- 輸出範圍：$(-1, 1)$
- 導數：$\tanh'(x) = 1 - \tanh^2(x)$
- 零均值輸出

```python
def tanh(x: float) -> float:
    """Tanh activation function."""
    return math.tanh(x)
```

**程式碼實現：** 在 `neural_network.py:32-34`

### 2.4 激活函數比較

| 函數 | 輸出範圍 | 導數特點 | 應用場景 |
|------|----------|----------|----------|
| Sigmoid | $(0, 1)$ | $\sigma(x)(1-\sigma(x))$ | 二分類輸出層 |
| ReLU | $[0, +\infty)$ | $1$ 或 $0$ | 隱藏層 |
| Tanh | $(-1, 1)$ | $1 - \tanh^2(x)$ | 隱藏層 |

---

## 3. 前饋網路 (Feedforward Network)

### 3.1 網路結構

前饋網路由多個全連接層 (DenseLayer) 組成，信息單向流動：

$$\mathbf{y} = f(\mathbf{x}; \theta) = f^{(L)}(f^{(L-1)}(...(f^{(1)}(\mathbf{x}))...))$$

其中 $\theta$ 表示所有層的權重參數。

### 3.2 DenseLayer 類

每層執行以下計算：

$$a_i^{(l)} = \sigma\left(\sum_{j=1}^{n^{(l-1)}} w_{ij}^{(l)} a_j^{(l-1)} + b_i^{(l)}\right)$$

矩陣形式：

$$\mathbf{a}^{(l)} = \sigma(\mathbf{W}^{(l)} \mathbf{a}^{(l-1)} + \mathbf{b}^{(l)})$$

```python
class DenseLayer:
    """A fully connected layer."""
    
    def __init__(self, input_size: int, output_size: int, activation: str = 'sigmoid'):
        # Xavier 初始化
        bound = math.sqrt(1.0 / input_size)
```

**程式碼實現：** 在 `neural_network.py:42-86`

### 3.3 權重初始化

本模組使用 Xavier 初始化：

$$w \sim \mathcal{U}\left(-\sqrt{\frac{1}{n_{in}}, \sqrt{\frac{1}{n_{in}}}\right)$$

這確保了前向傳播時輸入輸出方差一致。

---

## 4. 損失函數 (Loss Functions)

### 4.1 均方誤差 (Mean Squared Error, MSE)

$$L_{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

**導數：**

$$\frac{\partial L_{MSE}}{\partial \hat{y}_i} = \frac{2}{n}(y_i - \hat{y}_i)$$

```python
def mse_loss(y_pred: List[float], y_true: List[float]) -> float:
    """Mean squared error loss."""
    return sum((y_pred[i] - y_true[i]) ** 2 for i in range(len(y_pred))) / len(y_pred)
```

**程式碼實現：** 在 `neural_network.py:113-117`

### 4.2 交叉熵損失 (Cross-Entropy Loss)

對於分類任務，交叉熵損失更為常用：

$$L_{CE} = -\sum_{i=1}^{n} y_i \log(\hat{y}_i)$$

**特點：**
- 梯度更陡峭，收斂更快
- 適用於softmax輸出層

---

## 5. 梯度下降與反向傳播

### 5.1 梯度下降

參數更新規則：

$$\theta^{(new)} = \theta^{(old)} - \eta \nabla_{\theta} L$$

其中 $\eta$ 是學習率，$\nabla_{\theta} L$ 是損失函數相對於參數的梯度。

### 5.2 反向傳播 (Backpropagation)

反向傳播利用鏈式法則計算每個參數的梯度。

對於第 $l$ 層的權重 $w_{ij}^{(l)}$：

$$\frac{\partial L}{\partial w_{ij}^{(l)}} = \frac{\partial L}{\partial a_i^{(l)}} \cdot \frac{\partial a_i^{(l)}}{\partial z_i^{(l)}} \cdot \frac{\partial z_i^{(l)}}{\partial w_{ij}^{(l)}}$$

簡化為：

$$\frac{\partial L}{\partial w_{ij}^{(l)}} = \delta_i^{(l)} \cdot a_j^{(l-1)}$$

其中 $\delta_i^{(l)}$ 是第 $l$ 層第 $i$ 個神經元的誤差項。

### 5.3 誤差反向傳播

$$\delta_i^{(l)} = \sigma'(z_i^{(l)}) \sum_{k=1}^{n^{(l+1)}} w_{ki}^{(l+1)} \delta_k^{(l+1)}$$

```python
# 輸出層誤差計算
error = mse_loss_derivative(output, y)
for i in range(len(error)):
    error[i] *= layer.activation_deriv(weighted_sums[-1][i])

# 隱藏層誤差反向傳播
for l in range(len(network.layers) - 1, -1, -1):
    prev_error[j] += (layer.weights[i][j] * error[i] * 
                    network.layers[l-1].activation_deriv(weighted_sums[l-1][j]))
```

**程式碼實現：** 在 `neural_network.py:179-203`

---

## 6. 鏈式法則 (Chain Rule)

鏈式法则是反向傳播的數學基礎。

### 6.1 單變量鏈式法則

若 $y = f(u)$ 且 $u = g(x)$，則：

$$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$$

### 6.2 多變量鏈式法則

若 $z = f(u_1, u_2, ..., u_n)$，其中每個 $u_i = g_i(x)$，則：

$$\frac{\partial z}{\partial x} = \sum_{i=1}^{n} \frac{\partial z}{\partial u_i} \cdot \frac{\partial u_i}{\partial x}$$

### 6.3 神經網路中的應用

對於複合函數 $L = f(g(h(\mathbf{x})))$：

$$\frac{\partial L}{\partial \mathbf{x}} = \frac{\partial L}{\partial f} \cdot \frac{\partial f}{\partial g} \cdot \frac{\partial g}{\partial h} \cdot \frac{\partial h}{\partial \mathbf{x}}$$

---

## 7. 學習率與收斂

### 7.1 學習率 (Learning Rate)

學習率 $\eta$ 控制梯度下降的步長：

$$\theta^{(new)} = \theta^{(old)} - \eta \nabla_{\theta} L$$

**學習率過大：** 可能導致震盪或不收斂

**學習率過小：** 收斂緩慢，可能陷入局部最小值

### 7.2 收斂判斷

訓練收斂的常見標準：
- 損失函數值低於閾值
- 損失變化率低於閾值
- 達到最大迭代次數

```python
def train_neural_network(
    network: NeuralNetwork,
    x_train: List[List[float]],
    y_train: List[List[float]],
    epochs: int = 100,
    learning_rate: float = 0.1
) -> List[float]:
```

**程式碼實現：** 在 `neural_network.py:127-206`

---

## 8. 過擬合與正則化

### 8.1 過擬合 (Overfitting)

當模型在訓練集上表現良好但在測試集上表現較差時，稱為過擬合。

**原因：**
- 模型複雜度過高
- 訓練數據不足
- 噪聲過多

### 8.2 正則化技術

#### L1 正則化 (Lasso)

$$L_{total} = L_{original} + \lambda \sum_{i} |w_i|$$

促進稀疏權重。

#### L2 正則化 (Ridge)

$$L_{total} = L_{original} + \lambda \sum_{i} w_i^2$$

懲罰大權重，防止過擬合。

#### Dropout

在訓練時隨機關閉部分神經元，增強模型魯棒性。

### 8.3 改進建議

本模組可進一步擴展：
- 添加 L1/L2 正則化項
- 實現 dropout
- 添加 early stopping
- 實現學習率衰減

---

## 模組使用範例

```python
from lean4py.neural_network import DenseLayer, NeuralNetwork, train_neural_network

# 創建網路
net = NeuralNetwork()
net.add_layer(DenseLayer(2, 4, activation='relu'))
net.add_layer(DenseLayer(4, 2, activation='sigmoid'))

# 訓練數據 (XOR 問題)
x_train = [[0, 0], [0, 1], [1, 0], [1, 1]]
y_train = [[1, 0], [0, 1], [0, 1], [1, 0]]

# 訓練
losses = train_neural_network(net, x_train, y_train, epochs=1000, learning_rate=0.1)

# 預測
result = net.predict([1, 0])  # 返回類別索引
```

---

## 數學符號表

| 符號 | 含義 |
|------|------|
| $\mathbf{x}$ | 輸入向量 |
| $\mathbf{w}$ | 權重向量 |
| $b$ | 偏置項 |
| $\sigma$ | 激活函數 |
| $\eta$ | 學習率 |
| $L$ | 損失函數 |
| $\nabla$ | 梯度運算符 |
| $\theta$ | 參數集合 |

---

*本文件對應 `neural_network.py` v1.34.0*