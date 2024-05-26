# Try scattering unary + and - around and see what happens.

# I m p o r t s

import os
import unittest
from decimal import Decimal

from sscalc.exceptions import Error
from sscalc.model import table, make_table, ShlexReader
from sscalc.yacc import parse

class TestUnary(unittest.TestCase):
    def setUp(self):
        if not table:
            with ShlexReader(os.path.join("tests", "data", "basic.txt")) as reader:
                make_table(reader)

    def test_add_1(self):
        self.assertEqual(parse("1++1"), Decimal(2))

    def test_add_2(self):
        self.assertEqual(parse("1+-1"), Decimal(0))

    def test_add_3(self):
        self.assertEqual(parse("+1+1"), Decimal(2))

    def test_add_4(self):
        self.assertEqual(parse("-1+1"), Decimal(0))

    def test_sub_1(self):
        self.assertEqual(parse("1-+1"), Decimal(0))

    def test_sub_2(self):
        self.assertEqual(parse("1--1"), Decimal(2))

    def test_mul_1(self):
        self.assertEqual(parse("2*+3"), Decimal(6))

    def test_mul_2(self):
        self.assertEqual(parse("2*-3"), Decimal(-6))

    def test_div_1(self):
        self.assertEqual(parse("1/+3"), Decimal(1) / Decimal(3))

    def test_div_2(self):
        self.assertEqual(parse("1/-3"), Decimal(1) / Decimal(-3))

    def test_div_3(self):
        self.assertEqual(parse("+1/3"), Decimal(1) / Decimal(3))

    def test_div_4(self):
        self.assertEqual(parse("-1/3"), Decimal(-1) / Decimal(3))

    def test_idiv_1(self):
        self.assertEqual(parse("-1//3"), Decimal(0))

    def test_idiv_2(self):
        self.assertEqual(parse("1//-3"), Decimal(0))

# M a i n   P r o g r a m

if __name__ == '__main__':
    unittest.main()
