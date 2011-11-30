import time
import datetime
import calendar
from collections import Mapping

__all__ = (
    'dstDelta',
    'timetuples', 'mkdatetime', 'mktimestamp', 'timestamp',
    'TimeInterval', 'Duration', 'seconds',
)


def dstDelta():
    "Returns the timedelta representing the DST offset from the localtime."
    return datetime.timedelta(seconds=0 if not time.daylight else (time.timezone - time.altzone))


STRUCT_TIME_FIELDS = ('year', 'month', 'mday', 'hour', 'min', 'sec', 'wday', 'yday', 'isdst')

def timetuples(*tts, **kw):
    """ timetuples(*tts, year=None, month=None, mday=None, hour=None, min=None, sec=None, wday=None, yday=None, isdst=None)
        
        Merge the given tuples (including time.struct_time), first to last skipping None-valued indices, and
        finally overriding with keyword args whenever not None. Missing values are set to 0 (including 
        tm_wday, tm_yday, and tm_isdst irrespective of the specified date).
    """
    out = [0] * 9
    for tt in tts:
        for idx, v in enumerate(tt):
            if v is not None:
                out[idx] = v
    for idx, name in enumerate(STRUCT_TIME_FIELDS):
        v = kw.get(name, None)
        if v is not None:
            out[idx] = v
    return time.struct_time(out)



def mkdatetime(t):
    "Returns a datetime as parsed by timestamp()"
    return datetime.datetime.fromtimestamp(timestamp(t))

def mktimestamp(year, month, day, hour=0, minute=0, second=0, microsecond=0, is_dst=-1, tzinfo=None):
    "Returns seconds since the epoch for given datetime components."
    if tzinfo:
        tt = datetime.datetime(year, month, day, hour, minute, second, microsecond, tzinfo).timetuple()
    else:
        tt = time.struct_time(year, month, day, hour, minute, second, microsecond, is_dst)
    return time.mktime(tt)

def timestamp(t, *args, **kw):
    """ Converts a value to a unix timestamp represented by a float, accepting:
        (a) Arguments:
            
            year, month, day, [hour, [minute, [second, [microsecond, [is_dst=-1, [tzinfo]]]]]]
            
            Missing values replaced with 0, excepting is_dst and tzinfo.
        (b) A single value to convert:
            - datetime, time.struct_time, int, long, float, double: cast to float without interpolation
            - string: converted using time.strptime
            - datetime.time: as timestamp with year, month, and day from time.localtime(0)
            - datetime.date: as datetime.datetime(year, month, day)
            - tuple, list, dict: expanded and then converted again
    """
    if len(args) > 1 or (args and 'month' in kw) or ('month' in kw and 'day' in kw):
        return mktimestamp(t, *args, **kw)
    
    if isinstance(t, basestring):
        ts = time.strptime(t)
    elif isinstance(t, time.struct_time):
        ts = time.mktime(t) # calendar.timegm(t) if t[8] is 0 else time.mktime(t)
    elif isinstance(t, Mapping):
        ts = timestamp(**t)
    elif isinstance(t, (list, tuple)):
        ts = timestamp(*t)
    elif isinstance(t, (datetime.datetime, datetime.date)):
        ts = timestamp(t.timetuple())
    elif isinstance(t, datetime.time):
        lt = time.localtime(0) # start at epoch
        ts = timestamp(lt.tm_year, lt.tm_mon, lt.tm_mday, t.hour, t.minute, t.second, t.microsecond, t.tzinfo)
    else:
        ts = t
    return float(ts)

INTERVALS = [
    ('year',    31449600.0),
    ('week',    604800.0),
    ('day',     86400.0),
    ('hour',    3600.0),
    ('minute',  60.0)
]

def seconds(seconds=0, minutes=0, hours=0, days=0, weeks=0, years=0, **kv):
    "Returns the number (float) of seconds represented by the date/time fragments provided."
    for (name, unit) in INTERVALS:
        seconds += float(kv.get(name, 0.0) or locals()['%ss' % name]) * unit
    return float(seconds)


class Duration(object):
    """ Represents a duration of time. 
    """
    
    def __init__(self, start, end=None, show_ms=False):
        """ Creates a time interval from start and end values. All input values 
            are cast using mkdatetime(). If end is omitted, it is assumed to 
            be now().
        """
        self.start = mkdatetime(start)
        self.end   = mkdatetime(end or datetime.datetime.now())
        self.seconds = timestamp(self.end) - timestamp(self.start)
        self.show_ms = show_ms
    
    def __contains__(self, t):
        """ Tests whether a datetime is in the interval.
        """
        return self.start < mkdatetime(t) < self.end
    
    def __cmp__(self, t):
        "Tests whether a datetime is before, after, or in the interval."
        t = mkdatetime(t)
        return (-1 if t < self.start else
                (1 if t > self.end   else 0))
    
    def __str__(self):
        i = self.seconds
        out = []
        
        for (name, unit) in INTERVALS:
            if i >= unit:
                units = (i // unit)
                i -= units * unit
                out.append("%i %s%s" % (units, name, 's' if units > 1 else ''))
        
        if i:
            out.append(("%.3f second%s" if self.show_ms else "%i second%s") % (i, 's' if i > 1.0 else ''))
        
        return ' '.join(out)

# Backwards compat
TimeInterval = Duration
