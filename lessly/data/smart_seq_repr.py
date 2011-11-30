import yaml


class YAMLObject(yaml.YAMLObject):
    """
    An object that can dump itself to a YAML stream
    and load itself from a YAML stream.
    """
    
    yaml_tag = None
    yaml_flow_style = None
    
    @classmethod
    def from_yaml(cls, loader, node):
        """ Convert a representation node to a Python object. """
        return loader.construct_yaml_object(node, cls)
    
    @classmethod
    def to_yaml(cls, dumper, data):
        """ Convert a Python object to a representation node. """
        return dumper.represent_yaml_object(cls.yaml_tag, data, cls,
                flow_style=cls.yaml_flow_style)
    


class YamlSmartSeqRepresenter(object):
    """ Creates sequence nodes with inline style when they have few elements,
        but create them with flow style when they're bigger.
        
        Wait, isn't this what default_flow_style=None does with some exceptions?
    """
    
    def __init__(self, max_inline=2):
        self.max_inline = max_inline
    
    def __call__(self, dumper, data):
        tag = u'tag:yaml.org,2002:seq'
        flow_style = None
        
        return dumper.represent_sequence(tag, data, flow_style)
    



def install(max_inline=2):
    smartr = YamlSmartSeqRepresenter(max_inline)
    yaml.add_representer(list, smartr)
    yaml.add_multi_representer(list, smartr)
    
