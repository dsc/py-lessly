#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ('walk',)

from itertools import chain, repeat
from collections import Iterable, Mapping, Set, Sequence


def I(x, *args, **kwargs): return x

class walk(object):
    """ walk tree of iterables, emitting elements.
    """
    
    def __init__(self, it, containers=(list, tuple, Mapping, Set)):
        self.it = it
        self.containers = containers
    
    def __iter__(self):
        
        if isinstance(it, Mapping):
            return new(it, ( fn((k, walkmap(fn,v,new,containers))) if isinstance(v, containers) else fn((k,v)) for k,v in iteritems(it) ))
        else:
            return new(it, ( walkmap(fn, el, new, containers) if isinstance(el, containers) else fn(el) for el in iter(it) ))

class Walker(walk):
    """ A Walker walks a tree of iterables, invoking `leaf(val, key)` for each leaf,
        and `branch(container, key)` for each branch. Keys will be indices
        via `enumerate` for non-Mapping types.
        
        `containers`: a tuple of types which trigger recursion. Defaults to:
        (list, tuple, Mapping, Set).
        
    """
    containers = (list, tuple, Mapping, Set,)
    it = None
    
    
    def __init__(self, it=None):
        self.containers = tuple() if containers is None else containers
        self.it = it
    
    def newBranch(self, branch):
        return type(branch)()
    
    def leaf(self, val, key):
        return val
    
    def __iter__(self):
        return self.map(self.it)
    
    def map(self, it):
        



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

