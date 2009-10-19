
class NumericMixin(object):
    """Infers [sub, ...] from add, neg, """
    
    def __sub__(self, other):
        return self + -other
    

class NumericValMixin(object):
    """Infers much more by assuming the existence of a __val__ property."""
    
    
    # math
    def __add__(self, other):
        return self.__val__ + other
    
    def __radd__(self, other):
        return self.__val__ + other
    
    def __neg__(self):
        return -self.__val__
    
    def __sub__(self, other):
        return self.__val__ + -other
    
    def __rsub__(self, other):
        return -self.__val__ + other
    
    def __mul__(self, other):
        return self.__val__ * other
    
    def __rmul__(self, other):
        return self.__val__ * other
    
    def __div__(self, other):
        return self.__val__ / other
    
    def __rdiv__(self, other):
        return self.__val__ / other
    
    def __floordiv__(self, other):
        return self.__val__ // other
    
    def __rfloordiv__(self, other):
        return self.__val__ // other
    
    def __abs__(self):
        return abs(self.__val__)
    
    def __floordiv__(self, other):
        return self.__val__ // other
    
    def __nonzero__(self):
        return self.__val__ != 0
    
    # comp
    def __eq__(self, other):
        return self.__val__ == other
    
    def __lt__(self, other):
        return self.__val__ < other
    
    def __cmp__(self, other):
        return  ( 0 if self.__val__ == other else
                 -1 if self.__val__  < other else 1)
    



