# I m p o r t s

import sys
import argparse

from .exceptions import Error
from .model import make_table, table
from .yacc import parse

# F u n c t i o n s

def run(argv):
    parser = argparse.ArgumentParser(description="Spreadsheet-like calculator.")
    parser.add_argument("-b", "--bare", action="store_true", help="Output only results, not expressions.")
    parser.add_argument("-c", "--csv", action="store_true", help="Read CSV input.")
    parser.add_argument("expression", type=str, nargs='+', help="Arithmetic expression(s) to evaluate.")
    args = parser.parse_args(argv)
    if args.csv:
        make_table(model.CsvReader())
    else:
        make_table(model.ShlexReader())
    for expression in args.expression:
        result = str(parse(expression))
        if not args.bare:
            sys.stdout.write(f"{expression} = ")
        sys.stdout.write(f"{result}\n")
