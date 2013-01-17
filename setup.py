#! python
from setuptools import setup, find_packages

setup(
    name             = 'lessly',
    description      = 'Convenience tools: sometimes useful, oft inscrutable, certainly educational.',
    version          = '0.1.0',
    
    author           = 'David Alan Schoonover',
    author_email     = 'dsc@less.ly',
    
    packages         = find_packages(),
    install_requires = [
        'path        >= 2.2',
        'bunch       >= 1.0',
        'PyYAML      >= 3.10',
        'markdown    >= 2.1.0',
        'lxml        >= 2.3',
        'pyquery     >= 1.1',
        'jsonlib2    >= 1.5.2',
        'anyjson     >= 0.3.1',
        "colorama    >= 0.2.4",
    ],
    zip_safe         = False,
    license          = 'MIT',
)
