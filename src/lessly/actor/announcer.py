__all__ = ('Announcer', 'AnnouncingMethod', 'AnnouncingClassMethod')
from types import MethodType, FunctionType
from functools import wraps
from lessly.actor.publisher import Multicaster, Publisher
from lessly.fn.method import methodize, find_in_mro

Announcer = None
def nop(*args, **kw): pass

# class AnnouncingProperty(Multicaster):
#     """ A wrapped property from an Annoucer object.
#     """
#     
#     def __init__(self, value=None, fget=None, fset=None, fdel=None, doc=None):
#         L = locals()
#         if isinstance(value, property):
#             for name in ('fget', 'fset', 'fdel'):
#                 L[name] = L[name] or getattr(value, name)
#         else:
#             self.value = value
#         
#         self.__doc__ = doc or fget.__doc__ if fget else ""
#         for name in ('fget', 'fset', 'fdel'):
#             if L[name]:
#                 setattr(self, name, L[name])
#     
#     def fget(self):
#         return self.value
#     
#     def __get__(self, instance, owner):
#         value = self.fget()
#         self.fire( instance, value )
#         return value
#     
#     def fset(self, value):
#         self.value = value
#     
#     def __set__(self, instance, value ):
#         self.fire( instance, value )
#         self.fset(value)
#     
#     def fdel(self):
#         del self.value
#     
#     def __delete__(self, instance):
#         self.fire( instance, value )
#         self.fdel(value)


class AnnouncingMethod(Multicaster):
    """ A wrapped method from a Announcer object.
    """
    
    def __init__(self, method):
        self.method = method
        Multicaster.__init__(self)
    
    def __call__(self, instance, *args, **kw):
        # print "%s --> %s( self=%s, *%r, **%r )" % (self, self.method.__name__, args[0], args[1:], kw)
        name = self.method.__name__
        result = self.method(*args, **kw)
        self.fire( *(name,instance,result)+args, **kw )
        return result

class AnnouncingClassMethod(Multicaster):
    """ A wrapped class method from a Announcer object.
    """
    
    def __init__(self, method):
        self.method = method
        Multicaster.__init__(self)
    
    def __call__(self, cls, *args, **kw):
        # print "%s --> %s( self=%s, *%r, **%r )" % (self, self.method.__name__, args[0], args[1:], kw)
        name = self.method.__name__
        if name == '__new__':
            result = self.method(cls)
        else:
            result = self.method(cls, *args, **kw)
        self.fire( *(name,cls,result)+args, **kw )
        return result

class MetaAnnouncer(type):
    def __new__(mcls, name, bases, cls_dict):
        cls = type.__new__(mcls, name, bases, cls_dict)
        
        if not isinstance(cls.__new__, AnnouncingClassMethod):
            cls.__new__ = wraps(cls.__new__)(AnnouncingClassMethod(cls.__new__))
        
        # cls._getter  = find_in_mro('__getattribute__', cls, Announcer) or object.__getattribute__
        cls._setter  = find_in_mro('__setattr__', cls, Announcer) or object.__setattr__
        cls._deleter = find_in_mro('__delattr__', cls, Announcer) or object.__delattr__
        
        return cls


EXCLUDED_ATTRS = ('__getattribute__', '__setattr__', '__delattr__', 'listeners', 'listen', 'unlisten', 'fire')

class Announcer(Publisher):
    """ Mixin which decorates all methods to publish their invocation as events.
        
        If you implement __new__ in your class, be sure to call 
        Announcer.__new__(YourCls) to setup the Multicaster there.
    """
    __metaclass__ = MetaAnnouncer
    
    __del__ = nop
    
    def __init__(self):
        props = dir(self)
        Publisher.__init__(self)
        
        for k in props:
            v = getattr(self, k)
            if isinstance(v, MethodType) and k not in EXCLUDED_ATTRS:
                # print 'Decorating %s=%s (%s) as Announcer...' % (k, v, type(v))
                setattr(self, k, methodize( AnnouncingMethod(v), self, wrap=v ))
    
    # def __getattribute__(self, attr):
    #     cls = type(self)
    #     value = cls._getter(self, attr)
    #     cls.fire(self, 'get:'+attr, self, attr, value )
    #     return value
    
    def __setattr__(self, attr, value):
        cls = type(self)
        if attr not in EXCLUDED_ATTRS:
            cls.fire(self, 'set:'+attr, self, attr, value )
        cls._setter(self, attr, value)
    
    def __delattr__(self, attr):
        cls = type(self)
        if attr not in EXCLUDED_ATTRS:
            cls.fire(self, 'del:'+attr, self, attr )
        cls._deleter(self, attr)
    


