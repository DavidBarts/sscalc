# I m p o r t s

import os, sys
import csv
import shlex
import re
from .exceptions import Error
from decimal import Decimal, InvalidOperation

# V a r i a b l e s

_ENCODING = 'UTF-8'

# Our data model, a list of lists, representing the spreadsheet. A cell is
# a Decimal if it can be parsed as a Decimal value, else a string.
table = []

# C l a s s e s

class SplittingReader(object):
    def read(self):
        raise NotImplementedError("read not defined")

    def close(self):
        raise NotImplementedError("close not defined")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

class ShlexReader(SplittingReader):
    def __init__(self, file_name=0):
        self._fp = open(file_name, encoding=_ENCODING)
        self._line = 0

    def read(self):
        line = self._fp.readline()
        if not line:
            return None
        self._line += 1
        try:
            return shlex.split(line, comments=True)
        except ValueError as e:
            message = str(e) or "shlex syntax error"
            raise Error(f"line {self._line}: {message}")

    def close(self):
        self._fp.close()

class RegexReader(SplittingReader):
    def __init__(self, regex, file_name=0):
        self._regex = re.compile(regex)
        self._fp = open(file_name, encoding=_ENCODING)

    def read(self):
        line = self._fp.readline()
        if not line:
            return None
        return self._regex.split(line[:-1] if line.endswith("\n") else line)

class CsvReader(SplittingReader):
    def __init__(self, file_name=0):
        self._fp = open(file_name, encoding=_ENCODING, newline='')
        self._rdr = csv.reader(self._fp)

    def read(self):
        return next(self._rdr, None)

    def close(self):
        self._fp.close()

# F u n c t i o n s

def make_table(reader):
    global table
    table.clear()
    while True:
        raw = reader.read()
        if raw is None:
            break
        table.append([ _coerce_decimal(x) for x in raw ])

def _coerce_decimal(raw):
    try:
        return Decimal(raw)
    except InvalidOperation:
        return raw
