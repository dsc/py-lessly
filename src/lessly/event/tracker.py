from weakref import WeakKeyDictionary
from actor import Actor
from publisher import Publisher

class Tracker(Actor, WeakKeyDictionary):
    "Weakly tracks the creation of a class's instances."
    
    def __init__(self, tracked_cls, *args, **kw):
        WeakKeyDictionary.__init__(self)
        Actor.__init__(self)
        tracked_cls.__init__.listen(self)
        # tracked_cls.__del__.listen(self)
        self.tracked_cls = tracked_cls
    
    def receive(self, method, instance, *args, **kw):
        print "Tracker.receive(method=%s, instance=%s, *%r, **%r)" % (method, instance, args, kw)
        if method == '__init__':
            self[instance] = {}
        elif method == '__del__':
            del self[instance]
    
    def __str__(self):
        return "<%s for %ss len=%s>" % (self.__class__.__name__, self.tracked_cls.__name__, len(self))

