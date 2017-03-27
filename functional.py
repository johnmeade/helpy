'functional helpers to clean up functional code'


from functools import reduce


def identity(x):
    return x


def flip(f):
    '''Flip the order of arguments for a functions with two arguments.
    Especially useful with currying.

    Example:

    powflip = flip( math.pow )
    assert powflip(2,3) == 9

    # with currying:
    pow2 = curry( flip( math.pow ) )(2)
    assert pow2(3) == 9
    '''
    return lambda x, y: f(y, x)


def foldr(f, xs, acc=None):
    'Like reduce, but processes list elements from index -1 to index 0'
    if acc == None:
        lst = list(reversed(xs))
        return reduce(f, lst[1:], lst[0])
    else:
        return reduce(f, reversed(xs), acc)


def appended(lst, x):
    lst.append(x)
    return lst


def argsorted(lst, **kwa):
    '''Return the list of indices that sort the input list. This uses default
    python sorting key, optionally supply your own with the "key" keyword arg.
    examples:
    argsorted([49,52,31]) == [2,0,1]
    argsorted([49,52,31], key=lambda x: -x) == [1,0,2]
    '''

    # cast to list to handle python3 lazy functools
    xs = list(lst)

    # actual key function will receive a list index, so we wrap transformation
    # around the it.
    if 'key' in kwa:
        key = kwa['key']
        if not callable(key):
            raise Exception("Keyword argument 'key' must be callable")
        wrapped_key = lambda i: key( xs[i] )
    else:
        wrapped_key = xs.__getitem__

    return sorted(range(len(xs)), key=wrapped_key)
