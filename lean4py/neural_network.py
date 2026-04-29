"""Neural Network module for basic feedforward networks."""

from typing import List, Callable, Optional
import math


def sigmoid(x: float) -> float:
    """Sigmoid activation function."""
    if x > 500:
        return 1.0
    if x < -500:
        return 0.0
    return 1.0 / (1.0 + math.exp(-x))


def sigmoid_derivative(x: float) -> float:
    """Derivative of sigmoid."""
    s = sigmoid(x)
    return s * (1 - s)


def relu(x: float) -> float:
    """ReLU activation function."""
    return max(0.0, x)


def relu_derivative(x: float) -> float:
    """Derivative of ReLU."""
    return 1.0 if x > 0 else 0.0


def tanh(x: float) -> float:
    """Tanh activation function."""
    return math.tanh(x)


def tanh_derivative(x: float) -> float:
    """Derivative of tanh."""
    return 1 - math.tanh(x) ** 2


class DenseLayer:
    """A fully connected layer."""
    
    def __init__(self, input_size: int, output_size: int, activation: str = 'sigmoid'):
        self.input_size = input_size
        self.output_size = output_size
        self.activation_name = activation
        
        # Initialize weights with small random values
        self.weights = []
        for i in range(output_size):
            row = []
            for j in range(input_size + 1):  # +1 for bias
                # Xavier initialization
                bound = math.sqrt(1.0 / input_size)
                import random
                row.append(random.uniform(-bound, bound))
            self.weights.append(row)
        
        # Activation function
        if activation == 'sigmoid':
            self.activation = sigmoid
            self.activation_deriv = sigmoid_derivative
        elif activation == 'relu':
            self.activation = relu
            self.activation_deriv = relu_derivative
        elif activation == 'tanh':
            self.activation = tanh
            self.activation_deriv = tanh_derivative
        else:
            self.activation = sigmoid
            self.activation_deriv = sigmoid_derivative
    
    def forward(self, x: List[float]) -> List[float]:
        """Forward pass through the layer."""
        # Add bias term
        x_with_bias = x + [1.0]
        
        output = []
        for i in range(self.output_size):
            # Compute weighted sum
            z = sum(self.weights[i][j] * x_with_bias[j] 
                   for j in range(self.input_size + 1))
            output.append(self.activation(z))
        
        return output


class NeuralNetwork:
    """Simple feedforward neural network."""
    
    def __init__(self):
        self.layers: List[DenseLayer] = []
    
    def add_layer(self, layer: DenseLayer):
        """Add a layer to the network."""
        self.layers.append(layer)
    
    def forward(self, x: List[float]) -> List[float]:
        """Forward pass through the entire network."""
        output = x
        for layer in self.layers:
            output = layer.forward(output)
        return output
    
    def predict(self, x: List[float]) -> int:
        """Predict class (for classification)."""
        output = self.forward(x)
        return output.index(max(output))


def mse_loss(y_pred: List[float], y_true: List[float]) -> float:
    """Mean squared error loss."""
    if len(y_pred) != len(y_true):
        return 0.0
    return sum((y_pred[i] - y_true[i]) ** 2 for i in range(len(y_pred))) / len(y_pred)


def mse_loss_derivative(y_pred: List[float], y_true: List[float]) -> List[float]:
    """Derivative of MSE loss."""
    if len(y_pred) != len(y_true):
        return [0.0] * len(y_pred)
    return [2 * (y_pred[i] - y_true[i]) / len(y_pred) for i in range(len(y_pred))]


def train_neural_network(
    network: NeuralNetwork,
    x_train: List[List[float]],
    y_train: List[List[float]],
    epochs: int = 100,
    learning_rate: float = 0.1
) -> List[float]:
    """Train a neural network using backpropagation.
    
    Args:
        network: NeuralNetwork instance
        x_train: Input data
        y_train: Target data (one-hot encoded)
        epochs: Number of training epochs
        learning_rate: Learning rate for weight updates
        
    Returns:
        List of loss values per epoch
    """
    losses = []
    
    for epoch in range(epochs):
        total_loss = 0.0
        
        for idx in range(len(x_train)):
            x = x_train[idx]
            y = y_train[idx]
            
            # Forward pass - store intermediate values for backprop
            activations = [x]  # Store activations for each layer
            weighted_sums = []  # Store weighted sums (z values)
            
            current_input = x
            for layer in network.layers:
                # Add bias
                current_with_bias = current_input + [1.0]
                z = []
                a = []
                for i in range(layer.output_size):
                    z_val = sum(layer.weights[i][j] * current_with_bias[j] 
                               for j in range(layer.input_size + 1))
                    z.append(z_val)
                    a.append(layer.activation(z_val))
                weighted_sums.append(z)
                activations.append(a)
                current_input = a
            
            # Compute loss
            output = activations[-1]
            loss = mse_loss(output, y)
            total_loss += loss
            
            # Backward pass
            # Output layer error
            error = mse_loss_derivative(output, y)
            for i in range(len(error)):
                error[i] *= layer.activation_deriv(weighted_sums[-1][i])
            
            # Backpropagate through layers
            for l in range(len(network.layers) - 1, -1, -1):
                layer = network.layers[l]
                
                # Update weights
                input_with_bias = activations[l] + [1.0]
                for i in range(layer.output_size):
                    for j in range(layer.input_size + 1):
                        layer.weights[i][j] -= learning_rate * error[i] * input_with_bias[j]
                
                # Compute error for previous layer (if not input layer)
                if l > 0:
                    prev_error = [0.0] * network.layers[l-1].output_size
                    for j in range(network.layers[l-1].output_size):
                        for i in range(layer.output_size):
                            prev_error[j] += (layer.weights[i][j] * error[i] * 
                                            network.layers[l-1].activation_deriv(
                                                weighted_sums[l-1][j]))
                    error = prev_error
        
        losses.append(total_loss / len(x_train))
    
    return losses
