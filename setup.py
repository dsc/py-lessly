#! python
from setuptools import setup, find_packages

setup(
    name = "lessly",
    version = "0.0.1",
    description = "A collection of tools I find useful.",
    long_description = """ A collection of tools I find useful. """,
    url = "http://tire.less.ly/hacking/lib",
    
    author = "David Schoonover",
    author_email = "dsc@less.ly",
    
    packages=find_packages('.', exclude=['ez_setup']),
    # entry_points={
    #     'console_scripts': ['lessly = lessly:main']
    # },
    install_requires=[
        "bunch>=1.0",
    ],
    keywords = [],
    classifiers = [],
    zip_safe = True,

)
