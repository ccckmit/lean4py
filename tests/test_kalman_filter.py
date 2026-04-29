"""Tests for Kalman Filter module."""

import sys
sys.path.insert(0, '/Users/Shared/ccc/project/lean4py')

from lean4py.kalman_filter import KalmanFilter, kalman_smooth


class TestKalmanFilter:
    """Tests for Kalman Filter."""
    
    def test_initialization(self):
        """Test Kalman filter initializes correctly."""
        kf = KalmanFilter(state_dim=2, obs_dim=2)
        
        assert kf.state_dim == 2
        assert kf.obs_dim == 2
        assert len(kf.x) == 2
        assert len(kf.P) == 2
    
    def test_predict(self):
        """Test prediction step."""
        kf = KalmanFilter(state_dim=2, obs_dim=2)
        kf.F = [[1.0, 1.0], [0.0, 1.0]]  # Constant velocity model
        
        x_pred = kf.predict()
        
        assert len(x_pred) == 2
    
    def test_update(self):
        """Test update step."""
        kf = KalmanFilter(state_dim=2, obs_dim=2)
        kf.H = [[1.0, 0.0], [0.0, 1.0]]
        
        z = [1.0, 2.0]
        x_updated = kf.update(z)
        
        assert len(x_updated) == 2
    
    def test_predict_update_cycle(self):
        """Test predict followed by update."""
        kf = KalmanFilter(state_dim=2, obs_dim=2)
        
        # Predict
        kf.predict()
        # Update
        kf.update([1.0, 2.0])
        
        # State should be updated
        assert len(kf.x) == 2


class TestKalmanSmooth:
    """Tests for Kalman smoother."""
    
    def test_smooth_small_sequence(self):
        """Test smoothing a small sequence."""
        # Simple case
        xs = [[1.0, 2.0], [1.1, 2.1], [1.2, 2.2]]
        Ps = [[[0.1, 0.0], [0.0, 0.1]] for _ in range(3)]
        F = [[1.0, 0.0], [0.0, 1.0]]
        
        smoothed_xs, smoothed_Ps = kalman_smooth(xs, Ps, F)
        
        assert len(smoothed_xs) == 3
        assert len(smoothed_Ps) == 3
    
    def test_empty_input(self):
        """Test with empty input."""
        smoothed_xs, smoothed_Ps = kalman_smooth([], [], [[1.0]])
        
        assert smoothed_xs == []
        assert smoothed_Ps == []