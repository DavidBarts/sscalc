sscalc: a SpreadSheet CALCulator
================================

Introduction
------------

This program reads UTF-8 text from standard input, which can be either
whitespace-delimited or in CSV form, turns any field that can be parsed
as a number into a number, then evaluates the passed expression as if it
were an expression in a spreadsheet. Calculations are performed using
decimal arithmetic, not binary floating point.

I wrote sscalc because:

1.  I tend to create simple "spreadsheets" as text files
2.  I do not like how all standard spreadsheet programs use binary
    floating point (instead of decimal) for calculations (this can cause
    errors with financial data).

The main goal has been to create something simple that suits my
purposes.

Requirements
------------

Sscalc requires [PLY (Python Lex-Yacc)](https://github.com/dabeaz/ply).
Beyond that, it has no prerequisites other than a working install of
Python 3.11 or greater.

Installing
----------

    python3 setup.py build
    python3 setup.py install

Command Syntax
--------------

sscalc \[ *options* \] *expression*

An Example
----------

Given the following as the contents of `liability.txt`:

    DATE             AMOUNT
    2023-05-15       594.00
    2023-05-17      2222.00
    2023-07-06       551.00
    2023-12-14       594.00
    ------------------------

Then:

    $ sscalc "@sum(b2:b5)" < liability.txt
    3961.0000

More Examples
-------------

### Case Insensitivity

Like traditional spreadsheets, the expression language is
case-insensitive:

    $ sscalc "@SUM(B2:B5)" < liability.txt
    3961.0000

### Extracting a Single Column

    $ sscalc b2 < liability.txt
    594.0000

### Only Numeric Columns Can Be Referred To

This is because an expression's column references are intended to be
operated on arithmetically:

    $ sscalc "@sum(a2:a5)" < liability.txt
    sscalc: A2:A5 - A2 is not numeric

### Controlling Rounding

By default, sscalc rounds to four decimal places. The `-p` or `--places`
option may be used to change this:

    $ sscalc -p 2 b2 < liability.txt
    594.00

So-called "bankers'" rounding is used:

    $ sscalc -p 0 '121.5' < /dev/null
    122
    $ sscalc -p 0 '122.5' < /dev/null
    122

Other forms of rounding can be achieved with judicious use of `@INT`:

    $ sscalc -p 0 '@int(122.5 + .5)' < /dev/null
    123

### White Space Is Ignored in Expressions

> $ sscalc "@sum(b2 : b5)" &lt; liability.txt 3961.0000

### White Space in Columns

By default, sscalc uses `shlex` to parse a row into columns. In other
words, columns are delimited by runs of one or more whitespace
characters, and single or double quotes must be used if input data
itself contains spaces:

    NAME                                   SYMBOL          SHARES
    "Microsoft Corporation"                MSFT            2.9024
    "Apple, Inc."                          AAPL            5.5723
    "Berkshire Hathaway, Inc."             BRK.B           1.2576
    "Eli Lilly and Company"                LLY             8.0921

If you were not to do this, then it would be hard to refer to the count
of shares as column 3, because the name would get parsed as anything
from two to four columns in the above example.

The other way to work around this is of course to use CSV data (see
below).

### CSV Data

The `-c` or `--csv` option will cause standard input to be parsed as
CSV.

Pre-Defined Constants
---------------------

There is one pre-defined constant, `@PI`, the ratio of a circle's
circumference to its diameter.

Built-In Functions
------------------

`@ABS`  
Accepts a single argument, and returns the absolute value of that
argument.

`@AVERAGE`  
Accepts one or more arguments, and returns the arithmetic mean of the
passed values.

`@COUNT`  
Returns the count of its arguments.

`@EXP`  
Accepts a single argument, and returns *e* to the power of that
argument. This is the inverse function to `@LN`.

`@INT`  
Accepts a single argument, and returns the integer portion of that
argument.

`@LN`  
Accepts a single argument, and returns the natural logarithm of that
argument.

`@LOG10`  
Accepts a single argument, and returns the common (base 10) logarithm of
that argument.

`@MAX`  
Accepts one or more arguments, and returns the greatest argument.

`@MIN`  
Accepts one or more arguments, and returns the least argument.

`@ROUND`  
Accepts one or two arguments. With one argument, performs bankers'
rounding to the nearest integer. With two arguments, performs bankers'
rounding to the specified number of decimal places.

`@SQRT`  
Accepts a single argument, and returns the square root of that argument.

`@SUM`  
Accepts one or more arguments, and returns the sum of its arguments.

### Ranges in Function Arguments

A function argument may be of the form *ref*`:`*ref*, where *ref* is a
valid cell reference (e.g. `A10`, `C3`, etc.) This will cause all
arguments in the rectangular range from the first (upper left) to the
second (lower right) cell to be passed. It is an error if any cell in
the region is non-numeric or does not exist.
