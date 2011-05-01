try:
    __import__('pkg_resources').declare_namespace(__name__)
except: pass

import lessly.misc
from lessly.misc import *

import lessly.collect
from lessly.collect.tools import items, merge, cons

import lessly.fn
from lessly.fn import curry, compose, starcompose
from lessly.dates import timestamp

import lessly.csvtools
csv = lessly.csvtools