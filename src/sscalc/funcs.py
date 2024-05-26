# I m p o r t s

from decimal import Decimal, ROUND_DOWN

from .exceptions import Error

# V a r i a b l e s

# We use this prefix so that e.g. our implementation of @SUM can call the
# Python sum builtin.
_FUNC_PREFIX = "f_"

# F u n c t i o n s

def _assertHasArgs(name, args):
    if len(args) < 1:
        raise Error(f"{name} requires at least one argument")

def _assertOneArg(name, args):
    if len(args) != 1:
        raise Error(f"{name} requires a single argument")

def _assert12Args(name, args):
    if len(args) not in set([1, 2]):
        raise Error(f"{name} requires 1 or 2 arguments")

def f_sum(*args):
    _assertHasArgs('@SUM')
    return sum(args)

def f_count(*args):
    return Decimal(len(args))

def f_min(*args):
    _assertHasArgs('@MIN')
    return min(args)

def f_max(*args):
    _assertHasArgs('@MAX')
    return max(args)

def f_average(*args):
    _assertHasArgs('@AVERAGE')
    return sum(args) / Decimal(len(args))

def f_abs(*args):
    _assertOneArg('@ABS')
    return abs(args[0])

def f_int(*args):
    _assertOneArg('@INT')
    return Decimal(int(args[0]))

def f_round(*args):
    _assert12Args('@ROUND')
    if len(args) == 1:
        return round(args[0])
    else:
        return round(args[0], int(args[1]))

def f_exp(*args):
    _assertOneArg('@EXP')
    return args[0].exp()

def f_ln(*args):
    _assertOneArg('@LN')
    return args[0].ln()

def f_log10(*args):
    _assertOneArg('@LOG10')
    return args[0].log10()

def f_sqrt(*args):
    _assertOneArg('@SQRT')
    return args[0].sqrt()
