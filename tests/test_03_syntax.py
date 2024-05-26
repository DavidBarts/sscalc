# Testing what syntax we should (and should not) support. A few of these
# might end up duplicating basic tests.

# I m p o r t s

import os
import unittest
from decimal import Decimal, getcontext

from sscalc.exceptions import Error
from sscalc.model import table, make_table, ShlexReader
from sscalc.yacc import parse

class TestShlex(unittest.TestCase):
    def setUp(self):
        if not table:
            with ShlexReader(os.path.join("tests", "data", "basic.txt")) as reader:
                make_table(reader)

    def test_add(self):
        self.assertEqual(parse("1+1"), Decimal(2))

    def test_sub(self):
        self.assertEqual(parse("1-1"), Decimal(0))

    def test_mul(self):
        self.assertEqual(parse("2*3"), Decimal(6))

    def test_div(self):
        self.assertEqual(parse("1/3"), Decimal(1) / Decimal(3))

    def test_idiv(self):
        self.assertEqual(parse("1//3"), Decimal(0))

    def test_mod(self):
        self.assertEqual(parse("1%3"), Decimal(1))

    def test_exp(self):
        self.assertEqual(parse("2**3"), Decimal(8))

    def test_basic_exp(self):
        self.assertEqual(parse("2^3"), Decimal(8))

    def test_unary_plus(self):
        self.assertEqual(parse("2**+3"), Decimal(8))

    def test_unary_minus(self):
        self.assertEqual(parse("2**-3"), Decimal("0.125"))

    def test_call(self):
        self.assertEqual(parse("@sqrt(4)"), Decimal(2))

    def test_parens(self):
        self.assertEqual(parse("(1+2)*3"), Decimal(9))

    def test_order(self):
        self.assertEqual(parse("1+2*3"), Decimal(7))

    def test_range(self):
        self.assertEqual(parse("@count(b2:b4, b5)"), Decimal(4))

    def test_decimals(self):
        self.assertEqual(parse("100*.01"), Decimal(1))

    def test_frac_exp(self):
        self.assertEqual(parse("4**.5"), Decimal(2))
        
    def test_const(self):
        mine = Decimal("3.141592653589793238462643383280")
        theirs = parse("@pi")
        maxdiff = Decimal("0.1") ** getcontext().prec
        self.assertTrue(abs(mine - theirs) <= maxdiff)

# M a i n   P r o g r a m

if __name__ == '__main__':
    unittest.main()
