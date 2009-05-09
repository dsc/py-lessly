__all__ = ('Multicaster', 'Publisher')
import collections, itertools


class Multicaster(list):
    "A simple multicaster."
    
    def __init__(self):
        list.__init__(self)
    
    def listen(self, listener):
        self.append(listener)
    
    def unlisten(self, listener):
        try:
            self.remove(listener)
        except ValueError: pass
    
    def fire(self, *data, **kwdata):
        for listener in self[:]:
            listener(data, kwdata)
    
    def __str__(self):
        return "<%s len=%s>" % (self.__class__.__name__, len(self))

class Publisher(object):
    "A multi-channel multicaster."
    
    def __init__(self):
        self.listeners = collections.defaultdict(Multicaster)
    
    def listen(self, event, listener):
        """ Registers a listener to be notified of an event. Listener must be 
            callable, and will be invoked with:
            
            listener(event, *data, **kwdata)
            
            Subscribing to event=None notifies listener of all events.
        """
        self.listeners[event].listen(listener)
    
    def unlisten(self, event, listener):
        """ Removes a registered listener.
        """
        self.listeners[event].unlisten(listener)
    
    def fire(self, event, *data, **kwdata):
        """ Broadcasts an event to all registered listeners with supplied data.
        """
        self.listeners[event].fire(event, *data, **kwdata)
        self.listeners[None].fire(event, *data, **kwdata)
    
    def __str__(self):
        return "<%s events=%s>" % (self.__class__.__name__, len(self.listeners))



