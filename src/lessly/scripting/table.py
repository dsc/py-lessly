""" Formats data as a table of monospace, plain-text rows / columns.
"""

from collections import Mapping
from itertools import repeat

from lessly.collect import merge


def mkFieldMap(fields, args=[], kwargs={}, default=None):
    base = dict(zip(fields, repeat(default)))
    if isinstance(args, Mapping):
        args = [args]
    if args:
        if len(args) == 1:
            first = args[0]
            if isinstance(first, Mapping):
                return merge(base, kwargs, first)
            elif isinstance(first, basestring):
                args = first.strip().split()
            else:
                args = first
        base.update( zip(fields, args)[:len(args)] )
    return merge(base, kwargs)


class FieldBearer(object):
    fields = tuple()
    
    def mkFieldMap(self, args=[], kwargs={}, default=None):
        return mkFieldMap(self.fields, args, kwargs, default)
    
    def __repr__(self):
        return '%s(fields=%r)' % (self.__class__.__name__, self.fields)



class MonospaceTable(FieldBearer, list):
    """ Formats data as a monospace-aligned table for plain-text output.
    """
    _done_header = False
    
    
    def __init__(self, fields, head_fmt=None, row_fmt=None):
        """ `fields` : str | iterable
            Ordered list of field-names for columns. If str, trimmed and split on whitespace.
            
            `head_fmt` : sequence | mapping | TableHeadFormatter [optional]
            Ordered list or (fieldname,fmt) mapping of format-strings for header-columns.
            
            `row_fmt` : sequence | mapping | TableRowFormatter [optional]
            Ordered list or (fieldname,fmt) mapping of format-strings for each row's columns.
        """
        if isinstance(fields, basestring):
            fields = fields.strip().split()
        
        self.fields = fields
    
    def head(self):
        pass
    
    def append(self, *args, **kwargs):
        list.append(self, self.mkFieldMap(args, kwargs))
    
    def __repr__(self):
        return '%s(fields=%r, rows=%s)' % (self.__class__.__name__, self.fields, len(self))
    
    def __str__(self):
        return ''
    
    
    


class TableRowFormatter(FieldBearer):
    
    def __init__(self, fields, fmts, spacing=2):
        self.fields = fields
        self.spacing = spacing
        
        if isinstance(fmts, basestring):
            fmts = fmts.strip().split()
        self.fmt = (' '*spacing).join(fmts)
    
    def mkMaxLens(self, maxlens=0):
        if isinstance(maxlens, Mapping):
            return maxlens
        if isinstance(maxlens, int):
            maxlens = self.mkFieldMap(default=maxlens)
        elif isinstance(maxlens, (list, set)):
            maxlens = self.mkFieldMap(maxlens)
        return dict( (k+'len', v) for k, v in maxlens.iteritems() )
    
    def format(self, args=[], kwargs={}, maxlens=0, default=None):
        maxlens = self.mkMaxLens(maxlens)
        values  = self.mkFieldMap(args, kwargs, default)
        return self.fmt.format(**merge(maxlens, values))
    


class TableHeadFormatter(TableRowFormatter):
    """ Represents a monospace table header. """
    
    def __init__(self, fields, spacing=2):
        fmts = [ '{%(f)s: ^{%(f)slen}}' % {'f':f} for f in fields ]
        super(TableHeadFormatter, self).__init__(fields, fmts, spacing)
    
    def format(self, args=[], kwargs={}, maxlens=0, default=None):
        maxlens = self.mkMaxLens(maxlens)
        row = super(TableHeadFormatter, self).format(args, kwargs, maxlens, default)
        return row + '\n' + (' '*self.spacing)

