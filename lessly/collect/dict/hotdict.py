#!/usr/bin/env python
# -*- coding: utf-8 -*-

class HotDict(dict):
    limit   = None
    hotlist = None
    
    def __init__(self, limit):
        super(HotDict, self).__init__()
        self.limit = limit
        self.hotlist = []
    
    def __setitem__(self, k, v):
        if len(self) >= self.limit:
            del self[self.hotlist[0]]
        del self[k]
        self.hotlist.append(k)
        dict.__setitem__(self, k, v)
    
    def setdefault(self, k, d):
        if k in self:
            return self[k]
        else:
            self[k] = d
            return d
    
    def __delitem__(self, k):
        if k in self:
            self.hotlist.remove(k)
            dict.__delitem__(self, k)
    
    def get_top(self, n):
        return [ (k, self[k]) for k in self.hotlist[:n] ]
