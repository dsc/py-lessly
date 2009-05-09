# meh


@curry
def trackedclass(OuterType, InnerType, prop_instances=None, prop_outer=None, on_new=None):
    """ Automatically (weakly) tracks instances of the inner class on the instance 
        of the outer class.
    """
    if prop_outer is None:
        prop_outer = OuterType.__name__.lower()
    if prop_instances is None:
        prop_instances = InnerType.__name__.lower() + 's'
    
    # Create the instances-set on init
    @wrap_method(OuterType, name='__init__')
    def tracked_init_m(self, *args, **kw):
        setattr(self, prop_instances, WeakSet())
        tracked_init_m._wrapped(self, *args, **kw)
    
    # Add new instance to managing class
    @wrap_method(InnerType, name='__init__')
    def tracked_init(self, *args, **kw):
        outer = getattr(self, prop_outer)
        getattr(outer, prop_instances).add(self)
        tracked_init._wrapped(self, *args, **kw)
    
    return innerclass(OuterType, InnerType, prop_outer)



class Bar(object):
    def __init__(self):
        print "Bar.__init__()"
    
    def mkfoo(self):
        return Foo()

@trackedclass(Bar)
class Foo(object):
    def __init__(self):
        print "Foo.__init__()"

