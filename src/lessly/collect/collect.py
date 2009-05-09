""" Operations on collections.
"""
__all__ = ('items', 'cons', 'merge', 'isany', 'isall', 'weave')

from itertools import chain


def cons(hd, tl):
    return (hd,)+tl

def items( *cs, **kw ):
    return chain(*[ c.iteritems() if isinstance( c, dict ) else iter(c)
        for c in cs+(kw,) if c is not None ])

def merge( *cs, **kw ):
    return type(cs[0] if cs and cs[0] is not None else kw)( items(*cs,**kw) )

def isany( f, xs ):
    for x in xs:
        if f(x):
            return True
    return False

def isall( f, xs ):
    for x in xs:
        if not f(x):
            return False
    return True

def weave( *iterables ):
    iterables = map(iter, iterables)
    while iterables:
        for it in iterables[:]:
            try:
                yield it.next()
            except StopIteration:
                iterables.remove(it)

