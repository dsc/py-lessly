import stackless, weakref
from abc import abstractmethod, ABCMeta
from collections import Sequence

class Actor(object):
    """ Implements the Actor model using Stackless.
    """
    __metaclass__ = ABCMeta
    
    def __init__(self, *args, **kw):
        self.queue = stackless.channel()
        
        actor = weakref.ref(self)
        def _tasklet():
            try:
                while actor():
                    args, kw = actor().queue.receive()
                    actor().receive(*args, **kw)
            except AttributeError: pass
        
        stackless.tasklet( _tasklet )()
    
    
    @abstractmethod
    def receive(self, *args, **kw):
        "Receives all messages sent to this actor."
        pass
    
    def __rrshift__(self, msg):
        "Sends a message to this object: (args, kw) >> actor"
        try:
            args, kw = msg
            args = args if isinstance(args, Sequence) else [args]
            self.send(*args, **kw) # exception implies kw is not a map
        except:
            msg = msg if isinstance(msg, Sequence) else [msg]
            self.queue.send( (msg, {}) )
    
    def send(self, *args, **kw):
        self.queue.send( (args, kw) )
    


