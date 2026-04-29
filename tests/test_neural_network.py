"""Tests for neural network module."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.neural_network import (
    DenseLayer, NeuralNetwork, 
    sigmoid, relu, tanh,
    mse_loss, train_neural_network
)
import math


class TestActivationFunctions:
    """Tests for activation functions."""
    
    def test_sigmoid(self):
        """Test sigmoid function."""
        assert sigmoid(0) == 0.5
        assert sigmoid(100) > 0.99
        assert sigmoid(-100) < 0.01
        assert 0 < sigmoid(1) < 1
    
    def test_relu(self):
        """Test ReLU function."""
        assert relu(1.0) == 1.0
        assert relu(0.0) == 0.0
        assert relu(-1.0) == 0.0
        assert relu(10.0) == 10.0
    
    def test_tanh(self):
        """Test tanh function."""
        assert tanh(0) == 0.0
        assert tanh(100) > 0.99
        assert tanh(-100) < -0.99
        assert -1 < tanh(0.5) < 1


class TestDenseLayer:
    """Tests for DenseLayer."""
    
    def test_initialization(self):
        """Test layer initializes correctly."""
        layer = DenseLayer(input_size=3, output_size=2, activation='sigmoid')
        
        assert layer.input_size == 3
        assert layer.output_size == 2
        assert len(layer.weights) == 2  # output_size rows
        assert len(layer.weights[0]) == 4  # input_size + 1 (bias)
    
    def test_forward_pass(self):
        """Test forward pass through layer."""
        layer = DenseLayer(input_size=2, output_size=1, activation='sigmoid')
        
        # Simple input
        x = [0.5, 0.5]
        output = layer.forward(x)
        
        assert len(output) == 1
        assert 0 < output[0] < 1  # sigmoid output
    
    def test_relu_layer(self):
        """Test ReLU layer."""
        layer = DenseLayer(input_size=1, output_size=1, activation='relu')
        
        assert layer.activation(1.0) == 1.0
        assert layer.activation(-1.0) == 0.0


class TestNeuralNetwork:
    """Tests for NeuralNetwork class."""
    
    def test_add_layer(self):
        """Test adding layers to network."""
        net = NeuralNetwork()
        layer1 = DenseLayer(input_size=2, output_size=3, activation='sigmoid')
        layer2 = DenseLayer(input_size=3, output_size=1, activation='sigmoid')
        
        net.add_layer(layer1)
        net.add_layer(layer2)
        
        assert len(net.layers) == 2
    
    def test_forward_pass(self):
        """Test forward pass through network."""
        net = NeuralNetwork()
        net.add_layer(DenseLayer(2, 3, 'sigmoid'))
        net.add_layer(DenseLayer(3, 1, 'sigmoid'))
        
        x = [0.5, 0.3]
        output = net.forward(x)
        
        assert len(output) == 1
        assert 0 < output[0] < 1
    
    def test_predict_classification(self):
        """Test prediction for classification."""
        net = NeuralNetwork()
        net.add_layer(DenseLayer(2, 2, 'sigmoid'))
        
        x = [0.5, 0.3]
        pred = net.predict(x)
        
        assert pred in [0, 1]


class TestMSE:
    """Tests for MSE loss."""
    
    def test_mse_loss(self):
        """Test MSE computation."""
        y_pred = [1.0, 2.0, 3.0]
        y_true = [1.0, 2.0, 3.0]
        
        loss = mse_loss(y_pred, y_true)
        assert loss == 0.0
        
        y_pred2 = [1.0, 2.0, 3.0]
        y_true2 = [2.0, 3.0, 4.0]
        loss2 = mse_loss(y_pred2, y_true2)
        assert loss2 == 1.0  # (1+1+1)/3 = 1
    
    def test_mse_mismatch_length(self):
        """Test MSE with mismatched lengths."""
        loss = mse_loss([1.0], [1.0, 2.0])
        assert loss == 0.0


class TestTraining:
    """Tests for training function."""
    
    def test_simple_training(self):
        """Test training on simple data."""
        net = NeuralNetwork()
        net.add_layer(DenseLayer(1, 2, 'sigmoid'))
        net.add_layer(DenseLayer(2, 1, 'sigmoid'))
        
        # Simple data: y = x
        x_train = [[0.0], [0.5], [1.0]]
        y_train = [[0.0], [0.5], [1.0]]
        
        losses = train_neural_network(
            net, x_train, y_train, 
            epochs=10, learning_rate=0.1
        )
        
        assert len(losses) == 10
        assert all(l >= 0 for l in losses)
        # Loss should generally decrease
        assert losses[-1] <= losses[0] * 1.5  # Allow some tolerance
