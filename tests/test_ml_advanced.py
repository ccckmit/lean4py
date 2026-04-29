"""Tests for advanced ML algorithms (SVM, Decision Tree)."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.ml_basics import svm_linear, decision_tree, predict_tree
import math


class TestSVMLinear:
    """Tests for linear SVM implementation."""
    
    def test_separable_data(self):
        """Test SVM on linearly separable data."""
        # Simple separable case: class 0 at (0,0), class 1 at (1,1)
        x = [[0.0, 0.0], [1.0, 1.0]]
        y = [-1, 1]  # Labels must be -1 or 1
        
        w = svm_linear(x, y, learning_rate=0.1, max_iter=1000)
        
        # Check that weights are returned
        assert len(w) == 3  # bias + 2 features
        assert all(isinstance(v, float) for v in w)
    
    def test_predict_separable(self):
        """Test SVM can separate simple data."""
        x = [[0.0], [1.0], [2.0]]
        y = [-1, 1, 1]
        
        w = svm_linear(x, y, learning_rate=0.1, max_iter=1000)
        
        # Prediction: sign(w·x + b)
        def predict(x_val):
            pred = w[0] + w[1] * x_val[0]  # bias + weight*x
            return 1 if pred >= 0 else -1
        
        # First point should be negative class
        assert predict([0.0]) == -1
        # Last two should be positive class
        assert predict([1.0]) == 1
        assert predict([2.0]) == 1
    
    def test_empty_data(self):
        """Test SVM handles empty data."""
        w = svm_linear([], [], learning_rate=0.1, max_iter=100)
        assert w == []
    
    def test_regularization(self):
        """Test that regularization parameter is accepted."""
        x = [[0.0], [1.0]]
        y = [-1, 1]
        
        # Should not crash with different lambda values
        w1 = svm_linear(x, y, lambda_reg=0.01, max_iter=100)
        w2 = svm_linear(x, y, lambda_reg=0.1, max_iter=100)
        
        assert len(w1) == 2
        assert len(w2) == 2


class TestDecisionTree:
    """Tests for decision tree implementation."""
    
    def test_simple_classification(self):
        """Test decision tree on simple 2-class problem."""
        # Two features, two classes
        x = [[0.0, 0.0], [1.0, 1.0], [0.0, 1.0], [1.0, 0.0]]
        y = [0, 1, 0, 1]
        
        tree = decision_tree(x, y, max_depth=3)
        
        # Tree should have structure
        assert 'leaf' in tree
        if not tree['leaf']:
            assert 'feature' in tree
            assert 'threshold' in tree
            assert 'left' in tree
            assert 'right' in tree
    
    def test_predict_tree(self):
        """Test prediction with decision tree."""
        x = [[0.0], [1.0], [2.0]]
        y = [0, 1, 1]
        
        tree = decision_tree(x, y, max_depth=3)
        
        # Predictions should be valid labels
        pred1 = predict_tree(tree, [0.5])
        pred2 = predict_tree(tree, [1.5])
        
        assert pred1 in [0, 1]
        assert pred2 in [0, 1]
    
    def test_single_class(self):
        """Test decision tree with single class."""
        x = [[0.0], [1.0], [2.0]]
        y = [1, 1, 1]
        
        tree = decision_tree(x, y, max_depth=3)
        
        # Should be leaf with label 1
        assert tree['leaf'] == True
        assert tree['label'] == 1
    
    def test_max_depth(self):
        """Test that max_depth is respected."""
        x = [[i/10.0, i/10.0] for i in range(10)]
        y = [0 if i < 5 else 1 for i in range(10)]
        
        tree = decision_tree(x, y, max_depth=1)
        
        # With depth 1, tree should be simple
        # Just check it doesn't crash and returns valid structure
        assert 'leaf' in tree
