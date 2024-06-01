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

1.  I tend to create simple “spreadsheets” as text files
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

sscalc \[ *options* \] *expression* \[...\]

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
    @sum(b2:b5) = 3961.00

More Examples
-------------

### Case Insensitivity

Like traditional spreadsheets, the expression language is
case-insensitive:

    $ sscalc "@SUM(B2:B5)" < liability.txt
    @SUM(B2:B5) = 3961.00

### Extracting a Single Column

    $ sscalc b2 < liability.txt
    b2 = 594.00

This can be useful to verify that one is pulling in the correct cells:

    $ sscalc b2 b5 "@sum(b2:b5)" < liability.txt
    b2 = 594.00
    b5 = 594.00
    @sum(b2:b5) = 3961.00

### Suppressing Expression Output

The `-b`/`--bare` option will cause the outputting of expressions to be
suppressed:

    $ sscalc --bare b2 < liability.txt
    594.00

### Only Numeric Cells Can Be Referred To

This is because an expression’s cell references are intended to be
operated on arithmetically:

    $ sscalc -b "@sum(a2:a5)" < liability.txt
    sscalc: A2:A5 - A2 is not numeric

### Controlling Rounding

Sscalc uses Python’s built-in `decimal` library for its arithmetic, and
follows its default rules for significant figures (which match the
standard ones you learned in arithmetic class). Normally this produces
reasonable output, but sometimes you get meaningless fractional cents,
such as when applying an exchange rate:

    $ sscalc b2*1.3467 < liability.txt
    b2*1.3467 = 799.939800

In that case, `@ROUND` can be useful:

    $ sscalc '@round(b2*1.3467,2)' < liability.txt
    @round(b2*1.3467,2) = 799.94

So-called “bankers’” rounding is used:

    $ sscalc '@round(121.5)' < /dev/null
    @round(121.5) = 122
    $ sscalc '@round(122.5)' < /dev/null
    @round(122.5) = 122

Other forms of rounding can be achieved with judicious use of `@INT`:

    $ sscalc '@int(122.5 + .5)' < /dev/null
    @int(122.5 + .5) = 123

### White Space Is Ignored in Expressions

    $ sscalc -b "@sum(b2 : b5)" < liability.txt
    3961.00

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

### Splitting into Fields with Regular Expressions

The `-r` or `--regex` may be used to specify a (Python) regular
expression, which will be used instead of shlex to split the input into
fields. For example, `--regex='\s+'` will use runs of one or more
whitespace characters as delimiters.

Operators
---------

The following arithmetic operators are available:

`+` `-` `*` `/`  
Addition, subtraction, multiplication, and division (the latter being
decimal floating point division, not integer division).

`//` `%`  
Integer division and modulus.

`**` `^`  
Exponentiation (the two forms are equivalent).

`(` `)`  
For grouping and to force precedence of evaluation.

Pre-Defined Constants
---------------------

There is one pre-defined constant, `@PI`, the ratio of a circle’s
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
Accepts one or two arguments. With one argument, performs bankers’
rounding to the nearest integer. With two arguments, performs bankers’
rounding to the specified number of decimal places.

`@SQRT`  
Accepts a single argument, and returns the square root of that argument.

`@SUM`  
Accepts one or more arguments, and returns the sum of its arguments.

### Ranges in Function Arguments

A function argument may be of the form *ref*`:`*ref*, where *ref* is a
valid cell reference (e.g. `A10`, `C3`, etc.) This will cause all cells
in the rectangular range from the first (upper left) to the second
(lower right) cell to be passed as arguments. It is an error if any cell
in the region is non-numeric or does not exist.
