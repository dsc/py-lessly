#! python
from setuptools import setup, find_packages

setup(
    name = "lessly",
    version = "0.0.1",
    package_dir = {'': 'src'},
    packages = ["lessly", "lessly.actor", "lessly.fn", "lessly.collect", "lessly.meta"],
    
    author = "David Schoonover",
    author_email = "dsc@less.ly",
    description = "A collection of useful tools.",
    long_description = """A collection of useful tools.""",
    url = "http://tire.less.ly/hacking/lib",
    
    zip_safe = False,
    
    classifiers = [
        'awesome'
    ],
)

