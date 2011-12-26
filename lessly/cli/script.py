#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, argparse


class Script(object):
    "Base class for scripts."
    
    def __init__(self, *args, **options):
        self.__dict__.update(**options)
        self.__options__ = options
    
    def __call__(self):
        return 0
    
    def __repr__(self):
        return '{self.__class__.__name__}(options={self.__options__!r})'.format(self=self)
    
    def __str__(self):
        return repr(self)
    
    
    @classmethod
    def parse(cls, *args, **overrides):
        parsed = cls.parser.parse_args(args or None)
        values = dict(**parsed.__dict__)
        values.update(overrides)
        return values
    
    @classmethod
    def main(cls, *args, **overrides):
        values = cls.parse(*args, **overrides)
        return cls(**values)() or 0
    


