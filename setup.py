#! python
from setuptools import setup, find_packages

setup(
    name             = 'lessly',
    version          = '0.0.1',
    
    author           = 'David Alan Schoonover',
    author_email     = 'dsc@less.ly',
    
    packages         = find_packages('.', exclude=['ez_setup']),
    install_requires = [
        'bunch    >= 1.0',
        'PyYAML   >= 3.10',
        'markdown >= 2.1.0',
        'lxml     >= 2.3',
        'pyquery  >= 1.1',
    ],
    zip_safe         = True,
)
