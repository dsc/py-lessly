from functools import wraps
from lessly.fn import curry
from types import MethodType

__all__ = ('methodize', 'find_in_mro',)

@curry
def methodize(_callable, instance, cls=None, wrap=None):
    "Circumvents the fact that non-function callables are not converted to instance methods."
    
    def wrapper(*args, **kw):
        return wrapper._callable(*args, **kw)
    
    for name in dir(_callable):
        m = getattr(_callable, name)
        if callable(m) and not name.startswith('__'):
            setattr(wrapper, name, getattr(_callable, name))
    wrapper._callable = _callable
    
    m = wraps(wrap)(wrapper) if wrap else wrapper
    return MethodType(m, instance, cls or type(instance))



def find_in_mro(name, o, exclude=None):
    """ Recursively looks up the value of the attribute `name` in the object's class's MRO.
        Note that this implies the object itself is not searched. (If you wanted that, just
        use `getattr`.)
    """
    if not exclude: exclude = tuple()
    mro = o.mro() if isinstance(o, type) else type(o).mro()
    for cls in mro:
        if cls not in exclude and __dict__ in cls and name in cls.__dict__ and cls.__dict__[name] not in exclude:
            return cls.__dict__[name]
    return None


