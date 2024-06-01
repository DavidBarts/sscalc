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
    iftype = parser.add_mutually_exclusive_group()
    iftype.add_argument("-c", "--csv", action="store_true", help="Read CSV input.")
    iftype.add_argument("-r", "--regex", action="store", default=None, help="Use specified regular expression to split into fields.")
    parser.add_argument("expression", type=str, nargs='+', help="Arithmetic expression(s) to evaluate.")
    args = parser.parse_args(argv)
    if args.csv:
        make_table(model.CsvReader())
    elif args.regex:
        make_table(model.RegexReader(args.regex))
    else:
        make_table(model.ShlexReader())
    for expression in args.expression:
        result = str(parse(expression))
        if not args.bare:
            sys.stdout.write(f"{expression} = ")
        sys.stdout.write(f"{result}\n")
