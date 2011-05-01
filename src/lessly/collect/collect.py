""" Operations on collections.
"""
__all__ = ('items', 'cons', 'merge', 'isany', 'isall', 'weave', 'walkmap')

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

def partition(it, sep):
    """ Partitions an iterable at the first occurrence of sep, and return a 3-tuple
        containing the list of items before the separator, the separator itself,
        and the unexhausted iterator. If the separator is not found, return a 3-tuple of
        (the exhausted iterable as a list, None, []).
    """
    before = []
    it = iter(it)
    for val in it:
        if val == sep:
            break
        else:
            before.append(val)
    else:
        return (before, None, [])
    return (before, sep, it)

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

def walkmap(fn, it, new=None, containers=(list, tuple, Mapping, Set)):
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
        return new(it, ( fn((k, walkmap(fn,v,new,containers))) if isinstance(v, containers) else fn((k,v)) for k,v in iteritems(it) ))
    else:
        return new(it, ( walkmap(fn, el, new, containers) if isinstance(el, containers) else fn(el) for el in iter(it) ))



def walkDepthFirst(root):
    """ Walks a heirarchy of iterables depth-first, emitting the elements.
    """
    parent = iter(root)
    parents = [[]]
    child = None
    while parents:
        try:
            child = parent.next()
        except StopIteration:
            if parents:
                parent = iter(parents.pop())
                continue
            else:
                break
        yield child
        if isinstance(child, Iterable) and not isinstance(child, basestring):
            parents.append(parent)
            parent = iter(child)


def walkBreadthFirst(root):
    parent = iter(root) #<-- if this were iter([]), and
    parents = [[]]      #<-- this were [root], we'd see starting element in results
    child = None
    while parts:
        try:
            child = parent.next()
        except StopIteration:
            parent = iter(parents.pop(0))
            continue
        if isinstance(child, Iterable) and not isinstance(child, basestring):
            parents.append(child)
        yield child


