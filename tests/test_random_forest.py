"""Tests for random forest classifier."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.ml_basics import random_forest, predict_random_forest


class TestRandomForest:
    """Tests for random forest."""
    
    def test_simple_classification(self):
        """Test random forest on simple data."""
        # Simple 2-class problem
        x = [[0.0, 0.0], [1.0, 1.0], [0.0, 1.0], [1.0, 0.0]]
        y = [0, 1, 0, 1]
        
        trees = random_forest(x, y, n_trees=5, max_depth=3)
        
        assert len(trees) == 5
        # Each tree should have structure
        for tree in trees:
            assert 'leaf' in tree
    
    def test_prediction(self):
        """Test prediction with random forest."""
        x = [[i*0.1, i*0.1] for i in range(10)]
        y = [0 if i < 5 else 1 for i in range(10)]
        
        trees = random_forest(x, y, n_trees=10, max_depth=3)
        
        # Predict on training-like point
        pred = predict_random_forest(trees, [0.2, 0.2])
        assert pred in [0, 1]
        
        pred2 = predict_random_forest(trees, [0.8, 0.8])
        assert pred2 in [0, 1]
    
    def test_empty_data(self):
        """Test with empty data."""
        trees = random_forest([], [], n_trees=5)
        assert trees == []
        
        pred = predict_random_forest([], [1.0, 1.0])
        assert pred == 0  # Default
    
    def test_single_tree(self):
        """Test with single tree."""
        x = [[0.0], [1.0], [2.0]]
        y = [0, 1, 1]
        
        trees = random_forest(x, y, n_trees=1, max_depth=2)
        
        assert len(trees) == 1
        pred = predict_random_forest(trees, [0.5])
        assert pred in [0, 1]
