
class AttributeProxy(object):
    
    def __init__(self, proxy_to):
        self._proxy_to = proxy_to
    
    @property
    def _proxy_target(self):
        return getattr(self, self._proxy_to)
    
    # only called if k not found in normal places 
    def __getattr__(self, k):
        return getattr(self._proxy_target, k)
    
    def __setattr__(self, k, v):
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
            object.__setattr__(self, k, v)
        except AttributeError:
            setattr(self._proxy_target, k, v)
    
    def __delattr__(self, k):
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
            object.__delattr__(self, k)
        except AttributeError:
            delattr(self._proxy_target, k)
    

