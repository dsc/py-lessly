#!/usr/bin/env python
# encoding: utf-8

__all__ = ('Tracker')

from weakref import WeakKeyDictionary
from lessly.actor.actor import Actor
from lessly.actor.publisher import Publisher
from lessly.actor.announcer import Announcer, AnnouncingMethod, AnnouncingClassMethod

class Tracker(Actor, WeakKeyDictionary):
    """ Weakly tracks the creation of a class's instances.
        
        >>> class Foo(object): pass
        ... t = Tracker(Foo)
        ... f = Foo()
        ... assert len(t) == 1
        ... del f
        ... assert len(t) == 0
    """
    
    def __init__(self, tracked_cls):
        WeakKeyDictionary.__init__(self)
        self.tracked_cls = tracked_cls
        
        # Prepend Announcer if not present in class hierarchy
        if Announcer not in tracked_cls.__bases__:
            if '__new__' in tracked_cls.__dict__.keys():
                tracked_cls.__new__ = AnnouncingClassMethod(tracked_cls.__new__)
            tracked_cls.__bases__ = (Announcer,)+tracked_cls.__bases__
            
        
        # listen for new instances
        tracked_cls.__new__.listen(self.receive)
    
    def receive(self, method, instance, *args, **kw):
        print "Tracker.receive(method=%s, instance=%s, *%r, **%r)" % (method, instance, args, kw)
        if method == '__new__':
            self[instance] = {}
        elif method == '__del__':
            del self[instance]
    
    def __str__(self):
        return "<%s len=%s>" % (repr(self), len(self))
    
    def __repr__(self):
        return "%s(%s)" % (
            self.__class__.__name__, 
            self.tracked_cls.__name__)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
