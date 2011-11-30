# try: # pragma: no cover
#     __import__('pkg_resources').declare_namespace(__name__)
# except ImportError: # pragma: no cover
#     __import__('pkgutil').extend_path(__path__, __name__)


import lessly.misc
from .misc import *

import lessly.collect
from .collect.tools import (
    cons, items, iteritems, merge,
    pluck, pluckattr, xpluck, xpluckattr, invoke, xinvoke,
    find, uniqued,
)
from .collect.dict import *
# from .collect.dict.bunchbunch import *

# import lessly.fn
# from .fn import curry, compose, starcompose
from compose import curry, compose, starcompose

import lessly.dates
from .dates import timestamp

from .data import csvtools as csv
# csv = lessly.csvtools

import lessly.cli
import lessly.cli.options
from .cli.options import FileType

