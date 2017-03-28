
from sys import stdout
from datetime import datetime as dt
from helpy.misc import flatten


class Timer:

    def __init__(self):
        self.start = dt.now()
        self.last = self.start
        self.log = Log()

    def total_seconds(self):
        return (dt.now() - self.start).total_seconds()

    def get_delta(self):
        return (dt.now() - self.last).total_seconds()

    def print_total(self):
        log.printf( 'Total runtime:', self.total_seconds(), 'seconds' )

    def print_delta(self):
        log.printf( '+', (now - self.last).total_seconds(), 'seconds' )

    def reset_delta(self):
        self.last = dt.now()


class Log:

    def __init__(self, indent_str='  ', prefix='', suffix='', join='', loglvl=0):
        self.indent_str = indent_str
        self.prefix = prefix
        self.suffix = suffix
        self.join = join
        self.num_indents = 0
        self.loglvl = loglvl

    def indent(self, n=1):
        self.num_indents = self.num_indents + n

    def dedent(self, n=1):
        self.num_indents = max(0, self.num_indents - n)

    def fmt(self, string, *args, **kwargs):
        'quicker printing of formatted strings'
        if 'loglvl' in kwargs and kwargs['loglvl'] < self.loglvl: return
        return (self.join).join( flatten(
            self.prefix,
            [ self.indent_str ] * self.num_indents,
            string.format( *args, **kwargs ),
            self.suffix ))

    def printf(self, string, *args, **kwargs):
        'formatted printing'
        if 'loglvl' in kwargs and kwargs['loglvl'] < self.loglvl: return
        print( self.fmt(string, *args, **kwargs) )

    def iprintf(self, string, *args, **kwargs):
        'inline formatted printing'
        if 'loglvl' in kwargs and kwargs['loglvl'] < self.loglvl: return
        stdout.write( self.fmt(string, *args, **kwargs) )
        stdout.flush()
