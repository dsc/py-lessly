#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Operations on collections.
"""

__all__ = (
    'get_dotted', 'set_dotted', 'del_dotted', 'has_dotted',
    'items', 'cons', 'merge',
    'xpluck', 'xpluckattr', 'pluck', 'pluckattr', 'xinvoke', 'invoke',
    'find', 'uniqued', 'isany', 'isall', 'is_any', 'is_all',
    'batch', 'weave', 'walk', 'walkmap', 'walkBreadthFirst', 'walkDepthFirst',
)

from operator import eq
from itertools import chain, repeat
from collections import Iterable, Mapping, Set, Sequence

from .dict import get_dotted, set_dotted, del_dotted, has_dotted


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



def xpluck(it, key, default=None):
    "Gets given key from each dict in iterable, yielding results."
    for d in it:
        yield d.get(key, default)

def pluck(it, key, default=None):
    "Gets given key from each dict in iterable, returning list of results."
    return list(xpluck(it, key, default))

def xpluckattr(it, attr, default=None):
    "Gets given attribute from each object in iterable, yielding results."
    for o in it:
        yield getattr(o, name, default)

def pluckattr(it, key, default=None):
    "Gets given attribute from each object in iterable, returning list of results."
    return list(xpluckattr(it, key, default))


def xinvoke(it, attr, *args, **kwargs):
    "Invokes method of each object in iterable, yielding the results."
    for o in it:
        m = getattr(o, attr)
        yield m(*args, **kwargs)

def invoke(it, attr, *args, **kwargs):
    "Invokes method of each object in iterable, returning list of results."
    return list(xinvoke(it, attr, *args, **kwargs))


def find(it, test=bool, default=None):
    "Returns the first item for which the test returns truth-y."
    for v in it:
        if test(v): return v
    return default

def uniqued(it):
    "Create a copy of the iterable with only unique values."
    if isinstance(it, (set, frozenset)):
        return type(it)(it)
    if isinstance(it, dict):
        values = set()
        out = {}
        for k, v in it.items():
            if v in values: continue
            values.add(v)
            out[k] = v
    else:
        out = []
        for v in it:
            if v not in out: out.append(v)
        # convert to tuple or whatever if necessary
        if isinstance(it, basestring):
            out = ''.join(out)
        elif not isinstance(it, list):
            out = type(it)(out)
    return out


def isany(it, test=bool):
    "True if `test(x)` for any `x` in the iterable."
    for x in it:
        if test(x): return True
    return False

def isall(it, test=bool):
    "True if `test(x)` for any `x` in the iterable."
    for x in it:
        if not test(x): return False
    return True

is_any = isany
is_all = isall



def batch(it, n, fill_with=None):
    """ A filter that batches items. It works pretty much like `slice`
        just the other way round. It returns a list of lists with the
        given number of items. If you provide a second parameter this
        is used to fill missing items. See this example:
        
        .. sourcecode:: html+jinja
            
            <table>
            {%- for row in items|batch(3, '&nbsp;') %}
              <tr>
              {%- for column in row %}
                <td>{{ column }}</td>
              {%- endfor %}
              </tr>
            {%- endfor %}
            </table>
    """
    result = []
    tmp = []
    for item in it:
        if len(tmp) == n:
            yield tmp
            tmp = []
        tmp.append(item)
    if tmp:
        if fill_with is not None and len(tmp) < n:
            tmp += [fill_with] * (n - len(tmp))
        yield tmp



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



def weave(*iterables):
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


def walk(root, depthFirst=True):
    return walkDepthFirst(root) if depthFirst else walkBreadthFirst(root)

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
    while parents:
        try:
            child = parent.next()
        except StopIteration:
            parent = iter(parents.pop(0))
            continue
        if isinstance(child, Iterable) and not isinstance(child, basestring):
            parents.append(child)
        yield child


def ncycles(it, n):
    "Iterates the sequence elements n times"
    return chain.from_iterable(repeat(it, n))


