from functools import wraps
from lessly.compose import curry

@curry
def methodize(_callable, wrap=None):
    "Circumvents the fact that callables are not converted to instance methods."
    def wrapper(*args, **kw):
        return wrapper._callable(*args, **kw)
    
    for name, m in _callable.__class__.__dict__.iteritems():
        if callable(m) and not name.startswith('__'):
            setattr(wrapper, name, getattr(_callable, name))
    wrapper._callable = _callable
    
    if wrap:
        return wraps(wrap)(wrapper)
    else:
        return wrapper
