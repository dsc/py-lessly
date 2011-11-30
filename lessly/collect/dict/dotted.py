from functools import wraps
from lessly.symbol import NULL

__all__ = ('get_dotted', 'set_dotted', 'del_dotted', 'has_dotted',)


def key_to_list(fn):
    @wraps(fn)
    def wrapper(o, key, *args, **kwargs):
        key = key.split('.') if isinstance(key, basestring) else list(key)
        return fn(o, key, *args, **kwargs)
    return wrapper

@key_to_list
def get_dotted(o, key, default=None):
    """ Gets a potentially nested key (dot-separated) from the dict.
    """
    if not isinstance(o, dict):
        raise TypeError("Cannot get_dotted on a non-dict! Got: o=%r (%s)" % (o, type(o).__name__))
    
    if not key: return default
    k = key.pop(0)
    
    try:
        # reached the end of the lookup chain
        if not key: return o.get(k, default)
        
        # throws KeyError when missing
        v = o[k]
        
        # continue lookup chain
        if isinstance(v, dict):
            return get_dotted(v, key, default)
        # chain not exhausted, but we can't go on!
        else:
            return default
    
    # missing link in chain
    except KeyError:
        return default

@key_to_list
def set_dotted(o, key, value):
    """ Sets a key-value pair in the dict interpreting a dot-separated key
        as a series of nested dictionaries, created as necessary.
    """
    if not isinstance(o, dict):
        raise TypeError("Cannot set_dotted on a non-dict! Got: o=%r (%s)" % (o, type(o).__name__))
    
    if not key: return
    k = key.pop(0)
    
    # reached the end of the lookup chain
    if not key:
        o[k] = value
        return
    
    # fetch next dict, creating any missing links and bulldozing any non-dict values
    if isinstance(o.get(k), dict):
        v = o[k]
    else:
        v = o[k] = Bunch()
    
    set_dotted(v, key, value)


@key_to_list
def del_dotted(o, key, default=NULL):
    """ Deletes a potentially nested key (dot-separated) from the dict.
    """
    if not isinstance(o, dict):
        raise TypeError("Cannot del_dotted on a non-dict! Got: o=%r (%s)" % (o, type(o).__name__))
    
    if not key: return default
    k = key.pop(0)
    
    try:
        # reached the end of the lookup chain
        if not key:
            v = o.get(k, default)
            del o[k]
            return v
        
        # throws KeyError when missing
        v = o[k]
        
        # continue lookup chain
        if isinstance(v, dict):
            return del_dotted(v, key, default)
        # chain not exhausted, but we can't go on!
        else:
            return default
    
    # missing link in chain
    except KeyError:
        return default


@key_to_list
def has_dotted(o, key):
    """ Tests whether a series of nested dicts contain a dot-separated key.
    """
    if not isinstance(o, dict):
        raise TypeError("Cannot has_dotted on a non-dict! Got: o=%r (%s)" % (o, type(o).__name__))
    v = get_dotted(o, key, NULL)
    return v is not NULL



