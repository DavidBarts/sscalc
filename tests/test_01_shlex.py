# Basic tests of operating on the default (shlex) input format.

# I m p o r t s

import os
import unittest
from decimal import Decimal

from sscalc.exceptions import Error
from sscalc.model import table, make_table, ShlexReader
from sscalc.yacc import parse

class TestShlex(unittest.TestCase):
    def setUp(self):
        if not table:
            with ShlexReader(os.path.join("tests", "data", "basic.txt")) as reader:
                make_table(reader)

    def test_access_numeric(self):
        self.assertEqual(parse("b2"), Decimal(594))

    def test_access_nonnumeric(self):
        self.assertRaisesRegex(Error, "A1.*not numeric", parse, "A1")

    def test_access_notexist(self):
        self.assertRaisesRegex(Error, "Z1.*not exist", parse, "Z1")

    def test_final_row(self):
        self.assertEqual(parse("b5"), Decimal(594))

    def test_beyond_final(self):
        self.assertRaisesRegex(Error, "not exist", parse, "b6")

    def test_count(self):
        # part of testing we can read all data cells
        self.assertEqual(parse("@count(b2:b5)"), Decimal(4))

    def test_sum(self):
        # part of testing we can read all data cells
        self.assertEqual(parse("@sum(b2:b5)"), Decimal(3961))

# M a i n   P r o g r a m

if __name__ == '__main__':
    unittest.main()
