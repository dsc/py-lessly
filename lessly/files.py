import fileinput, os
from path import path

__all__ = ('Tee', 'next_filename', 'mkdirp',)


class Tee(object):
    """ Write to multiple files at once.
    """
    
    def __init__(self, *files):
        self.files = files
    
    def __iter__(self):
        return fileinput.FileInput(self.files)
    
    def xpluck(self, attr, default=None):
        for f in self.files:
            yield getattr(f, name, default)
    
    def pluck(self, attr, default=None):
        return list(self.pluck(attr, default))
    
    def xinvoke(self, name, *args, **kwargs):
        for f in self.files:
            yield getattr(f, name)(*args, **kwargs)
    
    def invoke(self, name, *args, **kwargs):
        return list(self.invoke(name, *args, **kwargs))
    
    def write(self, data):
        self.invoke('write', data)
    
    def flush(self):
        self.invoke('flush')
    
    def close(self):
        self.invoke('close')
    
    @property
    def first(self):
        return self.files[0]
    
    @property
    def closed(self):
        return any(self.xpluck('closed'))
    
    @property
    def encoding(self):
        return self.first.encoding
    
    @property
    def name(self):
        return self.first.name
    
    def __repr__(self):
        return 'Tee(%s)' % ', '.join(repr(name) for name in self.xpluck('name'))
    


def next_filename(name, path=os.getcwd()):
    """ Takes a filename with one printf-style slot to be filled with an integer 
        and returns the filename with the slot filled incrementally to the next 
        free name.
    """
    names = os.listdir(path)
    i = 0
    while os.path.exists(name % i):
        i += 1
    return name % i

def mkdirp(dirpath):
    "Makes all intermediate directories and path only if they do not exist."
    dirpath = path(dirpath)
    if not dirpath.exists():
        dirpath.makedirs()
    return dirpath

