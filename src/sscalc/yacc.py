# Overall grammar:
# expr : LPAREN expr RPAREN
#      | expr ADDSUB expr
#      | expr MULDIV expr
#      | expr EXPO expr
#      | ADDSUB expr %prec UNARY
#      | NUMBER
#      | REFERENCE
#      | IDENTIFIER  ! constant
#      | IDENTIFIER LPAREN params RPAREN  ! call
# params : param
#        | params ARGSEP param
# param : expr
#       | REFERENCE RANGE REFERENCE

# I m p o r t s

from decimal import Decimal
from ply import yacc

from .exceptions import Error
from .lexer import tokens  # required by PLY
from .model import table
from . import funcs

# V a r i a b l e s

# Define precedence global here if needed

_ADDSUB_DISPATCH = {
    '+' : lambda a, b: a + b,
    '-' : lambda a, b: a - b,
}

_MULDIV_DISPATCH = {
    '*' : lambda a, b: a * b,
    '/' : lambda a, b: a / b,
    '//' : lambda a, b: a // b,
    '%' : lambda a, b: a % b,
}

_CONSTANTS = {
    "@PI": Decimal("3.141592653589793238462643383280"),
}

# Operator precedence

precedence = (
    ('left', 'ADDSUB'),
    ('left', 'MULDIV'),
    ('right', 'EXPO'),
    ('right', 'UNARY'),
)

# F u n c t i o n s

# The only one that is intended to be called extrnally.

def parse(expression):
    parser = yacc.yacc()
    return parser.parse(expression)

# Helpers for going from spreadsheet-style cell designators to row and
# column indices.

def _getcoords(refspec):
    if refspec == "" or refspec[0] < 'A' or refspec[0] > 'Z':
        raise Error(f"{refspec!r} - invalid reference specification")
    col = ord(refspec[0]) - ord('A')
    try:
        row = int(refspec[1:]) - 1
    except ValueError:
        raise Error(f"{refspec!r} - invalid reference specification")
    if row >= len(table) or col >= len(table[row]):
        raise Error(f"{refspec!r} - cell does not exist")
    return row, col

def _getcell(r, c):
    return chr(ord('A') + c) + str(r + 1)

def _getrange(start, end):
    accum = []
    start = start.upper()
    end = end.upper()
    sr, sc = _getcoords(start)
    er, ec = _getcoords(end)
    if sc > ec or sr > er:
        raise Error(f"{start}:{end} - starting greater than ending")
    for r in range(sr, er+1):
        lim = len(table[r])
        for c in range(sc, ec+1):
            if c >= lim:
                cell = _getcell(r, c)
                raise Error(f"{start}:{end} - {cell} does not exist")
            val = table[r][c]
            if isinstance(val, Decimal):
                accum.append(val)
            else:
                cell = _getcell(r, c)
                raise Error(f"{start}:{end} - {cell} is not numeric")
    return accum

# expr

def p_expr_lparen_expr_rparen(p):
    'expr : LPAREN expr RPAREN'
    p[0] = p[2]

def p_expr_expr_addsub_expr(p):
    'expr : expr ADDSUB expr'
    p[0] = _ADDSUB_DISPATCH[p[2]](p[1], p[3])

def p_expr_expr_muldiv_expr(p):
    'expr : expr MULDIV expr'
    p[0] = _MULDIV_DISPATCH[p[2]](p[1], p[3])

def p_expr_expr_expo_expr(p):
    'expr : expr EXPO expr'
    p[0] = p[1] ** p[3]

def p_expr_addsub_expr(p):
    'expr : ADDSUB expr %prec UNARY'
    p[0] = -p[2] if p[1] == '-' else p[2]

def p_expr_number(p):
    'expr : NUMBER'
    p[0] = Decimal(p[1])

def p_expr_reference(p):
    'expr : REFERENCE'
    ref = p[1].upper()
    r, c = _getcoords(ref)
    if r >= len(table) or c >= len(table[r]):
        raise Error(f"{ref} does not exist")
    val = table[r][c]
    if isinstance(val, Decimal):
        p[0] = val
    else:
        raise Error(f"{ref} is not numeric")

# constant
def p_expr_identifier(p):
    'expr : IDENTIFIER'
    const = p[1].upper()
    try:
        p[0] = _CONSTANTS[const]
    except KeyError:
        raise Error(f"{const} - constant does not exist")

# call
def p_expr_identifier_lparen_params_rparen(p):
    'expr : IDENTIFIER LPAREN params RPAREN'
    func = p[1].upper()
    try:
        p[0] = getattr(funcs, funcs._FUNC_PREFIX + p[1][1:].lower())(*p[3])
    except AttributeError:
        func = p[1].upper()
        raise Error(f"{func} - function does not exist")

# params

def p_params_param(p):
    'params : param'
    p[0] = p[1]

def p_params_params_argsep_param(p):
    'params : params ARGSEP param'
    p[0] = p[1] + p[3]

# param

def p_param_expr(p):
    'param : expr'
    p[0] = (p[1],)

def p_param_reference_range_reference(p):
    'param : REFERENCE RANGE REFERENCE'
    p[0] = tuple(_getrange(p[1], p[3]))
