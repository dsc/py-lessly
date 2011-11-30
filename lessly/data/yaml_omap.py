#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ('yaml', 'OrderedDict',)

import yaml
from yaml import *
from yaml.constructor import BaseConstructor, Constructor, SafeConstructor, ConstructorError
from yaml.representer import BaseRepresenter, Representer, SafeRepresenter
import collections

try:
    # included in standard lib from Python 2.7
    from collections import OrderedDict
except ImportError:
    # try importing the backported drop-in replacement
    # it's available on PyPI
    from ordereddict import OrderedDict




def construct_ordered_mapping(self, node, deep=False):
    if not isinstance(node, yaml.MappingNode):
        raise ConstructorError(None, None, "expected a mapping node, but found %s" % node.id, node.start_mark)
    
    mapping = OrderedDict()
    for key_node, value_node in node.value:
        key = self.construct_object(key_node, deep=deep)
        
        if not isinstance(key, collections.Hashable):
            raise ConstructorError("while constructing a mapping", node.start_mark, "found unhashable key", key_node.start_mark)
        
        value = self.construct_object(value_node, deep=deep)
        mapping[key] = value
    
    return mapping

BaseConstructor.construct_mapping = construct_ordered_mapping


def construct_yaml_map_with_ordered_dict(self, node):
    data = OrderedDict()
    yield data
    value = self.construct_mapping(node)
    data.update(value)

for t in [u'tag:yaml.org,2002:map', u'tag:yaml.org,2002:omap']:
    SafeConstructor.add_constructor( t, construct_yaml_map_with_ordered_dict )
    Constructor.add_constructor( t, construct_yaml_map_with_ordered_dict )
    yaml.add_constructor( t, construct_yaml_map_with_ordered_dict )


def represent_ordered_mapping(self, tag, mapping, flow_style=None):
    value = []
    node = yaml.MappingNode(tag, value, flow_style=flow_style)
    best_style = True
    
    if self.alias_key is not None:
        self.represented_objects[self.alias_key] = node
    
    if hasattr(mapping, 'items'):
        mapping = list(mapping.items())
    
    for item_key, item_value in mapping:
        node_key = self.represent_data(item_key)
        node_value = self.represent_data(item_value)
        if not (isinstance(node_key, yaml.ScalarNode) and not node_key.style):
            best_style = False
        if not (isinstance(node_value, yaml.ScalarNode) and not node_value.style):
            best_style = False
        value.append((node_key, node_value))
    if flow_style is None:
        if self.default_flow_style is not None:
            node.flow_style = self.default_flow_style
        else:
            node.flow_style = best_style
    
    return node


BaseRepresenter.represent_mapping = represent_ordered_mapping
SafeRepresenter.add_representer(OrderedDict, SafeRepresenter.represent_dict)
Representer.add_representer(OrderedDict, SafeRepresenter.represent_dict)
yaml.add_representer(OrderedDict, SafeRepresenter.represent_dict)

