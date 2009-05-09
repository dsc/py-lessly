""" The recipes from the itertools docs in the Python Std Lib
"""
from itertools import *

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def enumerate(iterable, start=0):
    return izip(count(start), iterable)

def tabulate(function, start=0):
    "Return function(0), function(1), ..."
    return imap(function, count(start))

def nth(iterable, n):
    "Returns the nth item or empty list"
    return list(islice(iterable, n, n+1))

def quantify(iterable, pred=bool):
    "Count how many times the predicate is true"
    return sum(imap(pred, iterable))

def padnone(iterable):
    """ Returns the sequence elements and then returns None indefinitely.
        Useful for emulating the behavior of the built-in map() function.
    """
    return chain(iterable, repeat(None))

def ncycles(iterable, n):
    "Returns the sequence elements n times"
    return chain.from_iterable(repeat(iterable, n))

def dotproduct(vec1, vec2):
    return sum(imap(operator.mul, vec1, vec2))

def flatten(listOfLists):
    return list(chain.from_iterable(listOfLists))

def repeatfunc(func, times=None, *args):
    """Repeat calls to func with specified arguments.

    Example:  repeatfunc(random.random)
    """
    if times is None:
        return starmap(func, repeat(args))
    return starmap(func, repeat(args, times))

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    for elem in b:
        break
    return izip(a, b)

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))

def powerset(iterable):
    "powerset('ab') --> set([]), set(['a']), set(['b']), set(['a', 'b'])"
    # Recipe credited to Eric Raymond
    pairs = [(2**i, x) for i, x in enumerate(iterable)]
    for n in xrange(2**len(pairs)):
        yield set(x for m, x in pairs if m&n)

def compress(data, selectors):
    "compress('ABCDEF', [1,0,1,0,1,1]) --> A C E F"
    return (d for d, s in izip(data, selectors) if s)

def combinations_with_replacement(iterable, r):
    "combinations_with_replacement('ABC', 3) --> AA AB AC BB BC CC"
    pool = tuple(iterable)
    n = len(pool)
    indices = [0] * r
    yield tuple(pool[i] for i in indices)
    while 1:
        for i in reversed(range(r)):
            if indices[i] != n - 1:
                break
        else:
            return
        indices[i:] = [indices[i] + 1] * (r - i)
        yield tuple(pool[i] for i in indices)
