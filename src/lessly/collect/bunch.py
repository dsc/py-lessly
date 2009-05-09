from collect import items

class Bunch(dict):
    """ A dictionary that provides attribute-style access.
    """
    
    def __repr__(self):
        keys = self.keys()
        keys.sort()
        args = ', '.join(['%s=%r' % (key, self[key]) for key in keys])
        return '%s(%s)' % (self.__class__.__name__, args)
    
    def __contains__(self, k):
        try:
            return hasattr(self, k) or dict.__contains__(self, k)
        except:
            return False
    
    # only called if k not found in normal places 
    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)
    
    def __setattr__(self, k, v):
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
            object.__setattr__(self, k, v)
        except:
            try:
                self[k] = v
            except:
                raise AttributeError(k)
    
    def __delattr__(self, k):
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
            object.__delattr__(self, k)
        except:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)
    


class BunchBunch(Bunch):
    """ A dictionary that provides attribute-style access and
        recursively setting dot-separated keys.
    """
    
    def __init__(self, __d=None, **kv):
        dict.__init__(self)
        self.update(__d, **kv)
    
    def setdotted(self, key, value):
        """ Sets a key-value pair in the dict interpreting a dot-separated key
            as a series of nested dictionaries, created as necessary.
        """
        try:
            k, rest = key.split('.',1)
            if not isinstance(self.get(k), BunchBunch):
                self[k] = BunchBunch()
                self[k].setdotted(rest, value)
        except ValueError:
            self[key] = BunchBunch(value) if isinstance(value, dict) else value
    
    def update(self, __d, **kv):
        "Accepts any number of dictionaries, and interprets dotted keys recursively."
        for k,v in items(__d,kv):
            self.setdotted(k,v)
        return self
    
    def deepcopy(self):
        c = self.copy()
        for k, v in c.iteritems():
            if hasattr(v, 'deepcopy') and callable(v.deepcopy):
                c[k] = v.deepcopy()
            elif isinstance(v, dict):
                c[k] = v.copy()
        return c
    
    def copy(self):
        return BunchBunch( dict.copy(self) )

