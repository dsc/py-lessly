#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ('profile',)

import time, functools, textwrap
import numpy as np

from pprint import pprint


class profile(object):
    """ Profiling data. """
    func   = None
    times  = None
    _array = None
    
    
    def __init__(self, func):
        self.func  = func
        functools.update_wrapper(self, func)
        self.reset()
    
    def reset(self):
        self.times = []
        self._array = None
        return self
    
    def __call__(self, *args, **kwargs):
        start   = time.time()
        result  = self.func(*args, **kwargs)
        elapsed = time.time() - start
        self.times.append( elapsed * 1000 )
        self._array = None
        return result
    
    def __len__(self):
        return len(self.times)
    
    @property
    def count(self): return len(self.times)
    
    @property
    def max(self): return max(self.times)
    
    @property
    def min(self): return min(self.times)
    
    @property
    def extent(self): return [self.min, self.max]
    
    @property
    def mean(self): return np.mean( self.array )  # float(sum(self.times)) / len(self.times)
    
    @property
    def std(self): return np.std( self.array )
    
    @property
    def var(self): return np.var( self.array )
    
    @property
    def array(self):
        if self._array is None: self._array = np.array(self.times)
        return self._array
    
    
    def histogram(self, bins=8, density=False):
        return np.histogram(self.array, bins=bins, density=density)
    
    
    def spark(self, hist, bounds):
        # ticks = '▁ ▂ ▃ ▄ ▅ ▆ ▇ █'.split()
        ticks = u'\u2581 \u2582 \u2583 \u2584 \u2585 \u2586 \u2587 \u2588'.split()
        
        mn, mx = min(hist), max(hist)
        scale  = ((mx - mn) << 24) / 23
        scaled = [ ((int(h) - mn) << 24) / scale for h in hist ]
        
        # pprint(locals())
        cols = [
                [
                    ( ticks[-1]       if top > (i * 8)        else
                    ( ticks[top/3]    if top > ((i-1) * 8)    else
                    ( ticks[0]        if top == 0 and i == 1  else u'  ' )))
                        for i in xrange(1, 4)
                ]
                for top in scaled
            ]
        rows = [ row for row in zip(*map(reversed, cols)) ]
        
        # chart = u'\n'.join( u' '.join(row) for row in rows )
        # print chart
        
        return rows, cols
    
    
    def summary(self, bins=8, density=False):
        name, count  = self.__name__, self.count
        mean, std    = self.mean, self.std
        
        hist, bounds = self.histogram(bins, density)
        rows, cols   = self.spark(hist, bounds)
        chart        = (u'\n\t').join( u' '.join(row) for row in rows )
        
        rowLen       = len(u' '.join(rows[0])) - 3
        labels       = u' '.join([
            u'{: >9.2f}'.format( bounds[0] ),
            u'{: ^{rowLen}.2f}'.format( bounds[(len(bounds)-1)/2], rowLen=rowLen ),
            u'{:.2f}'.format( bounds[-1] )
        ])
        
        s = textwrap.dedent(u"""
                {name}() called {count} times
                
                \t{chart}
                {labels}
                
                  mean: {mean: >10.3f}ms
                  \u03C3:   {std: >10.3f}ms
            """).format(**locals())
        
        return s
    





