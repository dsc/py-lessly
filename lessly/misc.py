""" Very miscellaneous but useful functions.
"""
import os, os.path, sys, subprocess, urlparse, re
from itertools import izip, izip_longest
from lessly.collect.tools import merge, walkmap

# backwards compat
from lessly.strings import trim, title_case
from lessly.data.yamltools import toyaml, ppyaml, write_yaml
from lessly.files import next_filename


__all__ = (
    'trim', 'title_case', 'next_filename', 
    'toyaml', 'ppyaml', 'write_yaml',
    'bin_size', 'bin_repr', 'bin_chunks', 'pack_fmt',
    'displaymatch', 
    'decodekv', 
    'stream',
    'keystringer',
    'check_output',
)


def bin_size(i):
    "Number of bits needed to represent the absolute value of i."
    return len(bin(abs(i))) - 2

def bin_chunks(b, size=8):
    bs = bin(b)[2:]
    while len(bs) % size != 0:
        bs = '0'+bs
    for chunk in izip(*([iter(bs)] * size)):
        yield ''.join(chunk)

def bin_repr(b, size=4, per_line=4):
    return '\n'.join(' '.join(tokens) for tokens in izip_longest( fillvalue='', *([iter(bin_chunks(b, size))] * per_line) ))

    # 
    # out = ''
    # line = []
    # for i, chunk in enumerate(bin_chunks(b, size=size)):
    #     line.append(chunk)
    #     if (i+1) % per_line == 0:
    #         out += ' '.join(line) + '\n'
    #         line = []
    # return out

FORMAT_SIZES = [ ('b', 4), ('h', 8), ('i', 16), ('l', 16), ('q', 32) ]
def pack_fmt(i, signed=True):
    """ Returns the smallest format-character from the struct module that will 
        accommodate the number i.
    """
    if isinstance(i, float):
        return 'f' if abs(i) < sys.maxint else 'd'
    else:
        size = bin_size(i)
        for fmt, fmtsize in FORMAT_SIZES:
            if size <= fmtsize:
                return fmt if signed else fmt.upper()
        raise ValueError("What did you doooo?")


def displaymatch(match):
    "Pretty printers regex matches."
    if match is None:
        return None
    return '<Match: %r, \n\tgroups=%r, \n\tgroupdict=%r>' % (match.group(), match.groups(), match.groupdict())


def decodekv(s, lists=False, keep_blank_values=True, strict_parsing=False):
    "As urlparse.parse_qs, but preserves empty keys by default and de-lists the dict."
    opt = dict(keep_blank_values=keep_blank_values, strict_parsing=strict_parsing)
    return urlparse.parse_qs(s, **opt) if lists else dict(urlparse.parse_qsl(s, **opt))



try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


def stream(txt=''):
    s = StringIO()
    s.write(txt)
    s.flush()
    s.seek(0)
    return s


def cxrange(start, end=None, step=1):
    if end is None:
        end = start
        start = 'a'
    for n in xrange(ord(start), ord(end), step):
        yield chr(n)

def crange(start, end=None, step=1):
    return list(cxrange(start, end, step))


# unicode keys in dicts look terrible when prettyprinted

def _keystringer(kv):
    if isinstance(kv, tuple):
        k,v = kv
        try:
            return (str(k), str(v) if isinstance(v, unicode) else (dict(v) if isinstance(v, dict) else v))
        except UnicodeEncodeError:
            print 'key: {k!r}\nvalue: {v!r}'.format(**locals())
            raise
    else:
        return kv

def keystringer(*records):
    rs = [ (walkmap(_keystringer, r) if isinstance(r, dict) else r) for r in records ]
    if len(records) == len(rs) == 1:
        return rs[0]
    else:
        return rs

try:
    from subprocess import check_output
except:
    # Ported from 2.7
    def check_output(*popenargs, **kwargs):
        """ Run command with arguments and return its output as a byte string.
        
        If the exit code was non-zero it raises a CalledProcessError.  The
        CalledProcessError object will have the return code in the returncode
        attribute and output in the output attribute.
        
        The arguments are the same as for the Popen constructor.  Example:
        
        >>> check_output(["ls", "-l", "/dev/null"])
        'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'
        
        The stdout argument is not allowed as it is used internally.
        To capture standard error in the result, use stderr=subprocess.STDOUT.
        
        >>> check_output(["/bin/sh", "-c",
                          "ls -l non_existent_file ; exit 0"],
                         stderr=subprocess.STDOUT)
        'ls: non_existent_file: No such file or directory\n'
        """
        if 'stdout' in kwargs:
            raise ValueError('stdout argument not allowed, it will be overridden.')
        process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
        output, unused_err = process.communicate()
        retcode = process.poll()
        if retcode:
            cmd = kwargs.get("args")
            if cmd is None:
                cmd = popenargs[0]
            raise subprocess.CalledProcessError(retcode, cmd)
        return output



if __name__ == '__main__':
    import doctest
    doctest.testmod()
