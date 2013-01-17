#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys, argparse, colorama
from colorama import Fore, Back, Style

__all__ = ('Script',)
ERROR = '%sError:%s ' % (Fore.RED, Style.RESET_ALL)

def add_colors(d):
    for color in 'BLACK BLUE CYAN GREEN MAGENTA RED WHITE YELLOW RESET'.split():
        d.setdefault(color, getattr(Fore, color))
    for style in 'BRIGHT DIM NORMAL RESET_ALL'.split():
        d.setdefault(style, getattr(Style, style))
    return d



class Script(object):
    "Scripting base class."
    verbose = True
    parser = None
    
    
    def __init__(self, *args, **options):
        self.__dict__.update(**options)
        self.__args__    = args
        self.__options__ = options
    
    
    def log(self, message, *args, **kwargs):
        "Log a message to stderr if verbose."
        _end      = kwargs.pop('_end', '\n')
        _outfile  = kwargs.pop('_outfile', sys.stderr)
        _is_error = kwargs.pop('_is_error', False)
        
        if self.verbose or _is_error:
            kwargs.setdefault('self', self)
            msg = (ERROR if _is_error else '') + message.format(*args, **kwargs) + Style.RESET_ALL
            print(msg, end=_end, file=_outfile)
        return True
    
    def error(self, message, *args, **kwargs):
        "Log a non-fatal error to stderr. (For fatal errors, just raise.)"
        kwargs.setdefault('_is_error', True)
        return self.log(message, *args, **kwargs)
    
    
    def run(self):
        raise Exception('Script.run() is not implemented!')
    
    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)
    
    
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
    def create(cls, *args, **overrides):
        values = cls.parse(*args, **overrides)
        return cls(**values)
    
    @classmethod
    def main(cls, *args, **overrides):
        return cls.create(*args, **overrides)() or 0
    
    


