class Nat:
    """A natural number (non-negative integer).

    Supports arithmetic: +, *, -, comparisons: <=, <, >=, >,
    and reverse operations: __radd__, __rmul__.
    """
    def __init__(self, n: int):
        if n < 0:
            raise ValueError("Natural numbers must be non-negative")
        self.n = n

    def __repr__(self):
        return f"Nat({self.n})"

    def __eq__(self, other):
        return isinstance(other, Nat) and self.n == other.n

    def __hash__(self):
        return hash(self.n)

    def __add__(self, other):
        return Nat(self.n + other.n)

    def __mul__(self, other):
        return Nat(self.n * other.n)

    def __sub__(self, other):
        result = self.n - other.n
        return Nat(result if result >= 0 else 0)

    def __le__(self, other):
        return self.n <= other.n

    def __lt__(self, other):
        return self.n < other.n

    def __ge__(self, other):
        return self.n >= other.n

    def __gt__(self, other):
        return self.n > other.n

    def __radd__(self, other):
        return Nat(other.n + self.n) if isinstance(other, Nat) else Nat(other + self.n)

    def __rmul__(self, other):
        return Nat(other * self.n) if isinstance(other, int) else Nat(other.n * self.n)


def nat(n: int) -> Nat:
    """Create a natural number from an integer (must be >= 0)."""
    return Nat(n)


def zero() -> Nat:
    """Return the natural number 0."""
    return Nat(0)


def succ(n: Nat) -> Nat:
    """Return the successor of n (n + 1)."""
    return Nat(n.n + 1)


def pred(n: Nat) -> Nat:
    """Return the predecessor of n (max(0, n-1))."""
    return Nat(max(0, n.n - 1))


def is_zero(n: Nat) -> bool:
    """Check if n is zero."""
    return n.n == 0


class NatInduction:
    """Structural induction for natural numbers."""
    @staticmethod
    def prove(P: callable, n: Nat) -> bool:
        if n.n == 0:
            return P(Nat(0))
        return NatInduction.prove(P, pred(n)) and P(n)


def nat_add(a: Nat, b: Nat) -> Nat:
    """Add two natural numbers (a + b)."""
    return a + b


def nat_mul(a: Nat, b: Nat) -> Nat:
    """Multiply two natural numbers (a * b)."""
    return a * b


def nat_sub(a: Nat, b: Nat) -> Nat:
    """Subtract b from a, clamping at 0 (a - b)."""
    return a - b


def nat_le(a: Nat, b: Nat) -> bool:
    """Check if a <= b."""
    return a <= b


def nat_lt(a: Nat, b: Nat) -> bool:
    """Check if a < b."""
    return a < b


def nat_eq(a: Nat, b: Nat) -> bool:
    """Check if a == b."""
    return a == b


def factorial(n: Nat) -> Nat:
    """Return n! (n factorial)."""
    result = 1
    for i in range(2, n.n + 1):
        result *= i
    return Nat(result)


def fibonacci(n: Nat) -> Nat:
    """Return the nth Fibonacci number (0-indexed: fib(0)=0, fib(1)=1)."""
    if n.n <= 1:
        return n
    a, b = Nat(0), Nat(1)
    for _ in range(2, n.n + 1):
        a, b = b, Nat(a.n + b.n)
    return b


def nat_gcd(a: Nat, b: Nat) -> Nat:
    """Compute GCD of two natural numbers using Euclidean algorithm."""
    a_val, b_val = a.n, b.n
    while b_val != 0:
        a_val, b_val = b_val, a_val % b_val
    return Nat(a_val)


def nat_is_prime(n: Nat) -> bool:
    """Check if n is prime."""
    v = n.n
    if v < 2:
        return False
    if v == 2:
        return True
    if v % 2 == 0:
        return False
    for i in range(3, int(v ** 0.5) + 1, 2):
        if v % i == 0:
            return False
    return True


def nat_even(n: Nat) -> bool:
    """Check if n is even."""
    return n.n % 2 == 0


def nat_odd(n: Nat) -> bool:
    """Check if n is odd."""
    return n.n % 2 == 1