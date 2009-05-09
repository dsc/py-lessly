from functools import wraps, partial
from publisher import Multicaster, Publisher
from abc import abstractmethod, ABCMeta
from types import MethodType, UnboundMethodType



def methodize(_callable, instance, cls=None, wrap=None):
    "Circumvents the fact that callables are not converted to instance methods."
    def wrapper(*args, **kw):
        return wrapper._callable(*args, **kw)
    
    for name in dir(_callable):
        m = getattr(_callable, name)
        if callable(m) and not name.startswith('__'):
            setattr(wrapper, name, getattr(_callable, name))
    wrapper._callable = _callable
    
    m = wraps(wrap)(wrapper) if wrap else wrapper
    return MethodType(m, instance, cls or instance.__class__)


class AnnouncingMethod(Multicaster):
    """ A wrapped method from a Journal object.
    """
    
    def __init__(self, method):
        self.method = method
        Multicaster.__init__(self)
    
    def __call__(self, *args, **kw):
        # print "%s --> %s( self=%s, *%r, **%r )" % (self, self.method.__name__, args[0], args[1:], kw)
        self.fire( ((self.method.__name__,)+args, kw) )
        return self.method(*args, **kw)



Announcer = None

class MetaAnnouncer(ABCMeta):
    """ Metaclass for Journals, wrapping their methods to publish events.
    """
    
    def __new__(mcls, name, bases, cls_dict):
        if Announcer is not None:
            def nop(self, *args, **kw): pass
            
            # ensure important methods
            for k in ('__init__', '__del__'):
                if k not in cls_dict:
                    cls_dict[k] = nop
            
            for k, v in cls_dict.iteritems():
                if callable(v):
                    cls_dict[k] = methodize(AnnouncingMethod(v), v)
        
        return ABCMeta.__new__(mcls, name, bases, cls_dict)


class Announcer(object):
    """ An abstract actor which publishes events.
    """
    
    def __init__(self):
        props = dir(self)
        
        # ensure important methods
        if '__del__' not in props:
            def nop(self, *args, **kw): pass
            self.__del__ = methodize(nop, self)
        
        for k in props:
            v = getattr(self, k)
            print k, v, type(v)
            if isinstance(v, MethodType):
                setattr(self, k, methodize( AnnouncingMethod(v), self, wrap=v ))


class FooPub(Announcer):
    
    def receive(self, *args, **kw):
        print "%s.receive( *%r, **%r )" % (self, args, kw)
    

