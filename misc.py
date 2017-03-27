'''
Utilities for common tasks in making Python scripts
'''


import os
from os import makedirs, getcwd
from os.path import join, exists
from datetime import datetime as dt
from helpy.curried import curry


DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%Hh%Mm%Ss'
DATETIME_FORMAT = '_'.join([ DATE_FORMAT, TIME_FORMAT ])


def do(generator):
    '''Execute generator to completion, throwing away results.
    Example:
    do( makedirs(p) for p in paths if not exists(p) )
    '''
    for _ in generator: pass


def ensure_folders(folders, root=getcwd()):
    "Make all supplied directories if they don't already exist"
    prefixed = curry(join)(root)
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
