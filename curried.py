'Curried helpers for cleaner funcitonal style programming'


import sys
import helpy.functional as fnc
from functools import reduce as py_reduce


if sys.version_info.major >= 3 and sys.version_info.minor >= 3:
    from inspect import signature
    def __arg_count__(f):
        return len( signature(f).parameters )
else:
    from inspect import getargspec
    def __arg_count__(f):
        return len( getargspec(f).args )


py_map = map
py_filter = filter


def curry(f):
    '''Curry simple functions, excluding any built-ins that are implemented in
    C. Some C functions (like reduce) are provided in this module. To curry
    other such built-in not in this module, you must wrap it in a python
    function or lambda like so:

    curried_max = curry(lambda x, y: max(x, y))
    max9 = curried_max(9)
    assert max9(8) == 9
    assert max9(13) == 13

    Note that this implementation tried to be
    immutable, ie the following will not work:

    foo = lambda x, y, z: x+y+z
    f = curry( foo )
    f(9)
    f(8) # independent from the above line
    f(7) # again, just creates a new instance

    Instead, a new instance is returned at each evaluation, so for example the
    following works:

    foo = lambda x, y, z: x+y+z
    f = curry( foo )(9)
    g = f(8)
    assert g(7) == 9+8+7
    assert g(6) == 9+8+6
    assert f(5)(2) == 9+5+2
    '''
    n = __arg_count__(f)
    return __curry__(f, n-1, [])


def __curry__(f, n, args):
    '''Curries the first n args of f, keeping track of all passed args along the
    way. The final call will spread the arg list into the actual call to f.
    '''
    # Note that we need to make a copy of the args list to stop python from
    # using the same one for repeated calls. For example, without this the
    # following will fail on the last statement:
    # `f=lambda x,y: x+y; g=curry(f)(1); g(2); g(3)`
    if n == 0: return lambda x: f( *fnc.appended(args[:], x) )
    else: return lambda x: __curry__( f, n-1, fnc.appended(args[:], x) )



def pipe(*fns):
    '''Apply functions in pipe-order and curry the argument. Note that this
    currently only works with functions that take one arg, so you may want
    to wrap all args into a list.

    Example:

    f(g(h(x))) == pipe(h,g,f)(x)
    '''
    return lambda x: py_reduce(lambda acc, f: f(acc), fns, x)


#
#  Faster currying for common functions (and built-ins)
#


def eq(val): return lambda x: x == val
def not_eq(val): return lambda x: x != val
def lt(val): return lambda x: x < val
def lte(val): return lambda x: x <= val
def gt(val): return lambda x: x > val
def gte(val): return lambda x: x > val


def startswith(s):
    return lambda x: x.startswith(s)


def endswith(s):
    return lambda x: x.endswith(s)


def map(f):
    return lambda lst: py_map(f, lst)


def filter(f):
    return lambda lst: py_filter(f, lst)


def reduce(f):
    # can't use default args with lambdas, need full py function defs
    def _list(lst):
        def _init(init=None):
            if init == None: return py_reduce(f, lst)
            else: return py_reduce(f, lst, init)
        return _init
    return _list


def sort_by(f):
    return lambda lst: sorted(lst, key=f)


def argsort_by(f):
    return lambda lst: fnc.argsorted(lst, key=f)
