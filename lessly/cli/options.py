#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, codecs, locale
import argparse
from path import path


__all__ = ('FileType', 'PathType', 'DirectoryType', 'PathTypeError',)


class PathTypeError(TypeError):
    """ TypeError that provides `path` and `type` attributes tracking expectations. """
    
    def __init__(self, message, filepath, pathtype):
        super(PathTypeError, self).__init__(message, filepath, pathtype)
        self.message = message
        self.path    = filepath
        self.type    = pathtype



class FileType(argparse.FileType):
    """Factory for creating file object types
    
    Instances of FileType are typically passed as type= arguments to the
    ArgumentParser add_argument() method.
    
    Keyword Arguments:
        - mode='r' -- A string indicating how the file is to be opened. Accepts the
            same values as the builtin open() function.
        - encoding=None -- The file's encoding. None is treated as per the `codecs`
            module (as bytes).
        - errors='strict' -- Error handling as defined in the `codecs` module:
            'strict', 'ignore', 'replace', 'xmlcharrefreplace', 'backslashreplace'
        - bufsize=-1 -- The file's desired buffer size. Accepts the same values as
            the builtin open() function.
    """
    
    def __init__(self, mode='r', encoding=None, errors='strict', bufsize=-1):
        self._mode     = mode
        self._encoding = encoding
        self._errors   = errors
        self._bufsize  = bufsize
    
    def __call__(self, f):
        mode = self._mode
        enc = self._encoding
        
        # the special path "-" means sys.std{in,out}
        if f == '-':
            if 'r' in mode:
                f = '/dev/stdin'
                enc = enc or sys.stdin.encoding or locale.getpreferredencoding().lower()
            elif 'w' in mode:
                f = '/dev/stdout'
                enc = enc or sys.stdout.encoding or locale.getpreferredencoding().lower()
            else:
                msg = _('argument "-" with mode %r') % mode
                raise ValueError(msg)
        
        # all other paths are used as ... paths
        try:
            return codecs.open( f, mode=mode, encoding=enc or None,
                errors=self._errors, buffering=self._bufsize )
        except IOError as e:
            message = _("can't open '%s': %s")
            raise ArgumentTypeError(message % (f, e))
    
    def __repr__(self):
        args = self._mode, self._encoding, self._errors, self._bufsize
        args_str = ', '.join(repr(arg) for arg in args if arg != -1)
        return '%s(%s)' % (type(self).__name__, args_str)



class PathType(object):
    """ Factory for validating a path and wrapping it as a `path`.
        
        Keyword Arguments:
            - base=u'' -- Base path to resolve the passed path from.
            - mustExist=False -- Validate directory exists, raising OSError otherwise.
            - expand=True -- Expand the path.
            - abspath=False -- Resolve the absolute path.
    """
    base      = u''
    mustExist = True
    expand    = True
    abspath   = False
    
    
    def __init__(self, base=u'', mustExist=True, expand=True, abspath=False):
        self.base      = path(base)
        self.mustExist = mustExist
        self.expand    = expand
        self.abspath   = abspath
    
    
    def checkExists(self, p):
        if self.mustExist and not p.exists():
            raise OSError(2, 'No such file or directory', p)
        return p
    
    def __call__(self, p):
        p = self.base/p
        if self.expand:
            p = p.expand()
        if self.abspath():
            p = p.abspath()
        return self.checkExists(p)
    
    
    def __repr__(self):
        return "%s(%s)" % ( type(self).__name__, 
            ', '.join( '%s=%r' % (k,v) for k,v in self.__dict__.items() if not k[0] == '_' ) )
    


class DirectoryType(PathType):
    """ Factory for validating a directory path and wrapping it as a `path`.
    """
    mkdirs = True
    
    
    def __init__(self, base=u'', mkdirs=True, mustExist=False, expand=True, abspath=False):
        """ Factory for validating a directory path and wrapping it as a `path`. If a given
            path is not a directory, TypeError is raised.
            
            Keyword Arguments:
                - base=u'' -- Base path to resolve the passed path from.
                - mkdirs=True -- If directory does not exist, make it and all intermediary
                    directories.
                - mustExist=False -- Validate directory exists, raising OSError otherwise.
                - expand=True -- Expand the path.
                - abspath=False -- Resolve the absolute path.
        """
        super(DirectoryType, self).__init__(base, mustExist, expand, abspath)
        self.mkdirs = mkdirs
    
    
    def checkExists(self, p):
        if self.mkdirs and not p.exists():
            p.makedirs()
        if p.exists() and not p.isdir():
            raise PathTypeError('Path is not a directory', p, self)
        return super(PathType, self).checkExists(p)
    


