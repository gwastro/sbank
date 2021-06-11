# -*- coding: utf-8 -#-
# Copyright (2021) Cardiff University (macleoddm@cardiff.ac.uk)

"""Build configuration for sbank
"""

import os, sys

from setuptools import setup, Extension

import numpy

from Cython.Build import cythonize

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"


# define cython options
cython_compile_args = [
    "-O3",
    "-w",
    "-ffast-math",
    "-ffinite-math-only",
    "-std=c99",
]
cython_directives = {
    "embedsignature": True,
    "language_level": 3,
}

# enable coverage for cython
if int(os.getenv("CYTHON_LINETRACE", "0")):
    cython_directives["linetrace"] = True
    cython_compile_args.append("-DCYTHON_TRACE")

# define compiled extensions
for curr_path in sys.path[::-1]:
    curr_dir = os.path.join(sys.path[-1], 'lalsuite.dylibs')
    print (curr_dir)
    if os.path.isdir(curr_dir):
        lalsuite_lib_dir = curr_dir
        break
exts = [
    Extension(
        "sbank.overlap_cpu",
        ["sbank/overlap_cpu.pyx"],
        include_dirs=[numpy.get_include()],
        library_dirs=[lalsuite_lib_dir],
        language="c",
        libraries=["lal"],
        extra_compile_args=cython_compile_args,
        extra_link_args=[],
    ),
]

# -- build the thing
# this function only manually specifies things that aren't
# supported by setup.cfg (as of setuptools-30.3.0)
setup(
    ext_modules=cythonize(exts, compiler_directives=cython_directives),
)
