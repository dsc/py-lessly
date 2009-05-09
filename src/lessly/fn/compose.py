from collections import namedtuple
from functools import partial, wraps
from inspect import getargspec
from lessly import items, cons, merge

__all__ = ('curry', 'compose', 'starcompose')

UnwrappedPartial = namedtuple('UnwrappedPartial', 'func args keywords')

def unwrap(fn):
    if isinstance(fn, partial):
        uw = unwrap(fn.func)
        return UnwrappedPartial(uw.func, uw.args+fn.args, merge(uw.keywords,fn.keywords))
    else:
        return UnwrappedPartial(fn, tuple(), {})

def curry(f):
    "A curried function."
    (f, args, kw) = unwrap(f)
    spec = getargspec(f)
    num_defs = len(spec.defaults or [])
    pos = len(spec.args) - num_defs
    openkw = set( spec.args[:-num_defs] )
    
    def curried( *args, **kw ):
        closedpos = set(spec.args[:len(args)])
        if pos > len(args) and len( openkw - closedpos - set(kw) ):
            return wraps(f)(partial(curried, *args, **kw))
        else:
            return f(*args, **kw)
    
    return wraps(f)(partial(curried, *args, **kw))

@curry
def compose(f, g, *fns):
    "The composition of f(g(*a, **kw))."
    g = g if not len(fns) else compose( *cons(g,fns) )
    
    @wraps(g)
    def composed(*args, **kwargs):
        return f( g(*args, **kwargs) )
    
    return composed

@curry
def starcompose(f, g, *fns):
    "The composition of f(*g(*a, **kw))."
    g = g if not len(fns) else starcompose( *cons(g,fns) )
    
    @wraps(g)
    def composed(*args, **kwargs):
        v = g(*args, **kwargs)
        if isinstance(v, dict):
            return f(**v)
        else:
            return f(*v)
    
    return composed

