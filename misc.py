'''
Utilities for common tasks in making Python scripts. This is a base file that
should not import from anything else in this package.
'''


import os
from os import makedirs, getcwd
from os.path import join, exists
from datetime import datetime as dt


DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%Hh%Mm%Ss'
DATETIME_FORMAT = '_'.join([ DATE_FORMAT, TIME_FORMAT ])


def flatten(*x):
    '''Append all passed args to the input list. Args can be any
    Example:
    flatten( [1,2], 3 )
    >>> [1, 2, 3]
    flatten( [1,2], [(3,[2,6,(9,8,7)]),[4,5]], 4 )
    >>> [1, 2, 3, 2, 6, 9, 8, 7, 4, 5, 4]
    '''
    lst = []
    for y in x:
        t = type(y)
        if t == list or t == tuple:
            for z in flatten(*y):
                lst.append(z)
        else:
            lst.append(y)
    return lst


def do(generator):
    '''Execute generator to completion, throwing away results.
    Example:
    do( makedirs(p) for p in paths if not exists(p) )
    '''
    for _ in generator: pass


def ensure_folders(folders, root=getcwd()):
    "Make all supplied directories if they don't already exist"
    prefixed = lambda x: join(root, x)
    do( makedirs(d) for d in map(prefixed, folders) if not exists(d) )


def datetime_str(format=DATETIME_FORMAT):
    "get a timestamp"
    return dt.strftime( dt.now(), format )


def assertion(value_of=None, type_of=None, is_one_of=None):
    'assert something, ex: `assertion(type_of=x, is_one_of=[int, str])`'

    if value_of != None and type_of != None:
        raise Exception("Don't supply both a 'value_of' and a 'type_of' arg")

    elif value_of != None and value_of not in is_one_of:
        raise AssertionError( "value of {} is not in {}".format(
            value_of, is_one_of) )

    elif type_of != None:
        typ = type(type_of)
        if typ not in is_one_of:
            raise AssertionError( "type of {} ({}) is not in {}".format(
                type_of, typ, is_one_of) )
