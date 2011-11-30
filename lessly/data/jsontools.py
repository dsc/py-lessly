#!/usr/bin/env python
# -*- coding: utf-8 -*-

# look into universaljson on pypi
# dump, load for both


USE_DEMJSON = False

if USE_DEMJSON:
    import demjson
    
    def fromjson(txt, cls=None):
        if cls:
            return demjson.decode(txt, strict=False, cls=cls)
        else:
            return demjson.decode(txt, strict=False)
    
    def tojson(obj):
        return demjson.encode(obj, strict=False)
    
    JSONDecodeError = demjson.JSONDecodeError
else:
    try:
        import cjson as json
    except ImportError:
        import json
    
    def fromjson(txt, strict=False):
        return json.loads(txt)
    
    def tojson(obj, strict=False):
        return json.dumps(obj)
    
    JSONDecodeError = ValueError


