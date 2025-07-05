# tests.py

import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result, quote = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)
        self.assertIsInstance(quote, str)

    def test_subtraction(self):
        result, quote = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)
        self.assertIsInstance(quote, str)

    def test_multiplication(self):
        result, quote = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)
        self.assertIsInstance(quote, str)

    def test_division(self):
        result, quote = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)
        self.assertIsInstance(quote, str)

    def test_nested_expression(self):
        result, quote = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)
        self.assertIsInstance(quote, str)

    def test_complex_expression(self):
        result, quote = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)
        self.assertIsInstance(quote, str)

    def test_empty_expression(self):
        result, quote = self.calculator.evaluate("")
        self.assertIsNone(result)
        self.assertIsInstance(quote, str)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")

    def test_modulus(self):
        result, quote = self.calculator.evaluate("10 % 3")
        self.assertEqual(result, 1)
        self.assertIsInstance(quote, str)

    def test_modulus_complex(self):
        result, quote = self.calculator.evaluate("20 % 6 + 1")
        self.assertEqual(result, 3.0)
        self.assertIsInstance(quote, str)


if __name__ == "__main__":
    unittest.main()
