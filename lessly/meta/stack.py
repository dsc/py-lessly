import logging
log = logging.getLogger('rpg')

import inspect, weakref
from contextlib import contextmanager

from proxy import AttributeProxy
from lessly.meta.managed import InnerClass

class StackFrame(AttributeProxy):
    """ Context manager for a frame on the stack. Provides convenience for 
        chaining frames and prevents leaks due to reference cycles.
    """
    weakframe = None
    frame = None
    
    def __init__(self, frame=None):
        super(StackFrame, self).__init__('frame')
        self.weakframe = weakref.ref(frame or inspect.currentframe().f_back)
    
    def cleanup(self, *args, **kw):
        try:
            del self.frame
        finally:
            self.frame = None
    
    def previous(self):
        "Moves up to the previous frame in the stack."
        if self.frame:
            f_back = StackFrame(self.frame.f_back)
            if f_back:
                try:
                    self.cleanup()
                    self.frame = f_back
                    return self
                finally:
                    del f_back
            else:
                return None
        else:
            raise ReferenceError("Can only traverse the stack in a context block!")
    
    def locals(self):
        return self.frame.f_locals
    
    def globals(self):
        return self.frame.f_globals
    
    def code(self):
        return self.frame.f_code
    
    ### Context Manager Protocol ###
    
    def __enter__(self):
        self.frame = self.weakframe()
        return self
    
    __exit__ = cleanup
    __del__ = cleanup
    

def find_calling_instance(Type):
    frame = inspect.currentframe().f_back
    try:
        while frame:
            for v in frame.f_locals.values():
                if isinstance(v, Type):
                    return v
                # elif issubclass(type(v), InnerClass):
                #     log.debug('InnerClass detected while looking for %s: <%s at 0x%x>...' % (Type, type(v).__name__, id(v)))
                #     for attr in dir(v):
                #         inner = getattr(v, attr, None)
                #         if isinstance(inner, Type):
                #             log.debug('--> success! %s' % inner)
                #             return inner
                
            frame = frame.f_back
    finally:
        del frame
