""" Very miscellaneous but useful functions.
"""

__all__ = ('bin_size', 'displaymatch', 'decodekv')


def bin_size(i):
    "Number of bits needed to represent the absolute value of i."
    return len(bin(abs(i))) - 2


def displaymatch(match):
    "Pretty printers regex matches."
    if match is None:
        return None
    return '<Match: %r, groups=%r>' % (match.group(), match.groups())


from urllib import unquote_plus
def decodekv(s):
    "As urlparse.parse_qs, but preserves empty keys."
    return dict( map(unquote_plus, pair.split('=')) for pair in s.split('&') )

