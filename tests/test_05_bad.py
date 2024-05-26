# Crap syntax should be rejected as such.

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

    def test_incomplete_add(self):
        self.assertRaises(Error, parse, "1+")

    def test_incomplete_sub(self):
        self.assertRaises(Error, parse, "1-")

    def test_incomplete_mul_1(self):
        self.assertRaises(Error, parse, "*3")

    def test_incomplete_mul_2(self):
        self.assertRaises(Error, parse, "2*")

    def test_incomplete_div_1(self):
        self.assertRaises(Error, parse, "/3")

    def test_incomplete_div_2(self):
        self.assertRaises(Error, parse, "1/")

    def test_incomplete_idiv_1(self):
        self.assertRaises(Error, parse, "//3")

    def test_incomplete_idiv_2(self):
        self.assertRaises(Error, parse, "1//")

    def test_incomplete_exp_1a(self):
        self.assertRaises(Error, parse, "**2")

    def test_incomplete_exp_1b(self):
        self.assertRaises(Error, parse, "2**")

    def test_incomplete_exp_2a(self):
        self.assertRaises(Error, parse, "^2")

    def test_incomplete_exp_2b(self):
        self.assertRaises(Error, parse, "2^")

    def test_total_garbage(self):
        self.assertRaises(Error, parse, '&HY]t9uUw"aT')

    def test_unbal_1(self):
        self.assertRaises(Error, parse, '(1+2*3')

    def test_unbal_2(self):
        self.assertRaises(Error, parse, '1+2)*3')

# M a i n   P r o g r a m

if __name__ == '__main__':
    unittest.main()
