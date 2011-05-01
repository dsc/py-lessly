from utils.basis import iter

class DotDict(dict):
    def __init__(self, obj={}, **kw):
        super(DotDict, self).__init__(
            dict( (k, DotDict.fromdict(v)) for (k,v) in iter(obj) ),
            **dict( (k, DotDict.fromdict(v)) for (k,v) in kw.iteritems() ))
    
    def __getattr__(self, attr):
        return self.get(attr, None)
    
    __delattr__ = dict.__delitem__
    
    def __setattr__(self, k, v):
        return dict.__setitem__( self, k, DotDict.fromdict(v) )
    
    
    def copy(self):
        return DotDict(**super(DotDict, self).copy())
    
    
    @staticmethod
    def fromdict(d):
        if hasattr(d,'__class__') and d.__class__ is dict:
            return DotDict(d)
        else:
            return d
    

