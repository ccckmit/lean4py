"""Tests for control_theory module."""

import pytest
from lean4py.control_theory import (
    LyapunovStability, StateSpaceRepresentation,
    Controllability, Observability, OptimalControl, KalmanFilter
)


class TestLyapunovStability:
    """Test Lyapunov stability."""

    def test_is_stable(self):
        V = lambda y: y * y
        dV_dt = lambda y: -2.0 * y * y
        assert LyapunovStability.is_stable(V, dV_dt) is True

    def test_lyapunov_function(self):
        y = (1.0, 2.0)
        result = LyapunovStability.lyapunov_function(y)
        assert result >= 0

    def test_is_asymptotically_stable(self):
        V = lambda y: y * y
        dV_dt = lambda y: -2.0 * y * y
        assert LyapunovStability.is_asymptotically_stable(V, dV_dt) is True


class TestStateSpaceRepresentation:
    """Test state-space representation."""

    def test_creation(self):
        A = [[0.0, 1.0], [-1.0, -1.0]]
        B = [[0.0], [1.0]]
        sys = StateSpaceRepresentation(A, B)
        assert sys.system_dim() == 2
        assert sys.input_dim() == 1

    def test_output_dim(self):
        A = [[0.0]]
        B = [[1.0]]
        C = [[1.0]]
        sys = StateSpaceRepresentation(A, B, C)
        assert sys.output_dim() == 1


class TestControllability:
    """Test controllability."""

    def test_is_controllable(self):
        A = [[0.0, 1.0], [-1.0, -1.0]]
        B = [[0.0], [1.0]]
        assert Controllability.is_controllable(A, B) is True

    def test_controllability_matrix(self):
        A = [[0.0, 1.0], [-1.0, -1.0]]
        B = [[0.0], [1.0]]
        W = Controllability.controllability_matrix(A, B)
        assert len(W) == 2
        assert len(W[0]) == 2


class TestObservability:
    """Test observability."""

    def test_is_observable(self):
        A = [[0.0, 1.0], [-1.0, -1.0]]
        C = [[1.0, 0.0]]
        assert Observability.is_observable(A, C) is True

    def test_observability_matrix(self):
        A = [[0.0, 1.0], [-1.0, -1.0]]
        C = [[1.0, 0.0]]
        W = Observability.observability_matrix(A, C)
        assert len(W) == 2


class TestOptimalControl:
    """Test optimal control."""

    def test_hamiltonian(self):
        state = (1.0,)
        control = (0.5,)
        costate = (1.0,)
        dynamics = lambda x, u: (u[0],)
        H = OptimalControl.hamiltonian(state, control, costate, dynamics)
        assert isinstance(H, (int, float))

    def test_optimal_control(self):
        H = lambda c: c * c
        control_space = [(0.0,), (1.0,)]
        result = OptimalControl.optimal_control(H, control_space)
        assert result is not None


class TestKalmanFilter:
    """Test Kalman filter."""

    def test_predict(self):
        state = (1.0, 0.0)
        A = [[1.0, 0.1], [0.0, 1.0]]
        Q = [[0.01, 0.0], [0.0, 0.01]]
        new_state, P = KalmanFilter.predict(state, A, Q)
        assert len(new_state) == 2

    def test_update(self):
        state = (1.0, 0.0)
        P = [[1.0, 0.0], [0.0, 1.0]]
        z = (1.1,)
        H = [[1.0, 0.0]]
        R = [[0.1]]
        new_state, new_P = KalmanFilter.update(state, P, z, H, R)
        assert len(new_state) == 2
