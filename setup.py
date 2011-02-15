#!/usr/bin/env python
# encoding: utf-8

import os
import re

from distutils.core import setup

rel_file = lambda *args: os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

def read_from(filename):
    fp = open(filename)
    try:
        return fp.read()
    finally:
        fp.close()

def get_long_description():
    return read_from(rel_file('README.md'))

def get_version():
    data = read_from(rel_file('pInstagram.py'))
    return re.search(r"__version__ = '([^']+)'", data).group(1)


setup(    
    name             = 'pInstagram',
    author           = 'Mattias Gunneras',
    author_email     = 'mattias@breakfastny.com',
    description      = 'pInstagram is an API client for Instagram',
    long_description = get_long_description(),
    install_requires = 'restclient',
    py_modules       = ['pInstagram'],
    url              = 'https://github.com/mgunneras/pInstagram',
    version          = get_version(),
    classifiers = [
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)