import re, lxml, pyquery

NS_PAT = re.compile(r'xmlns="[^"]+" ?', re.I)

class DOM(pyquery.PyQuery):
    
    def __init__(self, *args, **kwargs):
        selector = context = None
        
        if len(args) == 1:
            context = args[0]
            args_head = tuple()
            args_tail = args[1:]
        elif len(args) >= 2:
            selector, context = args[:2]
            args_head = (selector,)
            args_tail = args[3:]
        
        # we delete the namespace, otherwise selectors don't work
        if isinstance(context, basestring):
            context, n = NS_PAT.subn('', context)
        
        args = args_head + (context,) + args_tail
        pyquery.PyQuery.__init__(self, *args, **kwargs)
    
    def iter(self):
        # Iterate by index, or face infinite recursion!
        for i in xrange(len(self)):
            el = self[i]
            if isinstance(el, (lxml.etree._Element, lxml.etree.ElementBase)):
                yield DOM(el)
            else:
                yield el
        
        raise StopIteration()
    
    def eq(self, idx):
        return DOM(self[idx])
    
    @classmethod
    def fromFile(Cls, f):
        return Cls(lxml.html.parse(f).getroot())
    
    @classmethod
    def fromPath(Cls, path):
        return Cls.fromFile(txt)
    
