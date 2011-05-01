
class Ordering(object):
    """ Ordering mixin.
        Including classes must implement either:
         * __cmp__ or
         * __eq__ and one of __lt__ or __gt__
        
        Failure to do so will result in an infinite loop. A metaclass could check,
        or we could all just not be dumb.
    """
    
    def __cmp__(self, o):
        return ( 0 if self.__eq__(o) else
               (-1 if self.__lt__(o) else 1 ))
    
    def __eq__(self, o):
        return self.__cmp__(o) == 0
    
    def __lt__(self, o):
        return self.__cmp__(o) == -1
    
    def __gt__(self, o):
        return self.__cmp__(o) == 1
    
    def __ne__(self, o):
        return not self.__eq__(o)
    
    def __ge__(self, o):
        return self.__cmp__(o) != -1
    
    def __le__(self, o):
        return self.__cmp__(o) != 1


