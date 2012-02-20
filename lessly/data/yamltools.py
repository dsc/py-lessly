#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ('DEFAULT_OPTIONS', 'toyaml', 'write_yaml', 'PPDumper', 'ppyaml',)

import yaml
from lessly.collect.tools import merge

DEFAULT_OPTIONS = {
    'indent' : 4,
    # 'default_flow_style' : False,
    # 'explicit_start' : True,
}

def toyaml(*records, **kw):
    if kw: records += (kw,)
    # SafeDumper will not emit python/foo tags for unicode or objects
    return yaml.safe_dump_all(records, **DEFAULT_OPTIONS)

def write_yaml(*records, **options):
    options = merge({}, DEFAULT_OPTIONS, options)
    return yaml.safe_dump_all(records, **options)


from path import path
from yaml.representer import Representer, SafeRepresenter
SafeRepresenter.add_representer(path, SafeRepresenter.represent_unicode)
SafeRepresenter.add_multi_representer(path, SafeRepresenter.represent_unicode)

Representer.add_representer(path, Representer.represent_unicode)
Representer.add_multi_representer(path, Representer.represent_unicode)


import types
from yaml import Dumper, SafeDumper

class PPDumper(SafeDumper, Dumper):
    pass

# PPDumper.add_representer(unicode, SafeDumper.represent_unicode)
# PPDumper.add_representer(types.ClassType, Dumper.represent_name)
# PPDumper.add_representer(types.FunctionType, Dumper.represent_name)
# PPDumper.add_representer(types.BuiltinFunctionType, Dumper.represent_name)
# PPDumper.add_representer(types.ModuleType, Dumper.represent_module)
# PPDumper.add_multi_representer(types.InstanceType, Dumper.represent_instance)
# PPDumper.add_multi_representer(object, Dumper.represent_object)
PPDumper.add_multi_representer(dict, PPDumper.represent_dict)

def ppyaml(*records, **kw):
    if kw: records += (kw,)
    print yaml.dump_all(records, Dumper=PPDumper, **DEFAULT_OPTIONS)

