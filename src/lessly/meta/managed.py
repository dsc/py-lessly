__all__ = ('innerclass', 'tracked', 'trackedinner')

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
    
    def set_outer(_name, _cls, _instance, *args, **kw):
        setattr(_instance, prop, find_calling_instance(_instance._outer_type))
    
    if issubclass(InnerCls, Announcer):
        InnerCls.__new__.listen(set_outer)
        
    else:
        wrapped = InnerCls.__init__ if hasattr(InnerCls, '__init__') else None
        def inner_init(self, *args, **kw):
            cls = self.__class__
            set_outer(cls.__name__, cls, self, *args, **kw)
            if wrapped:
                wrapped(self, *args, **kw)
        
        InnerCls.__init__ = wraps(wrapped)(inner_init) if wrapped else inner_init
    
    return InnerCls

@curry
def tracked(cls, prop='instances'):
    """ Class decorator. Maintains a weak collection of all instances on the class.
    """
    if issubclass(cls, Announcer):
        cls.__new__ = AnnouncingClassMethod(cls.__new__)
    
    instances = WeakKeyDictionary()
    if not hasattr(cls, prop):
        setattr(cls, prop, instances)
    
    def add_instance(_name, _cls, _instance, *args, **kw):
        getattr(_cls, prop)[_instance] = {}
    
    cls.__new__.listen(add_instance)
    return cls

@curry
def trackedinner(OuterCls, InnerCls, plural_prop=None, parent_prop=None, track_prop='instances'):
    """ Class decorator. Attributes this class's instances to the calling 
        OuterClass on instantiation, and keeps a collection of those inner
        instances on the outer instance.
        
        Applies both the innerclass and tracked decorators as well as its
        own.
        
        >>> class OuterFoo(object):
        ...   def __init__(self):
        ...     print "%s.__init__()" % self
        ...   def frob(self):
        ...     return InnerFoo()
        
        >>> class InnerFoo(object):
        ...   def __init__(self):
        ...     print "%s.__init__()" % self
        ...
        ... InnerFoo = trackedinner(OuterFoo, InnerFoo)
        ...
        ... o1 = OuterFoo()
        ... f1 = o1.frob()
        ... assert len(o1.innerfoos) == 1
        ... 
        ... o2 = OuterFoo()
        ... f2 = o2.frob()
        ... assert len(o2.innerfoos) == 1
        ... f3 = o1.frob()
        ... assert len(o1.innerfoos) == 2
        ... 
        ... del f2
        ... assert len(o1.innerfoos) == 2
        ... assert len(o2.innerfoos) == 0
    """
    parent_prop = parent_prop or OuterCls.__name__.lower()
    # XXX: write pluralize()
    plural_prop = plural_prop or InnerCls.__name__.lower()+'s'
    
    wrapped_outer_init = OuterCls.__init__
    def outer_init(self, *args, **kw):
        if not hasattr(self, plural_prop):
            setattr(self, plural_prop, WeakKeyDictionary())
        wrapped_outer_init(self, *args, **kw)
    OuterCls.__init__ = wraps(wrapped_outer_init)(outer_init)
    
    wrapped_inner_init = InnerCls.__init__
    def inner_init(self, *args, **kw):
        getattr(getattr(self, parent_prop), plural_prop)[self] = {}
        wrapped_inner_init(self, *args, **kw)
    InnerCls.__init__ = wraps(wrapped_inner_init)(inner_init)
    
    InnerCls = tracked(innerclass(OuterCls, InnerCls, prop=parent_prop), prop=track_prop)
    return InnerCls


