from abc import abstractmethod, ABCMeta
from collections import Sequence

class Actor(object):
    """ Implements the Actor model.
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def receive(self, *args, **kw):
        "Receives all messages sent to this actor."
        pass
    
    def __rrshift__(self, msg):
        "Sends a message to this object: (args, kw) >> actor"
        try:
            args, kw = msg
            args = args if isinstance(args, Sequence) else [args]
            self.receive(*args, **kw)
        # exception implies kw is not a map
        except TypeError:
            msg = msg if isinstance(msg, Sequence) else [msg]
            self.receive( (msg, {}) )
    


