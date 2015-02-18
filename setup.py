# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 16:42:51 2015

@author: kerpowski
"""

from distutils.core import setup
from Cython.Build import cythonize
import numpy

sourcefiles = ['ChessLib.py', 'ChessAI.py']

compiler_directives={#'profile': True,
                     'boundscheck': False,
                     'cdivision': True,
                     'language_level':3}
                     

ext_modules = cythonize(sourcefiles, compiler_directives=compiler_directives)

setup(
    name = 'Make Chess Fast',
    ext_modules = ext_modules,
    include_dirs=[numpy.get_include()]
)