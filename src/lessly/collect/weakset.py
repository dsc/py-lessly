import weakref

class WeakSet(set):
    """A set which holds its elements weakly."""
    
    def __init__(self, iterable=()):
        super(WeakSet, self).__init__(iterable)
    

