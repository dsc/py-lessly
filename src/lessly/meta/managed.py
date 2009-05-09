import inspect
from functools import wraps

from lessly import curry
from lessly.collect.weakset import WeakSet
from lessly.meta.stack import find_calling_instance

@curry
def wrap_method(cls, method, name=None):
    if name is None:
        name = method.__name__
    
    if hasattr(cls, name):
        wrapped = getattr(cls, name)
        wrapper = wraps(wrapped)(method)
        wrapper._wrapped = wrapped
    else:
        wrapper = method
        wrapper._wrapped = lambda self, *args, **kw: None
    
    setattr(cls, name, wrapper)
    return wrapper

@curry
def innerclass(OuterType, InnerType, prop=None):
    "Attributes this class's instances to the calling OuterClass on instantiation."
    InnerType._outer_type = OuterType
    if prop is None:
        prop = OuterType.__name__.lower()
    
    @wrap_method(InnerType, name='__init__')
    def inner_init(self, *args, **kw):
        setattr(self, prop, find_calling_instance(self._outer_type))
        inner_init._wrapped(self, *args, **kw)
    
    return InnerType

