""" Operations on collections.
"""
__all__ = ('items', 'cons', 'merge', 'isany', 'isall', 'weave', 'walk')

from itertools import chain
from collections import Iterable, Mapping, Set, Sequence


def cons(hd, tl):
    return (hd,)+tl

def iteritems(it, index=False):
    "Attempts to return an Iterator of (key, value) pairs."
    if hasattr(it, 'iteritems') and callable(it.iteritems):
        for kv in it.iteritems():
            yield kv
    elif isinstance(it, Mapping):
        for k in it:
            yield (k, it[k])
    elif isinstance(it, Sequence):
        if index:
            for v in it:
                yield (it.index(v), v)
        else:
            for iv in enumerate(it):
                yield iv
    else:
        raise TypeError("Iterable %s is not mappable or indexable" % type(it).__name__)

def items( *cs, **kw ):
    return chain(*[ iteritems(c) if isinstance(c, Mapping) else iter(c) for c in cs+(kw,) if c ])

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
    """ Breadth-first iteration across the iterable's elements. With iterables
        of mixed-length, exhausted collections are skipped.
        
        >>> ''.join(weave( 'abc', '  ', '123' ))
        'a 1b 2c3'
    """
    iterables = map(iter, iterables)
    while iterables:
        for it in iterables[:]:
            try:
                yield it.next()
            except StopIteration:
                iterables.remove(it)

def walk(fn, it, new=None, containers=(list, tuple, Mapping, Set)):
    """ Recursively maps all elements in a potentially hierarchical iterable
        `it`, returning an iterable of the same shape. Mappings emit (key, value) 
        pairs as their elements (acquired using lessly.collect.items()).
        
        `new`: a callable new(iterable, data) -> new_iterable invoked 
        when a new instance of a mapped iterable is needed.
        
        `containers`: a tuple of types which trigger recursion. Defaults to: 
        (list, tuple, Mapping, Set).
    """
    if new is None:
        def new(c, data):
            return type(c)(data)
        
    if isinstance(it, Mapping):
        return new(it, ( fn((k, walk(fn,v,new,containers))) if isinstance(v, containers) else fn((k,v)) for k,v in iteritems(it)))
    else:
        return new(it, (walk(fn, el, new, containers) if isinstance(el, containers) else fn(el) for el in iter(it)))

