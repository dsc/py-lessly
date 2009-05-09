__all__ = ('innerclass', 'tracked')

from weakref import WeakKeyDictionary
from functools import wraps
from lessly.fn import curry
from lessly.meta.stack import find_calling_instance
from lessly.actor.announcer import Announcer, AnnouncingMethod, AnnouncingClassMethod


@curry
def innerclass(OuterCls, InnerCls, prop=None):
    """ Class decorator. Attributes this class's instances to the calling 
        OuterClass on instantiation.
    """
    InnerCls._outer_type = OuterCls
    if prop is None:
        prop = OuterCls.__name__.lower()
    
    wrapped = InnerCls.__init__ if hasattr(InnerCls, '__init__') else None
    def inner_init(self, *args, **kw):
        setattr(self, prop, find_calling_instance(self._outer_type))
        if wrapped:
            wrapped(self, *args, **kw)
    
    InnerCls.__init__ = wraps(wrapped)(inner_init) if wrapped else inner_init
    return InnerCls

@curry
def tracked(cls, prop='instances'):
    if Announcer not in cls.__bases__:
        cls.__new__ = AnnouncingClassMethod(cls.__new__)
    
    instances = WeakKeyDictionary()
    setattr(cls, prop, instances)
    
    def add_instance(name, cls, instance, *args, **kw):
        instances[cls] = {}
    
    cls.__new__.listen()
    return cls