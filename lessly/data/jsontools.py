#!/usr/bin/env python
# -*- coding: utf-8 -*-

import anyjson
from anyjson import force_implementation, dumps, loads
force_implementation('jsonlib2')



import json
from collections import OrderedDict

ordered_decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)

class OrderedJSONDecoder(json.JSONDecoder):
    """ As `JSONDecoder`, but passing `collections.OrderedDict`
        for `object_pairs_hook` by default.
    """
    
    def __init__(self,
            encoding=None,
            object_hook=None,
            parse_float=None,
            parse_int=None,
            parse_constant=None,
            strict=True,
            object_pairs_hook=OrderedDict
    ):
        super(OrderedJSONDecoder, self).__init__(
                encoding=encoding,
                object_hook=object_hook,
                parse_float=parse_float,
                parse_int=parse_int,
                parse_constant=parse_constant,
                strict=strict,
                object_pairs_hook=object_pairs_hook
            )
        
    


