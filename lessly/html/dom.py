import pyquery, lxml

class DOM(pyquery.PyQuery):
    
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
    
    @staticmethod
    def from_file(f):
        return DOM(lxml.html.parse(f).getroot())
    
    @staticmethod
    def from_path(path):
        return DOM.from_file(open(path, 'rU'))
    
