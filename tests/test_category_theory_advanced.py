"""Tests for category_theory_advanced.py v1.28."""

import unittest
from lean4py.category_theory_advanced import (
    AdjointFunctor, Limit, Colimit,
    YonedaLemma, Monad, Comonad
)


class TestAdjointFunctor(unittest.TestCase):
    def test_is_adjoint(self):
        result = AdjointFunctor.is_adjoint(lambda x: x, lambda x: x, "C", "D")
        self.assertTrue(result)

    def test_unit(self):
        result = AdjointFunctor.unit(lambda x: x, lambda x: x)
        self.assertEqual(result["name"], "unit")

    def test_counit(self):
        result = AdjointFunctor.counit(lambda x: x, lambda x: x)
        self.assertEqual(result["name"], "counit")


class TestLimit(unittest.TestCase):
    def test_product(self):
        result = Limit.product([1, 2, 3])
        self.assertEqual(result["type"], "product")

    def test_equalizer(self):
        f = lambda x: x
        result = Limit.equalizer(f, f)
        self.assertEqual(result["type"], "equalizer")

    def test_pullback(self):
        f = lambda x: x
        g = lambda x: x
        result = Limit.pullback(f, g)
        self.assertEqual(result["type"], "pullback")


class TestColimit(unittest.TestCase):
    def test_coproduct(self):
        result = Colimit.coproduct([1, 2, 3])
        self.assertEqual(result["type"], "coproduct")

    def test_coequalizer(self):
        f = lambda x: x
        result = Colimit.coequalizer(f, f)
        self.assertEqual(result["type"], "coequalizer")

    def test_pushout(self):
        f = lambda x: x
        g = lambda x: x
        result = Colimit.pushout(f, g)
        self.assertEqual(result["type"], "pushout")


class TestYonedaLemma(unittest.TestCase):
    def test_embedding(self):
        result = YonedaLemma.embedding("C", "X")
        self.assertEqual(result["type"], "yoneda_embedding")

    def test_isomorphism(self):
        result = YonedaLemma.isomorphism(lambda x: x, "X")
        self.assertTrue(result)


class TestMonad(unittest.TestCase):
    def test_creation(self):
        m = Monad(lambda x: x, lambda x: x, lambda x: x)
        self.assertTrue(m.is_monad())


class TestComonad(unittest.TestCase):
    def test_creation(self):
        c = Comonad(lambda x: x, lambda x: x, lambda x: x)
        self.assertTrue(c.is_comonad())


if __name__ == "__main__":
    unittest.main()
