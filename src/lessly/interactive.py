import types

def deepreload(module, stack=None):
    stack = stack or set()
    for k, v in module.__dict__.iteritems():
        if isinstance(v, types.ModuleType):
            if v in stack:
                module.__dict__[k] = v
            else:
                stack.add(v)
                module.__dict__[k] = deepreload(v, stack)
    return reload(module)