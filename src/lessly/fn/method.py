from functools import wraps
from lessly.fn import curry
from types import MethodType

@curry
def methodize(_callable, instance, cls=None, wrap=None):
    "Circumvents the fact that callables are not converted to instance methods."
    def wrapper(*args, **kw):
        return wrapper._callable(*args, **kw)
    
    for name in dir(_callable):
        m = getattr(_callable, name)
        if callable(m) and not name.startswith('__'):
            setattr(wrapper, name, getattr(_callable, name))
    wrapper._callable = _callable
    
    m = wraps(wrap)(wrapper) if wrap else wrapper
    return MethodType(m, instance, cls or instance.__class__)
