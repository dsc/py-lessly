import sys, codecs, locale
import argparse

__all__ = ('FileType',)


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

