import yaml

def toyaml(*records, **kw):
    if kw: records += (kw,)
    # SafeDumper will not emit python/foo tags for unicode or objects
    return yaml.safe_dump_all(records, indent=4) # default_flow_style=False, explicit_start=True


DEFAULT_OPTIONS = {
    'indent' : 4,
    # 'default_flow_style' : False,
    # 'explicit_start' : True,
}

def write_yaml(*records, **options):
    options = merge({}, DEFAULT_OPTIONS, options)
    return yaml.safe_dump_all(records, **options)


from path import path
from yaml.representer import Representer, SafeRepresenter
SafeRepresenter.add_representer(path, SafeRepresenter.represent_unicode)
SafeRepresenter.add_multi_representer(path, SafeRepresenter.represent_unicode)

Representer.add_representer(path, Representer.represent_unicode)
Representer.add_multi_representer(path, Representer.represent_unicode)
