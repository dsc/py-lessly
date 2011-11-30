__all__ = ('Symbol', 'NULL',)

from collections import namedtuple


class Symbol(namedtuple('Symbol', 'val nonzero')):
    def __iter__(self, val, nonzero=None):
        super(Symbol, self).__init__( (val, bool(nonzero or val)) )
    def __nonzero__(self):
        return self.nonzero
    def __str__(self):
        return ':'+self.val

NULL = Symbol('null', False)


