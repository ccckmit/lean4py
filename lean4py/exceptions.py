class Lean4PyError(Exception):
    """Base exception for lean4py."""
    pass


class DimensionError(Lean4PyError):
    """Raised when matrix/vector dimensions don't match."""
    pass


class NotInvertibleError(Lean4PyError):
    """Raised when matrix is not invertible or determinant is zero."""
    pass


class ConvergenceError(Lean4PyError):
    """Raised when numerical method fails to converge."""
    pass


class GraphError(Lean4PyError):
    """Raised for graph-related errors (e.g., vertex not found)."""
    pass


class ProbabilityError(Lean4PyError):
    """Raised for probability-related errors (e.g., invalid distribution)."""
    pass
