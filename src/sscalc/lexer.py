# I m p o r t s

from ply import lex

from .exceptions import Error

# V a r i a b l e s

# Standard token types this lexer supports. We SHOUT here so that
# terminals (i.e. these lex tokens) can be distinguished as what they are
# in the compile (yacc) stage. XXX - This DOES NOT define the order in
# which tokens are recognized, see:
# https://ply.readthedocs.io/en/latest/ply.html#lex
tokens = (
    'ADDSUB',
    'MULDIV',
    'EXPO',
    'RANGE',
    'ARGSEP',
    'LPAREN',
    'RPAREN',
    'REFERENCE',
    'IDENTIFIER',
    'NUMBER',
)

# F u n c t i o n s

# We define all tokens with functions, even for simple tokens that result
# in dummy functions. This is because using functions lets us impose our
# own ordering priority on things. Using string scalars causes PLY to
# impose its own order, based on crude regex length.

def t_WHITESPACE(t):
    r'\s+'
    pass  # ignore all whitespace

def t_NUMBER(t):
    r'(\d+\.\d+|\d+\.?|\.\d+)([Ee][+-]?\d+)?'
    return t

def t_ADDSUB(t):
    r'\+|-'
    return t

# must precede MULDIV to grab ** before *
def t_EXPO(t):
    r'\^|\*\*'
    return t

def t_MULDIV(t):
    r'\*|//|/|%'
    return t

def t_RANGE(t):
    r':'
    return t

def t_ARGSEP(t):
    r','
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_REFERENCE(t):
    r'[A-Za-z]\d+'
    return t

def t_IDENTIFIER(t):
    r'@\w+'
    return t

# PLY requires we define this one.

def t_error(t):
    offset = t.lexer.lexpos
    raise Error(f"invalid token at offset {offset}")

# Build the lexer object

lexer = lex.lex()
