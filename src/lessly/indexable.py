
class Indexable(object):
    def __contains__(self, k):
        return hasattr(self, k)
    
    def __getitem__(self, k):
        return getattr(self, k)
    
    def __setitem__(self, k, v):
        return setattr(self, k, v)

