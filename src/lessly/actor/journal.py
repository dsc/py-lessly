from functools import wraps
from actor import Actor
from abc import abstractmethod, ABCMeta
from types import FunctionType, MethodType, UnboundMethodType



def methodize(_callable, wrap=None):
    "Circumvents the fact that callables are not converted to instance methods."
    def wrapper(*args, **kw):
        return wrapper._callable(*args, **kw)
    
    for name, m in _callable.__class__.__dict__.iteritems():
        if callable(m) and not name.startswith('__'):
            setattr(wrapper, name, getattr(_callable, name))
    wrapper._callable = _callable
    
    if wrap:
        return wraps(wrap)(wrapper)
    else:
        return wrapper


class PublisherMethod(object):
    """ A wrapped method from a Publisher object.
    """
    
    def __init__(self, method):
        self.method = method
        self.listeners = set()
    
    def listen(self, actor):
        "Registers an actor to be notified when the method is called."
        if not isinstance(actor, Actor):
            raise TypeError('listen() requires an actor: %s' % actor)
        self.listeners.add(actor)
    
    def unlisten(self, actor):
        "Removes a registered actor."
        self.listeners.discard(actor)
    
    def fire(self, msg):
        "Broadcasts a message to all registered listeners."
        for listener in self.listeners:
            msg >> listener
    
    def __call__(self, *args, **kw):
        # print "%s --> %s( self=%s, *%r, **%r )" % (self, self.method.__name__, args[0], args[1:], kw)
        self.fire( ((self.method.__name__,)+args, kw) )
        return self.method(*args, **kw)



Publisher = None

class MetaPublisher(ABCMeta):
    """ Metaclass for Publishers, wrapping their methods to publish events.
    """
    
    def __new__(mcls, name, bases, cls_dict):
        if Publisher is not None:
            def nop(self, *args, **kw): pass
            
            # ensure important methods
            for k in ('__init__', '__del__'):
                if k not in cls_dict:
                    cls_dict[k] = nop
            
            for k, v in cls_dict.iteritems():
                if callable(v):
                    cls_dict[k] = methodize(PublisherMethod(v), v)
        
        return ABCMeta.__new__(mcls, name, bases, cls_dict)


class Publisher(Actor):
    """ An abstract actor which publishes events.
    """
    __metaclass__ = MetaPublisher
    
    def __init__(self, *args, **kw):
        Actor.__init__(self)
    

# 
# class FooPub(Publisher):
#     def __init__(self):
#         super(FooPub, self).__init__()
#     
#     def receive(self, *args, **kw):
#         print "%s.receive( *%r, **%r )" % (self, args, kw)
#     
#     def lol(self, *args, **kw):
#         print 'lol'
# 
# 
# 
