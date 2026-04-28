import pytest
from lean4py.nat import (
    Nat, nat, zero, succ, pred, is_zero,
    NatInduction, nat_add, nat_mul, nat_sub,
    nat_le, nat_lt, nat_eq,
    factorial, fibonacci, nat_gcd, nat_is_prime, nat_even, nat_odd
)


class TestNat:
    def test_nat_constructor(self):
        n = Nat(5)
        assert n.n == 5

    def test_nat_negative_raises(self):
        with pytest.raises(ValueError, match="Natural numbers must be non-negative"):
            Nat(-1)

    def test_nat_zero(self):
        n = Nat(0)
        assert n.n == 0

    def test_repr(self):
        assert repr(Nat(3)) == "Nat(3)"
        assert repr(Nat(0)) == "Nat(0)"

    def test_equality(self):
        assert Nat(5) == Nat(5)
        assert Nat(5) != Nat(3)
        assert not (Nat(5) == Nat(3))

    def test_hash(self):
        n1 = Nat(5)
        n2 = Nat(5)
        assert hash(n1) == hash(n2)
        s = {n1, n2}
        assert len(s) == 1

    def test_add(self):
        a, b = Nat(3), Nat(4)
        result = a + b
        assert result.n == 7
        assert isinstance(result, Nat)

    def test_mul(self):
        a, b = Nat(3), Nat(4)
        result = a * b
        assert result.n == 12

    def test_sub(self):
        a, b = Nat(7), Nat(3)
        result = a - b
        assert result.n == 4

    def test_sub_underflow(self):
        a, b = Nat(3), Nat(5)
        result = a - b
        assert result.n == 0

    def test_le(self):
        assert Nat(3) <= Nat(5)
        assert Nat(5) <= Nat(5)
        assert not (Nat(5) <= Nat(3))

    def test_lt(self):
        assert Nat(3) < Nat(5)
        assert not (Nat(5) < Nat(5))
        assert not (Nat(5) < Nat(3))

    def test_ge(self):
        assert Nat(5) >= Nat(3)
        assert Nat(5) >= Nat(5)
        assert not (Nat(3) >= Nat(5))

    def test_gt(self):
        assert Nat(5) > Nat(3)
        assert not (Nat(5) > Nat(5))
        assert not (Nat(3) > Nat(5))

    def test_radd(self):
        a = Nat(3)
        result = 5 + a
        assert result.n == 8

    def test_rmul(self):
        a = Nat(3)
        result = 5 * a
        assert result.n == 15


class TestNatFunctions:
    def test_nat_factory(self):
        n = nat(10)
        assert isinstance(n, Nat)
        assert n.n == 10

    def test_zero(self):
        z = zero()
        assert z.n == 0
        assert isinstance(z, Nat)

    def test_succ(self):
        n = succ(Nat(5))
        assert n.n == 6

    def test_succ_zero(self):
        n = succ(zero())
        assert n.n == 1

    def test_pred(self):
        n = pred(Nat(5))
        assert n.n == 4

    def test_pred_zero(self):
        n = pred(zero())
        assert n.n == 0

    def test_is_zero_true(self):
        assert is_zero(zero()) is True

    def test_is_zero_false(self):
        assert is_zero(Nat(5)) is False


class TestNatInduction:
    def test_induction_base_case(self):
        assert NatInduction.prove(lambda n: True, Nat(0)) is True

    def test_induction_property(self):
        def less_than_10(n: Nat) -> bool:
            return n.n < 10
        assert NatInduction.prove(less_than_10, Nat(5)) is True

    def test_induction_false(self):
        def is_zero_prop(n: Nat) -> bool:
            return n.n == 0
        assert NatInduction.prove(is_zero_prop, Nat(3)) is False


class TestNatArithmetic:
    def test_nat_add(self):
        result = nat_add(Nat(3), Nat(4))
        assert result.n == 7

    def test_nat_mul(self):
        result = nat_mul(Nat(3), Nat(4))
        assert result.n == 12

    def test_nat_sub(self):
        result = nat_sub(Nat(7), Nat(3))
        assert result.n == 4

    def test_nat_sub_underflow(self):
        result = nat_sub(Nat(3), Nat(5))
        assert result.n == 0


class TestNatComparisons:
    def test_nat_le(self):
        assert nat_le(Nat(3), Nat(5)) is True
        assert nat_le(Nat(5), Nat(5)) is True
        assert nat_le(Nat(5), Nat(3)) is False

    def test_nat_lt(self):
        assert nat_lt(Nat(3), Nat(5)) is True
        assert nat_lt(Nat(5), Nat(5)) is False
        assert nat_lt(Nat(5), Nat(3)) is False

    def test_nat_eq(self):
        assert nat_eq(Nat(5), Nat(5)) is True
        assert nat_eq(Nat(5), Nat(3)) is False


class TestNatExtended:
    def test_factorial_zero(self):
        result = factorial(Nat(0))
        assert result.n == 1

    def test_factorial_one(self):
        result = factorial(Nat(1))
        assert result.n == 1

    def test_factorial_five(self):
        result = factorial(Nat(5))
        assert result.n == 120

    def test_fibonacci_zero(self):
        result = fibonacci(Nat(0))
        assert result.n == 0

    def test_fibonacci_one(self):
        result = fibonacci(Nat(1))
        assert result.n == 1

    def test_fibonacci_five(self):
        result = fibonacci(Nat(5))
        assert result.n == 5

    def test_fibonacci_ten(self):
        result = fibonacci(Nat(10))
        assert result.n == 55

    def test_gcd(self):
        assert nat_gcd(Nat(12), Nat(8)).n == 4
        assert nat_gcd(Nat(7), Nat(5)).n == 1
        assert nat_gcd(Nat(0), Nat(5)).n == 5

    def test_is_prime(self):
        assert nat_is_prime(Nat(2)) is True
        assert nat_is_prime(Nat(3)) is True
        assert nat_is_prime(Nat(4)) is False
        assert nat_is_prime(Nat(17)) is True

    def test_even(self):
        assert nat_even(Nat(0)) is True
        assert nat_even(Nat(2)) is True
        assert nat_even(Nat(3)) is False

    def test_odd(self):
        assert nat_odd(Nat(1)) is True
        assert nat_odd(Nat(3)) is True
        assert nat_odd(Nat(2)) is False
