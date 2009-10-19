__all__ = ('Announcer', 'AnnouncingMethod', 'AnnouncingClassMethod')
from collections import defaultdict
from types import MethodType, FunctionType
from functools import wraps
from lessly.actor.publisher import Multicaster, Publisher
from lessly.fn import curry
from lessly.fn.method import methodize, find_in_mro

def nop(*args, **kw): pass

def announce_method(method):
    instance = method.__self__
    def wrapper(self, *args, **kw):
        result = method(*args, **kw)
        self.fire( *('call:'+method.__name__,self,result)+args, **kw )
        return result
    return MethodType(wraps(method)(wrapper), instance, type(instance))

EXCLUDED_ATTRS = ('__init__', 
    '__getattribute__', '__setattr__', '__delattr__', 
    'listeners', 'listen', 'listenAll', 'unlisten', 'unlistenAll', 'fire')

class MetaAnnouncer(type):
    def __new__(mcs, name, bases, cls_dict):
        cls_dict['cls_listeners'] = defaultdict(Multicaster) # Class listeners copied to each instance.
        return type.__new__(mcs, name, bases, cls_dict)
    

class Announcer(Publisher):
    """ Mixin which decorates all methods to publish their invocation as events.
    """
    __metaclass__ = MetaAnnouncer
    
    __del__ = nop
    
    def __init__(self):
        Publisher.__init__(self)
        props = dir(self)
        
        for k in props:
            v = getattr(self, k)
            if isinstance(v, MethodType) and k not in EXCLUDED_ATTRS:
                # print 'Decorating %s=%s (%s) as Announcer...' % (k, v, type(v))
                setattr(self, k, announce_method(v))
        
        self.fire('call:__init__', self)
    
    def fire(self, event, *data, **kwdata):
        """ Broadcasts an event to all registered listeners with supplied data.
        """
        self.listeners[event].fire(event, *data, **kwdata)
        self.listeners[None].fire(event, *data, **kwdata)
        self.cls_listeners[event].fire(event, *data, **kwdata)
        self.cls_listeners[None].fire(event, *data, **kwdata)
    
    def __setattr__(self, attr, value):
        if attr not in EXCLUDED_ATTRS:
            self.fire('set:'+attr, self, attr, value )
        object.__setattr__(self, attr, value)
    
    def __delattr__(self, attr):
        if attr not in EXCLUDED_ATTRS:
            self.fire('del:'+attr, self, attr ) 
        object.__delattr__(self, attr)
    
    @classmethod
    def listenAll(cls, event, listener):
        cls.cls_listeners[event].listen(listener)
    
    @classmethod
    def unlistenAll(cls, event, listener):
        cls.cls_listeners[event].unlisten(listener)


