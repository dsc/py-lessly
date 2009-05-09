import time
import datetime
from collections import Mapping


def mkdatetime(t):
    "Returns a datetime as parsed by timestamp()"
    return datetime.datetime.fromtimestamp(timestamp(t))

def mktimestamp(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None):
    "Returns seconds since the epoch for a datetime."
    return time.mktime(datetime.datetime(year, month, day, hour, minute, second, tzinfo).timetuple())

def timestamp(t, *args, **kw):
    """ Converts a value to a unix timestamp represented by a float, accepting:
        (a) Arguments:
            
            year, month, day, [hour, [minute, [second, [microsecond, [tzinfo]]]]]
            
            Missing values replaced with 0s.
        (b) A single value to convert:
            - string: converted using time.strptime
            - tuple, list, dict: converted using lessly.dates.timestamp()
            - datetime.time: as timestamp with year, month, and day from time.localtime(0)
            - datetime.date: as datetime.datetime(year, month, day)
            - datetime, int, long, float, double: no interpolation
    """
    if len(args) > 1 or (args and 'month' in kw) or ('month' in kw and 'day' in kw):
        return mktimestamp(t, *args, **kw)
    
    if isinstance(t, basestring):
        ts = time.strptime(t)
    elif isinstance(t, Mapping):
        ts = timestamp(**v)
    elif isinstance(t, (list, tuple)):
        ts = timestamp(*v)
    elif isinstance(t, datetime.time):
        lt = time.localtime(0)
        ts = timestamp(lt.tm_year, lt.tm_mon, lt.tm_mday, t.hour, t.minute, t.second, t.microsecond, t.tzinfo)
    elif isinstance(t, (datetime.datetime, datetime.date)):
        ts = time.mktime(t.timetuple())
    else:
        ts = t
    return float(ts)


class TimeInterval(object):
    """ Represents an interval of time between two datetimes.
    """
    
    def __init__(self, start, end=None):
        """ Creates a time interval from start and end values. All input values 
            are cast using mkdatetime(). If end is omitted, it is assumed to 
            be now().
        """
        self.start = mkdatetime(start)
        self.end   = mkdatetime(end)
    
    def __contains__(self, t):
        """ Tests whether a datetime is in the interval.
        """
        return self.start < mkdatetime(t) < self.end
    
    def __cmp__(self, t):
        "Tests whether a datetime is before, after, or in the interval."
        t = mkdatetime(t)
        return (-1 if t < self.start else
                (1 if t > self.end   else 0))

