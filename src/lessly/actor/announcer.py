__all__ = ('AnnouncingMethod', 'AnnouncingClassMethod', 'Announcer')
from types import MethodType
from lessly.actor.publisher import Multicaster, Publisher
from lessly.fn.method import methodize

def nop(self, *args, **kw): pass

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
        self.fire( ((name,instance,result)+args, kw) )
        return result

class AnnouncingClassMethod(Multicaster):
    """ A wrapped class method from a Announcer object.
    """
    
    def __init__(self, method):
        self.method  = method
        self.name    = name
        Multicaster.__init__(self)
    
    def __call__(self, cls, *args, **kw):
        # print "%s --> %s( self=%s, *%r, **%r )" % (self, self.method.__name__, args[0], args[1:], kw)
        name = self.name or self.method.__name__
        result = self.method(cls, *args, **kw)
        self.fire( ((name,cls,result)+args, kw) )
        return result

class Announcer(object):
    """ An abstract actor which publishes events.
        
        If you implement __new__ in your class, be sure to call 
        Announcer.__new__(YourCls) to setup the Multicaster there.
    """
    
    __new__ = AnnouncingClassMethod(type.__new__)
    
    def __init__(self):
        props = dir(self)
        
        for k in props:
            v = getattr(self, k)
            if isinstance(v, MethodType):
                # print 'Decorating %s=%s (%s) as Announcer...' % (k, v, type(v))
                setattr(self, k, methodize( AnnouncingMethod(v), self, wrap=v ))
    
    __del__ = nop

