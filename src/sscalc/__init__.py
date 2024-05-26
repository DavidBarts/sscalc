# I m p o r t s

import argparse

from .exceptions import Error
from .model import make_table
from .yacc import parse

# F u n c t i o n s

def run(argv):
    parser = argparse.ArgumentParser(description="Spreadsheet-like calculator.")
    parser.add_argument("-c", "--csv", action="store_true", help="Read CSV input.")
    parser.add_argument("-p", "--places", action="store", type=int, default=4, help="Places to round output to.")
    parser.add_argument("expression", type=str, nargs=1, help="expression")
    args = parser.parse_args(argv)
    if args.csv:
        make_table(model.CsvReader())
    else:
        make_table(model.ShlexReader())
    result = parse(args.expression[0])
    print(round(result, args.places))
