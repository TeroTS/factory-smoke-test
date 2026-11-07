"""Verify the dependency-free demonstration baseline."""

import unittest

from calculator import add, multiply, subtract


class AdditionTest(unittest.TestCase):
    def test_positive_operands(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative_operands(self):
        self.assertEqual(add(-2, -3), -5)
        self.assertEqual(add(-2, 3), 1)
        self.assertEqual(add(2, -3), -1)

    def test_zero_operands(self):
        self.assertEqual(add(0, 5), 5)
        self.assertEqual(add(5, 0), 5)
        self.assertEqual(add(0, 0), 0)


class SubtractionTest(unittest.TestCase):
    def test_positive_operands(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_operand_order(self):
        self.assertEqual(subtract(3, 5), -2)

    def test_negative_operands(self):
        self.assertEqual(subtract(-2, -3), 1)
        self.assertEqual(subtract(-3, -2), -1)
        self.assertEqual(subtract(-2, 3), -5)
        self.assertEqual(subtract(2, -3), 5)

    def test_zero_operands(self):
        self.assertEqual(subtract(0, 5), -5)
        self.assertEqual(subtract(5, 0), 5)
        self.assertEqual(subtract(0, -5), 5)
        self.assertEqual(subtract(-5, 0), -5)
        self.assertEqual(subtract(0, 0), 0)


class MultiplicationTest(unittest.TestCase):
    def test_positive_operands(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_negative_operands(self):
        self.assertEqual(multiply(-2, -3), 6)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(2, -3), -6)

    def test_zero_operands(self):
        self.assertEqual(multiply(0, 5), 0)
        self.assertEqual(multiply(5, 0), 0)
        self.assertEqual(multiply(0, 0), 0)
